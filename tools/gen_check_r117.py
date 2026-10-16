#!/usr/bin/env python3
"""Generate tools/check_r117.py from check_r116.py: swap the docstring,
inject r117 theme-system contract asserts, relabel output.
No version bumps (style v58 / i18n v65 carried — guard-only ship).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r116.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r117 guards: theme-system contract (estate-wide inline setTheme).

(Carries the full r44-r116 chain, regenerated from check_r116.py; r116 ship
asserts remain in force below.)

SHIP (guard-only round — no site-file changes, no buster bumps):

The index.html deep pass (last unlensed surface) closed with zero functional
findings: theme toggle E2E both directions + persistence + aria-pressed,
language round-trip, back-to-top threshold (strict scrollY > 600), RTL home
layout, share-chip feedback chain. Two probe readings initially looked like
toggle no-ops — both were tool-bridge stale-snapshot artifacts (lesson (f):
read post-click state in a SEPARATE eval; same-eval reads can be stale).

The durable value: the estate's THEME SYSTEM now has gate-enforced contract
asserts (tools/audit_r117.py is the lens that established it):

1. ALL 15 pages: theme init present (localStorage.getItem('theme') x1) —
   the stored/OS theme must apply before first paint on every entry.
2. 13 navbar pages: inline function setTheme( x1 + BOTH buttons wired via
   inline onclick (light x1, dark x1). Parameter names vary across pages
   (t/theme) — asserts are signature-agnostic on purpose.
3. 404.html + offline.html: NO setTheme definition and NO toggle buttons —
   deliberate minimal chrome; they init the theme for background tokens but
   expose no toggle. Asserted ABSENT so a copy-paste re-add fails the gate.
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r117 theme-system asserts before the versions section
r117_block = '''
# --- r117 ship asserts (theme-system contract) --------------------------------------------------
_THEMA_NO_BTNS = ["404.html", "offline.html"]  # deliberate: minimal chrome, init only
for _page in PAGES:
    _t = (ROOT / _page).read_text(encoding="utf-8")
    ok(_t.count("localStorage.getItem('theme')") == 1,
       _page + ": theme init missing or duplicated")
    if _page in _THEMA_NO_BTNS:
        ok(_t.count("function setTheme(") == 0, _page + ": setTheme defined on buttonless page")
        ok(_t.count("onclick=\\"setTheme(") == 0, _page + ": theme button on buttonless page")
    else:
        ok(_t.count("function setTheme(") == 1, _page + ": inline setTheme missing")
        ok(_t.count("onclick=\\"setTheme('light')\\"") == 1, _page + ": light button unwired")
        ok(_t.count("onclick=\\"setTheme('dark')\\"") == 1, _page + ": dark button unwired")
_i18n_r117 = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok(_i18n_r117.count("theme-anim") >= 1, "i18n.js: r43 theme-anim arming missing")

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r117_block + anchor, 1)

# 3) no version changes this round.

# 4) relabel
out = out.replace('print("check_r116: FAILURES:")', 'print("check_r117: FAILURES:")')
out = out.replace('print(f"check_r116: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r117: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r117.py").write_text(out, encoding="utf-8")
print("check_r117.py written:", len(out), "bytes")
