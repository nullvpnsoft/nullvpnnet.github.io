#!/usr/bin/env python3
"""Generate tools/check_r113.py from check_r112.py: swap the docstring,
inject r113 ship asserts, update version pins style v56->v57, relabel output.
(i18n stays v65 this round — HTML/CSS-only ship; carried i18n pin unchanged.)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r112.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = '''#!/usr/bin/env python3
"""r113 guards: .checkout-overlay joins the @media print hide list.

(Carries the full r44-r112 chain, regenerated from check_r112.py; r112 ship
asserts remain in force below.)

SHIP (style.css only — print-sheet re-verify round; the estate-wide
reduced-motion lens closed as mature: 4 targeted blocks + the r-era global
nuclear block; the print lens found exactly one real gap):

The checkout overlay (.checkout-overlay, pricing.html) is position:fixed and
was NOT in the master @media print hide list (r50-r93 chain). A visitor who
opens the checkout modal and prints gets a 60%-opacity black slab over the
page — and Chromium repeats fixed boxes on EVERY printed page — with dead
controls underneath it. Interactive dialog chrome can never be meaningful on
paper. Fix: one token added to the existing hide list
(.copy-text-chip, .checkout-overlay { display: none !important; }) inside
the master block. Screen rendering untouched (the rule is print-scoped).

Style buster v56 -> v57 estate-wide (i18n.js stays v65 — no i18n changes).
Guard-chain note carried from r112: version literals live in BOTH the
versions loop AND the carried r108-era per-page pin assert — this gen
updates the versions loop (want_s), the style stale-residue assert
(v55+v56), and leaves the carried i18n pin at v65 (unchanged round).
"""'''

out = src[:start] + new_doc + src[end:]

# 2) r113 ship asserts before the versions section
r113_block = '''
# --- r113 ship asserts (.checkout-overlay print hygiene) ---------------------------------------
_css_r113 = (ROOT / "style.css").read_text(encoding="utf-8")
ok(_css_r113.count(".checkout-overlay") == 1, "style.css: .checkout-overlay token x!=1")
_mp = _css_r113.index("@media print")
_mcab = _css_r113.index("CABINET DESIGN ALIGNMENT")
ok(_css_r113.count(".checkout-overlay", _mp, _mcab) == 1,
   "style.css: .checkout-overlay not inside the master print block")
ok(_css_r113.count(".copy-text-chip,") == 1, "style.css: r113 list-split churned")
ok(_css_r113.count("r113: the checkout dialog is fixed-position") == 1,
   "style.css: r113 comment missing")
ok(_css_r113.count(".checkout-overlay { display: none !important; }") == 1,
   "style.css: r113 hide declaration churned")
_pricing_r113 = (ROOT / "pricing.html").read_text(encoding="utf-8")
ok(_pricing_r113.count('id="checkoutModal" class="checkout-overlay"') == 1,
   "pricing.html: overlay markup churned")

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r113_block + anchor, 1)

# 3) version pins: style v56 -> v57 (style changed; i18n stays v65).
#    r112 lesson: sweep BOTH the versions loop and the carried pin asserts.
out = out.replace('want_i, want_s = "i18n.js?v=65", "style.css?v=56"',
                  'want_i, want_s = "i18n.js?v=65", "style.css?v=57"')
out = out.replace('ok(t.count("style.css?v=55") == 0, f"{page}: stale v55 pin residue")',
                  'ok(t.count("style.css?v=55") == 0 and t.count("style.css?v=56") == 0, '
                  'f"{page}: stale style pin residue")')

# 4) relabel
out = out.replace('print("check_r112: FAILURES:")', 'print("check_r113: FAILURES:")')
out = out.replace('print(f"check_r112: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r113: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r113.py").write_text(out, encoding="utf-8")
print("check_r113.py written:", len(out), "bytes")
