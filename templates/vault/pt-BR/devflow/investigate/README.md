# Investigate

Dados que as skills `awsq` e `dbq` usam. Nenhuma credencial fica aqui: AWS usa SSO, bancos usam o cofre `pass`.

## AWS (`aws.json`)

Mapa de `<ambiente>/<papel>` para perfil do `~/.aws/config`, com a sessão SSO. O primeiro perfil é usado para checar se a sessão vale.

```json
{
  "sso_session": "minha-empresa",
  "profiles": {
    "stg/developer": {"profile": "empresa-stg-developer", "use_for": "tudo em staging: pipeline, logs, ECS, S3, SQS"},
    "prod/monitoring": {"profile": "empresa-prod-monitoring", "use_for": "CloudWatch Logs, métricas, alarmes, ECS"}
  }
}
```

Recursos de cada repositório (pipelines, log groups, serviços) ficam no perfil dele, em `../projects/<repo>.md`.

## Bancos (`pass`)

Entradas em `<projeto>/<ambiente>/db/<nome>`, com a URI na primeira linha (`mongodb://`, `mysql://`, `redis://`). Ambientes de teste da empresa (ex.: `hml`, `stg`) e o que cada banco guarda podem ser anotados abaixo.
