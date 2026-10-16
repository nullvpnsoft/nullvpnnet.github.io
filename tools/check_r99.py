#!/usr/bin/env python3
"""r99 guards: post-rotation verification round — two ships.

SHIP 1 (i18n.js, v57 -> v58): live OS-theme follow — visitors who never
picked a theme explicitly now get native-app behavior (page re-themes when
the OS flips). Explicit choice (stored 'theme') always wins. Legacy
addListener covered; button state mirrored via the pages' global
updateThemeButtons when present (404/offline have none — guarded).

SHIP 2 (style.css, v48 -> v49): .theme-btn was a FUNCTIONAL control still
carrying the decorative --border (mis-filed decorative in r98's inventory —
a real 1.4.11 miss: bg3 fill + 1.18:1 border) AND its hover used opacity .8,
the opacity-blend trap (active button's white-on-accent2 drifts toward the
4.5 AA line on hover). Now: border-strong boundary + hover lifts
border/glyph on non-active buttons only; the active (current-state) button
keeps full contrast.

The r98 living WCAG math carries forward. Decorative plain-border inventory
is now 12 (theme-btn lifted out of it); border-strong shorthands now 10.
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

# --- SHIP 1: live OS-theme follow -----------------------------------------------------
ok("14) Live OS-theme follow (r99)" in i18, "i18n.js: r99 OS-follow block missing")
ok("if (localStorage.getItem('theme')) return; /* explicit choice wins */" in i18,
   "i18n.js: explicit-choice guard missing")
ok("mqOS.addEventListener('change', osFollow)" in i18, "i18n.js: modern listener missing")
ok("mqOS.addListener(osFollow)" in i18, "i18n.js: legacy addListener missing")
ok("typeof updateThemeButtons === 'function'" in i18, "i18n.js: button mirror guard missing")
ok("e.matches ? 'dark' : 'light'" in i18, "i18n.js: flip direction missing")
ok(i18.count("mqOS.addEventListener('change', osFollow)") == 1, "i18n.js: OS listener call x!=1")

# --- SHIP 2: theme-btn functional boundary + hover rework -----------------------------
ok("border: 1px solid var(--border-strong); /* r99: functional control boundary (1.4.11)" in css,
   "style.css: theme-btn border swap missing")
ok(".theme-btn:hover { opacity: 0.8; }" not in css, "style.css: opacity-blend hover still present")
ok("@media (hover: hover) and (pointer: fine) { .theme-btn:hover:not(.active) { border-color: var(--accent-text); color: var(--accent-text); } }" in css,
   "style.css: r99 hover rework missing")
ok(".theme-btn.active { background: var(--accent2); color: #fff; border-color: var(--accent2); }" in css,
   "style.css: theme-btn active state churned")
ok('[data-theme="dark"] .theme-btn { background: var(--bg3); color: #ccc; }' in css,
   "style.css: theme-btn dark variant churned")

# --- inventory counts (evolved from r98) ------------------------------------------------
ok(css.count("border: 1px solid var(--border);") == 12,
   "style.css: decorative plain-border inventory changed (expected 12)")
ok(css.count("border: 1px solid var(--border-strong)") == 10,
   "style.css: border-strong shorthand count changed (expected 10)")
ok(css.count("--border-strong:") == 2, "style.css: token must be defined exactly twice")

# --- LIVING WCAG MATH (carried from r98) ------------------------------------------------
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
    bs, bg, bg2, bg3 = v.get("--border-strong"), v.get("--bg"), v.get("--bg2"), v.get("--bg3")
    t2, at = v.get("--text2"), v.get("--accent-text")
    ok(bs and bg and bg2 and bg3, f"{theme}: token parse failed")
    if bs and bg and bg2 and bg3:
        for sname, s in (("bg", bg), ("bg2", bg2), ("bg3", bg3)):
            r = ratio(bs, s)
            ok(r >= 3.0, f"{theme}: border-strong vs {sname} = {r:.2f} < 3.0")
    if t2 and bg and bg2 and bg3:
        for sname, s in (("bg", bg), ("bg2", bg2), ("bg3", bg3)):
            r = ratio(t2, s)
            ok(r >= 4.5, f"{theme}: text2 vs {sname} = {r:.2f} < 4.5 (AA drift)")
    if at and bg and bg2 and bg3:
        for sname, s in (("bg", bg), ("bg2", bg2), ("bg3", bg3)):
            r = ratio(at, s)
            ok(r >= 4.5, f"{theme}: accent-text vs {sname} = {r:.2f} < 4.5 (AA drift)")
ok(parse_block(":root {").get("--border-strong") == "#8a744a", "light border-strong hex drifted")
ok(parse_block('[data-theme="dark"] {').get("--border-strong") == "#64748b", "dark border-strong hex drifted")

# --- anti-churn (carried forward) --------------------------------------------------------
ok(css.count("idden]") >= 6, "style.css: r45 hidden-attr canary regressed")
ok(":root { accent-color: var(--accent); }" in css, "style.css: r89 accent churned")
ok(css.count("@page { margin: 14mm 12mm; }") == 1, "style.css: r91 @page churned")
ok("font-variant-numeric: tabular-nums" in css, "style.css: r92 tabular churned")
ok("content: var(--print-src, none)" in css, "style.css: r93 provenance churned")
ok(css.count("body::after") == 1, "style.css: body::after collision")
idx = (ROOT / "index.html").read_text(encoding="utf-8")
ok(idx.count("og:locale:alternate") == 6, "index.html: r92 og churned")
ok('<main id="main"' in idx, "index.html: r90 landmark churned")
ok("overflow-wrap:anywhere" in (ROOT / "success.html").read_text(encoding="utf-8"),
   "success.html: r91 fix churned")
ok(".faq-item p a, .success-note a, .hiw-note a, .nf-sub a, .dh-sub a," in css,
   "style.css: r94 prose rule churned")
ok(css.count("@media (forced-colors: active)") == 1, "style.css: r94 forced-colors churned")
ok('<p class="contact-sub" data-i18n="contact.sub">' in (ROOT / "contact.html").read_text(encoding="utf-8"),
   "contact.html: r94 contact-sub churned")
ok("## Privacy engineering" in (ROOT / "llms.txt").read_text(encoding="utf-8"),
   "llms.txt: r94 section churned")
ok("if (e.key !== 'Escape' || !faqFilter.value) return;" in i18, "i18n.js: r95 Escape churned")
ok("behavior: reduce ? 'auto' : 'smooth', block: 'center'" in i18, "i18n.js: r95 motion gate churned")
ok("@media print { .faq-filter { display: none !important; } }" in css, "style.css: r95 print-hide churned")
ok("const initialQ = (() => {" in i18, "i18n.js: r96 deep-link churned")
ok("if (q) u.searchParams.set('q', q);" in i18, "i18n.js: r96 q sync churned")
ok('maxlength="80"' in (ROOT / "faq.html").read_text(encoding="utf-8"), "faq.html: r96 maxlength churned")
ok(pricing.count("@media (prefers-reduced-motion: reduce){.checkout") == 1,
   "pricing.html: r96 reduce gate churned")
TRAP = ("querySelectorAll('button,a" + chr(91) + "href" + chr(93) +
        ",input,select,textarea," + chr(91) + "tabindex" + chr(93) + ":not(" +
        chr(91) + 'tabindex="-1"' + chr(93) + ")')")
ok(TRAP in pricing, "pricing.html: r44 trap selector drifted")
ok("caches.match(req, { ignoreSearch: true })" in (ROOT / "sw.js").read_text(encoding="utf-8"),
   "sw.js: r97 normalization churned")
ok("fetch('/', { method: 'HEAD', cache: 'no-store' })" in i18, "i18n.js: r97 probe churned")
ok("const CACHE = 'nullvpn-v3';" in (ROOT / "sw.js").read_text(encoding="utf-8"),
   "sw.js: cache name churned")
# r98 chain
ok("r98: functional boundaries" in css, "style.css: r98 token comment churned")
ok(css.count("border: 1px solid var(--border-strong); background: var(--bg3); /* r98 */") == 3,
   "style.css: r98 chip swaps churned")
ok("border:1px solid var(--border-strong,#64748b);border-radius:16px; /* r98: dialog boundary 1.4.11 */" in pricing,
   "pricing.html: r98 modal boundary churned")
ok("border: 1px solid var(--border-strong); background: var(--bg3); /* r98: offline nav chips are functional links */" in offline,
   "offline.html: r98 chip swap churned")

# --- versions ------------------------------------------------------------------------------
if "--post-bust" in sys.argv:
    want_i, want_s = "i18n.js?v=58", "style.css?v=49"
else:
    want_i, want_s = "i18n.js?v=57", "style.css?v=48"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")

if errs:
    print("check_r99: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r99: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages)")
