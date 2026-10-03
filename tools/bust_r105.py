#!/usr/bin/env python3
"""r105 buster: style.css v52 -> v53 AND i18n.js v59 -> v60 across all 15 pages.

Both estate files changed this round (SOON-pill decorative content + RTL
margin fix in style.css; nf.search.* keys in i18n.js for the 404 FAQ-search
form), so both busters run. Pre-asserts the r105 ships and the r104/r103
markers before touching anything; aborts without writing on any failure.
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
def ok(cond, msg):
    if not cond:
        errs.append(msg)

css = (ROOT / "style.css").read_text(encoding="utf-8")
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
sw = (ROOT / "sw.js").read_text(encoding="utf-8")
nf404 = (ROOT / "404.html").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")

# r105 ships in place before the bump
ok('@supports (content: "x" / "")' in css, "style.css: r105 @supports block missing")
ok('content: "SOON" / "";' in css, "style.css: r105 decorative SOON missing")
ok("margin-inline-start: 10px;" in css, "style.css: r105 RTL margin fix missing")
ok('class="nf-search" role="search" action="/faq.html" method="get"' in nf404,
   "404.html: r105 search form missing")
ok('name="q" maxlength="80"' in nf404, "404.html: r105 q input missing")
ok('data-i18n="nf.search.ph"' in nf404, "404.html: r105 placeholder key missing")
ok('data-i18n-aria="nf.search.ph"' in nf404, "404.html: r105 aria key missing")
ok('data-i18n="nf.search.go"' in nf404, "404.html: r105 submit key missing")
ok('"nf.search.ph": {' in i18, "i18n.js: nf.search.ph key missing")
ok('"nf.search.go": {' in i18, "i18n.js: nf.search.go key missing")

# r104 markers still in place
ok("html { scrollbar-width: thin; scrollbar-color: var(--border) transparent; scrollbar-gutter: stable; }" in css,
   "style.css: r104 gutter rule missing")
total_mailto = 0
bare = 0
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    total_mailto += t.count('href="mailto:support@nullvpn.net?subject=NullVPN%20Support"')
    bare += t.count('href="mailto:support@nullvpn.net"')
ok(total_mailto == 16, f"mailto subject count {total_mailto} != 16")
ok(bare == 0, f"bare mailto residue {bare} != 0")

# r103 markers still in place
ok("fetch(req, { cache: 'reload' })" in sw, "sw.js: r103 reload fetch churned")
ok("const CACHE = 'nullvpn-v4';" in sw, "sw.js: CACHE not v4")
ok("scrollbar-width:thin;scrollbar-gutter:stable;" in pricing,
   "pricing.html: r103 modal scrollbar decl churned")

if errs:
    print("bust_r105: PRE-ASSERT FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)

for page in PAGES:
    p = ROOT / page
    t = p.read_text(encoding="utf-8")
    n52, n53, n59, n60 = (t.count("style.css?v=52"), t.count("style.css?v=53"),
                          t.count("i18n.js?v=59"), t.count("i18n.js?v=60"))
    if n52 != 1 or n53 != 0 or n59 != 1 or n60 != 0:
        print(f"bust_r105: {page} unexpected pins (v52={n52} v53={n53} i59={n59} i60={n60}) — abort")
        sys.exit(1)
    t = t.replace("style.css?v=52", "style.css?v=53")
    t = t.replace("i18n.js?v=59", "i18n.js?v=60")
    p.write_text(t, encoding="utf-8")

print(f"bust_r105: OK — style v52 -> v53 + i18n v59 -> v60 on {len(PAGES)} pages")
