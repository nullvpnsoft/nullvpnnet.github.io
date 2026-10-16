#!/usr/bin/env python3
"""r117 audit: theme-system uniformity across the estate (read-only)."""
import glob
import re
from pathlib import Path

ROOT = Path('/home/z/my-project/nullvpn-site')
rows = []
for f in sorted(glob.glob(str(ROOT / '*.html'))):
    t = Path(f).read_text(encoding='utf-8')
    name = Path(f).name
    st = len(re.findall(r'function setTheme\(', t))
    oc_l = t.count("onclick=\"setTheme('light')\"")
    oc_d = t.count("onclick=\"setTheme('dark')\"")
    ub = len(re.findall(r'updateThemeButtons\(', t))
    init = t.count("localStorage.getItem('theme')")
    rows.append((name, st, oc_l, oc_d, ub, init))

w = max(len(r[0]) for r in rows)
print(f"{'page'.ljust(w)}  def light dark upd init")
for name, st, ol, od, ub, ini in rows:
    print(f"{name.ljust(w)}  {st:3} {ol:5} {od:4} {ub:3} {ini:4}")
