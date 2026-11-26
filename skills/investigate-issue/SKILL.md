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

1. **Start from what exists.** Read `index.md` (the symptom), the analyses (`type: Analysis`: reuse the map as the starting point) and an existing `type: Investigation` file, whatever its name (resume from it and keep writing to it; do not redo what is recorded or create a second one). Restate the symptom in one line: what happens, where, since when.

2. **Check the premise.** The report may be wrong: the behavior may be expected, the data may come wrong from another system, or the symptom may be somewhere else. Treat the reported symptom as a claim to verify, not a fact; do not look only for confirmation. The signal of the next step is also the premise test.

3. **Build a signal that goes red on the bug** (after Matt Pocock's `diagnosing-bugs`, MIT, see `THIRD_PARTY_NOTICES.md`). One command that drives the real code path and shows the user's exact symptom, deterministic and fast. In rough order: an existing or new test at the seam that reaches the bug; a request against a local server; a query showing the bad data (`dbq`); a log search showing the failure (`awsq`); a script replaying a captured payload. Show the command and its output.
   Two different outcomes when it does not go red:
   - **Premise not confirmed**: you could exercise the reported case (the same input, the same data, the real code path) and the behavior is the expected one. That is a valid result, not a failure: record the evidence and stop; say what would make the premise true (a different input, environment, moment).
   - **Could not build a signal**: you could not exercise the case (no access, no data, environment-specific). Say what you tried and what would unlock it (access, a sample payload, a log of the failing moment). Do not move on to theories without it.

4. **Reproduce and narrow down.** Run the signal; confirm it shows the reported symptom and not a nearby one. Cut inputs, data and steps one at a time while it stays red, to the smallest case.

5. **Collect facts** around the failing path: what the data looks like before and after, which calls run and in what order, what the logs say at the failure point, which branches the input takes. Record what was checked and found nothing too: it discards hypotheses. Do not explain the cause; describe what happens.

6. **Record** the investigation file: the existing `type: Investigation` one, or a new `<vault>/issues/<id>/investigation.md` (name in the configured language, e.g. `investigacao.md`), updating it as facts come in, so a dropped session loses nothing:

   ```markdown
   ---
   type: Investigation
   title: <symptom in a few words>
   signal: <the command that goes red>
   timestamp: YYYY-MM-DD
   ---

   # Symptom
   # Premise
   <confirmed | not confirmed | could not test>, with the evidence
   # Signal
   <command, output (redacted), red or green>
   # Reproduction
   <smallest case>
   # Facts
   - <fact> (evidence: <command/output, query, log line, file:line>)
   # Checked, nothing found
   # Open questions
   <what only people can answer, and who>
   # Corrections
   - YYYY-MM-DD: <fact> was wrong: <what is true, and why the first reading failed> (by <user or Claude>)
   ```

   Temporary scripts go to `<vault>/issues/<id>/scripts/`. A new reproduction test stays in the repository uncommitted; ask whether to keep it (it becomes the regression test of the fix) or remove it.

   **Corrections**: when a fact turns out wrong (the user says so, or a later check contradicts it), never delete it: strike it (`~~fact~~`), and add a line under Corrections with what is true and why the first reading failed. `/devflow:retro` reads this section to turn the lesson into a pointer, a convention or a skill fix.

7. **Next step.** Suggest `/devflow:diagnose <id>` to judge the facts, and list the open questions. Then ask what was useful.
