#!/usr/bin/env python3
"""
0$ University - QA & Deduplication Auditor
==========================================
Validates catalog format, character lengths, and existence of all referenced PDF documents.
"""

import os
import sys
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "config", "zero_dollar_uni_catalog.json")
HISTORY_PATH = os.path.join(ROOT_DIR, "config", "zero_dollar_uni_posted_history.json")
PDF_VAULT_DIR = os.path.join(ROOT_DIR, "documents", "pdf_vault")


def audit():
    print("=" * 80)
    print("🔍 0$ UNIVERSITY - CATALOG & DOCUMENT QA AUDITOR")
    print("=" * 80)

    if not os.path.exists(CATALOG_PATH):
        print(f"❌ Error: Catalog file not found at {CATALOG_PATH}")
        sys.exit(1)

    with open(CATALOG_PATH, "r") as f:
        catalog = json.load(f)

    print(f"📊 Total Catalog Entries: {len(catalog)}")

    errors = 0
    warnings = 0

    seen_ids = set()

    for idx, item in enumerate(catalog, 1):
        item_id = item.get("id")
        title = item.get("title", "")
        post_text = item.get("post_text", "")
        pdf_filename = item.get("pdf_filename")

        # Duplicate ID check
        if item_id in seen_ids:
            print(f"❌ [Item {idx}] Duplicate ID detected: {item_id}")
            errors += 1
        seen_ids.add(item_id)

        # Character length check
        text_len = len(post_text)
        if text_len < 500:
            print(f"⚠️ [Item {idx} ({item_id})] Text length too short ({text_len} chars): '{title}'")
            warnings += 1
        elif text_len > 3000:
            print(f"❌ [Item {idx} ({item_id})] Text length exceeds LinkedIn limits ({text_len} chars): '{title}'")
            errors += 1

        # PDF existence check
        if pdf_filename:
            pdf_path = os.path.join(PDF_VAULT_DIR, pdf_filename)
            if not os.path.exists(pdf_path):
                print(f"❌ [Item {idx} ({item_id})] Missing PDF document: '{pdf_filename}'")
                errors += 1
            else:
                size_kb = os.path.getsize(pdf_path) / 1024
                # verify non-empty
                if size_kb < 1:
                    print(f"❌ [Item {idx} ({item_id})] Corrupt or empty PDF: '{pdf_filename}' ({size_kb:.1f} KB)")
                    errors += 1

    print("-" * 80)
    if errors == 0:
        print(f"✅ QA AUDIT PASSED: {len(catalog)} entries verified with 0 errors and {warnings} warnings.")
    else:
        print(f"❌ QA AUDIT FAILED: {errors} errors found.")
        sys.exit(1)


if __name__ == "__main__":
    audit()
