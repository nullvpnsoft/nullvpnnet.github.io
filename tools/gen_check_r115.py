#!/usr/bin/env python3
"""Generate tools/check_r115.py from check_r114.py: swap the docstring,
inject r115 ship asserts (heading-id anchor clearance), update style pin
v57->v58, widen style stale residue to v57, relabel output. i18n v65 stays.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r114.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = '''#!/usr/bin/env python3
"""r115 guards: heading-id anchor clearance (how-it-works deep links).

(Carries the full r44-r114 chain, regenerated from check_r114.py; r114 a11y
asserts remain in force below.)

SHIP (style.css only — how-it-works behavioral pass found the round's real
bug, the same failure signature r84 recorded for tr/th):

The anchor-offset rule (r41/r80/r84) granted scroll-margin-top clearance to
section[id], div[id], tr[id], th[id] — but r110's 7 deep-linked how-it-works
slugs live on H2 elements, which that selector list misses. Native fragment
re-anchoring gave them scroll-margin 0: #pay-when-ready landed at top -14px
on the live site (measured) while the navbar occupies 0..109px — the heading
is fully behind the sticky navbar on every viewport, on every entry (typed
URL, r82-adjacent shares, history restore). Fix: h1[id]..h6[id] join the
formula (calc(var(--nav-h) + 50px)); every future heading slug inherits the
correct clearance automatically. pricing's #checkoutTitle (h3, inside the
display:none modal) is unaffected. Screen rendering unchanged — scroll-margin
only participates in fragment scrolling.

Style buster v57 -> v58 estate-wide (i18n.js stays v65).
"""'''

out = src[:start] + new_doc + src[end:]

# 2) r115 ship asserts before the versions section
r115_block = '''
# --- r115 ship asserts (heading-id anchor clearance) --------------------------------------------
_css_r115 = (ROOT / "style.css").read_text(encoding="utf-8")
ok(_css_r115.count("h1[id], h2[id], h3[id], h4[id], h5[id], h6[id] { scroll-margin-top") == 1,
   "style.css: r115 heading-id selector missing")
ok(_css_r115.count("calc(var(--nav-h, 120px) + 50px); }") >= 1,
   "style.css: anchor-offset formula churned")
ok(_css_r115.count("r115: heading ids join the formula") == 1,
   "style.css: r115 comment missing")
ok(_css_r115.count("the exact signature the r84 note recorded for tr/th") == 1,
   "style.css: r115 provenance comment truncated")
_hiw_r115 = (ROOT / "how-it-works.html").read_text(encoding="utf-8")
for _slug in ["built-for-difficult-networks", "connection-experience", "three-steps",
              "install-the-app", "tap-connect", "pay-when-ready", "ready-to-connect"]:
    ok(_hiw_r115.count("<h2 id=\\"" + _slug + "\\"") == 1,
       "how-it-works.html: r115 h2 slug churned: " + _slug)

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r115_block + anchor, 1)

# 3) version pins: style v57 -> v58 (style changed; i18n stays v65).
out = out.replace('want_i, want_s = "i18n.js?v=65", "style.css?v=57"',
                  'want_i, want_s = "i18n.js?v=65", "style.css?v=58"')
out = out.replace('ok(t.count("style.css?v=55") == 0 and t.count("style.css?v=56") == 0, '
                  'f"{page}: stale style pin residue")',
                  'ok(t.count("style.css?v=55") == 0 and t.count("style.css?v=56") == 0 '
                  'and t.count("style.css?v=57") == 0, f"{page}: stale style pin residue")')

# 4) relabel
out = out.replace('print("check_r114: FAILURES:")', 'print("check_r115: FAILURES:")')
out = out.replace('print(f"check_r114: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r115: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r115.py").write_text(out, encoding="utf-8")
print("check_r115.py written:", len(out), "bytes")
