# Workspace

Where devflow skills exchange files: `<vault>/issues/<id>/` (Vault path in `~/.config/devflow/config.json`). The `<id>` is either:

- an **Issue key** from the tracker (`[A-Z][A-Z0-9]+-\d+`, e.g. `CAT-5924`): the workspace of that Issue;
- a **name** for work without an Issue: lowercase words with hyphens (e.g. `vendor-service-update`, `slow-job`). A name never looks like a key.

## Finding it

1. From the argument: a key, a browse link (take the key) or a name.
2. Otherwise from the conversation: a workspace already used in this session.
3. Otherwise ask once, suggesting a name from the subject ("I'll call it `vendor-service-update`, ok?"). `retro` works without a workspace and only asks when the user wants to save; `draw` always saves its page, so it asks.

## Creating it

When the folder does not exist, create it with `index.md` and `log.md` from `templates/issue/<language>/` at the root of the plugin. Without an Issue: `key:` and `link:` empty, `title` and `description` from the subject, `status:` empty; the Context section says what the work is about. `log.md` starts with only its heading: it records changes to the Issue (pick, plan, pull request), not the creation of the folder.

## Without an Issue

Every skill works the same way; only what depends on the tracker is skipped: no assignee or status changes, no Issue link, no key in titles or branch names unless the user gives one.

When the work later becomes an Issue, `/devflow:pick-issue <KEY> <name>` adopts the workspace: renames the folder to the key, fills the tracker fields of `index.md` and keeps every other file.

## Names

Files and folders that skills create in a workspace are named in the configured language (`investigacao.md`, `diagramas/`, `retro.md` stays `retro.md` when the word is the same), except `index.md`, `log.md` and `scripts/`, which keep their names in every language. Names are for people; skills find files by `type`.

## Finding files inside it

Find workspace files by their frontmatter `type`, never by file name: names follow the configured language (`investigation.md` is `investigacao.md` in pt-BR) and may change. When linking one file from another, use its real file name in the wikilink.

This table is the single source of who writes and reads what (`scripts/overview.py` draws it; keep the last two columns as plain lists of skill names).

| type | What | Written by | Read by |
| :-- | :-- | :-- | :-- |
| `Issue` | `index.md`: the Issue or the work (created by pick-issue, or by whichever skill opens the workspace) | pick-issue | plan-issue, investigate-issue, diagnose, open-pr |
| `Task` | one Task; the **Planning** is the Task whose file name starts with `1-` (rules in `references/tasks.md`) | plan-issue, refactor-plan, refactor | plan-issue, refactor, open-pr |
| `Analysis` | map and findings of a target | analyze | investigate-issue, diagnose, draw, plan-issue, refactor, refactor-plan |
| `Investigation` | facts, signal, premise, corrections | investigate-issue | diagnose, draw, plan-issue, open-pr, retro |
| `Diagnosis` | verdict on the problem | diagnose | draw, plan-issue, open-pr |
| `Refactor` | proof of one refactoring | refactor | open-pr |
| `Retro` | retrospective of a session | retro | |
| `log.md` | dated changes to the Issue (no frontmatter) | pick-issue, plan-issue, refactor-plan, open-pr | plan-issue |
| `diagrams/` | zoomable pages and their data | draw | |

`log.md` has no frontmatter. Folders (`diagrams/`, `scripts/`, `refactor/`, `refactor-plan/`) hold supporting files, not typed documents; `refactor-plan/plan.md` is the refactor plan's own record.
