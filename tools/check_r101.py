#!/usr/bin/env python3
"""r101 guards: checkout modal re-audit (least-recently-audited surface).

Finding (live QA repro): .checkout-modal had no max-height/overflow — on a
380px-tall landscape phone the centered dialog measured 404px with
scrollable:false: the CTAs were clipped and unreachable, and mobile has no
Escape key. Fixed with max-height + overflow-y:auto + overscroll-behavior.

FEATURE: in-modal plan switcher — three chips (monthly/quarterly/annual)
reusing the price.pN.name keys (zero new i18n vocabulary; group aria-label
reuses price.h). openCheckout's body was refactored into updatePlan(plan),
the single mutation path (h3 name + amount + chip state) shared by the plan
cards and the delegated chip listener. aria-pressed tracks the selection;
the r44 focus trap already recomputes per keypress, so the chips join the
cycle for free. Chip styling mirrors the faq-cat language (r98 boundary).

NOTE: checkout styles are page-local (pricing.html inline <style>) — this
round touches NO external asset, so i18n v59 + style v50 are asserted on
BOTH sides of the gate (no buster).
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
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
offline = (ROOT / "offline.html").read_text(encoding="utf-8")

# --- SHIP 1: in-modal plan switcher ------------------------------------------------------
ok('<div class="checkout-plans" role="group" data-i18n-aria="price.h" aria-label="Pricing">' in pricing,
   "pricing.html: checkout-plans group markup missing")
ok(pricing.count('data-plan="') == 3, "pricing.html: data-plan chips x!=3")
ok(pricing.count('aria-pressed="true"') == 1 and pricing.count('aria-pressed="false"') == 2,
   "pricing.html: aria-pressed initial state wrong")
ok(pricing.count('data-i18n="price.p1.name"') == 3, "pricing.html: p1.name usage x!=3 (card+modal h3+chip)")
ok(pricing.count('data-i18n="price.p3.name"') == 2, "pricing.html: p3.name usage x!=2 (card+chip)")
ok(pricing.count('data-i18n="price.p4.name"') == 2, "pricing.html: p4.name usage x!=2 (card+chip)")
ok("function updatePlan(plan){" in pricing, "pricing.html: updatePlan missing")
ok("window.openCheckout=function(plan){\n    updatePlan(plan);" in pricing,
   "pricing.html: openCheckout does not route through updatePlan")
ok("chips[i].classList.toggle('active',on);" in pricing and
   "chips[i].setAttribute('aria-pressed',on?'true':'false');" in pricing,
   "pricing.html: chip state sync missing")
ok("var b=e.target.closest('.checkout-plan');" in pricing and
   "if(b)updatePlan(b.getAttribute('data-plan'));" in pricing,
   "pricing.html: delegated chip listener missing")
# r44 comments/infra must have survived the refactor
ok("// r44: re-apply translations so the freshly swapped plan name renders in" in pricing,
   "pricing.html: r44 re-apply comment churned")

# --- SHIP 2: landscape clip fix + chip styling (page-local styles) ------------------------
ok("max-height:calc(100vh - 32px);overflow-y:auto;overscroll-behavior:contain;" in pricing,
   "pricing.html: modal scroll-escape missing")
ok("border:1px solid var(--border-strong,#64748b);cursor:pointer; /* r101: chip boundary 1.4.11 */" in pricing,
   "pricing.html: chip boundary comment/decl churned")
ok(".checkout-plan.active { background: var(--accent2); border-color: var(--accent2); color: #fff; }" in pricing,
   "pricing.html: chip active state missing")
ok(".checkout-plan:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }" in pricing,
   "pricing.html: chip focus-visible missing")
ok("@media (hover: hover) and (pointer: fine) { .checkout-plan:hover { color: var(--accent-text); border-color: var(--accent); } }" in pricing,
   "pricing.html: chip hover (opacity-trap-free) missing")
ok(".checkout-close{transition:none}.checkout-plan{transition:none}}" in pricing,
   "pricing.html: reduced-motion chip gate missing")
# r98 dialog boundary must survive the line edit
ok("border:1px solid var(--border-strong,#64748b);border-radius:16px; /* r98: dialog boundary 1.4.11 */" in pricing,
   "pricing.html: r98 modal boundary churned")

# --- carried-forward chains (r44-r100 highlights) -----------------------------------------
ok("let lastFilterLang = null; // r100: boot guard" in i18,
   "i18n.js: r100 lastFilterLang declaration churned")
ok("const langChanged = lastFilterLang !== null && lastFilterLang !== lang;" in i18,
   "i18n.js: r100 langChanged guard churned")
ok("statusEl.textContent = t('faq.filter.cleared', lang);" in i18,
   "i18n.js: r100 cleared-note write churned")
ok(i18.count('"faq.filter.cleared"') == 1, "i18n.js: cleared key x!=1")
ok("14) Live OS-theme follow (r99)" in i18, "i18n.js: r99 OS-follow churned")
ok("if (localStorage.getItem('theme')) return; /* explicit choice wins */" in i18,
   "i18n.js: r99 explicit-choice guard churned")
ok(".theme-btn:hover:not(.active) { border-color: var(--accent-text); color: var(--accent-text); }" in css,
   "style.css: r99 hover rework churned")
ok(css.count("border: 1px solid var(--border);") == 12,
   "style.css: decorative plain-border inventory changed (expected 12)")
ok(css.count("border: 1px solid var(--border-strong)") == 10,
   "style.css: border-strong shorthand count changed (expected 10)")
ok(css.count("--border-strong:") == 2, "style.css: token count changed")
ok("r98: functional boundaries" in css, "style.css: r98 token comment churned")
ok("border: 1px solid var(--border-strong); background: var(--bg3); /* r98: offline nav chips are functional links */" in offline,
   "offline.html: r98 chip swap churned")
ok("caches.match(req, { ignoreSearch: true })" in (ROOT / "sw.js").read_text(encoding="utf-8"),
   "sw.js: r97 normalization churned")
ok("fetch('/', { method: 'HEAD', cache: 'no-store' })" in i18, "i18n.js: r97 probe churned")
ok("if (e.key !== 'Escape' || !faqFilter.value) return;" in i18, "i18n.js: r95 Escape churned")
ok("behavior: reduce ? 'auto' : 'smooth', block: 'center'" in i18, "i18n.js: r95 motion gate churned")
ok("@media print { .faq-filter { display: none !important; } }" in css, "style.css: r95 print-hide churned")
ok("if (q) u.searchParams.set('q', q);" in i18, "i18n.js: r96 q sync churned")
ok('maxlength="80"' in (ROOT / "faq.html").read_text(encoding="utf-8"), "faq.html: r96 maxlength churned")
ok(pricing.count("@media (prefers-reduced-motion: reduce){.checkout") == 1,
   "pricing.html: r96 reduce gate churned")
TRAP = ("querySelectorAll('button,a" + chr(91) + "href" + chr(93) +
        ",input,select,textarea," + chr(91) + "tabindex" + chr(93) + ":not(" +
        chr(91) + 'tabindex="-1"' + chr(93) + ")')")
ok(TRAP in pricing, "pricing.html: r44 trap selector drifted")
ok(css.count("idden]") >= 6, "style.css: r45 hidden-attr canary regressed")
ok(":root { accent-color: var(--accent); }" in css, "style.css: r89 accent churned")
ok(css.count("@page { margin: 14mm 12mm; }") == 1, "style.css: r91 @page churned")
ok("font-variant-numeric: tabular-nums" in css, "style.css: r92 tabular churned")
ok("content: var(--print-src, none)" in css, "style.css: r93 provenance churned")
ok(css.count("body::after") == 1, "style.css: body::after collision")
ok(".faq-item p a, .success-note a, .hiw-note a, .nf-sub a, .dh-sub a," in css,
   "style.css: r94 prose rule churned")
ok(css.count("@media (forced-colors: active)") == 1, "style.css: r94 forced-colors churned")
ok("## Privacy engineering" in (ROOT / "llms.txt").read_text(encoding="utf-8"),
   "llms.txt: r94 section churned")

# --- LIVING WCAG MATH (r98) --------------------------------------------------------------
import re

def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _lum(hx):
    h = hx.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(fg, bg):
    a, b = sorted([_lum(fg), _lum(bg)], reverse=True)
    return (a + 0.05) / (b + 0.05)

def parse_block(marker):
    i = css.index(marker)
    j = css.index("}", i)
    return dict(re.findall(r"(--[a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", css[i:j]))

for marker, theme in ((":root {", "light"), ('[data-theme="dark"] {', "dark")):
    v = parse_block(marker)
    bs = v.get("--border-strong")
    for sname in ("--bg", "--bg2", "--bg3"):
        r = ratio(bs, v[sname])
        ok(r >= 3.0, f"{theme}: border-strong vs {sname} = {r:.2f} < 3.0")
    for tname in ("--text2", "--accent-text"):
        for sname in ("--bg", "--bg2", "--bg3"):
            r = ratio(v[tname], v[sname])
            ok(r >= 4.5, f"{theme}: {tname} vs {sname} = {r:.2f} < 4.5")

# --- versions (NO asset change this round: v59/v50 asserted on BOTH sides) ---------------
want_i, want_s = "i18n.js?v=59", "style.css?v=50"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")

if errs:
    print("check_r101: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r101: ALL GREEN ({len(PAGES)} pages, no-asset-bump round)")
