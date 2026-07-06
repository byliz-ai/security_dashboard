#!/usr/bin/env python3
"""
Security Intelligence Dashboard Generator
=========================================
Usage:
    python generate.py --scraped output/run_20260531_120000/scraped.json
    python generate.py --scraped output/run_20260531_120000/scraped.json --days 3
    python generate.py --scraped output/run_20260531_120000/scraped.json --run-dir output/run_20260531_120000

Country profiles, severity levels, regions, operational implications and
recommended actions are all built automatically from the scraped incidents.
A compact per-country daily count is retained in history.json (repo root) to
power the trend sparklines across runs.

Run pipeline.py instead of this script directly for the full automated workflow.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from collections import defaultdict

from data import COUNTRY_META, SOCIAL_MONITORS
from scraper import filter_incidents, build_country_profiles


# ── per-country sparkline history (last N days) ──────────────────────────────

# Durable rolling history: committed at the repo root so it survives across CI
# runs. output/ is gitignored and the workflow never commits site/runs/ back, so
# without this file every CI run rebuilt the trend chart from scratch and the
# sparklines were flat. Shape: {"Sudan": {"2026-07-06": 12, ...}, ...}
HISTORY_STORE = ROOT.parent / "history.json"


def _counts_from_incidents(incidents: list) -> dict:
    """Return {country: {date: count}} for a list of incident dicts."""
    daily = defaultdict(lambda: defaultdict(int))
    for inc in incidents or []:
        c = inc.get("country")
        d = (inc.get("date") or "")[:10]
        if c and d:
            daily[c][d] += 1
    return daily


def _merge_max(dst: dict, src: dict) -> None:
    """Merge src {country: {date: count}} into dst, keeping the max per date.
    max() (not +=) makes this idempotent: re-running the pipeline for the same
    day, or the same run showing up in multiple sources, never double-counts."""
    for country, days in src.items():
        bucket = dst.setdefault(country, {})
        for d, n in days.items():
            dd = d[:10]
            if dd:
                bucket[dd] = max(int(bucket.get(dd, 0)), int(n))


def _update_history_store(current_incidents: list, keep_days: int = 60) -> None:
    """Fold the current run's per-country daily counts into HISTORY_STORE,
    prune anything older than keep_days, and write it back. Never raises."""
    store: dict = {}
    if HISTORY_STORE.exists():
        try:
            loaded = json.loads(HISTORY_STORE.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                store = loaded
        except Exception:
            store = {}

    _merge_max(store, _counts_from_incidents(current_incidents))

    cutoff = (datetime.now(timezone.utc) - timedelta(days=keep_days)).strftime("%Y-%m-%d")
    for country in list(store.keys()):
        store[country] = {d: n for d, n in store[country].items() if d >= cutoff}
        if not store[country]:
            del store[country]

    try:
        HISTORY_STORE.write_text(
            json.dumps(store, indent=2, sort_keys=True, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as e:
        print(f"  ⚠  Could not write history store ({HISTORY_STORE}): {e}", file=sys.stderr)


def _load_history(window_days: int = 14, current_incidents: list = None) -> dict:
    """
    Build a per-country, per-day count map for sparklines from all available
    history sources, then slice the trailing N-day window ending today.

    Sources (merged with max() so none double-counts the others):
      1. HISTORY_STORE — durable rolling counts persisted across CI runs
      2. legacy run folders — local output/run_* and repo site/runs/run_*
      3. the current run's incidents (defensive; usually already in the store)

    Output: {"Sudan": [c0, c1, ..., c{N-1}], ...} where index 0 is the oldest
    day in the window and the last index is today.
    """
    repo_root = ROOT.parent
    daily: dict = {}   # {country: {date: count}}

    # 1. Durable rolling store (primary source across CI runs)
    if HISTORY_STORE.exists():
        try:
            store = json.loads(HISTORY_STORE.read_text(encoding="utf-8"))
            if isinstance(store, dict):
                _merge_max(daily, store)
        except Exception:
            pass

    # 2. Legacy run folders committed in the repo + local output dir (dev)
    seen_runs = set()
    for base in (ROOT / "output", repo_root / "site" / "runs"):
        if not base.exists():
            continue
        for run in base.glob("run_*"):
            if not run.is_dir() or run.name in seen_runs:
                continue
            seen_runs.add(run.name)
            ij = run / "incidents.json"
            if not ij.exists():
                continue
            try:
                items = json.loads(ij.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(items, list):
                _merge_max(daily, _counts_from_incidents(items))

    # 3. Current run (defensive — normally already folded into the store)
    if current_incidents:
        _merge_max(daily, _counts_from_incidents(current_incidents))

    # Build the trailing N-day window ending today
    today = datetime.now(timezone.utc).date()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(window_days - 1, -1, -1)]

    return {country: [counts.get(d, 0) for d in days]
            for country, counts in daily.items()}


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_scraped(path: Path) -> list:
    """Load a scraped JSON file (bare list or {incidents:[...]} dict)."""
    if not path.exists():
        print(f"  ⚠  File not found: {path}", file=sys.stderr)
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        items = raw.get("incidents", [])
    elif isinstance(raw, list):
        items = raw
    else:
        print(f"  ⚠  Unrecognised format: {path}", file=sys.stderr)
        return []
    # Strip internal metadata fields
    return [{k: v for k, v in i.items() if not k.startswith("_")} for i in items]


def _deduplicate(incidents: list) -> list:
    seen, out = set(), []
    for inc in incidents:
        key = inc.get("sourceUrl", "")
        if key and key in seen:
            continue
        seen.add(key)
        out.append(inc)
    return out


def _date_filter(incidents: list, days: int, now_utc: datetime) -> list:
    cutoff = (now_utc - timedelta(days=days)).strftime("%Y-%m-%d")
    kept = [i for i in incidents if i.get("date", "") >= cutoff]
    print(f"  ↳ Date filter : last {days} days (≥ {cutoff}) — {len(kept)}/{len(incidents)} kept")
    return kept


# ── generator ─────────────────────────────────────────────────────────────────

def generate(
    scraped_path: Path,
    run_dir: Optional[Path] = None,
    days: int = 3,
    report_date: Optional[str] = None,
) -> Path:
    """
    Generate the security dashboard HTML.

    Args:
        scraped_path : Path to raw scraped JSON (from scrape.py).
        run_dir      : Output directory. Defaults to output/run_YYYYMMDD_HHMMSS/
        days         : Reporting window in days; incidents outside are dropped.
        report_date  : Header date string. Defaults to current UTC datetime.

    Returns:
        Path to the generated HTML file.
    """
    now_utc = datetime.now(timezone.utc)

    if report_date is None:
        report_date = now_utc.strftime("%d %b %Y, %H:%M UTC")
    short_date = now_utc.strftime("%d %b %Y")

    # ── output folder ──────────────────────────────────────────────────────
    if run_dir is None:
        run_dir = ROOT / "output" / f"run_{now_utc.strftime('%Y%m%d_%H%M%S')}"
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    # ── load → filter → deduplicate → date-window ─────────────────────────
    print(f"\n  Loading scraped data from {scraped_path.name}…")
    raw_incidents = _load_scraped(scraped_path)
    print(f"  Raw incidents  : {len(raw_incidents)}")

    filtered   = filter_incidents(raw_incidents)
    print(f"  After filter   : {len(filtered)}")

    deduped    = _deduplicate(filtered)
    incidents  = _date_filter(deduped, days, now_utc)

    # ── build country profiles ─────────────────────────────────────────────
    print(f"  Building country profiles…")
    countries = build_country_profiles(incidents, COUNTRY_META, days=days)

    # ── sort incidents: Critical first, then date desc ─────────────────────
    _sev = {"Critical": 0, "High": 1, "Medium": 2}
    incidents.sort(key=lambda i: (_sev.get(i.get("severity","Medium"), 2), i.get("date","")))

    # ── save clean incidents JSON to run folder ────────────────────────────
    clean_json = run_dir / "incidents.json"
    clean_json.write_text(json.dumps(incidents, indent=2, ensure_ascii=False), encoding="utf-8")

    # ── load and fill template ─────────────────────────────────────────────
    template_path = ROOT / "template.html"
    if not template_path.exists():
        sys.exit(f"ERROR: template.html not found at {template_path}")

    template = template_path.read_text(encoding="utf-8")

    # ── source count (for header subtitle) ─────────────────────────────────
    try:
        from scraper.sources import SOURCES as _SRC
        total_sources = len(_SRC)
    except Exception:
        total_sources = 0

    # ── per-country 14-day history (sparklines + chart comparison) ─────────
    # Persist this run's counts into the durable store first so the window
    # (and every future run) reflects it, then build the trailing 14 days.
    _update_history_store(incidents)
    country_history = _load_history(window_days=14, current_incidents=incidents)

    html = (
        template
        .replace("__INCIDENTS_DATA__",       json.dumps(incidents,      ensure_ascii=False, separators=(",", ":")))
        .replace("__COUNTRIES_DATA__",       json.dumps(countries,      ensure_ascii=False, separators=(",", ":")))
        .replace("__SOCIAL_MONITORS_DATA__", json.dumps(SOCIAL_MONITORS,ensure_ascii=False, separators=(",", ":")))
        .replace("__GENERATED_DATE__",       report_date)
        .replace("__REPORT_DATE__",          short_date)
        .replace("__TOTAL_INCIDENTS__",      str(len(incidents)))
        .replace("__TOTAL_SOURCES__",        str(total_sources))
        .replace("__TIME_WINDOW_DAYS__",     str(days))
        .replace("__COUNTRY_HISTORY__",      json.dumps(country_history, ensure_ascii=False, separators=(",", ":")))
    )

    out_html = run_dir / f"security_dashboard_{now_utc.strftime('%Y%m%d_%H%M%S')}.html"
    out_html.write_text(html, encoding="utf-8")

    # ── summary ───────────────────────────────────────────────────────────
    by_country = {c["name"]: len([i for i in incidents if i.get("country")==c["name"]]) for c in countries}
    crit_n = sum(1 for i in incidents if i.get("severity") == "Critical")
    high_n = sum(1 for i in incidents if i.get("severity") == "High")

    print(f"\n✓  Dashboard generated")
    print(f"   Run folder : {run_dir.resolve()}")
    print(f"   File       : {out_html.name}")
    print(f"   Window     : last {days} days ({short_date})")
    print(f"   Incidents  : {len(incidents)} total  ({crit_n} Critical · {high_n} High)")
    print(f"   By country : {' · '.join(f'{k} {v}' for k,v in by_country.items() if v)}")

    return out_html


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the East Africa Security Intelligence Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--scraped", "-s",
        metavar="JSON_PATH",
        required=True,
        help="Path to scraped JSON file from scrape.py",
    )
    parser.add_argument(
        "--days", "-n",
        type=int,
        default=3,
        metavar="N",
        help="Reporting window in days (default: 3)",
    )
    parser.add_argument(
        "--run-dir",
        metavar="DIR",
        default=None,
        help="Output directory (default: output/run_YYYYMMDD_HHMMSS/)",
    )
    parser.add_argument(
        "--date", "-d",
        metavar="DATE",
        default=None,
        help="Report date string for the header (default: current UTC datetime)",
    )
    args = parser.parse_args()
    generate(
        scraped_path=Path(args.scraped),
        run_dir=Path(args.run_dir) if args.run_dir else None,
        days=args.days,
        report_date=args.date,
    )


if __name__ == "__main__":
    main()
