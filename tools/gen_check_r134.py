#!/usr/bin/env python3
"""Generate check_r134.py: extends the r44-r132 chain with the r134 gate.

r134 (Task 134 ship): QR phone-transfer card + legal print chip + styling.
  (a) download.html gains an engine-built (i18n.js section 15) QR card of the
      page's rel=canonical URL — self-contained byte-mode ECC-M v2/v3 encoder
      (GF(256) RS, full 8-mask penalty selection), verified decode-exact
      against the python qrcode reference AND cv2 + zbar before shipping.
      Desktop-only display; pre-paint build => zero CLS by construction.
  (b) terms/privacy/refund gain an engine-built (section 16) "Save as PDF"
      chip after .page-toc -> window.print() (r133 print styles verified on
      real paper); hidden on paper by the r134 print block.
  (c) styling detail: .page-toc pill background joins the transition list
      (scroll-spy active bg no longer snaps); .qr-card/.print-chip component
      styles light+dark+RTL.
  (d) busters: style v59 -> v60, i18n v69 -> v70 (carried pins moved; v68/v58
      join the stale lists). Key count 466 -> 470 (4 new keys x7 locales).

Teeth plan (mutation-tested after generation):
  M1: neutralize .qr-card display rule -> assert fires.
  M2: remove a dl.qr.* locale value -> key-count/locale assert fires.
  M3: drop the toc background transition -> assert fires.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "check_r132.py"
DST = ROOT / "tools" / "check_r134.py"

R134 = '''

# --- r134: QR phone-transfer card + print chip + styling details (Task 134) ---
ok(_i18n.count("15) QR") == 1, "i18n.js: r134 section-15 marker missing")
ok(_i18n.count('"Save as PDF" chip (r134)') == 1,
   "i18n.js: r134 section-16 marker missing")
# embedded encoder must carry its core machinery (names unique to section 15)
for _mk in ("function rsGenPoly(", "function rsEcc(", "function maskTest(",
            "function formatBits(", "function drawFormat(", "'qr-card'",
            "'dl.qr.title'", "'dl.qr.sub'", "'dl.qr.alt'",
            "data-i18n-aria', 'dl.qr.alt'"):
    ok(_mk in _i18n, "i18n.js: r134 QR machinery missing: " + _mk)
# 4 new keys x7 locales
for _k in ("dl.qr.title", "dl.qr.sub", "dl.qr.alt", "legal.print"):
    ok(_k in _T, "i18n.js: r134 key missing from T: " + _k)
    for _loc in ("en", "ru", "fa", "ar", "es", "ne", "fr"):
        ok(isinstance(_T[_k].get(_loc), str) and len(_T[_k][_loc]) > 2,
           f"i18n.js: r134 key {_k} locale {_loc} empty")
# legal print chip machinery + CSS
ok(_i18n.count("'print-chip'") == 1 and _i18n.count("'print-row'") == 1,
   "i18n.js: r134 print-chip build missing")
ok(_i18n.count("pcBtn.addEventListener('click', function () { window.print(); });") == 1,
   "i18n.js: print chip action missing")
ok(css.count("r134: QR phone-transfer card") == 1, "style.css: r134 QR block missing")
ok(css.count(".qr-card { display: none; flex-direction: column;") == 1,
   "style.css: qr-card desktop-only display gate missing")
ok(css.count(".qr-card { display: flex; }") == 1,
   "style.css: qr-card media display-flex rule missing")
ok(("[data-theme=" + chr(34) + "dark" + chr(34) + "] .qr-card { background: var(--bg3); }") in css,
   "style.css: qr-card dark variant missing")
ok(css.count("@media print { .qr-card, .print-row { display: none !important; } }") == 1,
   "style.css: r134 print-hide for qr-card/print-row missing")
ok(css.count(".print-chip") >= 4, "style.css: print-chip component styles missing")
# styling detail: toc pill background joins the transition (no snap on spy).
# Pinned as the FULL toc rule so a sibling component sharing the pattern
# cannot satisfy the check (the M3 mutation test caught exactly that).
ok(("/* r98 */ transition: color .15s ease, border-color .15s ease, "
    "background .15s ease; /* r134: background joins") in css,
   "style.css: r134 toc background transition missing")
# pre-existing a11y pins guarded against regression
for _pg in ("faq.html", "404.html"):
    ok('aria-keyshortcuts="/"' in (ROOT / _pg).read_text(encoding="utf-8"),
       _pg + ": aria-keyshortcuts pin lost")
ok(len(_T) == 470, f"i18n.js: key count drifted (got {len(_T)}, expected 470)")
'''

src = SRC.read_text(encoding="utf-8")
# carried pins: busters + counts
src = src.replace('ok(_nf.count("i18n.js?v=69") == 1, "404.html: i18n v69 pin x!=1")',
                  'ok(_nf.count("i18n.js?v=70") == 1, "404.html: i18n v70 pin x!=1")')
src = src.replace('want_i, want_s = "i18n.js?v=69", "style.css?v=59"',
                  'want_i, want_s = "i18n.js?v=70", "style.css?v=60"')
src = src.replace('ok(len(_T) == 466, f"i18n.js: key count drifted (got {len(_T)}, expected 466)")',
                  'ok(len(_T) == 470, f"i18n.js: key count drifted (got {len(_T)}, expected 470)")')
# stale-list extensions (v58 style, v68 i18n now banned)
src = src.replace('and t.count("style.css?v=58") == 0, f"{page}: stale style pin residue")',
                  'and t.count("style.css?v=58") == 0 and t.count("style.css?v=59") == 0, f"{page}: stale style pin residue")')
src = src.replace('and t.count("i18n.js?v=68") == 0, f"{page}: stale i18n pin residue")',
                  'and t.count("i18n.js?v=68") == 0 and t.count("i18n.js?v=69") == 0, f"{page}: stale i18n pin residue")')
src = src.replace('ok(len(_T) >= 450, f"i18n.js: T parse collapsed (got {len(_T)} keys, expected ~466)")',
                  'ok(len(_T) >= 450, f"i18n.js: T parse collapsed (got {len(_T)} keys, expected ~470)")')
src = src.replace('all 466 keys against every HTML', 'all 470 keys against every HTML')
# r134 carried pins: .print-chip adds one border-strong shorthand (10 -> 11)
# and .qr-card adds one plain-border shorthand (12 -> 13)
src = src.replace('ok(css.count("border: 1px solid var(--border-strong)") == 10,',
                  'ok(css.count("border: 1px solid var(--border-strong)") == 11,')
src = src.replace('style.css: border-strong shorthand count changed (expected 10)',
                  'style.css: border-strong shorthand count changed (expected 11)')
src = src.replace('ok(css.count("border: 1px solid var(--border);") == 12,',
                  'ok(css.count("border: 1px solid var(--border);") == 13,')
src = src.replace('style.css: decorative plain-border inventory changed (expected 12)',
                  'style.css: decorative plain-border inventory changed (expected 13)')
src = src.replace('check_r132: FAILURES:', 'check_r134: FAILURES:')
src = src.replace('print(f"check_r132: ALL GREEN', 'print(f"check_r134: ALL GREEN')
idx = src.rindex("\nif errs:")
out = src[:idx] + R134 + src[idx:]
DST.write_text(out, encoding="utf-8")
print(f"generated {DST} ({len(out.splitlines())} lines)")
