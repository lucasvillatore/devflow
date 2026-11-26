# devflow

This machine uses the devflow workflow. Vocabulary: an **Issue** is the tracker item (e.g. `ABC-123`); a **Task** is an internal unit of work planned from it (one file, one deliverable, one commit). Never mix the two.

Areas, in the usual order (each can be used on its own):

1. **issue**: pick the Issue and load its context.
2. **planning**: interview until no decision is open, then split into Tasks.
3. **development**: implement one Task at a time, validate, commit.
4. **delivery**: open the pull request.
5. **investigate**: read data, logs and infrastructure (read-only by default).
6. **knowledge**: the Vault's knowledge base (journeys, contexts, rules, glossary).

Every artifact of a piece of work lives in its **workspace**: `<vault>/issues/<ISSUE-KEY>/`, or `<vault>/issues/<name>/` for work without an Issue (the Vault path is in `~/.config/devflow/config.json`). Components exchange files there; they never depend on each other.

Company conventions (code standards, repository profiles) live in the Vault under `devflow/`, imported below when present.
