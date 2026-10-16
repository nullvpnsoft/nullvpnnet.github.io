#!/usr/bin/env python3
"""Generate tools/check_r114.py from check_r113.py: swap the docstring,
inject the r114 estate a11y-structure asserts (h1 uniqueness, empty headings,
unnamed links), relabel output. No version bumps this round (style v57 /
i18n v65 carried — guard-only ship; audit_r114.py is the lens tool).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r113.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = '''#!/usr/bin/env python3
"""r114 guards: estate a11y structure (headings + link purpose).

(Carries the full r44-r113 chain, regenerated from check_r113.py; r113 ship
asserts remain in force below.)

SHIP (guard-only round — no site-file changes, no buster bumps):

The r114 round ran two a11y lenses estate-wide (tool: tools/audit_r114.py):

1. HEADING HIERARCHY: every page has exactly one h1; no empty headings.
   Level skips (h1->h3 card headings, footer h4 column titles) were triaged
   as DELIBERATE (visual sizing + contentinfo landmark) and advisory-only —
   NOT asserted (would freeze a styling choice as a contract).

2. LINK PURPOSE: zero unnamed links estate-wide (every anchor carries text,
   data-i18n, aria-label, or an alt'd img child). WCAG 2.4.4 clean.

Both lenses are now PERMANENT asserts below: future regressions (an icon
link shipped without a name, an empty heading, a second h1) fail the gate
before deploy. The skip-level audit stays in audit_r114.py as a manual lens.
"""'''

out = src[:start] + new_doc + src[end:]

# 2) r114 a11y asserts before the versions section
r114_block = '''
# --- r114 ship asserts (estate a11y structure: headings + link purpose) ------------------------
import re as _re
_H = _re.compile(r'<h([1-6])[\\s>]', _re.I)
_A = _re.compile(r'<a\\b[^>]*>(.*?)</a>', _re.S | _re.I)
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

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r114_block + anchor, 1)

# 3) no version changes this round: style v57 / i18n v65 pins stay as-is.

# 4) relabel
out = out.replace('print("check_r113: FAILURES:")', 'print("check_r114: FAILURES:")')
out = out.replace('print(f"check_r113: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r114: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r114.py").write_text(out, encoding="utf-8")
print("check_r114.py written:", len(out), "bytes")
