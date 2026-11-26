#!/usr/bin/env python3
"""Test of complexity.py (when lizard is installed) and equivalence.py.

Usage: python3 test_refactor_tools.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run(*args, cwd=None):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=cwd)


with tempfile.TemporaryDirectory() as tmp:
    write = lambda name, lines: open(os.path.join(tmp, name), "w").write("\n".join(json.dumps(l) for l in lines) + "\n")
    write("b.jsonl", [{"id": 1, "input": 5, "output": {"a": 1, "b": 2}}, {"id": 2, "input": 0, "output": {"error": "X"}}])
    write("same.jsonl", [{"id": 2, "input": 0, "output": {"error": "X"}}, {"id": 1, "input": 5, "output": {"b": 2, "a": 1}}])
    write("diff.jsonl", [{"id": 1, "input": 5, "output": {"a": 1, "b": 3}}])
    eq = os.path.join(HERE, "equivalence.py")
    r = run(eq, os.path.join(tmp, "b.jsonl"), os.path.join(tmp, "same.jsonl"))
    assert r.returncode == 0 and "EQUIVALENT" in r.stdout, r.stdout
    r = run(eq, os.path.join(tmp, "b.jsonl"), os.path.join(tmp, "diff.jsonl"))
    assert r.returncode == 1 and "DIFFERENT 1" in r.stdout and "MISSING after: 2" in r.stdout, r.stdout

    has_lizard = run(os.path.join(HERE, "tools.py"), "path", "lizard").returncode == 0
    if has_lizard:
        open(os.path.join(tmp, "a.ts"), "w").write("export class C {\n  f(a: number): number { if (a > 1 && a < 5) { return 1 } else if (a < 0) { return 2 } return 0 }\n  g(): number { return 1 }\n}\n")
        cx = os.path.join(HERE, "complexity.py")
        r = run(cx, "measure", "a.ts", "--out", "before.json", cwd=tmp)
        assert r.returncode == 0, r.stderr
        rows = json.load(open(os.path.join(tmp, "before.json")))
        assert [(x["function"], x["ccn"]) for x in rows] == [("f", 4), ("g", 1)], rows
        r = run(cx, "measure", "a.ts", "--function", "g", cwd=tmp)
        assert [x["function"] for x in json.loads(r.stdout)] == ["g"]
        open(os.path.join(tmp, "a.ts"), "w").write("export class C {\n  f(a: number): number { return a }\n  g(): number { return 1 }\n}\n")
        run(cx, "measure", "a.ts", "--out", "after.json", cwd=tmp)
        r = run(cx, "compare", "before.json", "after.json", cwd=tmp)
        assert "| `f` (a.ts) | 4 | 1 |" in r.stdout and "highest CCN 4 → 1" in r.stdout, r.stdout

print("ok: equivalence detects identical, different and missing cases" + ("; complexity measures, filters and compares" if has_lizard else "; complexity skipped (lizard not installed)"))
