#!/usr/bin/env python3
"""devflow guardrails: test a PreToolUse hook against its cases and register it in ~/.claude/settings.json.

Usage:
  python3 guardrail.py test <hook.py> <hook.cases.json>
  python3 guardrail.py register <hook.py> [--matcher "Edit|Write|MultiEdit"] [--dry-run]

Cases file: [{"name": "...", "expect": "block" | "allow", "payload": {"tool_name": "Edit", "tool_input": {...}}}]
A case blocks when the hook exits with 2 or prints a PreToolUse "deny" or "ask" decision.
Standard library only.
"""
import argparse
import datetime
import difflib
import json
import os
import shutil
import subprocess
import sys

HOME = os.path.expanduser("~")
SETTINGS = os.path.join(HOME, ".claude", "settings.json")
BACKUPS = os.path.join(HOME, ".claude", "backups")


def blocked(result):
    if result.returncode == 2:
        return True
    try:
        output = json.loads(result.stdout or "{}")
    except ValueError:
        return False
    return (output.get("hookSpecificOutput") or {}).get("permissionDecision") in ("deny", "ask")


def test(args):
    with open(args.cases, encoding="utf-8") as handle:
        cases = json.load(handle)
    failures = 0
    for case in cases:
        result = subprocess.run([sys.executable, args.hook], input=json.dumps(case["payload"]),
                                capture_output=True, text=True, timeout=10,
                                cwd=os.path.dirname(os.path.abspath(args.hook)))
        got = "block" if blocked(result) else "allow"
        ok = got == case["expect"] and result.returncode in (0, 2)
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {case['name']}: expected {case['expect']}, got {got}"
              + ("" if ok else f"\n     exit {result.returncode}\n     {result.stderr.strip()[:500]}"))
    if not cases:
        print("FAIL no cases")
        failures = 1
    sys.exit(1 if failures else 0)


def command_for(hook):
    path = os.path.abspath(hook)
    if path.startswith(HOME + os.sep):
        path = "$HOME" + path[len(HOME):]
    return f'python3 "{path}"'


def register(args):
    current = {}
    if os.path.exists(SETTINGS):
        with open(SETTINGS, encoding="utf-8") as handle:
            current = json.load(handle)
    wanted = json.loads(json.dumps(current))
    command = command_for(args.hook)
    groups = wanted.setdefault("hooks", {}).setdefault("PreToolUse", [])
    if any(h.get("command") == command for g in groups for h in g.get("hooks", [])):
        print("already registered")
        return
    group = next((g for g in groups if g.get("matcher") == args.matcher), None)
    if group is None:
        group = {"matcher": args.matcher, "hooks": []}
        groups.append(group)
    group["hooks"].append({"type": "command", "command": command, "timeout": 10})
    old, new = json.dumps(current, indent=2) + "\n", json.dumps(wanted, indent=2) + "\n"
    print("".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), "settings.json (current)", "settings.json (new)")))
    if args.dry_run:
        print("(dry run: nothing written)")
        return
    if os.path.exists(SETTINGS):
        os.makedirs(BACKUPS, exist_ok=True)
        target = os.path.join(BACKUPS, f"settings.json.devflow-{datetime.datetime.now():%Y%m%d%H%M%S}")
        shutil.copy2(SETTINGS, target)
        print(f"settings backup: {target}")
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    with open(SETTINGS, "w", encoding="utf-8") as handle:
        handle.write(new)
    print("registered")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("test")
    run.add_argument("hook")
    run.add_argument("cases")
    reg = sub.add_parser("register")
    reg.add_argument("hook")
    reg.add_argument("--matcher", default="Edit|Write|MultiEdit")
    reg.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    test(args) if args.command == "test" else register(args)


if __name__ == "__main__":
    main()
