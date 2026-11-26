---
name: plan-issue
description: Plan an Issue - interview the user in rounds until no decision is open, recording decisions in the Issue workspace as they are made, then split the work into Task files with dependencies. Use when the user wants to plan, break down or design the solution of an Issue (Jira key like ABC-123), or to resume an unfinished planning.
argument-hint: "<ISSUE-KEY or workspace name>"
---

# Plan an Issue

Turn an Issue into Tasks through an interview. Writes only to the Issue workspace. No code, no tracker.

## Before starting

1. Read `~/.config/devflow/config.json` (`vault`, `language`). Without it, stop and tell the user to run `/devflow:setup`.
2. Find the workspace following `references/workspace.md` at the root of this plugin (two levels above this skill's directory); it may be an Issue key or a name.
3. Read the workspace, finding files by frontmatter `type` (see the reference): the Issue, `log.md`, every Task, and the Diagnosis, Investigation and Analysis files when they exist. Decisions they already settle (the root cause, a confirmed fact) are not asked again; open them as context in the first round. Without a workspace: for an Issue key, suggest `/devflow:pick-issue <KEY>` first; for a name, create it (see the reference) with the context the user gives.
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

4. **Write the Tasks** following `references/tasks.md` at the root of this plugin: numbering after the Planning, the checklist in the Planning, the `**Plan**` log entry. Then set the Planning's `status: done`.

## Re-planning

When the planning is resumed after Tasks exist, follow the rules of `references/tasks.md` (done Tasks are never rewritten, new Tasks take the next number, changes to open Tasks are confirmed first). Set the Planning back to `doing` while the interview runs and to `done` when the Tasks are written; the log entry is `**Replan**`.

## Answer

In the user's language, short: the decisions in a few lines, the Tasks in order (number, title, repository, dependencies), the "knowledge to record" items if any, and which Task can start first.
