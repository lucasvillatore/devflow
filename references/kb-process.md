# Knowledge base process

Shared reference for every `kb-*` skill and agent of devflow. Read it before any action.

## Three layers

1. **Framework (devflow):** the process, the roles and the checks. It knows nothing about a specific business.
2. **Base configuration (`<base>/.kb/`):** types, templates, names, style, diagram colors and review checklist. **Every format decision comes from here.** Never use a format that is not in the configuration.
3. **Content (`<base>/`):** journeys, business contexts, rules, terms.

Folder names, type names, section names and status values are whatever `.kb/base.yaml` says, in the base's own language (`language`). This file uses the English role names (journey, business context, business rule, process part, term, draft, active).

## Finding the base

- If the user passed `--base <path>`, use it.
- Otherwise read `vault` from `~/.config/devflow/config.json`. The base is that folder, and it must contain `.kb/base.yaml`.
- If neither works, stop and tell the user to run `/devflow:setup`.

## Configuration files

| File | Content |
| :--- | :--- |
| `.kb/base.yaml` | Folders, types, required sections per type, status values, names, the `to_be_confirmed` marker, forbidden phrases and terms, folders to skip |
| `.kb/templates/<Type>.md` | The template of each document type, with the rules of each section and a good example |
| `.kb/style.md` | How to write |
| `.kb/diagrams.md` | How to draw the mermaid diagrams and the colors per state |
| `.kb/review-checklist.md` | What the reviewer checks |

## Work folder

Each business context under construction has a work folder. Each phase delivers a file, so the process can resume in another session:

```
<base>/.kb/work/<Context>/
├── sources.md            repositories and branches used
├── findings/<repo>.md    researcher output, one per repository
├── outline.md            synthesizer output: proposed tree, divergences, pending decisions
└── decisions.md          the user's decisions, dated
```

Downloaded code stays outside the base, in the session's temporary directory.

## Gates

The process has mandatory stops. A stop only ends with an explicit answer from the user in the chat.

1. **Research** → **Outline** → **stop: the user decides and approves the outline**.
2. **Draft writing** → **Verification** → **Review** → **stop: the user reviews the documents**.
3. **Closing**: only documents the user approved move from the draft status to the active status.

## User corrections become configuration

When the user corrects format, naming, style, structure or a diagram:

1. Apply the correction to the document.
2. Record the convention in `.kb/`: in the type's template, `style.md`, `diagrams.md`, `review-checklist.md` or `base.yaml`. Use the most specific file.
3. Write the convention as a general rule, with the reason and a short example. Do not write the particular case.
4. If the correction contradicts an existing convention, replace the old one. Do not keep both.
5. Never record the convention only in the agent's memory. The configuration is what other users and the reviewer see.

**Business** decisions (what is a rule, what is a defect, what a term means) are not conventions. They go to the context's `decisions.md` and, on closing, to the context's `log.md`.

## Never

- Query a production database without an explicit request from the user.
- Present a code behavior as a business rule when nobody decided it. Use the base's `to_be_confirmed` marker from `base.yaml`.
- Move a document to the active status without the user's approval.
- Write the name of a system, service, queue, endpoint, table or class in the base.
