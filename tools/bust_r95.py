#!/usr/bin/env python3
"""r95 buster: BOTH assets changed this round — style.css v46 -> v47 AND
i18n.js v54 -> v55 across 15 pages. Pre-asserts r95 markers so we never bust
an unpatched tree.
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
S_OLD, S_NEW = "style.css?v=46", "style.css?v=47"
I_OLD, I_NEW = "i18n.js?v=54", "i18n.js?v=55"

# pre-asserts: r95 markers must exist before bumping
css = (ROOT / "style.css").read_text(encoding="utf-8")
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
if "@media print { .faq-filter { display: none !important; } }" not in css:
    print("bust_r95: style.css missing r95 print rule — aborting")
    sys.exit(1)
if "behavior: reduce ? 'auto' : 'smooth', block: 'center'" not in i18:
    print("bust_r95: i18n.js missing r95 motion gate — aborting")
    sys.exit(1)
if "if (e.key !== 'Escape' || !faqFilter.value) return;" not in i18:
    print("bust_r95: i18n.js missing r95 Escape handler — aborting")
    sys.exit(1)

bad = []
for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    ns, ni = text.count(S_OLD), text.count(I_OLD)
    if ns != 1 or ni != 1:
        bad.append(f"{page}: style {S_OLD} x{ns} / i18n {I_OLD} x{ni}")
        continue
    p.write_text(
        text.replace(S_OLD, S_NEW).replace(I_OLD, I_NEW),
        encoding="utf-8",
    )
    print(f"  bumped {page}")

if bad:
    print(f"bust_r95: FAILURES: {bad}")
    sys.exit(1)
print("bust_r95: style v46 -> v47 + i18n v54 -> v55 across 15 pages")
