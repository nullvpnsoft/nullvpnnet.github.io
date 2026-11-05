#!/usr/bin/env python3
#!/usr/bin/env python3
"""r112 guards: download.html release-grid i18n correctness.

(Carries the full r44-r111 chain, regenerated from check_r111.py; r111 ship asserts remain in force below.)

SHIP (download.html + i18n.js — spot-audit round covered success / download /
privacy / refund; only download had real findings, and all three were in the
inline release-metadata fetcher):

1. LANGUAGE-SWITCH STALENESS: i18n.js refreshed DL_META_I18N on every
   applyLang, but nothing re-rendered the ALREADY-RENDERED grid — after a
   switch the cells kept the previous language's labels forever. Fix:
   download.html exposes window.RERENDER_RELEASE_META (re-renders the live
   release if the fetch landed — window.__lastRelease cached by
   applyRelease — else the static placeholder); i18n.js calls it right after
   refreshing the label map, guarded (no-op on the other 14 pages).

2. SHAPE DRIFT: applyRelease rendered 6 cells while the r71 placeholder
   renders 7 (minAndroid was dropped) — the fetch fill would have re-flowed
   the grid, the exact CLS the r71 note fought. Fix: minAndroid row restored,
   parsed from the release body ("Minimum Android: 8.0", MIN_ANDROID_RE),
   em-dash placeholder when absent so the 7-cell shape is invariant.

3. UNLOCALIZED STATUS VALUE: applyRelease hardcoded EN "Stable" while every
   label around it localized. Fix: L('stable','Stable') + new key
   dl.meta.stable x7 locales + stable: t(...) in the DL_META_I18N map.

i18n buster v64 -> v65 estate-wide (style.css stays v56 — no style changes).
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
ok(_nf.count("i18n.js?v=65") == 1, "404.html: i18n v65 pin x!=1")
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
want_i, want_s = "i18n.js?v=65", "style.css?v=56"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")
    ok(t.count("style.css?v=55") == 0, f"{page}: stale v55 pin residue")
    ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0, f"{page}: stale i18n pin residue")
ok("color-scheme: light;" in css and "color-scheme: dark;" in css,
   "style.css: color-scheme theme props churned")

if errs:
    print("check_r112: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r112: ALL GREEN ({len(PAGES)} pages)")
