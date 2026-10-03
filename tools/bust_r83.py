#!/usr/bin/env python3
"""r83 cache-buster: style.css v36 -> v37 across all 15 pages.
Asserts the r83 markers exist in style.css before bumping, and that each
page carried v36 before the rewrite. i18n.js untouched (v49 stays)."""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
style = (root / "style.css").read_text(encoding="utf-8")

markers = [
    "r83: row headers",
    ".data-table tbody th[scope=\"row\"]",
    "r83: accent2 not accent",
]
for m in markers:
    if m not in style:
        sys.exit(f"ABORT: marker missing from style.css: {m}")

pages = sorted(root.glob("*.html"))
assert len(pages) == 15, f"expected 15 pages, found {len(pages)}: {pages}"
changed = 0
for p in pages:
    t = p.read_text(encoding="utf-8")
    assert "style.css?v=36" in t, f"{p.name}: no v36 style reference — abort"
    nt = t.replace("style.css?v=36", "style.css?v=37")
    if nt != t:
        p.write_text(nt, encoding="utf-8")
        changed += 1
print(f"bumped style.css v36 -> v37 on {changed} pages")
# verify
left = sum(1 for p in pages if "style.css?v=36" in p.read_text(encoding="utf-8"))
carry = sum(1 for p in pages if "style.css?v=37" in p.read_text(encoding="utf-8"))
print(f"verify: v36 remaining={left}, v37 carrying={carry}")
assert left == 0 and carry == 15, "buster verification failed"
print("r83 buster: OK")
