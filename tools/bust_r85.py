#!/usr/bin/env python3
"""r85 buster: i18n.js v49 -> v50 AND style.css v38 -> v39 across 15 pages.

Both assets changed: i18n.js gained 3 a11y.tbl.* keys; style.css recolored
the global focus ring. Pre-asserts both markers before bumping; verifies
exactly one reference of each new version per page afterwards.
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

i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
style = (ROOT / "style.css").read_text(encoding="utf-8")
if '"a11y.tbl.features"' not in i18n or '"a11y.tbl.privacy"' not in i18n:
    print("bust_r85: i18n.js missing r85 keys — aborting")
    sys.exit(1)
if "outline: 2px solid var(--text);\n  outline-offset: 2px;\n}\n/* r51" not in style:
    print("bust_r85: style.css missing r85 focus ring — aborting")
    sys.exit(1)

BUMPS = [("i18n.js?v=49", "i18n.js?v=50"), ("style.css?v=38", "style.css?v=39")]
bad = []
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    for old, new in BUMPS:
        n = text.count(old)
        if n != 1:
            bad.append(f"{page}: {n} occurrences of {old}")
            continue
        text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")
    print(f"  bumped {page}")

if bad:
    print(f"bust_r85: FAILURES: {bad}")
    sys.exit(1)

leftover = 0
for page in PAGES:
    text = (ROOT / page).read_text(encoding="utf-8")
    for old, new in BUMPS:
        if old in text or text.count(new) != 1:
            leftover += 1
            print(f"  VERIFY FAIL: {page} {old}->{new}")

print(f"bust_r85: {'FAILED' if leftover else 'ALL 15 PAGES i18n v50 + style v39'}")
sys.exit(1 if leftover else 0)
