# Layers: plugin, Vault, machine (Personal layer later)

devflow is generic and public-safe; everything specific to a company (AWS accounts, pipeline names, repository profiles, code conventions) lives in a **Vault** whose path is configured in the setup. The setup reads the Vault and wires the machine. We chose this over a single repo with everything because the plugin must be usable by anyone and outside one company. Credentials never go into either: they stay in the machine's secret store (`pass`).

A third layer, the **Personal layer** (the user's own repo with preferences, personal hooks and devflow choices), is planned but deferred (see `docs/backlog.md`). Until it exists, the devflow config lives in `~/.config/devflow/config.json` and guardrails are written straight into the user's global `~/.claude` (a repository scope is in the backlog).
