#!/usr/bin/env python3
"""Guardrail: <one-line rule>. PreToolUse hook for Edit|Write|MultiEdit; checks only added lines."""
import json
import os
import re
import sys

RULE = "<rule, in the user's language, saying what to do instead>"
FILES = re.compile(r"\.(ts|tsx|js|jsx)$")
PATTERN = re.compile(r"<pattern>")


def find(text):
    return [line.strip() for line in (text or "").splitlines() if PATTERN.search(line)]


def changes(tool, tool_input, path):
    if tool == "Write":
        try:
            with open(path, encoding="utf-8") as handle:
                current = handle.read()
        except OSError:
            current = ""
        return [(current, tool_input.get("content"))]
    if tool == "MultiEdit":
        return [(e.get("old_string"), e.get("new_string")) for e in tool_input.get("edits") or []]
    return [(tool_input.get("old_string"), tool_input.get("new_string"))]


def main():
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or ""
    if not FILES.search(path):
        return
    violations = []
    for old, new in changes(payload.get("tool_name"), tool_input, path):
        existing = set(find(old))
        violations += [item for item in find(new) if item not in existing]
    if not violations:
        return
    reason = f"{RULE} ({os.path.basename(path)}):\n" + "\n".join(violations[:8])
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))


if __name__ == "__main__":
    main()
