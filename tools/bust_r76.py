#!/usr/bin/env python3
"""r76 cache-buster: i18n.js v45 -> v46 across all HTML pages.
Direct-write script (r70 lesson: no template chains, no string-replace
inheritance from previous rounds' scripts). Single pair, asserted."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OLD = "i18n.js?v=45"
NEW = "i18n.js?v=46"

# every HTML file in the repo root participates (15 pages, r76 audit)
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
        # every page must carry exactly one i18n reference; a miss here means
        # the page drifted from the estate pattern -> fail loudly, not silently
        print(f"{p.name}: NO {OLD} FOUND", file=sys.stderr)
        sys.exit(1)

# post-assertions: new pair present, old pair extinct anywhere
for p in pages:
    txt = p.read_text(encoding="utf-8")
    assert NEW in txt, f"{p.name} missing {NEW}"
    assert OLD not in txt, f"{p.name} still carries {OLD}"

leftover = [p.name for p in ROOT.glob("*.html") if OLD in p.read_text(encoding="utf-8")]
assert not leftover, f"old buster survives in {leftover}"

print(f"OK: {changed}/15 pages bumped {OLD} -> {NEW}")
