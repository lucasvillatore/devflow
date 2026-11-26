---
name: dbq
description: Query databases (MongoDB, MySQL, Redis) read-only through `dbq`, which reads the connection from the `pass` store and never prints it. Use whenever the user asks to look at, query, count or investigate data in a database.
---

# Databases through dbq

`dbq <project> <env> <name> [client args]` reads the URI at `<project>/<env>/db/<name>` in `pass` and opens the right client (`mongosh`, `mysql` or `redis-cli`). Extra arguments go to the client. The command is on the PATH while devflow is enabled.

Find the databases with `pass ls` (entry names only). Notes about environments and databases may be in `<vault>/devflow/investigate/README.md`.

## Queries (always non-interactive)

```bash
dbq shop stg main --eval 'db.orders.countDocuments({status: "paid"})'           # MongoDB
dbq shop stg main --eval 'JSON.stringify(db.orders.find({}, {status:1}).limit(5).toArray())'
dbq shop stg main -e 'SELECT id, status FROM orders ORDER BY id DESC LIMIT 5'   # MySQL
dbq shop stg cache --scan --pattern 'session:*' | head -20                      # Redis
```

## Rules

- **Never** run `pass show` nor print a URI or password. Use only `dbq`.
- **Read-only by default.** Before any write (`insert`, `update`, `delete`, `drop`, `UPDATE`, `DELETE`, `ALTER`, `TRUNCATE`, `SET`, `DEL`, `FLUSH*`...), show the exact command and ask for explicit confirmation, above all in production.
- Always limit results (`LIMIT`, `.limit()`, `| head`); prefer counts and aggregations to dumping collections.
- When the environment is unclear, use a test environment before production, or ask.
- If `dbq` hangs or fails asking for the GPG passphrase, ask the user to unlock the store in their terminal (e.g. typing `! pass show <entry> >/dev/null` at the prompt) and try again.
- `is not in the pass store`: run `pass ls` and check the name with the user.
