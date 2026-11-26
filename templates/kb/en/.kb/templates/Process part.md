# Template: Process part

## What it is

One of the parts of a business process: a kind of review, a stage of a flow. It explains what the part does, what it requires and how its result affects the whole process.

## Where it lives

In a process parts folder inside the context, listed in `folders.process_parts` of `base.yaml`. Example: `Business contexts/Order approval/Review types/Credit review.md`. The frontmatter uses `type: Business rule`.

## Sections

- `# What it is`: what the part does, in one or two sentences, with the main idea in bold. May have a short example.
- `# Minimum fields`: list of the data the part needs, each in bold with one sentence.
- `# What it does`: numbered list of steps. May have `##` for a group.
- `# Result`: the possible states in Name/Description blocks. Non-terminal before terminal.
- `# Impact`: list. When the part fails the process, what it changes in the other parts.
- `# Example`: one sentence that explains how to read the diagrams and one `##` per scenario.

## Part split into sub-parts

When the part runs separately for each kind of item:

- `# What it is` applies to all.
- `# Common to all kinds` holds what applies to all, with the template sections as `##`.
- Each sub-part is a `#`, with the template sections as `##`. Repeat only the sections that change.

## Does not contain

- The rules of the whole process (order, dependencies, final result). They live in standalone rules at the context root.
- Repetition of another part. Link to it.
