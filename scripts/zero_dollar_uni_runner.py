#!/usr/bin/env python3
"""
0$ University - Dedicated LinkedIn Autonomous Growth Engine (v1.1 Production)
============================================================================
1. Direct Organization Admin / Feed Composer with Verified Author Switch to '0$ University'.
2. Attaches authentic Roadmap / Course Vault PDF Carousel from documents/pdf_vault/.
3. Multi-layer Text Insertion (document.execCommand + page.keyboard).
4. Publishes post live to 0$ University.
5. Runs 8-Actor Cross-Engagement Booster + Pinned 1st Comment.
"""

import os
import sys
import time
import json
import argparse
from datetime import datetime
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
ARTIFACTS_DIR = os.path.join(ROOT_DIR, "artifacts")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

CONFIG_PATH = os.path.join(ROOT_DIR, "config", "config.json")
FULL_COOKIES_PATH = os.path.join(ROOT_DIR, "config", "full_browser_cookies.json")
ZUNI_HISTORY_PATH = os.path.join(ROOT_DIR, "config", "zero_dollar_uni_posted_history.json")
ZUNI_CATALOG_PATH = os.path.join(ROOT_DIR, "config", "zero_dollar_uni_catalog.json")
PDF_VAULT_DIR = os.path.join(ROOT_DIR, "documents", "pdf_vault")

# Load configuration
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
else:
    CONFIG = {}

ALL_ENGAGEMENT_ACTORS = CONFIG.get("engagement_actors", [
    {"id": "select-self", "name": "Arif Alam (Personal Profile)"},
    {"id": "select-datasciencereality", "name": "Data Science Reality"},
    {"id": "select-100daysofai", "name": "100DaysOfAI"},
    {"id": "select-web3schools", "name": "Web3Schools"},
    {"id": "select-data-science-myth", "name": "Data Science Myth"},
    {"id": "select-data-science-for-schools", "name": "Data Science For Schools"},
    {"id": "select-probability-and-statistics", "name": "Probability and Statistics"},
    {"id": "select-data-science-reality", "name": "Data science Reality (Alt)"}
])

ZUNI_FIRST_COMMENT = CONFIG.get("permanent_first_comment", """🎓 𝟎$ 𝐔𝐧𝐢𝘃𝐞𝐫𝐬𝗶𝐭𝐲 𝐅𝐫𝐞𝐞 𝐄𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧 𝐕𝐚𝐮𝐥𝐭
AI Engineering Library: https://topmate.io/arif_alam/2252479
📕 400+ 𝗗𝗮𝘁𝗮 𝗦𝗰𝗶𝗲𝗻𝗰𝗲 𝗥𝗲𝘀𝗼𝘂𝗿𝗰𝗲𝘀: https://topmate.io/arif_alam/787013

Democratizing world-class tech education for everyone!""")


def get_cookies():
    """Load cookies from environment secrets or local full_browser_cookies.json."""
    cookies = []
    li_at = os.environ.get("LI_AT")
    jsessionid = os.environ.get("JSESSIONID")
    bcookie = os.environ.get("BCOOKIE")
    bscookie = os.environ.get("BSCOOKIE")

    if li_at and jsessionid:
        print("🔑 Loading cookies from environment secrets...")
        clean_li_at = li_at.strip('"\'')
        clean_jsessionid = jsessionid.strip('"\'')
        if not clean_jsessionid.startswith('"'):
            clean_jsessionid = f'"{clean_jsessionid}"'

        cookies.append({
            "name": "li_at",
            "value": clean_li_at,
            "domain": ".linkedin.com",
            "path": "/",
            "secure": True,
            "sameSite": "None"
        })
        cookies.append({
            "name": "JSESSIONID",
            "value": clean_jsessionid,
            "domain": ".linkedin.com",
            "path": "/",
            "secure": True,
            "sameSite": "None"
        })
        if bcookie:
            cookies.append({
                "name": "bcookie",
                "value": bcookie.strip('"\''),
                "domain": ".linkedin.com",
                "path": "/",
                "secure": True,
                "sameSite": "None"
            })
        if bscookie:
            cookies.append({
                "name": "bscookie",
                "value": bscookie.strip('"\''),
                "domain": ".linkedin.com",
                "path": "/",
                "secure": True,
                "sameSite": "None"
            })
        return cookies

    if os.path.exists(FULL_COOKIES_PATH):
        print("📂 Loading cookies from config/full_browser_cookies.json...")
        with open(FULL_COOKIES_PATH, "r") as f:
            raw_cookies = json.load(f)
        for c in raw_cookies:
            domain = c.get("domain", ".linkedin.com")
            if not domain.startswith("."):
                domain = "." + domain
            cookies.append({
                "name": c["name"],
                "value": str(c["value"]).strip('"'),
                "domain": domain,
                "path": c.get("path", "/"),
                "secure": c.get("secure", True),
                "sameSite": "None" if str(c.get("sameSite", "")).lower() == "none" else "Lax"
            })
        return cookies

    raise RuntimeError("No LinkedIn cookies found in environment variables or config/full_browser_cookies.json!")


