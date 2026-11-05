#!/usr/bin/env python3
"""r84 guard: comparison deep-link landing + :target ring parity.

Asserts:
  1. style.css estate scroll-margin rule covers tr[id] + th[id] (the r80
     formula extension) — byte-exact selector line.
  2. comparison.html carries both r84 :target ring rules (row + column).
  3. comparison.html carries the fonts-ready retarget script (deterministic
     landing despite the r68 scrollIntoView racing webfont load).
  4. Anti-churn: features page-local margins (140px desktop / 300px mobile),
     features tr:target rings, pricing .pricing-card:target — all untouched.
  5. Estate inventory sanity: comparison has exactly 11 tbody tr[id] and
     5 thead th[id]; features has 5 tr[id]; the r80 formula comment marker.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []


def check(name, cond, detail=""):
    if cond:
        print(f"  PASS  {name}")
    else:
        failures.append(name)
        print(f"  FAIL  {name}  {detail}")


style = (ROOT / "style.css").read_text(encoding="utf-8")
comp = (ROOT / "comparison.html").read_text(encoding="utf-8")
feat = (ROOT / "features.html").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")

print("== 1. style.css estate rule (r80 formula + r84 extension) ==")
check(
    "estate selector covers tr[id] and th[id]",
    "section[id], div[id], tr[id], th[id] { scroll-margin-top: calc(var(--nav-h, 120px) + 50px); }" in style,
    "byte-exact rule line missing",
)
check("r84 comment marker present", "r84: tr[id] (comparison's 11 deep-linked rows" in style)
check("r80 ResizeObserver comment intact", "measures the real .navbar into --nav-h (ResizeObserver, r80)" in style)

print("== 2. comparison.html :target rings ==")
check("row ring rule", ".comp-table-wrap tbody tr:target{box-shadow:0 0 0 3px rgba(var(--accent-rgb),.28);}" in comp)
check("column ring rule", ".comp-table-wrap thead th:target{box-shadow:0 0 0 3px rgba(var(--accent-rgb),.28);}" in comp)
check("r84 ring comment marker", "r84: :target ring parity" in comp)

print("== 3. comparison.html fonts-ready retarget ==")
check("guards col-/row- hashes only", "if (!/^#(col-|row-)/.test(location.hash)) return;" in comp)
check("re-fires hashchange after fonts", "document.fonts.ready.then(function(){ setTimeout(retarget, 60); })" in comp)
check("fallback timeout branch", "setTimeout(retarget, 350)" in comp)

print("== 4. anti-churn (r78/r79 verified surfaces untouched) ==")
check("features desktop margin 140", ".feat-table tr[id], .feat-note[id] { scroll-margin-top: 140px; }" in feat)
check("features mobile margin 300", "scroll-margin-top: 300px" in feat)
check("features row ring", ".feat-table tr:target { box-shadow: 0 0 0 3px rgba(var(--accent-rgb), .28); }" in feat)
check("pricing card ring", ".pricing-card:target{border-color:var(--accent);box-shadow:0 0 0 3px rgba(var(--accent-rgb),.28)}" in pricing)
check("faq tint rule intact", ".faq-item:target {" in style)

print("== 5. inventory sanity ==")
rows = re.findall(r'<tr id="row-[a-z-]+">', comp)
cols = re.findall(r'<th scope="col"[^>]* id="col-[a-z-]+">', comp)
frows = re.findall(r'<tr id="feat-[a-z-]+">', feat)
check("comparison 11 deep-linked rows", len(rows) == 11, f"found {len(rows)}")
check("comparison 5 deep-linkable columns", len(cols) == 5, f"found {len(cols)}")
check("features 5 deep-linked rows", len(frows) == 5, f"found {len(frows)}")

print()
if failures:
    print(f"check_r84: {len(failures)} FAILURE(S): {failures}")
    sys.exit(1)
print("check_r84: ALL PASS")
