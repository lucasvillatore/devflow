---
name: analyze
description: (Experimental) Analyze a function, file or system flow - map its blocks and connections, suggest which improvement lenses fit (complexity, partial failures, error handling...) for the user to pick, then report findings with severity, file:line evidence and suggestions, saved for other skills to reuse. Use when the user asks to analyze code or a flow, review its design, or find improvements.
argument-hint: "<function, file or flow>"
---

# Analyze

**Experimental**: the user is still testing it. End by asking what was useful.

Three stops, in order: **map**, **lens suggestion**, **findings**. Analysis only: never change code here.

The references are at the root of this plugin (two levels above this skill's directory): `references/analysis-map.md` and `references/analysis-lenses.md`. Read `~/.config/devflow/config.json` (`vault`, `language`) and write in the configured language.

## Steps

1. **Map.** If an analysis of the same target already exists in the Issue workspace, show its map, ask whether the code changed since, and reuse it when it did not. Otherwise build the map following `references/analysis-map.md` and show it.

2. **Rejected before.** Read the section "Rejected improvements" of the repository profile `<vault>/devflow/projects/<repo>.md` (heading in the configured language). Improvements listed there are not suggested again; when a finding matches one, mention it in one line ("skipped: rejected on <date> because <reason>") unless the code changed in a way that removes the reason.

3. **Lens suggestion.** From what the map shows, recommend the **available** lenses in `references/analysis-lenses.md` that are worth it for this target, each with why (pointing at what the map found, e.g. "blocks 3 and 5 write to two APIs in sequence"), and in one line each why the others are not worth it here. Planned lenses can be mentioned as "would help, not available yet". Stop and wait for the user to pick.

4. **Findings.** Apply the chosen lenses. Each finding: severity, evidence (`file:line`), why it matters, the suggestion, the effort and the recommendation strength (strong, worth exploring, speculative; see the lenses reference). Order by severity, then strength. Read the code you need for each finding; do not guess. When a lens finds nothing, say so in one line.

5. **Save.** In the Issue workspace when there is an Issue (`<vault>/issues/<KEY>/analysis-<slug>.md`, file name in the configured language, e.g. `analise-<slug>.md`), otherwise ask whether to save it and where. Format:

   ```markdown
   ---
   type: Analysis
   title: <target>
   target: <function, file or flow>
   paths: [<repositories or files>]
   lenses: [<lenses applied>]
   timestamp: YYYY-MM-DD
   ---

   # Map
   <blocks: name, what it does, file:line, inferred>
   <connections>

   # Findings
   ## <lens>
   - **[high · strong]** <finding> (`file:line`): <why it matters>. Suggestion: <...>. Effort: <...>.
   ```

6. **Rejections.** When the user rejects a finding with a reason that will still hold later (a constraint, a decision, a trade-off they accept), offer to record it in the repository profile under "Rejected improvements": `- <improvement> (<module or file>): <reason>. YYYY-MM-DD`. Skip reasons that are only "not now".

7. **Next steps.** Offer what the findings can become: a before/after diagram of one improvement (`/devflow:draw before/after <finding>`), a diagram of the map (`/devflow:draw` reads this file and highlights the blocks with findings), Tasks (`/devflow:plan-issue`), a guardrail for a pattern that should never come back (`/devflow:add-guardrail`). Then ask what was useful and what was not.
