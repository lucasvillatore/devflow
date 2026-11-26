# Analysis lenses

What `/devflow:analyze` can look for once the map exists. To add a lens, add an entry; mark it **planned** until it is ready to use. Each finding has: severity (high, medium, low), evidence (`file:line`), why it matters, the suggestion, and the effort (small, medium, large).

## Complexity and readability (available)

Long functions, deep nesting, high cyclomatic or cognitive complexity (count the branches of the worst functions), mixed levels of abstraction in one function, names outside the domain, duplication, dead code, magic numbers.
- **Worth it when**: a function or file is hard to follow, or will be changed soon.

## Consistency and partial failures (available)

A sequence of writes that can stop halfway: write to API X, then API Y; Y fails and X stays written. Missing transaction, compensation or outbox; retries without idempotency; event ordering; race conditions; a cursor or checkpoint that advances before the write is confirmed; jobs that cannot resume where they stopped.
- **Worth it when**: the flow writes to more than one place (APIs, databases, queues, files) or runs in a job.

## Error handling (available)

Swallowed errors, generic catch blocks, a list of ignored errors written as "what fails" instead of "what can be skipped" (an unexpected error, like a 401, should stop the run), missing timeouts, errors that lose their cause, retries on errors that will never succeed.
- **Worth it when**: the flow calls external services or processes items in batches.

## Architecture (planned)

Shallow vs deep modules, coupling, infrastructure that knows the use case, dependency direction, business rules in the wrong layer.

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
