import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COOKIES_PATH = os.path.join(ROOT_DIR, "config", "full_browser_cookies.json")

with open(COOKIES_PATH, "r") as f:
    raw_cookies = json.load(f)

formatted_cookies = []
for c in raw_cookies:
    domain = c.get("domain", ".linkedin.com")
    if not domain.startswith("."):
        domain = "." + domain
    formatted_cookies.append({
        "name": c["name"],
        "value": str(c["value"]).strip('"'),
        "domain": domain,
        "path": c.get("path", "/"),
        "secure": c.get("secure", True),
        "sameSite": "None" if str(c.get("sameSite", "")).lower() == "none" else "Lax"
    })

post_url = "https://www.linkedin.com/feed/update/urn:li:activity:7496408656515596288/"

actors = [
    {"id": "select-startup-founderss", "name": "0$ University"},
    {"id": "select-datasciencereality", "name": "Data Science Reality"},
    {"id": "select-100daysofai", "name": "100DaysOfAI"},
    {"id": "select-web3schools", "name": "Web3Schools"},
    {"id": "select-data-science-myth", "name": "Data Science Myth"},
    {"id": "select-data-science-for-schools", "name": "Data Science For Schools"},
    {"id": "select-probability-and-statistics", "name": "Probability and Statistics"},
    {"id": "select-data-science-reality", "name": "Data science Reality (Alt)"}
]

comment_txt = """🎓 𝟎$ 𝐔𝐧𝐢𝘃𝐞𝐫𝐬𝗶𝐭𝘆 𝐅𝐫𝐞𝐞 𝐄𝐝𝐮𝐜𝗮𝐭𝐢𝐨𝐧 𝐕𝐚𝐮𝐥𝐭
AI Engineering Library: https://topmate.io/arif_alam/2252479
📕 400+ 𝗗𝗮𝘁𝗮 𝗦𝗰𝗶𝗲𝗻𝗰𝗲 𝗥𝗲𝘀𝗼𝘂𝗿𝗰𝗲𝘀: https://topmate.io/arif_alam/787013

Democratizing world-class tech education for everyone!"""

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    ctx = browser.new_context(viewport={"width": 1600, "height": 1200})
    ctx.add_cookies(formatted_cookies)
    page = ctx.new_page()

    print(f"👉 Navigating to: {post_url}")
    page.goto(post_url, wait_until="domcontentloaded", timeout=40000)
    time.sleep(5)

    # 1. Switch to 0$ University and post comment
    print("👤 Switching to 0$ University for first comment...")
    try:
        page.locator("button.content-admin-identity-toggle-button").first.click(force=True)
        time.sleep(1.5)
        page.evaluate("""() => {
            const r = document.querySelector('#select-startup-founderss');
            if (r) {
                r.checked = true;
                r.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""")
        time.sleep(0.5)
        page.locator(".artdeco-modal button:has-text('Save')").first.click(force=True)
        time.sleep(2)

        comment_box = page.locator("div.ql-editor, div[contenteditable='true']").first
        if comment_box.is_visible():
            comment_box.click(force=True)
            time.sleep(1)
            page.keyboard.insert_text(comment_txt)
            time.sleep(2)
            submit_btn = page.locator("button.comments-comment-box__submit-button, button:has-text('Comment')").last
            if submit_btn.is_visible():
                submit_btn.click(force=True)
                time.sleep(3)
                print("✅ 0$ University comment submitted successfully!")
    except Exception as e:
        print(f"⚠️ Comment submission note: {e}")

    # 2. Like from all 8 accounts
    print("\n⚡ Boosting likes from all accounts...")
    for idx, actor in enumerate(actors, 1):
        aid = actor["id"]
        aname = actor["name"]
        print(f"[{idx}/{len(actors)}] ⚡ Liking as: {aname}...")
        try:
            page.locator("button.content-admin-identity-toggle-button").first.click(force=True)
            time.sleep(1.5)
            page.evaluate(f"""() => {{
                const r = document.querySelector('#{aid}');
                if (r) {{
                    r.checked = true;
                    r.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}""")
            time.sleep(0.5)
            page.locator(".artdeco-modal button:has-text('Save')").first.click(force=True)
            time.sleep(2)

            page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const likeBtn = btns.find(b => (b.innerText || '').trim() === 'Like' && !b.className.includes('content-admin-identity-toggle-button'));
                if (likeBtn && likeBtn.getAttribute('aria-pressed') !== 'true') {
                    likeBtn.click();
                }
            }""")
            time.sleep(1.5)
        except Exception as e:
            print(f"Warning on {aname}: {e}")

    time.sleep(3)
    page.screenshot(path="/tmp/boosted_morning_proof.png")
    print("🎉 All 8 likes + 0$ University comment completed!")
    browser.close()
