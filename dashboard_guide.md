# Security Intelligence Dashboard — User Guide

A practical guide for accessing, reading, and maintaining your own copy of the dashboard.

---

## 1. How to download and open the dashboard

The dashboard is a single HTML file hosted on a GitHub repository. You do not need to install anything, sign up for any service, or use a terminal. Any modern web browser (Chrome, Safari, Edge or Firefox) is enough to open it.

### Option A — Download the full repository as a ZIP

1. Open your web browser and go to the repository URL provided by the consultancy (for example: `https://github.com/lizciat/security_dashboard`).
2. On the main page of the repository, find the green button labelled **&lt; &gt; Code** near the top right of the file list.
3. Click **&lt; &gt; Code**. A small menu will open. At the bottom of that menu, click **Download ZIP**.
4. Your browser will download a file called something like `security_dashboard-main.zip`. Save it to a folder you can find easily, such as your Desktop or Downloads folder.
5. Once the download finishes, find the ZIP file and double-click it to unzip it. A new folder will appear next to it.
6. Open the unzipped folder, then open the sub-folder named **site**.
7. Inside **site** you will see a file called **index.html**. Double-click it. The dashboard will open in your default browser.

### Option B — Download just the dashboard file

1. Open the repository in your browser as above.
2. Click on the folder named **site**.
3. Click on the file **index.html** to open its preview page.
4. On the preview page, look near the top right for a button with a download icon (a downward arrow) or the text **Raw**.
5. Right-click the **Raw** button and choose **Save Link As…** (or **Download Linked File** on Safari). Save the file as `index.html`.
6. Open the folder where you saved the file and double-click `index.html`. The dashboard will open in your browser.

> **Tip:** An internet connection is needed the first time you open the dashboard, because one small library that draws the charts is loaded from a public source.

---

## 2. How to read and use the dashboard

The dashboard is organised into clear sections so you can quickly see where the highest risk is, what is driving it, and which incidents to follow up. The layout is described below in the order you will see it on screen.

### 2.1 Top bar — what you are looking at

At the very top you will find the dashboard title and a short summary line that tells you the date the report was generated, the total number of incidents shown, the time window covered (for example **last 3 days**) and how many sources are being monitored. This line is your quick orientation each time you open the file.

### 2.2 Filter bar — narrowing the view

Below the title sits a row of filters. Use them to focus on what matters to you:

- **Country** — show only incidents in one of the monitored countries.
- **Severity** — show only Critical, High or Medium incidents.
- **Type** — narrow by threat type (for example Armed Conflict, Terrorism, Drone Attack).
- **Status** — show only items you have marked as New, Verified, Escalated, etc.
- **Min. confidence** — hide low-confidence items if you want only the strongest signals.
- **Origin** — show only traditional news, only social media signals, or both.
- **From date** — start the view from a specific day.

Active filters appear as small grey chips next to the bar so you always know what is applied. Click **↺ Clear** to reset everything.

### 2.3 Severity levels

Every incident carries one of three severity levels. The colour and the symbol are always shown together so the meaning is clear even when printing in black and white:

| Level | Meaning |
|---|---|
| 🔴 **● Critical (red)** | Active threat, requires immediate attention. Examples: large-scale armed clashes, mass-casualty events, drone strikes on populated areas. |
| 🟠 **▲ High (orange)** | Serious development, monitor closely and review within 24 hours. Examples: clashes between armed groups, IED attacks, political crises. |
| 🟡 **■ Medium (yellow)** | Relevant context. Keep on file but no immediate action required. |

### 2.4 Country intelligence panel

On the right side of the screen you will find a list of the monitored countries. Each row shows the country flag, the number of incidents, severity counts and a small line graph showing the 14-day trend. The arrow on the right indicates whether activity is rising, falling or stable.

Click on any country to open its detailed card. The card has several tabs:

- **Overview** — short summary, key regions affected, dominant threat types.
- **Incidents** — full list of recent incidents in that country.
- **Social** — X (Twitter) accounts being monitored, grouped by type (Press, Government, NGO, Analyst, Conflict Monitor).
- **Sources** — quick links to the news outlets used.
- **Actions** — recommended operational steps based on the threats observed.

