#!/usr/bin/env python3
"""
=============================================================================
CYBERPULSE • CYBERSECURITY THREAT INTEL & TELEGRAM BROADCASTER
=============================================================================
Features:
1. 7-Day Lookback Window: Captures all major & trending news from the past week.
2. 18+ Global & Indian Feeds: India (CERT-In, Cybercrime), US (CISA), UK (NCSC),
   AI Security, Hacker Tools (Flipper Zero, SDR), & Deep Research.
3. Trending Priority Scoring: Prioritizes critical 0-days, major breaches & exploits.
4. Randomized 30-45 Min Intervals: Avoids fixed schedules and rate limits.
5. Anti-Flood Telegram Pacing: Gentle delay between messages to prevent spam bans.
=============================================================================
"""

import os
import sys
import json
import re
import time
import random
import email.utils
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# =============================================================================
# SECTION 1: HELPER FUNCTIONS (ID & STRING CLEANING)
# =============================================================================

def clean_chat_id(raw_id):
    """
    Cleans and formats Telegram Chat IDs.
    Accepts: '@my_channel', 'my_channel', 'https://t.me/my_channel', '-100123456789'
    Returns: Standardized '@my_channel' or numeric string '-100123456789'
    """
    if not raw_id:
        return ""
    raw_id = raw_id.strip().strip("'\"")
    # If the user pasted a full link like https://t.me/Cyber_pulse_News
    if "t.me/" in raw_id:
        raw_id = "@" + raw_id.split("t.me/")[-1].strip("/@")
    # If it's a public handle without '@' and not numeric
    elif not raw_id.startswith("@") and not raw_id.startswith("-") and not raw_id.isdigit():
        raw_id = "@" + raw_id
    return raw_id

def escape_html(text):
    """Escapes special HTML characters for Telegram's HTML parse mode."""
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def clean_html(raw_html):
    """Strips HTML tags and normalizes whitespace into readable text."""
    if not raw_html:
        return ""
    clean = re.sub(r"<[^>]+>", " ", raw_html)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

# =============================================================================
# SECTION 2: CONFIGURATION & CREDENTIALS
# =============================================================================

# Read secrets from GitHub Actions environment variables
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip().strip("'\"")
CHAT_ID = clean_chat_id(os.environ.get("TELEGRAM_CHAT_ID", ""))
FILTER_MODE = os.environ.get("FILTER_MODE", "all").strip().lower() # 'all', 'zerodays_only', 'india_only'
MAX_SEND = int(os.environ.get("MAX_SEND", "6")) # Number of articles to send per run

# File to remember already sent articles (prevents duplicate spam)
HISTORY_FILE = "sent_history.json"

# How many days back to look for news (7 days = 1 full week)
LOOKBACK_DAYS = 7

# =============================================================================
# SECTION 3: MONITORED RSS / ATOM FEEDS (18+ SOURCES)
# =============================================================================

