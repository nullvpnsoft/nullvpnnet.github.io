#!/usr/bin/env python3
"""r92 buster: style.css v43 -> v44 across 15 pages (tabular-nums on .price
is the CSS change; og alternates / input attrs / llms.txt are unversioned
HTML+txt). i18n.js did NOT change — v53 must remain untouched everywhere.
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
S_OLD, S_NEW = "style.css?v=43", "style.css?v=44"

style = (ROOT / "style.css").read_text(encoding="utf-8")
if "font-variant-numeric: tabular-nums" not in style or "r92: tabular digits" not in style:
    print("bust_r92: style.css missing r92 markers — aborting")
    sys.exit(1)
idx = (ROOT / "index.html").read_text(encoding="utf-8")
if idx.count("og:locale:alternate") != 6:
    print("bust_r92: index.html missing r92 og alternates — aborting")
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
    print(f"bust_r92: FAILURES: {bad}")
    sys.exit(1)
print("bust_r92: v43 -> v44 across 15 pages; i18n v53 untouched")
