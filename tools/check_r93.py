#!/usr/bin/env python3
"""r93 guards: referrerpolicy="no-referrer" on all outbound links (privacy —
no Referer leakage of ?lang/deep-links to t.me/github/tonviewer), comparison
print @page landscape, print provenance footer (--print-src on legal pages),
plus standing anti-churn. Pre-bust asserts v44; --post-bust asserts v45.
"""
import re
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

# --- SHIP 1: referrerpolicy on outbound links --------------------------------
ext_total = 0
for pg in PAGES:
    t = (ROOT / pg).read_text(encoding="utf-8")
    for m in re.finditer(r'<a\s[^>]*href="(https?://[^"]+)"[^>]*>', t):
        if "nullvpn.net" in m.group(1):
            continue
        ext_total += 1
        ok('referrerpolicy="no-referrer"' in m.group(0), f"{pg}: outbound link missing referrerpolicy: {m.group(1)[:60]}")
ok(ext_total == 32, f"expected 32 outbound links estate-wide, found {ext_total}")

# --- SHIP 2: comparison landscape print ---------------------------------------
c = (ROOT / "comparison.html").read_text(encoding="utf-8")
ok("@page{size:landscape;}" in c, "comparison.html: landscape @page missing")
ok("r93: the 752px matrix" in c, "comparison.html: r93 comment missing")

# --- SHIP 3: provenance footer ------------------------------------------------
css = (ROOT / "style.css").read_text(encoding="utf-8")
ok("content: var(--print-src, none)" in css, "style.css: provenance rule missing")
ok(css.count("body::after") == 1, "style.css: body::after collision")
for pg, slug in [("terms.html", "terms"), ("privacy.html", "privacy"), ("refund.html", "refund")]:
    t = (ROOT / pg).read_text(encoding="utf-8")
    ok(f"--print-src: 'Source: https://nullvpn.net/{slug}.html'" in t,
       f"{pg}: --print-src opt-in missing")

# --- SHIP 1b: embedded anchors inside i18n.js translations carry it too -----
# (setLang rebuilds translated HTML via innerHTML — attrs must live in the
# strings themselves; grep must use ESCAPED quotes href=\" inside i18n.js)
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
BS = chr(92)  # backslash — translation strings carry ESCAPED quotes
RP = 'referrerpolicy=' + BS + '"no-referrer' + BS + '"'
NOOP = 'rel=' + BS + '"noopener' + BS + '"'
ok(i18.count(RP) == 81, f"i18n.js: embedded referrerpolicy count != 81 (got {i18.count(RP)})")
bare = [i for i in range(len(i18)) if i18.startswith(NOOP, i) and not i18[i + len(NOOP):i + len(NOOP) + 40].lstrip().startswith(RP)]
ok(not bare, f"i18n.js: {len(bare)} noopener anchors without referrerpolicy")

# --- anti-churn ---------------------------------------------------------------
ok(css.count("idden]") >= 6, "style.css: r45 canary regressed")
ok(":root { accent-color: var(--accent); }" in css, "style.css: r89 accent churned")
ok(css.count("@page { margin: 14mm 12mm; }") == 1, "style.css: r91 @page churned")
ok("font-variant-numeric: tabular-nums" in css, "style.css: r92 tabular churned")
idx = (ROOT / "index.html").read_text(encoding="utf-8")
ok(idx.count("og:locale:alternate") == 6, "index.html: r92 og alternates churned")
ok('<main id="main"' in idx and '"@type": "SoftwareApplication"' in idx, "index.html: r90/r88 churned")
suc = (ROOT / "success.html").read_text(encoding="utf-8")
ok("overflow-wrap:anywhere" in suc, "success.html: r91 overflow fix churned")

# --- versions -----------------------------------------------------------------
want_i = "i18n.js?v=54" if "--post-bust" in sys.argv else "i18n.js?v=53"
want_s = "style.css?v=45"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")

if errs:
    print("check_r93: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r93: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages, {ext_total} outbound links)")
