#!/usr/bin/env python3
"""r99 buster: BOTH shared assets changed — i18n.js (OS-theme follow,
v57 -> v58) and style.css (theme-btn boundary + hover rework, v48 -> v49).
Bumps both refs x15 with pre-asserts on all ships.
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
I_OLD, I_NEW = "i18n.js?v=57", "i18n.js?v=58"
S_OLD, S_NEW = "style.css?v=48", "style.css?v=49"

# pre-asserts
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
if "14) Live OS-theme follow (r99)" not in i18:
    print("bust_r99: i18n.js missing r99 OS-follow — aborting")
    sys.exit(1)
css = (ROOT / "style.css").read_text(encoding="utf-8")
if ".theme-btn:hover:not(.active)" not in css:
    print("bust_r99: style.css missing r99 hover rework — aborting")
    sys.exit(1)
if css.count("border: 1px solid var(--border-strong)") != 10:
    print("bust_r99: style.css border-strong count != 10 — aborting")
    sys.exit(1)

for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    ni, ns = text.count(I_OLD), text.count(S_OLD)
    if ni != 1 or ns != 1:
        print(f"bust_r99: {page}: {I_OLD} x{ni} / {S_OLD} x{ns} — aborting")
        sys.exit(1)
    p.write_text(text.replace(I_OLD, I_NEW).replace(S_OLD, S_NEW), encoding="utf-8")
print(f"bust_r99: bumped {I_OLD}->{I_NEW} and {S_OLD}->{S_NEW} on {len(PAGES)} pages")
