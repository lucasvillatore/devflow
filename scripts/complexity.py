#!/usr/bin/env python3
"""Measure complexity per function with lizard, and compare two measurements.

Usage:
  python3 complexity.py measure <path>... [--function <name>] [--out <file.json>]
  python3 complexity.py compare <before.json> <after.json>

measure: one entry per function: file (relative to the repository root), function, start, end, ccn (cyclomatic complexity), nloc, params.
Measure whole files for a refactoring: functions extracted by it must be counted in "after".
compare: a Markdown table of the functions that changed, appeared or disappeared, plus the totals.
lizard comes from devflow's tools (python3 tools.py install lizard). Standard library only.
"""
import csv
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS = {}


def relative(path):
    """Path relative to the repository root (git), so measurements taken from different folders compare."""
    path = os.path.abspath(path)
    folder = os.path.dirname(path)
    if folder not in ROOTS:
        result = subprocess.run(["git", "-C", folder, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        ROOTS[folder] = result.stdout.strip() if result.returncode == 0 else os.getcwd()
    return os.path.relpath(path, ROOTS[folder])


def lizard():
    result = subprocess.run([sys.executable, os.path.join(HERE, "tools.py"), "path", "lizard"], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(result.stderr.strip() or "lizard is not installed")
    return result.stdout.strip()


def measure(paths, function=None):
    result = subprocess.run([lizard(), "--csv", *paths], capture_output=True, text=True)
    if result.returncode not in (0, 1):
        sys.exit(result.stderr.strip())
    rows = []
    for row in csv.reader(io.StringIO(result.stdout)):
        if len(row) < 11:
            continue
        nloc, ccn, _tokens, params, _length, _location, path, name, _long, start, end = row[:11]
        if function and name != function and not name.endswith("::" + function):
            continue
        rows.append({"file": relative(path), "function": name, "start": int(start), "end": int(end),
                     "ccn": int(ccn), "nloc": int(nloc), "params": int(params)})
    return sorted(rows, key=lambda r: (-r["ccn"], r["file"], r["start"]))


def compare(before, after):
    key = lambda r: (r["file"], r["function"])
    old, new = {key(r): r for r in before}, {key(r): r for r in after}
    lines = ["| Function | CCN before | CCN after | NLOC before | NLOC after |", "| :-- | --: | --: | --: | --: |"]
    for k in sorted(set(old) | set(new)):
        a, b = old.get(k), new.get(k)
        if a and b and (a["ccn"], a["nloc"]) == (b["ccn"], b["nloc"]):
            continue
        cell = lambda r, f: str(r[f]) if r else "—"
        lines.append(f"| `{k[1]}` ({k[0]}) | {cell(a, 'ccn')} | {cell(b, 'ccn')} | {cell(a, 'nloc')} | {cell(b, 'nloc')} |")
    total = lambda rows, f: sum(r[f] for r in rows)
    worst = lambda rows: max((r["ccn"] for r in rows), default=0)
    lines += ["", f"Totals: CCN {total(before, 'ccn')} → {total(after, 'ccn')}, NLOC {total(before, 'nloc')} → {total(after, 'nloc')}, "
              f"functions {len(before)} → {len(after)}, highest CCN {worst(before)} → {worst(after)}"]
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ("measure", "compare"):
        sys.exit(__doc__)
    if args[0] == "compare":
        if len(args) != 3:
            sys.exit(__doc__)
        print(compare(*(json.load(open(p, encoding="utf-8")) for p in args[1:])))
        return
    out = function = None
    paths = []
    rest = args[1:]
    while rest:
        item = rest.pop(0)
        if item == "--out":
            out = rest.pop(0)
        elif item == "--function":
            function = rest.pop(0)
        else:
            paths.append(item)
    if not paths:
        sys.exit(__doc__)
    rows = measure(paths, function)
    text = json.dumps(rows, indent=2)
    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
