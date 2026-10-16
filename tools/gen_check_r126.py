#!/usr/bin/env python3
"""Generate tools/check_r126.py from check_r125.py: swap the docstring,
add the r126 success-card nv-l hide gate, relabel output. Buster pins carried
(i18n v68 / style v58 — success.html inline rule only).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r125.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r126 guards: success-card nv-l hide (CLS ritual, round 3).

(Carries the full r44-r125 chain, regenerated from check_r125.py; the r125
pricing refund callout, r124 telegram-rescue, r123 HUD-context, r122
download-hero hide, r121 locale-bootstrap contract, r118-r120 value-quality
gates all remain in force.)

SHIP (same defect family as r121/r122, third member): the fr full 15-page
perf sweep (this round, post-deploy) caught success.html CLS 0.026 on a
live warm load — the ONLY reading above the 0.000-0.004 noise floor across
the now-complete 7-locale full-cycle matrix. Mechanism: the r121 nv-l guard
hides only .nav-inner (r122 added download's .dh-cta/.dh-note); success.html's
centered .success-card (h1/subtitle/details/notes — min-height:60vh flex
child, so ANY text re-wrap re-centers every card child) was unprotected,
and the EN->locale applyLang swap re-wrapped it when a slow resource let
first paint win the race (1/10 in the hunt loop — intermittent like r122's
2/5, but the mechanism family is proven and fr strings are the longest).

Fix: success.html inline rule extended to
html.nv-l .nav-inner{visibility:hidden}html.nv-l .success-card{visibility:hidden}
— layout-preserving, revealed by the same applyLang nv-l removal (2s
failsafe unchanged). LCP IMPROVED (136-144ms vs ~312ms pre-fix: the EN
pre-swap text can no longer be the LCP candidate; LCP lands on the revealed
localized text). en path untouched (no nv-l class, card visible at once).
Local E2E: fr x4 CLS 0.000 + 'Paiement réussi !' post-reveal; en immediate.
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r126 asserts before the r125 block
r126_block = '''
# --- r126 ship asserts (success-card nv-l hide) ----------------------------------------------------
_sc = (ROOT / "success.html").read_text(encoding="utf-8")
ok(_sc.count('<style>html.nv-l .nav-inner{visibility:hidden}html.nv-l .success-card{visibility:hidden}</style>') == 1,
   "success.html: r126 extended card-hide rule missing (nav-inner + success-card)")
for _p in PAGES:
    if _p == "success.html":
        continue
    _t126 = (ROOT / _p).read_text(encoding="utf-8")
    ok(_t126.count("html.nv-l .success-card") == 0,
       _p + ": success-only card-hide rule leaked onto " + _p)

'''
anchor = "\n# --- r125 ship asserts"
assert anchor in out, "r125 anchor not found"
out = out.replace(anchor, r126_block + anchor, 1)

# 3) relabel
out = out.replace('print("check_r125: FAILURES:")', 'print("check_r126: FAILURES:")')
out = out.replace('print(f"check_r125: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r126: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r126.py").write_text(out, encoding="utf-8")
print("check_r126.py written:", len(out), "bytes")
