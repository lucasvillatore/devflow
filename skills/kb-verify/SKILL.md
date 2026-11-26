---
name: kb-verify
description: Run the mechanical checks of the knowledge base - valid YAML frontmatter, fields and types, template sections, broken links, anchor links, forbidden phrases and terms. Use when asked to verify or validate the base, or after editing documents.
argument-hint: "[file or folder] [--base <path>]"
---

# Verify the base

1. Find the base (see `references/kb-process.md` at the root of this plugin, two levels above this skill's directory).
2. Run the plugin's `scripts/kb_verify.py`:

   `python3 <plugin>/scripts/kb_verify.py --base "<base>" [--path "<file or folder, relative to the base>"]`

3. Show the result to the user: errors first, then warnings.
4. Fix nothing unless asked. If the user asks, fix and run again until there are no errors.

Errors break the base (invalid YAML, broken link, missing required section). Warnings are suspicions (system term, forbidden phrase) and may be false positives.
