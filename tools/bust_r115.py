#!/usr/bin/env python3
"""r115 sweep: bump cache busters across all 15 pages.
style.css v57 -> v58 (heading ids join the anchor-offset scroll-margin rule)
i18n.js   v65 stays (no i18n changes this round — verified)
Idempotent: verifies pre-state x1 each, post-state x1 each, zero stale residue.
"""
import sys
from pathlib import Path

ROOT = Path('/home/z/my-project/nullvpn-site')
PAGES = ["404.html", "comparison.html", "contact.html", "download.html", "faq.html",
         "features.html", "how-it-works.html", "index.html", "offline.html",
         "pricing.html", "privacy.html", "refund.html", "success.html", "terms.html",
         "web3.html"]

errs = []
for page in PAGES:
    p = ROOT / page
    t = p.read_text(encoding='utf-8')
    pre_s, pre_i = t.count('style.css?v=57'), t.count('i18n.js?v=65')
    stale_s, stale_i = t.count('style.css?v=58'), t.count('i18n.js?v=66')
    if pre_s != 1 or pre_i != 1 or stale_s or stale_i:
        errs.append(f'{page}: pre v57={pre_s} v65={pre_i} '
                    f'stale v58={stale_s} v66={stale_i} — skip')
        continue
    t = t.replace('style.css?v=57', 'style.css?v=58')
    post_s, post_i = t.count('style.css?v=58'), t.count('i18n.js?v=65')
    res_s, res_i = t.count('style.css?v=57'), t.count('i18n.js?v=66')
    if post_s != 1 or post_i != 1 or res_s or res_i:
        errs.append(f'{page}: POST BAD v58={post_s} v65={post_i} res={res_s}/{res_i}')
        continue
    p.write_text(t, encoding='utf-8')

if errs:
    print('bust_r115: FAILURES:')
    for e in errs:
        print('  -', e)
    sys.exit(1)
print(f'bust_r115: OK ({len(PAGES)} pages) style v57->v58, i18n v65 carried')
