---
name: ask
description: Explain what devflow is and which devflow skill fits a situation. Use when the user asks what devflow does, which command to use for something, or whether devflow can do something.
argument-hint: "[question]"
---

# Ask devflow

1. Run `python3 <plugin>/scripts/catalog.py` (the plugin root is two levels above this skill's directory). Its output is the only source of truth about what devflow has; do not describe skills from memory.

2. **No question:** give a short overview in the user's language: what devflow is, the Areas in order with their skills, which Areas are off, and whether setup is done.

3. **With a question:** answer with the best fit:
   - **It exists:** name the skill (`/devflow:<skill>`), one sentence on why it fits, and what to pass to it. If its Area is off, say so and that `/devflow:setup` turns it on. If two skills fit, say which comes first.
   - **It is planned:** say it is in the backlog and not available yet, and the closest thing that exists today, if any.
   - **It does not exist:** say so plainly, then ask whether the user wants to suggest it as an issue on the devflow repository (in the catalog output).

4. **If the user wants the issue:** write a draft in English, in a code block, and stop:

   ```
   Title: <short imperative summary>

   ## Situation
   <what the user was trying to do>

   ## Expected
   <what devflow should offer>

   ## Today
   <what exists that comes closest, or "nothing">
   ```

   Opening it on GitHub automatically is not available yet: the user copies it, or explicitly asks you to run `gh issue create` on the repository.

For a visual overview (Areas, the usual flows, the workspace files), run `python3 <plugin>/scripts/overview.py --open`: it writes `<vault>/devflow/overview.html` in the user's language and opens it.

## Rules

- Never invent a skill, flag or Area that is not in the catalog.
- Answer in a few lines; the catalog is for you, not to be pasted whole.
