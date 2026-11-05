#!/usr/bin/env python3
"""Generate check_r132.py: extends the r44-r128 chain with the r132 gate.

r132 (Task 132 ship): pre-paint install reveal + 63-dead-key prune.
  (a) r131 OWNER-CALL option (b) implemented, hardened: download.html head
      boot adds html.bip-ready pre-parse when localStorage 'nv_bip' is set
      and the view is not standalone; style.css .bip-ready #dl-install
      overrides the UA [hidden] rule so the CTA occupies its slot at first
      paint (r131 root cause — post-paint .dh-cta re-wrap, 0.010 CLS every
      repeat visit — structurally impossible). i18n.js section 9 owns the
      flag lifecycle: BIP sets nv_bip; appinstalled / dead-click / 4s
      no-BIP timeout / standalone launch clear it (nvBipArrived guards the
      timeout against consuming a clicked prompt).
  (b) r127 OWNER-CALL dead-key prune: 63 keys removed from T (529 -> 466 x7,
      usages 803 unchanged). Conservative criterion: a key is dead only if
      its name appears NOWHERE as a quoted literal in any shipped file —
      rescued families (success.plan.*, a11y.copyfail, share.done/answer/
      clause, anchor chips) are asserted ALIVE as tripwires.
  (c) busters: style v58 -> v59, i18n v68 -> v69 (carried pins moved).

Teeth plan (mutation-tested after generation):
  M1: neutralize .bip-ready rule in style.css -> override-rule assert fires.
  M2: re-inject pruned key literal into i18n.js -> tripwire + count fires.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "check_r128.py"
DST = ROOT / "tools" / "check_r132.py"

R132 = '''

# --- r132: pre-paint install reveal + 63-dead-key prune (Task 132 ship) -------
_i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
# (a) install CLS fix — boot guard + CSS override + flag lifecycle
_dl = (ROOT / "download.html").read_text(encoding="utf-8")
ok(_dl.count("r132: pre-paint install reveal") == 1, "download.html: r132 boot marker missing")
ok(_dl.count('localStorage.getItem("nv_bip")') == 1, "download.html: nv_bip flag read missing")
ok(_dl.count('classList.add("bip-ready")') == 1, "download.html: bip-ready add missing")
ok(_dl.count("(display-mode: standalone)") == 1, "download.html: standalone guard missing")
ok(_i18n.count("r132: zero-CLS repeat views") == 1, "i18n.js: r132 section-9 marker missing")
ok(_i18n.count("localStorage.setItem('nv_bip', '1')") == 1, "i18n.js: nv_bip setItem x!=1")
ok(_i18n.count("localStorage.removeItem('nv_bip')") == 1, "i18n.js: nv_bip removeItem x!=1")
ok(_i18n.count("localStorage.getItem('nv_bip')") == 1, "i18n.js: nv_bip getItem x!=1")
ok(_i18n.count("nvBipArrived") == 4, "i18n.js: nvBipArrived lifecycle x!=4 (decl+set+read+comment)")
ok(_i18n.count("'bip-ready'") == 1, "i18n.js: bip-ready class remove x!=1")
ok(css.count(".bip-ready #dl-install { display: inline-block !important; }") == 1,
   "style.css: bip-ready override rule missing (must carry !important vs the r45 author guard)")
ok(css.count(".bip-ready #dl-install,") == 1 and
   css.count("#dl-install { display: none !important; }") == 1,
   "style.css: print hide for #dl-install missing (variant selector outranked reveal rule)")
ok(css.count("r132: pre-paint install reveal") == 1, "style.css: r132 marker missing")
# (b) dead-key prune tripwire: 63 pruned names stay out of every shipped file
_DEAD63 = ["nav.whynull", "nav.cta", "index.badge", "index.h1a", "index.h1b",
    "index.sub", "index.btn.get", "index.btn.compare", "index.btn.how",
    "index.trust1", "index.trust2", "index.trust3", "index.trust4", "index.sp",
    "index.prob.h", "index.prob1", "index.prob2", "index.prob3", "index.prob4",
    "index.diff.h", "index.feat.more", "index.cta.also",
    "tech.h", "tech.1", "tech.2", "tech.3", "tech.4", "tech.5", "tech.6",
    "price.monthly", "price.quarterly", "price.annual", "price.billed.mo",
    "price.f1", "price.f2", "price.f3", "price.f4", "price.f5", "price.f6",
    "price.f7", "price.f8", "price.f9", "price.btn.mo", "price.btn.qt",
    "price.btn.an", "price.pay.h", "price.pay.p", "price.pay.p2",
    "faq.section.how", "faq.section.privacy", "faq.section.setup",
    "faq.section.access", "priv.q6", "priv.a6", "comp.hero.badge",
    "comp.hero.h1", "comp.hero.lead", "comp.table.nullvpn",
    "comp.row.restrictive", "comp.row.strictnat", "comp.val.unavailable",
    "comp.val.inconsistent", "refund.more"]
_PAGE_SRC = {p: (ROOT / p).read_text(encoding="utf-8") for p in PAGES}
for _k in _DEAD63:
    ok(('"' + _k + '"') not in _i18n, "i18n.js: pruned key re-introduced: " + _k)
    for _p, _t in _PAGE_SRC.items():
        ok(('"' + _k + '"') not in _t and ("'" + _k + "'") not in _t,
           _p + ": pruned key referenced: " + _k)
# (c) rescued dynamic families MUST remain in T (r128-E2E-proven contracts)
for _k in ("success.plan.monthly", "success.plan.quarterly", "success.plan.annual",
           "a11y.copyfail", "share.done", "share.answer", "share.clause",
           "faq.anchor.label", "faq.anchor.clause", "comp.anchor.row",
           "pricing.anchor.plan", "feat.anchor.row"):
    ok(_k in _T, "i18n.js: rescued dynamic key missing from T: " + _k)
ok(len(_T) == 466, f"i18n.js: key count drifted (got {len(_T)}, expected 466)")

if errs:
'''

src = SRC.read_text(encoding="utf-8")
src = src.replace("all 529 keys against every HTML", "all 466 keys against every HTML")
src = src.replace('ok(len(_T) >= 500, f"i18n.js: T parse collapsed (got {len(_T)} keys, expected ~529)")',
                  'ok(len(_T) >= 450, f"i18n.js: T parse collapsed (got {len(_T)} keys, expected ~466)")')
src = src.replace('ok(_nf.count("i18n.js?v=68") == 1, "404.html: i18n v68 pin x!=1")',
                  'ok(_nf.count("i18n.js?v=69") == 1, "404.html: i18n v69 pin x!=1")')
src = src.replace('want_i, want_s = "i18n.js?v=68", "style.css?v=58"',
                  'want_i, want_s = "i18n.js?v=69", "style.css?v=59"')
src = src.replace('ok(t.count("style.css?v=55") == 0 and t.count("style.css?v=56") == 0 and t.count("style.css?v=57") == 0, f"{page}: stale style pin residue")',
                  'ok(t.count("style.css?v=55") == 0 and t.count("style.css?v=56") == 0 and t.count("style.css?v=57") == 0 and t.count("style.css?v=58") == 0, f"{page}: stale style pin residue")')
src = src.replace('ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0 and t.count("i18n.js?v=65") == 0 and t.count("i18n.js?v=66") == 0 and t.count("i18n.js?v=67") == 0, f"{page}: stale i18n pin residue")',
                  'ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0 and t.count("i18n.js?v=65") == 0 and t.count("i18n.js?v=66") == 0 and t.count("i18n.js?v=67") == 0 and t.count("i18n.js?v=68") == 0, f"{page}: stale i18n pin residue")')
# r127-carried brand allowlist: comp.table.nullvpn pruned -> 16 -> 12 block,
# 35 -> 31 pairs total.
src = src.replace('''for _bk in ("comp.table.expressvpn", "comp.table.nordvpn",
            "comp.table.nullvpn", "comp.table.protonvpn"):
    for _bl in _R118_LOCS:
        _R118_BRAND_ALLOW.add((_bk, _bl))          # 16: comparison VPN brand names, Latin by design''',
'''for _bk in ("comp.table.expressvpn", "comp.table.nordvpn",
            "comp.table.protonvpn"):
    for _bl in _R118_LOCS:
        _R118_BRAND_ALLOW.add((_bk, _bl))          # 12: comparison VPN brand names, Latin by design (r132: comp.table.nullvpn pruned)''')
src = src.replace('# 35 (key, locale) pairs total — exact r118-audited clean state;',
                  '# 31 (key, locale) pairs total (r132: -4 comp.table.nullvpn pairs) — r118-audited clean state;')
src = src.replace('expected 35 pinned pairs)', 'expected 31 pinned pairs)')
# r127-carried dead-key pin: all 55 pinned-dead keys are now PRUNED from T —
# expected dead set becomes EMPTY; the live recomputation stays as the
# future-orphan tripwire, and the r132 section's _DEAD63 bans the names.
src = src.replace('''_EXPECTED_DEAD = frozenset([
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
])''',
'''# r132: the r127 pinned dead-set (55 keys) is fully pruned from T — expected
# dead set is now EMPTY; the recomputation below remains as the future-orphan
# tripwire (element removed without re-homing its i18n keys), and the r132
# section's _DEAD63 tripwire bans the pruned names outright. (The r127 pin's
# tech.*/nav.cta exclusions were detector substring collisions with
# how.tech.* — the conservative full-name r132 audit proved them dead too.)
_EXPECTED_DEAD = frozenset()''')
src = src.replace('check_r128: FAILURES:', 'check_r132: FAILURES:')
src = src.replace('print(f"check_r128: ALL GREEN', 'print(f"check_r132: ALL GREEN')
idx = src.rindex("\nif errs:")
out = src[:idx] + R132[: R132.rindex("\nif errs:")] + "\n" + src[idx + 1:]
DST.write_text(out, encoding="utf-8")
print(f"check_r132.py written ({len(out)} bytes) from check_r128.py + r132 section")
