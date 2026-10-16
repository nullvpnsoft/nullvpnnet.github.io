#!/usr/bin/env python3
"""r87 buster: i18n.js v51 -> v52 AND style.css v39 -> v40 across 15 pages.

i18n.js changed (getLang ?lang= deep link); style.css changed (standard
scrollbar properties). llms.txt is a NEW file — no buster applies to it.
Pre-asserts both r87 markers before touching anything.
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
I_OLD, I_NEW = "i18n.js?v=51", "i18n.js?v=52"
S_OLD, S_NEW = "style.css?v=39", "style.css?v=40"

i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
style = (ROOT / "style.css").read_text(encoding="utf-8")
if "hasOwnProperty.call(T['nav.home'], qp)" not in i18n or "r87: ?lang= deep link" not in i18n:
    print("bust_r87: i18n.js missing r87 markers — aborting")
    sys.exit(1)
if "scrollbar-width: thin" not in style or "r87: standard scrollbar properties" not in style:
    print("bust_r87: style.css missing r87 markers — aborting")
    sys.exit(1)

bad = []
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    ni, ns = text.count(I_OLD), text.count(S_OLD)
    if ni != 1 or ns != 1:
        bad.append(f"{page}: i18n {I_OLD} x{ni}, style {S_OLD} x{ns}")
        continue
    p.write_text(text.replace(I_OLD, I_NEW).replace(S_OLD, S_NEW), encoding="utf-8")
    print(f"  bumped {page}")

if bad:
    print(f"bust_r87: FAILURES: {bad}")
    sys.exit(1)

leftover = 0
for page in PAGES:
    text = (ROOT / page).read_text(encoding="utf-8")
    if I_OLD in text or S_OLD in text or text.count(I_NEW) != 1 or text.count(S_NEW) != 1:
        leftover += 1
        print(f"  VERIFY FAIL: {page}")

print(f"bust_r87: {'FAILED' if leftover else 'ALL 15 PAGES i18n v52 + style v40'}")
sys.exit(1 if leftover else 0)
