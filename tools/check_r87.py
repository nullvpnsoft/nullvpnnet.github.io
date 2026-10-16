#!/usr/bin/env python3
"""r87 guard: ?lang= deep link, llms.txt, scrollbar parity + anti-churn.

Anti-churn surfaces: r86 permalink chips (pricing/features), r84 estate
scroll-margin formula, r85 keyboard-scrollable regions, r82 ItemList,
print block, ::selection, webkit scrollbar block (must coexist, not be
replaced, by the r87 standard properties).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
fails = []


def need(cond, msg):
    if not cond:
        fails.append(msg)


i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")
style = (ROOT / "style.css").read_text(encoding="utf-8")
pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
features = (ROOT / "features.html").read_text(encoding="utf-8")
comparison = (ROOT / "comparison.html").read_text(encoding="utf-8")
faq = (ROOT / "faq.html").read_text(encoding="utf-8")

# ---- Ship 1: ?lang= deep link -------------------------------------------
need("r87: ?lang= deep link" in i18n, "i18n: missing r87 comment")
need("new URLSearchParams(location.search).get('lang')" in i18n, "i18n: no ?lang read")
need("Object.prototype.hasOwnProperty.call(T['nav.home'], qp)" in i18n,
     "i18n: qp not hasOwnProperty-validated (prototype-key hole)")
need("localStorage.setItem(STORAGE_KEY, qp)" in i18n, "i18n: ?lang not persisted")
need("u.searchParams.delete('lang')" in i18n, "i18n: param not stripped")
need("history.replaceState" in i18n, "i18n: no replaceState strip")
need("u.pathname + u.search + u.hash" in i18n, "i18n: strip loses sibling params/hash")
# entire branch inside try/catch (old WebViews) — the qp read must sit in a
# guarded function: count try blocks around getLang is brittle; instead assert
# the catch immediately following the branch exists.
need("no URLSearchParams/URL (old WebViews): fall through" in i18n,
     "i18n: ?lang branch missing old-WebView catch")
# localStorage read + browser sniff still present after the new branch
need("localStorage.getItem(STORAGE_KEY)" in i18n, "i18n: localStorage read gone")
need("navigator.language" in i18n, "i18n: browser sniff gone")

# ---- Ship 2: llms.txt ----------------------------------------------------
lt = ROOT / "llms.txt"
need(lt.exists(), "llms.txt missing")
if lt.exists():
    t = lt.read_text(encoding="utf-8")
    need(t.startswith("# NullVPN\n"), "llms.txt: missing H1 first line")
    need("\n> " in t, "llms.txt: missing blockquote summary")
    for u in ["https://nullvpn.net/", "features.html", "pricing.html",
              "comparison.html", "how-it-works.html", "download.html",
              "web3.html", "faq.html", "contact.html", "terms.html",
              "privacy.html", "refund.html"]:
        need(u in t, f"llms.txt: missing URL {u}")
    need("t.me/nullvpn_net" in t and "support@nullvpn.net" in t and
         "t.me/nullvpnnetbot" in t, "llms.txt: support contacts incomplete")
    for code in ["en", "ru", "fa", "ar", "es", "ne", "fr"]:
        need(code in t, f"llms.txt: missing lang code {code}")
    need("?lang=xx" in t, "llms.txt: ?lang= undocumented")

# ---- Ship 3: scrollbar parity -------------------------------------------
need("html { scrollbar-width: thin; scrollbar-color: var(--border) transparent; }" in style,
     "style: r87 standard scrollbar rule missing/altered")
need("r87: standard scrollbar properties" in style, "style: missing r87 comment")
# anti-churn: webkit block coexists
need("::-webkit-scrollbar { width: 6px; height: 6px; }" in style,
     "style: webkit scrollbar block was removed (must coexist)")
need("::selection { background: rgba(var(--accent-rgb), 0.28); }" in style,
     "style: ::selection rule churned")

# ---- anti-churn: prior rounds --------------------------------------------
need("section[id], div[id], tr[id], th[id] { scroll-margin-top: calc(var(--nav-h, 120px) + 50px); }" in style,
     "style: r84 estate scroll-margin formula churned")
need("makePermalinkChip" in i18n, "i18n: r86 chip engine churned")
need('id="plan-annual"' in pricing and 'id="plan-monthly"' in pricing,
     "pricing: plan anchors churned")
need("#feat-accessibility" in features, "features: r86 chip targets churned")
need('id="row-nologs"' in comparison, "comparison: r84 row ids churned")
need('id="col-protonvpn"' in comparison, "comparison: r84 col ids churned")
need("fonts.ready" in comparison, "comparison: r84 fonts-ready retarget churned")
need("tabindex" in i18n, "i18n: r85 keyboard-scrollable engine churned")
need("faqFilter" in i18n, "i18n: FAQ filter engine churned")

# ---- versions ------------------------------------------------------------
for page in ["index.html", "pricing.html", "faq.html"]:
    t = (ROOT / page).read_text(encoding="utf-8")
    need("i18n.js?v=52" in t, f"{page}: i18n not v52")
    need("style.css?v=40" in t, f"{page}: style not v40")

if fails:
    print("check_r87: FAILED")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("check_r87: ALL PASS (ships + anti-churn + versions)")
