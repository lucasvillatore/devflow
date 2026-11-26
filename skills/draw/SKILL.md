---
name: draw
description: (Experimental) Turn code or a system flow into a diagram of its concepts - a long function or file grouped into blocks by responsibility, or the path of data across services, queues, jobs and databases - analysed first, then a recommended format with reasons for the user to pick, then drawn with file:line on each block. Use when the user asks to draw, diagram or visualize a function, file or flow, or when understanding something would take a lot of reading.
argument-hint: "<function, file, flow, ISSUE-KEY or workspace name> | before/after <finding>"
---

# Draw

**Experimental**: the user is still testing whether diagrams help them read. Keep each diagram small and end by asking what helped and what did not.

The goal is understanding at a glance: concepts and how they connect, in the user's domain language, not a line-by-line flowchart.

## Steps

Three stops, in order: **analysis**, **suggestion**, **drawing**. The user picks the format; never draw before they do.

1. **Analysis.** Always analyse before drawing.
   - **An Issue key or workspace name as the argument** (`references/workspace.md`) draws the whole problem: read everything in `<vault>/issues/<id>/` that exists: the analyses (`type: Analysis`, their map), the investigation (`type: Investigation`, the signal, the reproduction and the facts) and the diagnosis (`type: Diagnosis`, the verdict and the classification). Say which ones you found. The map comes from the analysis; when there is none, build it following `references/analysis-map.md`.
   - **A function, file or flow as the argument**: if an analysis of the same target exists, use its map and say so; otherwise build the map following `references/analysis-map.md` at the root of this plugin (two levels above this skill's directory).
   - Show the map, plus what each block carries from the other files: findings, facts, and its diagnosis class.

2. **Suggestion.** Read `references/draw-formats.md` at the root of this plugin. From what the analysis found, recommend one **available** format and say:
   - why it is the best fit for this flow, pointing at what the analysis found (e.g. "three services call each other in order, so a sequence shows it best");
   - for each other format, available or planned, why it fits less, in one line.
   When the flow is too big for one picture, say how you would split it (an overview plus one diagram per group).
   Stop and wait for the user to pick. If they pick a planned format, say it is not available yet and ask for another.

3. **Drawing.** When there is a diagnosis or findings, color each block by what it carries, using the Vault's `.kb/diagrams.md` classes: the cause that **explains** in `bad`; **probable** causes in `bad` with a dashed border; what **contributes** in `wait`; blocks with only **unrelated** improvements in `info`; the rest without a class. Mark the path the reproduction takes with solid arrows and label where the signal goes red. When the problem needs two views (the code structure and the order of calls across systems), suggest both in step 2 and draw each one the user picks.

   In the chosen format, following the Vault's `.kb/diagrams.md` when it exists (colors per state, solid line for the normal path, dashed for a detour or an inferred link). At most about 12 nodes per diagram. Each node: the concept name and, on a second line, the `file:line` range (`calc[Compute price<br/>cart.service.ts:120-210]`). Under the diagram, a short legend: one line per block saying what it does.

4. **Show it with zoom.** Every drawing becomes a zoomable page (a frame per diagram with zoom in/out, fit and drag, like draw.io), always saved in the workspace (`references/workspace.md`; ask for a name if the session has none):
   - write the data (title, subtitle, the diagrams with their legend, and the explanation for a before/after, before and after sharing a `pair` id so they render side by side) to `<vault>/issues/<id>/diagrams/<slug>.json` (folder name in the configured language, e.g. `diagramas/`);
   - run `python3 <plugin>/scripts/draw_view.py <that json> <same folder>/<slug>.html --open`, which writes the page next to the data and opens it in the browser;
   - redrawing the same thing overwrites the same `<slug>` files.
   Publish it as an Artifact only if the user asks. Also show the Mermaid source in the conversation, short.

5. **Also keep it in the knowledge?** When the drawing explains something that outlives this work, offer to copy the Mermaid source to where it will be read again, and write only if the user agrees:
   - a business flow → the knowledge base (suggest `/devflow:kb-journey` or `/devflow:kb-context` to fold it into a journey or context);
   - a technical flow of a repository → its profile `<vault>/devflow/projects/<repo>.md`, under a `## Diagrams` section: the Mermaid source only, no link to the page (the workspace is git-ignored, so the link would break on other machines).

6. **Feedback.** Ask what helped and what did not (format, size, grouping, missing detail). When the answer changes how diagrams should be drawn or which format fits which case, offer to record it in the Vault's `.kb/diagrams.md` or propose a change to `references/draw-formats.md`.

## Before/after

When the argument asks for a before/after, or the user picks one improvement from an analysis, draw the same part of the code twice, side by side: **before** (as it is) and **after** (with the improvement). Same layout and names in both so only the change stands out: what is removed or changed in `bad`, what is new in `ok`. Steps 1, 2, 4, 5 and 6 still apply (the map, the format the user picks, the zoomable page in the workspace, keeping it in the knowledge, feedback). Under the two diagrams, the explanation, always in this order:

1. **What changes**: one line per block that enters, leaves or moves.
2. **Why**: each reason with its basis, strongest first:
   - **fact**: data, log or reproduction from the investigation (e.g. "1,150 of yesterday's 1,200 updates had no change");
   - **code**: the `file:line` that shows the problem;
   - **team convention**: a Vault convention or a guardrail;
   - **principle**: a named one (idempotency, fail fast, deep module, single responsibility).
   A reason with no basis is marked **opinion**.
3. **Gain**, measurable when possible: fewer calls, complexity from X to Y, a test that becomes possible, a partial failure that disappears.
4. **Cost and risk**: what gets worse or more complex, what could break, and whether it is reversible (two-way door) or not (one-way door).
5. **Alternatives discarded**: other ways to solve it, each with why it is not the recommendation.
