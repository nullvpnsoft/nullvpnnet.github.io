#!/usr/bin/env python3
"""r83 guard — table semantics estate-wide + AA contrast fixes.
Fails loudly if any scope attribute, continuity rule, or contrast fix is lost."""
import re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

def check(cond, msg):
    if not cond:
        errors.append(msg)

# ── 1. thead scope="col" estate-wide (all three tables) ──────────────────
for page, expected_cols in (("features.html", 4), ("privacy.html", 4), ("comparison.html", 6)):
    html = (root / page).read_text(encoding="utf-8")
    thead = re.search(r"<thead>(.*?)</thead>", html, re.S)
    check(thead is not None, f"{page}: no <thead> found")
    if thead:
        ths = re.findall(r"<th\b[^>]*>", thead.group(1))
        check(len(ths) == expected_cols,
              f"{page}: thead has {len(ths)} th, expected {expected_cols}")
        for th in ths:
            check('scope="col"' in th, f"{page}: thead th missing scope=\"col\": {th}")

# ── 2. tbody row headers th[scope="row"] ─────────────────────────────────
priv = (root / "privacy.html").read_text(encoding="utf-8")
priv_body = re.search(r"<tbody>(.*?)</tbody>", priv, re.S).group(1)
check(len(re.findall(r'<th scope="row"', priv_body)) == 6,
      "privacy: expected 6 tbody th[scope=row]")
check('<tr><td data-i18n="priv.tbl.r' not in priv_body,
      "privacy: tbody still has a td first-cell (r1-r6 rows must be th)")

comp = (root / "comparison.html").read_text(encoding="utf-8")
comp_body = re.search(r"<tbody>(.*?)</tbody>", comp, re.S).group(1)
check(len(re.findall(r'<th scope="row"', comp_body)) == 11,
      "comparison: expected 11 tbody th[scope=row]")
check('<tr><td data-i18n="comp.row.' not in comp_body,
      "comparison: tbody still has a td row label (all 11 must be th)")

# ── 3. CSS continuity rules ───────────────────────────────────────────────
comp_css = re.search(r"<style>(.*?)</style>", comp, re.S).group(1)
check("tbody th[scope=\"row\"]{padding:13px 16px" in comp_css,
      "comparison: r83 continuity rule missing (tbody th[scope=row])")
check('tbody tr.comp-row-pin th[scope="row"]{background:rgba(var(--accent-rgb),.16)' in comp_css,
      "comparison: row-pin th variant missing")
check("tbody tr.comp-row-pin th[scope=\"row\"]{animation:compPinIn" in comp_css,
      "comparison: row-pin th animation variant missing")

css = (root / "style.css").read_text(encoding="utf-8")
check(".data-table tbody th[scope=\"row\"] { background: transparent;" in css,
      "style.css: .data-table tbody th[scope=row] continuity rule missing")
check(".data-table tr:last-child th { border-bottom: none; }" in css,
      "style.css: .data-table last-row th border rule missing")

# ── 4. AA contrast fixes (accent→accent2 on small white text) ─────────────
def blocks(selector, text):
    """All rule bodies for a selector. Group selectors (.a,\n.b {) also match,
    so callers pass if ANY body carries the wanted declaration."""
    return re.findall(re.escape(selector) + r"\s*\{(.*?)\n\}", text, re.S)

def line_rule(selector, text):
    """Single-line rule bodies (group selectors capture empty/whitespace only)."""
    return re.findall(re.escape(selector) + r"\s*\{([^\n]*)", text)

check(any("background: var(--accent2)" in b for b in blocks(".btn-nav-primary", css)),
      "style.css: .btn-nav-primary must use accent2")
check(any("border: 1.5px solid var(--accent2)" in b for b in blocks(".btn-nav-primary", css)),
      "style.css: .btn-nav-primary border must use accent2")
check(any("var(--accent3)" in r for r in line_rule(".btn-nav-primary:hover", css)),
      "style.css: .btn-nav-primary:hover must lift to accent3")
check(".lang-btn.active { background: var(--accent2)" in css,
      "style.css: .lang-btn.active must use accent2")
check(any("background: var(--accent2)" in b for b in blocks(".popular-badge", css)),
      "style.css: .popular-badge must use accent2")
skip = " ".join(blocks(".skip-link", css))
check("background: var(--accent2)" in skip,
      "style.css: .skip-link must use accent2")
# back-to-top deliberately left on accent (icon-only, non-text 3:1 passes at 3.68)
btt = " ".join(blocks(".back-to-top", css))
check("background: var(--accent);" in btt,
      "style.css: .back-to-top should stay on accent (non-text 3:1 — do not drift)")

if errors:
    print("R83 GUARD FAILURES:")
    for e in errors:
        print("  ✗", e)
    sys.exit(1)
print("r83 guard: ALL PASS — scope estate + continuity rules + AA fixes intact")
