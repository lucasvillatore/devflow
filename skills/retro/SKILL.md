---
name: retro
description: Retrospective of the current session - lists what went wrong or cost the user time, by severity, with the fix for each (a guardrail, a devflow change, a Vault convention), and the knowledge the session had to discover that is missing from the Vault. Writes nothing without the user's choice. Use when the user asks for a retro or retrospective of the session.
disable-model-invocation: true
argument-hint: "[ISSUE-KEY, only to pick where retro.md is saved]"
---

# Retro

Look back at this session and turn what went wrong into lasting fixes to the environment: checks, pointers, access, conventions. Categories adapted from Matt Pocock's `retro` (MIT, see `THIRD_PARTY_NOTICES.md`). The session is the evidence: quote it. Speak the user's language.

## Before starting

- Read `~/.config/devflow/config.json` (`vault`). Without it, skip the Vault parts and say so.
- The evidence is this conversation. If it was compacted and the summary is not enough, read the session transcript: the newest `.jsonl` in `~/.claude/projects/<working directory with / replaced by ->/`. Read only what you need.
- The Issue key comes from the argument or the conversation, when there is one.

## 1. Find the candidates

Go through the session looking for:

- **Corrections**: the user said something was wrong, asked to redo, undid a change, or repeated an instruction.
- **Friction**: questions the user could not answer, back-and-forth on something that was already known, long detours, permission prompts that kept coming back.
- **Rule breaks**: something done against the user's preferences, the Vault conventions or a devflow skill's steps (an edit without confirmation, a write in production, a file outside the Task).
- **Navigation**: the agent took long to find a file, a command or where something lives. A pointer (repository profile, Vault convention) would have saved it.
- **Automated checks**: a mistake a check could have caught (lint, types, tests, a hook). Look at what the repository already has first (`package.json` scripts, pre-commit, CI): a check that exists but is not wired or is broken is the finding. A repository with no check at all is a finding too.
- **Information access**: something the agent needed and could not see (logs, data, a service, a document). Could it get read-only access next time?
- **Tool economy**: expensive or repeated tool calls (huge outputs, the same search many times, a slow command) that a narrower command or a small script would replace.
- **Steering files**: instructions in `~/.claude/CLAUDE.md`, `~/.claude/rules/`, the repository's `CLAUDE.md` or the Vault conventions that were ignored, contradicted each other, or change nothing (no-ops). Large steering files are a finding by themselves.
- **devflow gaps**: a skill missing a step, asking the wrong thing, or a step the user had to do by hand every time.
- **Missing knowledge**: facts the session had to discover (a business rule, a term, a repository's quirk, a command, how to reach some data) that are not in the Vault. Check the Vault before listing one.

Drop anything that happened once for a reason that will not repeat.

## 2. Show the list

In two groups, highest severity first. Severity: **high** (wrong result, risk, or the user had to step in), **medium** (time lost), **low** (annoyance).

**Improvements**, one block each:

```
[high] <what happened, one line>
  Evidence: "<short quote or the action>"
  Fix: <what to change> → <where>
```

Where the fix goes:
- a **mechanical** rule (a fixed pattern, a banned call, a file location) → a deterministic check: **guardrail** hook, `/devflow:add-guardrail "<the rule>"`, or, when it is the team's, a lint rule or CI job in the repository (suggest it; the repository is the team's);
- a **judgement** rule about Claude's behavior → **guardrail** as a rule file (`/devflow:add-guardrail` picks it);
- a team rule that needs judgement → **Vault convention** (`<vault>/devflow/conventions.md`);
- a repository fact (command, branch, resource, where things live) → **repository profile** (`<vault>/devflow/projects/<repo>.md`);
- an instruction that is a no-op or contradicts another → **remove or merge it**, in the file where it lives;
- a devflow skill that should behave differently → **devflow issue** (draft in English, same format as `/devflow:ask`, on the repository shown by `python3 <plugin>/scripts/catalog.py`).

Prefer a check to an instruction: an instruction costs context in every session and can be ignored; a check costs nothing until it fires.

**Missing knowledge**, one line each: the fact, where it belongs (glossary term, business rule, journey, repository profile, investigate notes) and the evidence.

Then ask which items to act on.

## 3. Act on the chosen items

- **Guardrail**: give the exact `/devflow:add-guardrail "..."` command for each; the user runs it (one guardrail per run).
- **Vault convention, repository profile, investigate notes**: show the lines and the file, write after confirmation.
- **Knowledge base** (term, rule, journey): suggest the kb skill that writes it (`/devflow:kb-context` or `/devflow:kb-journey`); do not write base documents here.
- **devflow issue**: show the draft; run `gh issue create` only if the user asks.

## 4. Record

When there is an Issue workspace, write `<vault>/issues/<KEY>/retro.md` with the list and what was done with each item. Do not add a `log.md` entry: the log only records changes to the Issue's state.

## Answer

What was acted on and where, and what was left (with the commands to run later).
