# Formato de pull request

Usado pela `open-pr`. Edite à vontade: a skill segue este arquivo.

- Idioma: português
- Referência: <link de um PR bom do time, opcional>

## Título

`<tipo>(<CHAVE>): <o que muda, em minúsculas>`, com tipo de conventional commit (`feat`, `fix`, `refactor`, `test`, `chore`). Ex.: `feat(ABC-123): frete grátis por região no checkout`.

## Corpo

```markdown
[<CHAVE>](<link da Issue>): <1 a 3 frases: o problema e o que este PR muda, na linguagem do domínio>

## Summary

<menor visual que deixa o ponto claro, com o texto curto que ele apoia>

## <seções extras, só quando houver>

## Evidence

- **Before:** <saída/teste/comportamento antes>
  **After:** <saída/teste/comportamento depois>

<saída dos testes e demais evidências>

## Merge Danger

**Door:** <one-way ou two-way>

<como voltar atrás, se two-way>

**Blast Radius:** <uma palavra>

- <consequência do merge, um bullet cada>
```

### Summary

Escolha a **menor vista** que mostra a mudança; uma ou duas bastam:

- árvore de arquivos com `diff` (`+`/`-`) para estrutura nova ou mudada, com um comentário curto por arquivo;
- pseudocódigo ou árvore de chamadas, em `diff` quando o fluxo já existia;
- bloco `text` com o formato de documentos ou tabelas novas;
- tabela quando há casos a comparar.

### Seções extras

Inclua quando a branch tiver: **carga/configuração manual** (o que foi gravado, onde, se já está em staging, script fora do repo), **testes em staging** (tabela `ID | Cenário | Esperado | Antes | Depois | ✅`). Omita a seção quando não houver.

### Evidence

Prefira evidência executada: teste que falhava e passa, saída de comando, tabela de staging. Liste os testes novos pelo comportamento que cobrem.

### Merge Danger

- **Door:** two-way quando dá para reverter sem perda (revert, flag, config); one-way quando há ação destrutiva ou difícil de desfazer (dados apagados, migração sem volta).
- **Blast Radius:** a área afetada numa palavra. Nos bullets: passos obrigatórios antes do deploy, mudança de comportamento para quem consome, efeitos em produção.
