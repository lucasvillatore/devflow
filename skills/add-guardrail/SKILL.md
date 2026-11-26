---
name: add-guardrail
description: Turn feedback about the agent's behavior or code into a guardrail in the user's global Claude setup - a blocking PreToolUse hook when the rule can be checked mechanically, a rule file in ~/.claude/rules/ when it needs judgement, or a team convention in the Vault. Tests the hook before registering it. Use when the user dislikes something Claude did and wants it never to happen again, or asks to add a guardrail, hook or rule.
argument-hint: "<what Claude did that should not happen>"
---

# Add a guardrail

Turn one piece of feedback into one guardrail. Guardrails are the user's: they live in `~/.claude/`, never in devflow or in a repository.

The scripts and templates are at the root of this plugin (two levels above this skill's directory): `scripts/guardrail.py` and `templates/guardrail/hook.py`.

## Steps

1. **Understand the rule.** From the feedback (and the code or conversation it refers to), state the rule in one sentence, with what to do instead, and two or three concrete examples: one that breaks it and one close to it that does not. Confirm with the user.

2. **Pick the mechanism** and say why:
   - **Hook**: the rule can be checked on the text being written (a pattern in added lines of certain files). Blocks the edit and explains why.
   - **Rule file**: the rule needs judgement ("do not create an abstraction for a single use"). Goes to `~/.claude/rules/<topic>.md`; with `paths:` in its frontmatter (e.g. `["**/*.ts"]`) when it applies only to some files, so it loads only when those files are touched. Prefer adding to an existing topic file over creating a new one. Do not grow `~/.claude/CLAUDE.md`.
   - **Vault convention**: the rule is the team's, not only the user's. Goes to `<vault>/devflow/conventions.md` (Vault path in `~/.config/devflow/config.json`).
   When a hook would have frequent false positives, say so and propose the rule file instead.

3. **Write it.**
   - **Hook** in `~/.claude/hooks/<rule-name>.py`:
     - Follow the folder's pattern: read the existing hooks; if they share a base module (e.g. a `Guardrail` class), subclass it like the neighbors do. Otherwise start from `templates/guardrail/hook.py` (self-contained, standard library only).
     - Check only **added** lines, so existing code never blocks an edit. Block by default (a `deny` decision with the rule and the offending lines). Write the message in the user's language.
     - Write `~/.claude/hooks/<rule-name>.cases.json` with at least one case that must block and one that must pass, from the examples of step 1 (format in the script's docstring).
     - Run `python3 <plugin>/scripts/guardrail.py test <hook> <cases>` until every case passes.
   - **Rule file** or **convention**: one or two short lines, phrased as an instruction with the reason.
   Show the user the result (hook code and cases, or the text and its destination) and wait for confirmation before the next step.

4. **Register** (hook only). Run `python3 <plugin>/scripts/guardrail.py register <hook> --dry-run`, show the diff, wait for confirmation, then run it without `--dry-run`. Never edit `settings.json` by hand.

## Answer

The rule, the mechanism, the files written, the backup path, and that hooks and rules take effect in the next session (or after `/hooks` reloads them).
