---
name: awsq
description: Query AWS accounts read-only through `awsq`, which picks the SSO profile for an environment and role from the Vault. Use to check pipelines and deploys, logs, ECS services, S3 buckets or SQS queues.
---

# AWS through awsq

`awsq <env> <role> <aws args>` runs the `aws` CLI with the SSO profile mapped in `<vault>/devflow/investigate/aws.json`. `awsq profiles` lists the mapped profiles and what each is for. The command is on the PATH while devflow is enabled.

Before the first command, run `awsq profiles` and read the repository profile `<vault>/devflow/projects/<repo>.md` for its resources (pipelines, log groups, services). If `aws.json` is missing, show the format in `<vault>/devflow/investigate/README.md` and ask the user for the profiles in their `~/.aws/config`.

## Expired session

When a command exits with code **75** and prints `SSO: session expired` (any other code is an error from the `aws` CLI itself: read its message, do not log in again):

1. Run `awsq login`. It starts the login in the background and prints the approval link and code.
2. Give the link to the user to approve in the browser.
3. Confirm with `awsq status` and run the original command again.

## Rules

- Read-only: `list-*`, `describe-*`, `get-*`, `logs filter-log-events` / `tail`, `s3 ls`. Before any write (deploy, `start-pipeline-execution`, `s3 cp/rm`, `sqs send/purge`, `update-*`), show the exact command and ask for explicit confirmation, above all in production.
- Limit the output (`--max-items`, `--query`, `| head`) and prefer counts to large listings.
- Use the profile whose `use_for` covers the service; in production, the narrowest one.
- A resource learned during the investigation (log group, pipeline) and missing from the repository profile: offer to add it there.
