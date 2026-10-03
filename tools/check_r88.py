#!/usr/bin/env python3
"""r88 guard: SoftwareApplication JSON-LD on index, comparison <caption>,
apple-touch-icon parity on utility pages + anti-churn.

Anti-churn surfaces: r87 ?lang= validation + standard scrollbar rule,
r86 permalink chip engine, r84 estate scroll-margin formula + row/col
deep-link ids + fonts-ready retarget, r85 keyboard-scrollable region,
FAQ filter, ::selection, webkit scrollbar coexistence, index Organization
block (must remain byte-intact alongside the new SoftwareApplication).
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


i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
style = (ROOT / "style.css").read_text(encoding="utf-8")
index = (ROOT / "index.html").read_text(encoding="utf-8")
comparison = (ROOT / "comparison.html").read_text(encoding="utf-8")
p404 = (ROOT / "404.html").read_text(encoding="utf-8")
offline = (ROOT / "offline.html").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
features = (ROOT / "features.html").read_text(encoding="utf-8")

# ---- Ship 1: index SoftwareApplication JSON-LD ---------------------------
blocks = re.findall(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>', index, re.S)
need(len(blocks) == 2, f"index: expected 2 ld+json blocks, found {len(blocks)}")
if len(blocks) == 2:
    org = json.loads(blocks[0])
    app = json.loads(blocks[1])
    # Organization block untouched (long-standing, byte-equivalent facts)
    need(org.get("@type") == "Organization", "index: block 1 no longer Organization")
    need(org.get("name") == "NullVPN" and org.get("logo", "").endswith("/logo.png"),
         "index: Organization name/logo churned")
    cp = org.get("contactPoint", [])
    need(cp and cp[0].get("email") == "support@nullvpn.net",
         "index: Organization contactPoint churned")
    # SoftwareApplication — the new graph
    need(app.get("@type") == "SoftwareApplication", "index: block 2 not SoftwareApplication")
    need(app.get("name") == "NullVPN", "index: app name wrong")
    need(app.get("applicationCategory") == "SecurityApplication",
         "index: applicationCategory wrong")
    need(app.get("operatingSystem") == "Android, Web",
         "index: operatingSystem must stay factual (Android, Web)")
    need("difficult networks" in app.get("description", ""),
         "index: app description not the live meta copy")
    need(app.get("publisher", {}).get("name") == "NullVPN",
         "index: publisher missing (must be inlined, not @id-referenced)")
    offers = app.get("offers", [])
    need(len(offers) == 3, f"index: expected 3 offers, got {len(offers)}")
    prices = sorted(o.get("price") for o in offers)
    need(prices == ["10.00", "3.00", "35.00"], f"index: offer prices wrong {prices}")
    need(all(o.get("priceCurrency") == "USD" for o in offers), "index: currency wrong")
    need(all(o.get("availability") == "https://schema.org/InStock" for o in offers),
         "index: availability wrong")
    need(all(o.get("url") == "https://nullvpn.net/pricing.html" for o in offers),
         "index: offer urls must point at pricing")
    need("aggregateRating" not in json.dumps(app),
         "index: aggregateRating must never appear (no fabricated ratings)")

# ---- Ship 2: comparison <caption> ----------------------------------------
need('<caption data-i18n="comp.table.caption">' in comparison,
     "comparison: caption element missing/i18n key wrong")
cap_pos = comparison.find('<caption data-i18n="comp.table.caption">')
thead_pos = comparison.find("<thead>")
need(0 < cap_pos < thead_pos, "comparison: caption must precede thead inside table")
need('Feature matrix — identical criteria checked for every service.</caption>' in comparison,
     "comparison: EN caption copy drifted")
need(".comp-table-wrap caption{caption-side:top;text-align:start;padding:0 0 12px;"
     "font-size:.72rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;"
     "color:var(--text2);}" in comparison,
     "comparison: r88 caption eyebrow rule missing/altered")
need("r88: the matrix finally carries a real <caption>" in comparison,
     "comparison: r88 caption comment missing")
# i18n key complete in all 7 locales
need('"comp.table.caption": {' in i18n, "i18n: comp.table.caption key missing")
need('ru: "Матрица функций — одни и те же критерии проверены для каждого сервиса.",' in i18n,
     "i18n: caption ru missing")
need("fr: \"Matrice des fonctionnalités — les mêmes critères vérifiés pour chaque service.\"," in i18n,
     "i18n: caption fr missing")

# ---- Ride-along: touch-icon parity ---------------------------------------
need('rel="apple-touch-icon"' in p404, "404: apple-touch-icon missing")
need('rel="apple-touch-icon"' in offline, "offline: apple-touch-icon missing")

# ---- anti-churn: prior rounds --------------------------------------------
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
need(".comp-table-wrap tbody tr:target{box-shadow:0 0 0 3px rgba(var(--accent-rgb),.28);}" in comparison,
     "comparison: r84 :target ring churned")
need('tabindex="0" role="region"' in comparison, "comparison: r85 keyboard region churned")
need("faqFilter" in i18n, "i18n: FAQ filter engine churned")
need("::selection { background: rgba(var(--accent-rgb), 0.28); }" in style,
     "style: ::selection rule churned")
need('id="plan-annual"' in pricing, "pricing: plan anchors churned")
need("#feat-accessibility" in features, "features: r86 chip targets churned")

# ---- versions (pre-bust state) --------------------------------------------
for page in ["index.html", "comparison.html", "pricing.html"]:
    t = (ROOT / page).read_text(encoding="utf-8")
    need("i18n.js?v=52" in t, f"{page}: i18n not v52 (pre-bust)")
    need("style.css?v=40" in t, f"{page}: style not v40")

if fails:
    print("check_r88: FAILED")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("check_r88: ALL PASS (ships + anti-churn + versions)")
