#!/usr/bin/env python3
"""r83 contrast audit — WCAG 2.1 ratios for every text/surface pair in style.css.
AA: >= 4.5 normal text, >= 3.0 large text (>=24px or >=18.66px bold)."""
def lum(hexc):
    hexc = hexc.lstrip('#')
    r, g, b = (int(hexc[i:i+2], 16)/255 for i in (0, 2, 4))
    f = lambda c: c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)

def ratio(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1+0.05)/(l2+0.05)

themes = {
    'LIGHT': {'bg':'#f7e7ce','bg2':'#fef9f0','bg3':'#f0e2c7',
              'text':'#1f1a12','text2':'#6a5a39','accent-text':'#1d4ed8',
              'accent':'#3b82f6','accent2':'#2563eb','accent3':'#1d4ed8'},
    'DARK':  {'bg':'#0a0f1a','bg2':'#0f172a','bg3':'#1e293b',
              'text':'#f1f5f9','text2':'#94a3b8','accent-text':'#60a5fa',
              'accent':'#3b82f6','accent2':'#2563eb','accent3':'#1d4ed8'},
}
fails = []
for tname, v in themes.items():
    print(f"=== {tname} ===")
    pairs = [(f, s) for f in ('text','text2','accent-text') for s in ('bg','bg2','bg3')]
    pairs += [('white','accent'), ('white','accent2'), ('white','accent3'),
              ('accent-text','accent'), ('white','text2')]
    for f, s in pairs:
        fg = '#ffffff' if f == 'white' else v[f]
        r = ratio(fg, v[s])
        flag = 'PASS' if r >= 4.5 else ('LARGE-ONLY' if r >= 3.0 else 'FAIL')
        if flag != 'PASS':
            fails.append((tname, f, s, r, flag))
        print(f"  {f:>12} on {s:<10} {r:5.2f}  {flag}")
print("\n=== NON-PASSING ===")
for t, f, s, r, fl in fails:
    print(f"  {t}: {f} on {s} = {r:.2f} ({fl})")
