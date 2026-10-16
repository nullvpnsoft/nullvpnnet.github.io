#!/usr/bin/env python3
"""Generate tools/check_r122.py from check_r121.py: swap the docstring,
add the download-hero nv-l hide gate, relabel output. Version pins carried
(i18n v67 / style v58 — HTML-inline round, no asset bytes changed).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r121.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r122 guards: download-hero nv-l hide (estate CLS ritual, round 2).

(Carries the full r44-r121 chain, regenerated from check_r121.py; the r121
locale-bootstrap + navbar-reveal contract, r118 value-quality, r119
Latin-locale and r120 sibling-identity gates all remain in force.)

SHIP (CLS ritual follow-up): the r121-recommended per-round ?perf=1 estate
sweep (15 pages x fa + ar/ne spot checks) found ONE residual shift class:
download.html hero CTA row (.dh-cta inline <p>: btn-primary + btn-ghost +
share-chip + .dh-note) re-wraps when the post-paint applyLang() swap swaps
EN->locale labels (fa CLS 0.018-0.022 on 2/5 warm loads, ne 0.018 on 1/1
hunted run; sources A.btn-ghost/A.btn-primary/P.dh-note/BUTTON.share-chip
at ~200-380ms). Every other page x every tested locale: CLS 0.000-0.003.

web3.html HUD/dir anomalies in the same sweep were FALSE ALARMS: web3 is a
deliberate 1500ms bridge-redirect to tonviewer.com (CF RUM/CrUX comment in
source, r74 cancel control) — the probe followed the redirect, so dir/lang/
storage/HUD readings came from the cross-origin target. No site defect.

Fix: download.html's inline r121 rule extended from
html.nv-l .nav-inner{visibility:hidden}
to also hide .dh-cta/.dh-note under html.nv-l — layout-preserving, revealed
by the same applyLang() nv-l removal (2s failsafe unchanged). en path and
LCP untouched (h1/dh-sub stay visible; buttons verified visible post-reveal
with localized labels).
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r122 asserts before the versions section
r122_block = '''
# --- r122 ship asserts (download-hero nv-l hide) --------------------------------------------------
_dh = (ROOT / "download.html").read_text(encoding="utf-8")
ok('html.nv-l .nav-inner{visibility:hidden}html.nv-l .dh-cta,html.nv-l .dh-note{visibility:hidden}' in _dh,
   "download.html: r122 extended hero-hide rule missing (dh-cta/dh-note)")
for _p in PAGES:
    if _p == "download.html":
        continue
    _t122 = (ROOT / _p).read_text(encoding="utf-8")
    ok(_t122.count("html.nv-l .dh-cta") == 0,
       _p + ": download-only hero-hide rule leaked onto " + _p)

'''
anchor = "\n# --- versions"
assert anchor in out, "versions anchor not found"
out = out.replace(anchor, r122_block + anchor, 1)

# 3) no version changes this round (HTML inline only).

# 4) relabel
out = out.replace('print("check_r121: FAILURES:")', 'print("check_r122: FAILURES:")')
out = out.replace('print(f"check_r121: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r122: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r122.py").write_text(out, encoding="utf-8")
print("check_r122.py written:", len(out), "bytes")