FEEDS = [
    # --- 🇮🇳 INDIA & REGIONAL SOURCES ---
    {
        "name": "The420 Cyber News India",
        "url": "https://www.the420.in/feed/",
        "icon": "🇮🇳",
        "default_region": "🇮🇳 India"
    },
    {
        "name": "Cyber Security News (India & Global)",
        "url": "https://cybersecuritynews.com/feed/",
        "icon": "🛡️",
        "default_region": "🇮🇳 India / Global"
    },
    {
        "name": "GBHackers InfoSec",
        "url": "https://gbhackers.com/feed/",
        "icon": "⚡",
        "default_region": "🇮🇳 India / Global"
    },

    # --- 🇺🇸 US & 🇬🇧 UK GOVERNMENT THREAT ADVISORIES ---
    {
        "name": "CISA Advisories (US)",
        "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
        "icon": "🚨",
        "default_region": "🇺🇸 United States"
    },
    {
        "name": "NCSC UK Alerts (UK)",
        "url": "https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml",
        "icon": "🇬🇧",
        "default_region": "🇬🇧 United Kingdom"
    },

    # --- 🌐 GLOBAL BREAKING NEWS & ZERO-DAYS ---
    {
        "name": "The Hacker News",
        "url": "https://feeds.feedburner.com/TheHackersNews",
        "icon": "⚡",
        "default_region": "🌐 Global"
    },
    {
        "name": "Dark Reading",
        "url": "https://www.darkreading.com/rss.xml",
        "icon": "👁️",
        "default_region": "🌐 Global"
    },
    {
        "name": "The Register Security",
        "url": "https://www.theregister.com/security/headlines.atom",
        "icon": "🪓",
        "default_region": "🌐 Global"
    },
    {
        "name": "Krebs on Security",
        "url": "https://krebsonsecurity.com/feed/",
        "icon": "🛡️",
        "default_region": "🌐 Global"
    },
    {
        "name": "SecurityWeek",
        "url": "https://www.securityweek.com/feed/",
        "icon": "🌐",
        "default_region": "🌐 Global"
    },
    {
        "name": "Security Affairs",
        "url": "https://securityaffairs.com/feed",
        "icon": "🕵️",
        "default_region": "🌐 Global"
    },
    {
        "name": "SANS Internet Storm Center",
        "url": "https://isc.sans.edu/rssfeed.xml",
        "icon": "⛈️",
        "default_region": "🌐 Global"
    },

    # --- 🥷 SECURITY ENGINEERING & DEEP RESEARCH ---
    {
        "name": "PortSwigger Web Security Research",
        "url": "https://portswigger.net/research/rss",
        "icon": "🧪",
        "default_region": "🌐 Global"
    },
    {
        "name": "Cisco Talos Threat Intel",
        "url": "https://blog.talosintelligence.com/rss/",
        "icon": "🎯",
        "default_region": "🌐 Global"
    },
    {
        "name": "Microsoft Security Blog",
        "url": "https://www.microsoft.com/en-us/security/blog/feed/",
        "icon": "🏢",
        "default_region": "🌐 Global"
    },
    {
        "name": "Cloudflare Security",
        "url": "https://blog.cloudflare.com/tag/security/rss/",
        "icon": "☁️",
        "default_region": "🌐 Global"
    },

    # --- 🛠️ HACKER TOOLS, GADGETS & HARDWARE HACKS ---
    {
        "name": "Hackaday Security Hacks",
        "url": "https://hackaday.com/category/security-hacks/feed/",
        "icon": "🛠️",
        "default_region": "🌐 Global"
    },
    {
        "name": "Help Net Security",
        "url": "https://www.helpnetsecurity.com/feed/",
        "icon": "🔐",
        "default_region": "🌐 Global"
    }
]

# =============================================================================
# SECTION 4: DATE PARSING & 7-DAY FILTER
# =============================================================================

