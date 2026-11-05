#!/usr/bin/env python3
"""Generate check_r128.py: extends the r44-r127 chain with the r128 gate.

r128 (Task 127): legal-trio nav canonicalization. privacy/terms/refund
navs lacked the .nav-top-row wrapper every other content page has, so
.nav-inner (column flex) stacked 4 children as blocks -> a 164px navbar
(vs 108px canonical) and a dead RTL row-reverse rule; their nav-links
were the legacy generation (Home / t.me Support / raw mailto). The fix
wraps the top row, standardizes the 6-link set, and moves the mailto pin
from 16 to 13 across the carried chain (r104-r127 sections edited).

Teeth plan (mutation-tested after generation):
  M1: strip .nav-top-row wrapper on a legal page -> wrapper assert fires.
  M2: re-inject legacy nav.home link -> block-scan assert fires.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "check_r127.py"
DST = ROOT / "tools" / "check_r128.py"

R128 = '''

# --- r128: legal-trio nav canonicalization (Task 127 re-lens catch) -----------
# privacy/terms/refund now carry the canonical nav: .nav-top-row wrapper
# (logo + actions + controls in one flex row, RTL row-reverse aware) plus the
# standard 6-link nav-links set used by every other content page. Legacy
# markers (nav.home link, t.me Support, raw mailto) are banned from the nav
# block; they remain available via the footer social row, contact.html,
# llms.txt and security.txt. mailto pin moved 16 -> 13 in the carried chain.
LEGAL = ["privacy.html", "terms.html", "refund.html"]
STD6 = ["nav.features", "nav.how", "nav.compare", "nav.pricing", "nav.faq", "nav.contact"]
for page in LEGAL:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count('<div class="nav-inner">\\n      <div class="nav-top-row">') == 1,
       page + ": nav-top-row wrapper missing (r128 canonical nav)")
    ok(t.count("r128: legal-trio nav canonicalization") == 1,
       page + ": r128 comment marker missing")
    i = t.index('<div class="nav-inner">')
    j = t.index("</nav>", i)
    block = t[i:j]
    for k in STD6:
        # nav.contact is x2 by design (nav-actions CTA + nav-links item);
        # the other five live only in nav-links.
        want = 2 if k == "nav.contact" else 1
        ok(block.count('data-i18n="' + k + '"') == want,
           page + ": standard nav key " + k + " != x" + str(want) + " in nav block")
    ok(block.count("nav.home") == 0, page + ": legacy nav.home still in nav block")
    ok(block.count("t.me") == 0, page + ": legacy t.me link still in nav block")
    ok(block.count("mailto") == 0, page + ": legacy mailto still in nav block")
# Uniformity: every other keyed nav-links page (index has an unkeyed set;
# 404/offline are chrome-less) carries the SAME 6-key set inside its nav block.
KEYED = [p for p in PAGES if p not in LEGAL and p not in ("index.html", "404.html", "offline.html")]
for page in KEYED:
    t = (ROOT / page).read_text(encoding="utf-8")
    i = t.index('<div class="nav-inner">')
    j = t.index("</nav>", i)
    block = t[i:j]
    for k in STD6:
        want = 2 if k == "nav.contact" else 1
        ok(block.count('data-i18n="' + k + '"') == want,
           page + ": nav uniformity — " + k + " != x" + str(want) + " in nav block")

if errs:
'''

src = SRC.read_text(encoding="utf-8")
src = src.replace('check_r127: FAILURES:', 'check_r128: FAILURES:')
src = src.replace('print(f"check_r127: ALL GREEN', 'print(f"check_r128: ALL GREEN')
# Splice our section before the final 'if errs:' so the asserts join the chain tail.
idx = src.rindex("\nif errs:")
out = src[:idx] + R128[: R128.rindex("\nif errs:")] + "\n" + src[idx + 1:]
DST.write_text(out, encoding="utf-8")
print(f"check_r128.py written ({len(out)} bytes) from check_r127.py + r128 section")
