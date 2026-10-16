#!/usr/bin/env python3
"""r108 sweep: bump cache busters across all 15 pages.
style.css v54 -> v55 (reduced-transparency block added)
i18n.js   v60 -> v61 (2c slash-shortcut handler added)
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
    pre_s, pre_i = t.count('style.css?v=54'), t.count('i18n.js?v=60')
    stale_s, stale_i = t.count('style.css?v=55'), t.count('i18n.js?v=61')
    if pre_s != 1 or pre_i != 1 or stale_s or stale_i:
        errs.append(f'{page}: pre v54={pre_s} v60={pre_i} '
                    f'stale v55={stale_s} v61={stale_i} — skip')
        continue
    t = t.replace('style.css?v=54', 'style.css?v=55')
    t = t.replace('i18n.js?v=60', 'i18n.js?v=61')
    post_s, post_i = t.count('style.css?v=55'), t.count('i18n.js?v=61')
    res_s, res_i = t.count('style.css?v=54'), t.count('i18n.js?v=60')
    if post_s != 1 or post_i != 1 or res_s or res_i:
        errs.append(f'{page}: POST BAD v55={post_s} v61={post_i} res={res_s}/{res_i}')
        continue
    p.write_text(t, encoding='utf-8')
    print(f'{page}: v55/v61 OK')

if errs:
    print('SWEEP FAILURES:')
    [print(' -', e) for e in errs]
    sys.exit(1)
print(f'sweep_r108: ALL {len(PAGES)} pages bumped to style v55 / i18n v61')
