#!/usr/bin/env python3
"""r100 guards (milestone): language-switch x active-filter interaction.

Finding (live QA): the r92-era re-run kept a TEXT query across a language
switch and re-applied it against the new locale's text — an EN term against
RU text is a guaranteed 0-hit dead end (0/11, empty state, foreign word left
in the box). Category choices were always portable (data-cat is a locale-
independent key) but text queries are not.

SHIP 1 (i18n.js, v58 -> v59): on a REAL language change (boot-safe via
lastFilterLang — the first pass must not wipe the r96 ?q= deep link, which
the wiring restores before the boot applyLang pass), clear the query, re-run
the filter through the canonical path (URL ?q= slot syncs away), and announce
the reset via the existing aria-live status line (new key faq.filter.cleared,
525 keys x7). Categories survive the switch.

SHIP 2 (style.css, v49 -> v50): the transient note reads as system feedback,
not results — .faq-filter-status.is-note italic treatment; applyFaqFilter
retires the note class on any subsequent filter run.

Perf audit (milestone): fonts preloaded (r54), zero raster images (CSS/SVG
site), i18n.js loaded at end of body — nothing to fix.
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

# --- SHIP 1: language-switch query reset ------------------------------------------------
ok("let lastFilterLang = null; // r100: boot guard" in i18,
   "i18n.js: lastFilterLang declaration missing")
ok("const langChanged = lastFilterLang !== null && lastFilterLang !== lang;" in i18,
   "i18n.js: langChanged boot-safe guard missing")
ok("const hadQuery = !!faqFilter.value;" in i18, "i18n.js: hadQuery capture missing")
ok("if (hadQuery) faqFilter.value = '';" in i18, "i18n.js: query clear missing")
ok("statusEl.textContent = t('faq.filter.cleared', lang);" in i18,
   "i18n.js: cleared-note write missing")
ok("statusEl.classList.add('is-note')" in i18 and "statusEl.classList.contains('is-note')" in i18,
   "i18n.js: note class lifecycle missing")
ok(i18.count('"faq.filter.cleared"') == 1, "i18n.js: cleared key x!=1")
for loc in ["en:", "ru:", "fa:", "ar:", "es:", "ne:", "fr:"]:
    pass  # key completeness is enforced by check_html_i18n (525x7)
ok("status.classList.remove('is-note'); /* typing/filtering retires the r100 note */" in i18,
   "i18n.js: applyFaqFilter note-retire missing")
ok(i18.count("applyFaqFilter();\n        if (hadQuery && activeCat === 'all') {") == 1,
   "i18n.js: clear-then-announce sequence x!=1")
# deep-link restore must still run AFTER the ?cat= restore and BEFORE boot applyLang
ok("if (initialQ) {" in i18, "i18n.js: r96 deep-link restore churned")

# --- SHIP 2: note styling ---------------------------------------------------------------
ok(".faq-filter-status.is-note { font-style: italic; }" in css,
   "style.css: is-note rule missing")

# --- carried-forward chains (r97-r99 highlights) -----------------------------------------
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
ok("border:1px solid var(--border-strong,#64748b);border-radius:16px; /* r98: dialog boundary 1.4.11 */" in pricing,
   "pricing.html: r98 modal boundary churned")
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

# --- versions ------------------------------------------------------------------------------
if "--post-bust" in sys.argv:
    want_i, want_s = "i18n.js?v=59", "style.css?v=50"
else:
    want_i, want_s = "i18n.js?v=58", "style.css?v=49"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")

if errs:
    print("check_r100: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r100: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages)")
