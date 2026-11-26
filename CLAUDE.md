# Working on devflow

This repository is the devflow plugin itself. Changes here change how every session works on the user's machines, so they go through the same discipline as any other work.

## Before proposing anything

1. Run `python3 scripts/catalog.py`: what exists, per Area, and what is planned.
2. Read `docs/backlog.md`: the idea may already be designed there, with decisions taken.
3. Read `CONTEXT.md` (the vocabulary) and `docs/adr/` (decisions not to re-litigate).

Then classify the request: it **exists** (point to it), it **extends** something (which skill, reference or script changes), it is a **new Component** (which Area; new ones start in `experimental`), or it is **in the backlog** (start from that design).

## Designing a change

- Interview in rounds following `references/grilling.md`: the whole frontier of open decisions per round, numbered, each with a recommendation; the decisions are the user's. Look up cheap facts yourself (this repository, the user's Vault); do not send agents to explore unless the user asks.
- Offer two or three ways when there is a real choice, each checked against the principles below.
- Keep `CONTEXT.md` a glossary only: when a term is settled, add or fix it right away; when the user uses a term in two senses, point it out. No implementation details there.
- Write an ADR in `docs/adr/` (next number, a title and one paragraph) only when the decision is hard to reverse, would surprise a future reader, **and** came from a real trade-off.
- When the design is settled and the user confirms, build it; anything deferred goes to `docs/backlog.md` with the decisions already taken.

## Principles

- **Components never call each other.** They exchange files in the workspace `<vault>/issues/<id>/` (`references/workspace.md`). A Component must work on its own and degrade gracefully when the files it reads are missing.
- **Deterministic work goes in scripts** (`scripts/`, standard library only, with a test), not in skill prose. Skills talk to the user and decide; scripts write config, measure, compare, render.
- **Company data lives in the Vault**, never in the plugin: tracker site, AWS profiles, repository profiles, conventions, PR format. The plugin ships generic templates in `templates/vault/<lang>/`.
- **Everything in the plugin is in English.** Artifacts written for the user follow the configured language (`~/.config/devflow/config.json`).
- **Shared procedures go in `references/`**, read only when needed; skill descriptions cost context in every session, so prefer one skill with a reference over several near-identical skills.
- **External or irreversible actions** (push, PR, tracker, databases, cloud) are shown and confirmed before they run. Read-only by default.
- **New Components start in the `experimental` Area** and move to their real Area once the user has validated them.

## Where things go

| What | Where |
| :-- | :-- |
| A skill | `skills/<name>/SKILL.md` (frontmatter `name`, `description` with when to use it, optional `argument-hint`, `disable-model-invocation: true` for user-only skills); register it in `components.json` under its Area |
| Plugin files from a skill | referred to as "at the root of this plugin (two levels above this skill's directory)" |
| A shared procedure or catalog | `references/` |
| A script | `scripts/<name>.py` plus `scripts/test_<name>.py` |
| A command on the user's PATH | `bin/` |
| An external tool | an entry in `tools.json` (`devflow`, `user` or `project` kind); never install a project tool |
| Vault files | `templates/vault/pt-BR/` **and** `templates/vault/en/`; `setup.py check` flags machines missing them, `setup.py apply` adds them |
| Workspace file templates | `templates/issue/<lang>/` |
| Third-party material | adapt, do not copy whole; credit it in `THIRD_PARTY_NOTICES.md` |

`plugin.json` has no `version` on purpose: every commit is a new version for the users.

## Before committing

Run every test:

```bash
python3 scripts/test_setup.py && python3 scripts/test_kb_verify.py && python3 scripts/test_guardrail.py && python3 scripts/test_refactor_tools.py && python3 scripts/test_bin.py
```

Check that `python3 scripts/catalog.py` lists the change in the right Area. When a change affects the user's machine (the CLAUDE.md block from `references/flow.md`, settings, new Vault files), say so: the user runs `/devflow:setup` or the setup script applies it. Commit and push only when the user asks.
