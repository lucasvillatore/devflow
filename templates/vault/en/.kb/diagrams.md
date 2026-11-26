# Diagrams

## Rules

- Use mermaid `flowchart LR`.
- Each box shows the name and the state or role in its own text: `rev[Review<br/>skipped]`.
- Before the scenarios, one sentence explains how to read the arrows. Example: "The arrow shows the order's path to the result."
- Each scenario is a `##` with one sentence and one diagram.
- A journey only has a diagram when the path really branches. A solid line is the normal path, a dashed line (`-.->`) is a detour.
- No diamonds for internal system decisions.

## Colors per state

Declare only the classes used in the diagram.

```
classDef ok fill:#d9f2e3,stroke:#1d7a46,color:#14301f
classDef bad fill:#fbe0dd,stroke:#b3261e,color:#3d1e1b
classDef wait fill:#fbeedf,stroke:#b4570e,color:#3a2817
classDef info fill:#e8eefb,stroke:#2456c9,color:#14213d
classDef skip fill:#eceef2,stroke:#5d6779,color:#1b2230,stroke-dasharray: 4 3
```

- `ok`: approved, done, happy end.
- `bad`: rejected, refused, error.
- `wait`: waiting or process running. Add `stroke-dasharray: 4 3` when it is pending.
- `info`: step, information, in progress.
- `skip`: ignored, not requested.
