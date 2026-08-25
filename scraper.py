#!/usr/bin/env python3
"""
CyberPulse • Comprehensive Cybersecurity & Tech Threat Intelligence Scraper
Scrapes:
- Breaking Cyber News & Zero-Days
- Security Engineering & Reverse Engineering Research
- Hacker Tools, Hardware Gadgets (Flipper Zero, SDR, BadUSB)
- AI Security, LLM Prompt Injections & Jailbreaks
- Threat Actor Intelligence & Malware Deep-Dives
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def clean_chat_id(raw_id):
    if not raw_id:
        return ""
    raw_id = raw_id.strip().strip("'\"")
    # If user pasted a full t.me link
    if "t.me/" in raw_id:
        raw_id = "@" + raw_id.split("t.me/")[-1].strip("/@")
    # If it's a public channel handle without @ and not numeric ID
    elif not raw_id.startswith("@") and not raw_id.startswith("-") and not raw_id.isdigit():
        raw_id = "@" + raw_id
    return raw_id

# 1. Telegram Configuration from GitHub Secrets / Environment Variables
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip().strip("'\"")
CHAT_ID = clean_chat_id(os.environ.get("TELEGRAM_CHAT_ID", ""))
FILTER_MODE = os.environ.get("FILTER_MODE", "all").strip() # 'all' or 'zerodays_only'
MAX_SEND = int(os.environ.get("MAX_SEND", "6"))

HISTORY_FILE = "sent_history.json"

# 2. Comprehensive Cybersecurity Feeds (News, Research, Gadgets, AI, Tools)
FEEDS = [
    # Breaking News & Threat Intel
    {
        "name": "The Hacker News",
        "url": "https://feeds.feedburner.com/TheHackersNews",
        "icon": "⚡"
    },
    {
        "name": "CISA Advisories",
        "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
        "icon": "🚨"
    },
    {
        "name": "Dark Reading",
        "url": "https://www.darkreading.com/rss.xml",
        "icon": "👁️"
    },
    {
        "name": "The Register Security",
        "url": "https://www.theregister.com/security/headlines.atom",
        "icon": "🪓"
    },
    {
        "name": "Krebs on Security",
        "url": "https://krebsonsecurity.com/feed/",
        "icon": "🛡️"
    },
    {
        "name": "SecurityWeek",
        "url": "https://www.securityweek.com/feed/",
        "icon": "🌐"
    },
    {
        "name": "Security Affairs",
        "url": "https://securityaffairs.com/feed",
        "icon": "🕵️"
    },
    {
        "name": "SANS Internet Storm Center",
        "url": "https://isc.sans.edu/rssfeed.xml",
        "icon": "⛈️"
    },
    # Security Engineering & Deep Research Blogs
    {
        "name": "PortSwigger Research",
        "url": "https://portswigger.net/research/rss",
        "icon": "🧪"
    },
    {
        "name": "Cisco Talos Threat Intel",
        "url": "https://blog.talosintelligence.com/rss/",
        "icon": "🎯"
    },
    {
        "name": "Microsoft Security Blog",
        "url": "https://www.microsoft.com/en-us/security/blog/feed/",
        "icon": "🏢"
    },
    {
        "name": "Cloudflare Security",
        "url": "https://blog.cloudflare.com/tag/security/rss/",
        "icon": "☁️"
    },
    # Hacker Gadgets, Tools & Hardware Hacks
    {
        "name": "Hackaday Security Hacks",
        "url": "https://hackaday.com/category/security-hacks/feed/",
        "icon": "🛠️"
    },
    {
        "name": "Help Net Security",
        "url": "https://www.helpnetsecurity.com/feed/",
        "icon": "🔐"
    }
]

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    # Keep latest 400 entries to maintain lightweight repo
    if len(history) > 400:
        history = history[-400:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def fetch_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 CyberPulseBot/1.0"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read()
    except Exception as e:
        print(f"[-] Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return None

def extract_cves(text):
    matches = re.findall(r"CVE-\d{4}-\d{4,7}", text, re.IGNORECASE)
    return list(dict.fromkeys([m.upper() for m in matches]))

def categorize(title, snippet, source_name=""):
    text = f"{title} {snippet} {source_name}".lower()

    # 1. AI Security & LLM Hacks
    if re.search(r"artificial intelligence|ai security|llm|chatgpt|openai|claude|prompt injection|jailbreak|model poisoning|deepfake|ai agent|machine learning", text):
        return "🤖 AI Security & LLMs"

    # 2. Hacker Gadgets & Security Tools
    if re.search(r"flipper zero|wifi pineapple|badusb|hardware hack|sdr|radio frequency|firmware|ghidra|burp suite|nmap|metasploit|yubikey|proxmark|teardown|gadget|open-source tool", text) or "Hackaday" in source_name:
        return "🛠️ Tools & Hardware Gadgets"

    # 3. Security Engineering & Deep Research
    if re.search(r"reverse engineering|binary exploitation|kernel|heap|cryptography|writeup|fuzzing|research|proof of concept|poc|patch analysis", text) or "PortSwigger" in source_name or "Talos" in source_name:
        return "🥷 Security Engineering & Research"

    # 4. Zero-Days & Exploits
    if re.search(r"zero-day|0-day|exploit|vulnerability|rce|buffer overflow|privilege escalation|flaw|cve-|unauthenticated", text):
        return "🔴 Zero-Days & Exploits"

    # 5. Ransomware & Malware
    if re.search(r"ransomware|lockbit|blackcat|alphv|malware|trojan|stealer|botnet|backdoor|infostealer", text):
        return "💀 Ransomware & Malware"

    # 6. Data Breaches & Leaks
    if re.search(r"breach|leaked|database dump|stolen data|compromised|passwords|exfiltrated|credentials", text):
        return "💼 Data Breaches"

    # 7. CISA & Gov Advisories
    if re.search(r"cisa|fbi|nsa|advisory|directive|homeland security|kev catalog", text):
        return "🚨 CISA & Advisories"

    # 8. Cloud & Supply Chain
    if re.search(r"aws|azure|cloud|kubernetes|docker|github|npm|pypi|supply chain", text):
        return "🌐 Cloud & DevSecOps"

    # 9. Nation-State & APT
    if re.search(r"apt|nation-state|china|russia|north korea|iran|espionage|cozy bear|sandworm", text):
        return "⚔️ Nation-State & APT"

    return "🛡️ Cybersecurity"

def clean_html(raw_html):
    if not raw_html:
        return ""
    clean = re.sub(r"<[^>]+>", " ", raw_html)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

def extract_image(item_xml, raw_desc):
    # 1. Enclosure tag
    enclosure = item_xml.find("enclosure")
    if enclosure is not None and "url" in enclosure.attrib:
        url = enclosure.attrib["url"]
        if not url.endswith(".mp3") and not url.endswith(".wav"):
            return url

    # 2. Media content or thumbnail tag
    for tag in ["{http://search.yahoo.com/mrss/}content", "{http://search.yahoo.com/mrss/}thumbnail"]:
        media = item_xml.find(tag)
        if media is not None and "url" in media.attrib:
            return media.attrib["url"]

    # 3. img tag inside HTML description
    if raw_desc:
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', raw_desc, re.IGNORECASE)
        if match:
            src = match.group(1)
            if "feedburner" not in src and "doubleclick" not in src and "gravatar" not in src and not src.endswith(".gif"):
                return src
    return None

def parse_feed(feed_info):
    xml_data = fetch_url(feed_info["url"])
    if not xml_data:
        return []

    articles = []
    try:
        root = ET.fromstring(xml_data)

        # Check RSS 2.0 (<channel><item>)
        items = root.findall(".//item")
        if items:
            for item in items:
                title_el = item.find("title")
                link_el = item.find("link")
                desc_el = item.find("description")

                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                link = link_el.text.strip() if link_el is not None and link_el.text else ""
                raw_desc = desc_el.text if desc_el is not None and desc_el.text else ""

                if not title or not link:
                    continue

                snippet = clean_html(raw_desc)[:320]
                image = extract_image(item, raw_desc)
                cves = extract_cves(f"{title} {snippet}")
                category = categorize(title, snippet, feed_info["name"])

                item_id = f"{feed_info['name']}:{link}"
                articles.append({
                    "id": item_id,
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "category": category,
                    "cves": cves,
                    "image": image,
                    "source": feed_info["name"],
                    "icon": feed_info["icon"]
                })
        else:
            # Check Atom (<feed><entry>)
            entries = root.findall(".//{http://www.w3.org/2005/Atom}entry") or root.findall(".//entry")
            for entry in entries:
                title_el = entry.find("{http://www.w3.org/2005/Atom}title") or entry.find("title")
                link_el = entry.find("{http://www.w3.org/2005/Atom}link") or entry.find("link")
                summary_el = entry.find("{http://www.w3.org/2005/Atom}summary") or entry.find("summary") or entry.find("content")

                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                link = ""
                if link_el is not None:
                    link = link_el.attrib.get("href", "") or (link_el.text.strip() if link_el.text else "")
                raw_desc = summary_el.text if summary_el is not None and summary_el.text else ""

                if not title or not link:
                    continue

                snippet = clean_html(raw_desc)[:320]
                image = extract_image(entry, raw_desc)
                cves = extract_cves(f"{title} {snippet}")
                category = categorize(title, snippet, feed_info["name"])

                item_id = f"{feed_info['name']}:{link}"
                articles.append({
                    "id": item_id,
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "category": category,
                    "cves": cves,
                    "image": image,
                    "source": feed_info["name"],
                    "icon": feed_info["icon"]
                })
    except Exception as e:
        print(f"[-] XML Parse error for {feed_info['name']}: {e}", file=sys.stderr)

    return articles

def escape_html(text):
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def send_telegram(item):
    if not BOT_TOKEN or not CHAT_ID:
        print("[!] Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be configured in GitHub Secrets!")
        return False

    cve_str = f"\n🔴 <b>CVEs:</b> {', '.join(item['cves'])}" if item["cves"] else ""
    safe_title = escape_html(item["title"])
    safe_snippet = escape_html(item["snippet"])
    safe_source = escape_html(item["source"])
    safe_cat = escape_html(item["category"])

    message_text = (
        f"🚨 <b>CYBERPULSE INTEL ALERT</b> 🚨\n\n"
        f"<b>{safe_title}</b>\n\n"
        f"📁 <b>Category:</b> {safe_cat}\n"
        f"📡 <b>Source:</b> {item['icon']} {safe_source}{cve_str}\n\n"
        f"📝 <b>Intel Brief:</b>\n{safe_snippet}\n\n"
        f"🔗 <a href=\"{item['link']}\">Read Full Story</a>"
    )

    keyboard = {
        "inline_keyboard": [
            [{"text": "🌐 Read Full Story", "url": item["link"]}]
        ]
    }

    # Try sendPhoto if image exists
    if item.get("image") and item["image"].startswith("http"):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            payload = {
                "chat_id": CHAT_ID,
                "photo": item["image"],
                "caption": message_text[:1024],
                "parse_mode": "HTML",
                "reply_markup": keyboard
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return True
        except Exception as e:
            print(f"[-] sendPhoto failed ({e}), falling back to sendMessage...")

    # Fallback to sendMessage
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
            "reply_markup": keyboard
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[-] sendMessage failed: {e}", file=sys.stderr)
        return False

def main():
    print("====================================================")
    print("🛡️  CyberPulse • Expanded Threat Intel & Tools Bot")
    print(f"⏰ Execution Time: {datetime.now(timezone.utc).isoformat()} UTC")
    print(f"📡 Monitored Feeds: {len(FEEDS)} Sources (News, Tools, AI, Research)")
    print("====================================================")

    if not BOT_TOKEN or not CHAT_ID:
        print("[!] Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in GitHub Repository Secrets.")
        print("[!] Please add them under: Settings -> Secrets and variables -> Actions")
        sys.exit(0)

    history = load_history()
    seen_ids = set(history)
    print(f"[+] Loaded {len(seen_ids)} previously sent article IDs from history.")

    all_articles = []
    for feed in FEEDS:
        print(f"[+] Scraping: {feed['name']}...")
        arts = parse_feed(feed)
        all_articles.extend(arts)

    print(f"[+] Total live articles scraped across all sources: {len(all_articles)}")

    # Filter unread articles
    unread = [a for a in all_articles if a["id"] not in seen_ids]
    print(f"[+] Found {len(unread)} new unread articles.")

    if FILTER_MODE == "zerodays_only":
        unread = [a for a in unread if "Zero-Days" in a["category"] or a["cves"]]
        print(f"[+] Filtered for Zero-Days only: {len(unread)} remaining.")

    sent_count = 0
    for article in unread[:MAX_SEND]:
        print(f"[*] Dispatching: [{article['category']}] {article['title'][:45]}...")
        if send_telegram(article):
            history.append(article["id"])
            sent_count += 1
        else:
            print(f"[-] Failed to send: {article['title']}")

    print(f"[✓] Successfully sent {sent_count} new articles to Telegram!")
    save_history(history)

if __name__ == "__main__":
    main()
