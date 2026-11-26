# devflow

The vocabulary of the devflow plugin. Domain terms of a company or product live in the **Vault**, not here.

## Language

**Issue**:
A unit of work in the issue tracker (e.g. a Jira item such as `CAT-5927`). It is what gets picked, planned and delivered.
_Avoid_: ticket, card, task

**Task**:
An internal unit of work produced by planning an Issue: one file in the Issue workspace, one deliverable, one commit.
_Avoid_: subtask, step

**Issue workspace**:
The folder `<vault>/issues/<ISSUE-KEY>/`, ignored by the Vault's git, where every artifact of an Issue lives. Each Task says which repository it changes.
_Avoid_: scratch folder, work dir

**Contract**:
A file in the Issue workspace that one Component writes and another reads (e.g. `0-issue.md`, `N-<task>.md`). Components depend on Contracts, never on each other.
_Avoid_: handoff, interface

**Component**:
Any self-contained part of devflow (a skill, an agent, a script) that can be turned on or off in the setup.
_Avoid_: box, module, feature

**Area**:
A group of Components that serve one phase or concern: base, issue, planning, development, delivery, investigate, knowledge.
_Avoid_: phase (a phase is one kind of Area), category

**Vault**:
The knowledge base of a company or team, in a configurable folder: glossary, conventions, repository profiles, investigate data. Never holds credentials.
_Avoid_: KB folder, docs

**Personal layer**:
The user's own git repo (e.g. `ai-setup`) with preferences (`AGENTS.md`), personal hooks and devflow choices. Travels between the user's machines. Deferred: see `docs/backlog.md`.
_Avoid_: dotfiles, profile

**Guardrail**:
A rule that steers the agent, created from feedback: a hook when the rule is mechanical, an instruction when it needs judgement, a Vault convention when it belongs to the team.
_Avoid_: lint rule, policy

## Relationships

- An **Issue** is planned into one or more **Tasks**; all of them live in its **Issue workspace**.
- **Components** talk only through **Contracts**.
- The setup reads the devflow config and the **Vault** and wires the machine; it never writes into devflow itself.
- A **Guardrail** is saved in `~/.claude` (global) or in a repository's `.claude/` (local), never in devflow. Once the **Personal layer** exists, global Guardrails move there.
- The **Issue workspace** lives inside the **Vault** but is not part of its knowledge.

## Flagged ambiguities

- "task" was used both for the Jira item and for the internal files: resolved as **Issue** and **Task**.
- "box" (caixinha) was used for any part of the plugin: resolved as **Component**; groups of Components are **Areas**.
