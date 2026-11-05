#!/usr/bin/env python3
"""Generate check_r135.py: extends the r44-r134 chain with the r135 gate.

r135 (Task 135 ship): locale deep-scan + content-surface hover affordances.
  (a) getLang() scans the FULL navigator.languages preference list (first
      supported base-2 match wins) instead of only navigator.language[0] —
      a 'de'-primary visitor with a supported 'ru' second choice now gets RU
      instead of a silent EN default. Auto-detect stays un-persisted: an
      explicit stored choice always outranks it.
  (b) style.css r135 block: hover affordances for the content surfaces that
      had none — .pricing-card (border-strong + shadow + 2px lift; featured
      keeps accent; dark shadow variant; reduced-motion drops the lift) and
      gated row tints (.faq-item / .data-table tbody tr, accent .04 = the
      r80 features-page token, one shade under the :target .07). Comparison
      intentionally excluded (r59 column spotlight would fight a row tint).
      Block sits BEFORE .faq-item:target so the deep-link tint wins the
      cascade (equal specificity, later rule wins).
  (c) busters: style v60 -> v61, i18n v70 -> v71 (carried pins moved; v59/v70
      join the stale lists). Key count stays 470 (no new keys — hovers and
      the deep-scan add no visitor-facing strings).

Teeth plan (mutation-tested after generation):
  M1: neutralize the hover-gate media line -> assert fires.
  M2: delete the deep-scan for-loop -> assert fires.
  M3: neutralize the full .faq-item:hover line -> assert fires (full-line
      anchor per the r134 M3 lesson: pattern-family pins need full rules).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "check_r134.py"
DST = ROOT / "tools" / "check_r135.py"

R135 = '''

# --- r135: locale deep-scan + content-surface hover affordances (Task 135) ---
# (a) getLang() deep-scans the full preference list, not just entry [0]
ok(_i18n.count("navigator.languages && navigator.languages.length") == 1,
   "i18n.js: r135 navigator.languages guard missing")
ok(_i18n.count("for (const pref of prefs)") == 1,
   "i18n.js: r135 preference-list loop missing")
ok(_i18n.count("r135: scan the FULL preference list") == 1,
   "i18n.js: r135 deep-scan comment marker missing")
# (b) style.css hover systems
ok(css.count("r135 — hover affordances for CONTENT surfaces") == 1,
   "style.css: r135 hover block marker missing")
# the gate itself, anchored to the block (the bare media line occurs 31x
# estate-wide; only the r135 wrap is followed by the pricing-card opener)
# chr(10): generator triple-quotes would eat a literal \\n escape (lesson v)
ok(css.count("@media (hover: hover) and (pointer: fine) {" + chr(10) + "  .pricing-card:hover {") == 1,
   "style.css: r135 hover gate media wrap missing")
# full-line anchors (r134 M3 lesson: pattern pins need the full rule)
ok(css.count("    transform: translateY(-2px);") == 1,
   "style.css: pricing-card hover lift missing")
ok(css.count("  .faq-item:hover { background: rgba(var(--accent-rgb), .04); }") == 1,
   "style.css: faq-item hover tint line missing")
ok(css.count("  .data-table tbody tr:hover { background: rgba(var(--accent-rgb), .04); }") == 1,
   "style.css: data-table hover tint line missing")
ok(css.count("  .pricing-card.featured:hover {") == 1,
   "style.css: featured card hover rule missing")
ok(css.count('[data-theme="dark"] .pricing-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,.45); }') == 1,
   "style.css: dark shadow variant missing")
ok(css.count("  .pricing-card:hover { transform: none; }") == 1,
   "style.css: reduced-motion lift suppression missing")
# the r135 block must sit BEFORE .faq-item:target so the deep-link tint
# wins the cascade when both apply (equal specificity, later rule wins)
ok(css.index("r135 — hover affordances") < css.index(".faq-item:target {"),
   "style.css: r135 hover block must precede .faq-item:target")
# features-page row hover (r80) pinned — the token this round aligned to
ok('rgba(var(--accent-rgb), .04); }' in (ROOT / "features.html").read_text(encoding="utf-8"),
   "features.html: r80 row-hover token lost")
'''

src = SRC.read_text(encoding="utf-8")
# carried pins: busters + counts
src = src.replace('ok(_nf.count("i18n.js?v=70") == 1, "404.html: i18n v70 pin x!=1")',
                  'ok(_nf.count("i18n.js?v=71") == 1, "404.html: i18n v71 pin x!=1")')
src = src.replace('want_i, want_s = "i18n.js?v=70", "style.css?v=60"',
                  'want_i, want_s = "i18n.js?v=71", "style.css?v=61"')
# stale-list extensions (v59 style, v69 i18n now banned)
src = src.replace('and t.count("style.css?v=58") == 0 and t.count("style.css?v=59") == 0, f"{page}: stale style pin residue")',
                  'and t.count("style.css?v=58") == 0 and t.count("style.css?v=59") == 0 and t.count("style.css?v=60") == 0, f"{page}: stale style pin residue")')
src = src.replace('and t.count("i18n.js?v=68") == 0 and t.count("i18n.js?v=69") == 0, f"{page}: stale i18n pin residue")',
                  'and t.count("i18n.js?v=68") == 0 and t.count("i18n.js?v=69") == 0 and t.count("i18n.js?v=70") == 0, f"{page}: stale i18n pin residue")')
# NOTE: check_r134.py carries the FULL stale chains (v55..v59 style, v63..v69
# i18n). The substring replaces above target the TAIL of those chains, which
# is unique enough: the style chain ends ...v58)==0 and ...v59)==0, and the
# i18n chain ends ...v68)==0 and ...v69)==0. After replacement the tails
# become ...v59)==0 and ...v60)==0 / ...v69)==0 and ...v70)==0.
src = src.replace('all 470 keys against every HTML', 'all 470 keys against every HTML')
src = src.replace('check_r134: FAILURES:', 'check_r135: FAILURES:')
src = src.replace('print(f"check_r134: ALL GREEN', 'print(f"check_r135: ALL GREEN')
idx = src.rindex("\nif errs:")
out = src[:idx] + R135 + src[idx:]
DST.write_text(out, encoding="utf-8")
print(f"generated {DST} ({len(out.splitlines())} lines)")
