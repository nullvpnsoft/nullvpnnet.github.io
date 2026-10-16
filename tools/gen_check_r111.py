#!/usr/bin/env python3
"""Generate tools/check_r111.py from check_r110.py: swap the docstring,
inject r111 ship asserts before the versions section, fix the final label."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r110.py").read_text(encoding="utf-8")

old_doc = '''#!/usr/bin/env python3
"""r110 guards: how-it-works step anchors + no-JS story sync.

(Carries the full r44-r107 chain, regenerated from check_r107.py; r107 ship asserts remain in force below.)

SHIP 1 (x15 pages, SEO-sweep feature): og:image carried no enrichment — added
og:image:width 1200 / height 630 (dimensions verified by JPEG SOF parse of
og-cover.jpg, so crawlers skip re-probing), og:image:alt + twitter:image:alt
(social-preview accessibility, image described from actual content: NullVPN
wordmark + tagline on navy/gold waves).

SHIP 2 (pricing.html, styling detail): .checkout-plan was the last primary
control without press feedback — :active scale(.95) mirrors the
.faq-cat/.copy-chip tactile language, transform .12s ease joins the chip
transition, and the r101-era reduced-motion gate already zeroes it.

HTML-only round: style.css stays v54, i18n.js stays v60 — no buster; the
guard asserts the carried pins and the full r44-r106 chain.
"""'''

new_doc = '''#!/usr/bin/env python3
"""r111 guards: web3.html noscript honesty layer.

(Carries the full r44-r110 chain, regenerated from check_r110.py; r110 ship asserts remain in force below.)

SHIP (web3.html, audit fix — spot-audit round covered comparison / offline /
web3 / contact; only web3 had a real gap): the bridge's whole function is a
JS timer, and with scripting off the spinner span forever, the progress row
kept promising "Connecting to TON…", and the cancel/share controls sat dead.
The noscript layer: head <noscript><style> hides the spinner, the redirecting
text span (via :not(#web3Cancelled) — a CSS copy of the data-i18n attribute
string would be counted as a real i18n usage by check_html_i18n, r111
count-hygiene note), and the dead cancel/share controls; a body
<noscript><p class="web3-nojs"> stands in with the truth and points at the
manual mirror link. .web3-nojs mirrors .dl-progress rhythm so the swap
doesn't shift the layout grammar. EN-only by construction — the i18n engine
cannot run without JS (same convention as the r110 fallback sync).

HTML-only round: style.css stays v56, i18n.js stays v64 — no buster; the
guard asserts the carried pins and the full r44-r110 chain.
"""'''

assert old_doc in src, "docstring anchor not found"
out = src.replace(old_doc, new_doc)

r111_block = '''
# --- r111 ship asserts (web3.html noscript honesty) --------------------------------------------
_w3 = (ROOT / "web3.html").read_text(encoding="utf-8")
ok(_w3.count("</noscript>") == 2, "web3.html: noscript blocks x!=2 (head style + body note; opening-tag comment mentions excluded by matching the closer)")
ok(_w3.count(".dl-spinner { display: none; }") == 1,
   "web3.html: noscript spinner hide x!=1")
ok(_w3.count(".dl-progress span:not(#web3Cancelled) { display: none; }") == 1,
   "web3.html: noscript redirecting-span hide x!=1")
ok(_w3.count("count-hygiene note") == 1,
   "web3.html: r111 count-hygiene comment missing")
ok(_w3.count("#web3Cancel, .web3-actions .share-chip { display: none; }") == 1,
   "web3.html: noscript dead-control hides x!=1")
ok(_w3.count('<noscript><p class="web3-nojs">') == 1,
   "web3.html: noscript note p missing (precise: only the real element opens with the tag)")
ok(_w3.count("JavaScript is off") == 1, "web3.html: noscript note text missing")
ok(_w3.count("the automatic redirect can&rsquo;t run") == 1,
   "web3.html: noscript note verb missing (shipped as rsquo entity)")
ok(".web3-nojs { display: flex;" in _w3,
   "web3.html: .web3-nojs styling missing from page style block")
ok(_w3.count("r111: noscript honesty") == 1, "web3.html: r111 head comment missing")
ok(_w3.count("r111: scripting-off note") == 1, "web3.html: r111 body comment missing")

'''
anchor = "\n# --- versions (r107: HTML-only round"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r111_block + anchor)

out = out.replace('print("check_r107: FAILURES:")', 'print("check_r111: FAILURES:")')
out = out.replace('print(f"check_r107: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r111: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r111.py").write_text(out, encoding="utf-8")
print("check_r111.py written:", len(out), "bytes")
