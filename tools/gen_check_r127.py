#!/usr/bin/env python3
"""Generate tools/check_r127.py from check_r126.py: swap the docstring,
add the r126 dead-key orphan-detector gate (pinned T-table reverse scan),
relabel output. Buster pins carried (i18n v68 / style v58).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r126.py").read_text(encoding="utf-8")

start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r127 guards: dead-key orphan detector (T-table reverse scan, pinned).

(Carries the full r44-r126 chain, regenerated from check_r126.py; the r126
success-card hide, r125 refund callout, r124 telegram-rescue, r123
HUD-context, r122 download-hero hide, r121 locale-bootstrap contract,
r118-r120 value-quality gates all remain in force.)

SHIP (tooling gate for the r125 defect class): scripts/deadkey_scan.py
settle the TRUE dead set — T keys translated x7 but used by NO surface —
by boundary-safe full-name matching of all 529 keys against every HTML
data-i18n attr + every tools/*.js + sw.js + branding.js literal + engine
t() calls. Result: 55 dead keys (r119 documented only 7; the rest are
superseded vocabularies — price.f1-f9/btn.*/monthly/quarterly/annual,
index.prob1-4/trust1-4/h1b/sub, faq.section.*, priv.q6/a6, comp.row.*,
comp.val.*, nav.whynull, refund.more, price.pay.h/p2 etc). Verified: 4
spot-greps + no dynamic key concatenation exists in the engine (t() calls
are full literals). PRUNING stays declined (r119 standing: churn; dead
keys are translated future-proofing). Instead the set is PINNED: any
future edit that orphans a live key (the silent r125 regression — element
removed, last usage of translated content lost) grows the set and FAILS
the gate; reviving a dead key also fails (deliberate changes refresh the
list). Sentinel live asserts guard the scanner itself.

QA this round: es full 15-page sweep — the LAST locale gap — 14/15
CLS 0.000-0.003, LCP 176-416ms (web3 = known bridge artifact): the
7-locale full-cycle perf matrix is now genuinely complete. download.html
re-lens (r122 surface) CLEAN: r122 hide rule live in CSSOM, fa CTA
reveals Persian labels, RELEASE_META dormant, #dl-install present.
\"\"\""""

out = src[:start] + new_doc + src[end:]

r127_block = '''
# --- r127 ship asserts (dead-key orphan detector, pinned set) --------------------------------------
import re as _re
_eng127 = (ROOT / "i18n.js").read_text(encoding="utf-8")
_k127 = _re.findall(r'(?:^|[\\s,])(?:\"([a-z0-9_.]+)\"|([a-z0-9_.]+)):\\s*\\{', _eng127, _re.M)
_keys127 = sorted({a or b for a, b in _k127 if (a or b).count("_") >= 1 or "." in (a or b)})
_keys127 = [k for k in _keys127 if "." in k]
_corpus127 = ""
for _p in list(ROOT.glob("*.html")) + list((ROOT / "tools").glob("*.js")) + [ROOT / "sw.js", ROOT / "branding.js"]:
    if _p.exists():
        _corpus127 += _p.read_text(encoding="utf-8", errors="replace")
_dead127 = []
for _k in _keys127:
    _uses = len(_re.findall(_re.escape(_k) + r'(?![a-z0-9_.])', _corpus127))
    _defh = len(_re.findall(_re.escape(_k) + r'"\\s*:\\s*\\{', _eng127)) + len(_re.findall(r'(?<![\\w"])' + _re.escape(_k) + r'\\s*:\\s*\\{', _eng127))
    _extra = len(_re.findall(_re.escape(_k) + r'(?![a-z0-9_])', _eng127)) - _defh
    if _uses == 0 and _extra <= 0:
        _dead127.append(_k)
_EXPECTED_DEAD = frozenset([
    'comp.hero.badge', 'comp.hero.h1', 'comp.hero.lead', 'comp.row.restrictive',
    'comp.row.strictnat', 'comp.table.nullvpn', 'comp.val.inconsistent', 'comp.val.unavailable',
    'faq.section.access', 'faq.section.how', 'faq.section.privacy', 'faq.section.setup',
    'index.badge', 'index.btn.compare', 'index.btn.get', 'index.btn.how',
    'index.cta.also', 'index.diff.h', 'index.feat.more', 'index.h1a',
    'index.h1b', 'index.prob.h', 'index.prob1', 'index.prob2',
    'index.prob3', 'index.prob4', 'index.sp', 'index.sub',
    'index.trust1', 'index.trust2', 'index.trust3', 'index.trust4',
    'nav.whynull', 'price.annual', 'price.billed.mo', 'price.btn.an',
    'price.btn.mo', 'price.btn.qt', 'price.f1', 'price.f2',
    'price.f3', 'price.f4', 'price.f5', 'price.f6',
    'price.f7', 'price.f8', 'price.f9', 'price.monthly',
    'price.pay.h', 'price.pay.p', 'price.pay.p2', 'price.quarterly',
    'priv.a6', 'priv.q6', 'refund.more',
])
ok(set(_dead127) == _EXPECTED_DEAD,
   "dead-key set drifted: orphaned=" + ",".join(sorted(set(_dead127) - _EXPECTED_DEAD)) +
   " revived=" + ",".join(sorted(_EXPECTED_DEAD - set(_dead127))) +
   " (orphaned = element removed without re-homing its i18n keys; revived = refresh the pin)")
for _sent in ["nav.download", "share.btn", "price.refund.p", "faq.cat.all", "a11y.skip"]:
    ok(_sent not in _dead127, "sentinel live key misclassified dead: " + _sent)

'''
anchor = "\n# --- r126 ship asserts"
assert anchor in out, "r126 anchor not found"
out = out.replace(anchor, r127_block + anchor, 1)

out = out.replace('print("check_r126: FAILURES:")', 'print("check_r127: FAILURES:")')
out = out.replace('print(f"check_r126: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r127: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r127.py").write_text(out, encoding="utf-8")
print("check_r127.py written:", len(out), "bytes")
