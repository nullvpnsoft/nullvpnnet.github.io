#!/usr/bin/env python3
"""gen_check_r139.py — generate tools/check_r139.py from check_r136.py.

r139 = visible-detail round:
  SHIP F: effective-monthly price lines (price.p3.eff / price.p4.eff, 7 locales
          each) rendered via .price-eff spans on pricing.html
  SHIP S: navbar elevation on scroll (.navbar.scrolled + i18n.js 5b toggle),
          QR-card entrance (qrIn), search-mark pulse (markPulse via --mark-a
          custom property), reduced-motion suppression for all motion
  Busters: i18n v72->v73, style v61->v62. Keys 470->472, usages 803->805.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "check_r136.py"
DST = ROOT / "tools" / "check_r139.py"

src = SRC.read_text(encoding="utf-8")

# 1. version pins
assert src.count('i18n.js?v=72') >= 2
src = src.replace("i18n.js?v=72", "i18n.js?v=73")
assert src.count('style.css?v=61') >= 1
src = src.replace("style.css?v=61", "style.css?v=62")

# 2. stale residue lists extended
old_i_stale = 't.count("i18n.js?v=70") == 0 and t.count("i18n.js?v=71") == 0, '
new_i_stale = ('t.count("i18n.js?v=70") == 0 and t.count("i18n.js?v=71") == 0 and '
               't.count("i18n.js?v=72") == 0, ')
assert src.count(old_i_stale) == 1, "i18n stale anchor"
src = src.replace(old_i_stale, new_i_stale)

old_s_stale = 't.count("style.css?v=60") == 0, f"{page}: stale style pin residue")'
new_s_stale = ('t.count("style.css?v=60") == 0 and t.count("style.css?v=61") == 0, '
               'f"{page}: stale style pin residue")')
assert src.count(old_s_stale) == 1, "style stale anchor"
src = src.replace(old_s_stale, new_s_stale)

# 3. key count 470 -> 472 (two hard pins + two soft mentions)
assert src.count("== 470") == 2, src.count("== 470")
src = src.replace("== 470", "== 472")
src = src.replace("~470", "~472")
src = src.replace("all 470 keys", "all 472 keys")

# 4. identity
src = src.replace('print("check_r136: FAILURES:")', 'print("check_r139: FAILURES:")')
src = src.replace('print(f"check_r136: ALL GREEN', 'print(f"check_r139: ALL GREEN')

# 5. docstring banner
old_banner = '"""r136 guards: contact e-mail migration to nullvpn@googlegroups.com'
new_banner = ('"""r139 guards: visible-detail round (price-eff lines x7 locales,\n'
              'navbar elevation, qrIn entrance, markPulse, busters v73/v62).\n'
              '\n'
              '(Carries the full r44-r136 chain, regenerated from check_r136.py.)\n'
              '\n'
              'r136 guards: contact e-mail migration to nullvpn@googlegroups.com')
assert src.count(old_banner) == 1, "r136 banner anchor"
src = src.replace(old_banner, new_banner)

# 6. r139 section before the verdict (RAW string — single backslashes survive)
anchor = '\nif errs:\n    print("check_r139: FAILURES:")'
assert src.count(anchor) == 1, "verdict anchor"
r139 = r'''
# --- r139: visible-detail round --------------------------------------------------------------
_i139 = (ROOT / "i18n.js").read_text(encoding="utf-8")
_p139 = (ROOT / "pricing.html").read_text(encoding="utf-8")
_css139 = (ROOT / "style.css").read_text(encoding="utf-8")
for _k in ("price.p3.eff", "price.p4.eff"):
    ok(_i139.count('"' + _k + '": {') == 1, f"i18n.js: {_k} key missing")
    _m139 = re.search(r'"' + _k + r'": \{(.*?)\n  \}', _i139, re.S)
    ok(_m139 is not None, f"i18n.js: {_k} block unparsable")
    if _m139:
        _vals139 = re.findall(r'\w{2}: "[^"]+"', _m139.group(1))
        ok(len(_vals139) == 7, f"i18n.js: {_k} has {len(_vals139)} locales, expected 7")
ok(_p139.count('data-i18n="price.p3.eff"') == 1, "pricing.html: p3.eff usage x!=1")
ok(_p139.count('data-i18n="price.p4.eff"') == 1, "pricing.html: p4.eff usage x!=1")
ok('class="price-eff"' in _p139, "pricing.html: .price-eff class missing")
ok("\n.navbar.scrolled { box-shadow: 0 2px 14px rgba(0, 0, 0, 0.10); }" in _css139, "style.css: navbar elevation rule missing")
ok('[data-theme="dark"] .navbar.scrolled' in _css139, "style.css: navbar dark shadow missing")
ok("@keyframes qrIn" in _css139 and ".qr-card { animation: qrIn" in _css139,
   "style.css: qrIn entrance missing")
ok("@keyframes markPulse" in _css139 and ".faq-item mark { --mark-a: 0.16; animation: markPulse" in _css139,
   "style.css: markPulse missing")
ok('[data-theme="dark"] .faq-item mark { --mark-a: 0.30; }' in _css139,
   "style.css: dark mark pulse target missing")
ok(".price-eff { display: block;" in _css139, "style.css: .price-eff rule missing")
ok(".qr-card, .faq-item mark { animation: none; }" in _css139,
   "style.css: reduced-motion suppression missing")
ok("5b) Navbar elevation on scroll (r139)" in _i139, "i18n.js: nav elevation section missing")
ok("nav.classList.toggle('scrolled'" in _i139, "i18n.js: nav scrolled toggle missing")
'''
src = src.replace(anchor, r139 + anchor)

DST.write_text(src, encoding="utf-8")
print(f"written {DST} ({len(src.splitlines())} lines)")
