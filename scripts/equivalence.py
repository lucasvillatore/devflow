#!/usr/bin/env python3
"""Compare the outputs of the code before and after a refactoring, for the same inputs.

Usage: python3 equivalence.py <before.jsonl> <after.jsonl>

Each line of both files: {"id": "<case id>", "input": <anything>, "output": <anything>}
(an error is recorded as the output, e.g. {"error": "TypeError", "message": "..."}).
Exit 0 when every case has the same output in both files, 1 otherwise, with the differences.
Standard library only.
"""
import json
import sys


def load(path):
    cases = {}
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if line.strip():
                case = json.loads(line)
                if "id" not in case or "output" not in case:
                    sys.exit(f"{path}:{number}: each line needs 'id' and 'output'")
                if str(case["id"]) in cases:
                    sys.exit(f"{path}:{number}: duplicate id {case['id']!r}: every case needs its own id")
                cases[str(case["id"])] = case
    return cases


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    before, after = load(sys.argv[1]), load(sys.argv[2])
    canonical = lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False)
    missing = sorted(set(before) - set(after))
    extra = sorted(set(after) - set(before))
    different = [k for k in sorted(set(before) & set(after)) if canonical(before[k]["output"]) != canonical(after[k]["output"])]
    print(f"cases: {len(before)} before, {len(after)} after; identical: {len(set(before) & set(after)) - len(different)}")
    for k in missing:
        print(f"MISSING after: {k}")
    for k in extra:
        print(f"ONLY after: {k}")
    for k in different[:20]:
        print(f"DIFFERENT {k}\n  input:  {canonical(before[k].get('input'))[:300]}\n  before: {canonical(before[k]['output'])[:300]}\n  after:  {canonical(after[k]['output'])[:300]}")
    if len(different) > 20:
        print(f"... and {len(different) - 20} more")
    ok = not (missing or extra or different)
    print("EQUIVALENT" if ok else "NOT EQUIVALENT")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
