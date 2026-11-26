---
name: setup
description: Set up or update devflow on this machine - template language, Vault location and skeleton, active Areas, auto memory off, and the devflow block in the global CLAUDE.md. Run after installing or updating the plugin, or to change the Vault or the active Areas.
disable-model-invocation: true
---

# Set up devflow

The script `scripts/setup.py` at the root of this plugin (two levels above this skill's directory) does all the writing. You talk to the user; the script writes. Speak the user's language.

## Steps

1. Run `python3 <plugin>/scripts/setup.py status` and read the result. If a config already exists, its values are the defaults for every question below.

2. Ask, in one round, with a recommendation for each:
   - **Template language**: one of `languages` from the status. It sets the language of the Vault templates and of every artifact devflow generates.
   - **Vault path**: where the knowledge base lives. It may be an existing folder, a folder inside another git repo, or a new one. Say whether it exists and whether it already has a `.kb/`.
   - **Areas**: which Areas to turn on. Required Areas are always on. A turned-off Area's skills are not used by Claude on its own; the user can still type them.

3. Run the same script with `apply --language <l> --vault "<path>" --areas <a,b,...> --dry-run` and show the user, briefly, what will change: config, Vault files to create, settings diff, CLAUDE.md diff, warnings.

4. **Stop** and wait for explicit confirmation. Then run it again without `--dry-run`.

5. Report what was written, where the backups are, and what is left for the user:
   - restart the session (or `/reload-plugins`) so the CLAUDE.md block and settings take effect;
   - `pip install pyyaml` if the script warned about it;
   - put the Vault under git if they want it versioned (the setup never runs `git init`).

## Rules

- Never write the config, the Vault, `settings.json` or `CLAUDE.md` by hand: always through the script, so runs stay idempotent.
- The script only adds missing Vault files; it never overwrites existing ones. If the user wants a template file refreshed, they delete it first.
- Running setup again after a plugin update refreshes the CLAUDE.md block.
