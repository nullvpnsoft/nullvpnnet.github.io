#!/usr/bin/env python3
"""r92 guards: og:locale:alternate x6 on all 15 pages (factual locales),
FAQ filter mobile UX attrs (enterkeyhint/autocapitalize), tabular-nums on
price figures, llms.txt Security section, plus standing anti-churn
(r45/r88/r89/r90/r91). Run pre-bust (v43) and post-bust (v44 --post-bust).
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
ALTS = ["ru_RU", "fa_IR", "ar_AR", "es_ES", "ne_NP", "fr_FR"]

errs = []
def ok(cond, msg):
    if not cond:
        errs.append(msg)

# --- SHIP 1: og:locale:alternate --------------------------------------------
for pg in PAGES:
    t = (ROOT / pg).read_text(encoding="utf-8")
    ok(t.count('<meta property="og:locale" content="en_US"/>') == 1,
       f"{pg}: og:locale anchor x{t.count('<meta property=\"og:locale\" content=\"en_US\"/>')}")
    for l in ALTS:
        ok(f'<meta property="og:locale:alternate" content="{l}"/>' in t,
           f"{pg}: missing og:locale:alternate {l}")
    ok(t.count('og:locale:alternate') == 6, f"{pg}: alternates count != 6")

# --- SHIP 2: FAQ filter mobile UX -------------------------------------------
faq = (ROOT / "faq.html").read_text(encoding="utf-8")
ok('enterkeyhint="search"' in faq and 'autocapitalize="off"' in faq,
   "faq.html: filter input missing enterkeyhint/autocapitalize")
ok(".faq-filter input::-webkit-search-cancel-button { display: none; }" in (ROOT / "style.css").read_text(encoding="utf-8"),
   "style.css: native search cancel un-hidden (double-clear regression)")

# --- SHIP 3: tabular-nums on price figures ----------------------------------
css = (ROOT / "style.css").read_text(encoding="utf-8")
ok("font-variant-numeric: tabular-nums" in css, "style.css: .price tabular-nums missing")
ok("r92: tabular digits" in css, "style.css: r92 comment missing")
pr = (ROOT / "pricing.html").read_text(encoding="utf-8")
ok("font-variant-numeric:tabular-nums}" in pr, "pricing.html: .checkout-amount tabular-nums missing")

# --- SHIP 4: llms.txt Security section --------------------------------------
ll = (ROOT / "llms.txt").read_text(encoding="utf-8")
ok("## Security" in ll, "llms.txt: Security section missing")
ok("/.well-known/security.txt" in ll, "llms.txt: security.txt path missing")
sec = (ROOT / ".well-known" / "security.txt").read_text(encoding="utf-8")
ok(sec.count("Contact: ") == 2 and "Expires: 2027-04-02T00:00:00Z" in sec,
   "security.txt: r91 surface churned")

# --- anti-churn: standing surfaces ------------------------------------------
ok(css.count("idden]") >= 6, "style.css: r45 [hidden]-guard family regressed (canary)")
ok(":root { accent-color: var(--accent); }" in css, "style.css: r89 accent-color churned")
ok(css.count("@page { margin: 14mm 12mm; }") == 1, "style.css: r91 @page churned")
ok("section, main { padding: 14px 0 !important; }" in css, "style.css: r90 print parity churned")
idx = (ROOT / "index.html").read_text(encoding="utf-8")
ok('<main id="main"' in idx and '"@type": "SoftwareApplication"' in idx,
   "index.html: r90 landmark or r88 JSON-LD churned")
suc = (ROOT / "success.html").read_text(encoding="utf-8")
ok("overflow-wrap:anywhere" in suc, "success.html: r91 overflow fix churned")

# --- versions ----------------------------------------------------------------
want_s, want_i = ("style.css?v=44", "i18n.js?v=53") if "--post-bust" in sys.argv else ("style.css?v=43", "i18n.js?v=53")
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")

if errs:
    print("check_r92: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r92: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages)")
