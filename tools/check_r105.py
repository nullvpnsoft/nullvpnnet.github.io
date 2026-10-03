#!/usr/bin/env python3
"""r105 guards: SOON-pill a11y + RTL gap fix; 404 FAQ-search recovery form.

SHIP 1 (style.css, a11y + styling details): the .feat-card--wide h3::after
"SOON" pill is CSS generated content, which joins the accessible name —
screen readers heard "Ad Guard coming soon SOON" (the h3 text already says
"coming soon"). The alternative-text syntax (content: "SOON" / "") marks it
decorative for AT, behind @supports so engines without the syntax keep the
visible pill. Companion RTL detail: the pill's margin-left became
margin-inline-start (in RTL the ::after sits at line-end and needs its gap
on the inline-start side — with margin-left the pill hugged the text).

SHIP 2 (404.html, feature): FAQ-search recovery — a plain GET form
(role=search, action=/faq.html, name=q) that lands on the verified faq.html
?q= boot contract (r96 shareable filter, r100 pristine reset). Zero JS:
works with forms-native submit; i18n via two new keys nf.search.ph /
nf.search.go (x7 locales; ph doubles as the input's aria-label through
data-i18n-aria). Styling mirrors the faq-filter input: border-strong
functional boundary (r98 taxonomy), accent focus ring, 16px font (iOS
focus-zoom guard), 44px touch floor (r72); the submit reuses .btn-primary
(font already set, r53 wrap-safe).

style.css + i18n.js changed -> v53 / v60 buster; sw.js untouched (r103's
v4/reload asserted carried).
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
sw = (ROOT / "sw.js").read_text(encoding="utf-8")
nf404 = (ROOT / "404.html").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
offline = (ROOT / "offline.html").read_text(encoding="utf-8")
success = (ROOT / "success.html").read_text(encoding="utf-8")
web3 = (ROOT / "web3.html").read_text(encoding="utf-8")
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
faq = (ROOT / "faq.html").read_text(encoding="utf-8")

# --- SHIP 1: SOON pill decorative + RTL margin --------------------------------------------
ok('.feat-card--wide h3::after {\n  content: "SOON";' in css,
   "style.css: SOON pill rule drifted")
ok("@supports (content: \"x\" / \"\") {" in css, "style.css: r105 @supports gate missing")
ok("  .feat-card--wide h3::after { content: \"SOON\" / \"\"; }" in css,
   "style.css: r105 decorative SOON decl missing")
ok("margin-inline-start: 10px;" in css, "style.css: r105 RTL margin-inline-start missing")
ok(css.count("margin-left: 10px;") == 0, "style.css: r105 margin-left residue")
ok(css.count("@supports (content:") == 1, "style.css: unexpected extra @supports content block")

# --- SHIP 2: 404 FAQ-search recovery form ---------------------------------------------------
ok('<form class="nf-search" role="search" action="/faq.html" method="get">' in nf404,
   "404.html: r105 form element drifted")
ok('name="q" maxlength="80" autocomplete="off" spellcheck="false" autocapitalize="off" enterkeyhint="search"' in nf404,
   "404.html: r105 input attribute set drifted")
ok('data-i18n="nf.search.ph" placeholder="Search the FAQ…" data-i18n-aria="nf.search.ph" aria-label="Search the FAQ…"' in nf404,
   "404.html: r105 input i18n wiring drifted")
ok('<button type="submit" class="btn-primary" data-i18n="nf.search.go">Search</button>' in nf404,
   "404.html: r105 submit button drifted")
ok(".nf-search input {" in nf404 and "border: 1px solid var(--border-strong); border-radius: 10px; /* r98: input boundary 1.4.11 */" in nf404,
   "404.html: r105 input boundary language drifted")
ok("font-size: 16px; font-family: var(--font); caret-color: var(--accent-text);" in nf404,
   "404.html: r105 iOS zoom guard / caret drifted")
ok(".nf-search .btn-primary { min-height: 44px; display: inline-flex; align-items: center; }" in nf404,
   "404.html: r105 touch floor drifted")
# keys: presence + 7 locales each (key block opens, then all six non-EN locale lines inside)
for key in ("nf.search.ph", "nf.search.go"):
    i = i18.index(f'"{key}": {{')
    block = i18[i:i18.index("},", i)]
    for loc in ("ru:", "fa:", "ar:", "es:", "ne:", "fr:"):
        ok(loc in block, f"i18n.js: {key} missing locale {loc}")
ok(i18.count('"nf.search.ph": {') == 1 and i18.count('"nf.search.go": {') == 1,
   "i18n.js: r105 key duplication")
# usage counts on 404: placeholder + aria (same key twice) + submit
ok(nf404.count('data-i18n="nf.search.ph"') == 1, "404.html: nf.search.ph usage != 1")
ok(nf404.count('data-i18n-aria="nf.search.ph"') == 1, "404.html: nf.search.ph aria usage != 1")
ok(nf404.count('data-i18n="nf.search.go"') == 1, "404.html: nf.search.go usage != 1")

# --- carried-forward chain (r104) -----------------------------------------------------------
ok("html { scrollbar-width: thin; scrollbar-color: var(--border) transparent; scrollbar-gutter: stable; }" in css,
   "style.css: r104 html gutter rule drifted")
ok("r104: scrollbar-gutter: stable" in css, "style.css: r104 comment churned")
total_mailto = 0
bare = 0
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    total_mailto += t.count('href="mailto:support@nullvpn.net?subject=NullVPN%20Support"')
    bare += t.count('href="mailto:support@nullvpn.net"')
ok(total_mailto == 13, f"mailto subject count {total_mailto} != 13  [r128: -3 legal-nav legacy mailtos -> standard 6-link nav]")
ok(bare == 0, f"bare mailto residue {bare} != 0")
ok('href="mailto:support@nullvpn.net?subject=NullVPN%20Support"' in (ROOT / "contact.html").read_text(encoding="utf-8"),
   "contact.html: subject prefill missing on the triage-critical page")

# --- carried-forward chain (r103) ----------------------------------------------------------
ok("const CACHE = 'nullvpn-v4';" in sw, "sw.js: CACHE v4 churned")
ok("fetch(req, { cache: 'reload' })" in sw, "sw.js: r103 reload fetch churned")
ok(sw.index("if (isNav)") < sw.index("cache: 'reload'"), "sw.js: reload outside isNav branch")
ok("clean.search = '';" in sw and "clean.hash = '';" in sw, "sw.js: r97 pathname put churned")
ok("caches.match(req, { ignoreSearch: true })" in sw, "sw.js: r97 normalization churned")
ok("if (resp.ok && resp.type === 'basic') {" in sw, "sw.js: r70 ok-only guard churned")
ok("(?:style\\.css|i18n\\.js|branding\\.js)\\?v=\\d+" in sw, "sw.js: r45 discovery regex churned")
ok("fetch('/', { cache: 'no-store' })" in sw, "sw.js: precache no-store churned")
ok(".tbl-scroll { overflow-x: auto; margin: 14px 0 20px; border: 1px solid var(--border); border-radius: 12px; -webkit-overflow-scrolling: touch; scrollbar-width: thin; /* r103: match the page's thin themed scrollbar (width doesn't inherit) */ }" in css,
   "style.css: r103 tbl-scroll line drifted")
ok("max-height:calc(100vh - 32px);overflow-y:auto;overscroll-behavior:contain;scrollbar-width:thin;scrollbar-gutter:stable;" in pricing,
   "pricing.html: r103 modal scrollbar decl missing")

# --- carried-forward chain (r102) ----------------------------------------------------------
ok("var raw=params.get('payment_id')||'';" in success, "success.html: raw capture missing")
ok("var pid=raw ? (raw.length>24 ? raw.slice(0,12)+'\\u2026'+raw.slice(-8) : raw) : '\\u2014';" in success,
   "success.html: truncation expression drifted")
ok("if(raw)document.getElementById('successPaymentId').title=raw;" in success,
   "success.html: full-value tooltip missing")
ok('<meta name="robots" content="noindex"/>' in web3, "web3.html: noindex missing")
ok(sitemap.count("web3.html") == 0, "sitemap.xml: web3 entry still present")
ok(sitemap.count("<url>") == 11, "sitemap.xml: url count != 11")

# --- carried-forward chain (r101) ----------------------------------------------------------
ok('<div class="checkout-plans" role="group" data-i18n-aria="price.h" aria-label="Pricing">' in pricing,
   "pricing.html: checkout-plans group markup missing")
ok(pricing.count('data-plan="') == 3, "pricing.html: data-plan chips x!=3")
ok(pricing.count('aria-pressed="true"') == 1 and pricing.count('aria-pressed="false"') == 2,
   "pricing.html: aria-pressed initial state wrong")
ok("function updatePlan(plan){" in pricing, "pricing.html: updatePlan missing")
ok("border:1px solid var(--border-strong,#64748b);cursor:pointer; /* r101: chip boundary 1.4.11 */" in pricing,
   "pricing.html: chip boundary comment/decl churned")
ok(".checkout-close{transition:none}.checkout-plan{transition:none}}" in pricing,
   "pricing.html: reduced-motion chip gate missing")
ok("border:1px solid var(--border-strong,#64748b);border-radius:16px; /* r98: dialog boundary 1.4.11 */" in pricing,
   "pricing.html: r98 modal boundary churned")

# --- carried-forward chain (r44-r100) ------------------------------------------------------
ok("let lastFilterLang = null; // r100: boot guard" in i18, "i18n.js: r100 boot guard churned")
ok("const langChanged = lastFilterLang !== null && lastFilterLang !== lang;" in i18,
   "i18n.js: r100 langChanged guard churned")
ok("statusEl.textContent = t('faq.filter.cleared', lang);" in i18, "i18n.js: r100 cleared write churned")
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
ok("fetch('/', { method: 'HEAD', cache: 'no-store' })" in i18, "i18n.js: r97 probe churned")
ok("if (e.key !== 'Escape' || !faqFilter.value) return;" in i18, "i18n.js: r95 Escape churned")
ok("behavior: reduce ? 'auto' : 'smooth', block: 'center'" in i18, "i18n.js: r95 motion gate churned")
ok("@media print { .faq-filter { display: none !important; } }" in css, "style.css: r95 print-hide churned")
ok("if (q) u.searchParams.set('q', q);" in i18, "i18n.js: r96 q sync churned")
ok('maxlength="80"' in faq, "faq.html: r96 maxlength churned")
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

# --- versions (v53/i60 post; v52/i59 residue zero) ----------------------------------------
want_i, want_s = "i18n.js?v=60", "style.css?v=53"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")
    ok(t.count("style.css?v=52") == 0, f"{page}: stale v52 pin residue")
    ok(t.count("i18n.js?v=59") == 0, f"{page}: stale i59 pin residue")
ok("color-scheme: light;" in css and "color-scheme: dark;" in css,
   "style.css: color-scheme theme props churned")

if errs:
    print("check_r105: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r105: ALL GREEN ({len(PAGES)} pages)")
