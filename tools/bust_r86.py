#!/usr/bin/env python3
"""r86 buster: i18n.js v50 -> v51 across 15 pages.

Only i18n.js changed (engine + 2 keys); style.css untouched (v39 stays);
page-local HTML styles ride network-first HTML (no buster needed).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "404.html", "comparison.html", "contact.html", "download.html", "faq.html",
    "features.html", "how-it-works.html", "index.html", "offline.html",
    "pricing.html", "privacy.html", "refund.html", "success.html", "terms.html",
    "web3.html",
]
OLD, NEW = "i18n.js?v=50", "i18n.js?v=51"

i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
if '"pricing.anchor.plan"' not in i18n or "makePermalinkChip" not in i18n:
    print("bust_r86: i18n.js missing r86 markers — aborting")
    sys.exit(1)

bad = []
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    n = text.count(OLD)
    if n != 1:
        bad.append(f"{page}: {n} occurrences of {OLD}")
        continue
    p.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print(f"  bumped {page}")

if bad:
    print(f"bust_r86: FAILURES: {bad}")
    sys.exit(1)

leftover = 0
for page in PAGES:
    text = (ROOT / page).read_text(encoding="utf-8")
    if OLD in text or text.count(NEW) != 1:
        leftover += 1
        print(f"  VERIFY FAIL: {page}")
    if "style.css?v=39" not in text:
        leftover += 1
        print(f"  VERIFY FAIL: {page} style version changed unexpectedly")

print(f"bust_r86: {'FAILED' if leftover else 'ALL 15 PAGES i18n v51, style v39 untouched'}")
sys.exit(1 if leftover else 0)
