#!/usr/bin/env python3
"""Generate tools/check_r121.py from check_r120.py: swap the docstring,
inject the locale-bootstrap + navbar-reveal contract gates, relabel output.
i18n buster bumped v66 -> v67 (applyLang changed; SW serves buster-versioned
assets cache-first — HTML itself is network-first, so only the engine pin moves).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r120.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r121 guards: pre-paint locale bootstrap + navbar reveal contract.

(Carries the full r44-r120 chain, regenerated from check_r120.py; the r118
value-quality asserts, r119 Latin-locale debt gates and r120 sibling-identity
gates remain in force.)

SHIP (CLS fix round): the ?perf=1 HUD caught repeat-visitor layout shifts the
visual lenses had missed — warm SW-cached loads painted the static EN LTR
layout first, then the deferred applyLang() flipped html[dir] (fa/ar) and
re-wrapped the painted navbar text (locale label widths differ): measured CLS
0.062-0.251 on comparison.html (2x the 0.1 "poor" threshold at worst), with
shift sources = .nav-actions/.lang-selector/.logo/.theme-toggle/LI at ~210ms.

Fix (3 parts, all contract-gated here):
  1. HEAD LOCALE BOOTSTRAP on every page (after the color-scheme meta):
     resolves ?lang= param > stored nullvpn_lang over the same 7-locale set
     (mirrors getLang(); navigator.language deliberately NOT mirrored —
     first-visit cold loads paint after applyLang anyway, CLS 0.002) and
     sets html[lang]/[dir] BEFORE first paint. Non-EN also adds html.nv-l
     and arms a 2s failsafe reveal.
  2. INLINE RULE html.nv-l .nav-inner{visibility:hidden} — layout-preserving
     hide; the EN->locale text swap now paints invisibly (visibility toggles
     produce no layout-shift entries), so neither the dir flip nor the label
     swap can reflow visible chrome.
  3. applyLang() removes nv-l as its final step — the normal reveal path
     (idempotent across explicit language switches).
  4. i18n.js buster v66 -> v67 (cache-first asset: cached engines lack the
     reveal line and would leave the navbar hidden until the failsafe).

E2E evidence: comparison warm loads CLS 0.062-0.251 -> 0.000 (5/5 local
runs); fa nav renders Persian labels pre-reveal; en path untouched (no
class, no hide); 15/15 pages sweep clean; failsafe proven by serving a copy
without i18n.js (navbar hidden at t0, revealed after the 2s timeout).
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r121 asserts before the versions section
r121_block = '''
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

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r121_block + anchor, 1)

# 3) i18n buster bump v66 -> v67: applyLang gained the nv-l reveal line, and the
#    SW serves buster-versioned assets cache-first — an unbumped i18n.js would
#    keep cached (no reveal) for repeat visitors and the navbar would stay
#    hidden until the failsafe. The carried v66 pins are bumped with the chain.
out = out.replace('want_i, want_s = "i18n.js?v=66", "style.css?v=58"',
                  'want_i, want_s = "i18n.js?v=67", "style.css?v=58"')
out = out.replace('i18n.js?v=66"', 'i18n.js?v=67"')  # 404 per-page pin
t_old = 't.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0 and t.count("i18n.js?v=65") == 0'
t_new = 't.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0 and t.count("i18n.js?v=65") == 0 and t.count("i18n.js?v=66") == 0'
assert t_old in out, "residue line not found"
out = out.replace(t_old, t_new, 1)
out = out.replace('i18n v66 / style v58 — no asset busters bumped', 'i18n v67 / style v58')

# 4) relabel
out = out.replace('print("check_r120: FAILURES:")', 'print("check_r121: FAILURES:")')
out = out.replace('print(f"check_r120: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r121: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r121.py").write_text(out, encoding="utf-8")
print("check_r121.py written:", len(out), "bytes")