def parse_pub_date(date_str):
    """
    Parses various RSS/Atom date formats (RFC 2822, ISO 8601, UTC).
    Returns a timezone-aware datetime object in UTC.
    """
    if not date_str:
        return datetime.now(timezone.utc)
    
    # Try RFC 2822 format (e.g. 'Tue, 25 Aug 2026 10:00:00 GMT')
    try:
        dt = email.utils.parsedate_to_datetime(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # Try ISO 8601 format (e.g. '2026-08-25T10:00:00Z')
    try:
        clean = date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    return datetime.now(timezone.utc)

# =============================================================================
# SECTION 5: THREAT CATEGORIZATION & REGION DETECTION
# =============================================================================

def extract_cves(text):
    """Extracts unique CVE identifiers (e.g. CVE-2024-38856)."""
    matches = re.findall(r"CVE-\d{4}-\d{4,7}", text, re.IGNORECASE)
    return list(dict.fromkeys([m.upper() for m in matches]))

def detect_region(title, snippet, feed_info):
    """Detects the geographical region based on content and source."""
    text = f"{title} {snippet} {feed_info.get('name', '')}".lower()

    # 1. India Keywords
    if any(k in text for k in [
        "india", "indian", "cert-in", "delhi", "mumbai", "bengaluru", "bangalore", "hyderabad",
        "rbi", "sebi", "upi", "aadhaar", "cbi", "cyber cell", "the420", "patna", "noida", "gurugram",
        "chennai", "kolkata", "pune", "meity", "i4c", "dpdp"
    ]) or "The420" in feed_info.get("name", ""):
        return "🇮🇳 India"

    # 2. United States Keywords
    if any(k in text for k in ["cisa", "fbi", "nsa", "white house", "pentagon", "united states", "u.s.", "doj", "treasury"]) or "CISA" in feed_info.get("name", ""):
        return "🇺🇸 United States"

    # 3. United Kingdom Keywords
    if any(k in text for k in ["ncsc", "uk", "gchq", "london", "britain", "england", "british"]) or "NCSC" in feed_info.get("name", ""):
        return "🇬🇧 United Kingdom"

    # 4. Europe Keywords
    if any(k in text for k in ["european union", "eu ", "enisa", "gdpr", "germany", "france", "netherlands", "bsi", "anssi"]):
        return "🇪🇺 Europe"

    # 5. Asia-Pacific Keywords
    if any(k in text for k in ["australia", "acsc", "singapore", "singcert", "japan", "jpcert", "taiwan", "south korea"]):
        return "🌏 Asia-Pacific"

    # Fallback to feed's default region
    return feed_info.get("default_region", "🌐 Global")

def categorize(title, snippet, source_name=""):
    """Categorizes the story into one of the core cybersecurity topics."""
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
    if re.search(r"cisa|cert-in|fbi|nsa|advisory|directive|homeland security|kev catalog", text):
        return "🚨 CISA & CERT Advisories"

    # 8. Cloud & Supply Chain
    if re.search(r"aws|azure|cloud|kubernetes|docker|github|npm|pypi|supply chain", text):
        return "🌐 Cloud & DevSecOps"

    # 9. Nation-State & APT
    if re.search(r"apt|nation-state|china|russia|north korea|iran|espionage|cozy bear|sandworm", text):
        return "⚔️ Nation-State & APT"

    return "🛡️ Cybersecurity"

def calculate_priority_score(item, now_utc):
    """
    Scores articles based on impact and recency (within the 7-day lookback window).
    Major & trending stories (0-days, major breaches, Indian CERT-In, AI hacks) rank highest.
    """
    score = 0

    # Boost for Critical Zero-Days & CVEs
    if item["cves"] or "Zero-Days" in item["category"]:
        score += 50

    # Boost for Major Indian Cybercrime & CERT-In News
    if "India" in item["region"]:
        score += 40

    # Boost for Ransomware & Extortion Campaigns
    if "Ransomware" in item["category"]:
        score += 35

    # Boost for AI Security & LLM Hacks
    if "AI Security" in item["category"]:
        score += 30

    # Boost for Hacker Gadgets & Hardware
    if "Tools" in item["category"]:
        score += 25

    # Boost for Security Engineering Research
    if "Engineering" in item["category"]:
        score += 25

    # Recency weighting: Newer articles within the 7-day window receive extra points
    days_old = max(0, (now_utc - item["pub_dt"]).total_seconds() / 86400)
    score += max(0, int((7 - days_old) * 5))

    return score

# =============================================================================
# SECTION 6: FEED FETCHER & XML PARSER
# =============================================================================

def fetch_url(url):
    """Downloads raw content from a URL with custom User-Agent and timeout."""
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

def extract_image(item_xml, raw_desc):
    """Extracts hero image from RSS enclosures, media tags, or <img> in description."""
    # 1. Enclosure tag (<enclosure url="...">)
    enclosure = item_xml.find("enclosure")
    if enclosure is not None and "url" in enclosure.attrib:
        url = enclosure.attrib["url"]
        if not url.endswith(".mp3") and not url.endswith(".wav"):
            return url

    # 2. Media content or thumbnail tag (<media:content url="...">)
    for tag in ["{http://search.yahoo.com/mrss/}content", "{http://search.yahoo.com/mrss/}thumbnail"]:
        media = item_xml.find(tag)
        if media is not None and "url" in media.attrib:
            return media.attrib["url"]

    # 3. <img> tag inside HTML description
    if raw_desc:
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', raw_desc, re.IGNORECASE)
        if match:
            src = match.group(1)
            if "feedburner" not in src and "doubleclick" not in src and "gravatar" not in src and not src.endswith(".gif"):
                return src
    return None

def parse_feed(feed_info, cutoff_dt):
    """
    Parses an RSS or Atom feed and extracts articles published within the 7-day lookback window.
    """
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
                date_el = item.find("pubDate")
                if date_el is None:
                    date_el = item.find("{http://purl.org/dc/elements/1.1/}date")

                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                link = link_el.text.strip() if link_el is not None and link_el.text else ""
                raw_desc = desc_el.text if desc_el is not None and desc_el.text else ""
                raw_date = date_el.text if date_el is not None and date_el.text else ""

                if not title or not link:
                    continue

                # Parse publication date and apply 7-Day Lookback Filter
                pub_dt = parse_pub_date(raw_date)
                if pub_dt < cutoff_dt:
                    continue # Skip articles older than 7 days

                snippet = clean_html(raw_desc)[:320]
                image = extract_image(item, raw_desc)
                cves = extract_cves(f"{title} {snippet}")
                category = categorize(title, snippet, feed_info["name"])
                region = detect_region(title, snippet, feed_info)

                item_id = f"{feed_info['name']}:{link}"
                articles.append({
                    "id": item_id,
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "category": category,
                    "region": region,
                    "cves": cves,
                    "image": image,
                    "source": feed_info["name"],
                    "icon": feed_info["icon"],
                    "pub_dt": pub_dt
                })
        else:
            # Check Atom (<feed><entry>)
            entries = root.findall(".//{http://www.w3.org/2005/Atom}entry") or root.findall(".//entry")
            for entry in entries:
                title_el = entry.find("{http://www.w3.org/2005/Atom}title") or entry.find("title")
                link_el = entry.find("{http://www.w3.org/2005/Atom}link") or entry.find("link")
                summary_el = entry.find("{http://www.w3.org/2005/Atom}summary") or entry.find("summary") or entry.find("content")
                date_el = entry.find("{http://www.w3.org/2005/Atom}updated")
                if date_el is None:
                    date_el = entry.find("{http://www.w3.org/2005/Atom}published")
                if date_el is None:
                    date_el = entry.find("updated")

                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                link = ""
                if link_el is not None:
                    link = link_el.attrib.get("href", "") or (link_el.text.strip() if link_el.text else "")
                raw_desc = summary_el.text if summary_el is not None and summary_el.text else ""
                raw_date = date_el.text if date_el is not None and date_el.text else ""

                if not title or not link:
                    continue

                # Parse publication date and apply 7-Day Lookback Filter
                pub_dt = parse_pub_date(raw_date)
                if pub_dt < cutoff_dt:
                    continue # Skip articles older than 7 days

                snippet = clean_html(raw_desc)[:320]
                image = extract_image(entry, raw_desc)
                cves = extract_cves(f"{title} {snippet}")
                category = categorize(title, snippet, feed_info["name"])
                region = detect_region(title, snippet, feed_info)

                item_id = f"{feed_info['name']}:{link}"
                articles.append({
                    "id": item_id,
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "category": category,
                    "region": region,
                    "cves": cves,
                    "image": image,
                    "source": feed_info["name"],
                    "icon": feed_info["icon"],
                    "pub_dt": pub_dt
                })
    except Exception as e:
        print(f"[-] XML Parse error for {feed_info['name']}: {e}", file=sys.stderr)

    return articles

# =============================================================================
# SECTION 7: TELEGRAM DISPATCHER & MESSAGE FORMATTER
# =============================================================================

def send_telegram(item):
    """
    Sends formatted threat intel bulletin to Telegram channel/chat.
    Tries sendPhoto first (with image), falling back to sendMessage.
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("[!] Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be configured in GitHub Secrets!")
        return False

    cve_str = f"\n🔴 <b>CVEs:</b> {', '.join(item['cves'])}" if item["cves"] else ""
    safe_title = escape_html(item["title"])
    safe_snippet = escape_html(item["snippet"])
    safe_source = escape_html(item["source"])
    safe_cat = escape_html(item["category"])
    safe_region = escape_html(item["region"])
    
    # Format relative date (e.g. "Aug 25, 2026")
    date_formatted = item["pub_dt"].strftime("%b %d, %Y")

    message_text = (
        f"🚨 <b>CYBERPULSE INTEL ALERT</b> 🚨\n\n"
        f"<b>{safe_title}</b>\n\n"
        f"📁 <b>Category:</b> {safe_cat}\n"
        f"🌍 <b>Region:</b> {safe_region}\n"
        f"📡 <b>Source:</b> {item['icon']} {safe_source} • {date_formatted}{cve_str}\n\n"
        f"📝 <b>Intel Brief:</b>\n{safe_snippet}\n\n"
        f"🔗 <a href=\"{item['link']}\">Read Full Story</a>"
    )

    keyboard = {
        "inline_keyboard": [
            [{"text": "🌐 Read Full Story", "url": item["link"]}]
        ]
    }

    # 1. Try sendPhoto if valid image URL is present
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
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    return True
        except Exception as e:
            print(f"[-] sendPhoto failed ({e}), falling back to sendMessage...")

    # 2. Fallback to sendMessage
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
        with urllib.request.urlopen(req, timeout=12) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[-] sendMessage failed: {e}", file=sys.stderr)
        return False

# =============================================================================
# SECTION 8: MAIN EXECUTION ENGINE
# =============================================================================

def main():
    now_utc = datetime.now(timezone.utc)
    cutoff_7_days = now_utc - timedelta(days=LOOKBACK_DAYS)
    
    # Peak traffic detection: 06:00 to 18:00 UTC (active daytime across Asia, Europe, US)
    is_peak_time = (6 <= now_utc.hour <= 18)

    print("===================================================================")
    print("🛡️  CyberPulse • 7-Day Threat Intel & Telegram Broadcaster")
    print(f"⏰ Execution Time: {now_utc.isoformat()} UTC")
    print(f"📅 Lookback Window: Past {LOOKBACK_DAYS} Days (Since {cutoff_7_days.strftime('%Y-%m-%d')})")
    print(f"📡 Peak Hours Active: {'YES (Throttled Pacing)' if is_peak_time else 'NO (Normal Speed)'}")
    print(f"🌐 Monitored Feeds: {len(FEEDS)} Global & Indian Sources")
    print("===================================================================")

    if not BOT_TOKEN or not CHAT_ID:
        print("[!] Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in GitHub Repository Secrets.")
        print("[!] Please add them under: Settings -> Secrets and variables -> Actions")
        sys.exit(0)

    # 1. Randomized startup jitter (3 to 10 seconds) to avoid rigid execution spikes
    jitter = random.uniform(3.0, 10.0)
    print(f"[+] Initial randomized startup jitter: {jitter:.1f}s...")
    time.sleep(jitter)

    # 2. Load already-sent article history
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
    seen_ids = set(history)
    print(f"[+] Loaded {len(seen_ids)} previously dispatched article IDs from history.")

    # 3. Scrape all feeds for articles within the 7-day lookback window
    all_articles = []
    for feed in FEEDS:
        print(f"[+] Scraping: {feed['name']}...")
        arts = parse_feed(feed, cutoff_7_days)
        all_articles.extend(arts)

    print(f"[+] Total articles collected within 7-day window: {len(all_articles)}")

    # 4. Deduplicate unread articles
    unread = [a for a in all_articles if a["id"] not in seen_ids]
    print(f"[+] Found {len(unread)} unread articles from the past week.")

    # 5. Apply custom filter modes if configured
    if FILTER_MODE == "zerodays_only":
        unread = [a for a in unread if "Zero-Days" in a["category"] or a["cves"]]
        print(f"[+] Filtered for Zero-Days only: {len(unread)} remaining.")
    elif FILTER_MODE == "india_only":
        unread = [a for a in unread if "India" in a["region"]]
        print(f"[+] Filtered for India only: {len(unread)} remaining.")

    # 6. Priority & Trending Scoring: Sort highest priority stories first
    unread.sort(key=lambda item: calculate_priority_score(item, now_utc), reverse=True)

    # 7. Dispatch top stories with anti-flood pacing
    sent_count = 0
    for article in unread[:MAX_SEND]:
        print(f"[*] Dispatching: [{article['region']}] [{article['category']}] {article['title'][:40]}...")
        if send_telegram(article):
            history.append(article["id"])
            sent_count += 1

            # Anti-flood delay: 2.5-4.5s during peak hours; 1.2-2.0s off-peak
            pacing_delay = random.uniform(2.5, 4.5) if is_peak_time else random.uniform(1.2, 2.0)
            time.sleep(pacing_delay)
        else:
            print(f"[-] Failed to send: {article['title']}")

    print(f"[✓] Successfully dispatched {sent_count} major/trending articles to Telegram!")

    # 8. Save updated history (keep latest 500 entries)
    if len(history) > 500:
        history = history[-500:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

if __name__ == "__main__":
    main()
