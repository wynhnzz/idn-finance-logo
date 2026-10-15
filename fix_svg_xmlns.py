#!/usr/bin/env python3
"""Add the missing xmlns (and xmlns:xlink when needed) to every SVG in icon/."""
import re
import sys
from pathlib import Path
from xml.dom import minidom

folder = Path(sys.argv[1] if len(sys.argv) > 1 else "icon")
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

fixed = skipped = 0
bad = []

for f in sorted(folder.glob("*.svg")):
    text = f.read_text(encoding="utf-8")
    m = re.search(r"<svg\b[^>]*>", text)
    if not m:
        bad.append(f.name)
        continue
    tag = m.group(0)
    add = ""
    if "xmlns=" not in tag:
        add += f' xmlns="{SVG_NS}"'
    if "xlink:" in text and "xmlns:xlink=" not in tag:
        add += f' xmlns:xlink="{XLINK_NS}"'
    if not add:
        skipped += 1
        continue
    new_tag = tag.replace("<svg", "<svg" + add, 1)
    new_text = text[:m.start()] + new_tag + text[m.end():]
    try:
        minidom.parseString(new_text.encode("utf-8"))
    except Exception as e:
        bad.append(f"{f.name} ({e})")
        continue
    f.write_text(new_text, encoding="utf-8")
    fixed += 1

print(f"fixed={fixed} already_ok={skipped} problems={len(bad)}")
for b in bad:
    print("  !", b)
