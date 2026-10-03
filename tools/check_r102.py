#!/usr/bin/env python3
"""r102 guards: least-audited surfaces sweep (success flow + web3 bridge).

BASELINE QA verdict: both surfaces functionally healthy (plan localization,
bogus/no-param fallbacks, copy chip, RTL flip, web3 cancel/bfcache) — no bugs.
Ships are hygiene + readability, found by the sweep:

SHIP 1 (success.html): long payment IDs (113-char JWT-ish strings observed)
rendered as a 3-line monospace blob (r91 anywhere-wrap made it survivable,
not readable). Now truncated to first12 + ellipsis + last8 — enough to match
the ID against the bot/wallet receipt. Full value preserved twice: title
tooltip on the span, data-copy on the chip (copy stays lossless).

SHIP 2 (web3.html + sitemap.xml): the 1.5s auto-redirect bridge was the only
utility page missing noindex (success/offline/404 all have it) AND was still
listed in sitemap.xml — an indexed bridge page is a doorway-signal liability
and a dead search result. noindex added, sitemap entry removed (12 -> 11).

NO external asset touched: i18n v59 + style v50 asserted on BOTH sides.
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
success = (ROOT / "success.html").read_text(encoding="utf-8")
web3 = (ROOT / "web3.html").read_text(encoding="utf-8")
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

# --- SHIP 1: payment-ID truncation (success.html) ---------------------------------------
ok("var raw=params.get('payment_id')||'';" in success,
   "success.html: raw payment_id capture missing")
# NOTE: the file contains literal backslash-u JS escapes -> doubled backslash here
ok("var pid=raw ? (raw.length>24 ? raw.slice(0,12)+'\\u2026'+raw.slice(-8) : raw) : '\\u2014';" in success,
   "success.html: truncation expression drifted")
ok("if(raw)document.getElementById('successPaymentId').title=raw;" in success,
   "success.html: full-value tooltip missing")
ok("if(payChip&&raw){payChip.setAttribute('data-copy',raw);payChip.hidden=false;}" in success,
   "success.html: copy chip wiring churned (must use raw, full value)")
ok("r102: long payment IDs" in success, "success.html: r102 comment churned")
# r91 fallback + r77 engine wiring must survive
ok("overflow-wrap:anywhere" in success, "success.html: r91 anywhere fallback churned")
ok("document.getElementById('successPaymentId').textContent=pid;" in success,
   "success.html: single textContent write missing")
# semantic check of the same expression in Python (13..25 char boundary samples)
def trunc(raw):
    return raw if len(raw) <= 24 else raw[:12] + "\u2026" + raw[-8:]
ok(trunc("a" * 24) == "a" * 24, "r102 logic: 24-char must NOT truncate")
ok(len(trunc("a" * 25)) == 21, "r102 logic: 25-char must truncate to 21")
ok(len(trunc("b" * 113)) == 21, "r102 logic: 113-char -> 21")
ok(trunc("c" * 25)[-8:] == "c" * 8, "r102 logic: suffix window wrong")

# --- SHIP 2: web3 noindex + sitemap removal ---------------------------------------------
ok('<meta name="robots" content="noindex"/>' in web3,
   "web3.html: noindex meta missing")
ok("r102: this page is a 1.5s auto-redirect bridge" in web3,
   "web3.html: r102 comment churned")
ok('rel="canonical" href="https://nullvpn.net/web3.html"' in web3,
   "web3.html: canonical churned")
ok(sitemap.count("web3.html") == 0, "sitemap.xml: web3 entry still present")
ok(sitemap.count("<url>") == 11, "sitemap.xml: url count != 11 (expected 12->11)")
ok(sitemap.count("success.html") == 0, "sitemap.xml: success must never be listed")

# --- carried-forward chain (r101 ships) ---------------------------------------------------
ok('<div class="checkout-plans" role="group" data-i18n-aria="price.h" aria-label="Pricing">' in pricing,
   "pricing.html: checkout-plans group markup missing")
ok(pricing.count('data-plan="') == 3, "pricing.html: data-plan chips x!=3")
ok(pricing.count('aria-pressed="true"') == 1 and pricing.count('aria-pressed="false"') == 2,
   "pricing.html: aria-pressed initial state wrong")
ok("function updatePlan(plan){" in pricing, "pricing.html: updatePlan missing")
ok("var b=e.target.closest('.checkout-plan');" in pricing and
   "if(b)updatePlan(b.getAttribute('data-plan'));" in pricing,
   "pricing.html: delegated chip listener missing")
ok("max-height:calc(100vh - 32px);overflow-y:auto;overscroll-behavior:contain;" in pricing,
   "pricing.html: modal scroll-escape missing")
ok("border:1px solid var(--border-strong,#64748b);cursor:pointer; /* r101: chip boundary 1.4.11 */" in pricing,
   "pricing.html: chip boundary comment/decl churned")
ok(".checkout-close{transition:none}.checkout-plan{transition:none}}" in pricing,
   "pricing.html: reduced-motion chip gate missing")
ok("border:1px solid var(--border-strong,#64748b);border-radius:16px; /* r98: dialog boundary 1.4.11 */" in pricing,
   "pricing.html: r98 modal boundary churned")

# --- carried-forward chain (r44-r100 highlights) ------------------------------------------
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
    print("check_r102: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r102: ALL GREEN ({len(PAGES)} pages, no-asset-bump round)")
