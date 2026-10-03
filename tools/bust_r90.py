#!/usr/bin/env python3
"""r90 buster: style.css v41 -> v42 across 15 pages. i18n.js did NOT change
(main landmark swap is HTML-only, contrast/print are CSS), so v53 must remain
untouched everywhere. Pre-asserts r90 markers before touching anything.
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
S_OLD, S_NEW = "style.css?v=41", "style.css?v=42"

style = (ROOT / "style.css").read_text(encoding="utf-8")
index = (ROOT / "index.html").read_text(encoding="utf-8")
if "--border: #8f7448" not in style or "r90: borders join the lift" not in style:
    print("bust_r90: style.css missing r90 markers — aborting")
    sys.exit(1)
if '<main id="main"' not in index or '<section id="main"' in index:
    print("bust_r90: index.html missing r90 main landmark — aborting")
    sys.exit(1)

bad = []
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    ns = text.count(S_OLD)
    if ns != 1:
        bad.append(f"{page}: style {S_OLD} x{ns}")
        continue
    p.write_text(text.replace(S_OLD, S_NEW), encoding="utf-8")
    print(f"  bumped {page}")

if bad:
    print(f"bust_r90: FAILURES: {bad}")
    sys.exit(1)

leftover = 0
for page in PAGES:
    text = (ROOT / page).read_text(encoding="utf-8")
    if S_OLD in text or text.count(S_NEW) != 1 or text.count("i18n.js?v=53") != 1:
        leftover += 1
        print(f"  VERIFY FAIL: {page}")

print(f"bust_r90: {'FAILED' if leftover else 'ALL 15 PAGES style v42 + i18n v53 untouched'}")
sys.exit(1 if leftover else 0)
