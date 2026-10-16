#!/usr/bin/env python3
"""r79 cache-buster: i18n.js v47 -> v48 across all HTML pages.
Direct-write script (r70 lesson). Single pair, asserted. This round's i18n
delta: new key nf.suggest (404 rescue banner, x7 locales) -> 517 -> 518 keys."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OLD = "i18n.js?v=47"
NEW = "i18n.js?v=48"

pages = sorted(ROOT.glob("*.html"))
assert len(pages) == 15, f"expected 15 pages, found {len(pages)}"

# i18n.js must carry the round's new key before any page is bumped
i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
assert '"nf.suggest"' in i18n, "i18n.js missing nf.suggest key"
assert OLD not in i18n and NEW not in i18n, "buster targets HTML refs only"

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
