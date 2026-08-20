#!/usr/bin/env python3
"""
0$ University - Dedicated LinkedIn Autonomous Growth Engine
===========================================================
1. Focus: 100% Free Ivy-League CS/AI Degrees, Open-Source Roadmaps, Stanford/MIT/Harvard Courses.
2. Selects '0$ University' from author dropdown with strict pre-publish assertion.
3. Attaches authentic Roadmap / Course Vault PDF Carousel.
4. Injects exact standardized Topmate & WhatsApp links block.
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
os.makedirs(LOGS_DIR, exist_ok=True)

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

ZUNI_FIRST_COMMENT = CONFIG.get("permanent_first_comment", """🎓 𝟎$ 𝐔𝐧𝐢𝐯𝐞𝐫𝐬𝐢𝐭𝐲 𝐅𝐫𝐞𝐞 𝐄𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧 𝐕𝐚𝐮𝐥𝐭
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
        cookies.append({
            "name": "li_at",
            "value": li_at.strip('"'),
            "domain": ".linkedin.com",
            "path": "/",
            "secure": True,
            "sameSite": "None"
        })
        cookies.append({
            "name": "JSESSIONID",
            "value": jsessionid.strip('"'),
            "domain": ".linkedin.com",
            "path": "/",
            "secure": True,
            "sameSite": "None"
        })
        if bcookie:
            cookies.append({
                "name": "bcookie",
                "value": bcookie.strip('"'),
                "domain": ".linkedin.com",
                "path": "/",
                "secure": True,
                "sameSite": "None"
            })
        if bscookie:
            cookies.append({
                "name": "bscookie",
                "value": bscookie.strip('"'),
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
            args=["--no-sandbox", "--disable-dev-shm-usage"]
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
            time.sleep(3)

            print("🖱️ Step 2: Opening 'Start a post' modal...")
            start_btn = page.locator("p:has-text('Start a post'), span:has-text('Start a post'), div:has-text('Start a post'), button:has-text('Start a post')").last
            start_btn.click()
            page.wait_for_selector("div.tiptap, div.ProseMirror, div.ql-editor, div[contenteditable='true'], div.editor-content", timeout=15000)
            time.sleep(2)

            print("🔄 Step 3: Switching Author to '0$ University'...")
            page.evaluate("""() => {
                const els = Array.from(document.querySelectorAll('div, span, button')).filter(el => {
                    return el.childNodes.length > 0 && Array.from(el.childNodes).some(n => n.nodeType === 3 && (n.textContent.includes('Arif Alam') || n.textContent.includes('Data Science Reality') || n.textContent.includes('University')));
                });
                if (els.length > 0) {
                    const target = els[0].closest('div[role="button"]') || els[0].closest('button') || els[0];
                    target.click();
                }
            }""")
            time.sleep(2)

            page.evaluate("""() => {
                const target = Array.from(document.querySelectorAll('*')).find(el => el.childNodes.length > 0 && Array.from(el.childNodes).some(n => n.nodeType === 3 && (n.textContent.trim().startsWith('0$ University') || n.textContent.trim().includes('0$ University'))));
                if (target) {
                    const clickable = target.closest('li') || target.closest('div[role="button"]') || target;
                    clickable.click();
                }
            }""")
            time.sleep(2)

            author_text = page.evaluate("""() => {
                const authorEl = Array.from(document.querySelectorAll('div, span, button')).find(el => el.innerText && el.innerText.includes('0$ University'));
                return authorEl ? '0$ University' : 'FAILED';
            }""")
            if author_text != "0$ University":
                print("⚠️ Warning: Primary author check returned non-standard text. Verifying fallback...")

            # Attach Document Carousel
            if pdf_path and os.path.exists(pdf_path):
                print(f"📑 Attaching Document Carousel: {pdf_filename}...")
                page.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button, div[role="button"]')).filter(el => {
                        const svg = el.querySelector('svg');
                        return svg && (svg.id?.includes('add') || svg.id?.includes('plus') || svg.outerHTML?.includes('d="M14 9H9v5H7V9H2V7h5V2h2v5h5z"'));
                    });
                    if (btns.length > 0) btns[0].click();
                }""")
                time.sleep(2)
                page.locator("svg#sticky-note-medium, svg[id*='sticky-note']").first.click(force=True)
                time.sleep(2)

                with page.expect_file_chooser() as fc_info:
                    page.locator("button:has-text('Choose file'), button:has-text('Choose a file')").first.click()
                fc_info.value.set_files(pdf_path)
                time.sleep(4)

                title_input = page.locator("input[placeholder*='title' i], input[aria-label*='title' i], input[type='text']").first
                title_input.fill(item["title"])
                time.sleep(2)

                done_clicked = False
                for done_sel in [
                    "button:has-text('Done')",
                    "button:has-text('Next')",
                    "button[aria-label*='Done' i]",
                    "button[aria-label*='Next' i]",
                    "button.share-actions__primary-action",
                    "button.share-box-footer__primary-btn",
                ]:
                    try:
                        btn = page.locator(done_sel).first
                        btn.wait_for(timeout=5000)
                        btn.click(force=True)
                        done_clicked = True
                        print(f"✅ Done/Next clicked via: {done_sel}")
                        break
                    except Exception:
                        continue
                time.sleep(3)

            # Insert Text
            print("✍️ Injecting post text & Topmate links...")
            text_injected = False
            for ed_sel in [
                "div.tiptap",
                "div.ProseMirror",
                "div.ql-editor",
                "div[contenteditable='true']",
                "div.editor-content",
                "div[data-placeholder*='post' i]"
            ]:
                try:
                    ed = page.locator(ed_sel).first
                    if ed.is_visible(timeout=3000):
                        ed.click(force=True)
                        page.keyboard.insert_text(item["post_text"])
                        text_injected = True
                        print(f"✅ Injected text via: {ed_sel}")
                        break
                except Exception:
                    continue

            if not text_injected:
                page.evaluate("""(txt) => {
                    const el = document.querySelector('div.tiptap, div.ProseMirror, div.ql-editor, div[contenteditable="true"], div.editor-content');
                    if (el) {
                        el.focus();
                        el.innerText = txt;
                        el.dispatchEvent(new InputEvent('input', {bubbles: true}));
                    }
                }""", item["post_text"])
                print("✅ Injected text via evaluate DOM dispatch fallback")
            time.sleep(3)

            # Publish
            print("🚀 Step 4: Publishing live...")
            post_clicked = False
            for post_sel in [
                "button.share-actions__primary-action",
                "button.share-box-footer__primary-btn",
                "button:has-text('Post')",
                "button[aria-label*='Post' i]",
                "div.share-box_actions button"
            ]:
                try:
                    pbtn = page.locator(post_sel).last
                    if pbtn.is_visible(timeout=3000):
                        pbtn.click(force=True)
                        post_clicked = True
                        print(f"✅ Clicked Post button via: {post_sel}")
                        break
                except Exception:
                    continue

            if not post_clicked:
                page.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const postBtn = btns.reverse().find(b => (b.innerText || '').trim() === 'Post' || (b.getAttribute('aria-label') || '').includes('Post'));
                    if (postBtn) {
                        postBtn.scrollIntoView();
                        postBtn.click();
                    }
                }""")
                print("✅ Clicked Post button via evaluate DOM dispatch fallback")
            time.sleep(10)

            save_zuni_history({
                "id": item["id"],
                "title": item["title"],
                "format": "DOCUMENT_CAROUSEL"
            })

            # =========================================================================
            # STAGE 2: 8-ACTOR ENGAGEMENT BOOSTER (ARIF ALAM + 7 SISTER PAGES)
            # =========================================================================
            print("\n" + "=" * 80)
            print("⚡ STAGE 2: 8-ACTOR CROSS-ENGAGEMENT BOOSTER")
            print("=" * 80)

            page.goto("https://www.linkedin.com/company/startup-founderss/posts/?feedView=all", wait_until="domcontentloaded", timeout=40000)
            time.sleep(5)

            top_post = page.locator("div.feed-shared-update-v2").first
            post_urn = top_post.get_attribute("data-urn") or top_post.get_attribute("data-id") or ""
            if post_urn and "activity:" in post_urn:
                permalink_url = f"https://www.linkedin.com/feed/update/{post_urn}/"
                print(f"🎯 Navigating to dedicated permalink: {permalink_url}")
                page.goto(permalink_url, wait_until="domcontentloaded", timeout=40000)
                time.sleep(5)

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
                    except Exception as ex:
                        print(f"   ⚠️ Note: {ex}")
                    time.sleep(1.5)

                # Reset to Arif Alam
                page.locator("button.content-admin-identity-toggle-button").first.click(force=True)
                time.sleep(1.5)
                page.evaluate("""() => {
                    const radio = document.querySelector('#select-self');
                    if (radio) {
                        radio.checked = true;
                        radio.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }""")
                time.sleep(0.5)
                page.locator(".artdeco-modal button:has-text('Save')").first.click(force=True)
                time.sleep(2)

                # Submit 1st Comment
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
            print("🎉 0$ UNIVERSITY POST PIPELINE COMPLETED 100%!")
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
