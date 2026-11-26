# Perfis de repositório

Um arquivo por repositório (`<repo>.md`, com o nome da pasta do repo). As skills do devflow leem e completam estes arquivos; quando falta um campo, perguntam e gravam.

```markdown
# <repo>

- Caminho local: ~/dev/<repo>
- Branch default: main
- Testes dos arquivos alterados: <comando, com {files}>
- Lint dos arquivos alterados: <comando, com {files}>
- Build: <comando>
- Suíte completa: <comando>
- Limite de complexidade: 10
```

Acrescente o que mais for específico do repo (pipeline de staging, recursos, cuidados). A seção `## Melhorias recusadas` guarda melhorias que você recusou com motivo; a `analyze` não sugere de novo.