### 2.5 Incident feed

The main column shows every incident as an individual card. Each card includes the country, threat type, severity badge, source, date, a short description, the region and a confidence bar. Click anywhere on the card (outside the buttons) to open a full detail window with all available information and a direct link to the original article.

Use the small buttons on each card to add the incident to your briefing, mark it as **Verified**, **Escalated** or **Archived**. These markers are stored in your browser so they remain when you reopen the same file on the same computer.

### 2.6 Other views

At the top of the filter bar there are three view tabs:

- **Timeline** — default card feed.
- **Table** — sortable spreadsheet-style view of every incident, useful when you want to scan many items quickly.
- **Analytics** — summary charts: incidents by threat type, severity by country, incidents over time, and the most active sources. Every chart shows the exact numbers next to each bar.

### 2.7 Social media signals

Some incidents come from monitored X (Twitter) accounts rather than from news outlets. These items show the source name as a handle (for example **@martinplaut**) and represent unverified field-level information. They are useful for early warning but should always be cross-checked against a news source before being acted upon. The **Origin** filter lets you separate news and social signals when needed.

### 2.8 Briefing

When you click **+ Add to Brief** on an incident card, that item is added to a queue on the right side of the screen (or accessible from the **Brief** button at the top on smaller screens). Pressing **Generate Brief** creates a clean, pre-formatted intelligence summary that you can copy and paste into an email or messaging tool.

---

## 3. How to get an updated version

The dashboard is refreshed on a regular basis by the consultancy. Each new version is published to the same GitHub repository, and the main `site/index.html` file is replaced with the latest version. You do not need to do anything special to receive updates — simply download the file again whenever you want the most recent data.

Past reports are kept inside `site/runs/`. Each subfolder has a name in the format `run_YYYYMMDD_HHMMSS`, where the digits are the date and time of that report. The highest number is the most recent. If you only need the latest, you do not have to look inside this folder — just use `site/index.html`.

---

## 4. Setting up your own copy of the dashboard

If you want your own private copy of the dashboard that you control and can update on your own schedule, you can copy ("fork") the repository into your personal GitHub account.

### 4.1 Create a free GitHub account

Skip this step if you already have one.

1. Go to `https://github.com` in your browser.
2. Click **Sign up** in the top right.
3. Follow the prompts: enter your email, choose a username and password, verify your email.

### 4.2 Fork the consultancy repository into your account

"Forking" means creating your own copy of a repository under your own GitHub username. Your copy is independent — you can update it without affecting the original.

1. Make sure you are logged in to your GitHub account.
2. Open the consultancy repository link in your browser: `https://github.com/lizciat/security_dashboard`.
3. In the top right of the page, click the **Fork** button.
4. On the next screen, leave the default options as they are and click the green **Create fork** button.
5. After a few seconds, GitHub will redirect you to your own copy. The URL will look like `https://github.com/<your-username>/security_dashboard`.

You now own a private working copy of the dashboard project. Bookmark this page — it is where you will go for everything else in this guide.

### 4.3 Enable the live web version (optional)

If you want your forked dashboard to be visible at a public URL like `https://<your-username>.github.io/security_dashboard/`, do the following one-time setup:

1. On your forked repository, click the **Settings** tab near the top.
2. In the left sidebar, click **Pages**.
3. Under **Source**, click the dropdown and choose **GitHub Actions**.
4. Save. Your dashboard will be published automatically the next time the workflow runs.

---

## 5. Connecting your own Xquik account

The dashboard collects signals from X (Twitter) accounts using a service called **Xquik**. To run the dashboard from your forked repository, you will need a Xquik account and an API key.

### 5.1 Create a Xquik account

1. Open `https://xquik.com` in your browser.
2. Click **Sign up** (or **Get started**) and follow the steps to register: email, password, and any verification step.
3. Once you are logged in, you will see your Xquik dashboard.

### 5.2 Generate your Xquik API key

An API key is a long secret code that lets the dashboard fetch data on your behalf. Treat it like a password — do not share it publicly.

