---
name: open-pr
description: Open a GitHub pull request in the team's format from the Vault - checks the branch, gathers commits, the Issue workspace and evidence, shows title and body for approval, pushes and creates the PR, then offers to move the Issue to code review. Use when the user asks to open, create or push a PR.
argument-hint: "[ISSUE-KEY]"
---

# Open a pull request

Push the current branch and open the PR with a title and body in the team's format. Every external action (push, PR, tracker) waits for the user's approval.

## Before starting

1. Read `~/.config/devflow/config.json` (`vault`). Without it, stop and tell the user to run `/devflow:setup`.
2. Read `<vault>/devflow/pull-request.md` (title, body, language, reference PR) and `<vault>/devflow/tracker.md` (site, code review status). If the PR format file is missing, tell the user to run `/devflow:setup`.
3. Read the repository profile `<vault>/devflow/projects/<repo>.md`, where `<repo>` is the name of the repository folder. Missing profile or missing field: ask the user for it and write it there.
4. The Issue key comes from the argument, the branch name or the commits (`[A-Z][A-Z0-9]+-\d+`).

## Steps

1. **Check the branch.** Done when it is not the default branch, nothing uncommitted belongs to the PR, and the profile's lint and tests passed on this branch (run them if there is no recent result in the conversation). Report failures and stop.

2. **Gather the material.** `git log <base>..HEAD`, `git diff --stat <base>...HEAD`, the Issue workspace `<vault>/issues/<KEY>/` when it exists (`index.md`, the Planning, `done` Tasks and their "Decisions" sections) and the evidence already produced in the conversation (test output, staging validation, commands run against data). Done when every commit of the branch is covered by some part of the body.

3. **Write title and body** following `pull-request.md`, in its language. The Issue link is `https://<site>/browse/<KEY>`. End the body with the attribution line Claude Code asks for, if any. Show both to the user and wait for approval: the PR is visible to the team.

4. **Publish.** Write the body to a file in the scratchpad, then `git push -u origin <branch>` and `gh pr create --base <default branch> --title "<title>" --body-file <file>`. Done when the command returns the PR URL.

5. **Record and move.**
   - Add a `log.md` entry on top in the Issue workspace, when it exists: `## YYYY-MM-DD` and `**PR**: <url>`.
   - Ask whether to move the Issue to the code review status from `tracker.md` (ask for the status and write it there if it is missing). On yes, list the transitions and use the one that leads there; never chain transitions on your own.

## Changing an open PR

`gh pr view --json body` → edit the body file → `gh pr edit --body-file <file>`, after showing the change.

## Answer

The PR URL, and the tracker status from → to (or that it was not moved).
