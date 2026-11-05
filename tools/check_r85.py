#!/usr/bin/env python3
"""r85 guard: keyboard-scrollable regions + focus-ring contrast + theme state.

Asserts:
  1. i18n.js carries the 3 new a11y.tbl.* keys in all 7 locales.
  2. The 3 overflow wrappers are focusable labelled regions
     (tabindex="0" + role="region" + data-i18n-aria) in their pages.
  3. style.css global focus ring is 2px var(--text) (WCAG 1.4.11 — the old
     rgba(accent,.55) blended to ~1.98:1 light / 3.75:1 dark; light FAILED),
     the dark alpha override is GONE, and the @supports-not fallback matches.
  4. Every page with a theme pair syncs aria-pressed (13 pages), and NO
     `toggle(...).setAttribute` chain exists anywhere (the v1 patch bug —
     classList.toggle returns a boolean; chaining throws at runtime).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []
LOCALES = ["en", "ru", "fa", "ar", "es", "ne", "fr"]

def check(name, cond, detail=""):
    if cond:
        print(f"  PASS  {name}")
    else:
        failures.append(name)
        print(f"  FAIL  {name}  {detail}")

i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
style = (ROOT / "style.css").read_text(encoding="utf-8")

print("== 1. i18n keys ==")
for key in ["a11y.tbl.features", "a11y.tbl.comparison", "a11y.tbl.privacy"]:
    m = re.search(r'"' + key + r'":\s*\{(.*?)\},\s*\n\s*"', i18n, re.S)
    body = m.group(1) if m else ""
    missing = [loc for loc in LOCALES if not re.search(r'\b' + loc + r'\s*:', body)]
    check(f"{key} x7 locales", m and not missing, f"missing {missing}")

print("== 2. keyboard-scrollable regions ==")
wrappers = [
    ("features.html", "feat-table-wrap", "a11y.tbl.features"),
    ("comparison.html", "comp-table-wrap", "a11y.tbl.comparison"),
    ("privacy.html", "tbl-scroll", "a11y.tbl.privacy"),
]
for page, cls, key in wrappers:
    text = (ROOT / page).read_text(encoding="utf-8")
    pat = re.compile(r'<div class="' + cls + r'" tabindex="0" role="region" aria-label="[^"]+" data-i18n-aria="' + key + r'">')
    check(f"{page} .{cls} focusable labelled region", bool(pat.search(text)))

print("== 3. focus ring ==")
check("global ring 2px var(--text)",
      ":where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {\n  outline: 2px solid var(--text);\n  outline-offset: 2px;\n}" in style)
check("dark alpha override removed", "[data-theme=\"dark\"] :where(a, button" not in style)
check("@supports-not fallback recolored",
      re.search(r"@supports not selector\(:focus-visible\) \{[^}]*outline: 2px solid var\(--text\);", style, re.S) is not None)
check("r85 measured-numbers comment", "failing WCAG 1.4.11" in style)

print("== 4. theme aria-pressed (13 pages) ==")
chain = re.compile(r"toggle\([^)]*\)\.setAttribute")
for html_file in sorted(ROOT.glob("*.html")):
    text = html_file.read_text(encoding="utf-8")
    has_pair = 'id="themeLight"' in text
    n_pressed = text.count("aria-pressed")
    if has_pair:
        check(f"{html_file.name} syncs aria-pressed", n_pressed >= 2, f"count={n_pressed}")
    else:
        check(f"{html_file.name} no theme pair", n_pressed == 0 or html_file.name in ("404.html", "offline.html"), f"count={n_pressed}")
    if chain.search(text):
        check(f"{html_file.name} no toggle-setAttribute chain", False)
    else:
        print(f"  PASS  {html_file.name} chain-free")

print()
if failures:
    print(f"check_r85: {len(failures)} FAILURE(S): {failures}")
    sys.exit(1)
print("check_r85: ALL PASS")
