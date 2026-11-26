#!/usr/bin/env python3
"""Fill the zoomable diagram page (templates/draw/viewer.html) with diagram data.

Usage: python3 draw_view.py <data.json> <out.html> [--open]

data.json: {"title", "subtitle", "diagrams": [{"title", "mermaid", "legend": [...], "pair": "<id>"}],
            "explanation": [{"heading", "items": [...]}]}
Diagrams sharing a "pair" id render side by side (before/after). Standard library only.
"""
import json
import os
import re
import subprocess
import sys

TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "draw", "viewer.html")


def main():
    args = [a for a in sys.argv[1:] if a != "--open"]
    if len(args) != 2:
        sys.exit(__doc__)
    with open(args[0], encoding="utf-8") as handle:
        data = json.load(handle)
    if not data.get("diagrams"):
        sys.exit("no diagrams in the data")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    with open(TEMPLATE, encoding="utf-8") as handle:
        page = handle.read()
    page, count = re.subn(r'(<script type="application/json" id="data">\n).*?(\n</script>)',
                          lambda m: m.group(1) + payload + m.group(2), page, count=1, flags=re.S)
    if count != 1:
        sys.exit("data block not found in the template")
    page = page.replace("<title>Diagram</title>", f"<title>{data.get('title', 'Diagram')[:60]}</title>", 1)
    os.makedirs(os.path.dirname(os.path.abspath(args[1])), exist_ok=True)
    with open(args[1], "w", encoding="utf-8") as handle:
        handle.write(page)
    print(os.path.abspath(args[1]))
    if "--open" in sys.argv:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.Popen([opener, args[1]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
