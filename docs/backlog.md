# Backlog

Items deferred on purpose. When the Vault exists, this list moves there.

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

## Review stage (development)

A reviewer agent that reads only the diff and enforces judgement-call conventions from the Vault, so the implementing agent does not carry them in context.

## retro

User-invoked retrospective of a session (based on Matt Pocock's `retro`): lists improvement candidates by severity, then offers to turn each into a guardrail through `add-guardrail`.

It also looks for **missing knowledge**: facts the session had to discover (a business rule, a term, a repository's quirk, how to reach some data) that are not in the Vault yet, and suggests where each one goes (glossary term, business rule, repository profile, convention).

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
