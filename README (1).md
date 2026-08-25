# ⚡ CyberPulse • Automated Cyber Threat Intel, AI Security & Tools Broadcaster

<p align="center">
  <img src="channel_icon.png" width="140" height="140" alt="CyberPulse Logo" style="border-radius: 50%;">
</p>

<p align="center">
  <b>A 100% serverless, zero-cost threat intelligence bot that delivers real-time cybersecurity news, security engineering writeups, hacker hardware gadgets, AI/LLM security research, and Zero-Day alerts straight to Telegram.</b>
</p>

<p align="center">
  <a href="https://t.me/Cyber_pulse_News"><img src="https://img.shields.io/badge/Telegram-Join%20Channel-229ED9?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Channel"></a>
  <img src="https://img.shields.io/badge/GitHub%20Actions-Automated%2024%2F7-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

## 📌 Live Demo Channel

See all news, AI security research, and hacker tool writeups live on Telegram:  
👉 **[t.me/Cyber_pulse_News](https://t.me/Cyber_pulse_News)**

---

## 🌐 Complete Topics & Sources Monitored

CyberPulse tracks across 4 core cybersecurity pillars:

### 1. 🤖 AI Security & LLM Hacks
- **Topics**: Prompt injections, jailbreaks, LLM Red Teaming, AI agent vulnerabilities, model poisoning, and deepfakes.

### 2. 🛠️ Hacker Gadgets & Security Tools
- **Sources**: *Hackaday Security Hacks*, *Help Net Security*.
- **Topics**: Hardware teardowns, Flipper Zero, SDR/Radio frequency hacks, BadUSB, Wi-Fi Pineapple, Burp Suite, Ghidra, Nmap, and open-source tooling.

### 3. 🥷 Security Engineering & Deep Research
- **Sources**: *PortSwigger Web Security Research*, *Cisco Talos Threat Intelligence*, *Microsoft Security Intelligence*, *Cloudflare Security*.
- **Topics**: Reverse engineering, kernel exploits, HTTP request smuggling, binary analysis, protocol vulnerabilities, and defensive architecture.

### 4. 🚨 Breaking News, Zero-Days & Advisories
- **Sources**: *The Hacker News*, *CISA Advisories (US-CERT)*, *Dark Reading*, *Krebs on Security*, *The Register Security*, *SecurityWeek*, *SANS Internet Storm Center*, *Security Affairs*.
- **Topics**: Critical CVE disclosures (CVSS 10.0), active ransomware campaigns, data breaches, and government directives.

---

## ✨ Features

- **🚀 100% Serverless & Free**: Powered entirely by **GitHub Actions** cron schedules. No hosting, VPS, or maintenance required.
- **⏱️ Automated 24/7 Monitoring**: Runs automatically every **15 minutes** in the cloud.
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
| **`MAX_SEND`** | `6` | Maximum number of new articles sent per 15-minute run (prevents Telegram rate limits). |

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
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
