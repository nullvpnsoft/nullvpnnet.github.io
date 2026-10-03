#!/usr/bin/env python3
"""r96 guards: form-boundary lens ships — shareable ?q= search deep-links
(capture + sync + restore), maxlength boundary on the FAQ input, and the
reduced-motion gate for the checkout modal entrance (pricing page-local CSS).
style.css is UNTOUCHED this round (v47 must hold both sides); i18n goes
v55 (pre) -> v56 (post).
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

# --- SHIP 1: ?q= deep links ----------------------------------------------------
ok("const initialQ = (() => {" in i18, "i18n.js: initialQ capture missing")
ok("(new URLSearchParams(location.search).get('q') || '').slice(0, 80)" in i18,
   "i18n.js: initialQ read/cap missing")
ok(i18.count("const initialQ") == 1, "i18n.js: initialQ capture x!=1")
ok("if (q) u.searchParams.set('q', q);" in i18, "i18n.js: q URL sync missing")
ok("else u.searchParams.delete('q');" in i18, "i18n.js: q URL cleanup missing")
ok("if (initialQ) {" in i18 and "faqFilter.value = initialQ;" in i18,
   "i18n.js: q deep-link restore missing")
# restore must run INSIDE if(faqFilter) but AFTER the ?cat= block: it must
# appear after the emptyReset wiring (the last block before the close).
er = i18.find("faqEmptyReset")
qr = i18.find("if (initialQ) {")
ok(0 < er < qr, "i18n.js: q restore ordered before the ?cat= machinery")

# --- SHIP 2: maxlength boundary -------------------------------------------------
faq = (ROOT / "faq.html").read_text(encoding="utf-8")
ok('maxlength="80"' in faq, "faq.html: maxlength missing")
ok(faq.count('maxlength="80"') == 1, "faq.html: maxlength x!=1")

# --- SHIP 3: checkout reduced-motion gate ----------------------------------------
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
ok("@media (prefers-reduced-motion: reduce){.checkout-overlay,.checkout-modal{animation:none}.checkout-close{transition:none}}" in pricing,
   "pricing.html: reduced-motion gate missing")
ok(pricing.count("@media (prefers-reduced-motion: reduce){.checkout") == 1,
   "pricing.html: reduce block x!=1")  # r96 comment also mentions it; count the selector

# --- anti-churn (carried forward) -------------------------------------------------
ok(css.count("idden]") >= 6, "style.css: r45 hidden-attr canary regressed")
ok(":root { accent-color: var(--accent); }" in css, "style.css: r89 accent churned")
ok(css.count("@page { margin: 14mm 12mm; }") == 1, "style.css: r91 @page churned")
ok("font-variant-numeric: tabular-nums" in css, "style.css: r92 tabular churned")
ok("content: var(--print-src, none)" in css, "style.css: r93 provenance churned")
ok(css.count("body::after") == 1, "style.css: body::after collision")
idx = (ROOT / "index.html").read_text(encoding="utf-8")
ok(idx.count("og:locale:alternate") == 6, "index.html: r92 og churned")
ok('<main id="main"' in idx, "index.html: r90 landmark churned")
suc = (ROOT / "success.html").read_text(encoding="utf-8")
ok("overflow-wrap:anywhere" in suc, "success.html: r91 fix churned")
BS = chr(92)
ok(i18.count('referrerpolicy=' + BS + '"no-referrer' + BS + '"') == 81,
   "i18n.js: r93b embedded referrerpolicy count drifted")
ok(".faq-item p a, .success-note a, .hiw-note a, .nf-sub a, .dh-sub a," in css,
   "style.css: r94 prose rule churned")
ok(css.count("@media (forced-colors: active)") == 1, "style.css: r94 forced-colors churned")
ok('<p class="contact-sub" data-i18n="contact.sub">' in (ROOT / "contact.html").read_text(encoding="utf-8"),
   "contact.html: r94 contact-sub churned")
ll = (ROOT / "llms.txt").read_text(encoding="utf-8")
ok("## Privacy engineering" in ll, "llms.txt: r94 section churned")
ok("if (e.key !== 'Escape' || !faqFilter.value) return;" in i18, "i18n.js: r95 Escape churned")
ok("behavior: reduce ? 'auto' : 'smooth', block: 'center'" in i18, "i18n.js: r95 motion gate churned")
ok("@media print { .faq-filter { display: none !important; } }" in css, "style.css: r95 print-hide churned")
ok("querySelectorAll('button,a[href],input,select,textarea,[tabindex]:not([tabindex=\"-1\"])')" in
   (ROOT / "pricing.html").read_text(encoding="utf-8"), "pricing.html: r44 trap selector drifted")

# --- versions -----------------------------------------------------------------------
want_i = "i18n.js?v=56" if "--post-bust" in sys.argv else "i18n.js?v=55"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")
    ok(t.count("style.css?v=47") == 1, f"{page}: style v47 must hold (unchanged asset)")

if errs:
    print("check_r96: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r96: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages)")
