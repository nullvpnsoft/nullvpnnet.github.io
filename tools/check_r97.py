#!/usr/bin/env python3
"""r97 guards: offline-navigation lens — SW nav cache normalization (pathname
keys + ignoreSearch fallback matching), probe-verified reconnect (no blind
reload on radio-wake 'online' events), and the zero-layout-shift back-online
toast. i18n goes v56 (pre) -> v57 (post); style v47 holds; sw.js and
offline.html are unversioned (SW byte-diff / precache refresh propagate them).
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

sw = (ROOT / "sw.js").read_text(encoding="utf-8")
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
off = (ROOT / "offline.html").read_text(encoding="utf-8")

# --- SHIP 1: SW nav cache normalization ----------------------------------------
ok("caches.match(req, { ignoreSearch: true })" in sw, "sw.js: ignoreSearch match missing")
ok(sw.count("ignoreSearch: true") == 1, "sw.js: ignoreSearch x!=1")
ok("clean.search = '';" in sw and "clean.hash = '';" in sw, "sw.js: nav key normalization missing")
ok("c.put(new Request(clean.href), copy)" in sw, "sw.js: normalized nav put missing")
ok("r97: navigations are cached under their PATHNAME" in sw, "sw.js: r97 header comment missing")
ok("const CACHE = 'nullvpn-v3';" in sw, "sw.js: cache name churned")

# --- SHIP 2: probe-verified reconnect --------------------------------------------
ok("fetch('/', { method: 'HEAD', cache: 'no-store' })" in i18,
   "i18n.js: reconnect probe missing")
ok("if (!r.ok) return;" in i18, "i18n.js: probe ok-guard missing")
ok("still offline: stay silent, listener re-arms" in i18, "i18n.js: probe failure path missing")
ok(i18.count("setTimeout(() => location.reload(), 900)") == 1,
   "i18n.js: reload timing x!=1")

# --- SHIP 3: fixed toast ----------------------------------------------------------
ok("position: fixed; left: 50%; bottom: 26px; transform: translate(-50%, 0);" in off,
   "offline.html: fixed toast missing")
ok("box-shadow: 0 6px 18px rgba(0,0,0,.28); z-index: 80;" in off,
   "offline.html: toast shadow/z-index missing")
ok("transform: translate(-50%, 4px)" in off, "offline.html: toast keyframe transform missing")
ok("width: max-content; max-width: calc(100vw - 32px);" in off, "offline.html: toast width guard missing")

# --- anti-churn (carried forward) ---------------------------------------------------
css = (ROOT / "style.css").read_text(encoding="utf-8")
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
ok("const initialQ = (() => {" in i18, "i18n.js: r96 deep-link churned")
ok("if (q) u.searchParams.set('q', q);" in i18, "i18n.js: r96 q sync churned")
faq = (ROOT / "faq.html").read_text(encoding="utf-8")
ok('maxlength="80"' in faq, "faq.html: r96 maxlength churned")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
ok(pricing.count("@media (prefers-reduced-motion: reduce){.checkout") == 1,
   "pricing.html: r96 reduce gate churned")
ok("querySelectorAll('button,a[href],input,select,textarea,[tabindex]:not([tabindex=\"-1\"])')" in pricing,
   "pricing.html: r44 trap selector drifted")

# --- versions -----------------------------------------------------------------------
want_i = "i18n.js?v=57" if "--post-bust" in sys.argv else "i18n.js?v=56"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")
    ok(t.count("style.css?v=47") == 1, f"{page}: style v47 must hold (unchanged asset)")

if errs:
    print("check_r97: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r97: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages)")
