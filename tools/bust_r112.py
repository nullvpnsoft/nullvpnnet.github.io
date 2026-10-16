#!/usr/bin/env python3
"""r112 sweep: bump cache busters across all 15 pages.
style.css v55 stays (no style changes this round — verified)
i18n.js   v64 -> v65 (dl.meta.stable key + release-grid re-render hook)
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
    pre_s, pre_i = t.count('style.css?v=56'), t.count('i18n.js?v=64')
    stale_s, stale_i = t.count('style.css?v=57'), t.count('i18n.js?v=65')
    if pre_s != 1 or pre_i != 1 or stale_s or stale_i:
        errs.append(f'{page}: pre v56={pre_s} v64={pre_i} '
                    f'stale v57={stale_s} v65={stale_i} — skip')
        continue
    t = t.replace('i18n.js?v=64', 'i18n.js?v=65')
    post_s, post_i = t.count('style.css?v=56'), t.count('i18n.js?v=65')
    res_s, res_i = t.count('style.css?v=57'), t.count('i18n.js?v=64')
    if post_s != 1 or post_i != 1 or res_s or res_i:
        errs.append(f'{page}: POST BAD v56={post_s} v65={post_i} res={res_s}/{res_i}')
        continue
    p.write_text(t, encoding='utf-8')
    print(f'{page}: v56/v65 OK')

if errs:
    print('SWEEP FAILURES:')
    [print(' -', e) for e in errs]
    sys.exit(1)
print(f'bust_r112: ALL {len(PAGES)} pages now style v56 / i18n v65')
