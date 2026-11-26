# Analysis lenses

What `/devflow:analyze` can look for once the map exists. To add a lens, add an entry; mark it **planned** until it is ready to use. Each finding has: severity (high, medium, low), evidence (`file:line`), why it matters, the suggestion, the effort (small, medium, large) and the recommendation strength (**strong**: the evidence is clear and the gain is worth the cost; **worth exploring**: likely worth it, needs a closer look; **speculative**: a hunch, cheap to drop).

## Complexity and readability (available)

Long functions, deep nesting, high cyclomatic or cognitive complexity (count the branches of the worst functions), mixed levels of abstraction in one function, names outside the domain, duplication, dead code, magic numbers.
- **Worth it when**: a function or file is hard to follow, or will be changed soon.

## Consistency and partial failures (available)

A sequence of writes that can stop halfway: write to API X, then API Y; Y fails and X stays written. Missing transaction, compensation or outbox; retries without idempotency; event ordering; race conditions; a cursor or checkpoint that advances before the write is confirmed; jobs that cannot resume where they stopped.
- **Worth it when**: the flow writes to more than one place (APIs, databases, queues, files) or runs in a job.

## Error handling (available)

Swallowed errors, generic catch blocks, a list of ignored errors written as "what fails" instead of "what can be skipped" (an unexpected error, like a 401, should stop the run), missing timeouts, errors that lose their cause, retries on errors that will never succeed.
- **Worth it when**: the flow calls external services or processes items in batches.

## Architecture (available)

Adapted from Matt Pocock's `improve-codebase-architecture` and `codebase-design` (MIT, see `THIRD_PARTY_NOTICES.md`). Use their vocabulary exactly: **module** (anything with an interface and an implementation), **interface** (everything a caller must know to use it), **depth** (a lot of behavior behind a small interface), **seam** (where behavior can change without editing in place), **adapter**, **leverage** (what callers get from depth), **locality** (what maintainers get: change and bugs concentrated in one place).

- Look for: understanding one concept means bouncing between many small modules; **shallow** modules whose interface is nearly as complex as the implementation; pure functions extracted for testability while the bugs hide in how they are called (no locality); coupled modules leaking across seams; infrastructure that knows the use case; business rules in the wrong layer; parts untested or hard to test through their interface.
- **Deletion test** for anything that looks shallow: would deleting it concentrate complexity (a real signal) or just move it?
- Weight the **hot spots**: files that change often (`git log --oneline -- <path>`); deepening pays off where future changes land.
- Do not re-suggest what an ADR in the repository settles, unless the friction is real enough to reopen it (say so).
- **Worth it when**: a module is hard to change or test, or the same area keeps showing up in commits and bugs.

## Testability (planned)

Branches without tests, code hard to isolate, where a test seam fits.

## Performance and cost (planned)

N+1 queries, network calls inside loops, unbounded queries, missing indexes, large payloads.

## Observability (planned)

Whether a partial failure can be located: logs at failure points, correlation ids, metrics.

## Security (planned)

Input validation, secrets in logs, authorization.

## Team conventions (planned)

The Vault conventions and the user's guardrails applied to the analysed code.
