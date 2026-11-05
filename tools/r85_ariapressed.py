#!/usr/bin/env python3
"""r85 patch: sync aria-pressed on the theme pair in every setTheme/init path.

The lang buttons already announce pressed state (i18n.js applyLang); the
theme buttons only toggled a visual .active class, so screen readers never
announced which theme is active. This chains setAttribute onto each existing
classList.toggle — zero behaviour change, state now mirrors the class.

Variants in the estate (13 pages carry the pair; 404/offline have none):
  - one-liner setTheme + init IIFE (7 pages): param t, count 2 per page
  - multi-line setTheme + init IIFE (5 pages): param t, count 2 per page
  - index.html: setTheme(theme) -> updateThemeButtons(theme) helper (count 1
    per selector — both call sites route through it)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ONELINE = ["success.html", "pricing.html", "how-it-works.html", "faq.html",
           "features.html", "contact.html", "comparison.html"]
MULTILINE = ["web3.html", "terms.html", "refund.html", "privacy.html",
             "download.html"]
INDEX = ["index.html"]

LIGHT_RE = re.compile(r"toggle\('active',\s*(\w+)\s*===\s*'light'\)")
DARK_RE = re.compile(r"toggle\('active',\s*(\w+)\s*===\s*'dark'\)")

failures = []

def patch(page, expected):
    p = ROOT / page
    text = p.read_text(encoding="utf-8")
    if 'id="themeLight"' not in text:
        failures.append(f"{page}: has setTheme but no themeLight button")
        return
    lights = LIGHT_RE.findall(text)
    darks = DARK_RE.findall(text)
    if len(lights) != expected or len(darks) != expected:
        failures.append(f"{page}: expected {expected} light/dark toggle sites, "
                        f"found {len(lights)}/{len(darks)}")
        return
    params = set(lights) | set(darks)
    if len(params) != 1:
        failures.append(f"{page}: mixed param names {params}")
        return
    var = params.pop()
    new_text = LIGHT_RE.sub(
        f"toggle('active', {var} === 'light').setAttribute('aria-pressed', {var} === 'light')"
        if " === 'light'" in text else "",
        text)
    # safer: deterministic re-sub with spacing preserved from match is complex;
    # use function repl that keeps original inner spacing
    def light_repl(m):
        return f"toggle('active', {m.group(1)} === 'light').setAttribute('aria-pressed', {m.group(1)} === 'light')"
    def dark_repl(m):
        return f"toggle('active', {m.group(1)} === 'dark').setAttribute('aria-pressed', {m.group(1)} === 'dark')"
    new_text = LIGHT_RE.sub(light_repl, text)
    new_text = DARK_RE.sub(dark_repl, new_text)
    if new_text.count("aria-pressed") < expected * 2:
        failures.append(f"{page}: patch did not take (aria-pressed count)")
        return
    p.write_text(new_text, encoding="utf-8")
    print(f"  patched {page} ({expected} site(s) x light+dark)")

for page in ONELINE + MULTILINE:
    patch(page, 2)
for page in INDEX:
    patch(page, 1)

if failures:
    print(f"r85_ariapressed: FAILURES: {failures}")
    sys.exit(1)
print("r85_ariapressed: ALL 13 PAGES PATCHED")
