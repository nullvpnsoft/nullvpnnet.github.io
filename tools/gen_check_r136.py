#!/usr/bin/env python3
"""gen_check_r136.py — generate tools/check_r136.py from check_r135.py.

r136 = contact e-mail migration: support@nullvpn.net -> nullvpn@googlegroups.com
(site-wide: 15 pages, i18n.js, security.txt x2, llms.txt) + i18n buster v71->v72.

Carries the full r44-r135 chain with:
  - mailto pins re-pointed at the new address (subject-form == 13, bare == 0)
  - want_i v71 -> v72; stale i18n residue list extended with v71
  - NEW r136 section: estate-wide old-address zero-leak (support@/admin@),
    new-address presence pins (i18n 49, 3 copy-chips, JSON-LD, security.txt x2,
    llms.txt)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "check_r135.py"
DST = ROOT / "tools" / "check_r136.py"

src = SRC.read_text(encoding="utf-8")

# 1. e-mail re-point inside carried pins (mailto subject/bare/contact prefill)
assert src.count("support@nullvpn.net") == 3, "expected exactly 3 email refs in r135 guard"
src = src.replace("support@nullvpn.net", "nullvpn@googlegroups.com")

# 2. version pins v71 -> v72
n_v71 = src.count("i18n.js?v=71")
assert n_v71 >= 2, f"expected >=2 v71 refs, got {n_v71}"
src = src.replace("i18n.js?v=71", "i18n.js?v=72")

# 3. extend the stale i18n residue list with v71
old_stale = 't.count("i18n.js?v=70") == 0, f"{page}: stale i18n pin residue")'
new_stale = ('t.count("i18n.js?v=70") == 0 and t.count("i18n.js?v=71") == 0, '
             'f"{page}: stale i18n pin residue")')
assert src.count(old_stale) == 1, "stale i18n list anchor not found"
src = src.replace(old_stale, new_stale)

# 4. identity of the guard
src = src.replace('print("check_r135: FAILURES:")', 'print("check_r136: FAILURES:")')
src = src.replace('print(f"check_r135: ALL GREEN', 'print(f"check_r136: ALL GREEN')

# 5. prepend the r136 docstring banner
old_banner = '"""r127 guards:'
new_banner = ('"""r136 guards: contact e-mail migration to nullvpn@googlegroups.com\n'
              '(site-wide swap + i18n buster v72; old-address zero-leak estate-wide).\n'
              '\n'
              '(Carries the full r44-r135 chain, regenerated from check_r135.py.)\n'
              '\n'
              'r127 guards:')
assert src.count(old_banner) == 1, "docstring banner anchor not found"
src = src.replace(old_banner, new_banner)

# 6. inject the r136 section before the final verdict block
anchor = '\nif errs:\n    print("check_r136: FAILURES:")'
assert src.count(anchor) == 1, "verdict anchor not found"
r136_section = '''
# --- r136: contact e-mail migration (support@nullvpn.net -> nullvpn@googlegroups.com) --------
_NEW_EMAIL = "nullvpn@googlegroups.com"
_leak_files = list(PAGES) + ["i18n.js", "security.txt", ".well-known/security.txt", "llms.txt"]
for _f in _leak_files:
    _t = (ROOT / _f).read_text(encoding="utf-8")
    ok(_t.count("support@nullvpn.net") == 0, f"{_f}: old support@ address residue")
    ok(_t.count("admin@nullvpn.net") == 0, f"{_f}: admin@ residue")
_i136 = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok(_i136.count(_NEW_EMAIL) == 49, f"i18n.js: new e-mail count {_i136.count(_NEW_EMAIL)} != 49")
_chip_total = sum((ROOT / _p).read_text(encoding="utf-8").count('data-copy="' + _NEW_EMAIL + '"')
                  for _p in PAGES)
ok(_chip_total == 3, f"copy-chip data-copy count {_chip_total} != 3 (contact/success/refund)")
ok('"email": "' + _NEW_EMAIL + '"' in (ROOT / "index.html").read_text(encoding="utf-8"),
   "index.html: JSON-LD ContactPoint e-mail not migrated")
for _sf in ("security.txt", ".well-known/security.txt"):
    ok("Contact: mailto:" + _NEW_EMAIL in (ROOT / _sf).read_text(encoding="utf-8"),
       _sf + ": Contact mailto not migrated")
ok(_NEW_EMAIL in (ROOT / "llms.txt").read_text(encoding="utf-8"), "llms.txt: e-mail not migrated")
'''
src = src.replace(anchor, r136_section + anchor)

DST.write_text(src, encoding="utf-8")
print(f"written {DST} ({len(src.splitlines())} lines)")
