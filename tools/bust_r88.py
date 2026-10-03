#!/usr/bin/env python3
"""r88 buster: i18n.js v52 -> v53 across 15 pages. style.css did NOT change
this round (the caption rule is page-local in comparison.html), so v40 must
remain untouched everywhere. Pre-asserts r88 markers before touching anything.
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
I_OLD, I_NEW = "i18n.js?v=52", "i18n.js?v=53"

i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
comparison = (ROOT / "comparison.html").read_text(encoding="utf-8")
if '"comp.table.caption": {' not in i18n or "r88" not in i18n:
    print("bust_r88: i18n.js missing r88 markers — aborting")
    sys.exit(1)
if '<caption data-i18n="comp.table.caption">' not in comparison:
    print("bust_r88: comparison.html missing r88 caption — aborting")
    sys.exit(1)

bad = []
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    ni = text.count(I_OLD)
    if ni != 1:
        bad.append(f"{page}: i18n {I_OLD} x{ni}")
        continue
    p.write_text(text.replace(I_OLD, I_NEW), encoding="utf-8")
    print(f"  bumped {page}")

if bad:
    print(f"bust_r88: FAILURES: {bad}")
    sys.exit(1)

leftover = 0
for page in PAGES:
    text = (ROOT / page).read_text(encoding="utf-8")
    if I_OLD in text or text.count(I_NEW) != 1 or text.count("style.css?v=40") != 1:
        leftover += 1
        print(f"  VERIFY FAIL: {page}")

print(f"bust_r88: {'FAILED' if leftover else 'ALL 15 PAGES i18n v53 + style v40 untouched'}")
sys.exit(1 if leftover else 0)
