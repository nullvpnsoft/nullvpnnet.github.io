#!/usr/bin/env python3
"""r98 guards: dark-theme secondary contrast lens.

Finding: dark TEXT all passes AA comfortably (text2 >= 5.71, accent-text >=
5.75 on every surface) — the r46 text lift holds. But BORDERS fail WCAG 1.4.11
non-text contrast (3:1): #293548 measured 1.55/1.44/1.18 vs bg/bg2/bg3. Decor-
ative edges (card outlines, section rules) are exempt — containers are not UI
components — but FUNCTIONAL boundaries are not: the FAQ search input, ghost/
nav buttons, language selector, faq-cat chips, toc pills, copy/share/copy-text
chips, the pricing checkout modal, and the offline nav chips all rely on their
border for identification.

Ships: --border-strong token (light #8a744a warm brown / dark #64748b slate-500)
applied to 9 style.css selectors + pricing.html checkout-modal + offline.html
.of-list a. The guard also RECOMPUTES the WCAG ratios from the token hexes so
any future palette drift (bg3 lightening, border-strong change) fails here.

Versions: style v47 (pre) -> v48 (post); i18n v57 holds (no key changes).
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
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
offline = (ROOT / "offline.html").read_text(encoding="utf-8")
i18 = (ROOT / "i18n.js").read_text(encoding="utf-8")

# --- SHIP 1: --border-strong tokens -------------------------------------------------
LIGHT_T = "--border-strong: #8a744a;"
DARK_T = "--border-strong: #64748b;"
ok(css.count(LIGHT_T) == 1, "style.css: light border-strong token x!=1")
ok(css.count(DARK_T) == 1, "style.css: dark border-strong token x!=1")
ok(css.count("--border-strong:") == 2, "style.css: token must be defined exactly twice")
ok("r98: functional boundaries" in css, "style.css: r98 token comment missing")

# 13 surviving plain shorthands = the DECORATIVE inventory (cards, notes, toc
# container, tbl-scroll, theme-btn, print outline) — they must keep --border.
ok(css.count("border: 1px solid var(--border);") == 13,
   "style.css: decorative plain-border inventory changed (expected 13)")
FN = "border: 1px solid var(--border-strong)"
ok(css.count(FN) == 9, f"style.css: border-strong shorthand x{css.count(FN)} != 9")
ok("border: 1px solid var(--border-strong); /* r98: border IS the control identity" in css,
   "style.css: btn-ghost swap missing")
ok("border: 1px solid var(--border-strong); /* r98: bg3 fill alone is sub-3:1 vs bg */" in css,
   "style.css: btn-nav swap missing")
ok("border: 1px solid var(--border-strong); /* r98 */\n  border-radius: 8px;" in css,
   "style.css: lang-selector swap missing")
ok("border: 1px solid var(--border-strong); border-radius: 10px; /* r98: input boundary 1.4.11 */" in css,
   "style.css: faq-filter input swap missing")
ok("border: 1px solid var(--border-strong); cursor: pointer; /* r98: chip boundary 1.4.11 */" in css,
   "style.css: faq-cat swap missing")
ok(".page-toc a { font-size: .82rem; font-weight: 600; padding: 5px 11px; border-radius: 999px; background: var(--bg); color: var(--text2); border: 1px solid var(--border-strong); text-decoration: none; /* r98 */" in css,
   "style.css: page-toc pill swap missing")
ok(css.count("border: 1px solid var(--border-strong); background: var(--bg3); /* r98 */") == 3,
   "style.css: copy/share/copy-text chip swaps != 3")

# decorative estate must NOT have been lifted
ok(css.count("border-bottom: 1px solid var(--border);") >= 5,
   "style.css: decorative section rules regressed")
ok("scrollbar-color: var(--border) transparent" in css, "style.css: decorative scrollbar churned")
ok(".page-toc { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 6px; padding: 12px 14px; background: var(--bg2); border: 1px solid var(--border); border-radius: 14px; }" in css,
   "style.css: page-toc container (decorative) churned")

# --- SHIP 2: checkout modal dialog boundary ------------------------------------------
ok("border:1px solid var(--border-strong,#64748b);border-radius:16px; /* r98: dialog boundary 1.4.11 */" in pricing,
   "pricing.html: checkout-modal boundary swap missing")

# --- SHIP 3: offline nav chips --------------------------------------------------------
ok("border: 1px solid var(--border-strong); background: var(--bg3); /* r98: offline nav chips are functional links */" in offline,
   "offline.html: of-list chip swap missing")
ok(".of-card { max-width: 560px; width: 100%; text-align: center; background: var(--bg2); border: 1px solid var(--border); border-radius: 18px; padding: 48px 32px; }" in offline,
   "offline.html: of-card (decorative container) churned")

# --- LIVING WCAG MATH: recompute ratios from the actual token hexes ------------------
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
    """Extract --var: #hex pairs from the CSS block starting at marker."""
    i = css.index(marker)
    j = css.index("}", i)
    return dict(re.findall(r"(--[a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", css[i:j]))

for marker, theme in ((":root {", "light"), ('[data-theme="dark"] {', "dark")):
    v = parse_block(marker)
    bs, bg, bg2, bg3 = v.get("--border-strong"), v.get("--bg"), v.get("--bg2"), v.get("--bg3")
    t2, at = v.get("--text2"), v.get("--accent-text")
    ok(bs is not None and bg is not None and bg2 is not None and bg3 is not None,
       f"{theme}: token parse failed ({bs},{bg},{bg2},{bg3})")
    if bs and bg and bg2 and bg3:
        for surf_name, surf in (("bg", bg), ("bg2", bg2), ("bg3", bg3)):
            r = ratio(bs, surf)
            ok(r >= 3.0, f"{theme}: border-strong {bs} vs {surf_name} {surf} = {r:.2f} < 3.0 (1.4.11)")
    if t2 and bg and bg2 and bg3:
        for surf_name, surf in (("bg", bg), ("bg2", bg2), ("bg3", bg3)):
            r = ratio(t2, surf)
            ok(r >= 4.5, f"{theme}: text2 {t2} vs {surf_name} {surf} = {r:.2f} < 4.5 (AA drift)")
    if at and bg and bg2 and bg3:
        for surf_name, surf in (("bg", bg), ("bg2", bg2), ("bg3", bg3)):
            r = ratio(at, surf)
            ok(r >= 4.5, f"{theme}: accent-text {at} vs {surf_name} {surf} = {r:.2f} < 4.5 (AA drift)")
ok(parse_block(":root {").get("--border-strong") == "#8a744a", "light border-strong hex drifted")
ok(parse_block('[data-theme="dark"] {').get("--border-strong") == "#64748b", "dark border-strong hex drifted")

# --- anti-churn (carried forward from check_r97) --------------------------------------
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
   "sw.js: cache name churned without a deliberate precache decision")

# --- versions --------------------------------------------------------------------------
want_s = "style.css?v=48" if "--post-bust" in sys.argv else "style.css?v=47"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count("i18n.js?v=57") == 1, f"{page}: i18n v57 must hold x1")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")

if errs:
    print("check_r98: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r98: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages, WCAG math verified)")
