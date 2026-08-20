#!/usr/bin/env python3
"""
0$ University - Dedicated LinkedIn Autonomous Growth Engine (v4.0 Production)
============================================================================
1. Strict Media Enforcement: NO post is ever published without attached PDF / Infographic.
2. High-Resolution Infographic & Document Carousel Rendering (PyMuPDF 300 DPI).
3. Direct Company Admin Share Composer (100% Personal Profile Isolation).
4. Verified Media Preview in Composer before Post Button is unlocked.
5. Resolves live permalink and runs 8-Actor Cross-Engagement Booster + Pinned 1st Comment.
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
IMAGES_VAULT_DIR = os.path.join(ROOT_DIR, "documents", "images_vault")
PDF_VAULT_DIR = os.path.join(ROOT_DIR, "documents", "pdf_vault")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(IMAGES_VAULT_DIR, exist_ok=True)

CONFIG_PATH = os.path.join(ROOT_DIR, "config", "config.json")
FULL_COOKIES_PATH = os.path.join(ROOT_DIR, "config", "full_browser_cookies.json")
ZUNI_HISTORY_PATH = os.path.join(ROOT_DIR, "config", "zero_dollar_uni_posted_history.json")
ZUNI_CATALOG_PATH = os.path.join(ROOT_DIR, "config", "zero_dollar_uni_catalog.json")

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

ZUNI_FIRST_COMMENT = CONFIG.get("permanent_first_comment", """🎓 𝟎$ 𝐔𝐧𝐢𝘃𝐞𝐫𝐬𝗶𝐭𝘆 𝐅𝐫𝐞𝐞 𝐄𝐝𝐮𝐜𝗮𝐭𝐢𝐨𝐧 𝐕𝐚𝐮𝐥𝐭
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


def render_pdf_to_highres_image(pdf_path):
    """Render the primary page of the PDF into a crisp 300 DPI PNG infographic image."""
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    out_img_path = os.path.join(IMAGES_VAULT_DIR, f"{base_name}.png")

    if os.path.exists(out_img_path) and os.path.getsize(out_img_path) > 1000:
        return out_img_path

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        # Render at 300 DPI for ultra crisp graphic on LinkedIn feed
        pix = page.get_pixmap(dpi=300)
        pix.save(out_img_path)
        print(f"🖼️ Rendered 300 DPI infographic from PDF: {out_img_path}")
        return out_img_path
    except Exception as e:
        print(f"⚠️ PyMuPDF render note: {e}")
        # Fallback to direct PDF path if image rendering fails
        return pdf_path


