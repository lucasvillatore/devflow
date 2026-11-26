---
name: kb-context
description: Create or complete a business context in the knowledge base from the code of one or more repositories. Researches in parallel, builds an outline with pending decisions, stops for the user, then writes drafts, verifies and reviews. Use when asked to document a business subject, create a context, or extract the rules of a process from repositories.
argument-hint: "<Context> <owner/repo[@branch]> ... [--base <path>]"
---

# Document a business context

First read `references/kb-process.md` at the root of this plugin (two levels above this skill's directory). It defines the configuration, the work folder, the gates and where corrections go.

Arguments: the context name (a business name, quoted if it has spaces), one or more repositories `owner/repo[@branch]` and, optionally, `--base <path>`. Without repositories, ask which ones. Without a branch, use the repository's default branch.

## Phase 1: preparation

1. Find the base and check that `<base>/.kb/base.yaml` exists (see `kb-process.md`).
2. Create the work folder `<base>/.kb/work/<Context>/` with `findings/`.
3. If the folder already has `outline.md` or `decisions.md`, this context is in progress. Show which phase it stopped at and continue from there, without redoing the research unless the user asks.
4. Download each repository into the session's temporary directory, one empty directory per repository:
   `gh api repos/<owner>/<repo>/tarball/<branch> > <tmp>/<repo>.tgz && tar xzf <tmp>/<repo>.tgz -C <tmp>/<repo> --strip-components=1`
5. Write `sources.md` in the work folder: repository, branch, date and local path.

## Phase 2: research

Run one `kb-researcher` agent per repository, **all in the same message**, so they run in parallel. In each request:

- the context and one sentence about the subject;
- the code path and the output path `findings/<repo>.md`;
- one line about the role of the other repositories, so it can explain the link.

Wait for all of them. Do not research in parallel yourself.

## Phase 3: outline

1. Run the `kb-synthesizer` agent with the base path, the context and the work folder.
2. Read `outline.md` and show the user: the proposed tree, the divergences and the pending decisions, each with its suggestion.
3. **Stop.** Write no base document until the user answers the decisions and approves the outline. "Go ahead" approves every suggestion.
4. Write the answers to `decisions.md`, dated, one decision per item. If the user changes the tree, update `outline.md`.

## Phase 4: writing

1. Split the approved documents into groups of up to five, by type or by dependency (terms first, then process parts, then rules).
2. Run one `kb-writer` agent per group, in parallel, with the base path, the work folder and the list of documents.
3. Update the `index.md` files of the context, the glossary and the contexts folder yourself, in the format `* [Title](file.md) - description`. The context index starts with the introduction and a "where to start" section.

## Phase 5: verification and review

1. Run `python3 <plugin>/scripts/kb_verify.py --base "<base>" --path "<context folder>"` and fix every error.
2. Run the `kb-reviewer` agent on the context and fix what it points out. "Outside the checklist" items: show them to the user, do not apply them.
3. Run the verification again on the whole base.
4. Show the user the list of documents written, what is still "to be confirmed" and the "outside the checklist" items. **Stop.** The user reviews the documents.

## Afterwards

- Every format, naming or style correction from the user becomes a convention in `.kb/` (see `kb-process.md`).
- When the user approves, use the `kb-close` skill.
