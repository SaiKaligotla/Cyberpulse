# ⚡ CyberPulse • Automated Cybersecurity Threat Intel & Telegram Broadcaster

<p align="center">
  <img src="channel_icon.png" width="140" height="140" alt="CyberPulse Logo" style="border-radius: 50%;">
</p>

<p align="center">
  <b>A 100% serverless, zero-cost, automated threat intelligence scraper that delivers real-time hacker news, Zero-Day alerts, ransomware reports, and CISA advisories straight to Telegram.</b>
</p>

<p align="center">
  <a href="https://t.me/Cyber_pulse_News"><img src="https://img.shields.io/badge/Telegram-Join%20Channel-229ED9?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Channel"></a>
  <img src="https://img.shields.io/badge/GitHub%20Actions-Automated%2024%2F7-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

## 📌 Live Demo Channel

You can see this bot in live action on Telegram:  
👉 **[t.me/Cyber_pulse_News](https://t.me/Cyber_pulse_News)**

---

## ✨ Features

- **🚀 100% Serverless & Free**: Powered entirely by **GitHub Actions** cron schedules. No VPS, no hosting fees, and zero maintenance.
- **⏱️ Automated 24/7 Monitoring**: Scrapes the web every **15 minutes** in the background.
- **🌐 8+ Premier Threat Intelligence Sources**:
  - ⚡ **The Hacker News**
  - 🚨 **CISA Advisories (US-CERT)**
  - 👁️ **Dark Reading**
  - 🪓 **The Register Security**
  - 🛡️ **Krebs on Security**
  - 🌐 **SecurityWeek**
  - ⛈️ **SANS Internet Storm Center (ISC)**
  - 🕵️ **Security Affairs**
- **🔴 Automatic CVE Tagging**: Automatically detects and tags CVE identifiers (e.g. `CVE-2024-38856`).
- **📁 Smart Threat Categorization**: Categorizes news into *Zero-Days & Exploits*, *Ransomware & Malware*, *Data Breaches*, *CISA Advisories*, *AI Security*, *Cloud & Supply Chain*, and *Nation-State / APT*.
- **📸 Rich Telegram Cards**: Formats posts with hero images, bold headlines, clean summaries, and inline direct article links.
- **🛡️ Deduplication Engine**: Uses `sent_history.json` to track already-dispatched stories so your channel never gets spammed with duplicate articles.
- **🔒 Secure**: API tokens and chat IDs are stored securely in encrypted **GitHub Secrets**.

---

## 🚀 How to Set Up Your Own Bot (3-Minute Guide)

Anyone can fork this repository and launch their own automated Telegram news broadcast in 4 simple steps:

### Step 1: Fork or Clone This Repository
Click the **Fork** button at the top right of this page to create a copy under your GitHub account.

---

### Step 2: Create Your Telegram Bot & Channel

1. **Create the Bot**:
   - Open Telegram and message **[@BotFather](https://t.me/BotFather)**.
   - Send `/newbot`, choose a name and username for your bot.
   - Copy the generated **Bot Token** (e.g. `1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ`).
2. **Create or Open Your Channel**:
   - Create a Telegram Channel (or use an existing one).
   - Go to **Channel Info ➔ Manage Channel (or Pencil icon) ➔ Administrators ➔ Add Administrator**.
   - Search for your bot's username and add it as an admin with the **"Post Messages"** permission.
3. **Get Your Channel Handle or Chat ID**:
   - If your channel is **Public**: Your Chat ID is `@your_channel_name` (e.g. `@Cyber_pulse_News`).
   - If your channel is **Private**: Forward any message from the channel to **[@userinfobot](https://t.me/userinfobot)** to get your numeric ID starting with `-100` (e.g. `-1001234567890`).

---

### Step 3: Add Secrets to GitHub

1. In your forked repository, click **Settings** (top tab).
2. In the left sidebar, navigate to **Secrets and variables ➔ Actions**.
3. Click **"New repository secret"** and add the following two secrets:

| Secret Name | Example Value | Description |
|---|---|---|
| **`TELEGRAM_BOT_TOKEN`** | `1234567890:ABCdefGhI...` | The token you got from @BotFather |
| **`TELEGRAM_CHAT_ID`** | `@your_channel_name` or `-100...` | Your channel username or private chat ID |

---

### Step 4: Enable Workflow Write Permissions

GitHub Actions needs permission to commit the `sent_history.json` file so it can remember which articles have already been sent:

1. In your repository, go to **Settings ➔ Actions ➔ General**.
2. Scroll down to **Workflow permissions**.
3. Select **"Read and write permissions"**.
4. Check **"Allow GitHub Actions to create and approve pull requests"**.
5. Click **Save**.

---

### Step 5: Test It!

1. Go to the **Actions** tab at the top of your GitHub repository.
2. Click **"CyberPulse Telegram News Scraper"** on the left.
3. Click **"Run workflow" ➔ "Run workflow"**.

🎉 **You're done!** Your bot will post the first batch of articles immediately and continue monitoring and posting 24/7 every 15 minutes.

---

## ⚙️ Customization & Environment Variables

You can customize your feed by adding optional variables under **Settings ➔ Secrets and variables ➔ Actions ➔ Variables**:

| Variable Name | Default | Options / Description |
|---|---|---|
| **`FILTER_MODE`** | `all` | Set to `zerodays_only` if you only want alerts for Zero-Days & Critical CVEs. |
| **`MAX_SEND`** | `5` | Maximum number of new articles sent per 15-minute run (prevents Telegram rate limits). |

### Adding Custom Feeds:
You can easily add new RSS/Atom feeds by editing the `FEEDS` list in `scraper.py`:

```python
FEEDS = [
    {
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/",
        "icon": "💻"
    },
    ...
]
