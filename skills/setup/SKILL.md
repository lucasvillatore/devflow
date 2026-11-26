---
name: setup
description: See and change devflow's setup on this machine with selectable options - template language, Vault location and skeleton, active Areas, auto memory off, the devflow block in the global CLAUDE.md, and the external tools. Run after installing or updating the plugin, to see the current setup, or to change the Vault or the active Areas.
disable-model-invocation: true
---

# Set up devflow

The script `scripts/setup.py` at the root of this plugin (two levels above this skill's directory) does all the writing. You talk to the user; the script writes. Speak the user's language.

## Steps

Use the question tool with selectable options (AskUserQuestion) for every choice that has options; free text only where no option can exist (a folder path, through the tool's "Other" answer). Recommended options come first, marked "(Recommended)".

1. **Show the current setup.** Run `python3 <plugin>/scripts/setup.py status` and show a short table: language, Vault path (exists? has a `.kb/`?), Areas on and off (required ones marked), auto memory, whether the machine is up to date (`up_to_date`), PyYAML, and the external tools (`tools`). With no config yet, say devflow is not set up and go to step 3 with every question.

2. **What to change.** One multi-select question: language, Vault, Areas, or nothing (only looking). "Nothing" ends here; if `up_to_date` is false, offer to just re-apply the current config instead.

3. **Ask only what was picked**, each as options, with the current value marked "(current)":
   - **Language**: one option per entry of `languages`. It sets the language of the Vault templates and of every artifact devflow generates.
   - **Vault**: "keep `<current path>`" (Recommended), plus the "Other" answer for a new path. For a new path, say whether it exists and whether it has a `.kb/`.
   - **Areas**: multi-select with one option per Area (at most four per question: split into two questions when needed), each with its skills in the description and the current state; required Areas are not offered (always on). A turned-off Area's skills are not used by Claude on its own; the user can still type them.
   Values not asked keep their current value.

4. **Preview.** Run `apply --language <l> --vault "<path>" --areas <a,b,...> --dry-run` and show briefly what will change: config, Vault files to create, settings diff, CLAUDE.md diff, warnings.

5. **Confirm** with options: "Apply" / "Cancel". Only on "Apply", run it again without `--dry-run`.

6. Report what was written, where the backups are, and what is left for the user:
   - restart the session (or `/reload-plugins`) so the CLAUDE.md block and settings take effect;
   - `pip install pyyaml` if the script warned about it;
   - a missing external tool: the install command from `python3 <plugin>/scripts/tools.py check` (devflow tools can be installed with the user's ok);
   - put the Vault under git if they want it versioned (the setup never runs `git init`).

## Rules

- Never write the config, the Vault, `settings.json` or `CLAUDE.md` by hand: always through the script, so runs stay idempotent.
- The script only adds missing Vault files; it never overwrites existing ones. If the user wants a template file refreshed, they delete it first.
- Running setup again after a plugin update refreshes the CLAUDE.md block.
