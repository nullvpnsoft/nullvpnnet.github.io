#!/usr/bin/env python3
"""Generate tools/check_r123.py from check_r122.py: swap the docstring,
add the r123 HUD-context gate, bump buster pins v67->v68, relabel output.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r122.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r123 guards: perf-HUD context segment + i18n buster v68.

(Carries the full r44-r122 chain, regenerated from check_r122.py; the r122
download-hero hide, r121 locale-bootstrap + navbar-reveal contract, r118
value-quality, r119 Latin-locale and r120 sibling-identity gates all remain
in force.)

SHIP (diagnostics): the per-round ?perf=1 estate ritual (this round: ru 15
pages + fr/es spot checks — locale rotation fa r121/122, ar/ne r122, ru/fr/es
r123 COMPLETE, estate CLS 0.000-0.004) again hit the two probe-triage
frictions r122 recorded: the HUD did not self-identify its RESOLVED locale
(carried-storage ambiguity cost a re-probe on faq) nor its ORIGIN (the web3
bridge redirect to tonviewer.com poisoned readings and needed title/origin
triage). Fix: HUD textContent gains a context segment —
' | ' + resolved lang + '/' + dir + ' @ ' + host + '/' + page —
maintainer-diagnostics output (still ?perf=1-gated, aria-hidden, numeric/
locale-independent by the same r70 policy). Redirect probes now self-expose:
host flips to tonviewer.com in the chip. i18n buster v67 -> v68 (cache-first
asset; cached engines render the shorter HUD line forever).

Re-lens rotation this round: success.html (oldest, r116) and faq.html
(r119) — all contracts re-verified live (r102 truncation, r77 chip gating,
plan-key mapping, faq locale-scoped filter + mark, switch-resets-filter,
#faq-N anchor clearance, JSON-LD FAQPage 11 Q&As). Zero site defects found;
the only site change is the HUD context segment + buster.
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r123 asserts before the versions section
r123_block = '''
# --- r123 ship asserts (perf-HUD context segment) -------------------------------------------------
_eng = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok(_eng.count("' | ' + (document.documentElement.lang || '?') + '/' + (document.documentElement.dir || '?') +") == 1,
   "i18n.js: r123 HUD lang/dir context segment missing")
ok(_eng.count("' @ ' + location.host + '/' + (location.pathname.split('/').pop() || '')") == 1,
   "i18n.js: r123 HUD origin/page context segment missing")
ok(_eng.count("r123: context segment (page/lang/dir @ host)") == 1,
   "i18n.js: r123 HUD section comment missing")
ok(_eng.count("' @ ' + location.host") <= 1,
   "i18n.js: HUD context segment duplicated")

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r123_block + anchor, 1)

# 3) version bump: v67 -> v68 everywhere it is pinned as wanted; v67 joins residue
out = out.replace('ok(_nf.count("i18n.js?v=67") == 1, "404.html: i18n v66 pin x!=1")',
                  'ok(_nf.count("i18n.js?v=68") == 1, "404.html: i18n v68 pin x!=1")')
out = out.replace('want_i, want_s = "i18n.js?v=67", "style.css?v=58"',
                  'want_i, want_s = "i18n.js?v=68", "style.css?v=58"')
out = out.replace('ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0 and t.count("i18n.js?v=65") == 0 and t.count("i18n.js?v=66") == 0, f"{page}: stale i18n pin residue")',
                  'ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0 and t.count("i18n.js?v=65") == 0 and t.count("i18n.js?v=66") == 0 and t.count("i18n.js?v=67") == 0, f"{page}: stale i18n pin residue")')

# 4) relabel
out = out.replace('print("check_r122: FAILURES:")', 'print("check_r123: FAILURES:")')
out = out.replace('print(f"check_r122: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r123: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r123.py").write_text(out, encoding="utf-8")
print("check_r123.py written:", len(out), "bytes")
