#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
#!/usr/bin/env python3
"""r127 guards: dead-key orphan detector (T-table reverse scan, pinned).

(Carries the full r44-r126 chain, regenerated from check_r126.py; the r126
success-card hide, r125 refund callout, r124 telegram-rescue, r123
HUD-context, r122 download-hero hide, r121 locale-bootstrap contract,
r118-r120 value-quality gates all remain in force.)

SHIP (tooling gate for the r125 defect class): scripts/deadkey_scan.py
settle the TRUE dead set — T keys translated x7 but used by NO surface —
by boundary-safe full-name matching of all 466 keys against every HTML
data-i18n attr + every tools/*.js + sw.js + branding.js literal + engine
t() calls. Result: 55 dead keys (r119 documented only 7; the rest are
superseded vocabularies — price.f1-f9/btn.*/monthly/quarterly/annual,
index.prob1-4/trust1-4/h1b/sub, faq.section.*, priv.q6/a6, comp.row.*,
comp.val.*, nav.whynull, refund.more, price.pay.h/p2 etc). Verified: 4
spot-greps + no dynamic key concatenation exists in the engine (t() calls
are full literals). PRUNING stays declined (r119 standing: churn; dead
keys are translated future-proofing). Instead the set is PINNED: any
future edit that orphans a live key (the silent r125 regression — element
removed, last usage of translated content lost) grows the set and FAILS
the gate; reviving a dead key also fails (deliberate changes refresh the
list). Sentinel live asserts guard the scanner itself.

QA this round: es full 15-page sweep — the LAST locale gap — 14/15
CLS 0.000-0.003, LCP 176-416ms (web3 = known bridge artifact): the
7-locale full-cycle perf matrix is now genuinely complete. download.html
re-lens (r122 surface) CLEAN: r122 hide rule live in CSSOM, fa CTA
reveals Persian labels, RELEASE_META dormant, #dl-install present.
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
feat = (ROOT / "features.html").read_text(encoding="utf-8")
deploy_sh = (ROOT / "tools" / "deploy_historyless.sh").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
offline = (ROOT / "offline.html").read_text(encoding="utf-8")
success = (ROOT / "success.html").read_text(encoding="utf-8")
web3 = (ROOT / "web3.html").read_text(encoding="utf-8")
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
faq = (ROOT / "faq.html").read_text(encoding="utf-8")

# --- SHIP 1: deploy-time lastmod stamping ---------------------------------------------------
ok("echo \"[0/5] stamping sitemap lastmod\"" in deploy_sh, "deploy script: stamp step missing")
ok('sed -i.bak "s|<lastmod>[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]</lastmod>|<lastmod>${TODAY}</lastmod>|g" sitemap.xml' in deploy_sh,
   "deploy script: stamp sed drifted")
ok('TODAY="$(TZ=Asia/Shanghai date +%F 2>/dev/null)"' in deploy_sh, "deploy script: TZ date drift")
ok("[ -n \"$TODAY\" ] || TODAY=\"$(date +%F)\"" in deploy_sh, "deploy script: date fallback drift")
ok(deploy_sh.index("[0/5] stamping sitemap lastmod") < deploy_sh.index("[1/5] staging working tree"),
   "deploy script: stamp must run BEFORE staging")
ok(deploy_sh.index("if [ -f sitemap.xml ]; then") < deploy_sh.index("[1/5] staging working tree"),
   "deploy script: stamp guard drift")
ok("&& rm -f sitemap.xml.bak || true" in deploy_sh, "deploy script: non-fatal cleanup drift")
ok(sitemap.count("<url>") == 11, "sitemap.xml: url count != 11")
ok(sitemap.count("<lastmod>") == 11, "sitemap.xml: lastmod count != 11")

# --- SHIP 2: orphans/widows rag control ------------------------------------------------------
ok("p, li, dd, dt, figcaption { orphans: 3; widows: 3; }" in css,
   "style.css: r106 orphans/widows rule drifted")
ok("/* r106: rag control" in css, "style.css: r106 comment churned")

# --- SHIP 3: features.html scrollbar consistency ---------------------------------------------
ok(".feat-table-wrap { overflow-x: auto; margin-top: 32px; scrollbar-width: thin; scrollbar-color: var(--border) transparent; -webkit-overflow-scrolling: touch; }" in feat,
   "features.html: r106 thin-scrollbar decl drifted")
ok("/* r106: match the page's thin themed scrollbar" in feat, "features.html: r106 comment churned")

# --- carried-forward chain (r105) -----------------------------------------------------------
ok('.feat-card--wide h3::after {\n  content: "SOON";' in css,
   "style.css: SOON pill rule drifted")
ok("@supports (content: \"x\" / \"\") {" in css, "style.css: r105 @supports gate missing")
ok("  .feat-card--wide h3::after { content: \"SOON\" / \"\"; }" in css,
   "style.css: r105 decorative SOON decl missing")
ok("margin-inline-start: 10px;" in css, "style.css: r105 RTL margin-inline-start missing")
ok(css.count("margin-left: 10px;") == 0, "style.css: r105 margin-left residue")
ok(css.count("@supports (content:") == 1, "style.css: unexpected extra @supports content block")
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
for key in ("nf.search.ph", "nf.search.go"):
    i = i18.index(f'"{key}": {{')
    block = i18[i:i18.index("},", i)]
    for loc in ("ru:", "fa:", "ar:", "es:", "ne:", "fr:"):
        ok(loc in block, f"i18n.js: {key} missing locale {loc}")
ok(i18.count('"nf.search.ph": {') == 1 and i18.count('"nf.search.go": {') == 1,
   "i18n.js: r105 key duplication")
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

# r59/r90 living prefers-contrast math (carry-forward, values asserted in comments)
i = css.index("@media (prefers-contrast: more) {")
pc = css[i:css.index("}", css.index("[data-theme=\"dark\"] { --text2:", i))]
ok("--text2: #55482e" in pc and "--border: #8f7448" in pc, "style.css: r59 light contrast lift churned")
ok("--text2: #c3cedd" in pc and "--border: #64789a" in pc, "style.css: r90 dark contrast lift churned")

# --- SHIP 1: OG/Twitter image enrichment (x15) ----------------------------------------------
OG_ALT = "NullVPN — private connectivity for difficult networks. Brand cover with gold wave lines on dark navy."
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count('<meta property="og:image" content="https://nullvpn.net/og-cover.jpg"/>') == 1,
       f"{page}: og:image anchor drifted")
    ok(t.count('<meta property="og:image:width" content="1200"/>') == 1, f"{page}: og:image:width missing")
    ok(t.count('<meta property="og:image:height" content="630"/>') == 1, f"{page}: og:image:height missing")
    ok(t.count(f'<meta property="og:image:alt" content="{OG_ALT}"/>') == 1, f"{page}: og:image:alt missing")
    ok(t.count(f'<meta name="twitter:image:alt" content="{OG_ALT}"/>') == 1, f"{page}: twitter:image:alt missing")
ok((ROOT / "og-cover.jpg").exists(), "og-cover.jpg missing")

# --- SHIP 2: checkout-plan press feedback ----------------------------------------------------
ok("transition:background .15s ease,color .15s ease,border-color .15s ease,transform .12s ease /* r107: transform joins so the press scales */" in pricing,
   "pricing.html: r107 chip transition drifted")
ok(".checkout-plan:active { transform: scale(.95); }" in pricing,
   "pricing.html: r107 chip press rule missing")
ok("/* r107: press feedback" in pricing, "pricing.html: r107 press comment missing")
ok(pricing.count(".checkout-plan:active") == 1, "pricing.html: chip :active x!=1")

# --- r112 ship asserts (download.html release-grid i18n correctness) ---------------------------
_dl = (ROOT / "download.html").read_text(encoding="utf-8")
ok(_dl.count("var MIN_ANDROID_RE = ") == 1, "download.html: MIN_ANDROID_RE missing")
ok(_dl.count("minimum\\s+android") == 1, "download.html: MIN_ANDROID_RE body churned")
ok(_dl.count("window.__lastRelease = rel;") == 1, "download.html: __lastRelease cache missing")
ok(_dl.count("window.RERENDER_RELEASE_META = function () {") == 1,
   "download.html: re-render hook missing")
ok(_dl.count("if (window.__lastRelease) applyRelease(window.__lastRelease);") == 1,
   "download.html: hook live-release branch missing")
ok(_dl.count("else if (window.RELEASE_META) renderStatic(window.RELEASE_META);") == 1,
   "download.html: hook static branch missing")
ok(_dl.count("[L('minandroid', 'Minimum Android'), minA || '—'],") == 1,
   "download.html: applyRelease minAndroid row missing")
ok(_dl.count("apk ? L('stable', 'Stable') : '—'") == 1,
   "download.html: status value not localized")
ok(_dl.count("r112: language-switch re-render") == 1, "download.html: r112 hook comment missing")
ok(_dl.count("r112: minimum-Android line") == 1, "download.html: r112 regex comment missing")
ok(_dl.count("apk ? 'Stable' : ") == 0, "download.html: stale hardcoded EN status residue")

_i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok(_i18n.count('"dl.meta.stable"') == 1, "i18n.js: dl.meta.stable key missing")
for _loc in ["en", "ru", "fa", "ar", "es", "ne", "fr"]:
    _seg = _i18n[_i18n.find('"dl.meta.stable"'):_i18n.find('"dl.meta.stable"') + 220]
    ok(_seg.count(_loc + ":") >= 1, "i18n.js: dl.meta.stable missing locale " + _loc)
ok(_i18n.count("stable: t('dl.meta.stable', lang),") == 1,
   "i18n.js: DL_META_I18N stable entry missing")
ok(_i18n.count("window.RERENDER_RELEASE_META === 'function'") == 1,
   "i18n.js: re-render hook call missing")
ok(_i18n.count("r112: labels follow the language immediately") == 1,
   "i18n.js: r112 comment missing")


# --- r113 ship asserts (.checkout-overlay print hygiene) ---------------------------------------
_css_r113 = (ROOT / "style.css").read_text(encoding="utf-8")
ok(_css_r113.count(".checkout-overlay") == 1, "style.css: .checkout-overlay token x!=1")
_mp = _css_r113.index("@media print")
_mcab = _css_r113.index("CABINET DESIGN ALIGNMENT")
ok(_css_r113.count(".checkout-overlay", _mp, _mcab) == 1,
   "style.css: .checkout-overlay not inside the master print block")
ok(_css_r113.count(".copy-text-chip,") == 1, "style.css: r113 list-split churned")
ok(_css_r113.count("r113: the checkout dialog is fixed-position") == 1,
   "style.css: r113 comment missing")
ok(_css_r113.count(".checkout-overlay { display: none !important; }") == 1,
   "style.css: r113 hide declaration churned")
_pricing_r113 = (ROOT / "pricing.html").read_text(encoding="utf-8")
ok(_pricing_r113.count('id="checkoutModal" class="checkout-overlay"') == 1,
   "pricing.html: overlay markup churned")


# --- r114 ship asserts (estate a11y structure: headings + link purpose) ------------------------
import re as _re
_H = _re.compile(r'<h([1-6])[\s>]', _re.I)
_A = _re.compile(r'<a\b[^>]*>(.*?)</a>', _re.S | _re.I)
for _page in PAGES:
    _t = (ROOT / _page).read_text(encoding="utf-8")
    _b = _t[_t.index("<body"):] if "<body" in _t else _t
    _lv = [int(_m.group(1)) for _m in _H.finditer(_b)]
    ok(_lv.count(1) == 1, _page + ": h1 count x!=1")
    for _m in _H.finditer(_b):
        _open_end = _b.index(">", _m.start())
        _tag = "</h" + _m.group(1)
        _close = _b.lower().index(_tag, _open_end)
        _inner = _b[_open_end + 1:_close]
        _txt = _re.sub(r"<[^>]+>", "", _inner).strip()
        ok(_txt or "data-i18n" in _inner, _page + ": empty heading near " + str(_m.start()))
    for _m in _A.finditer(_b):
        _attrs, _inner = _m.group(0), _m.group(1)
        _txt = _re.sub(r"<[^>]+>", "", _inner).strip()
        if _txt:
            continue
        _named = ("aria-label=" in _attrs or "data-i18n" in _attrs
                  or _re.search(r'<img[^>]*alt="[^"]+"', _inner, _re.I))
        ok(_named, _page + ": unnamed link near " + str(_m.start()))


# --- r115 ship asserts (heading-id anchor clearance) --------------------------------------------
_css_r115 = (ROOT / "style.css").read_text(encoding="utf-8")
ok(_css_r115.count("h1[id], h2[id], h3[id], h4[id], h5[id], h6[id] { scroll-margin-top") == 1,
   "style.css: r115 heading-id selector missing")
ok(_css_r115.count("calc(var(--nav-h, 120px) + 50px); }") >= 1,
   "style.css: anchor-offset formula churned")
ok(_css_r115.count("r115: heading ids join the formula") == 1,
   "style.css: r115 comment missing")
ok(_css_r115.count("the exact signature the r84 note recorded for tr/th") == 1,
   "style.css: r115 provenance comment truncated")
_hiw_r115 = (ROOT / "how-it-works.html").read_text(encoding="utf-8")
for _slug in ["built-for-difficult-networks", "connection-experience", "three-steps",
              "install-the-app", "tap-connect", "pay-when-ready", "ready-to-connect"]:
    ok(_hiw_r115.count("<h2 id=\"" + _slug + "\"") == 1,
       "how-it-works.html: r115 h2 slug churned: " + _slug)


# --- r116 ship asserts (offline fixed-toast print hygiene) --------------------------------------
_off = (ROOT / "offline.html").read_text(encoding="utf-8")
ok(_off.count("@media print { .of-live { display: none !important; } }") == 1,
   "offline.html: r116 print rule missing")
ok(_off.count("r116: print hygiene") == 1, "offline.html: r116 comment missing")
ok(_off.count(".of-live {") >= 2, "offline.html: of-live base rule churned")


# --- r117 ship asserts (theme-system contract) --------------------------------------------------
_THEMA_NO_BTNS = ["404.html", "offline.html"]  # deliberate: minimal chrome, init only
for _page in PAGES:
    _t = (ROOT / _page).read_text(encoding="utf-8")
    ok(_t.count("localStorage.getItem('theme')") == 1,
       _page + ": theme init missing or duplicated")
    if _page in _THEMA_NO_BTNS:
        ok(_t.count("function setTheme(") == 0, _page + ": setTheme defined on buttonless page")
        ok(_t.count("onclick=\"setTheme(") == 0, _page + ": theme button on buttonless page")
    else:
        ok(_t.count("function setTheme(") == 1, _page + ": inline setTheme missing")
        ok(_t.count("onclick=\"setTheme('light')\"") == 1, _page + ": light button unwired")
        ok(_t.count("onclick=\"setTheme('dark')\"") == 1, _page + ": dark button unwired")
_i18n_r117 = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok(_i18n_r117.count("theme-anim") >= 1, "i18n.js: r43 theme-anim arming missing")


# --- r118 ship asserts (locale-value quality gate + contract source pins) -----------------------
import unicodedata as _uni

def _script_chars(s):
    has = set()
    for ch in s:
        name = _uni.name(ch, "")
        if "DEVANAGARI" in name: has.add("deva")
        elif "CYRILLIC" in name: has.add("cyrl")
        elif "ARABIC" in name: has.add("arab")
    return has

_LOCS = ["en", "ru", "fa", "ar", "es", "ne", "fr"]
_NATIVE = {"ru": "cyrl", "fa": "arab", "ar": "arab", "ne": "deva"}
_FOREIGN = {"en": {"cyrl", "deva", "arab"}, "es": {"cyrl", "deva", "arab"}, "fr": {"cyrl", "deva", "arab"},
            "ru": {"deva"}, "fa": {"cyrl", "deva"}, "ar": {"cyrl", "deva"}, "ne": {"cyrl"}}

def _parse_T(text):
    """Parse the T table: key -> {locale: value}. String-aware brace scanner —
    a naive [^{}]* body regex silently drops keys whose values contain {year}."""
    start = text.find("const T = {")
    if start == -1:
        return {}
    i = text.find("{", start)
    n = len(text)
    j, depth, in_str, esc = i + 1, 1, False, False
    while j < n and depth > 0:
        c = text[j]
        if in_str:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': in_str = False
        else:
            if c == '"': in_str = True
            elif c == "{": depth += 1
            elif c == "}": depth -= 1
        j += 1
    t_src = text[i + 1:j - 1]
    import re as _re
    key_re = _re.compile(r'"([a-z0-9_.\-]+)"\s*:\s*\{')
    val_re = _re.compile(r'\b(en|ru|fa|ar|es|ne|fr)\s*:\s*"((?:[^"\\]|\\.)*)"')
    table, k, tn = {}, 0, len(t_src)
    while k < tn:
        m = key_re.search(t_src, k)
        if not m:
            break
        key = m.group(1)
        b, depth, in_str, esc = m.end(), 1, False, False
        while b < tn and depth > 0:
            c = t_src[b]
            if in_str:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == '"': in_str = False
            else:
                if c == '"': in_str = True
                elif c == "{": depth += 1
                elif c == "}": depth -= 1
            b += 1
        entry = {}
        for vm in val_re.finditer(t_src[m.end():b - 1]):
            entry[vm.group(1)] = vm.group(2).replace('\\"', '"').replace("\\n", "\n")
        if len(entry) >= 5:
            table[key] = entry
        k = b
    return table

_T = _parse_T((ROOT / "i18n.js").read_text(encoding="utf-8"))
ok(len(_T) >= 450, f"i18n.js: T parse collapsed (got {len(_T)} keys, expected ~466)")

# 1) {year} parity + 2) no empty values
_year_fail = [(k, l) for k, e in _T.items() if "{year}" in e.get("en", "")
              for l in _LOCS if l != "en" and "{year}" not in e.get(l, "")]
ok(not _year_fail, "i18n.js: {year} parity broken: " + repr(_year_fail[:4]))
_empty = [(k, l) for k, e in _T.items() for l, v in e.items() if not v.strip()]
ok(not _empty, "i18n.js: empty locale values: " + repr(_empty[:4]))

# 3) native-script presence (>= 12 chars) with exact pinned brand allowlist
_R118_LOCS = ("ru", "fa", "ar", "ne")
_R118_BRAND_ALLOW = set()
for _bk in ("comp.table.expressvpn", "comp.table.nordvpn",
            "comp.table.protonvpn"):
    for _bl in _R118_LOCS:
        _R118_BRAND_ALLOW.add((_bk, _bl))          # 12: comparison VPN brand names, Latin by design (r132: comp.table.nullvpn pruned)
for _bk, _bls in (("comp.val.lightway", ("ar", "fa", "ru")),
                  ("comp.val.stealth", ("ar", "fa", "ru")),
                  ("comp.val.telegramweb3", ("ar", "ne", "ru")),
                  ("contact.web3.h", ("ar", "fa", "ne", "ru")),
                  ("how.nullvpn.h", ("ar", "fa", "ne", "ru"))):
    for _bl in _bls:
        _R118_BRAND_ALLOW.add((_bk, _bl))          # 13: protocol labels + TON heading, Latin by design
_R118_BRAND_ALLOW.add(("price.p3.amount", "ru"))   # 1 000 ₽ — currency format, no Cyrillic by design
_R118_BRAND_ALLOW.add(("price.p4.amount", "ru"))   # 3 500 ₽
# 31 (key, locale) pairs total (r132: -4 comp.table.nullvpn pairs) — r118-audited clean state; the gate itself
# surfaced the fa/ar pairs (the audit lens skipped no-native checks for
# Arabic-script locales) and price amounts. Drift either way = conscious edit.
_no_native = []
for _k, _e in _T.items():
    for _l, _need in _NATIVE.items():
        _v = _e.get(_l, "")
        if len(_v) >= 6 and _need not in _script_chars(_v) and (_k, _l) not in _R118_BRAND_ALLOW:
            _no_native.append((_k, _l))
ok(not _no_native, "i18n.js: native-script missing (untranslated or brand beyond allowlist): " + repr(_no_native[:4]))
_allow_drift = set()
for _k, _e in _T.items():
    for _l in _NATIVE:
        _v = _e.get(_l, "")
        if len(_v) >= 6 and _NATIVE[_l] not in _script_chars(_v):
            _allow_drift.add((_k, _l))
ok(_allow_drift == _R118_BRAND_ALLOW,
   f"i18n.js: brand allowlist drifted (got {len(_allow_drift)} pairs: {sorted(_allow_drift)[:6]}..., expected 31 pinned pairs)")

# 4) foreign-script leaks: zero tolerance
_leaks = []
for _k, _e in _T.items():
    for _l, _bad in _FOREIGN.items():
        _v = _e.get(_l, "")
        if _script_chars(_v) & _bad:
            _leaks.append((_k, _l))
ok(not _leaks, "i18n.js: foreign-script leaks: " + repr(_leaks[:4]))

# 5) untranslated sentinel: es/ne identical to en (>= 24 chars) == pinned set
_R118_IDENTICAL_OK = {("contact.sup.tg.btn", "es")}  # brand handle button, by design
_identical = {(k, l) for k, e in _T.items() for l in ("es", "ne")
              if e.get(l, "") == e.get("en", "") and len(e.get("en", "")) >= 24}
ok(_identical == _R118_IDENTICAL_OK,
   f"i18n.js: es/ne == en sentinel drifted (got {sorted(_identical)})")

# 6a) i18n.js r64 chrome-sync source pins (byte `in` — file bytes are ground truth)
_i18n_r118 = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok('meta[name="theme-color"]:not([media])' in _i18n_r118,
   "i18n.js: r64 chrome-sync selector missing")
ok('meta[name="theme-color"][media]' in _i18n_r118,
   "i18n.js: r64 [media]-collapse selector missing")
ok("Browser-chrome theme sync (r64)" in _i18n_r118, "i18n.js: r64 block comment missing")
ok("Live OS-theme follow (r99)" in _i18n_r118, "i18n.js: r99 OS-follow block missing")

# 6b) style.css r104 scrollbar-gutter html rule (checkout scroll-lock shift guard)
css_r118 = (ROOT / "style.css").read_text(encoding="utf-8")
ok(css_r118.count("html { scrollbar-width: thin; scrollbar-color: var(--border) transparent; scrollbar-gutter: stable; }") == 1,
   "style.css: r104 scrollbar-gutter html rule churned")
ok("r104: scrollbar-gutter: stable" in css_r118, "style.css: r104 comment missing")

# 6c) per-page no-JS fallback meta contract
for _page in PAGES:
    _t = (ROOT / _page).read_text(encoding="utf-8")
    ok(_t.count('<meta name="theme-color" content="#f7e7ce"/>') == 1,
       _page + ": static light theme-color meta missing")
    ok(_t.count('<meta name="theme-color" content="#0a0f1a" media="(prefers-color-scheme: dark)"/>') == 1,
       _page + ": static dark media theme-color meta missing")
    ok(_t.count('<meta name="color-scheme" content="light dark"') == 1,
       _page + ": color-scheme meta missing")


# --- r119 ship asserts (Latin-locale debt gate) --------------------------------------------------
import re as _re119

_norm119 = lambda s: _re119.sub(r"\s+", " ", (s or "")).strip().lower()

# 1) es==fr identity: zero tolerance (Latin-locale un-localized debt detector)
_ident_ef = sorted(k for k, e in _T.items()
                   if len(e.get("es", "")) >= 24 and e.get("es", "") == e.get("fr", ""))
ok(not _ident_ef, "i18n.js: es==fr identical (untranslated debt): " + repr(_ident_ef[:4]))

# 2) cross-key en paraphrase: a locale value equal to a DIFFERENT key's en value
_en_norms = {}
for _k, _e in _T.items():
    _en_norms.setdefault(_norm119(_e.get("en", "")), set()).add(_k)
_para = []
for _k, _e in _T.items():
    for _l in _LOCS[1:]:
        _v = _norm119(_e.get(_l, ""))
        if len(_v) >= 12:
            _others = sorted(o for o in _en_norms.get(_v, set()) if o != _k)
            if _others:
                _para.append((_k, _l, _others[0]))
ok(not _para, "i18n.js: value equals another key's en (borrowed paraphrase): " + repr(_para[:4]))


# --- r120 ship asserts (sibling-locale identity gates) -------------------------------------------
_norm120 = lambda s: _re119.sub(r"\s+", " ", (s or "")).strip()

# 1) fa==ar identity: zero tolerance (same-script un-localized debt detector)
_ident_fa_ar = sorted(k for k, e in _T.items()
                      if len(e.get("fa", "")) >= 12 and _norm120(e.get("fa", "")) == _norm120(e.get("ar", "")))
ok(not _ident_fa_ar, "i18n.js: fa==ar identical (untranslated debt): " + repr(_ident_fa_ar[:4]))

# 2) ru==ne identity: only the by-design shared Latin value may coincide
_ident_ru_ne = sorted(k for k, e in _T.items()
                      if len(e.get("ru", "")) >= 16 and _norm120(e.get("ru", "")) == _norm120(e.get("ne", "")))
ok(_ident_ru_ne == ["comp.val.telegramweb3"],
   f"i18n.js: ru==ne identity drifted (got {_ident_ru_ne}, expected [comp.val.telegramweb3])")


# --- r121 ship asserts (locale bootstrap + navbar reveal contract) --------------------------------
_BOOT_TAG = 'getItem("nullvpn_lang")'
_BOOT_DIR = '(l==="fa"||l==="ar")?"rtl":"ltr"'
_BOOT_CLS = 'classList.add("nv-l")'
_BOOT_SAFE = 'setTimeout(function(){document.documentElement.classList.remove("nv-l")},2000)'
_NVL_RULE = 'html.nv-l .nav-inner{visibility:hidden}'

for _page in PAGES:
    _t121 = (ROOT / _page).read_text(encoding="utf-8")
    ok(_BOOT_TAG in _t121, _page + ": r121 locale bootstrap missing (storage read)")
    ok(_BOOT_DIR in _t121, _page + ": r121 bootstrap dir ternary missing")
    ok(_BOOT_CLS in _t121, _page + ": r121 bootstrap nv-l class arm missing")
    ok(_BOOT_SAFE in _t121, _page + ": r121 bootstrap 2s failsafe missing")
    ok(_NVL_RULE in _t121, _page + ": r121 inline navbar hide rule missing")

# engine mirror pins — the bootstrap hardcodes the RTL set the engine owns;
# if RTL_LANGS ever changes, the bootstrap dir ternary must change in lockstep
ok("const RTL_LANGS = ['fa', 'ar'];" in i18,
   "i18n.js: RTL_LANGS churned — bootstrap dir ternary must be updated in lockstep")
ok("document.documentElement.classList.remove('nv-l')" in i18,
   "i18n.js: applyLang nv-l reveal line missing (navbar would stay hidden for non-EN)")
ok("updateFeatureTexts(lang);" in i18, "i18n.js: applyLang tail anchor churned")


# --- r122 ship asserts (download-hero nv-l hide) --------------------------------------------------
_dh = (ROOT / "download.html").read_text(encoding="utf-8")
ok('html.nv-l .nav-inner{visibility:hidden}html.nv-l .dh-cta,html.nv-l .dh-note{visibility:hidden}' in _dh,
   "download.html: r122 extended hero-hide rule missing (dh-cta/dh-note)")
for _p in PAGES:
    if _p == "download.html":
        continue
    _t122 = (ROOT / _p).read_text(encoding="utf-8")
    ok(_t122.count("html.nv-l .dh-cta") == 0,
       _p + ": download-only hero-hide rule leaked onto " + _p)


# --- r127 ship asserts (dead-key orphan detector, pinned set) --------------------------------------
import re as _re
_eng127 = (ROOT / "i18n.js").read_text(encoding="utf-8")
_k127 = _re.findall(r'(?:^|[\s,])(?:"([a-z0-9_.]+)"|([a-z0-9_.]+)):\s*\{', _eng127, _re.M)
_keys127 = sorted({a or b for a, b in _k127 if (a or b).count("_") >= 1 or "." in (a or b)})
_keys127 = [k for k in _keys127 if "." in k]
_corpus127 = ""
for _p in list(ROOT.glob("*.html")) + list((ROOT / "tools").glob("*.js")) + [ROOT / "sw.js", ROOT / "branding.js"]:
    if _p.exists():
        _corpus127 += _p.read_text(encoding="utf-8", errors="replace")
_dead127 = []
for _k in _keys127:
    _uses = len(_re.findall(_re.escape(_k) + r'(?![a-z0-9_.])', _corpus127))
    _defh = len(_re.findall(_re.escape(_k) + r'"\s*:\s*\{', _eng127)) + len(_re.findall(r'(?<![\w"])' + _re.escape(_k) + r'\s*:\s*\{', _eng127))
    _extra = len(_re.findall(_re.escape(_k) + r'(?![a-z0-9_])', _eng127)) - _defh
    if _uses == 0 and _extra <= 0:
        _dead127.append(_k)
# r132: the r127 pinned dead-set (55 keys) is fully pruned from T — expected
# dead set is now EMPTY; the recomputation below remains as the future-orphan
# tripwire (element removed without re-homing its i18n keys), and the r132
# section's _DEAD63 tripwire bans the pruned names outright. (The r127 pin's
# tech.*/nav.cta exclusions were detector substring collisions with
# how.tech.* — the conservative full-name r132 audit proved them dead too.)
_EXPECTED_DEAD = frozenset()
ok(set(_dead127) == _EXPECTED_DEAD,
   "dead-key set drifted: orphaned=" + ",".join(sorted(set(_dead127) - _EXPECTED_DEAD)) +
   " revived=" + ",".join(sorted(_EXPECTED_DEAD - set(_dead127))) +
   " (orphaned = element removed without re-homing its i18n keys; revived = refresh the pin)")
for _sent in ["nav.download", "share.btn", "price.refund.p", "faq.cat.all", "a11y.skip"]:
    ok(_sent not in _dead127, "sentinel live key misclassified dead: " + _sent)


# --- r126 ship asserts (success-card nv-l hide) ----------------------------------------------------
_sc = (ROOT / "success.html").read_text(encoding="utf-8")
ok(_sc.count('<style>html.nv-l .nav-inner{visibility:hidden}html.nv-l .success-card{visibility:hidden}</style>') == 1,
   "success.html: r126 extended card-hide rule missing (nav-inner + success-card)")
for _p in PAGES:
    if _p == "success.html":
        continue
    _t126 = (ROOT / _p).read_text(encoding="utf-8")
    ok(_t126.count("html.nv-l .success-card") == 0,
       _p + ": success-only card-hide rule leaked onto " + _p)


# --- r125 ship asserts (pricing refund callout restored) -------------------------------------------
_pc125 = (ROOT / "pricing.html").read_text(encoding="utf-8")
ok(_pc125.count('data-i18n="price.refund.h"') == 1,
   "pricing.html: price.refund.h not attached (orphaned key must be used exactly once)")
ok(_pc125.count('data-i18n="price.refund.p"') == 1,
   "pricing.html: price.refund.p not attached (orphaned key must be used exactly once)")
ok(_pc125.count("r125: refund assurance restored to the point of purchase") == 1,
   "pricing.html: r125 callout comment missing")
# the callout must be a .pricing-note block (same visual language as howpay)
ok('<div class="pricing-note">\n        <h3 data-i18n="price.refund.h">' in _pc125,
   "pricing.html: refund callout is not a .pricing-note block")


# --- r124 ship asserts (404 telegram rescue aliases) -----------------------------------------------
_nf124 = (ROOT / "404.html").read_text(encoding="utf-8")
for _row in ["['telegram',     '/contact.html',      'nav.contact']",
             "['channel',      '/contact.html',      'nav.contact']",
             "['tg',           '/contact.html',      'nav.contact']",
             "['bot',          '/contact.html',      'nav.contact']"]:
    ok(_nf124.count(_row) == 1, "404.html: r124 rescue alias row missing: " + _row)
ok(_nf124.count("r124: the Telegram surface") == 1, "404.html: r124 rescue comment missing")
# ordering contract: the specific contact rows precede the short aliases (first-match-wins)
_ok_contact = _nf124.find("['contact',")
_ok_tg = _nf124.find("['tg',")
_ok_bot = _nf124.find("['bot',")
ok(_ok_contact != -1 and _ok_tg != -1 and _ok_bot != -1 and _ok_contact < _ok_tg < _ok_bot,
   "404.html: r124 alias ordering broken (specific rows must precede short aliases)")


# --- r123 ship asserts (perf-HUD context segment) -------------------------------------------------
_eng = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok(_eng.count("' | ' + (document.documentElement.lang || '?') + '/' + (document.documentElement.dir || '?') +") == 1,
   "i18n.js: r123 HUD lang/dir context segment missing")
ok(_eng.count("' @ ' + location.host + '/' + (location.pathname.split('/').pop() || '')") == 1,
   "i18n.js: r123 HUD origin/page context segment missing")
ok(_eng.count("r123: context segment (page/lang/dir @ host)") == 1,
   "i18n.js: r123 HUD section comment missing")
ok(_eng.count("' @ ' + location.host") <= 1,
   "i18n.js: HUD context segment duplicated")


# --- versions (v54 post; v53 residue zero; i18n v60 both sides) ---------------------------- ----------------------------------------

# --- r108 ship asserts -----------------------------------------------------------------------
ok(css.count("@media (prefers-reduced-transparency: reduce)") == 1, "style.css: reduced-transparency media query x!=1")
ok(css.count(".navbar { background: rgb(245,245,245); backdrop-filter: none; -webkit-backdrop-filter: none; }") == 1,
   "style.css: navbar opaque light rule x!=1")
ok(css.count("[data-theme=\"dark\"] .navbar { background: rgb(13,13,13); }") == 1,
   "style.css: navbar opaque dark rule x!=1")
ok(css.count(".perf-hud { background: rgb(10,15,26); backdrop-filter: none; -webkit-backdrop-filter: none; }") == 1,
   "style.css: perf-hud opaque rule x!=1")
_nf = (ROOT / "404.html").read_text(encoding="utf-8")
ok(_nf.count('.nf-suggest:not(' + '[' + 'hidden' + ']' + ')') == 1,
   "404.html: nf-suggest hidden-gate churned")
ok(_nf.count('class="nf-inputwrap"') == 1, "404.html: inputwrap span x!=1")
ok(_nf.count('.nf-search:focus-within .faq-filter-kbd') == 1,
   "404.html: kbd focus-hide rule x!=1")
ok(_nf.count('aria-keyshortcuts="/"') == 1, "404.html: aria-keyshortcuts x!=1")
ok(_nf.count('<kbd class="faq-filter-kbd" aria-hidden="true">/</kbd>') == 1,
   "404.html: kbd chip x!=1")
ok(_nf.count('padding-inline-end: 34px') == 1, "404.html: chip clearance x!=1")
ok(_nf.count('action="/faq.html" method="get"') == 1,
   "404.html: zero-JS GET contract churned")
ok(_nf.count("i18n.js?v=69") == 1, "404.html: i18n v69 pin x!=1")
_i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok(_i18n.count('2c) "/" shortcut on the 404 recovery search') == 1,
   "i18n.js: 2c comment x!=1")
ok(_i18n.count("document.querySelector('.nf-search input')") == 1,
   "i18n.js: 2c selector x!=1")
ok(_i18n.count("if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;") == 1,
   "i18n.js: 2b guard x!=1")
ok(_i18n.count("if (e.ctrlKey || e.metaKey || e.altKey) return;") == 1,
   "i18n.js: 2c shared modifier guard x!=1")


# --- r109 ship asserts ------------------------------------------------------------------------
ok(_nf.count(".nf-search input:not(:placeholder-shown) ~ .faq-filter-kbd") == 1,
   "404.html: placeholder-shown chip hide x!=1")
ok(_nf.count("r109: chip also hides once the field HOLDS a query") == 1,
   "404.html: r109 comment missing")
ok(_i18n.count("else if (e.key === 'Escape' && document.activeElement === nfInput)") == 1,
   "i18n.js: 2c Escape branch x!=1")
ok(_i18n.count("nfInput.value = '';") == 1, "i18n.js: 2c Escape clear x!=1")
ok(_i18n.count("nfInput.blur();") == 1, "i18n.js: 2c Escape blur x!=1")
ok(_i18n.count("r109: Escape completes the keyboard loop") == 1,
   "i18n.js: r109 comment missing")


# --- r110 ship asserts ------------------------------------------------------------------------
_hiw = (ROOT / "how-it-works.html").read_text(encoding="utf-8")
for _slug in ["built-for-difficult-networks", "connection-experience", "three-steps",
              "install-the-app", "tap-connect", "pay-when-ready", "ready-to-connect"]:
    ok(_hiw.count('id="' + _slug + '"') == 1, "how-it-works.html: h2 slug missing: " + _slug)
ok(_hiw.count("Install the app") == 1, "how-it-works.html: s1 fallback not synced")
ok(_hiw.count("Tap Connect</h2>") == 1, "how-it-works.html: s2 fallback not synced")
ok(_hiw.count("Pay when you\u2019re ready</h2>") == 1, "how-it-works.html: s3 fallback not synced")
ok(_hiw.count("Get the APK directly from our website") == 1, "how-it-works.html: s1.p fallback not synced")
ok(_hiw.count("free for the first 3 days") == 1, "how-it-works.html: s2.p fallback not synced")
ok(_hiw.count("A token arrives by e-mail for the renewal") == 1, "how-it-works.html: s3.p fallback not synced")
ok(_hiw.count("Choose a plan") == 0 and _hiw.count("Pay your way") == 0,
   "how-it-works.html: stale story residue present")
ok(_i18n.count('"faq.anchor.step"') == 1, "i18n.js: faq.anchor.step key missing")
for _loc in ["en", "ru", "fa", "ar", "es", "ne", "fr"]:
    _seg = _i18n[_i18n.find('"faq.anchor.step"'):_i18n.find('"faq.anchor.step"') + 420]
    ok(_seg.count(_loc + ":") >= 1, "i18n.js: faq.anchor.step missing locale " + _loc)
ok(_i18n.count("7c) how-it-works step anchors") == 1, "i18n.js: 7c comment missing")
ok(_i18n.count("document.querySelector('h2[id]')") == 1,
   "i18n.js: 7c selector guard x!=1")
ok(_i18n.count("document.querySelectorAll('h2[id]')") == 1,
   "i18n.js: 7c selector query x!=1")
ok(_i18n.count("a.setAttribute('data-i18n-aria', 'faq.anchor.step');") == 1,
   "i18n.js: 7c aria binding missing")
_css = css
ok(_css.count("main h2[id]:focus") == 1, "style.css: h2 focus suppression missing")

# --- r111 ship asserts (web3.html noscript honesty) --------------------------------------------
_w3 = (ROOT / "web3.html").read_text(encoding="utf-8")
ok(_w3.count("</noscript>") == 2, "web3.html: noscript blocks x!=2 (head style + body note; opening-tag comment mentions excluded by matching the closer)")
ok(_w3.count(".dl-spinner { display: none; }") == 1,
   "web3.html: noscript spinner hide x!=1")
ok(_w3.count(".dl-progress span:not(#web3Cancelled) { display: none; }") == 1,
   "web3.html: noscript redirecting-span hide x!=1")
ok(_w3.count("count-hygiene note") == 1,
   "web3.html: r111 count-hygiene comment missing")
ok(_w3.count("#web3Cancel, .web3-actions .share-chip { display: none; }") == 1,
   "web3.html: noscript dead-control hides x!=1")
ok(_w3.count('<noscript><p class="web3-nojs">') == 1,
   "web3.html: noscript note p missing (precise: only the real element opens with the tag)")
ok(_w3.count("JavaScript is off") == 1, "web3.html: noscript note text missing")
ok(_w3.count("the automatic redirect can&rsquo;t run") == 1,
   "web3.html: noscript note verb missing (shipped as rsquo entity)")
ok(".web3-nojs { display: flex;" in _w3,
   "web3.html: .web3-nojs styling missing from page style block")
ok(_w3.count("r111: noscript honesty") == 1, "web3.html: r111 head comment missing")
ok(_w3.count("r111: scripting-off note") == 1, "web3.html: r111 body comment missing")


# --- versions (r107: HTML-only round — v54/v60 pins carry; stale residue asserted) -----------
want_i, want_s = "i18n.js?v=69", "style.css?v=59"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")
    ok(t.count("style.css?v=55") == 0 and t.count("style.css?v=56") == 0 and t.count("style.css?v=57") == 0 and t.count("style.css?v=58") == 0, f"{page}: stale style pin residue")
    ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0 and t.count("i18n.js?v=65") == 0 and t.count("i18n.js?v=66") == 0 and t.count("i18n.js?v=67") == 0 and t.count("i18n.js?v=68") == 0, f"{page}: stale i18n pin residue")
ok("color-scheme: light;" in css and "color-scheme: dark;" in css,
   "style.css: color-scheme theme props churned")


# --- r128: legal-trio nav canonicalization (Task 127 re-lens catch) -----------
# privacy/terms/refund now carry the canonical nav: .nav-top-row wrapper
# (logo + actions + controls in one flex row, RTL row-reverse aware) plus the
# standard 6-link nav-links set used by every other content page. Legacy
# markers (nav.home link, t.me Support, raw mailto) are banned from the nav
# block; they remain available via the footer social row, contact.html,
# llms.txt and security.txt. mailto pin moved 16 -> 13 in the carried chain.
LEGAL = ["privacy.html", "terms.html", "refund.html"]
STD6 = ["nav.features", "nav.how", "nav.compare", "nav.pricing", "nav.faq", "nav.contact"]
for page in LEGAL:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count('<div class="nav-inner">\n      <div class="nav-top-row">') == 1,
       page + ": nav-top-row wrapper missing (r128 canonical nav)")
    ok(t.count("r128: legal-trio nav canonicalization") == 1,
       page + ": r128 comment marker missing")
    i = t.index('<div class="nav-inner">')
    j = t.index("</nav>", i)
    block = t[i:j]
    for k in STD6:
        # nav.contact is x2 by design (nav-actions CTA + nav-links item);
        # the other five live only in nav-links.
        want = 2 if k == "nav.contact" else 1
        ok(block.count('data-i18n="' + k + '"') == want,
           page + ": standard nav key " + k + " != x" + str(want) + " in nav block")
    ok(block.count("nav.home") == 0, page + ": legacy nav.home still in nav block")
    ok(block.count("t.me") == 0, page + ": legacy t.me link still in nav block")
    ok(block.count("mailto") == 0, page + ": legacy mailto still in nav block")
# Uniformity: every other keyed nav-links page (index has an unkeyed set;
# 404/offline are chrome-less) carries the SAME 6-key set inside its nav block.
KEYED = [p for p in PAGES if p not in LEGAL and p not in ("index.html", "404.html", "offline.html")]
for page in KEYED:
    t = (ROOT / page).read_text(encoding="utf-8")
    i = t.index('<div class="nav-inner">')
    j = t.index("</nav>", i)
    block = t[i:j]
    for k in STD6:
        want = 2 if k == "nav.contact" else 1
        ok(block.count('data-i18n="' + k + '"') == want,
           page + ": nav uniformity — " + k + " != x" + str(want) + " in nav block")


# --- r132: pre-paint install reveal + 63-dead-key prune (Task 132 ship) -------
_i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
# (a) install CLS fix — boot guard + CSS override + flag lifecycle
_dl = (ROOT / "download.html").read_text(encoding="utf-8")
ok(_dl.count("r132: pre-paint install reveal") == 1, "download.html: r132 boot marker missing")
ok(_dl.count('localStorage.getItem("nv_bip")') == 1, "download.html: nv_bip flag read missing")
ok(_dl.count('classList.add("bip-ready")') == 1, "download.html: bip-ready add missing")
ok(_dl.count("(display-mode: standalone)") == 1, "download.html: standalone guard missing")
ok(_i18n.count("r132: zero-CLS repeat views") == 1, "i18n.js: r132 section-9 marker missing")
ok(_i18n.count("localStorage.setItem('nv_bip', '1')") == 1, "i18n.js: nv_bip setItem x!=1")
ok(_i18n.count("localStorage.removeItem('nv_bip')") == 1, "i18n.js: nv_bip removeItem x!=1")
ok(_i18n.count("localStorage.getItem('nv_bip')") == 1, "i18n.js: nv_bip getItem x!=1")
ok(_i18n.count("nvBipArrived") == 4, "i18n.js: nvBipArrived lifecycle x!=4 (decl+set+read+comment)")
ok(_i18n.count("'bip-ready'") == 1, "i18n.js: bip-ready class remove x!=1")
ok(css.count(".bip-ready #dl-install { display: inline-block !important; }") == 1,
   "style.css: bip-ready override rule missing (must carry !important vs the r45 author guard)")
ok(css.count(".bip-ready #dl-install,") == 1 and
   css.count("#dl-install { display: none !important; }") == 1,
   "style.css: print hide for #dl-install missing (variant selector outranked reveal rule)")
ok(css.count("r132: pre-paint install reveal") == 1, "style.css: r132 marker missing")
# (b) dead-key prune tripwire: 63 pruned names stay out of every shipped file
_DEAD63 = ["nav.whynull", "nav.cta", "index.badge", "index.h1a", "index.h1b",
    "index.sub", "index.btn.get", "index.btn.compare", "index.btn.how",
    "index.trust1", "index.trust2", "index.trust3", "index.trust4", "index.sp",
    "index.prob.h", "index.prob1", "index.prob2", "index.prob3", "index.prob4",
    "index.diff.h", "index.feat.more", "index.cta.also",
    "tech.h", "tech.1", "tech.2", "tech.3", "tech.4", "tech.5", "tech.6",
    "price.monthly", "price.quarterly", "price.annual", "price.billed.mo",
    "price.f1", "price.f2", "price.f3", "price.f4", "price.f5", "price.f6",
    "price.f7", "price.f8", "price.f9", "price.btn.mo", "price.btn.qt",
    "price.btn.an", "price.pay.h", "price.pay.p", "price.pay.p2",
    "faq.section.how", "faq.section.privacy", "faq.section.setup",
    "faq.section.access", "priv.q6", "priv.a6", "comp.hero.badge",
    "comp.hero.h1", "comp.hero.lead", "comp.table.nullvpn",
    "comp.row.restrictive", "comp.row.strictnat", "comp.val.unavailable",
    "comp.val.inconsistent", "refund.more"]
_PAGE_SRC = {p: (ROOT / p).read_text(encoding="utf-8") for p in PAGES}
for _k in _DEAD63:
    ok(('"' + _k + '"') not in _i18n, "i18n.js: pruned key re-introduced: " + _k)
    for _p, _t in _PAGE_SRC.items():
        ok(('"' + _k + '"') not in _t and ("'" + _k + "'") not in _t,
           _p + ": pruned key referenced: " + _k)
# (c) rescued dynamic families MUST remain in T (r128-E2E-proven contracts)
for _k in ("success.plan.monthly", "success.plan.quarterly", "success.plan.annual",
           "a11y.copyfail", "share.done", "share.answer", "share.clause",
           "faq.anchor.label", "faq.anchor.clause", "comp.anchor.row",
           "pricing.anchor.plan", "feat.anchor.row"):
    ok(_k in _T, "i18n.js: rescued dynamic key missing from T: " + _k)
ok(len(_T) == 466, f"i18n.js: key count drifted (got {len(_T)}, expected 466)")

if errs:
    print("check_r132: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r132: ALL GREEN ({len(PAGES)} pages)")
