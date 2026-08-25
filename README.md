# ⚡ CyberPulse • GitHub Actions Cybersecurity Telegram Scraper

A 100% free, serverless threat intelligence scraper that runs **24/7 directly on GitHub Actions** (no hosting, no InfinityFree, and no servers required). It automatically scrapes premier cybersecurity news and sends formatted alerts with CVEs, summaries, and images straight to your **Telegram chat or channel** every 15 minutes.

---

## 🚀 3-Minute Setup Guide for GitHub

### Step 1: Create a GitHub Repository & Upload Files
1. Create a new repository on [GitHub.com](https://github.com/new) (e.g. `cyber-news-telegram-bot`).
2. Upload or push these files to your repository:
   - `.github/workflows/scraper.yml`
   - `scraper.py`
   - `sent_history.json`
   - `README.md`

---

### Step 2: Add Your Telegram Credentials to GitHub Secrets
1. In your GitHub repository, click on **Settings** (top tab).
2. In the left sidebar, click **Secrets and variables** ➔ **Actions**.
3. Click the green **"New repository secret"** button and add two secrets:

| Secret Name | Value | How to Get It |
|---|---|---|
| **`TELEGRAM_BOT_TOKEN`** | `1234567890:ABCdef...` | Message **@BotFather** on Telegram ➔ send `/newbot` ➔ copy token |
| **`TELEGRAM_CHAT_ID`** | `987654321` or `@channel` | Message **@userinfobot** on Telegram ➔ copy your `Id` |

---

### Step 3: Enable Write Permissions for History Tracking
To ensure GitHub Actions can commit the `sent_history.json` file (so you **never receive duplicate news alerts**):

1. In your repository, go to **Settings** ➔ **Actions** ➔ **General**.
2. Scroll down to **Workflow permissions**.
3. Select **"Read and write permissions"**.
4. Check **"Allow GitHub Actions to create and approve pull requests"**.
5. Click **Save**.

---

### Step 4: Test & Run Workflow
1. Go to the **Actions** tab at the top of your repository.
2. Click **"CyberPulse Telegram News Scraper"** on the left.
3. Click **"Run workflow"** ➔ **"Run workflow"** button.
4. Check your Telegram — your first batch of live cybersecurity news will arrive instantly! 🎉

After the first run, GitHub Actions will automatically execute every **15 minutes** in the cloud 24/7!

---

## ⚙️ Optional Configuration Variables

You can optionally configure custom behavior under **Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **Variables**:

- **`FILTER_MODE`**: Set to `zerodays_only` if you only want alerts for Zero-Day exploits and critical CVEs (default: `all`).
- **`MAX_SEND`**: Maximum number of articles sent per 15-minute run (default: `5`).

---

## 🛡️ Sources Monitored

- ⚡ **The Hacker News**
- 🚨 **CISA Advisories (US-CERT)**
- 👁️ **Dark Reading**
- 🪓 **The Register Security**
- 🛡️ **Krebs on Security**
- 🌐 **SecurityWeek**
- ⛈️ **SANS Internet Storm Center (ISC)**
- 🕵️ **Security Affairs**
