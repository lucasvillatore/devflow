# devflow

A local development workflow for Claude Code, built to grow one Component at a time.

## Layers

| Layer | What | Where |
| :-- | :-- | :-- |
| Plugin | skills, agents, scripts, templates | this repo |
| Vault | company/team knowledge: glossary, conventions, repository profiles, investigate data | configured in the setup |
| Config | active Components, template language, Vault path | `~/.config/devflow/config.json` |
| Machine | `~/.claude` (CLAUDE.md block, settings) | written only by the setup; `bin/` reaches the PATH through the plugin |

Work happens in a workspace, `<vault>/issues/<ISSUE-KEY or name>/` (git-ignored), so it can be browsed in Obsidian.

See [CONTEXT.md](CONTEXT.md) for the vocabulary, [docs/adr](docs/adr) for the structural decisions and [docs/backlog.md](docs/backlog.md) for what is deferred.

## Areas and Components

The source of truth is [components.json](components.json): Areas, their skills, and which are required. To see what exists right now, with each skill's purpose and what is planned, run `/devflow:ask` or `python3 scripts/catalog.py`. New Components start in the `experimental` Area. Vault skeletons per language are in `templates/vault/`.

Working on devflow itself: see [CLAUDE.md](CLAUDE.md) (principles, where things go, the tests to run).

Requirements: `gh` authenticated and Python 3 with PyYAML (knowledge Area).

## Install

```
/plugin marketplace add lucasvillatore/devflow
/plugin install devflow@devflow
/devflow:setup
```

Then turn on auto-update: `/plugin` → Marketplaces → devflow → auto-update. Claude Code checks for new commits each session and shows "Plugin updated: devflow · Run /reload-plugins to apply". The repository is private, so git must be able to authenticate without prompting (`gh auth setup-git`).

When the plugin changes the setup's output, a session-start message asks you to run `/devflow:setup` again.

`/devflow:ask [question]` explains devflow and tells which skill fits.
