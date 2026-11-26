# Template: Business rule

## What it is

A business policy and its practical consequence. It covers a single subject.

## Where it lives

Standalone at the root of the context it constrains: `Business contexts/<Context>/<Rule name>.md`. Never inside a journey. Listed in the "Rules" section of the context's `index.md`.

## Name

States the policy, not the case or the technical moment. Good: "Minimum delivery time". Bad: "Zero time on update".

## Sections

- `# Rule`: one to three sentences, or a short list. Policy first, effect after. May have `##` for a subgroup (e.g. `## Trigger`) and `## To be confirmed` for undecided behavior.
- `# Example`: one sentence that explains how to read the diagrams and one `##` per scenario, each with one sentence and one diagram. See `diagrams.md`.

## Does not contain

- Links to journeys. To see where the rule applies, look at the backlinks.
- Citations, "Where it applies", tables.

## Good example

```markdown
---
type: Business rule
title: One review per order
description: Defines how many reviews the same order can have in progress.
tags: [order]
status: active
timestamp: 2026-01-15
---

# Rule

Each order is reviewed individually and has at most one review in progress. A new review request for an order still under review is refused.

# Example

## Request during a review

Order 123 is waiting for the credit review result. A new review request for order 123 arrives. The new request is refused.

(mermaid diagram)
```
