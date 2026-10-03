#!/usr/bin/env python3
"""r93 buster: style.css v44 -> v45 across 15 pages (provenance print rule
is the CSS change; referrerpolicy/@page/body vars are unversioned HTML).
i18n.js did NOT change — v53 must remain untouched everywhere.
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
S_OLD, S_NEW = "style.css?v=44", "style.css?v=45"

style = (ROOT / "style.css").read_text(encoding="utf-8")
if "content: var(--print-src, none)" not in style:
    print("bust_r93: style.css missing r93 provenance rule — aborting")
    sys.exit(1)
comp = (ROOT / "comparison.html").read_text(encoding="utf-8")
if "@page{size:landscape;}" not in comp:
    print("bust_r93: comparison.html missing r93 landscape — aborting")
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
    print(f"bust_r93: FAILURES: {bad}")
    sys.exit(1)
print("bust_r93: v44 -> v45 across 15 pages; i18n v53 untouched")