1. In your Xquik dashboard, look for a section called **API Keys**, **Developer**, or **Settings**. The exact label may vary slightly.
2. Click **Create new key** (or similar wording).
3. Give the key a descriptive name like "Security Dashboard".
4. Click **Generate**. A long string starting with `xq_…` will appear on screen.
5. **Copy this key immediately** and paste it somewhere safe (a password manager is ideal). For security reasons, Xquik will not show you the full key again after you leave this page.

> **Tip:** If you ever lose the key, you can come back and generate a new one. Just remember to update the GitHub secret afterwards (see Section 6).

---

## 6. Adding your Xquik key to your GitHub repository

The forked repository needs to know your Xquik key in order to fetch X data. GitHub provides a safe storage area for secrets like this so that the key never appears in the code or in any visible file.

### 6.1 Open the repository secrets page

1. Open your forked repository in the browser.
2. Click the **Settings** tab near the top.
3. In the left sidebar, scroll down to **Secrets and variables** and click on it to expand the menu.
4. Click **Actions** under that menu.

### 6.2 Add the key as a new secret

1. On the page that opens, click the green **New repository secret** button in the top right.
2. In the **Name** field, type exactly: `XQUIK_API_KEY`
   *(uppercase letters and underscores — no spaces, no quotation marks)*
3. In the **Secret** field, paste the full Xquik key you copied earlier. It should start with `xq_` and be one long line.
4. Click the green **Add secret** button.

The key is now safely stored. You will see it listed as `XQUIK_API_KEY` with no way to view its content again — this is normal and expected. If you ever need to change it, just click on it and select **Update**.

---

## 7. Manually updating the dashboard with GitHub Actions

Your repository is configured to refresh the dashboard automatically once per day. You can also trigger a manual refresh at any time — for example, after a major incident or when you have just added your Xquik key.

### 7.1 Trigger a manual refresh

1. Open your forked repository in the browser.
2. Click the **Actions** tab near the top of the page.
3. The first time you visit this tab on your forked repository, you may see a yellow banner asking you to enable workflows. Click the green **I understand my workflows, go ahead and enable them** button.
4. In the left sidebar, click on the workflow called **Daily Update**.
5. Above the list of past runs, on the right side, click the **Run workflow** button (a small dropdown).
6. Leave the branch as **main** and click the green **Run workflow** button inside the dropdown.

A new run will appear at the top of the list within a few seconds. It will show a yellow spinning icon while it works. After three to five minutes, it should turn into a green check mark, meaning the dashboard has been updated successfully.

### 7.2 What to do if the run fails

If the icon turns into a red cross instead of a green check mark:

1. Click on the failed run to see the details.
2. Click on the job named **build** to expand it.
3. Look for the step highlighted in red — it usually tells you what went wrong. Most common issues:
   - **`XQUIK_API_KEY not set` or auth errors** — the secret was not added correctly. Go back to Section 6 and re-check the name (must be exactly `XQUIK_API_KEY`) and that you pasted the full key.
   - **Quota exhausted** — your Xquik plan has reached its limit. Wait for the limit to reset, or upgrade your Xquik plan.

If you cannot resolve the issue yourself, contact the consultancy with a screenshot of the error.

### 7.3 View the updated dashboard

Once the workflow finishes successfully:

- **Live version** — if you enabled GitHub Pages (Section 4.3), refresh your dashboard URL: `https://<your-username>.github.io/security_dashboard/`.
- **Downloaded file** — go to the **site** folder in your repository, open `index.html`, and download it again using the **Raw** button as in Section 1, Option B.

---

## Quick checklist

| Action | Where to go |
|---|---|
| View the latest dashboard | `site/index.html` in the repository, or your GitHub Pages URL |
| See past reports | `site/runs/` folder, newest folder name is most recent |
| Create your own copy | Click **Fork** on the consultancy repository |
| Add your Xquik key | Repository **Settings** → **Secrets and variables** → **Actions** → **New repository secret** |
| Refresh the data manually | **Actions** tab → **Daily Update** → **Run workflow** |

---

If anything is unclear or the dashboard does not open as expected, please contact the consultancy team and we will assist you directly.
