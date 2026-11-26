---
name: diagnose
description: (Experimental) Judge why a problem happens and what to do about it, by crossing the problem (the Issue) with the code analysis and the investigation facts in the Issue workspace - root cause confirmed or probable, contributing factors, unrelated improvements, and a recommendation, each with its evidence and confidence. Use when the user wants the root cause or a verdict on a problem after analysing or investigating it.
argument-hint: "<ISSUE-KEY, workspace name or problem>"
---

# Diagnose

**Experimental**: the user is still testing it. End by asking what was useful.

Judge, do not gather: this skill reads what other skills produced and draws the conclusion. It does not read new code or run anything beyond checking a citation. When a conclusion needs a fact nobody gathered, say which one and which skill gets it.

Read `~/.config/devflow/config.json` (`vault`, `language`) and write in the configured language.

## Inputs

From the workspace (`references/workspace.md` at the root of this plugin (two levels above this skill's directory); an Issue key or a name). Find each input by its frontmatter `type`, never by file name:

- **the problem**: `index.md` (the symptom, how it shows up, the acceptance criteria); when it says little, the user's description;
- **the analysis**: every `type: Analysis` file (`/devflow:analyze`): the map and the code findings, neutral about the problem;
- **the investigation**: the `type: Investigation` file when it exists (`/devflow:investigate-issue`): facts with evidence, such as the reproduction, outputs, data, logs.

Say which inputs you have. Ignore facts struck out under the investigation's Corrections section (headings in the configured language, e.g. "Correções", "Premissa"). When the investigation says the **premise was not confirmed**, the verdict is that: say the reported behavior was not reproduced, with the evidence, and what would make it true; do not look for a cause anyway. With neither analysis nor investigation, stop and suggest `/devflow:analyze` (to read the code) and `/devflow:investigate-issue` (to get facts).

## Steps

1. **Restate the problem** in one or two lines: the symptom, where and when it shows up. Confirm with the user if the Issue is vague.

2. **Classify every finding and fact** against the problem:
   - **explains**: it causes exactly the symptom, and a fact from the investigation shows it (a reproduction, a log line, data in the partial state). This is the **confirmed** cause;
   - **probable**: the analysis points to it and the path matches the symptom, but no fact proves it yet. Say which fact would prove or discard it;
   - **contributes**: it makes the problem worse or hides it (a swallowed error, missing logs at the failure point);
   - **unrelated**: a real improvement that has nothing to do with this problem;
   - **discarded**: a hypothesis a fact rules out, with the fact.
   Every item keeps its evidence (`file:line`, command and output, query).

3. **Verdict.** The root cause (confirmed, or the most probable with the confidence: high, medium, low) and why, in a few lines. When causes are only probable, list the cheapest check that would confirm each one.

4. **Recommendation.** What to change to fix the cause, what to change to make the contributing factors visible next time, and what to leave for later (unrelated improvements). No implementation plan: that is `/devflow:plan-issue`.

5. **Save** `<vault>/issues/<id>/diagnosis.md` (name in the configured language, e.g. `diagnostico.md`):

   ```markdown
   ---
   type: Diagnosis
   title: <problem in a few words>
   confidence: <high | medium | low>
   inputs: ["[[<real file name of each input, without .md>]]"]
   timestamp: YYYY-MM-DD
   ---

   # Problem
   # Verdict
   # Explains
   # Probable
   # Contributes
   # Discarded
   # Unrelated improvements
   # Recommendation
   # Missing facts
   ```

   Leave out empty sections. If a diagnosis already exists, show what changed in the verdict and update it.

6. **Next step.** With a confirmed cause: `/devflow:plan-issue`, which reads this file. With only probable causes: `/devflow:investigate-issue` for the missing facts first, then diagnose again. Then ask what was useful.
