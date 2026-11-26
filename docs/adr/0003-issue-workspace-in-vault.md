# Issue workspace lives in the Vault, git-ignored

Each Issue's workspace is `<vault>/issues/<ISSUE-KEY>/`, ignored by the Vault's git. We considered `<repo>/.scratch/<KEY>/` (the original workflow) and a separate folder outside everything. Inside the repo breaks for Issues that touch several repositories and is invisible to worktree agents; a separate folder is hard to find. Inside the Vault, the user browses Issues in Obsidian next to the knowledge they produce, agents in worktrees read it by absolute path, and ignoring it in git keeps drafts out of the shared knowledge.
