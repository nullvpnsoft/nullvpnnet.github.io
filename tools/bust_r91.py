#!/usr/bin/env python3
"""r91 buster: style.css v42 -> v43 across 15 pages (@page print margins
are CSS; the success.html overflow fix is page-inline HTML and needs no
buster). i18n.js did NOT change — v53 must remain untouched everywhere.
Pre-asserts r91 markers before touching anything.
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
S_OLD, S_NEW = "style.css?v=42", "style.css?v=43"

style = (ROOT / "style.css").read_text(encoding="utf-8")
success = (ROOT / "success.html").read_text(encoding="utf-8")
if css := style:
    if "@page { margin: 14mm 12mm; }" not in css or "r91: explicit paper margins" not in css:
        print("bust_r91: style.css missing r91 markers — aborting")
        sys.exit(1)
if "overflow-wrap:anywhere" not in success:
    print("bust_r91: success.html missing r91 overflow fix — aborting")
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
    print(f"bust_r91: FAILURES: {bad}")
    sys.exit(1)
print("bust_r91: v42 -> v43 across 15 pages; i18n v53 untouched")
