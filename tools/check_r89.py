#!/usr/bin/env python3
"""r89 guard: PWA manifest screenshots, web3 BreadcrumbList, brand
accent/caret tokens + anti-churn.

Anti-churn surfaces: r88 index JSON-LD (org + app) + comparison caption,
r87 ?lang= validation + standard scrollbar rule, r86 chip engine, r84
estate formula + deep-link ids, r85 keyboard region, FAQ filter,
::selection, webkit scrollbar block, AND the r45 global [hidden] guard +
its siblings — asserted byte-exact after the r89 phantom-corruption
lesson (a display-layer artifact nearly triggered a fake fix; the real
rules must never be "restored" by a round that misreads them).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
fails = []


def need(cond, msg):
    if not cond:
        fails.append(msg)


try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
style = (ROOT / "style.css").read_text(encoding="utf-8")
index = (ROOT / "index.html").read_text(encoding="utf-8")
comparison = (ROOT / "comparison.html").read_text(encoding="utf-8")
web3 = (ROOT / "web3.html").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
features = (ROOT / "features.html").read_text(encoding="utf-8")

# ---- Ship 1: manifest screenshots ----------------------------------------
mf = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
need(mf.get("id") == "/" and mf.get("name") == "NullVPN", "manifest: identity churned")
need(len(mf.get("icons", [])) == 6, "manifest: icons count changed")
need(len(mf.get("shortcuts", [])) >= 3, "manifest: shortcuts churned")
shots = mf.get("screenshots", [])
need(len(shots) == 2, f"manifest: expected 2 screenshots, got {len(shots)}")
if len(shots) == 2:
    wide = next((s for s in shots if s.get("form_factor") == "wide"), None)
    narrow = next((s for s in shots if s.get("form_factor") == "narrow"), None)
    need(wide is not None and wide["src"] == "/manifest-shot-wide.png"
         and wide["sizes"] == "1280x720" and wide.get("label"),
         "manifest: wide screenshot entry wrong")
    need(narrow is not None and narrow["src"] == "/manifest-shot-narrow.png"
         and narrow["sizes"] == "375x812" and narrow.get("label"),
         "manifest: narrow screenshot entry wrong")

for fname, dims, maxkb in [("manifest-shot-wide.png", (1280, 720), 400),
                           ("manifest-shot-narrow.png", (375, 812), 200)]:
    f = ROOT / fname
    need(f.exists(), f"{fname} missing")
    if f.exists() and HAVE_PIL:
        im = Image.open(f)
        need(im.size == dims, f"{fname}: dims {im.size} != {dims}")
        kb = f.stat().st_size // 1024
        need(kb <= maxkb, f"{fname}: {kb}KB exceeds {maxkb}KB budget")

# ---- Ship 2: web3 BreadcrumbList -----------------------------------------
blocks = re.findall(
    r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', web3, re.S)
need(len(blocks) == 1, f"web3: expected 1 ld+json block, found {len(blocks)}")
if blocks:
    d = json.loads(blocks[0])
    need(d.get("@type") == "BreadcrumbList", "web3: not a BreadcrumbList")
    items = d.get("itemListElement", [])
    need(len(items) == 2 and items[1]["name"] == "TON Web3"
         and items[1]["item"] == "https://nullvpn.net/web3.html",
         "web3: breadcrumb items wrong")

# ---- Ship 3: brand accent/caret tokens ------------------------------------
need(":root { accent-color: var(--accent); }" in style,
     "style: r89 accent-color missing")
need(".faq-filter input { caret-color: var(--accent-text); }" in style,
     "style: r89 caret-color missing")
need("r89: native controls take the brand accent" in style,
     "style: r89 comment missing")

# ---- anti-churn: r88 + r45 guard byte-exact (phantom lesson) --------------
need('<caption data-i18n="comp.table.caption">' in comparison,
     "comparison: r88 caption churned")
blocks_idx = re.findall(
    r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', index, re.S)
need(len(blocks_idx) == 2, f"index: expected 2 ld+json blocks, got {len(blocks_idx)}")
if len(blocks_idx) == 2:
    need(json.loads(blocks_idx[0]).get("@type") == "Organization",
         "index: Organization block churned")
    need(json.loads(blocks_idx[1]).get("@type") == "SoftwareApplication",
         "index: SoftwareApplication block churned")
# r45 global [hidden] guard + siblings — byte-exact, never "restore" these
need("[hidden] { display: none !important; }" in style,
     "style: r45 global hidden guard MISSING (phantom-corruption canary)")
need(".faq-filter-clear[hidden] { display: none; }" in style,
     "style: r45-era clear-button hidden rule MISSING")
need(".faq-filter-clear:not([hidden]) ~ .faq-filter-kbd { display: none; }" in style,
     "style: kbd-swap rule MISSING")
need('a[href^="http"]::after' in style, "style: print link-annotation rule MISSING")

# ---- anti-churn: r84-r87 ---------------------------------------------------
need("Object.prototype.hasOwnProperty.call(T['nav.home'], qp)" in i18n,
     "i18n: r87 ?lang= validation churned")
need("html { scrollbar-width: thin; scrollbar-color: var(--border) transparent; }" in style,
     "style: r87 scrollbar rule churned")
need("section[id], div[id], tr[id], th[id] { scroll-margin-top: calc(var(--nav-h, 120px) + 50px); }" in style,
     "style: r84 estate scroll-margin formula churned")
need("makePermalinkChip" in i18n, "i18n: r86 chip engine churned")
need('id="row-nologs"' in comparison and 'id="col-protonvpn"' in comparison,
     "comparison: r84 deep-link ids churned")
need("fonts.ready" in comparison, "comparison: r84 fonts-ready retarget churned")
need('tabindex="0" role="region"' in comparison, "comparison: r85 keyboard region churned")
need("faqFilter" in i18n, "i18n: FAQ filter engine churned")
need("::selection { background: rgba(var(--accent-rgb), 0.28); }" in style,
     "style: ::selection rule churned")
need("::-webkit-scrollbar { width: 6px; height: 6px; }" in style,
     "style: webkit scrollbar block churned")
need('id="plan-annual"' in pricing, "pricing: plan anchors churned")
need("#feat-accessibility" in features, "features: r86 chip targets churned")
need('"comp.table.caption": {' in i18n, "i18n: r88 caption key churned")

# ---- versions (pre-bust state) --------------------------------------------
for page in ["index.html", "comparison.html", "faq.html"]:
    t = (ROOT / page).read_text(encoding="utf-8")
    need("i18n.js?v=53" in t, f"{page}: i18n not v53 (pre-bust)")
    need("style.css?v=40" in t, f"{page}: style not v40 (pre-bust)")

if fails:
    print("check_r89: FAILED")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("check_r89: ALL PASS (ships + anti-churn + versions)")
