# ⚡ CyberPulse • Automated Cyber Threat Intel, AI Security & Tools Broadcaster

<p align="center">
  <img src="channel_icon.png" width="140" height="140" alt="CyberPulse Logo" style="border-radius: 50%;">
</p>

<p align="center">
  <b>A 100% serverless, zero-cost threat intelligence bot that delivers real-time cybersecurity news from India (CERT-In, Cybercrime & Banking) and Global superpowers (US, UK, EU, APAC), plus AI Security & Hacker Tools straight to Telegram.</b>
</p>

<p align="center">
  <a href="https://t.me/Cyber_pulse_News"><img src="https://img.shields.io/badge/Telegram-Join%20Channel-229ED9?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Channel"></a>
  <img src="https://img.shields.io/badge/GitHub%20Actions-Automated%2024%2F7-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Coverage-India%20%26%20Global-orange?style=for-the-badge" alt="Regional Coverage">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

## 📌 Live Demo Channel

See all news, AI security research, and hacker tool writeups live on Telegram:  
👉 **[t.me/Cyber_pulse_News](https://t.me/Cyber_pulse_News)**

---

## 🌐 Complete Topics & Sources Monitored (18+ Feeds)

CyberPulse tracks across 5 core cybersecurity pillars:

### 1. 🇮🇳 India Threat Landscape & CERT-In
- **Sources**: *The420 Cyber News India*, *Cyber Security News (India & Global)*, *GBHackers InfoSec*.
- **Topics**: CERT-In vulnerability bulletins, Indian banking & UPI frauds, state police cyber cell operations, CBI investigations, DPDP Act compliance, and national cyber defense.

### 2. 🤖 AI Security & LLM Hacks
- **Topics**: Prompt injections, jailbreaks, LLM Red Teaming, AI agent vulnerabilities, model poisoning, and deepfakes.

### 3. 🛠️ Hacker Gadgets & Security Tools
- **Sources**: *Hackaday Security Hacks*, *Help Net Security*.
- **Topics**: Hardware teardowns, Flipper Zero, SDR/Radio frequency hacks, BadUSB, Wi-Fi Pineapple, Burp Suite, Ghidra, Nmap, and open-source tooling.

### 4. 🥷 Security Engineering & Deep Research
- **Sources**: *PortSwigger Web Security Research*, *Cisco Talos Threat Intelligence*, *Microsoft Security Intelligence*, *Cloudflare Security*.
- **Topics**: Reverse engineering, kernel exploits, HTTP request smuggling, binary analysis, protocol vulnerabilities, and defensive architecture.

### 5. 🚨 Breaking News, Zero-Days & Advisories
- **Sources**: *The Hacker News*, *CISA Advisories (US-CERT)*, *NCSC UK Alerts*, *Dark Reading*, *Krebs on Security*, *The Register Security*, *SecurityWeek*, *SANS Internet Storm Center*, *Security Affairs*.
- **Topics**: Critical CVE disclosures (CVSS 10.0), active ransomware campaigns, data breaches, and government directives.

---

## ✨ Features

- **🚀 100% Serverless & Free**: Runs automatically via **GitHub Actions**. No hosting, VPS, or maintenance required.
- **⏱️ Automated 24/7 Monitoring**: Scrapes every **30 minutes** with guaranteed on-time execution.
- **📅 7-Day Lookback & Priority Scoring**: Ranks and prioritizes the most critical Zero-Days, breaches, and major research from the past week.
- **🌍 Regional Flag Badging**: Automatically tags posts with country flags (`🇮🇳 India`, `🇺🇸 United States`, `🇬🇧 United Kingdom`, `🇪🇺 Europe`, `🌏 Asia-Pacific`, `🌐 Global`).
- **🔴 Automatic CVE Tagging**: Automatically detects and tags CVE identifiers (e.g. `CVE-2024-38856`).
- **📸 Rich Telegram Cards**: Formats alerts with hero images, category badges, bold headlines, clean summaries, and inline direct article links.
- **🛡️ Deduplication Engine**: Uses `sent_history.json` so your channel never gets spammed with duplicate posts.
- **🔒 Secure**: API tokens and chat IDs are stored securely in encrypted **GitHub Secrets**.

---

## 🚀 How to Set Up Your Own Bot (3-Minute Guide)

Anyone can fork this repository and launch their own automated Telegram threat intelligence channel:

### Step 1: Fork This Repository
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
3. Click **"New repository secret"** and add:

| Secret Name | Example Value | Description |
|---|---|---|
| **`TELEGRAM_BOT_TOKEN`** | `1234567890:ABCdefGhI...` | The token you got from @BotFather |
| **`TELEGRAM_CHAT_ID`** | `@your_channel_name` or `-100...` | Your channel username or private chat ID |

---

### Step 4: Enable Workflow Write Permissions

GitHub Actions needs permission to commit `sent_history.json` so it can track sent articles:

1. In your repository, go to **Settings ➔ Actions ➔ General**.
2. Scroll down to **Workflow permissions**.
3. Select **"Read and write permissions"**.
4. Check **"Allow GitHub Actions to create and approve pull requests"**.
5. Click **Save**.

---

### Step 5: (Optional) 100% Reliable 24/7 Scheduling via cron-job.org

To ensure your workflow runs on the exact minute without any delays from GitHub's queue:

1. Create a GitHub Token with `repo` & `workflow` scope at **[github.com/settings/tokens/new](https://github.com/settings/tokens/new)**.
2. Go to **[cron-job.org](https://cron-job.org)** (free) ➔ click **Create Cronjob**.
3. **URL**: `https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/actions/workflows/scraper.yml/dispatches`
4. **Method**: `POST`
5. **Schedule**: `Every 30 minutes`
6. **Headers**:
   - `Authorization`: `Bearer YOUR_GITHUB_TOKEN`
   - `Accept`: `application/vnd.github+json`
   - `Content-Type`: `application/json`
   - `User-Agent`: `CyberPulse-Cron`
7. **Body**: `{"ref":"main"}`

---

## ⚙️ Customization & Environment Variables

You can customize your feed by adding optional variables under **Settings ➔ Secrets and variables ➔ Actions ➔ Variables**:

| Variable Name | Default | Options / Description |
|---|---|---|
| **`FILTER_MODE`** | `all` | • `all` — Dispatches all news, tools, and research.<br>• `india_only` — Dispatches **only India & CERT-In** news.<br>• `zerodays_only` — Dispatches only Zero-Days & Critical CVEs. |
| **`MAX_SEND`** | `6` | Maximum number of new articles sent per 30-minute run (prevents Telegram rate limits). |

---

## 💻 Running Locally

```bash
# Clone repository
git clone https://github.com/SaiKaligotla/Cyberpulse.git
cd Cyberpulse

# Set environment variables and run
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="@your_channel_username"
python3 scraper.py
