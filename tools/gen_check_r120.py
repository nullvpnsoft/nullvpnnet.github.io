#!/usr/bin/env python3
"""Generate tools/check_r120.py from check_r119.py: swap the docstring,
inject the sibling-locale identity gates (fa==ar, ru==ne — the remaining
same-script locale pairs after r119's es==fr), relabel output.
Version pins carried (i18n v66 / style v58 — guard-only round).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r119.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r120 guards: sibling-locale identity gates (fa==ar, ru==ne).

(Carries the full r44-r119 chain, regenerated from check_r119.py; the r118
value-quality asserts and r119 Latin-locale debt gates remain in force.)

SHIP (guard-only round — zero site-file changes, no buster bumps):

The fa/ar runtime lens closed the last unlensed locale surface CLEAN:
faq RTL (Persian filter E2E 'بازپرداخت' -> 1 hit + <mark> highlight in RTL,
logical text-align:start, chips localized), pricing checkout modal RTL
geometry (centered, direction rtl, close reachable), ar home first lens
(62/62 Arabic nodes, 5 feat-cards, no overflow), contact fa (no overflow),
404 path-suggest verified LOCALE-AWARE live (rendered 'آیا منظورتان این بود:
قیمت‌ها' under stored fa). Re-lens rotation: web3 (noscript honesty, cancel,
no overflow) and download (43 i18n nodes) CLEAN. Console zero errors.

The durable value — the r119 playbook applied to the remaining same-script
locale pairs. Sibling identity = un-localized debt (a real Persian translation
essentially never equals the Arabic one; a real Russian never equals Nepali):

1. fa==ar identity (>= 12 chars): asserted EMPTY (verified pre-work).
2. ru==ne identity (>= 16 chars): asserted == {comp.val.telegramweb3} —
   the r118-allowlisted by-design Latin value ('Telegram + Web3 ✔'),
   identical in every locale except fa. Drift either way fails the gate.

Coverage matrix after r120 — every same-script sibling pair is gated:
es/fr (r119), fa/ar (r120), ru/ne (r120); cross-script debt is caught by
the r118 native-script + foreign-leak gates; en-identity debt by the r118
sentinel; borrowed paraphrases by the r119 cross-key gate.
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r120 asserts before the versions section (reuses _T from the r118 block)
r120_block = '''
# --- r120 ship asserts (sibling-locale identity gates) -------------------------------------------
_norm120 = lambda s: _re119.sub(r"\\s+", " ", (s or "")).strip()

# 1) fa==ar identity: zero tolerance (same-script un-localized debt detector)
_ident_fa_ar = sorted(k for k, e in _T.items()
                      if len(e.get("fa", "")) >= 12 and _norm120(e.get("fa", "")) == _norm120(e.get("ar", "")))
ok(not _ident_fa_ar, "i18n.js: fa==ar identical (untranslated debt): " + repr(_ident_fa_ar[:4]))

# 2) ru==ne identity: only the by-design shared Latin value may coincide
_ident_ru_ne = sorted(k for k, e in _T.items()
                      if len(e.get("ru", "")) >= 16 and _norm120(e.get("ru", "")) == _norm120(e.get("ne", "")))
ok(_ident_ru_ne == ["comp.val.telegramweb3"],
   f"i18n.js: ru==ne identity drifted (got {_ident_ru_ne}, expected [comp.val.telegramweb3])")

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r120_block + anchor, 1)

# 3) no version changes this round.

# 4) relabel
out = out.replace('print("check_r119: FAILURES:")', 'print("check_r120: FAILURES:")')
out = out.replace('print(f"check_r119: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r120: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r120.py").write_text(out, encoding="utf-8")
print("check_r120.py written:", len(out), "bytes")
