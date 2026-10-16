#!/usr/bin/env python3
"""Generate tools/check_r118.py from check_r117.py: swap the docstring,
inject the r118 locale-value quality gate + chrome-sync/scrollbar-gutter
source pins, relabel output. No version bumps (style v58 / i18n v65 carried
— guard-only ship).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r117.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r118 guards: locale-VALUE quality gate (es/ne lens institutionalized).

(Carries the full r44-r117 chain, regenerated from check_r117.py; r117 ship
asserts remain in force below.)

SHIP (guard-only round — no site-file changes, no buster bumps):

This round ran the due es/ne locale spot-check (last done r78) plus the
oldest re-lens rotation (web3/contact/offline, r111-era). All CLEAN — zero
functional findings, zero real translation gaps. Two styling-improvement
candidates were investigated and both proved ALREADY SHIPPED (verified live):
theme-color chrome sync = i18n.js r64 (collapses the static pair to one
dynamic meta, MutationObserver mirrors the toggle; branding.js r54 then
no-ops — interplay verified live: toggle dark -> single meta #0a0f1a);
checkout scroll-lock gutter = style.css r104 scrollbar-gutter: stable.
comparison col-pin deep link re-proven: sticky TH lands at scroll-margin
200px, 11 td + 1 th pins == the table's 11 feature rows (r116's log prose
said "12 td" — record slip, site correct; repo row- ids = 11).

The durable value — check_html_i18n counts keys/usages (529x7/798) but
inspects NO values. The r118 gate adds value-quality teeth (T parsed with a
string-aware brace scanner — a naive [^{}]* body regex silently drops keys
whose values contain {year}):

1. {year} PARITY: wherever en carries {year}, all 7 locales must too
   (a missing one renders a literal "{year}" to that locale's visitors).
2. NO EMPTY VALUES: any empty/whitespace locale value fails.
3. NATIVE-SCRIPT PRESENCE: values >= 6 chars must contain their locale's
   script (ru->Cyrillic, fa/ar->Arabic, ne->Devanagari) except an EXACT
   pinned allowlist of 35 (key, locale) pairs — brand/protocol labels kept
   Latin by design (VPN brand names, Lightway/Stealth/TON Web3/Telegram +
   Web3 protocol labels, the how.nullvpn.h heading) plus the two ru price
   amounts (1 000 ₽ / 3 500 ₽ — currency format carries no Cyrillic).
   Drift in EITHER direction fails — a new untranslated string or a new
   translation of an allowlisted one both force a conscious gate edit.
4. FOREIGN-SCRIPT LEAKS = zero tolerance: Devanagari/Cyrillic/Arabic
   characters inside en/es/fr values (paste errors the key-count gate
   cannot see).
5. UNTRANSLATED SENTINEL: es/ne values identical to en (>= 24 chars)
   must equal the exact pinned set ({contact.sup.tg.btn, es} — brand
   handle button, identical by design). A future stale English paragraph
   hiding in es/ne fails the gate.
6. Source pins for today's live-verified contracts: i18n.js r64 chrome
   sync (the :not([media]) selector + [media] removal selector + block
   comment; asserted via python byte `in` — tool output mangles brackets,
   file bytes do not) and style.css r104 scrollbar-gutter html rule; the
   static per-page meta pair (light + dark media) + color-scheme meta
   remain asserted as the no-JS fallback contract.
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r118 asserts before the versions section
r118_block = '''
# --- r118 ship asserts (locale-value quality gate + contract source pins) -----------------------
import unicodedata as _uni

def _script_chars(s):
    has = set()
    for ch in s:
        name = _uni.name(ch, "")
        if "DEVANAGARI" in name: has.add("deva")
        elif "CYRILLIC" in name: has.add("cyrl")
        elif "ARABIC" in name: has.add("arab")
    return has

_LOCS = ["en", "ru", "fa", "ar", "es", "ne", "fr"]
_NATIVE = {"ru": "cyrl", "fa": "arab", "ar": "arab", "ne": "deva"}
_FOREIGN = {"en": {"cyrl", "deva", "arab"}, "es": {"cyrl", "deva", "arab"}, "fr": {"cyrl", "deva", "arab"},
            "ru": {"deva"}, "fa": {"cyrl", "deva"}, "ar": {"cyrl", "deva"}, "ne": {"cyrl"}}

def _parse_T(text):
    """Parse the T table: key -> {locale: value}. String-aware brace scanner —
    a naive [^{}]* body regex silently drops keys whose values contain {year}."""
    start = text.find("const T = {")
    if start == -1:
        return {}
    i = text.find("{", start)
    n = len(text)
    j, depth, in_str, esc = i + 1, 1, False, False
    while j < n and depth > 0:
        c = text[j]
        if in_str:
            if esc: esc = False
            elif c == "\\\\": esc = True
            elif c == '"': in_str = False
        else:
            if c == '"': in_str = True
            elif c == "{": depth += 1
            elif c == "}": depth -= 1
        j += 1
    t_src = text[i + 1:j - 1]
    import re as _re
    key_re = _re.compile(r'"([a-z0-9_.\\-]+)"\\s*:\\s*\\{')
    val_re = _re.compile(r'\\b(en|ru|fa|ar|es|ne|fr)\\s*:\\s*"((?:[^"\\\\]|\\\\.)*)"')
    table, k, tn = {}, 0, len(t_src)
    while k < tn:
        m = key_re.search(t_src, k)
        if not m:
            break
        key = m.group(1)
        b, depth, in_str, esc = m.end(), 1, False, False
        while b < tn and depth > 0:
            c = t_src[b]
            if in_str:
                if esc: esc = False
                elif c == "\\\\": esc = True
                elif c == '"': in_str = False
            else:
                if c == '"': in_str = True
                elif c == "{": depth += 1
                elif c == "}": depth -= 1
            b += 1
        entry = {}
        for vm in val_re.finditer(t_src[m.end():b - 1]):
            entry[vm.group(1)] = vm.group(2).replace('\\\\"', '"').replace("\\\\n", "\\n")
        if len(entry) >= 5:
            table[key] = entry
        k = b
    return table

_T = _parse_T((ROOT / "i18n.js").read_text(encoding="utf-8"))
ok(len(_T) >= 500, f"i18n.js: T parse collapsed (got {len(_T)} keys, expected ~529)")

# 1) {year} parity + 2) no empty values
_year_fail = [(k, l) for k, e in _T.items() if "{year}" in e.get("en", "")
              for l in _LOCS if l != "en" and "{year}" not in e.get(l, "")]
ok(not _year_fail, "i18n.js: {year} parity broken: " + repr(_year_fail[:4]))
_empty = [(k, l) for k, e in _T.items() for l, v in e.items() if not v.strip()]
ok(not _empty, "i18n.js: empty locale values: " + repr(_empty[:4]))

# 3) native-script presence (>= 12 chars) with exact pinned brand allowlist
_R118_LOCS = ("ru", "fa", "ar", "ne")
_R118_BRAND_ALLOW = set()
for _bk in ("comp.table.expressvpn", "comp.table.nordvpn",
            "comp.table.nullvpn", "comp.table.protonvpn"):
    for _bl in _R118_LOCS:
        _R118_BRAND_ALLOW.add((_bk, _bl))          # 16: comparison VPN brand names, Latin by design
for _bk, _bls in (("comp.val.lightway", ("ar", "fa", "ru")),
                  ("comp.val.stealth", ("ar", "fa", "ru")),
                  ("comp.val.telegramweb3", ("ar", "ne", "ru")),
                  ("contact.web3.h", ("ar", "fa", "ne", "ru")),
                  ("how.nullvpn.h", ("ar", "fa", "ne", "ru"))):
    for _bl in _bls:
        _R118_BRAND_ALLOW.add((_bk, _bl))          # 13: protocol labels + TON heading, Latin by design
_R118_BRAND_ALLOW.add(("price.p3.amount", "ru"))   # 1 000 ₽ — currency format, no Cyrillic by design
_R118_BRAND_ALLOW.add(("price.p4.amount", "ru"))   # 3 500 ₽
# 35 (key, locale) pairs total — exact r118-audited clean state; the gate itself
# surfaced the fa/ar pairs (the audit lens skipped no-native checks for
# Arabic-script locales) and price amounts. Drift either way = conscious edit.
_no_native = []
for _k, _e in _T.items():
    for _l, _need in _NATIVE.items():
        _v = _e.get(_l, "")
        if len(_v) >= 6 and _need not in _script_chars(_v) and (_k, _l) not in _R118_BRAND_ALLOW:
            _no_native.append((_k, _l))
ok(not _no_native, "i18n.js: native-script missing (untranslated or brand beyond allowlist): " + repr(_no_native[:4]))
_allow_drift = set()
for _k, _e in _T.items():
    for _l in _NATIVE:
        _v = _e.get(_l, "")
        if len(_v) >= 6 and _NATIVE[_l] not in _script_chars(_v):
            _allow_drift.add((_k, _l))
ok(_allow_drift == _R118_BRAND_ALLOW,
   f"i18n.js: brand allowlist drifted (got {len(_allow_drift)} pairs: {sorted(_allow_drift)[:6]}..., expected 35 pinned pairs)")

# 4) foreign-script leaks: zero tolerance
_leaks = []
for _k, _e in _T.items():
    for _l, _bad in _FOREIGN.items():
        _v = _e.get(_l, "")
        if _script_chars(_v) & _bad:
            _leaks.append((_k, _l))
ok(not _leaks, "i18n.js: foreign-script leaks: " + repr(_leaks[:4]))

# 5) untranslated sentinel: es/ne identical to en (>= 24 chars) == pinned set
_R118_IDENTICAL_OK = {("contact.sup.tg.btn", "es")}  # brand handle button, by design
_identical = {(k, l) for k, e in _T.items() for l in ("es", "ne")
              if e.get(l, "") == e.get("en", "") and len(e.get("en", "")) >= 24}
ok(_identical == _R118_IDENTICAL_OK,
   f"i18n.js: es/ne == en sentinel drifted (got {sorted(_identical)})")

# 6a) i18n.js r64 chrome-sync source pins (byte `in` — file bytes are ground truth)
_i18n_r118 = (ROOT / "i18n.js").read_text(encoding="utf-8")
ok('meta[name="theme-color"]:not([media])' in _i18n_r118,
   "i18n.js: r64 chrome-sync selector missing")
ok('meta[name="theme-color"][media]' in _i18n_r118,
   "i18n.js: r64 [media]-collapse selector missing")
ok("Browser-chrome theme sync (r64)" in _i18n_r118, "i18n.js: r64 block comment missing")
ok("Live OS-theme follow (r99)" in _i18n_r118, "i18n.js: r99 OS-follow block missing")

# 6b) style.css r104 scrollbar-gutter html rule (checkout scroll-lock shift guard)
css_r118 = (ROOT / "style.css").read_text(encoding="utf-8")
ok(css_r118.count("html { scrollbar-width: thin; scrollbar-color: var(--border) transparent; scrollbar-gutter: stable; }") == 1,
   "style.css: r104 scrollbar-gutter html rule churned")
ok("r104: scrollbar-gutter: stable" in css_r118, "style.css: r104 comment missing")

# 6c) per-page no-JS fallback meta contract
for _page in PAGES:
    _t = (ROOT / _page).read_text(encoding="utf-8")
    ok(_t.count('<meta name="theme-color" content="#f7e7ce"/>') == 1,
       _page + ": static light theme-color meta missing")
    ok(_t.count('<meta name="theme-color" content="#0a0f1a" media="(prefers-color-scheme: dark)"/>') == 1,
       _page + ": static dark media theme-color meta missing")
    ok(_t.count('<meta name="color-scheme" content="light dark"') == 1,
       _page + ": color-scheme meta missing")

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r118_block + anchor, 1)

# 3) no version changes this round.

# 4) relabel
out = out.replace('print("check_r117: FAILURES:")', 'print("check_r118: FAILURES:")')
out = out.replace('print(f"check_r117: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r118: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r118.py").write_text(out, encoding="utf-8")
print("check_r118.py written:", len(out), "bytes")
