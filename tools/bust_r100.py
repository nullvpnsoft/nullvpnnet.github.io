#!/usr/bin/env python3
"""r100 buster: both assets changed — i18n.js (language-switch query reset +
cleared-note, v58 -> v59) and style.css (is-note italic, v49 -> v50).
Pre-asserts both ships before bumping.
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
I_OLD, I_NEW = "i18n.js?v=58", "i18n.js?v=59"
S_OLD, S_NEW = "style.css?v=49", "style.css?v=50"

i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
if "const langChanged = lastFilterLang !== null && lastFilterLang !== lang;" not in i18:
    print("bust_r100: i18n.js missing r100 langChanged guard — aborting")
    sys.exit(1)
if i18.count('"faq.filter.cleared"') != 1:
    print("bust_r100: i18n.js cleared key missing — aborting")
    sys.exit(1)
css = (ROOT / "style.css").read_text(encoding="utf-8")
if ".faq-filter-status.is-note { font-style: italic; }" not in css:
    print("bust_r100: style.css missing is-note rule — aborting")
    sys.exit(1)

for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    ni, ns = text.count(I_OLD), text.count(S_OLD)
    if ni != 1 or ns != 1:
        print(f"bust_r100: {page}: {I_OLD} x{ni} / {S_OLD} x{ns} — aborting")
        sys.exit(1)
    p.write_text(text.replace(I_OLD, I_NEW).replace(S_OLD, S_NEW), encoding="utf-8")
print(f"bust_r100: bumped {I_OLD}->{I_NEW} and {S_OLD}->{S_NEW} on {len(PAGES)} pages")
