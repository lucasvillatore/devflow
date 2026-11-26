---
name: refactor
description: (Experimental) Refactor a function or a class with proof that its contract did not change - measure complexity, pin the current behavior with characterization tests and recorded outputs, refactor in small steps, then show the same tests green, identical outputs before and after, and the complexity numbers. Works for TypeScript, JavaScript, PHP, Go and Java. Use when the user wants to simplify or refactor a function or class safely; for a whole project or module set, use refactor-plan.
argument-hint: "<function or class> [workspace]"
---

# Refactor with proof

**Experimental**: the user is still testing it. End by asking what was useful.

A refactoring changes the structure, never the contract. This skill works on **one function or one class**; a project goes through `/devflow:refactor-plan`, which turns it into Tasks that come back here one by one. Every claim of "same behavior" needs evidence produced by running things. The scripts are at the root of this plugin (two levels above this skill's directory): `scripts/tools.py`, `scripts/complexity.py`, `scripts/equivalence.py`; and the references `references/refactor-contracts.md` (what the contract is at each level) and `references/refactor-moves.md` (problem → move).

Workspace: `references/workspace.md` (an Issue key or a name). The evidence lives in `<vault>/issues/<id>/refactor/<slug>/` (folder name in the configured language, e.g. `refatoracao/`). Follow the repository's conventions and the user's guardrails in every line written.

## Steps

1. **Tools.** Run `python3 <plugin>/scripts/tools.py check lizard`. When missing, show the install command it prints and run it only after the user agrees. Mutation tools (`stryker`, `infection`, `gremlins`, `pit`) are optional: check them only if the user wants mutation testing; project tools are never installed by you, only suggested.

2. **Target, level and contract.** The target comes from the argument, a Task from `refactor-plan`, or an analysis finding (`type: Analysis` in the workspace). Say whether it is a function or a class and state its contract, following `references/refactor-contracts.md`. A target bigger than a class: stop and suggest `/devflow:refactor-plan`. Measure the **whole file** of the target (not only the function, so the functions extracted later are counted): `python3 <plugin>/scripts/complexity.py measure <file> --out <evidence>/before.json`. Show the target's numbers (CCN = number of independent paths; each path needs a test).

3. **Pin the current behavior.** Before touching the code:
   - find the existing tests of the target and run them;
   - for a class, test only through its public interface;
   - write **characterization tests**: they assert what the code does today, even when it looks wrong (a suspicious behavior is pinned and reported, not fixed here). One case per path (at least as many as the CCN), plus edge cases (empty, null, limits, errors) and real payloads when the user has them;
   - run them on the current code: all green;
   - measure branch coverage of the target with the repository's coverage command (from the repository profile `<vault>/devflow/projects/<repo>.md`; ask and record it when missing). Every branch of the target covered, or each uncovered one named with why;
   - record outputs: a small harness (in `<vault>/issues/<id>/scripts/`) runs the target over every characterization input plus generated ones, and writes `<evidence>/before.jsonl` (`{"id", "input", "output"}` per line; an error is an output). Creating the tests and the harness needs the user's ok, asked once with the plan of step 4.

4. **Propose.** Name the problems and the moves from `references/refactor-moves.md` that address them. Show the refactoring as a before/after in inline Mermaid, in the same shape as draw's before/after (the user can also run `/devflow:draw` on it) with the explanation (what changes, why with its basis, gain, cost and risk, alternatives). Stop and wait for the user's ok.

5. **Refactor in small steps.** One move at a time (extract a function, replace a condition, split a module). After each move, run the characterization tests; when one goes red, undo that move and try a smaller one. Never change a test to make it pass.

6. **Prove.**
   - the characterization and existing tests: green;
   - run the harness again into `<evidence>/after.jsonl`, then `python3 <plugin>/scripts/equivalence.py <evidence>/before.jsonl <evidence>/after.jsonl`: it must say `EQUIVALENT`;
   - `complexity.py measure <the same file> <any new file the refactoring created> --out <evidence>/after.json`, then `complexity.py compare <evidence>/before.json <evidence>/after.json`. Report the target **and** the functions extracted from it: complexity that only moved to a new function did not go away. The gain is the highest CCN among them and how the paths are split, not the target's CCN alone;
   - branch coverage again;
   - optional: mutation testing on the target, when the user wants it.
   When anything is not equivalent, show the difference and go back to step 5. Never claim equivalence without the `EQUIVALENT` line.

7. **Record** `<vault>/issues/<id>/refactor-<slug>.md` (name in the configured language, e.g. `refatoracao-<slug>.md`; frontmatter `type: Refactor`, `title`, `target`, `timestamp`): target, the complexity table, the tests added (by behavior), coverage before and after, the equivalence result (number of cases, command, output), suspicious behaviors pinned but not fixed, and the commands to reproduce. It is ready for the Evidence section of `/devflow:open-pr`.

8. **Close the Task** when the target came from one (a `refactor-plan` or `plan-issue` Task): follow "Closing a Task" in `references/tasks.md` (status `done`, its box ticked in the Planning). Offer the commit; never run it unasked.

The characterization tests stay in the repository as regression tests.

## Answer

The complexity before → after, the tests added, coverage, the equivalence line, suspicious behaviors found, and the path of the record. Then ask what was useful.
