---
name: plan-issue
description: Plan an Issue - interview the user in rounds until no decision is open, recording decisions in the Issue workspace as they are made, then split the work into Task files with dependencies. Use when the user wants to plan, break down or design the solution of an Issue (Jira key like ABC-123), or to resume an unfinished planning.
argument-hint: "<ISSUE-KEY>"
---

# Plan an Issue

Turn an Issue into Tasks through an interview. Writes only to the Issue workspace. No code, no tracker.

## Before starting

1. Read `~/.config/devflow/config.json` (`vault`, `language`). Without it, stop and tell the user to run `/devflow:setup`.
2. Get the key (`[A-Z][A-Z0-9]+-\d+`) from the argument; without one, ask. The workspace is `<vault>/issues/<KEY>/`.
3. Read the workspace: `index.md` (the Issue), `log.md`, every `N-*.md`. Without `index.md`, suggest `/devflow:pick-issue <KEY>` first, or ask the user for the context and go on.
4. Read `<vault>/devflow/workflow.md` (Task statuses) and, from the Vault's knowledge base, the glossary terms and contexts that match the Issue's subject (search the Vault for its key words). Read only what is relevant.

Read `references/grilling.md` and the templates in `templates/issue/<language>/` at the root of this plugin (two levels above this skill's directory). Write every file in the configured language.

## Files

- `1-planning.md` (title in the configured language, e.g. `1-planejamento.md` for pt-BR) from `planning.md`. It is a Task too.
- One file per Task from `task.md`, named `<N>-<slug>.md`: `N` is the next free number in the folder, `slug` is short kebab-case in the configured language.
- Links between files are Obsidian wikilinks without extension: `[[2-adjust-query]]`.

## Steps

1. **Open or resume the planning.**
   - No planning file: create it with `status: doing`, `timestamp` today, `paths` from `index.md`.
   - Planning exists: its Context holds the decisions made so far. Summarize them in two or three lines and resume the interview from the open ones.

2. **Interview** following `references/grilling.md`. After **each** answered round, write the settled decisions into the planning file before asking the next round:
   - **Context**: the decisions, one short line each, grouped by subject.
   - **How**: where the changes go, how the work is split, how data is read and stored.
   - **Knowledge to record**: terms, business rules or repository facts that came up and are not in the Vault. Do not write them into the knowledge base.
   An Issue that spans several repositories is planned once: decisions usually hold for all of them. Ask which repository each change belongs to.

3. **Stop** when the frontier is empty and wait for the user to confirm you are aligned.

4. **Write the Tasks.** One Task is one deliverable and one commit, in one repository.
   - Fill Context (only what this Task needs), What, How, Why (only when it is not obvious), Acceptance criteria (verifiable).
   - `paths`: the repository or files this Task touches (absolute paths that exist on this machine).
   - `depends_on`: wikilinks of Tasks that must be `done` first. Tasks without dependencies between them can be done in parallel.
   - `status: todo`, `timestamp` today.
   - In the planning file, list every Task under the Acceptance criteria as `- [ ] [[N-slug]]` and set the planning's `status: done`. Whoever finishes a Task checks its box.
   - Add a `log.md` entry on top: `## YYYY-MM-DD` and `**Plan**: <n> Tasks created (<repositories>)`.

## Re-planning

When the planning is resumed after Tasks exist:
- Never rewrite a Task with `status: done`, nor uncheck it in the planning.
- New Tasks take the next free number.
- Before changing a Task with `status: todo`, `doing` or `blocked`, show the change and wait for confirmation.
- Set the planning back to `doing` while the interview runs and to `done` when the Tasks are written. Log it as `**Replan**`.

## Answer

In the user's language, short: the decisions in a few lines, the Tasks in order (number, title, repository, dependencies), the "knowledge to record" items if any, and which Task can start first.
