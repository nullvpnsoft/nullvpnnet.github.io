#!/usr/bin/env python3
"""r94 guards: prose-link underlines (WCAG 1.4.1 + forced-colors resilience),
forced-colors:active block, contact-sub class hook, llms.txt Privacy
engineering section, plus standing anti-churn. Pre-bust asserts v45;
--post-bust asserts v46. i18n stays v54 both sides.
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

# --- SHIP 1: prose-link underline rule ---------------------------------------
css = (ROOT / "style.css").read_text(encoding="utf-8")
for sel in (".faq-item p a, .success-note a, .hiw-note a, .nf-sub a, .dh-sub a,",
            "text-underline-offset: 2px;", "r94: prose links get an accent underline"):
    ok(sel in css, f"style.css: prose rule missing {sel[:40]!r}")

# --- SHIP 2: forced-colors block ----------------------------------------------
ok("@media (forced-colors: active) {" in css, "style.css: forced-colors block missing")
ok(".yes, .no, .partial, .lg-swatch { forced-color-adjust: none; }" in css,
   "style.css: verdict forced-color-adjust missing")
ok(".btn-primary, .btn-nav-primary { forced-color-adjust: none; }" in css,
   "style.css: CTA forced-color-adjust missing")
ok(css.count("@media (forced-colors: active)") == 1, "style.css: forced-colors block x!=1")

# --- SHIP 3: contact-sub hook + llms section ----------------------------------
con = (ROOT / "contact.html").read_text(encoding="utf-8")
ok('<p class="contact-sub" data-i18n="contact.sub">' in con, "contact.html: contact-sub hook missing")
ll = (ROOT / "llms.txt").read_text(encoding="utf-8")
ok("## Privacy engineering" in ll, "llms.txt: Privacy engineering missing")
ok('referrerpolicy="no-referrer"' in ll, "llms.txt: referrerpolicy fact missing")
ok(ll.count("no third-party scripts") == 1, "llms.txt: duplicated tracking claim")

# --- anti-churn ---------------------------------------------------------------
ok(css.count("idden]") >= 6, "style.css: r45 canary regressed")
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
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")
BS = chr(92)
ok(i18.count('referrerpolicy=' + BS + '"no-referrer' + BS + '"') == 81,
   "i18n.js: r93b embedded referrerpolicy count drifted")

# --- versions -----------------------------------------------------------------
want_s = "style.css?v=46" if "--post-bust" in sys.argv else "style.css?v=45"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")
    ok(t.count("i18n.js?v=54") == 1, f"{page}: expected i18n.js?v=54 x1")

if errs:
    print("check_r94: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r94: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages)")
