#!/usr/bin/env python3
"""r80 cache-buster (2/2): i18n.js v48 -> v49 across all HTML pages.
Direct-write script (r70 lesson). Single pair, asserted. This round's i18n.js
delta: section 10b — measures the real navbar height into --nav-h via
ResizeObserver (consumed by style.css's calc() scroll-margin rule)."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OLD = "i18n.js?v=48"
NEW = "i18n.js?v=49"

pages = sorted(ROOT.glob("*.html"))
assert len(pages) == 15, f"expected 15 pages, found {len(pages)}"

src = (ROOT / "i18n.js").read_text(encoding="utf-8")
assert "10b) Exact anchor offset" in src, "i18n.js missing section 10b"
assert "--nav-h" in src, "i18n.js missing --nav-h setter"
assert OLD not in src and NEW not in src, "buster targets HTML refs only"

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
