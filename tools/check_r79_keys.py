#!/usr/bin/env python3
"""r79 sanity: every nav./footer. key referenced in 404.html's suggest MAP
must exist in i18n.js. Also asserts nf.suggest is present."""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "404.html").read_text(encoding="utf-8")
i18n = (ROOT / "i18n.js").read_text(encoding="utf-8")

keys = sorted(set(re.findall(r"'((?:nav|footer)\.[a-z.]+)'", src)))
missing = [k for k in keys if f'"{k}"' not in i18n]
print("404.html MAP keys:", keys)
print("key check:", "ALL PRESENT" if not missing else f"MISSING {missing}")
assert not missing
assert '"nf.suggest"' in i18n
print("nf.suggest present; OK")
