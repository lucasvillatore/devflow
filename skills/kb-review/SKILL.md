---
name: kb-review
description: Review knowledge base documents or a business context against the templates, style and checklist in the .kb/ configuration, and against the rest of the base. Only reports problems, fixes nothing. Use when asked to review, check or audit base documents.
argument-hint: "[file or folder] [--base <path>]"
---

# Review the base

First read `references/kb-process.md` at the root of this plugin (two levels above this skill's directory).

1. Find the base. Without an argument, review the whole base.
2. Run this plugin's `kb-reviewer` agent with the base path, the target and the path of the plugin's `scripts/kb_verify.py`. For the whole base, run one reviewer per context and one for the journeys and glossaries, in parallel.
3. Show the user the problems grouped by file, from most severe (structure, content) to least severe (writing, names).
4. **Fix nothing.** Fixing only happens when the user asks.
5. Show the "outside the checklist" items separately, with the suggested convention for `.kb/`.
