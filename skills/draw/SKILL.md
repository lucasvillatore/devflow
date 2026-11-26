---
name: draw
description: (Experimental) Turn code or a system flow into a diagram of its concepts - a long function or file grouped into blocks by responsibility, or the path of data across services, queues, jobs and databases - analysed first, then a recommended format with reasons for the user to pick, then drawn with file:line on each block. Use when the user asks to draw, diagram or visualize a function, file or flow, or when understanding something would take a lot of reading.
argument-hint: "<function, file or flow>"
---

# Draw

**Experimental**: the user is still testing whether diagrams help them read. Keep each diagram small and end by asking what helped and what did not.

The goal is understanding at a glance: concepts and how they connect, in the user's domain language, not a line-by-line flowchart.

## Steps

Three stops, in order: **analysis**, **suggestion**, **drawing**. The user picks the format; never draw before they do.

1. **Analysis.** Always analyse before drawing.
   - If an analysis of the same target exists in the Issue workspace (`type: Analysis`, written by `/devflow:analyze`), use its map and say so; its findings can be highlighted in the drawing (blocks with high-severity findings in the `bad` color).
   - Otherwise build the map following `references/analysis-map.md` at the root of this plugin (two levels above this skill's directory) and show it.

2. **Suggestion.** Read `references/draw-formats.md` at the root of this plugin. From what the analysis found, recommend one **available** format and say:
   - why it is the best fit for this flow, pointing at what the analysis found (e.g. "three services call each other in order, so a sequence shows it best");
   - for each other format, available or planned, why it fits less, in one line.
   When the flow is too big for one picture, say how you would split it (an overview plus one diagram per group).
   Stop and wait for the user to pick. If they pick a planned format, say it is not available yet and ask for another.

3. **Drawing.** In the chosen format, following the Vault's `.kb/diagrams.md` when it exists (colors per state, solid line for the normal path, dashed for a detour or an inferred link). At most about 12 nodes per diagram. Each node: the concept name and, on a second line, the `file:line` range (`calc[Compute price<br/>cart.service.ts:120-210]`). Under the diagram, a short legend: one line per block saying what it does.

4. **Save.** Ask where to save it, suggesting the place it will be read again:
   - a business flow → the knowledge base (suggest `/devflow:kb-journey` or `/devflow:kb-context` to fold it into a journey or context);
   - a technical flow of a repository → its profile `<vault>/devflow/projects/<repo>.md`, under a `## Diagrams` section;
   - something only this Issue needs → `<vault>/issues/<KEY>/diagrams.md` (or inside `investigation.md` when it exists).
   Write only after the user picks.

5. **Feedback.** Ask what helped and what did not (format, size, grouping, missing detail). When the answer changes how diagrams should be drawn or which format fits which case, offer to record it in the Vault's `.kb/diagrams.md` or propose a change to `references/draw-formats.md`.
