#!/usr/bin/env python3
"""Mechanical checks of a knowledge base, driven by <base>/.kb/base.yaml.

Usage: python3 kb_verify.py --base <path> [--config <.kb folder>] [--path <relative to the base>]
Output: ERROR and WARN lines per file. Exit code 1 when there is an error.
"""
import argparse
import os
import re
import sys
import urllib.parse

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is not installed: pip install pyyaml")

FENCE = re.compile(r"^(```|~~~)")
LINK = re.compile(r"\]\(([^)\s]+)\)")


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4:].lstrip("\n")


def outside_code(body):
    inside = False
    for n, line in enumerate(body.splitlines(), 1):
        if FENCE.match(line.strip()):
            inside = not inside
            continue
        if not inside:
            yield n, line


def headings(body, level=1):
    mark = "#" * level + " "
    return [line[len(mark):].strip() for _, line in outside_code(body) if line.startswith(mark)]


def check_file(path, rel, cfg, problems):
    def error(msg):
        problems.append(("ERROR", rel, msg))

    def warn(msg):
        problems.append(("WARN", rel, msg))

    text = open(path, encoding="utf-8").read()
    fm_text, body = split_frontmatter(text)
    name = os.path.basename(path)
    reserved = cfg.get("reserved", ["index.md", "log.md"])
    statuses = cfg.get("status", {})
    fm = {}

    if name in reserved:
        if fm_text is not None:
            try:
                fm = yaml.safe_load(fm_text) or {}
            except yaml.YAMLError as e:
                fm = None
                error(f"invalid YAML frontmatter (unquoted text with ': '?): {str(e).splitlines()[0]}")
            if fm is not None and not (rel == "index.md" and isinstance(fm, dict) and set(fm) <= {"okf_version"}):
                error(f"{name} cannot have frontmatter (only the root index.md, with okf_version)")
            if not isinstance(fm, dict):
                fm = {}
    else:
        parsed = False
        if fm_text is None:
            error("missing frontmatter")
        else:
            try:
                fm = yaml.safe_load(fm_text) or {}
                parsed = True
            except yaml.YAMLError as e:
                error(f"invalid YAML frontmatter (unquoted text with ': '?): {str(e).splitlines()[0]}")
        if parsed and not isinstance(fm, dict):
            error("frontmatter is not a list of fields (expected `field: value` lines)")
            fm = {}
            parsed = False
        if parsed:
            for field in cfg.get("required_fields", ["type"]):
                if not fm.get(field):
                    error(f"missing required field: {field}")
            types = cfg.get("types", {})
            valid = [t for t, d in types.items() if not (d or {}).get("template_only")]
            doc_type = fm.get("type")
            if doc_type is not None and not isinstance(doc_type, str):
                error(f"type must be a single text value, not {type(doc_type).__name__}")
                doc_type = None
            if doc_type and doc_type not in valid:
                error(f"type '{doc_type}' is not in the configuration ({', '.join(valid)})")
            status = fm.get("status")
            if status and status not in statuses.values():
                error(f"status '{status}' is not in the configuration")

            template = doc_type
            parts = cfg.get("folders", {}).get("process_parts", []) or []
            parts_template = next((t for t, d in types.items() if (d or {}).get("template_only")), None)
            if parts_template and any(p in rel.split(os.sep)[:-1] for p in parts):
                template = parts_template
            rule = types.get(template) or {}
            required = rule.get("sections", [])
            if status and status == statuses.get("draft") and "draft_sections" in rule:
                required = rule["draft_sections"]
            present = headings(body) + headings(body, 2)
            for s in required:
                if s not in present:
                    error(f"missing required section of template '{template}': # {s}")

    forbidden = cfg.get("forbidden", {})
    for s in headings(body):
        if s in forbidden.get("sections", []):
            error(f"forbidden section: # {s}")

    quiet = fm.get("type") in cfg.get("no_writing_warnings", [])
    phrases = [] if quiet else [re.compile(f, re.I) for f in forbidden.get("phrases", [])]
    terms = [] if quiet else [re.compile(rf"(?<![\w-]){re.escape(t)}(?![\w-])", re.I)
                              for t in forbidden.get("system_terms", [])]
    for n, line in outside_code(body):
        for f in phrases:
            if f.search(line):
                warn(f"body line {n}: forbidden phrase ({f.pattern}): {line.strip()[:80]}")
        for t in terms:
            m = t.search(line)
            if m:
                warn(f"body line {n}: system term '{m.group(0)}'")
        for target in LINK.findall(line):
            if re.match(r"^[a-z]+:", target):
                continue
            file_part, _, anchor = target.partition("#")
            if anchor and file_part.endswith(".md") and forbidden.get("anchor_links", True):
                warn(f"body line {n}: anchor link '#{anchor}', link to the file")
            if file_part.endswith(".md"):
                dest = os.path.normpath(os.path.join(os.path.dirname(path), urllib.parse.unquote(file_part)))
                if not os.path.exists(dest):
                    error(f"body line {n}: broken link: {file_part}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", required=True)
    ap.add_argument("--config", help="configuration folder (default: <base>/.kb)")
    ap.add_argument("--path", default="", help="file or folder relative to the base")
    a = ap.parse_args()

    base = os.path.abspath(os.path.expanduser(a.base))
    config_dir = os.path.abspath(os.path.expanduser(a.config or os.path.join(base, ".kb")))
    cfg_path = os.path.join(config_dir, "base.yaml")
    if not os.path.exists(cfg_path):
        sys.exit(f"configuration not found: {cfg_path}")
    cfg = yaml.safe_load(open(cfg_path, encoding="utf-8")) or {}
    skipped = set(cfg.get("skip_folders", []))

    target = os.path.join(base, a.path)
    if os.path.isfile(target):
        files = [target]
    else:
        files = []
        for root, dirs, names in os.walk(target):
            dirs[:] = [d for d in dirs if not d.startswith(".")
                       and os.path.relpath(os.path.join(root, d), base) not in skipped]
            files += [os.path.join(root, n) for n in names if n.endswith(".md")]

    problems = []
    for f in sorted(files):
        check_file(f, os.path.relpath(f, base), cfg, problems)

    for level in ("ERROR", "WARN"):
        for lv, rel, msg in problems:
            if lv == level:
                print(f"{lv:5} {rel}: {msg}")
    errors = sum(1 for p in problems if p[0] == "ERROR")
    print(f"\n{len(files)} files, {errors} errors, {len(problems) - errors} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
