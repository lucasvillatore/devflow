# devflow

The vocabulary of the devflow plugin. Domain terms of a company or product live in the **Vault**, not here.

## Language

**Issue**:
A unit of work in the issue tracker (e.g. a Jira item such as `CAT-5927`). It is what gets picked, planned and delivered.
_Avoid_: ticket, card, task

**Task**:
An internal unit of work produced by planning an Issue: one file in the Issue workspace, one deliverable, one commit. It has a local status (`todo`, `doing`, `blocked`, `done`, extensible in the Vault) and may depend on other Tasks.
_Avoid_: subtask, step

**Issue workspace**:
The folder `<vault>/issues/<ISSUE-KEY>/`, ignored by the Vault's git, where every artifact of an Issue lives: `index.md` (the Issue), `log.md` (dated changes to the Issue's state: pick, plan, pull request) and one file per Task. All of them use OKF frontmatter, so agents and Obsidian can query status and dependencies like a local tracker.
_Avoid_: scratch folder, work dir

**Planning**:
The first Task of an Issue workspace (`1-planning.md`, named in the Vault's language): the decisions of the interview, what is left to record in the Vault, and a checklist linking every Task.
_Avoid_: plan file, spec

**Analysis**, **Investigation**, **Diagnosis**:
Three files of an Issue workspace about a problem, each from its own Component: the Analysis reads the code and is neutral about the problem; the Investigation gathers facts by running things (reproduction, logs, data); the Diagnosis judges, crossing the problem with both, into a root cause (confirmed or probable) and a recommendation.
_Avoid_: report, study

**Contract**:
A file in the Issue workspace that one Component writes and another reads (e.g. the Issue's `index.md`, `N-<task>.md`). Components depend on Contracts, never on each other.
_Avoid_: handoff, interface

**Component**:
Any self-contained part of devflow (a skill, an agent, a script) that can be turned on or off in the setup.
_Avoid_: box, module, feature

**Area**:
A group of Components that serve one phase or concern: base, issue, planning, development, delivery, investigate, knowledge. The **experimental** Area holds Components the user is still testing; they move to their real Area once validated.
_Avoid_: phase (a phase is one kind of Area), category

**Vault**:
The knowledge base of a company or team, in a configurable folder: glossary, conventions, repository profiles, investigate data. Never holds credentials.
_Avoid_: KB folder, docs

**Personal layer**:
The user's own git repo (e.g. `ai-setup`) with preferences (`AGENTS.md`), personal hooks and devflow choices. Travels between the user's machines. Deferred: see `docs/backlog.md`.
_Avoid_: dotfiles, profile

**Guardrail**:
A rule that steers the agent, created from feedback: a hook when the rule is mechanical, a rule file (`~/.claude/rules/`) when it needs judgement, a Vault convention when it belongs to the team.
_Avoid_: lint rule, policy

**Tracker status**:
The status of an Issue in the issue tracker, mirrored in the Issue's `index.md`. Discovered from the tracker's transitions; the known list only grows.
_Avoid_: Task status

## Relationships

- An **Issue** is planned into one or more **Tasks**; all of them live in its **Issue workspace**.
- **Components** talk only through **Contracts**.
- The setup reads the devflow config and the **Vault** and wires the machine; it never writes into devflow itself.
- A **Guardrail** is saved in `~/.claude` (global), never in devflow; a repository scope may come later. Once the **Personal layer** exists, global Guardrails move there.
- The **Issue workspace** lives inside the **Vault** but is not part of its knowledge.

## Flagged ambiguities

- "task" was used both for the Jira item and for the internal files: resolved as **Issue** and **Task**.
- "box" (caixinha) was used for any part of the plugin: resolved as **Component**; groups of Components are **Areas**.
