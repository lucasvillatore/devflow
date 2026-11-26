#!/usr/bin/env python3
"""Print the devflow catalog: what devflow is, every Area with its skills and agents, which Areas are on, and what is planned.

Usage: python3 catalog.py
Standard library only.
"""
import json
import os
import re

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(os.path.expanduser("~"), ".config", "devflow", "config.json")


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def frontmatter(path):
    text = read(path)
    if not text.startswith("---\n"):
        return {}
    block = text[4:text.find("\n---", 4)]
    return dict(re.findall(r"^([\w-]+):\s*(.*)$", block, re.M))


def main():
    areas = json.loads(read(os.path.join(PLUGIN, "components.json")))["areas"]
    plugin = json.loads(read(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")))
    config = json.loads(read(CONFIG)) if os.path.exists(CONFIG) else None
    active = set(config.get("areas", [])) if config else None

    print(read(os.path.join(PLUGIN, "references", "flow.md")).strip())
    print("\n# Catalog\n")
    print("Setup: " + (f"done (Vault: {config['vault']}, language: {config['language']})" if config else "not done yet, run /devflow:setup"))
    for name, area in areas.items():
        state = "required" if area.get("required") else ("on" if active is None or name in active else "off")
        print(f"\n## {name} ({state})")
        skills = area.get("skills", [])
        if not skills:
            print("- nothing yet")
        for skill in skills:
            meta = frontmatter(os.path.join(PLUGIN, "skills", skill, "SKILL.md"))
            who = "user only" if meta.get("disable-model-invocation") == "true" else "user or Claude"
            print(f"- /devflow:{skill} ({who}): {meta.get('description', '')}")
    agents_dir = os.path.join(PLUGIN, "agents")
    if os.path.isdir(agents_dir):
        print("\n## agents (started by the skills, not by the user)")
        for name in sorted(os.listdir(agents_dir)):
            meta = frontmatter(os.path.join(agents_dir, name))
            print(f"- devflow:{meta.get('name', name[:-3])}: {meta.get('description', '')}")
    backlog = os.path.join(PLUGIN, "docs", "backlog.md")
    if os.path.exists(backlog):
        print("\n## planned (backlog, not available yet)")
        for title in re.findall(r"^## (.+)$", read(backlog), re.M):
            print(f"- {title}")
    print(f"\nRepository (for issues and suggestions): {plugin.get('repository', 'unknown')}")


if __name__ == "__main__":
    main()
