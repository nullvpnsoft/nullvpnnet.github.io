#!/usr/bin/env python3
"""r82: remove the STALE body FAQPage JSON-LD from faq.html (11 questions
incl. a phantom 'What is Ad Guard?' no longer on the visible page, plus an
outdated TON answer text — violating the markup-must-match-visible guideline).
The r82 head block (10 questions extracted from the live visible text this
round) becomes the single FAQPage. Idempotent with pre/post asserts."""
import os, sys

F = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "faq.html")
src = open(F, encoding="utf-8").read()

if src.count('"@type": "FAQPage"') == 0 and src.count('"@type":"FAQPage"') == 1:
    print("already replaced, nothing to do")
    sys.exit(0)

assert src.count('"@type": "FAQPage"') == 1, "expected exactly one stale block"
lines = src.split("\n")
# locate opening tag of the stale block (line index of '<script type="application/ld+json">' BEFORE the '"@type": "FAQPage"' line)
stale_idx = next(i for i, l in enumerate(lines) if '"@type": "FAQPage"' in l)
open_idx = max(i for i in range(stale_idx) if '<script type="application/ld+json">' in lines[i])
close_idx = next(i for i in range(stale_idx, len(lines)) if lines[i].strip() == "</script>")
# pre-asserts: block shape (verbose format: '{' then '"@context"')
assert lines[open_idx + 1].strip() == "{", "unexpected block start"
assert "schema.org" in lines[open_idx + 2], "unexpected block context line"
assert lines[close_idx + 1].strip() == "</body>", "stale block not at body end"

replacement = [
    "  <!-- r82: the pre-existing body FAQPage (11 questions) was REMOVED — it had",
    "       drifted from the visible page (phantom 'What is Ad Guard?' question the",
    "       page no longer shows; outdated TON answer text). The single FAQPage now",
    "       lives in <head>, extracted from the visible en text this round. -->",
]
lines[open_idx:close_idx + 1] = replacement
out = "\n".join(lines)
assert out.count('"@type": "FAQPage"') == 0, "stale block not fully removed"
assert out.count('"@type":"FAQPage"') == 1, "head block must be the only FAQPage"
open(F, "w", encoding="utf-8").write(out)
print("OK: stale body FAQPage removed (was lines %d-%d), head block is now the single FAQPage" % (open_idx + 1, close_idx + 1))
