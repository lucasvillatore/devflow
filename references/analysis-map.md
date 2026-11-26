# Analysis map

How devflow skills (`analyze`, `draw`) map a piece of code or a system flow before doing anything with it. The map is about concepts, not lines.

1. **Scope.** Decide what is mapped:
   - **code**: a function or file; read all of it;
   - **system flow**: a path across systems (e.g. "from checkout to the ERP"); follow calls, queues, jobs and databases through the repositories in the Issue's `paths` or the ones the user names.
   If the scope is unclear, ask one question before reading.

2. **Blocks.** Group the code into blocks by responsibility (validate input, compute price, apply coupon, persist, notify), not by syntax. For each block:
   - a name in domain language (the Vault glossary term when one exists);
   - what it does, one line;
   - its `file:line` range;
   - **inferred** when you did not read it in full.

3. **Connections.** How the blocks link: order, real branches (and the condition), calls between systems (sync or async), states and transitions when there are explicit states. Mark inferred links too.

4. **Show it short**: one line per block, then the connections. No judgement yet.
