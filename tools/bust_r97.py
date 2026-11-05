#!/usr/bin/env python3
"""r97 buster: i18n.js content changed (reconnect probe) -> v56 -> v57 x15.
style.css untouched (v47 holds). sw.js + offline.html are unversioned — their
changes propagate via the SW byte-diff update check and the precache refresh
that the byte-diff triggers.
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
I_OLD, I_NEW = "i18n.js?v=56", "i18n.js?v=57"

# pre-asserts: r97 markers must exist before bumping
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
if "fetch('/', { method: 'HEAD', cache: 'no-store' })" not in i18:
    print("bust_r97: i18n.js missing r97 probe — aborting")
    sys.exit(1)
sw = (ROOT / "sw.js").read_text(encoding="utf-8")
if "ignoreSearch: true" not in sw:
    print("bust_r97: sw.js missing r97 normalization — aborting")
    sys.exit(1)
off = (ROOT / "offline.html").read_text(encoding="utf-8")
if "position: fixed; left: 50%; bottom: 26px;" not in off:
    print("bust_r97: offline.html missing r97 toast — aborting")
    sys.exit(1)

bad = []
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    ni, ns = text.count(I_OLD), text.count("style.css?v=47")
    if ni != 1 or ns != 1:
        bad.append(f"{page}: i18n {I_OLD} x{ni} / style v47 x{ns}")
        continue
    p.write_text(text.replace(I_OLD, I_NEW), encoding="utf-8")
    print(f"  bumped {page}")

if bad:
    print(f"bust_r97: FAILURES: {bad}")
    sys.exit(1)
print("bust_r97: i18n v56 -> v57 across 15 pages; style v47 holds")
