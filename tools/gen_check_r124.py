#!/usr/bin/env python3
"""Generate tools/check_r124.py from check_r123.py: swap the docstring,
add the r124 404 telegram-rescue gate, relabel output. Buster pins carried
(i18n v68 / style v58 — 404.html inline JS only).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "check_r123.py").read_text(encoding="utf-8")

# 1) docstring swap
start = src.index('"""')
end = src.index('"""', start + 3) + 3
new_doc = """#!/usr/bin/env python3
\"\"\"r124 guards: 404 rescue aliases for the Telegram surface.

(Carries the full r44-r123 chain, regenerated from check_r123.py; the r123
HUD-context gate, r122 download-hero hide, r121 locale-bootstrap contract,
r118-r120 value-quality gates all remain in force.)

SHIP (small real feature): the r79 404 rescue MAP matched 34 aliases but
missed the brand's PRIMARY support channel — a visitor guessing /telegram,
/tg, /bot or /channel (all highly plausible dead paths for a Telegram-first
service) got no suggest box. contact.html carries dedicated Support / Bot /
Channel cards, so all four aliases rescue there with the nav.contact label.
Short aliases sit AFTER the specific contact/support rows (first-match-wins,
same rule as the r81 pricing block). Matching logic verified in isolation
(node harness): /telegram /tg /bot /channel /telegramx /my-bot-help
/news-channel -> contact; /pricingx /downloadx unregressed; unknown paths
still render no suggest. No buster bump (404.html is network-first HTML).

QA this round: re-lens of the r118 quartet (contact/offline/web3/404) ALL
CLEAN incl. true share-chip E2E and the web3 cancel control; ar full 15-page
perf sweep (the last locale without one — fa/ru/ar now full-cycle; ne still
spot-checks only, next round) CLS 0.000-0.004; regression contracts
(features deep-link 140>109, h2 slugs, index cap/feat cards) hold.
\"\"\""""

out = src[:start] + new_doc + src[end:]

# 2) r124 asserts before the r123 block
r124_block = '''
# --- r124 ship asserts (404 telegram rescue aliases) -----------------------------------------------
_nf124 = (ROOT / "404.html").read_text(encoding="utf-8")
for _row in ["['telegram',     '/contact.html',      'nav.contact']",
             "['channel',      '/contact.html',      'nav.contact']",
             "['tg',           '/contact.html',      'nav.contact']",
             "['bot',          '/contact.html',      'nav.contact']"]:
    ok(_nf124.count(_row) == 1, "404.html: r124 rescue alias row missing: " + _row)
ok(_nf124.count("r124: the Telegram surface") == 1, "404.html: r124 rescue comment missing")
# ordering contract: the specific contact rows precede the short aliases (first-match-wins)
_ok_contact = _nf124.find("['contact',")
_ok_tg = _nf124.find("['tg',")
_ok_bot = _nf124.find("['bot',")
ok(_ok_contact != -1 and _ok_tg != -1 and _ok_bot != -1 and _ok_contact < _ok_tg < _ok_bot,
   "404.html: r124 alias ordering broken (specific rows must precede short aliases)")

'''
anchor = "\n# --- r123 ship asserts"
assert anchor in out, "r123 anchor not found"
out = out.replace(anchor, r124_block + anchor, 1)

# 3) relabel
out = out.replace('print("check_r123: FAILURES:")', 'print("check_r124: FAILURES:")')
out = out.replace('print(f"check_r123: ALL GREEN ({len(PAGES)} pages)")',
                  'print(f"check_r124: ALL GREEN ({len(PAGES)} pages)")')

(ROOT / "tools" / "check_r124.py").write_text(out, encoding="utf-8")
print("check_r124.py written:", len(out), "bytes")
