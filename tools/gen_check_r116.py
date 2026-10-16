#!/usr/bin/env python3
"""Generate tools/check_r116.py from check_r115.py: swap the docstring,
inject r116 ship assert (offline.html fixed-toast print hygiene), relabel
output. No version bumps (style v58 / i18n v65 carried — HTML-only ship).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r115.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = '''#!/usr/bin/env python3
"""r116 guards: offline.html fixed-toast print hygiene + id-family audit.

(Carries the full r44-r115 chain, regenerated from check_r115.py; r115 ship
asserts remain in force below.)

SHIP 1 (offline.html, HTML-only — closes the r113 fixed-element audit's last
noted gap): .of-live (the r97 fixed bottom toast, position:fixed z-index 80,
accent background) had NO print rule — same dead-chrome-on-paper class as
r113's checkout overlay: an accent slab repeated on every printed sheet.
Fix: page-local @media print { .of-live { display: none !important; } } in
offline.html's inline style block. No buster bump (page-local CSS).

SHIP 2 (audit, no code change): the r115 bug-class sweep — every [id] in the
estate classified by family (audit via tools scripts): genuine deep-link
targets (section/div/tr/th/h1-h6) are all covered by the anchor-offset rule
since r115; the remaining p/a/span/time/ul ids are JavaScript handles (never
URL targets); main[id] deliberately stays OUT of the rule (a scroll-margin on
#main would push the skip-link landing 159px past the navbar, harming the
WCAG 2.4.1 jump). r115 coverage is COMPLETE; family audit documented here so
future id additions know the contract: URL-target families must join the
anchor-offset rule, JS-hook families must not.
"""'''

out = src[:start] + new_doc + src[end:]

# 2) r116 ship asserts before the versions section
r116_block = '''
# --- r116 ship asserts (offline fixed-toast print hygiene) --------------------------------------
_off = (ROOT / "offline.html").read_text(encoding="utf-8")
ok(_off.count("@media print { .of-live { display: none !important; } }") == 1,
   "offline.html: r116 print rule missing")
ok(_off.count("r116: print hygiene") == 1, "offline.html: r116 comment missing")
ok(_off.count(".of-live {") >= 2, "offline.html: of-live base rule churned")

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r116_block + anchor, 1)

# 3) no version changes this round: style v58 / i18n v65 pins stay as-is.

# 4) relabel
out = out.replace('print("check_r115: FAILURES:")', 'print("check_r116: FAILURES:")')
out = out.replace('print(f"check_r115: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r116: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r116.py").write_text(out, encoding="utf-8")
print("check_r116.py written:", len(out), "bytes")
