---
name: kb-journey
description: Create or evolve a journey in the knowledge base following its template - the path a person takes to a goal, with steps that point to rules and contexts, detours and open points. Use when asked to create, draw, complete or reorganize a journey.
argument-hint: "<Journey name> [what to change] [--base <path>]"
---

# Create or evolve a journey

First read `references/kb-process.md` at the root of this plugin (two levels above this skill's directory).

1. Find the base and read the journey template in `.kb/templates/`, `.kb/style.md` and `.kb/diagrams.md`.
2. Check it is a journey: a **person** walks the path. If it is a process the business runs on its own, tell the user it is a business context and suggest the `kb-context` skill.
3. Read the journeys `index.md` and, if the journey exists, its file.
4. Read the indexes of the contexts the journey crosses, to point each step to the right place. Use the rules and contexts that exist. What does not exist goes to the open points section. Do not invent steps.
5. Show the user the proposed steps, detours and open points. **Stop** and wait for approval before writing, unless the request already says exactly what to change.
6. Write with the draft status (or keep the current status of an active journey, if the change is small and the user asked).
7. Update the journeys `index.md`, grouped by who walks the path.
8. Run `python3 <plugin>/scripts/kb_verify.py --base "<base>" --path "<journeys folder>"` and fix the errors.

Every format correction from the user becomes a convention in the journey template or in `.kb/style.md`.
