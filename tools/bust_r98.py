#!/usr/bin/env python3
"""r98 buster: style.css content changed (border-strong token + 9 functional
boundary swaps) -> v47 -> v48 x15. i18n.js untouched (v57 holds — no key
changes this round). Pre-asserts all r98 ships before bumping.
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
S_OLD, S_NEW = "style.css?v=47", "style.css?v=48"

# pre-asserts: r98 markers must exist before bumping
css = (ROOT / "style.css").read_text(encoding="utf-8")
if css.count("--border-strong:") != 2:
    print("bust_r98: style.css token count != 2 — aborting")
    sys.exit(1)
if css.count("border: 1px solid var(--border-strong)") != 9:
    print("bust_r98: style.css selector swaps != 9 — aborting")
    sys.exit(1)
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
if "border:1px solid var(--border-strong,#64748b)" not in pricing:
    print("bust_r98: pricing.html modal swap missing — aborting")
    sys.exit(1)
offline = (ROOT / "offline.html").read_text(encoding="utf-8")
if "border: 1px solid var(--border-strong); background: var(--bg3); /* r98: offline nav chips are functional links */" not in offline:
    print("bust_r98: offline.html chip swap missing — aborting")
    sys.exit(1)

changed = 0
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    ni, ns = text.count("i18n.js?v=57"), text.count(S_OLD)
    if ni != 1 or ns != 1:
        print(f"bust_r98: {page}: i18n v57 x{ni} / style {S_OLD} x{ns} — aborting")
        sys.exit(1)
    p.write_text(text.replace(S_OLD, S_NEW), encoding="utf-8")
    changed += 1
print(f"bust_r98: bumped {S_OLD} -> {S_NEW} on {changed} pages; i18n v57 holds")
