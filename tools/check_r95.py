#!/usr/bin/env python3
"""r95 guards: keyboard-lens ships — Escape-to-clear FAQ filter, reduced-motion
gate on the `/` shortcut scrollIntoView, print-hide for .faq-filter. Plus the
standing anti-churn chain (now including r94 surfaces). Pre-bust asserts
style v46 + i18n v54; --post-bust asserts style v47 + i18n v55.

NOTE (r95 process lesson): tool-output display in this environment silently
drops the two-byte sequence `[h` from grep/sed/curl text (e.g. `[hidden]`
renders as `idden]`). ALL byte-sensitive adjudication MUST happen here in
Python (in-process reads), never via displayed shell text. od -c is the only
shell-side view that is immune.
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

# --- SHIP 1: Escape-to-clear FAQ filter ---------------------------------------
esc = "faqFilter.addEventListener('keydown', (e) => {"
ok(i18.count(esc) == 1, "i18n.js: Escape keydown handler missing or duplicated")
ok("if (e.key !== 'Escape' || !faqFilter.value) return;" in i18,
   "i18n.js: Escape guard clause missing")
ok("e.preventDefault();" in i18 and "faqFilter.value = '';" in i18,
   "i18n.js: Escape clear body missing")

# --- SHIP 2: reduced-motion gate on `/` shortcut ------------------------------
ok("const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;" in i18,
   "i18n.js: reduced-motion gate missing")
ok("behavior: reduce ? 'auto' : 'smooth', block: 'center'" in i18,
   "i18n.js: gated scrollIntoView missing")
ok(i18.count("behavior: reduce ? 'auto' : 'smooth', block: 'center'") == 1,
   "i18n.js: gated scrollIntoView x!=1")  # full string: back-to-top shares the shorter form (r45)

# --- SHIP 3: print-hide .faq-filter -------------------------------------------
ok("@media print { .faq-filter { display: none !important; } }" in css,
   "style.css: print-hide .faq-filter missing")
ok(css.count("@media print { .faq-filter") == 1, "style.css: print-hide .faq-filter x!=1")
ok("@media print { .faq-cats { display: none !important; } }" in css,
   "style.css: r-print .faq-cats hide churned")

# --- anti-churn (carried forward) ----------------------------------------------
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
# r94 surfaces
for sel in (".faq-item p a, .success-note a, .hiw-note a, .nf-sub a, .dh-sub a,",
            "text-underline-offset: 2px;"):
    ok(sel in css, f"style.css: r94 prose rule churned {sel[:30]!r}")
ok(css.count("@media (forced-colors: active)") == 1, "style.css: r94 forced-colors churned")
ok('<p class="contact-sub" data-i18n="contact.sub">' in (ROOT / "contact.html").read_text(encoding="utf-8"),
   "contact.html: r94 contact-sub churned")
ll = (ROOT / "llms.txt").read_text(encoding="utf-8")
ok("## Privacy engineering" in ll, "llms.txt: r94 section churned")
# r44 trap selector must stay VALID (a[href] form) — od-verified this round
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
ok("querySelectorAll('button,a[href],input,select,textarea,[tabindex]:not([tabindex=\"-1\"])')" in pricing,
   "pricing.html: r44 focus-trap selector drifted")

# --- versions -------------------------------------------------------------------
want_s = "style.css?v=47" if "--post-bust" in sys.argv else "style.css?v=46"
want_i = "i18n.js?v=55" if "--post-bust" in sys.argv else "i18n.js?v=54"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")

if errs:
    print("check_r95: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r95: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages)")
