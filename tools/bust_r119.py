#!/usr/bin/env python3
"""r119 sweep: bump cache busters across all 15 pages.
i18n.js   v65 -> v66 (es/fr translation-debt fix: 49 stale-English values
          replaced with real translations across 27 keys)
style.css v58 stays (no style changes this round — verified)
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
    pre_s, pre_i = t.count('style.css?v=58'), t.count('i18n.js?v=65')
    if pre_s != 1: errs.append(f"{page}: pre style.css?v=58 x{pre_s} (want 1)")
    if pre_i != 1: errs.append(f"{page}: pre i18n.js?v=65 x{pre_i} (want 1)")
    t = t.replace('i18n.js?v=65', 'i18n.js?v=66')
    post_s, post_i = t.count('style.css?v=58'), t.count('i18n.js?v=66')
    if post_s != 1: errs.append(f"{page}: post style.css?v=58 x{post_s}")
    if post_i != 1: errs.append(f"{page}: post i18n.js?v=66 x{post_i}")
    for stale in ('i18n.js?v=63', 'i18n.js?v=64', 'i18n.js?v=65'):
        if t.count(stale): errs.append(f"{page}: stale {stale} residue")
    p.write_text(t, encoding='utf-8')

if errs:
    print("bust_r119: FAILURES:")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"bust_r119: OK — i18n v65 -> v66 across {len(PAGES)} pages (style v58 carried)")
