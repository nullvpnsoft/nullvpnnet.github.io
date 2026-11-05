#!/usr/bin/env python3
"""r80 cache-buster: style.css v35 -> v36 across all HTML pages.
Direct-write script (r70 lesson). Single pair, asserted. This round's style.css
delta: global mobile scroll-margin 168 -> 300px (<=768px) — the deliberate
estate-wide fix for targets landing under the 224/269px mobile navbar.
i18n.js untouched (stays v48); sw.js untouched (no precache change — the new
style.css?v=36 is discovered via the homepage regex at SW install)."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OLD = "style.css?v=35"
NEW = "style.css?v=36"

pages = sorted(ROOT.glob("*.html"))
assert len(pages) == 15, f"expected 15 pages, found {len(pages)}"

css = (ROOT / "style.css").read_text(encoding="utf-8")
assert "scroll-margin-top: 300px" in css, "style.css missing the r80 300px rule"
assert OLD not in css and NEW not in css, "buster targets HTML refs only"

changed = 0
for p in pages:
    txt = p.read_text(encoding="utf-8")
    n = txt.count(OLD)
    if n:
        p.write_text(txt.replace(OLD, NEW), encoding="utf-8")
        changed += 1
        print(f"{p.name}: {n} ref(s) bumped")
    else:
        print(f"{p.name}: NO {OLD} FOUND", file=sys.stderr)
        sys.exit(1)

for p in pages:
    txt = p.read_text(encoding="utf-8")
    assert NEW in txt, f"{p.name} missing {NEW}"
    assert OLD not in txt, f"{p.name} still carries {OLD}"

print(f"OK: {changed}/15 pages bumped {OLD} -> {NEW}")
