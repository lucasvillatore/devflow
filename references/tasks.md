# Tasks

How devflow skills write and close Tasks in a workspace (`references/workspace.md`). Read `~/.config/devflow/config.json` (`vault`, `language`) before writing: names and headings follow the configured language. Every skill that creates Tasks follows this, so the Planning, the numbering and the log stay consistent.

## The Planning

- The Planning is always the Task numbered 1: `1-<planning>.md` (`1-planning.md`, `1-planejamento.md` in pt-BR), from `templates/issue/<language>/planning.md`.
- When a skill creates Tasks and there is no Planning yet, it creates one first: Context = what the Tasks come from (decisions, or a link to the skill's record), `status: doing` until the Tasks are written, then `done`.
- Under its Acceptance criteria, every Task is listed as `- [ ] [[N-slug]]`.

## Writing Tasks

- From `templates/issue/<language>/task.md`, named `<N>-<slug>.md`: `N` is the next free number **after the highest existing one, never 1**; `slug` short kebab-case in the configured language.
- One Task is one deliverable and one commit, in one repository.
- Fill Context (only what this Task needs), What, How, Why (only when not obvious), Acceptance criteria (verifiable).
- `paths`: the repository or files it touches (absolute paths that exist on this machine). `depends_on`: wikilinks of the Tasks that must be `done` first. `status: todo`, `timestamp` today.
- Add each new Task to the Planning's checklist.
- Add one `log.md` entry on top: `## YYYY-MM-DD` and `**Plan**: <n> Tasks created (<repositories>)`, or `**Replan**` when Tasks are added to an existing Planning.
- Never rewrite a Task with `status: done`, nor uncheck it. Before changing a Task that is `todo`, `doing` or `blocked`, show the change and wait for confirmation.
- **The Planning is the exception**: adding Tasks to its checklist and ticking boxes are always allowed, and a re-plan reopens it (`status: doing`), updates its Context and How, and closes it again (`done`).

## Closing a Task

When a Task's acceptance criteria are met (by a skill, or by hand while there is no development skill):
- set its `status: done` and `timestamp` today;
- tick its box in the Planning (`- [x]`);
- decisions taken while doing it go to its `Decisions` section;
- the commit is the user's call: offer it, never run it unasked.

No `log.md` entry: the log records changes to the Issue, not to each Task.
