# Refactor contracts

What must stay the same at each level, and how `/devflow:refactor` and `/devflow:refactor-plan` prove it. State the contract to the user before changing anything.

## Function

- **Contract**: signature (name, parameters, return type), the returned values, the errors thrown, and the side effects (what it writes, calls, publishes or logs when the log is relied on).
- **Proof**: characterization tests (at least one per path, CCN as the floor) and recorded outputs compared with `scripts/equivalence.py`. Side effects are recorded as part of the output (the calls made to a spy or fake, in order).

## Class

- **Contract**: public methods and properties, constructor and injected dependencies, and the side effects of each public method. Private members are free to change.
- **Proof**: characterization tests through the public interface only, plus recorded outputs per public method. When a class is split, the original stays as a facade with the same public interface (its callers do not change), unless the user asks to migrate callers too, which is expand-contract (below).

## Project

- **Contract**: what the outside world sees: HTTP endpoints (paths, status codes, response bodies), messages consumed and published, database schema and data written, scheduled jobs, CLI commands.
- **Proof**: contract tests at the border: recorded real requests and their responses (or messages and their effects), replayed before and after, compared with `scripts/equivalence.py`. Each inner change is a function or class refactoring with its own proof.
- A project is never refactored in one run: `/devflow:refactor-plan` turns it into Tasks.

## Expand-contract

For a change whose blast radius crosses the contract (renaming a field used everywhere, changing a public signature): expand (add the new form next to the old, nothing breaks), migrate callers in batches (each batch a Task, tests green per batch), contract (remove the old form once nothing uses it, proved by search and tests).
