# Draw formats

The formats `/devflow:draw` can suggest. To add one, add an entry; mark it **planned** until the skill can produce it.

## Mermaid flowchart (available)

Text inside the `.md`; Obsidian and GitHub render it.
- **Best for**: the control flow of a function or file, grouped into blocks by responsibility; a business path with real branches.
- **Not for**: many systems talking over time (use a sequence diagram); something whose essence is its states (use a state diagram); more than about 12 nodes in one picture.

## Mermaid sequence diagram (available)

- **Best for**: interaction between systems over time: requests, queues, jobs, databases, who calls whom and in what order.
- **Not for**: the internal logic of one function; flows without a clear time order.

## Mermaid state diagram (available)

- **Best for**: something with explicit states and transitions (an order's status, a job's lifecycle, an Issue's workflow).
- **Not for**: step-by-step logic or calls between systems.

## draw.io (planned)

A `.drawio` file (XML) edited visually in diagrams.net; Obsidian opens it with a plugin.
- **Best for**: diagrams the user wants to adjust by hand or show to the team with a free layout (architecture, many systems).
- **Not for**: diagrams that must stay in sync with text and be regenerated often.

## Obsidian Canvas (planned)

A `.canvas` file of cards and arrows in the Vault.
- **Best for**: a board of notes that link to the real files (an Issue's Tasks, a context's documents).
- **Not for**: precise control flow.

## HTML page (planned)

A local page or a private claude.ai Artifact, like the workflow prototype.
- **Best for**: interactive views: clicking through steps, filtering, simulating a flow.
- **Not for**: something that should live in the Vault as plain text.

## FigJam (planned)

A diagram in Figma through its connector.
- **Best for**: sharing and discussing with the team in a meeting.
- **Not for**: personal notes that live in the Vault.
