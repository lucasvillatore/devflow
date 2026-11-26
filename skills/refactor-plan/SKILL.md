---
name: refactor-plan
description: (Experimental) Plan the refactoring of a project or a set of modules without changing code - measure complexity across it, cross it with the hot spots in git history, pin the external contract with recorded border tests, and write prioritized Tasks, each a function or class refactoring for /devflow:refactor. Use when the user wants to refactor or clean up a whole project, service or module set.
argument-hint: "<project or path> [workspace] [why you want it refactored]"
---

# Plan a refactoring

Read `~/.config/devflow/config.json` (`vault`, `language`) and write in the configured language.

**Experimental**: the user is still testing it. End by asking what was useful.

No production code changes here: this skill measures, prioritizes, pins the external contract and writes Tasks. Each Task is later done by `/devflow:refactor` with its own proof.

The scripts and references are at the root of this plugin (two levels above this skill's directory): `scripts/tools.py`, `scripts/complexity.py`, `scripts/equivalence.py`, `references/refactor-contracts.md`, `references/refactor-moves.md`, `references/workspace.md`, `references/tasks.md`. Evidence goes to `<vault>/issues/<id>/refactor-plan/` (folder name in the configured language, e.g. `plano-refatoracao/`).

## Steps

1. **Tools and scope.** `python3 <plugin>/scripts/tools.py check lizard` (install with the user's ok). Agree on the scope: the repository, a service, or some folders; and what is out (generated code, migrations, vendored code).

2. **Measure.** `python3 <plugin>/scripts/complexity.py measure <paths> --out <evidence>/baseline.json`. Show the distribution: how many functions above CCN 10, 20, 40; the top 15.

3. **Hot spots.** Count changes per file in the git history (`git log --since=<period> --name-only --format=` over the scope, default one year). Cross with complexity: **complex and often changed** comes first; complex but never touched comes last (refactoring it pays off little). Add the analysis findings in the workspace when there are any.

4. **External contract.** Following the Project section of `references/refactor-contracts.md`, list what the outside world sees (endpoints, messages, schema, jobs, commands). Propose border contract tests: real requests and responses (or messages and effects) recorded and replayed with `scripts/equivalence.py`. Ask before writing them; they are the safety net of every Task.

5. **Candidates.** Apply "Is it worth it?" from `references/refactor-moves.md` to the project and to each candidate: the user's reason, when given, is a premise to verify first (e.g. "adding a new type touches many modules": count them); candidates below the limit (repository profile, default CCN 10) with no problem from the table and no confirmed reason stay out. When nothing is left, the answer is **"the project is healthy, nothing to prioritize"**, with the complexity distribution as evidence, and no Tasks are written. For each remaining candidate: the target (function or class), the problems and the moves from `references/refactor-moves.md`, the contract it must keep, the expected gain (CCN before → target), the risk, and the effort. Changes that cross the contract go as expand-contract (expand, migrate in batches, contract), one Task per step. Show the list and iterate with the user on order and granularity.

6. **Write the Tasks** following `references/tasks.md`: the Planning first when there is none (its Context points to `<evidence>/plan.md`), numbering after it, the checklist and the `**Plan**` log entry (`**Replan**` when a Planning already exists). One Task per refactoring, What = target and moves, How = the contract and the proof expected, Acceptance criteria = tests green, `EQUIVALENT`, CCN target reached, border contract tests green. `depends_on` for the order (the border tests first; expand before migrate before contract). Record the plan in `<evidence>/plan.md` with the baseline numbers and the reasoning.

7. **Answer**: the baseline, the top hot spots, the border tests proposed, and the Tasks in order. Each Task is done with `/devflow:refactor <target> <workspace>`. Then ask what was useful.
