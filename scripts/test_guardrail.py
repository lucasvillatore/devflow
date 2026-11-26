#!/usr/bin/env python3
"""Test of guardrail.py against a fake HOME: the hook template, filled in, blocks only added matches; register is idempotent, keeps foreign settings and backs them up.

Usage: python3 test_guardrail.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(os.path.dirname(HERE), "templates", "guardrail", "hook.py")


def run(home, *args):
    return subprocess.run([sys.executable, os.path.join(HERE, "guardrail.py"), *args],
                          env={**os.environ, "HOME": home}, capture_output=True, text=True)


def edit(old, new):
    return {"tool_name": "Edit", "tool_input": {"file_path": "/x/a.ts", "old_string": old, "new_string": new}}


with tempfile.TemporaryDirectory() as home:
    hooks = os.path.join(home, ".claude", "hooks")
    os.makedirs(hooks)
    hook = os.path.join(hooks, "no-console.py")
    source = open(TEMPLATE).read().replace('r"<pattern>"', r'r"console\.log\("').replace("<rule, in the user's language, saying what to do instead>", "No console.log")
    open(hook, "w").write(source)
    cases = os.path.join(hooks, "no-console.cases.json")
    json.dump([
        {"name": "new console.log", "expect": "block", "payload": edit("a()", "a()\nconsole.log(1)")},
        {"name": "existing console.log", "expect": "allow", "payload": edit("console.log(1)", "console.log(1)\nb()")},
        {"name": "other file type", "expect": "allow", "payload": {"tool_name": "Write", "tool_input": {"file_path": "/x/a.md", "content": "console.log("}}},
    ], open(cases, "w"))
    r = run(home, "test", hook, cases)
    assert r.returncode == 0, r.stdout + r.stderr

    json.dump([{"name": "wrong", "expect": "allow", "payload": edit("", "console.log(2)")}], open(cases, "w"))
    assert run(home, "test", hook, cases).returncode == 1

    settings = os.path.join(home, ".claude", "settings.json")
    json.dump({"theme": "auto"}, open(settings, "w"))
    r = run(home, "register", hook, "--dry-run")
    assert r.returncode == 0 and "PreToolUse" in r.stdout and json.load(open(settings)) == {"theme": "auto"}
    r = run(home, "register", hook)
    assert r.returncode == 0, r.stderr
    data = json.load(open(settings))
    assert data["theme"] == "auto"
    assert data["hooks"]["PreToolUse"][0]["hooks"][0]["command"] == 'python3 "$HOME/.claude/hooks/no-console.py"'
    assert os.listdir(os.path.join(home, ".claude", "backups"))
    assert "already registered" in run(home, "register", hook).stdout
    assert len(json.load(open(settings))["hooks"]["PreToolUse"][0]["hooks"]) == 1

print("ok: template blocks added matches only, test detects failures, register is idempotent and keeps settings")