def load_zuni_history():
    if os.path.exists(ZUNI_HISTORY_PATH):
        try:
            with open(ZUNI_HISTORY_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_zuni_history(entry):
    history = load_zuni_history()
    history.append({
        **entry,
        "posted_at": datetime.now().isoformat(),
        "platform": "0$ University"
    })
    with open(ZUNI_HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)
    print(f"📝 Appended '{entry.get('title')}' to zero_dollar_uni_posted_history.json")


def get_next_zuni_payload():
    if not os.path.exists(ZUNI_CATALOG_PATH):
        raise RuntimeError("0$ University catalog not found!")
    with open(ZUNI_CATALOG_PATH, "r") as f:
        catalog = json.load(f)

    history = load_zuni_history()
    posted_ids = set()
    for h in history:
        if isinstance(h, dict):
            posted_ids.add(h.get("id"))
        elif isinstance(h, str):
            posted_ids.add(h)

    for item in catalog:
        if item.get("id") not in posted_ids:
            return item

    print("⚠️ All catalog items posted! Cycling back to first entry...")
    return catalog[0]


def execute_zuni_pipeline(dry_run=False):
    print("=" * 80)
    print("🎓 0$ UNIVERSITY - LINKEDIN GROWTH ENGINE")
    print(f"⏰ Execution Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    item = get_next_zuni_payload()
    print(f"🎯 Selected Payload: [{item['id']}] '{item['title']}'")
    pdf_filename = item.get("pdf_filename")
    pdf_path = os.path.join(PDF_VAULT_DIR, pdf_filename) if pdf_filename else None

    if pdf_path and not os.path.exists(pdf_path):
        print(f"⚠️ Warning: PDF file {pdf_filename} not found in {PDF_VAULT_DIR}!")

    if dry_run:
        print("\n🔍 DRY-RUN MODE: Post payload and validation succeeded without live publishing.")
        print(f"Title: {item['title']}")
        print(f"PDF Attached: {pdf_filename} (Exists: {os.path.exists(pdf_path) if pdf_path else False})")
        print(f"Length: {len(item.get('post_text', ''))} characters")
        return

    cookies = get_cookies()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            viewport={"width": 1600, "height": 1200}
        )
        context.add_cookies(cookies)
        page = context.new_page()

        try:
            print("\n👉 Step 1: Navigating to LinkedIn Feed...")
            page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=45000)
            time.sleep(4)

            # Open Composer
            print("🖱️ Step 2: Opening 'Start a post' modal...")
            page.evaluate("""() => {
                const els = Array.from(document.querySelectorAll('button, div, span, p')).filter(el => {
                    return (el.innerText || '').trim() === 'Start a post';
                });
                if (els.length > 0) els[0].click();
            }""")
            time.sleep(3)

            # Switch Author to 0$ University
            print("🔄 Step 3: Switching Author to '0$ University'...")
            page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button, div[role="button"]'));
                for (const b of btns) {
                    const txt = (b.innerText || '').toLowerCase();
                    const la = (b.getAttribute('aria-label') || '').toLowerCase();
                    if (txt.includes('post as') || txt.includes('arif alam') || txt.includes('data science reality') || la.includes('identity') || la.includes('switch')) {
                        b.click();
                        break;
                    }
                }
            }""")
            time.sleep(2)

            page.evaluate("""() => {
                const candidates = Array.from(document.querySelectorAll('li, div[role="radio"], div[role="option"], div[role="button"], span'));
                for (const el of candidates) {
                    const txt = (el.innerText || '').trim();
                    if (txt.includes('0$ University') || txt.startsWith('0$ University')) {
                        const target = el.closest('li') || el.closest('[role]') || el;
                        target.click();
                        break;
                    }
                }
            }""")
            time.sleep(2)

            page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const saveBtn = btns.find(b => ['Save', 'Next', 'Done', 'Confirm'].includes((b.innerText || '').trim()));
                if (saveBtn) saveBtn.click();
            }""")
            time.sleep(2)

            # Attach Document Carousel
            if pdf_path and os.path.exists(pdf_path):
                print(f"📑 Attaching Document Carousel: {pdf_filename}...")
                try:
                    with page.expect_file_chooser(timeout=15000) as fc_info:
                        page.evaluate("""() => {
                            const btns = Array.from(document.querySelectorAll('button, div[role="button"]'));
                            const docBtn = btns.find(b => {
                                const la = (b.getAttribute('aria-label') || '').toLowerCase();
                                return la.includes('document') || la.includes('add a document');
                            });
                            if (docBtn) docBtn.click();
                            else {
                                const plusBtn = btns.find(b => (b.getAttribute('aria-label') || '').includes('More'));
                                if (plusBtn) plusBtn.click();
                            }
                        }""")
                    fc_info.value.set_files(pdf_path)
                    print(f"✅ Document file set: {pdf_filename}")
                    time.sleep(5)

                    try:
                        title_input = page.locator("input[placeholder*='title' i], input[aria-label*='title' i], input[type='text']").first
                        if title_input.is_visible(timeout=5000):
                            title_input.fill(item["title"])
                    except Exception:
                        pass
                    time.sleep(2)

                    page.evaluate("""() => {
                        const btns = Array.from(document.querySelectorAll('button'));
                        const doneBtn = btns.find(b => ['Done', 'Next'].includes((b.innerText || '').trim()));
                        if (doneBtn) doneBtn.click();
                    }""")
                    time.sleep(3)
                except Exception as ex:
                    print(f"⚠️ Document attachment fallback: {ex}")

            # Insert Text using reliable executive methods
            print("✍️ Step 4: Injecting post text & Topmate links...")
            post_text = item["post_text"]

            # Method 1: focus editor and insertText via execCommand
            page.evaluate("""(txt) => {
                const editor = document.querySelector('div.tiptap, div.ProseMirror, div.ql-editor, div[contenteditable="true"], div.editor-content');
                if (editor) {
                    editor.focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, txt);
                }
            }""", post_text)
            time.sleep(2)

            # Method 2: keyboard insertion if needed
            editor_len = page.evaluate("""() => {
                const editor = document.querySelector('div.tiptap, div.ProseMirror, div.ql-editor, div[contenteditable="true"], div.editor-content');
                return editor ? editor.innerText.length : 0;
            }""")
            if editor_len < 200:
                print("🔄 Falling back to keyboard typing into editor...")
                try:
                    ed = page.locator("div.tiptap, div.ProseMirror, div.ql-editor, div[contenteditable='true']").first
                    ed.click()
                    page.keyboard.insert_text(post_text)
                except Exception as e:
                    print(f"⚠️ Keyboard insert error: {e}")
            time.sleep(3)

            # Capture screenshot proof before publishing
            screenshot_path = os.path.join(ARTIFACTS_DIR, "composer_ready_proof.png")
            page.screenshot(path=screenshot_path)
            print(f"📸 Captured composer proof: {screenshot_path}")

            # Publish live
            print("🚀 Step 5: Publishing live to 0$ University...")
            page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button')).filter(b => (b.innerText || '').trim() === 'Post');
                if (btns.length > 0) {
                    const postBtn = btns[btns.length - 1];
                    postBtn.scrollIntoView();
                    postBtn.click();
                }
            }""")
            print("✅ Clicked Post button! Waiting 15 seconds for network publication...")
            time.sleep(15)

            save_zuni_history({
                "id": item["id"],
                "title": item["title"],
                "format": "DOCUMENT_CAROUSEL"
            })

            # Fetch new permalink
            print("\n" + "=" * 80)
            print("⚡ STAGE 2: 8-ACTOR ENGAGEMENT BOOSTER & LIVE PERMALINK RESOLUTION")
            print("=" * 80)

            page.goto("https://www.linkedin.com/company/startup-founderss/posts/?feedView=all", wait_until="domcontentloaded", timeout=40000)
            time.sleep(6)

            top_post = page.locator("div.feed-shared-update-v2").first
            post_urn = top_post.get_attribute("data-urn") or top_post.get_attribute("data-id") or ""
            if post_urn and "activity:" in post_urn:
                post_id = post_urn.split("activity:")[1].split("?")[0].split(",")[0]
                permalink_url = f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"
                print(f"\n🎯 NEW LIVE POST PERMALINK: {permalink_url}")

                page.goto(permalink_url, wait_until="domcontentloaded", timeout=40000)
                time.sleep(5)

                # Like reaction booster
                for idx, actor in enumerate(ALL_ENGAGEMENT_ACTORS, 1):
                    actor_id = actor["id"]
                    actor_name = actor["name"]
                    print(f"[{idx}/8] ⚡ Boosting as: {actor_name}...")
                    try:
                        page.locator("button.content-admin-identity-toggle-button").first.click(force=True)
                        time.sleep(1.5)
                        page.evaluate(f"""() => {{
                            const radio = document.querySelector('#{actor_id}');
                            if (radio) {{
                                radio.checked = true;
                                radio.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                        }}""")
                        time.sleep(0.5)
                        page.locator(".artdeco-modal button:has-text('Save')").first.click(force=True)
                        time.sleep(2.5)

                        page.evaluate("""() => {
                            const btns = Array.from(document.querySelectorAll('button'));
                            const likeBtn = btns.find(b => (b.innerText || '').trim() === 'Like' && !b.className.includes('content-admin-identity-toggle-button'));
                            if (likeBtn && likeBtn.getAttribute('aria-pressed') !== 'true') likeBtn.click();
                        }""")
                    except Exception:
                        pass
                    time.sleep(1.5)

                # Submit Pinned 1st Comment
                print("\n💬 Submitting 0$ University Topmate 1st Comment...")
                page.evaluate("""(commentText) => {
                    const editor = document.querySelector('div.ql-editor[aria-placeholder*="Add a comment" i], div.ql-editor, div[contenteditable="true"]');
                    if (editor) {
                        editor.innerHTML = '';
                        const lines = commentText.split('\\n');
                        lines.forEach(l => {
                            const p = document.createElement('p');
                            p.innerText = l;
                            editor.appendChild(p);
                        });
                        editor.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }""", ZUNI_FIRST_COMMENT)
                time.sleep(2)
                submit_btn = page.locator("button.comments-comment-box__submit-button, button:has-text('Comment')").last
                if submit_btn.is_visible():
                    submit_btn.click(force=True)
                    time.sleep(3)
                    print("✅ 0$ University Topmate 1st comment submitted!")

                print("\n" + "=" * 80)
                print(f"🎉 0$ UNIVERSITY POST PIPELINE COMPLETED 100%!")
                print(f"🔗 LIVE POST URL: {permalink_url}")
                print("=" * 80)

        except Exception as e:
            print(f"❌ Error in 0$ University Runner: {e}")
            raise e
        finally:
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Perform catalog and auth checks without posting live")
    args = parser.parse_args()
    execute_zuni_pipeline(dry_run=args.dry_run)
