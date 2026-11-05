#!/usr/bin/env python3
"""Generate tools/check_r125.py from check_r124.py: swap the docstring,
add the r125 pricing refund-callout gate, relabel output. Buster pins carried
(i18n v68 / style v58 — pricing.html markup only).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r124.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r125 guards: pricing refund callout restored (orphaned-key recovery).

(Carries the full r44-r124 chain, regenerated from check_r124.py; the r124
telegram-rescue gate, r123 HUD-context gate, r122 download-hero hide, r121
locale-bootstrap contract, r118-r120 value-quality gates all remain.)

SHIP (real defect found by the r125 re-lens): pricing.html carried NO
refund-policy copy beyond the footer link. The price.refund.h/p keys — the
owner-verified r3 decision '48h refund rule stated at the pricing page' —
lost their hosting element in a later pricing restructure and stayed
translated x7 but UNUSED ever since (a dead-key pair the r119 audit's
7-entry list missed; r119 scanned key names it already suspected, not the
full T-table against HTML usage). Fix: re-attach the callout as a second
.pricing-note after 'How payment works' — zero new i18n keys, no buster
bump (HTML is network-first), below-the-fold placement so the applyLang
EN->locale swap cannot shift viewport content (CLS verified 0.000 local).
E2E: en renders 'Refund policy' + 48h copy; fa swap renders 'سیاست بازگشت'
+ Persian copy RTL. Guard adds the two data-i18n attrs as byte asserts.

QA this round: re-lens r121 trio (features/comparison/pricing) CLEAN —
features share-chip + 5 id-rows + fa RTL mobile; comparison row-pin
(#row-nologs -> tr.comp-row-pin 6 cells clear of nav) AND hashchange
re-pin (#row-anonpay) both live; pricing plan anchors #plan-annual (110 >
109) + #plan-quarterly hashchange hold. fr full 15-page perf sweep run
post-deploy (r124's '7-locale full-cycle matrix' claim was premature —
es/fr were 7/6-page spot checks; this round closes the fr gap).
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r125 asserts before the r124 block
r125_block = '''
# --- r125 ship asserts (pricing refund callout restored) -------------------------------------------
_pc125 = (ROOT / "pricing.html").read_text(encoding="utf-8")
ok(_pc125.count('data-i18n="price.refund.h"') == 1,
   "pricing.html: price.refund.h not attached (orphaned key must be used exactly once)")
ok(_pc125.count('data-i18n="price.refund.p"') == 1,
   "pricing.html: price.refund.p not attached (orphaned key must be used exactly once)")
ok(_pc125.count("r125: refund assurance restored to the point of purchase") == 1,
   "pricing.html: r125 callout comment missing")
# the callout must be a .pricing-note block (same visual language as howpay)
ok('<div class="pricing-note">\\n        <h3 data-i18n="price.refund.h">' in _pc125,
   "pricing.html: refund callout is not a .pricing-note block")

'''
anchor = "\n# --- r124 ship asserts"
assert anchor in out, "r124 anchor not found"
out = out.replace(anchor, r125_block + anchor, 1)

# 3) relabel
out = out.replace('print("check_r124: FAILURES:")', 'print("check_r125: FAILURES:")')
out = out.replace('print(f"check_r124: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r125: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r125.py").write_text(out, encoding="utf-8")
print("check_r125.py written:", len(out), "bytes")
