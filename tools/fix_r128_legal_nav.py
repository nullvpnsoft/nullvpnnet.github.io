#!/usr/bin/env python3
"""r128: Fix the legal-trio nav legacy structure.

Defect (found live, Task 127 re-lens): privacy/terms/refund navs lack the
.nav-top-row wrapper that every other content page has. .nav-inner is a
column flex, so the logo, .nav-actions, .nav-controls and .nav-links stack
as FOUR rows -> navbar renders 164px tall vs 108px on all other pages, and
the RTL row-reverse rule for the top row never applies on these pages.

Fix: wrap logo + .nav-actions + .nav-controls in <div class="nav-top-row">
(matching the canonical 12-page nav), and replace the legacy nav-links set
(Home / Pricing / FAQ / Contact / t.me Support / raw mailto) with the
standard 6-link set used by every other content page. The email/t.me links
remain in the footer social row and contact page; nav.home is dead on all
other pages (logo serves the home role).

No i18n keys added or removed (nav.features/how/compare already exist x7;
nav.home + footer.support stay used elsewhere / footer respectively).
"""
import re
import sys

FILES = ['privacy.html', 'terms.html', 'refund.html']

STANDARD_LINKS = (
    '      <ul class="nav-links">\n'
    '        <li><a href="features.html" data-i18n="nav.features">Features</a></li>\n'
    '        <li><a href="how-it-works.html" data-i18n="nav.how">How It Works</a></li>\n'
    '        <li><a href="comparison.html" data-i18n="nav.compare">Compare</a></li>\n'
    '        <li><a href="pricing.html" data-i18n="nav.pricing">Pricing</a></li>\n'
    '        <li><a href="faq.html" data-i18n="nav.faq">FAQ</a></li>\n'
    '        <li><a href="contact.html" data-i18n="nav.contact">Contact</a></li>\n'
    '      </ul>'
)

LEGACY_UL = re.compile(
    r'      <ul class="nav-links">.*?</ul>', re.S
)

# The legacy block: bare children between nav-inner open and nav-links ul.
NAV_INNER = '<div class="nav-inner">'


def indent_two(block: str) -> str:
    """Indent every non-empty line of block by exactly 2 spaces."""
    out = []
    for line in block.split('\n'):
        out.append(('  ' + line) if line.strip() else line)
    return '\n'.join(out)


def fix(path: str) -> bool:
    html = open(path, encoding='utf-8').read()
    if 'nav-top-row' in html:
        print(f'{path}: already has nav-top-row — SKIP')
        return False
    if 'nav.home' not in html:
        print(f'{path}: no legacy nav.home link — SKIP (unexpected shape)')
        return False
    # 1. Locate the nav-inner open and the nav-links ul LINE START.
    i_open = html.index(NAV_INNER)
    i_ul_raw = html.index('<ul class="nav-links">', i_open)
    i_ul = html.rindex('\n', i_open, i_ul_raw) + 1  # include the UL line's indent
    legacy_ul_m = LEGACY_UL.search(html, i_ul)
    assert legacy_ul_m, f'{path}: legacy UL not found'
    # Body between nav-inner open line end and the UL line start.
    seg_start = html.index('\n', i_open) + 1
    body = html[seg_start:i_ul]
    # body ends right after '</div>' + newline (UL indent lives on the UL side now)
    assert body.rstrip().endswith('</div>'), f'{path}: unexpected tail before UL'
    wrapped = (
        '      <div class="nav-top-row">\n'
        + indent_two(body.rstrip())
        + '\n      </div>\n'
    )
    html = html[:seg_start] + wrapped + html[i_ul:]
    # 2. Replace the legacy UL with the standard set (regex still matches:
    #    html[i_ul:] starts with the 6-space-indented '<ul class="nav-links">').
    html = LEGACY_UL.sub(lambda m: STANDARD_LINKS, html, count=1)
    open(path, 'w', encoding='utf-8').write(html)
    print(f'{path}: nav-top-row wrapped + nav-links standardized')
    return True


def main() -> int:
    changed = 0
    for f in FILES:
        if fix(f):
            changed += 1
    print(f'changed: {changed}/{len(FILES)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
