#!/usr/bin/env python3
"""r94 buster: style.css v45 -> v46 across 15 pages (prose underline +
forced-colors are CSS; contact-sub hook and llms.txt are unversioned).
i18n.js did NOT change — v54 must remain untouched everywhere.
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
S_OLD, S_NEW = "style.css?v=45", "style.css?v=46"

style = (ROOT / "style.css").read_text(encoding="utf-8")
if "text-underline-offset: 2px" not in style or "@media (forced-colors: active)" not in style:
    print("bust_r94: style.css missing r94 markers — aborting")
    sys.exit(1)
if '<p class="contact-sub" data-i18n="contact.sub">' not in (ROOT / "contact.html").read_text(encoding="utf-8"):
    print("bust_r94: contact.html missing r94 hook — aborting")
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
    print(f"bust_r94: FAILURES: {bad}")
    sys.exit(1)
print("bust_r94: v45 -> v46 across 15 pages; i18n v54 untouched")
