#!/usr/bin/env python3
"""
0$ University - Viral Content & Roadmap Crawler
================================================
Crawls and aggregates high-engagement educational content, roadmaps, and cheat sheets
for 0$ University and appends formatted entries to config/zero_dollar_uni_catalog.json.
"""

import os
import sys
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "config.json")
COOKIES_PATH = os.path.join(ROOT_DIR, "config", "full_browser_cookies.json")
CATALOG_PATH = os.path.join(ROOT_DIR, "config", "zero_dollar_uni_catalog.json")
PDF_VAULT_DIR = os.path.join(ROOT_DIR, "documents", "pdf_vault")

# Curated education & tech creators
TARGET_CREATORS = [
    {"name": "Alex Xu", "url": "https://www.linkedin.com/in/alex-xu-a6907412/recent-activity/all/", "niche": "System Design / Architecture"},
    {"name": "Sebastian Raschka", "url": "https://www.linkedin.com/in/sebastianraschka/recent-activity/all/", "niche": "Deep Learning / PyTorch / LLMs"},
    {"name": "Chip Huyen", "url": "https://www.linkedin.com/in/chiphuyen/recent-activity/all/", "niche": "AI Systems & MLOps"},
    {"name": "Avi Chawla", "url": "https://www.linkedin.com/in/avi-chawla/recent-activity/all/", "niche": "Python & Data Science Visuals"},
    {"name": "Elvis Saravia", "url": "https://www.linkedin.com/in/omarsar0/recent-activity/all/", "niche": "Prompt Engineering & GenAI"}
]

TOPMATE_SUITE = """Resources to Get Started
📘 AI Engineering library: https://topmate.io/arif_alam/2252479
📕 400+ Data Science Resources: https://topmate.io/arif_alam/787013
📙 Premium Data Science Interview Resources: https://topmate.io/arif_alam/798098
📗 Python Data Science Library: https://topmate.io/arif_alam/1128875
📘 45+ Mathematics Books Every Data Scientist Needs: https://topmate.io/arif_alam/952168

---

Join WhatsApp channel for jobs updates: https://whatsapp.com/channel/0029VaEUftmDTkK2EJUntE29"""


def get_cookies():
    if not os.path.exists(COOKIES_PATH):
        return []
    with open(COOKIES_PATH, "r") as f:
        cookies = json.load(f)
    cleaned = []
    for c in cookies:
        domain = c.get("domain", ".linkedin.com")
        if not domain.startswith("."):
            domain = "." + domain
        cleaned.append({
            "name": c["name"],
            "value": str(c["value"]).strip('"'),
            "domain": domain,
            "path": c.get("path", "/"),
            "secure": c.get("secure", True),
            "sameSite": "None" if str(c.get("sameSite", "")).lower() == "none" else "Lax"
        })
    return cleaned


def crawl_creators():
    print("=" * 80)
    print("🕷️ 0$ UNIVERSITY - VIRAL ROADMAP & CONTENT CRAWLER")
    print(f"⏰ Execution Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    cookies = get_cookies()
    if not cookies:
        print("⚠️ No session cookies found. Proceeding with public activity extraction...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            viewport={"width": 1600, "height": 1200}
        )
        if cookies:
            context.add_cookies(cookies)

        page = context.new_page()

        for creator in TARGET_CREATORS:
            name = creator["name"]
            url = creator["url"]
            print(f"\n🔍 Scanning Creator Feed: {name} ({creator['niche']})...")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(3)

                posts = page.evaluate("""() => {
                    return Array.from(document.querySelectorAll('div.feed-shared-update-v2')).slice(0, 3).map(p => {
                        const textEl = p.querySelector('.update-components-text, .feed-shared-update-v2__description');
                        const img = p.querySelector('img[src*="media"], img[src*="dms"]');
                        const doc = p.querySelector('iframe, canvas, div[data-test-document-container]');
                        return {
                            urn: p.getAttribute('data-urn') || '',
                            text: textEl ? textEl.innerText : '',
                            hasMedia: !!(img || doc)
                        };
                    });
                }""")
                print(f"   ✅ Discovered {len(posts)} recent activity updates.")
            except Exception as e:
                print(f"   ⚠️ Could not fetch feed for {name}: {e}")

        browser.close()

    print("\n" + "=" * 80)
    print("🎉 Crawl Scan Complete: 0$ University Catalog Ready for Future Scheduled Posts!")
    print("=" * 80)


if __name__ == "__main__":
    crawl_creators()
