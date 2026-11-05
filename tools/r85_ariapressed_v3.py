#!/usr/bin/env python3
"""r85 patch v3 — finishes the remaining 3 pages (terms/refund/privacy).

v2 fixed 10 pages; the 3 that failed atomically carry a SECOND variant: an
init IIFE that caches the buttons into locals (l/d) and chains setAttribute
on those. v3 generalizes the chain-fix to any receiver:
  A) document.getElementById('themeLight').classList.toggle(...).setAttribute(...)
  B) l.classList.toggle(...).setAttribute(...)
Both become comma-operator statement groups. Pages already fixed by v2 are
verified chain-free and skipped. Every touched page gets inline-script
node --check. Final global assert: no toggle(...).setAttribute chain anywhere.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["success.html", "pricing.html", "how-it-works.html", "faq.html",
         "features.html", "contact.html", "comparison.html", "web3.html",
         "terms.html", "refund.html", "privacy.html", "download.html",
         "index.html"]

# A) receiver = document.getElementById('themeLight'|'themeDark')
CHAIN_A = re.compile(
    r"getElementById\('(themeLight|themeDark)'\)\.classList\.toggle\('active',\s*(\w+)\s*===\s*'(light|dark)'\)\.setAttribute\('aria-pressed',\s*\2\s*===\s*'\3'\)")
# B) receiver = bare identifier directly before .classList (l, d, ...)
CHAIN_B = re.compile(
    r"(?<![\w'.)\]])(\w+)\.classList\.toggle\('active',\s*(\w+)\s*===\s*'(light|dark)'\)\.setAttribute\('aria-pressed',\s*\2\s*===\s*'\3'\)")

RESIDUAL = re.compile(r"toggle\([^)]*\)\.setAttribute")

failures = []

def syntax_check(page, html):
    blocks = re.findall(r"<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>", html, re.S)
    for i, (attrs, body) in enumerate(blocks):
        if "application/ld+json" in attrs:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(body)
            tmp = f.name
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        Path(tmp).unlink()
        if r.returncode != 0:
            failures.append(f"{page} inline script #{i}: SYNTAX ERROR — {r.stderr.strip()[:200]}")

def fix_a(m):
    return (f"getElementById('{m.group(1)}').classList.toggle('active', {m.group(2)} === '{m.group(3)}'), "
            f"document.getElementById('{m.group(1)}').setAttribute('aria-pressed', {m.group(2)} === '{m.group(3)}')")

def fix_b(m):
    return (f"{m.group(1)}.classList.toggle('active', {m.group(2)} === '{m.group(3)}'), "
            f"{m.group(1)}.setAttribute('aria-pressed', {m.group(2)} === '{m.group(3)}')")

for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    n_a = len(CHAIN_A.findall(text))
    n_b = len(CHAIN_B.findall(text))
    if n_a == 0 and n_b == 0:
        if RESIDUAL.search(text):
            failures.append(f"{page}: residual chain not matched by A/B patterns")
        else:
            print(f"  skip {page} (already chain-free)")
        continue
    text = CHAIN_A.sub(fix_a, text)
    text = CHAIN_B.sub(fix_b, text)
    if RESIDUAL.search(text):
        failures.append(f"{page}: residual chain after patch")
        continue
    syntax_check(page, text)
    p.write_text(text, encoding="utf-8")
    print(f"  fixed {page} (A:{n_a} B:{n_b})")

# global final assert across ALL html
for html_file in ROOT.glob("*.html"):
    if RESIDUAL.search(html_file.read_text(encoding="utf-8")):
        failures.append(f"GLOBAL: chain remains in {html_file.name}")

if failures:
    print(f"r85_ariapressed_v3: FAILURES: {failures}")
    sys.exit(1)
print("r85_ariapressed_v3: ESTATE CHAIN-FREE, ALL PATCHED PAGES SYNTAX-CHECKED")
