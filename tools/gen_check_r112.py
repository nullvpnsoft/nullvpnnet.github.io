#!/usr/bin/env python3
"""Generate tools/check_r112.py from check_r111.py: swap the docstring,
inject r112 ship asserts, update version pins v64->v65, relabel output."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r111.py").read_text(encoding="utf-8")

# 1) docstring swap: replace everything between the first pair of triple
#    quotes with the r112 doc (the old doc spans to the closing quotes).
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = '''#!/usr/bin/env python3
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
"""'''

out = src[:start] + new_doc + src[end:]

# 2) r112 ship asserts before the versions section
r112_block = '''
# --- r112 ship asserts (download.html release-grid i18n correctness) ---------------------------
_dl = (ROOT / "download.html").read_text(encoding="utf-8")
ok(_dl.count("var MIN_ANDROID_RE = ") == 1, "download.html: MIN_ANDROID_RE missing")
ok(_dl.count("minimum\\\\s+android") == 1, "download.html: MIN_ANDROID_RE body churned")
ok(_dl.count("window.__lastRelease = rel;") == 1, "download.html: __lastRelease cache missing")
ok(_dl.count("window.RERENDER_RELEASE_META = function () {") == 1,
   "download.html: re-render hook missing")
ok(_dl.count("if (window.__lastRelease) applyRelease(window.__lastRelease);") == 1,
   "download.html: hook live-release branch missing")
ok(_dl.count("else if (window.RELEASE_META) renderStatic(window.RELEASE_META);") == 1,
   "download.html: hook static branch missing")
ok(_dl.count("[L('minandroid', 'Minimum Android'), minA || '\u2014'],") == 1,
   "download.html: applyRelease minAndroid row missing")
ok(_dl.count("apk ? L('stable', 'Stable') : '\u2014'") == 1,
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

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r112_block + anchor, 1)

# 3) version pins: v64 -> v65 (i18n changed; style stays v56) — both the
#    versions loop AND the carried r108-era per-page pin assert.
out = out.replace('want_i, want_s = "i18n.js?v=64", "style.css?v=56"',
                  'want_i, want_s = "i18n.js?v=65", "style.css?v=56"')
out = out.replace('ok(_nf.count("i18n.js?v=64") == 1, "404.html: i18n v64 pin x!=1")',
                  'ok(_nf.count("i18n.js?v=65") == 1, "404.html: i18n v65 pin x!=1")')
out = out.replace('ok(t.count("i18n.js?v=63") == 0, f"{page}: stale v63 pin residue")',
                  'ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0, '
                  'f"{page}: stale i18n pin residue")')

# 4) relabel
out = out.replace('print("check_r111: FAILURES:")', 'print("check_r112: FAILURES:")')
out = out.replace('print(f"check_r111: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r112: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r112.py").write_text(out, encoding="utf-8")
print("check_r112.py written:", len(out), "bytes")
