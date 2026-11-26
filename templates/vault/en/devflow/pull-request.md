# Pull request format

Used by `open-pr`. Edit freely: the skill follows this file.

- Language: English
- Reference: <link to a good team PR, optional>

## Title

`<type>(<KEY>): <what changes, lowercase>`, with a conventional commit type (`feat`, `fix`, `refactor`, `test`, `chore`). E.g. `feat(ABC-123): free shipping by region at checkout`.

## Body

```markdown
[<KEY>](<Issue link>): <1 to 3 sentences: the problem and what this PR changes, in domain language>

## Summary

<smallest visual that makes the point, with the short text it supports>

## <extra sections, only when there are any>

## Evidence

- **Before:** <output/test/behavior before>
  **After:** <output/test/behavior after>

<test output and other evidence>

## Merge Danger

**Door:** <one-way or two-way>

<how to roll back, if two-way>

**Blast Radius:** <one word>

- <consequence of the merge, one bullet each>
```

### Summary

Pick the **smallest view** that shows the change; one or two are enough:

- file tree in `diff` (`+`/`-`) for new or changed structure, with a short note per file;
- pseudocode or call tree, in `diff` when the flow already existed;
- a `text` block with the shape of new documents or tables;
- a table when there are cases to compare.

### Extra sections

Include when the branch has them: **manual load/configuration** (what was written, where, whether it is already in staging, scripts outside the repo), **staging tests** (table `ID | Scenario | Expected | Before | After | ✅`). Leave the section out otherwise.

### Evidence

Prefer executed evidence: a test that failed and now passes, command output, a staging table. List new tests by the behavior they cover.

### Merge Danger

- **Door:** two-way when it can be reverted without loss (revert, flag, config); one-way when there is a destructive or hard-to-undo action (deleted data, irreversible migration).
- **Blast Radius:** the affected area in one word. In the bullets: mandatory steps before deploy, behavior changes for consumers, effects in production.
