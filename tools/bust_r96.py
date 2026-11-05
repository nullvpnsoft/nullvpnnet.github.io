#!/usr/bin/env python3
"""r96 buster: i18n.js content changed (?q= machinery) -> v55 -> v56 x15.
style.css did NOT change -> v47 must hold on every page (asserted, untouched).
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
I_OLD, I_NEW = "i18n.js?v=55", "i18n.js?v=56"

# pre-asserts: r96 markers must exist before bumping
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
if "const initialQ = (() => {" not in i18 or "if (q) u.searchParams.set('q', q);" not in i18:
    print("bust_r96: i18n.js missing r96 ?q= machinery — aborting")
    sys.exit(1)
faq = (ROOT / "faq.html").read_text(encoding="utf-8")
if 'maxlength="80"' not in faq:
    print("bust_r96: faq.html missing maxlength — aborting")
    sys.exit(1)
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
if "@media (prefers-reduced-motion: reduce){.checkout-overlay,.checkout-modal{animation:none}" not in pricing:
    print("bust_r96: pricing.html missing reduce gate — aborting")
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
    print(f"bust_r96: FAILURES: {bad}")
    sys.exit(1)
print("bust_r96: i18n v55 -> v56 across 15 pages; style v47 holds")
