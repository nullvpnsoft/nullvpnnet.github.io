#!/usr/bin/env python3
"""r104 buster: style.css v51 -> v52 across all 15 pages.

Pre-asserts the r104 ships (mailto sweep + gutter rule) and r103 markers
before touching anything; aborts without writing on any failure.
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
sw = (ROOT / "sw.js").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")

# r104 ships in place before the bump
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
    print("bust_r104: PRE-ASSERT FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)

for page in PAGES:
    p = ROOT / page
    t = p.read_text(encoding="utf-8")
    n51, n52, n59 = t.count("style.css?v=51"), t.count("style.css?v=52"), t.count("i18n.js?v=59")
    if n51 != 1 or n52 != 0 or n59 != 1:
        print(f"bust_r104: {page} unexpected pins (v51={n51} v52={n52} i59={n59}) — abort")
        sys.exit(1)
    p.write_text(t.replace("style.css?v=51", "style.css?v=52"), encoding="utf-8")

print(f"bust_r104: OK — style v51 -> v52 on {len(PAGES)} pages (i18n v59 untouched)")
