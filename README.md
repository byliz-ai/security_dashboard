# East Africa Security Dashboard

Self-updating static dashboard tracking security incidents across Sudan, South Sudan, DRC, Somalia, and Ethiopia. A Python pipeline scrapes curated news + X (Twitter) sources, classifies incidents, and generates a self-contained HTML report.

**Live site:** https://lizciat.github.io/security_dashboard/
**Past runs:** https://lizciat.github.io/security_dashboard/runs/

> **Looking for the user guide?**
> Read [`dashboard_guide.md`](./dashboard_guide.md) directly in your browser, or download [`dashboard_guide.pdf`](./dashboard_guide.pdf) to print or share.

## How it updates

A GitHub Actions workflow runs every day at **06:00 UTC**:

1. Installs Python dependencies.
2. Runs `dashboard_generator/pipeline.py --days 3`.
3. Copies the newest dashboard HTML into `site/index.html` and archives the run under `site/runs/<timestamp>/`.
4. Publishes `site/` to GitHub Pages.

You can also trigger a run manually any time from the **Actions** tab → **Daily Update** → **Run workflow**.

## First-time setup (do this once)

### 1. Push the project to GitHub

Open Terminal, then:

```bash
cd "/Users/lizethllanos/Library/CloudStorage/GoogleDrive-llanoslizeth@gmail.com/My Drive/security dashboard"
git init
git branch -M main
git remote add origin https://github.com/lizciat/security_dashboard.git
git add .
git commit -m "Initial commit: security dashboard pipeline + daily auto-publish"
git push -u origin main
```

(If `git push` asks for a password, use a **GitHub Personal Access Token** instead — generate one at https://github.com/settings/tokens with the `repo` scope.)

### 2. Add the Xquik API key as a GitHub Secret

X/Twitter tweets are fetched through [Xquik](https://xquik.com). The workflow needs your API key as a repository secret:

1. Go to https://github.com/lizciat/security_dashboard/settings/secrets/actions
2. Click **New repository secret**.
3. Name: `XQUIK_API_KEY`
4. Value: paste your key (starts with `xq_…`).
5. Click **Add secret**.

If the secret is missing the pipeline still runs, but X accounts return 0 tweets.

### 3. Enable GitHub Pages

This is a one-click step in the browser:

1. Go to https://github.com/lizciat/security_dashboard/settings/pages
2. Under **Source**, select **GitHub Actions**.
3. Save.

That's it. The next workflow run will publish to `https://lizciat.github.io/security_dashboard/`.

### 4. Trigger the first run

Go to the **Actions** tab → **Daily Update** → **Run workflow** → **Run workflow** (green button). Wait ~3–5 minutes. Refresh the live URL.

## Project structure

```
security dashboard/
├── .github/workflows/daily.yml   ← cron + publish workflow
├── site/                         ← what gets published (built by workflow)
│   ├── index.html                ← newest dashboard
│   └── runs/<timestamp>/         ← archived past runs
├── dashboard_generator/
│   ├── pipeline.py               ← entry point (scrape + generate)
│   ├── scrape.py
│   ├── generate.py
│   ├── build_site.py             ← copies newest run into site/
│   ├── template.html
│   ├── data.py                   ← country metadata + X account lists
│   ├── scraper/                  ← fetcher, classifier, filter, sources
│   ├── requirements.txt
│   └── output/run_<timestamp>/   ← per-run artifacts (gitignored)
└── README.md
```

## Local development

```bash
cd dashboard_generator
pip install -r requirements.txt
python pipeline.py --days 3 --open
```

The dashboard HTML is written to `output/run_<timestamp>/`. Run `python build_site.py` to copy the newest output into `../site/index.html` for local preview.

## Notes / caveats

- **Xquik X scraping:** X/Twitter accounts are fetched via the Xquik REST API. If `XQUIK_API_KEY` is missing or the quota is exhausted, X sources return 0 tweets but the pipeline continues with RSS news sources.
- **Free tier:** GitHub Actions gives public repos unlimited free minutes; GitHub Pages has no bandwidth charge for normal use.
- **Time window:** The dashboard shows the last 3 days by default. Change `--days N` in `.github/workflows/daily.yml` to adjust.
