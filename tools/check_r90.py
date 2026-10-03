#!/usr/bin/env python3
"""r90 guard: <main> landmark on all content pages, print-rule parity,
prefers-contrast border lift + anti-churn.

Anti-churn surfaces: r89 manifest screenshots + web3 breadcrumb + accent
tokens, r88 index JSON-LD + comparison caption, r87 ?lang= + scrollbar,
r86 chips, r84 formula/ids/rings, r85 keyboard region, FAQ filter,
::selection, webkit scrollbar block, and the r45 global [hidden] guard
(phantom-corruption canary, byte-exact).
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


SWAPPED = ["index.html", "features.html", "how-it-works.html", "pricing.html",
           "comparison.html", "faq.html", "download.html", "refund.html",
           "privacy.html", "terms.html", "contact.html", "web3.html", "success.html"]

i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
style = (ROOT / "style.css").read_text(encoding="utf-8")
index = (ROOT / "index.html").read_text(encoding="utf-8")
comparison = (ROOT / "comparison.html").read_text(encoding="utf-8")
web3 = (ROOT / "web3.html").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
features = (ROOT / "features.html").read_text(encoding="utf-8")

# ---- Ship 1: <main> landmark swap ----------------------------------------
for name in SWAPPED:
    t = (ROOT / name).read_text(encoding="utf-8")
    need('<section id="main"' not in t, f"{name}: leftover <section id=\"main\">")
    need(t.count('<main id="main"') == 1, f"{name}: <main id=\"main\"> x{t.count('<main id=\"main\"')}")
    need(t.count("<main") == t.count("</main>"), f"{name}: unbalanced main tags")
# 404/offline already had <main>
for name in ["404.html", "offline.html"]:
    t = (ROOT / name).read_text(encoding="utf-8")
    need("<main" in t, f"{name}: main landmark missing")
# no page may end up with two <main>
for name in SWAPPED + ["404.html", "offline.html"]:
    t = (ROOT / name).read_text(encoding="utf-8")
    need(t.count("<main") == 1, f"{name}: expected exactly 1 <main>")

# ---- Ship 2: print rule parity --------------------------------------------
need("section, main { padding: 14px 0 !important; }" in style,
     "style: print section/main padding rule missing")
need("r90: main joins the padding rule" in style, "style: r90 print comment missing")

# ---- Ship 3: prefers-contrast border lift --------------------------------
need(":root { --text2: #55482e; --border: #8f7448; }" in style,
     "style: r90 light contrast tokens missing")
need('[data-theme="dark"] { --text2: #c3cedd; --border: #64789a; }' in style,
     "style: r90 dark contrast tokens missing")
need("r90: borders join the lift" in style, "style: r90 contrast comment missing")

# ---- anti-churn: r88/r89 --------------------------------------------------
mf = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
need(len(mf.get("screenshots", [])) == 2, "manifest: screenshots churned")
need("BreadcrumbList" in web3, "web3: r89 breadcrumb churned")
need(":root { accent-color: var(--accent); }" in style, "style: r89 accent-color churned")
need(".faq-filter input { caret-color: var(--accent-text); }" in style,
     "style: r89 caret-color churned")
blocks_idx = re.findall(
    r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', index, re.S)
need(len(blocks_idx) == 2, f"index: ld+json blocks {len(blocks_idx)}")
if len(blocks_idx) == 2:
    need(json.loads(blocks_idx[1]).get("@type") == "SoftwareApplication",
         "index: SoftwareApplication churned")
need('<caption data-i18n="comp.table.caption">' in comparison, "comparison: r88 caption churned")
need('"comp.table.caption": {' in i18n, "i18n: r88 caption key churned")

# ---- anti-churn: r84-r87 + r45 canary ------------------------------------
need("[hidden] { display: none !important; }" in style,
     "style: r45 global hidden guard MISSING (canary)")
need(".faq-filter-clear[hidden] { display: none; }" in style,
     "style: clear-button hidden rule MISSING (canary)")
need(".faq-filter-clear:not([hidden]) ~ .faq-filter-kbd { display: none; }" in style,
     "style: kbd-swap rule MISSING (canary)")
need('a[href^="http"]::after' in style, "style: print link-annotation rule MISSING (canary)")
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

# ---- versions (pre-bust state) --------------------------------------------
for page in ["index.html", "comparison.html", "faq.html"]:
    t = (ROOT / page).read_text(encoding="utf-8")
    need("i18n.js?v=53" in t, f"{page}: i18n not v53 (pre-bust)")
    need("style.css?v=41" in t, f"{page}: style not v41 (pre-bust)")

if fails:
    print("check_r90: FAILED")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("check_r90: ALL PASS (ships + anti-churn + versions)")
