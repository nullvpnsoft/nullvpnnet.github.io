#!/usr/bin/env python3
"""r89 buster: style.css v40 -> v41 across 15 pages. i18n.js did NOT change
this round (manifest screenshots, web3 JSON-LD and the accent tokens touch
no keys), so v53 must remain untouched everywhere. Pre-asserts r89 markers
before touching anything.
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
S_OLD, S_NEW = "style.css?v=40", "style.css?v=41"

style = (ROOT / "style.css").read_text(encoding="utf-8")
web3 = (ROOT / "web3.html").read_text(encoding="utf-8")
if ":root { accent-color: var(--accent); }" not in style or "r89" not in style:
    print("bust_r89: style.css missing r89 markers — aborting")
    sys.exit(1)
if "BreadcrumbList" not in web3:
    print("bust_r89: web3.html missing r89 breadcrumb — aborting")
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
    print(f"bust_r89: FAILURES: {bad}")
    sys.exit(1)

leftover = 0
for page in PAGES:
    text = (ROOT / page).read_text(encoding="utf-8")
    if S_OLD in text or text.count(S_NEW) != 1 or text.count("i18n.js?v=53") != 1:
        leftover += 1
        print(f"  VERIFY FAIL: {page}")

print(f"bust_r89: {'FAILED' if leftover else 'ALL 15 PAGES style v41 + i18n v53 untouched'}")
sys.exit(1 if leftover else 0)
