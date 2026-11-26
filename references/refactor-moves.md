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

## Is it worth it?

Refactoring working code always carries risk, so "nothing to refactor" is a valid result. Decide before writing any test.

**The user's reason is a premise.** When the user says why they want the refactoring ("every new shipping type touches 5 places", "this class keeps breaking", "I cannot test this"), verify it in the code before anything else: count the places that change together, look at the bug and change history of the area (`git log`), try to isolate the code in a test. The result is one of:
- **confirmed**: refactor aimed at that reason, and measure the gain by it ("5 places → 1"), not only by complexity;
- **partly confirmed**: show the real size of the problem; the user decides;
- **not confirmed**: say so with the evidence ("only 1 place changes; the other 4 already call the same function") and stop.
A reason that cannot be measured ("the team does it differently") rests on a Vault convention when one exists; otherwise it is an opinion. Say which, and let the user decide.

**Without a reason from the user**, the code has to justify it:
- **numbers**: CCN and size above the limit. Default limit: CCN 10 per function; a repository profile may set its own (`Complexity limit`);
- **problems**: each row of the table above checked, present or absent, with evidence;
- **context**: how often the code changes; stable code nobody touches pays off little.

When nothing justifies it, the answer is **"it is ok"**: the numbers, the problems checked and why none applies, and at most small optional touches (a name outside the domain) marked optional and not done. Only propose changes with a gain that can be shown (lower complexity, duplication removed, a responsibility split out, the user's confirmed reason addressed); "it would look nicer" is at most **speculative**.
