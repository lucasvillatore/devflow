# Repository profiles

One file per repository (`<repo>.md`, named after the repository folder). devflow skills read and complete these files; when a field is missing, they ask and write it.

```markdown
# <repo>

- Default branch: main
- Tests of changed files: <command, with {files}>
- Lint of changed files: <command, with {files}>
- Build: <command>
- Full suite: <command>
```

Add whatever else is specific to the repository (staging pipeline, resources, caveats). The `## Rejected improvements` section keeps improvements the user rejected with a reason; `analyze` does not suggest them again.
