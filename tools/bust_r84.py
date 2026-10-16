#!/usr/bin/env python3
"""r84 buster: style.css v37 -> v38 across all 15 pages.

style.css changed (estate scroll-margin rule); i18n.js untouched (v49 stays).
Asserts the r84 marker exists in style.css before bumping, and that every
page got exactly one version bump.
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
OLD, NEW = "style.css?v=37", "style.css?v=38"

style = (ROOT / "style.css").read_text(encoding="utf-8")
if "r84: tr[id] (comparison's 11 deep-linked rows" not in style:
    print("bust_r84: style.css missing r84 marker — aborting")
    sys.exit(1)
if f"section[id], div[id], tr[id], th[id]" not in style:
    print("bust_r84: style.css missing r84 selector — aborting")
    sys.exit(1)

bad = []
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    n = text.count(OLD)
    if n != 1:
        bad.append(f"{page}: {n} occurrences of {OLD}")
        continue
    p.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print(f"  bumped {page}")

if bad:
    print(f"bust_r84: FAILURES: {bad}")
    sys.exit(1)

# verify
leftover = 0
for page in PAGES:
    text = (ROOT / page).read_text(encoding="utf-8")
    if OLD in text:
        leftover += 1
        print(f"  VERIFY FAIL: {page} still carries {OLD}")
    if text.count(NEW) != 1:
        leftover += 1
        print(f"  VERIFY FAIL: {page} NEW count != 1")
i18n_ref = (ROOT / "index.html").read_text(encoding="utf-8")
if "i18n.js?v=49" not in i18n_ref:
    leftover += 1
    print("  VERIFY FAIL: i18n.js version changed unexpectedly")

print(f"bust_r84: {'FAILED' if leftover else 'ALL 15 PAGES v38, i18n v49 untouched'}")
sys.exit(1 if leftover else 0)
