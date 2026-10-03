#!/usr/bin/env python3
"""r77 cache-buster: i18n.js v46 -> v47 across all HTML pages.
Direct-write script (r70 lesson). Single pair, asserted."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OLD = "i18n.js?v=46"
NEW = "i18n.js?v=47"

pages = sorted(ROOT.glob("*.html"))
assert len(pages) == 15, f"expected 15 pages, found {len(pages)}"

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
