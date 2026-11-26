# Template: Journey

## What it is

The path a **person** takes to a business goal, from start to end. A process the business runs on its own (e.g. order approval, invoicing) is not a journey: it is a context. The journey points to the context's index.

## Where it lives

`Journeys/<Journey name>.md`. The name is the business goal. `Journeys/index.md` groups journeys by who walks the path.

## Sections

- `# Goal`: one or two sentences. Who walks the path and what they want.
- `# Flow` (optional): only when the path really branches. See `diagrams.md`.
- `# Steps`: numbered list, in order. Each step has one sentence and at most one link, to a rule or a context index.
- `# Detours` (when they exist): one item per detour, with the link to the rule that applies.
- `# Open points` (when something is missing): every gap, one per item.

In draft, only `# Goal` is required.

## Does not contain

- The text of a rule or the content of a process. Only the link.
- System names.

## Good example

```markdown
---
type: Journey
title: In-store pickup purchase
description: The customer's path from choosing a product to picking it up at a physical store.
tags: [purchase, pickup]
status: draft
timestamp: 2026-01-15
---

# Goal

The customer buys on the website and wants to pick up the product at a physical store.

# Steps

1. The customer chooses the product and the pickup store.
2. The order goes through [Order approval](../Business%20contexts/Order%20approval/index.md).
3. The customer picks up the product at the store.

# Detours

- **Product out of stock at the store:** the order is transferred. [Store transfer time](../Business%20contexts/Stock/Store%20transfer%20time.md) applies.

# Open points

- How the customer learns the product arrived at the store.
```
