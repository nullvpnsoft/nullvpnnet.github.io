#!/usr/bin/env python3
"""Generate tools/check_r119.py from check_r118.py: swap the docstring,
inject the r119 Latin-locale debt gate (es==fr identity + cross-key en
paraphrase), bump i18n pin v65 -> v66 with residue, relabel output.
style v58 carried (no style changes this round).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r118.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r119 guards: Latin-locale translation-debt gate (es/fr).

(Carries the full r44-r118 chain, regenerated from check_r118.py; the r118
locale-value asserts remain in force below.)

SHIP (i18n.js values + buster v65 -> v66; no HTML structure changes):

The ru/fr runtime lens caught a real defect the r118 gate could not see:
faq.q2 rendered ENGLISH under ?lang=es while the surrounding page was
Spanish. Root cause: 27 keys (49 values) carried stale ENGLISH PARAPHRASES
from an older en revision as their es and/or fr values — ru/fa/ar/ne were
refreshed in earlier rounds but es/fr were left behind. Affected surfaces
were prominent: index hero (index.h1a/badge/prob2/sp), comparison hero +
rows (comp.hero.h1/lead, comp.row.reachable/strictnat), FAQ questions and
five answers (faq.q1/q2/q5, faq.a1/a2/a4/a5/a8), pricing payment note
(price.pay.p), download step (dl.step1), how-it-works comparison columns
(how.regular.*, how.nullvpn.3, how.note3/4.h), feat.r5.p, contact.web3.p.

Why r118 missed it: the sentinel catches es/ne == OWN-en identity, but a
paraphrase differs from the key's current en. Two new detectors close the
class (both fed by the r118 string-aware _parse_T):

1. es==fr IDENTITY (>= 24 chars): a real Spanish translation essentially
   never equals the French one; identical values are un-localized debt.
   Asserted EMPTY (verified empirically after the fix — no legit pair).
2. CROSS-KEY en PARAPHRASE: any locale value (>= 12 chars, normalized)
   equal to a DIFFERENT key's en value = borrowed English. Asserted EMPTY.

All 49 values re-translated in-register (es=tu, fr=vous; straight
apostrophes per corpus 104:21; tags byte-preserved: faq.a5 <a> attrs,
price.pay.p <strong>). Verified live after deploy: faq q1/q2 render
Spanish/French; filter E2E hits the translated answer text.
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r119 asserts before the versions section (reuses _T from the r118 block)
r119_block = '''
# --- r119 ship asserts (Latin-locale debt gate) --------------------------------------------------
import re as _re119

_norm119 = lambda s: _re119.sub(r"\\s+", " ", (s or "")).strip().lower()

# 1) es==fr identity: zero tolerance (Latin-locale un-localized debt detector)
_ident_ef = sorted(k for k, e in _T.items()
                   if len(e.get("es", "")) >= 24 and e.get("es", "") == e.get("fr", ""))
ok(not _ident_ef, "i18n.js: es==fr identical (untranslated debt): " + repr(_ident_ef[:4]))

# 2) cross-key en paraphrase: a locale value equal to a DIFFERENT key's en value
_en_norms = {}
for _k, _e in _T.items():
    _en_norms.setdefault(_norm119(_e.get("en", "")), set()).add(_k)
_para = []
for _k, _e in _T.items():
    for _l in _LOCS[1:]:
        _v = _norm119(_e.get(_l, ""))
        if len(_v) >= 12:
            _others = sorted(o for o in _en_norms.get(_v, set()) if o != _k)
            if _others:
                _para.append((_k, _l, _others[0]))
ok(not _para, "i18n.js: value equals another key's en (borrowed paraphrase): " + repr(_para[:4]))

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r119_block + anchor, 1)

# 3) version bump: i18n v65 -> v66 (+ residue)
out = out.replace('want_i, want_s = "i18n.js?v=65", "style.css?v=58"',
                  'want_i, want_s = "i18n.js?v=66", "style.css?v=58"')
out = out.replace('ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0, f"{page}: stale i18n pin residue")',
                  'ok(t.count("i18n.js?v=63") == 0 and t.count("i18n.js?v=64") == 0 and t.count("i18n.js?v=65") == 0, f"{page}: stale i18n pin residue")')
# mid-chain current-pin assert (404 zero-JS GET contract round) rides the bump too
out = out.replace('ok(_nf.count("i18n.js?v=65") == 1, "404.html: i18n v65 pin x!=1")',
                  'ok(_nf.count("i18n.js?v=66") == 1, "404.html: i18n v66 pin x!=1")')
assert 'i18n.js?v=66' in out, "version bump failed"
assert 'v=65") == 1' not in out, "unbumped mid-chain v65 pin assert remains"

# 4) relabel
out = out.replace('print("check_r118: FAILURES:")', 'print("check_r119: FAILURES:")')
out = out.replace('print(f"check_r118: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r119: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r119.py").write_text(out, encoding="utf-8")
print("check_r119.py written:", len(out), "bytes")
