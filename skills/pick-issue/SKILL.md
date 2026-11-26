---
name: pick-issue
description: Pick up a tracker Issue (Jira key like ABC-123 or a browse link) - assign it to the user, move it to the in-development status, read description, comments and links, and write the Issue workspace (index.md and log.md) in the Vault. Use when the user wants to pick, take, assume or start an Issue.
argument-hint: "<ISSUE-KEY or link> [workspace name to adopt]"
---

# Pick an Issue

Assume an Issue for the user, gather its context and record it in the **Issue workspace** so other sessions and agents can work from it. Writes only to the tracker (assignee, status) and to the Vault. No code.

## Before starting

1. Read `~/.config/devflow/config.json` (`vault`, `language`). Without it, stop and tell the user to run `/devflow:setup`.
2. Extract the key with the pattern `[A-Z][A-Z0-9]+-\d+` from the argument (key or link, possibly with a query string). Without one, ask for the Issue before anything else.
3. Read `<vault>/devflow/tracker.md`: tool, site, the "in development" status and the known statuses. If the site is empty, take it from the link if the user gave one, otherwise ask; write it there. If the file is missing, tell the user to run `/devflow:setup`.

Templates are in `templates/issue/<language>/` at the root of this plugin (two levels above this skill's directory). Use the configured language for every heading and text you write.

## Steps

Use the Atlassian (Jira) connector. Each step ends at its criterion.

1. **Read the Issue.** Done when you have title, status and assignee. If it does not exist or there is no access, stop and say so.

2. **Assign it to the user.** Get the current user's accountId and set it as assignee.
   - Already the user: move on.
   - Someone else: say who and confirm with the user before changing it.
   Done when the user is the assignee.

3. **Move it to the in-development status** (from `tracker.md`). List the available transitions.
   - Append every status reachable or seen that is not yet under the known statuses in `tracker.md`. The list only grows; never remove or rename entries.
   - Already in that status: move on.
   - No transition leads there directly: show the current status and the available transitions and ask which way to go. Never chain transitions on your own.
   Done when the Issue is in the in-development status.

4. **Gather the context.** Read: full description and acceptance criteria; comments (decisions usually live there, especially the latest); parent or epic and subtasks; linked issues (title and status of each, content of blockers and blocked ones); Confluence pages and other links the connector can open. Done when each item was read or you know it does not exist.

5. **Find local paths.** From repository, service or file names mentioned in the Issue, look for folders that exist on this machine: siblings of the current repository, and the local path of the repositories in `<vault>/devflow/projects/` (the `Local path` line of each profile, in the Vault's language). When you find a repository's path and its profile lacks it, offer to add it. Keep only paths that exist. Ask the user which repositories or files the Issue touches when none are found or some seem missing; an empty list is fine.

6. **Write the Issue workspace** `<vault>/issues/<KEY>/`.
   - **Adopting a named workspace** (a second argument, or the user says the work started without an Issue, see `references/workspace.md`): rename `<vault>/issues/<name>/` to `<vault>/issues/<KEY>/`, fill the tracker fields of its `index.md` (`key`, `link`, `status`) and merge the Issue's context into its sections, keep every other file, and add a `log.md` entry `**Pick**: adopted from <name>`. Stop if both folders exist and ask.
   - **New workspace:** create `index.md` and `log.md` from the templates. Fill the frontmatter (`title`, one-sentence `description`, `key`, `link`, tracker `status`, `timestamp` today, `paths`) and the sections with what step 4 found, in the user's language, short and factual. Add a `log.md` entry.
   - **Existing workspace:** never touch any file other than `index.md` and `log.md`. Show the user what changed in the tracker since the last pick (status, description, new comments, links). Update the frontmatter, then ask:
     - **synthesize**: rewrite the sections as one coherent text with the new information, or
     - **append**: keep the sections and add a dated update section at the end.
     Add a `log.md` entry for the repick.
   - `log.md` entries go on top, newest first:

     ```
     ## YYYY-MM-DD

     **Pick** (or **Repick**): <what changed in the tracker and in the workspace, one or two lines>.
     ```

## Answer

In the user's language, short:

- **Issue**: key, title, link
- **Tracker**: what changed (assignee, status from → to) or what is pending and why
- **Workspace**: path of the `index.md`
- **Context**: the problem, what must be delivered and the acceptance criteria, in a few sentences
- **Points of attention**: dependencies, blockers, decisions in comments, ambiguities, missing information

End by saying you are ready for the next step, without proposing an implementation plan.
