# Investigate

Data used by the `awsq` and `dbq` skills. No credential lives here: AWS uses SSO, databases use the `pass` store.

## AWS (`aws.json`)

Map from `<env>/<role>` to a profile in `~/.aws/config`, plus the SSO session. The first profile is used to check whether the session is valid.

```json
{
  "sso_session": "my-company",
  "profiles": {
    "stg/developer": {"profile": "company-stg-developer", "use_for": "everything in staging: pipeline, logs, ECS, S3, SQS"},
    "prod/monitoring": {"profile": "company-prod-monitoring", "use_for": "CloudWatch Logs, metrics, alarms, ECS"}
  }
}
```

Resources of each repository (pipelines, log groups, services) go in its profile, `../projects/<repo>.md`.

## Databases (`pass`)

Entries at `<project>/<env>/db/<name>`, with the URI on the first line (`mongodb://`, `mysql://`, `redis://`). The company's test environments (e.g. `hml`, `stg`) and what each database holds can be noted below.
