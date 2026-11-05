#!/usr/bin/env python3
"""r85 patch v2 — FIXES the v1 chaining bug.

v1 chained .setAttribute() onto classList.toggle() — but toggle() returns a
BOOLEAN, not the element, so every patched setTheme/init would have thrown
TypeError at runtime. v2 rewrites the already-patched (broken) chain into a
comma-operator statement group (valid JS, no behaviour change):

  el.classList.toggle('active', v === 'light').setAttribute(...)   // BROKEN
  el.classList.toggle('active', v === 'light'),
    document.getElementById('themeLight').setAttribute(...)        // FIXED

Also node --check's every inline <script> block of every patched page.
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

BROKEN = re.compile(
    r"getElementById\('themeLight'\)\.classList\.toggle\('active',\s*(\w+)\s*===\s*'light'\)\.setAttribute\('aria-pressed',\s*\1\s*===\s*'light'\)")
BROKEN_D = re.compile(
    r"getElementById\('themeDark'\)\.classList\.toggle\('active',\s*(\w+)\s*===\s*'dark'\)\.setAttribute\('aria-pressed',\s*\1\s*===\s*'dark'\)")

failures = []

def syntax_check(page, html):
    """node --check every inline script block (skip src=, ld+json)."""
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

for page in PAGES:
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    n_light = len(BROKEN.findall(text))
    n_dark = len(BROKEN_D.findall(text))
    if n_light == 0 and n_dark == 0:
        failures.append(f"{page}: no v1 chain found — state unexpected")
        continue
    if n_light != n_dark:
        failures.append(f"{page}: light/dark chain mismatch {n_light}/{n_dark}")
        continue

    def fix(m, theme):
        v = m.group(1)
        tid = "themeLight" if theme == "light" else "themeDark"
        return (f"getElementById('{tid}').classList.toggle('active', {v} === '{theme}'), "
                f"document.getElementById('{tid}').setAttribute('aria-pressed', {v} === '{theme}')")

    text = BROKEN.sub(lambda m: fix(m, "light"), text)
    text = BROKEN_D.sub(lambda m: fix(m, "dark"), text)

    # verify: no chained toggle-onto-setAttribute remains anywhere
    if re.search(r"toggle\([^)]*\)\.setAttribute", text):
        failures.append(f"{page}: chained setAttribute still present")
        continue
    syntax_check(page, text)
    p.write_text(text, encoding="utf-8")
    print(f"  fixed {page} ({n_light} site(s))")

if failures:
    print(f"r85_ariapressed_v2: FAILURES: {failures}")
    sys.exit(1)
print("r85_ariapressed_v2: ALL 13 PAGES FIXED + SYNTAX CHECKED")
