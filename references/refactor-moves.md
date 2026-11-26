# Refactor moves

Problem → move. `/devflow:refactor` picks moves from here and names them in the proposal. To add one, add an entry. Each move must keep the contract (`references/refactor-contracts.md`).

| Problem | Signal | Move |
| :-- | :-- | :-- |
| Too many paths in one function | high CCN, deep nesting | guard clauses (return early); extract each branch body into a function; a lookup table or polymorphism for a long conditional on a type or code |
| Mixed levels of abstraction | a function that orchestrates and also computes or formats | split into the orchestrator and the steps it calls |
| Duplication | the same block in several places | extract the common block; parameterize what differs |
| Large class | many responsibilities, many dependencies injected | split by responsibility; the original becomes a facade |
| Long parameter list | many parameters, often passed together | group them into an object (parameter object) |
| Names outside the domain | names that do not match the Vault glossary | rename (inside: free; in the contract: expand-contract) |
| Dead code | never called, flags always on or off | remove, proving with a search for callers and the tests |
| Shallow modules | many small modules a concept bounces between; interface as complex as the implementation | merge into a deeper module behind a smaller interface (Architecture lens) |
| Temporal coupling | calls that must happen in a hidden order | make the order explicit in one function, or one call that does both |
| Primitive obsession | strings or numbers carrying rules (codes, money, ids) | a small type that holds the value and its rules |
