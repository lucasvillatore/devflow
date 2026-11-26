# devflow

A local development workflow for Claude Code, built to grow one Component at a time.

## Layers

| Layer | What | Where |
| :-- | :-- | :-- |
| Plugin | skills, agents, scripts, templates | this repo |
| Vault | company/team knowledge: glossary, conventions, repository profiles, investigate data | configured in the setup |
| Config | active Components, template language, Vault path | `~/.config/devflow/config.json` |
| Machine | `~/.claude`, `~/.aws`, `~/.local/bin` | written only by the setup |

Issues are worked in `<vault>/issues/<ISSUE-KEY>/` (git-ignored), so they can be browsed in Obsidian.

See [CONTEXT.md](CONTEXT.md) for the vocabulary, [docs/adr](docs/adr) for the structural decisions and [docs/backlog.md](docs/backlog.md) for what is deferred.

## Areas (v0)

| Area | Components |
| :-- | :-- |
| base | `setup`, `add-guardrail` |
| issue | `pick-issue` |
| planning | `plan-issue` |
| development | `dev-task` |
| delivery | `open-pr` |
| investigate | `awsq`, `dbq` |
| knowledge | `kb-context`, `kb-journey`, `kb-review`, `kb-verify`, `kb-close` (required) |

Status: knowledge Area migrated; the other Components are added one by one.

Requirements: `gh` authenticated and Python 3 with PyYAML (knowledge Area).

## Install

```
/plugin marketplace add <path-or-git-url-of-this-repo>
/plugin install devflow@devflow
/devflow:setup
```
