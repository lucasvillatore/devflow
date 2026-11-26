---
name: kb-close
description: Close knowledge base documents or a whole business context after the user approves them - moves the status from draft to active, records the decisions in the context's log.md and archives the work folder. Use when the user says a document or context is approved.
argument-hint: "<file, folder or context> [--base <path>]"
---

# Close what was approved

First read `references/kb-process.md` at the root of this plugin (two levels above this skill's directory).

Use this skill only with the user's explicit approval in the chat for the documents in question.

1. Find the base and list the target's documents with the draft status (`status.draft` in `base.yaml`). Show the list if the target is a folder.
2. Run `python3 <plugin>/scripts/kb_verify.py --base "<base>" --path "<target>"`. With errors, do not close: show the errors.
3. In each approved document, replace the draft status with the active status (`status.active`) and set `timestamp` to today. Change nothing else.
4. If the target is a context with a work folder in `.kb/work/<Context>/`:
   - Append to the context's `log.md` (create it if missing) an OKF entry, in the base's language:

     ```
     ## YYYY-MM-DD

     **Creation** (or **Update**) of the context. Documents: <list>.

     Decisions:
     - <each decision from decisions.md, one line>
     ```

     Newest dates go on top.
   - Move the work folder to `.kb/work/archived/<Context> YYYY-MM-DD/`.
5. Tell the user what became active and what is still a draft.
