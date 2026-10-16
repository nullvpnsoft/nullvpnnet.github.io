#!/usr/bin/env python3
"""r114 audit: estate-wide heading hierarchy + link-purpose lens.
Read-only; prints findings. Headings: per page, sequence of h1-h6 in document
order; flags (a) multiple/zero h1, (b) skipped levels (h1->h3 etc.), both
classic a11y-audit (WCAG 1.3.1 / 2.4.6) heuristics. Link purpose: anchors
with no text content AND no aria-label AND no img child with alt -> flags
(WCAG 2.4.4). data-i18n attributes count as text-bearing (populated at load).
"""
import re
from pathlib import Path

ROOT = Path('/home/z/my-project/nullvpn-site')
PAGES = ["404.html", "comparison.html", "contact.html", "download.html", "faq.html",
         "features.html", "how-it-works.html", "index.html", "offline.html",
         "pricing.html", "privacy.html", "refund.html", "success.html", "terms.html",
         "web3.html"]

HDR_RE = re.compile(r'<h([1-6])[\s>]', re.I)
A_RE = re.compile(r'<a\b[^>]*>(.*?)</a>', re.S | re.I)

issues = []
for page in PAGES:
    t = (ROOT / page).read_text(encoding='utf-8')
    body = t[t.index('<body'):] if '<body' in t else t

    # heading sequence in document order
    levels = [int(m.group(1)) for m in HDR_RE.finditer(body)]
    h1 = levels.count(1)
    if h1 != 1:
        issues.append(f'{page}: h1 count = {h1}')
    prev = None
    for lv in levels:
        if prev is not None and lv > prev + 1:
            issues.append(f'{page}: skipped level h{prev}->h{lv}')
        prev = lv

    # link purpose: anchors with no text and no accessible name
    for m in A_RE.finditer(body):
        attrs, inner = m.group(0), m.group(1)
        text = re.sub(r'<[^>]+>', '', inner).strip()
        if text:
            continue
        has_label = 'aria-label=' in attrs
        has_i18n = 'data-i18n' in attrs
        has_alt_img = re.search(r'<img[^>]*alt="[^"]+"', inner, re.I)
        has_ico = 'aria-hidden="true"' in inner  # icon-only with hidden deco: still needs a name
        if not has_label and not has_i18n and not has_alt_img:
            issues.append(f'{page}: unnamed link: {attrs[:110]}')

if issues:
    print(f'r114 audit: {len(issues)} finding(s)')
    for i in issues:
        print('  -', i)
else:
    print('r114 audit: CLEAN (headings + link purpose, 15 pages)')
