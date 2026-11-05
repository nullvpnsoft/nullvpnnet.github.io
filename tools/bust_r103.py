#!/usr/bin/env python3
"""r103 buster: style.css v50 -> v51 across all 15 pages.

Pre-asserts the r102 ship markers and the v50 baseline before touching
anything; aborts without writing if any precondition fails.
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

errs = []
css = (ROOT / "style.css").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
web3 = (ROOT / "web3.html").read_text(encoding="utf-8")
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

# pre-asserts: r103 ships in place before we bump
ok = lambda c, m: (None if c else errs.append(m))
ok("scrollbar-width: thin; /* r103: match the page's thin themed scrollbar" in css,
   "style.css: r103 tbl-scroll comment missing")
ok("scrollbar-width:thin;scrollbar-gutter:stable;" in pricing,
   "pricing.html: r103 modal scrollbar decl missing")
ok("fetch(req, { cache: 'reload' })" in (ROOT / "sw.js").read_text(encoding="utf-8"),
   "sw.js: r103 reload fetch missing")
ok("const CACHE = 'nullvpn-v4';" in (ROOT / "sw.js").read_text(encoding="utf-8"),
   "sw.js: CACHE not v4")
# pre-asserts: r102 ships still in place
ok("r102: long payment IDs" in (ROOT / "success.html").read_text(encoding="utf-8"),
   "success.html: r102 truncation missing")
ok('<meta name="robots" content="noindex"/>' in web3, "web3.html: noindex missing")
ok(sitemap.count("<url>") == 11, "sitemap.xml: url count != 11")

if errs:
    print("bust_r103: PRE-ASSERT FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)

for page in PAGES:
    p = ROOT / page
    t = p.read_text(encoding="utf-8")
    n50 = t.count("style.css?v=50")
    n51 = t.count("style.css?v=51")
    n59 = t.count("i18n.js?v=59")
    if n50 != 1 or n51 != 0 or n59 != 1:
        print(f"bust_r103: {page} unexpected pins (v50={n50} v51={n51} i59={n59}) — abort")
        sys.exit(1)
    p.write_text(t.replace("style.css?v=50", "style.css?v=51"), encoding="utf-8")

print(f"bust_r103: OK — style v50 -> v51 on {len(PAGES)} pages (i18n v59 untouched)")
