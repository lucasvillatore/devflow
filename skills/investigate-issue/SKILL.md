---
name: investigate-issue
description: (Experimental) Gather facts about a problem without concluding - build a signal that goes red on the bug (a failing test, a request, a query), reproduce it, and collect evidence from code, tests, logs and data (read-only), recorded in the Issue workspace for diagnose and plan-issue. Use when the cause of a bug is unknown, or the user needs to understand how the system behaves before planning.
argument-hint: "<ISSUE-KEY, workspace name or problem>"
---

# Investigate an Issue

**Experimental**: the user is still testing it. End by asking what was useful.

Gather **facts**, not conclusions. Every fact has its evidence: a command and its output, a query and its result, a log line, a `file:line`. The verdict is `/devflow:diagnose`'s job.

Read `~/.config/devflow/config.json` (`vault`, `language`) and write in the configured language. Find the workspace following `references/workspace.md` at the root of this plugin (two levels above this skill's directory); it may be an Issue key or a name. Create it when it does not exist.

## What runs without asking, and what does not

- **Alone**: reading code, logs, `awsq` and `dbq` read-only commands, running the repository's existing tests.
- **Only after the user's ok**: creating a new reproduction test or a temporary script, starting a local server, anything that takes long or costs money.
- **Never**: writes to databases, queues, buckets or any environment, even staging. If a fact can only be had by writing, say so and stop there.
- Never print credentials, URIs or tokens; quote only the lines that carry the signal.

## Steps

1. **Start from what exists.** Read `index.md` (the symptom), the analyses (`type: Analysis`: reuse the map as the starting point) and an existing `investigation.md` (resume from it; do not redo what is recorded). Restate the symptom in one line: what happens, where, since when.

2. **Build a signal that goes red on the bug** (after Matt Pocock's `diagnosing-bugs`, MIT, see `THIRD_PARTY_NOTICES.md`). One command that drives the real code path and shows the user's exact symptom, deterministic and fast. In rough order: an existing or new test at the seam that reaches the bug; a request against a local server; a query showing the bad data (`dbq`); a log search showing the failure (`awsq`); a script replaying a captured payload. Show the command and its output.
   When no signal can be built, stop and say what you tried and what would unlock it (access, a sample payload, a log of the failing moment). Do not move on to theories without it.

3. **Reproduce and narrow down.** Run the signal; confirm it shows the reported symptom and not a nearby one. Cut inputs, data and steps one at a time while it stays red, to the smallest case.

4. **Collect facts** around the failing path: what the data looks like before and after, which calls run and in what order, what the logs say at the failure point, which branches the input takes. Record what was checked and found nothing too: it discards hypotheses. Do not explain the cause; describe what happens.

5. **Record** `<vault>/issues/<id>/investigation.md` (name in the configured language, e.g. `investigacao.md`), updating it as facts come in, so a dropped session loses nothing:

   ```markdown
   ---
   type: Investigation
   title: <symptom in a few words>
   signal: <the command that goes red>
   timestamp: YYYY-MM-DD
   ---

   # Symptom
   # Signal
   <command, output (redacted), red or green>
   # Reproduction
   <smallest case>
   # Facts
   - <fact> (evidence: <command/output, query, log line, file:line>)
   # Checked, nothing found
   # Open questions
   <what only people can answer, and who>
   ```

   Temporary scripts go to `<vault>/issues/<id>/scripts/`. A new reproduction test stays in the repository uncommitted; ask whether to keep it (it becomes the regression test of the fix) or remove it.

6. **Next step.** Suggest `/devflow:diagnose <id>` to judge the facts, and list the open questions. Then ask what was useful.