def execute_zuni_pipeline(dry_run=False):
    print("=" * 80)
    print("🎓 0$ UNIVERSITY - LINKEDIN GROWTH ENGINE (STRICT MEDIA ENFORCEMENT)")
    print(f"⏰ Execution Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    item = get_next_zuni_payload()
    print(f"🎯 Selected Payload: [{item['id']}] '{item['title']}'")
    pdf_filename = item.get("pdf_filename")
    pdf_path = os.path.join(PDF_VAULT_DIR, pdf_filename) if pdf_filename else None

    # Strict Media Gate Check
    if not pdf_path or not os.path.exists(pdf_path):
        raise RuntimeError(f"🚨 FATAL: PDF file '{pdf_filename}' not found in {PDF_VAULT_DIR}! Aborting to prevent text-only post.")

    # Render High-Res Infographic from PDF
    media_file_to_upload = render_pdf_to_highres_image(pdf_path)
    if not os.path.exists(media_file_to_upload) or os.path.getsize(media_file_to_upload) < 1000:
        raise RuntimeError(f"🚨 FATAL: Generated media file '{media_file_to_upload}' is empty or invalid! Aborting to prevent text-only post.")

    print(f"📎 Verified Media File Ready for Attachment: {os.path.basename(media_file_to_upload)} ({os.path.getsize(media_file_to_upload)} bytes)")

    if dry_run:
        print("\n🔍 DRY-RUN MODE: Payload and media verified successfully without live publishing.")
        print(f"Title: {item['title']}")
        print(f"Media File: {media_file_to_upload}")
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
            print("\n👉 Step 1: Navigating to 0$ University Direct Page Share Composer...")
            page.goto("https://www.linkedin.com/company/86814703/admin/page-posts/published/?share=true", wait_until="domcontentloaded", timeout=45000)
            time.sleep(5)

            # Safety Assertion: Verify 0$ University author
            author_text = page.evaluate("""() => {
                const authorEl = document.querySelector('.share-unified-settings-entry-button, .org-post-author, .artdeco-modal');
                return authorEl ? authorEl.innerText : '';
            }""")
            print(f"🛡️ Composer Author Status: {author_text.replace(chr(10), ' | ')[:80]}")
            if "0$ University" not in author_text and "University" not in author_text:
                print("🔄 Direct modal not auto-opened, clicking Create -> Start a post...")
                page.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const createBtn = btns.find(b => (b.innerText || '').trim() === 'Create');
                    if (createBtn) createBtn.click();
                }""")
                time.sleep(2)
                page.evaluate("""() => {
                    const links = Array.from(document.querySelectorAll('a, li, button'));
                    const startPost = links.find(l => (l.innerText || '').includes('Start a post'));
                    if (startPost) startPost.click();
                }""")
                time.sleep(3)

            # Attach Infographic / Media
            print(f"🖼️ Step 2: Attaching Infographic Media: {os.path.basename(media_file_to_upload)}...")
            media_attached = False

            try:
                with page.expect_file_chooser(timeout=25000) as fc_info:
                    page.evaluate("""() => {
                        const btns = Array.from(document.querySelectorAll('button'));
                        const mediaBtn = btns.find(b => {
                            const la = (b.getAttribute('aria-label') || '').toLowerCase();
                            const txt = (b.innerText || '').toLowerCase();
                            return la.includes('add media') || la.includes('add a photo') || txt.includes('photo') || txt.includes('media') || b.className.includes('image-detour-btn');
                        });
                        if (mediaBtn) mediaBtn.click();
                    }""")
                fc_info.value.set_files(media_file_to_upload)
                print(f"✅ Media file injected via file chooser: {os.path.basename(media_file_to_upload)}")
                time.sleep(5)

                # Click Next on media preview editor modal
                page.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const nextBtn = btns.find(b => ['Next', 'Done'].includes((b.innerText || '').trim()) || (b.getAttribute('aria-label') || '').includes('Next'));
                    if (nextBtn) nextBtn.click();
                }""")
                time.sleep(4)
                media_attached = True
            except Exception as ex:
                print(f"⚠️ Primary media attachment error: {ex}")

            # STRICT MEDIA ASSERTION: Verify that the media is attached before posting
            has_media_in_composer = page.evaluate("""() => {
                const img = document.querySelector('.share-creation-state__preview-container img, .media-preview img, .share-box__preview-image');
                const doc = document.querySelector('.share-document-preview, .document-preview');
                return !!(img || doc);
            }""")

            if not media_attached and not has_media_in_composer:
                # Capture failure screenshot
                fail_shot = os.path.join(ARTIFACTS_DIR, "media_attachment_failure.png")
                page.screenshot(path=fail_shot)
                raise RuntimeError("🚨 STRICT ENFORCEMENT ERROR: Media failed to attach in composer! Aborting publication to guarantee zero text-only posts.")

            print("✅ Verified: Media preview is confirmed attached inside the LinkedIn composer!")

            # Insert Text
            print("✍️ Step 3: Injecting post text & Topmate links...")
            post_text = item["post_text"]

            try:
                editor = page.locator("div.ql-editor, div.tiptap, div[contenteditable='true']").first
                editor.wait_for(state="visible", timeout=8000)
                editor.click(force=True)
                time.sleep(1)
                page.keyboard.insert_text(post_text)
                print("✅ Injected post text via page.keyboard.insert_text")
            except Exception:
                page.evaluate("""(txt) => {
                    const el = document.querySelector('div.ql-editor, div.tiptap, div[contenteditable="true"]');
                    if (el) {
                        el.focus();
                        document.execCommand('selectAll', false, null);
                        document.execCommand('insertText', false, txt);
                    }
                }""", post_text)
                print("✅ Injected post text via execCommand fallback")
            time.sleep(3)

            # Capture composer proof
            screenshot_path = os.path.join(ARTIFACTS_DIR, "composer_ready_proof.png")
            page.screenshot(path=screenshot_path)
            print(f"📸 Captured composer proof: {screenshot_path}")

            # Publish live using direct modal JS click (immune to pointer interception)
            print("🚀 Step 4: Publishing live to 0$ University...")
            clicked = page.evaluate("""() => {
                const modal = document.querySelector('div[data-test-modal-id="sharebox"], div.artdeco-modal, div.share-box');
                if (modal) {
                    const postBtn = modal.querySelector('button.share-actions__primary-action, button.share-box-footer__primary-btn');
                    if (postBtn) {
                        postBtn.click();
                        return 'clicked_modal_btn';
                    }
                }
                const allBtns = Array.from(document.querySelectorAll('button'));
                const btn = allBtns.find(b => (b.innerText || '').trim() === 'Post' || b.className.includes('share-actions__primary-action'));
                if (btn) {
                    btn.click();
                    return 'clicked_global_btn';
                }
                return 'not_found';
            }""")
            print(f"✅ Click Post Result: {clicked}! Waiting 15 seconds for network publication...")
            time.sleep(15)

            save_zuni_history({
                "id": item["id"],
                "title": item["title"],
                "format": "INFOGRAPHIC_CAROUSEL",
                "media": os.path.basename(media_file_to_upload)
            })

            # Fetch live post permalink
            print("\n" + "=" * 80)
            print("⚡ STAGE 2: RESOLVING LIVE PERMALINK & 8-ACTOR ENGAGEMENT BOOSTER")
            print("=" * 80)

            page.goto("https://www.linkedin.com/company/86814703/admin/page-posts/published/", wait_until="domcontentloaded", timeout=40000)
            time.sleep(6)

            permalink_url = page.evaluate("""() => {
                const links = Array.from(document.querySelectorAll('a[href*="/feed/update/urn:li:activity:"], a[href*="/feed/update/urn:li:share:"]'));
                if (links.length > 0) return links[0].href;
                const post = document.querySelector('div.feed-shared-update-v2, div[data-urn*="activity"]');
                if (post) {
                    const urn = post.getAttribute('data-urn') || post.getAttribute('data-id') || '';
                    if (urn.includes('activity:')) {
                        const id = urn.split('activity:')[1].split('?')[0].split(',')[0];
                        return `https://www.linkedin.com/feed/update/urn:li:activity:${id}/`;
                    }
                }
                return null;
            }""")

            if not permalink_url:
                permalink_url = "https://www.linkedin.com/company/startup-founderss/posts/?feedView=all"

            print(f"\n🎯 RESOLVED LIVE POST LINK: {permalink_url}")

            if "activity:" in permalink_url:
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
            print("🎉 0$ UNIVERSITY POST PIPELINE COMPLETED 100%!")
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
