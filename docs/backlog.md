# Backlog

Items deferred on purpose, and the v0 Components not built yet.

## investigate-issue (investigate)

A step between `pick-issue` and `plan-issue` for Issues whose cause is not known yet: planning asked questions the user could not answer before understanding how the system works. Explores on purpose (code in the Issue's `paths`, `awsq`/`dbq` read-only, reproduction), based on Matt Pocock's `diagnosing-bugs` (a red-capable feedback loop before any hypothesis). Writes `issues/<KEY>/investigation.md` (not a Task): how it works today with `file:line` evidence marked confirmed or inferred, reproduction, root cause or live hypotheses, open questions, knowledge to record. `plan-issue` reads it, and offers to pause and investigate when the user answers "I don't know". Also usable without an Issue.

## dev-task (development)

Not built for now: the user asks for the implementation directly ("implement Task 2 of ABC-123"). Build it if keeping statuses, validation and commits consistent by hand gets tiresome. Draft decisions:

- `/devflow:dev-task <KEY> [N]`: without `N`, the next `todo` Task whose dependencies are `done`, among the Tasks of the repository the session is in.
- Branch and commit formats in `<vault>/devflow/git.md` (defaults in the template).
- Validation commands (changed files only, build, full suite) and the default branch in the repository profile `<vault>/devflow/projects/<repo>.md`; asked once and written when missing.
- Two stops: before implementing (what changes and why) and before committing (summary and message). No push.
- Files changed outside the Task: list them and ask; never revert without confirmation.
- Questions settled during the Task go to a "Decisions" section at the end of the Task file.
- Closing: Task `done`, its box checked in the Planning, `log.md` entry with the commit hash; `blocked` with the reason when stopped.
- Parallel Tasks in worktrees: later (the worktree starts from the default branch, not the Task's).

## Personal layer (`ai-setup`)

A personal git repo that travels between the user's machines: preferences in `AGENTS.md` (open format, any harness), `CLAUDE.md` with only `@AGENTS.md`, personal hooks in `hooks/`, and the devflow config (`devflow.json`) instead of `~/.config/devflow/config.json`. Until then, guardrails are written straight into `~/.claude` (global) or the repository's `.claude/` (local).

Decided so far:
- Name: `ai-setup`, private on the user's GitHub, cloned at `~/dev/ai-setup`.
- Hooks keep the Claude Code format; the logic is not split into a harness-neutral layer until a second harness exists.
- The setup asks only for the ai-setup path on a new machine; everything else comes from it.

Draft of the preferences `AGENTS.md` (from the user's current workflow):

```markdown
# Preferências

- Responder em português, curto e direto.
- Antes de criar ou editar arquivos, dizer o que muda e esperar confirmação. "Manda bala" ou "pode fazer" liberam.
- Ações externas ou irreversíveis (push, PR, banco, Jira, Drive) só com confirmação ou pedido explícito.
- Commitar só quando eu pedir.
- No planejamento, perguntar em vez de mandar agentes explorarem o código. Busca pontual (grep, ler um arquivo) só quando eu liberar.
- Quando eu colar um exemplo real de dado (JSON, resposta de API), tratar como fonte da verdade do contrato.
- Quando algo der errado, dizer de forma direta e corrigir.
- Preferência nova vai para este arquivo ou vira guardrail (`/devflow:add-guardrail`), nunca para memória.
```

The current personal hooks are in `~/.claude/hooks/` (`guardrails.py` plus 6 rules).

## Guardrails per repository

`add-guardrail` writes only to the user's global `~/.claude/`. Later: a repository scope, either personal (script in `~/.claude/hooks/`, registered in the repository's `.claude/settings.local.json`) or the team's (in the repository's `.claude/`, committed).

## Review stage (development)

A reviewer agent that reads only the diff and enforces judgement-call conventions from the Vault, so the implementing agent does not carry them in context.

## Staging and production

`deploy-staging` (merge, push with Trufflehog retry, pipeline watch) and `handoff-prod` (script + README package, Drive share).

## New Relic

Investigate component, once the connector authentication works.

## Issue trackers other than Jira

`pick-issue` is Jira-only; `0-issue.md` stays tracker-agnostic so others can be added.

## Company-specific kb configuration

When a Vault is created for a company, its own kb configuration (system terms, process part folders, examples from the real base) is applied on top of the generic template, with keys in the `base.yaml` format.

## Existing knowledge bases

A knowledge base that already exists outside the Vault is not migrated automatically. The user decides later whether to bring it in.

## More than one Vault per machine

The setup is per machine and points to a single Vault, so personal and company projects on the same computer share conventions and glossary. Options when it matters: a file in the repository pointing to another Vault, or one Vault per root folder (e.g. `~/work` → Vault A, `~/dev` → Vault B).

## Semantic versioning

`plugin.json` has no `version` today, so every commit is a new version (identified by its SHA) and auto-update picks it up. Move to semantic versions with a `CHANGELOG.md` once the plugin stabilizes or other people use it. Remember: with a fixed `version`, new commits do not reach users until it changes.

## Standard issue for the devflow repository

`/devflow:ask` drafts an issue when something does not exist. Next: a standard issue template on the repository and opening it with `gh issue create` after the user confirms.
