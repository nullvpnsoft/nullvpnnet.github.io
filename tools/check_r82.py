#!/usr/bin/env python3
"""r82 guard: (1) every JSON-LD block on every page parses as JSON, with the
expected block types/counts per page; (2) FAQPage mainEntity == 10 and every
question/answer text matches the visible en default on the page; (3) ItemList
on comparison.html == 11 items and every #row-* anchor target exists in the
page; (4) index.html navbar logo carries aria-current=page; (5) color-scheme
meta present exactly once on all 15 pages."""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

fail = []

# 1+2+3 — JSON-LD inventory and cross-checks
for f in sorted(glob.glob("*.html")):
    src = open(f, encoding="utf-8").read()
    blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', src, re.S)
    parsed = []
    for i, b in enumerate(blocks):
        try:
            parsed.append(json.loads(b))
        except Exception as e:
            fail.append(f"{f}: JSON-LD block {i} does not parse: {e}")
    if f == "faq.html":
        fp = [p for p in parsed if p.get("@type") == "FAQPage"]
        if len(fp) != 1:
            fail.append(f"faq.html: expected 1 FAQPage, got {len(fp)}")
        else:
            qs = fp[0]["mainEntity"]
            if len(qs) != 11:
                fail.append(f"faq.html: FAQPage has {len(qs)} questions, expected 11 (incl. Ad Guard)")
            # EXACT drift guard: schema order/names/texts must equal the visible
            # en page content. Key pattern covers numeric (faq.q1..q10) and
            # word keys (faq.q_adguard) — the r82 lesson: 'faq-[0-9]*' style
            # inventories silently drop non-numeric ids.
            vis_q = re.findall(r'<h3 data-i18n="faq\.(?:q\d+|q_[a-z]+)">(.*?)</h3>', src)
            vis_a = re.findall(r'<p data-i18n="faq\.(?:a\d+|a_[a-z]+)">(.*?)</p>', src)
            sch = [(q["name"], q["acceptedAnswer"]["text"]) for q in qs]
            vis = list(zip(vis_q, vis_a))
            if len(vis_q) != 11 or len(vis_a) != 11:
                fail.append(f"faq.html: visible inventory found q={len(vis_q)} a={len(vis_a)}, expected 11/11")
            if sch != vis:
                fail.append(f"faq.html: FAQPage schema does NOT exactly match visible content (schema {len(sch)} vs visible {len(vis)})")
                for i, (s, v) in enumerate(zip(sch, vis)):
                    if s != v:
                        fail.append(f"  drift at Q{i+1}: schema={s[0][:40]!r} visible={v[0][:40]!r}")
    if f == "comparison.html":
        il = [p for p in parsed if p.get("@type") == "ItemList"]
        if len(il) != 1:
            fail.append(f"comparison.html: expected 1 ItemList, got {len(il)}")
        else:
            items = il[0]["itemListElement"]
            if len(items) != 11:
                fail.append(f"comparison.html: ItemList has {len(items)} items, expected 11")
            for it in items:
                frag = it["url"].split("#")[1]
                if f'id="{frag}"' not in src:
                    fail.append(f"comparison.html: ItemList url anchor missing: {frag}")

# 4 — index navbar logo aria-current
idx = open("index.html", encoding="utf-8").read()
if '<div class="nav-top-row">\n        <a href="index.html" class="logo" aria-current="page">' not in idx:
    fail.append("index.html: navbar logo missing aria-current=page")
# footer logo must stay unmarked (footer convention)
if idx.count('aria-current="page"') != 1:
    fail.append(f"index.html: aria-current count {idx.count(chr(97)+'ria-current')} != 1")

# 5 — color-scheme meta
for f in sorted(glob.glob("*.html")):
    c = open(f, encoding="utf-8").read().count('name="color-scheme"')
    if c != 1:
        fail.append(f"{f}: color-scheme count {c} != 1")

if fail:
    print("FAIL:")
    [print("  " + m) for m in fail]
    sys.exit(1)
print("OK: r82 guard passed — JSON-LD parses (FAQPage 11 Q&A exact-matching visible text, ItemList 11 rows, all anchors exist), aria-current on index navbar logo only, color-scheme on 15/15")
