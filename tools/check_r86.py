#!/usr/bin/env python3
"""r86 guard: permalink chips on pricing plans + features rows.

Asserts:
  1. i18n.js carries pricing.anchor.plan + feat.anchor.row in all 7 locales.
  2. The r86 engine exists in i18n.js (shared makePermalinkChip helper, both
     surface selectors, both aria keys, idempotency checks) and sits INSIDE
     updateFeatureTexts but OUTSIDE the comp-table if-block (a first-draft
     misplacement put it inside — chips would only have built on comparison).
  3. The r68 comparison row-anchor engine is untouched (regression).
  4. Page-local h3 flex rules (FAQ mirror) present in pricing + features.
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
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
features = (ROOT / "features.html").read_text(encoding="utf-8")

print("== 1. i18n keys ==")
for key in ["pricing.anchor.plan", "feat.anchor.row"]:
    m = re.search(r'"' + key + r'":\s*\{(.*?)\n  \},', i18n, re.S)
    body = m.group(1) if m else ""
    missing = [loc for loc in LOCALES if not re.search(r'\b' + loc + r'\s*:', body)]
    check(f"{key} x7 locales", m and not missing, f"missing {missing}")

print("== 2. r86 engine ==")
check("shared chip helper", "const makePermalinkChip = (host, id, ariaKey) => {" in i18n)
check("pricing surface selector", "document.querySelectorAll('.pricing-card[id] h3')" in i18n)
check("features surface selector", "document.querySelectorAll('.feat-body h3')" in i18n)
check("idempotency: pricing", "if (h3.querySelector('.faq-anchor')) return;" in i18n)
check("uses canonical + fragment", "((can && can.href) || (location.origin + location.pathname)) + '#' + id" in i18n)
check("clipboard doctrine", "navigator.clipboard.writeText(url)" in i18n)
check("announce via copyLive", "live.textContent = t('a11y.copied', getLang());" in i18n)

# structural: engine must be inside updateFeatureTexts, outside comp-if
lines = i18n.split('\n')
def find(pred, frm=0):
    for i, l in enumerate(lines[frm:], frm + 1):
        if pred(l):
            return i
    return None
uf_start = find(lambda l: l.strip().startswith('function updateFeatureTexts'))
uf_depth, uf_close = 0, None
for i in range(uf_start - 1, len(lines)):
    uf_depth += lines[i].count('{') - lines[i].count('}')
    if uf_depth == 0:
        uf_close = i + 1
        break
r86_line = find(lambda l: '// r86: pricing plan + features row permalink chips' in l)
comp_if = find(lambda l: "if (document.querySelector('.comp-table-wrap table')) {" in l)
check("engine inside updateFeatureTexts", uf_start < r86_line < uf_close, f"uf {uf_start}-{uf_close}, r86 at {r86_line}")
check("engine outside comp-if (before it)", r86_line < comp_if, f"comp-if at {comp_if}")

print("== 3. r68 comparison engine regression ==")
check("row-anchor engine intact", "compT2.querySelectorAll('tbody tr[id]')" in i18n)
check("row-anchor class intact", "a.className = 'row-anchor';" in i18n)

print("== 4. page-local flex (FAQ mirror) ==")
check("features h3 flex", "justify-content: space-between;" in features and "r86: mirrors the FAQ h3 flex" in features)
check("pricing h3 flex", ".pricing-card h3{display:flex;align-items:baseline;justify-content:space-between;gap:12px;}" in pricing)

print()
if failures:
    print(f"check_r86: {len(failures)} FAILURE(S): {failures}")
    sys.exit(1)
print("check_r86: ALL PASS")
