# Workspace

Where devflow skills exchange files: `<vault>/issues/<id>/` (Vault path in `~/.config/devflow/config.json`). The `<id>` is either:

- an **Issue key** from the tracker (`[A-Z][A-Z0-9]+-\d+`, e.g. `CAT-5924`): the workspace of that Issue;
- a **name** for work without an Issue: lowercase words with hyphens (e.g. `vendor-service-update`, `slow-job`). A name never looks like a key.

## Finding it

1. From the argument: a key, a browse link (take the key) or a name.
2. Otherwise from the conversation: a workspace already used in this session.
3. Otherwise ask once, suggesting a name from the subject ("I'll call it `vendor-service-update`, ok?"). Skills that work fine without saving (`draw`, `retro`) may skip this and only ask when the user wants to save.

## Creating it

When the folder does not exist, create it with `index.md` and `log.md` from `templates/issue/<language>/` at the root of the plugin. Without an Issue: `key:` and `link:` empty, `title` and `description` from the subject, `status:` empty; the Context section says what the work is about. Add a `log.md` entry: `**Start**: <one line>`.

## Without an Issue

Every skill works the same way; only what depends on the tracker is skipped: no assignee or status changes, no Issue link, no key in titles or branch names unless the user gives one.

When the work later becomes an Issue, `/devflow:pick-issue <KEY> <name>` adopts the workspace: renames the folder to the key, fills the tracker fields of `index.md` and keeps every other file.
