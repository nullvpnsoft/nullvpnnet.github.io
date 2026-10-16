#!/usr/bin/env python3
"""r106 buster: style.css v53 -> v54 across all 15 pages.

style.css changed this round (orphans/widows rag control); i18n.js and
sw.js are untouched (v60 / nullvpn-v4 carried). features.html and the
deploy script changed too but carry no cache pins. Pre-asserts the r106
ships and the r105 markers before touching anything; aborts without
writing on any failure.
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
feat = (ROOT / "features.html").read_text(encoding="utf-8")
deploy_sh = (ROOT / "tools" / "deploy_historyless.sh").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")

# r106 ships in place before the bump
ok("p, li, dd, dt, figcaption { orphans: 3; widows: 3; }" in css,
   "style.css: r106 orphans/widows rule missing")
ok(".feat-table-wrap { overflow-x: auto; margin-top: 32px; scrollbar-width: thin; scrollbar-color: var(--border) transparent; -webkit-overflow-scrolling: touch; }" in feat,
   "features.html: r106 thin-scrollbar decl missing")
ok("[0/5] stamping sitemap lastmod" in deploy_sh, "deploy script: r106 stamp step missing")
ok('sed -i.bak "s|<lastmod>' in deploy_sh, "deploy script: r106 stamp sed missing")
ok("TZ=Asia/Shanghai date +%F" in deploy_sh, "deploy script: r106 TZ stamp missing")

# r105 markers still in place
ok('@supports (content: "x" / "")' in css, "style.css: r105 @supports block churned")
ok('content: "SOON" / "";' in css, "style.css: r105 decorative SOON churned")
ok("margin-inline-start: 10px;" in css, "style.css: r105 RTL margin fix churned")
ok('class="nf-search" role="search" action="/faq.html" method="get"' in nf404,
   "404.html: r105 search form churned")
ok('"nf.search.ph": {' in i18 and '"nf.search.go": {' in i18,
   "i18n.js: r105 nf.search keys churned")
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
    print("bust_r106: PRE-ASSERT FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)

for page in PAGES:
    p = ROOT / page
    t = p.read_text(encoding="utf-8")
    n53, n54, n60 = (t.count("style.css?v=53"), t.count("style.css?v=54"),
                     t.count("i18n.js?v=60"))
    if n53 != 1 or n54 != 0 or n60 != 1:
        print(f"bust_r106: {page} unexpected pins (v53={n53} v54={n54} i60={n60}) — abort")
        sys.exit(1)
    p.write_text(t.replace("style.css?v=53", "style.css?v=54"), encoding="utf-8")

print(f"bust_r106: OK — style v53 -> v54 on {len(PAGES)} pages (i18n v60 untouched)")
