#!/usr/bin/env python3
"""r91 guards: success-page long-ID overflow fix, RFC 9116 security.txt
(both RFC paths, factual fields only, Expires < 1 year), @page print
margins, plus the standing anti-churn surface (r88/r89/r90 + r45 canary).
Run BEFORE bust (v42 pre-asserts) and again AFTER bust (v43 post-asserts).
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "404.html", "comparison.html", "contact.html", "download.html", "faq.html",
    "features.html", "how-it-works.html", "index.html", "offline.html",
    "pricing.html", "privacy.html", "refund.html", "success.html", "terms.html",
    "web3.html",
]

errs = []
def ok(cond, msg):
    if not cond:
        errs.append(msg)

# --- SHIP 1: success.html overflow fix -------------------------------------
s = (ROOT / "success.html").read_text(encoding="utf-8")
ok(".success-details .row .value{font-weight:600;color:var(--text);font-size:.9rem;overflow-wrap:anywhere;min-width:0}" in s,
   "success.html: value rule missing overflow-wrap:anywhere")
ok(".success-details .row .paywrap{display:flex;align-items:center;gap:8px;flex-wrap:wrap;row-gap:4px}" in s,
   "success.html: paywrap rule missing flex-wrap")
ok("r91: payment IDs can be 64+ char hex hashes" in s, "success.html: r91 comment missing")
ok("/* r77: expose the copy chip only when a real payment ID arrived" in s, "success.html: r77 comment churned")
ok('if(planKeyMap[plan])' in s and "textContent=pid" in s, "success.html: param fallback logic churned")

# --- SHIP 2: security.txt (RFC 9116) ---------------------------------------
wellknown = (ROOT / ".well-known" / "security.txt").read_text(encoding="utf-8")
rootcopy = (ROOT / "security.txt").read_text(encoding="utf-8")
ok(wellknown == rootcopy, "security.txt: /.well-known and root copies differ")
ok(wellknown.count("Contact: ") == 2, "security.txt: expected exactly 2 Contact fields")
ok("Contact: mailto:support@nullvpn.net" in wellknown, "security.txt: mailto contact missing")
ok("Contact: https://t.me/nullvpn_net" in wellknown, "security.txt: telegram contact missing")
ok("Preferred-Languages: en, ru, fa, ar, es, ne, fr" in wellknown, "security.txt: Preferred-Languages wrong")
ok("Canonical: https://nullvpn.net/.well-known/security.txt" in wellknown, "security.txt: Canonical wrong")
ok("Policy: https://nullvpn.net/terms.html" in wellknown, "security.txt: Policy wrong")
for banned in ("Encryption:", "Hiring:", "CSAF:", "Acknowledgments:", "lang:"):
    ok(banned not in wellknown, f"security.txt: fabricated/unsupported field {banned!r}")
exp_line = next(l for l in wellknown.splitlines() if l.startswith("Expires:"))
exp_dt = datetime.fromisoformat(exp_line.split(" ", 1)[1].replace("Z", "+00:00"))
now = datetime.now(timezone.utc)
ok(exp_dt > now, "security.txt: Expires already in the past")
ok((exp_dt - now).days < 365, "security.txt: Expires must be < 1 year out (RFC 9116)")

# --- SHIP 3: @page print margins -------------------------------------------
css = (ROOT / "style.css").read_text(encoding="utf-8")
ok(css.count("@page { margin: 14mm 12mm; }") == 1, "style.css: @page rule count != 1")
ok(css.count("r91: explicit paper margins") == 1, "style.css: r91 comment count != 1")

# --- anti-churn: standing surfaces ------------------------------------------
ok(css.count("idden]") >= 6, "style.css: r45 [hidden]-guard family regressed (canary)")
ok(":root { accent-color: var(--accent); }" in css, "style.css: r89 accent-color churned")
ok("section, main { padding: 14px 0 !important; }" in css, "style.css: r90 print parity churned")
ok("/* r90: borders join the lift" in css and "--border: #8f7448" in css, "style.css: r90 contrast block churned")
idx = (ROOT / "index.html").read_text(encoding="utf-8")
ok('<main id="main"' in idx and '<section id="main"' not in idx, "index.html: r90 main landmark churned")
ok('"@type": "SoftwareApplication"' in idx, "index.html: r88 SoftwareApplication churned")
comp = (ROOT / "comparison.html").read_text(encoding="utf-8")
ok('<caption data-i18n="comp.table.caption">' in comp, "comparison.html: r88 caption churned")
man = (ROOT / "site.webmanifest").read_text(encoding="utf-8")
ok(man.count("manifest-shot-") == 2, "site.webmanifest: r89 screenshots churned")

# --- versions ----------------------------------------------------------------
if "--post-bust" in sys.argv:
    want_s, want_i = "style.css?v=43", "i18n.js?v=53"
else:
    want_s, want_i = "style.css?v=42", "i18n.js?v=53"
for page in PAGES:
    t = (ROOT / page).read_text(encoding="utf-8")
    ok(t.count(want_s) == 1, f"{page}: expected {want_s} x1")
    ok(t.count(want_i) == 1, f"{page}: expected {want_i} x1")

if errs:
    print("check_r91: FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print(f"check_r91: ALL GREEN ({'post' if '--post-bust' in sys.argv else 'pre'}-bust, {len(PAGES)} pages)")
