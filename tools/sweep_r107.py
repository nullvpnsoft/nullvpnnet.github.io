#!/usr/bin/env python3
"""r107 sweep: OG/Twitter image enrichment on all 15 pages.

og-cover.jpg is 1200x630 (verified by SOF parse). The estate carries
og:image + twitter:image on every page but none of the enrichment trio:
og:image:width/height (crawlers skip re-probing the image), og:image:alt +
twitter:image:alt (social-preview accessibility). This sweep inserts the
four metas after their anchor lines on all 15 pages. Idempotence guard:
aborts if any page already carries an enrichment tag.
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

OG_ANCHOR = '<meta property="og:image" content="https://nullvpn.net/og-cover.jpg"/>'
TW_ANCHOR = '<meta name="twitter:image" content="https://nullvpn.net/og-cover.jpg"/>'
ALT = "NullVPN — private connectivity for difficult networks. Brand cover with gold wave lines on dark navy."
OG_INSERT = (
    '<meta property="og:image:width" content="1200"/>\n'
    '  <meta property="og:image:height" content="630"/>\n'
    '  <meta property="og:image:alt" content="' + ALT + '"/>'
)
TW_INSERT = '<meta name="twitter:image:alt" content="' + ALT + '"/>'

errs = []
for page in PAGES:
    p = ROOT / page
    t = p.read_text(encoding="utf-8")
    if t.count(OG_ANCHOR) != 1:
        errs.append(f"{page}: og:image anchor x{t.count(OG_ANCHOR)} != 1")
    if t.count(TW_ANCHOR) != 1:
        errs.append(f"{page}: twitter:image anchor x{t.count(TW_ANCHOR)} != 1")
    if "og:image:width" in t:
        errs.append(f"{page}: already enriched — not idempotent, abort")
if errs:
    print("sweep_r107: PRE-CHECK FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)

for page in PAGES:
    p = ROOT / page
    t = p.read_text(encoding="utf-8")
    t = t.replace(OG_ANCHOR, OG_ANCHOR + "\n  " + OG_INSERT, 1)
    t = t.replace(TW_ANCHOR, TW_ANCHOR + "\n  " + TW_INSERT, 1)
    p.write_text(t, encoding="utf-8")

# post-counts
n_w = sum((ROOT / p).read_text(encoding="utf-8").count('og:image:width') for p in PAGES)
n_talt = sum((ROOT / p).read_text(encoding="utf-8").count('twitter:image:alt') for p in PAGES)
print(f"sweep_r107: OK — enrichment on {len(PAGES)} pages (og:image:width x{n_w}, twitter:image:alt x{n_talt})")
