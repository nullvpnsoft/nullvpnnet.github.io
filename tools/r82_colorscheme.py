#!/usr/bin/env python3
"""r82: add <meta name="color-scheme" content="light dark"/> after the viewport
meta on every page. style.css already declares color-scheme per theme (:21/:37),
but that only applies after CSS load — the meta lets the browser pick correct
UA styling for native controls (scrollbars, selects, autofill) from first
parse, closing the pre-CSS light-flash window for dark-mode users.
Idempotent; asserts exactly one insertion per file."""
import glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

VP = '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>'
META = '  <meta name="color-scheme" content="light dark"/>'

pages = sorted(glob.glob("*.html"))
assert len(pages) == 15, f"expected 15 pages, found {len(pages)}: {pages}"

for f in pages:
    with open(f, encoding="utf-8") as fh:
        src = fh.read()
    if 'name="color-scheme"' in src:
        assert src.count('name="color-scheme"') == 1, f"{f}: unexpected count"
        print(f"  {f}: already present, skipped")
        continue
    assert src.count(VP) == 1, f"{f}: viewport anchor count != 1"
    out = src.replace(VP, VP + "\n" + META, 1)
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"  {f}: inserted")

# post-assert: every page now carries exactly one
for f in pages:
    with open(f, encoding="utf-8") as fh:
        c = fh.read().count('name="color-scheme"')
    assert c == 1, f"{f}: post-assert failed ({c})"
print(f"OK: color-scheme meta present on all {len(pages)} pages")
