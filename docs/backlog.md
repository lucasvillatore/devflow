# Backlog

Items deferred on purpose, and the v0 Components not built yet.

## investigate-issue (investigate)

Gathers **facts** about a problem, without concluding: planning asked questions the user could not answer before understanding how the system behaves. Based on Matt Pocock's `diagnosing-bugs`: build a red-capable feedback loop (a failing test, a curl, a query) before anything else, then reproduce and minimise. Uses `awsq`/`dbq` read-only, logs and tests; starts from the analysis map (`references/analysis-map.md`) when an analysis exists. Writes `issues/<KEY>/investigation.md` (not a Task): the reproduction (command, output), observed facts with evidence, what was tried, open questions only people can answer. The verdict is `/devflow:diagnose`'s job; `plan-issue` reads both. When the user answers "I don't know" in planning, `plan-issue` offers to pause for analysis or investigation. Also usable without an Issue.

Split of the trio: `analyze` (the code, neutral), `investigate-issue` (the facts), `diagnose` (the verdict, crossing the problem with both).

## to-spec, to-tickets and triage (new work on the tracker)

Based on Matt Pocock's skills of the same name, with Jira (from `tracker.md`) in place of his tracker setup. To explore:

- **to-spec**: turn a conversation that already happened (no new interview) into a spec (problem, solution, user stories, implementation decisions without file paths, testing decisions, out of scope) and create it in the tracker as an epic or story.
- **to-tickets**: split a spec or plan into vertical-slice tickets (each crosses every layer, is demoable alone, fits one session), with "is blocked by" links; show the breakdown and iterate on granularity and blockers before creating anything. Tickets are the team's (tracker); Tasks stay internal to an Issue. Flow for new work: conversation → to-spec → to-tickets → each ticket goes through pick-issue → plan-issue.
- **triage**: a state machine for incoming Issues (category bug/enhancement; needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix): check whether it is already built or was rejected before, reproduce the bug, grill if needed, and end with an agent brief, a "we need this from you" comment, or a close with the reason. Useful when the user triages the team's bugs.

Open questions: does the user create epics and stories in Jira, or does that go through the PO (then generate text to paste instead of publishing)? Does the user triage bugs? Mapping of states to Jira statuses or labels, and of "blocked by" to the Jira link type.

## Visual views

The user reads better with visuals: the flow, an Issue's state and explanations should have a visual form, not only text. Best format still open. Options to explore:

- **Mermaid in the Vault**: Obsidian renders it natively. Skills could add a small diagram to what they write (the Task graph with `depends_on` in the Planning, the flow in `investigation.md`, the journey in the kb, which already has `.kb/diagrams.md`).
- **Obsidian Canvas / Bases**: a board of the Issue workspace (Tasks as cards by status) or a table view over the OKF frontmatter, with no code.
- **HTML page**: like `prototypes/workflow.prototype.html` (a clickable simulation of the flow), or a generated page per Issue (Jira status, Tasks, commits, PRs), opened locally or published as a private claude.ai Artifact.
- **FigJam diagrams** through the Figma connector, for architecture or flows to share with the team.

Testing now: `/devflow:draw` (experimental Area) analyses a function, file or system flow, recommends a format with reasons (the user picks) and draws it; formats in `references/draw-formats.md` (Mermaid available; draw.io, Canvas, HTML, FigJam planned); `retro` points to it when understanding cost a lot of reading. `/devflow:analyze` (experimental) maps the same targets and applies improvement lenses (`references/analysis-lenses.md`: complexity, partial failures and error handling available; architecture, testability, performance, observability, security and team conventions planned); `draw` reuses its map. `investigate-issue` should reuse the map too (`references/analysis-map.md`).

Skills that could use it: `ask` (show the flow and where the user is), `pick-issue` and `plan-issue` (Issue and Task graph), `investigate-issue` (how the system works today, call flow), `retro` (the session timeline), `open-pr` (the Summary already prefers a visual), kb skills (journeys). Related existing skills: Matt Pocock's `prototype`, and the `artifact-design`, `artifact-diagramming` and `dataviz` skills.

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
- Pausing: when the session ends in the middle of a Task, write a "Where I stopped" section in the Task file (what is done, what was tried and failed and why, what is left), so a fresh session resumes from it. This replaces a separate handoff skill (Matt Pocock's `handoff`): the Issue workspace already carries everything else between sessions.

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
