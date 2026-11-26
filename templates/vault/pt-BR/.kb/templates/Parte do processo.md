# Molde: Parte do processo

## O que é

Uma das partes de um processo do negócio: um tipo de análise, uma etapa de um fluxo. Explica o que a parte faz, o que exige e como o resultado dela afeta o processo inteiro.

## Onde fica

Numa pasta de partes do processo dentro do contexto, listada em `folders.process_parts` do `base.yaml`. Exemplo: `Contextos de negócio/Aprovação de pedido/Tipos de análise/Análise de crédito.md`. O frontmatter usa `type: Regra de negócio`.

## Seções

- `# O que é`: o que a parte faz, em uma ou duas frases, com a ideia principal em negrito. Pode ter um exemplo curto.
- `# Campos mínimos`: lista dos dados de que a parte precisa, cada um em negrito com uma frase.
- `# O que ela faz`: lista numerada dos passos. Pode ter `##` para um grupo.
- `# Resultado`: os estados possíveis em blocos Nome/Descrição. Não terminais antes dos terminais.
- `# Impacto`: lista. Quando a parte reprova o processo, o que ela muda nas outras partes.
- `# Exemplo`: uma frase que explica como ler os diagramas e um `##` por cenário.

## Parte dividida em subpartes

Quando a parte é feita separadamente para cada tipo de item:

- `# O que é` vale para todas.
- `# Em comum a todos os tipos` traz o que vale para todas, com as seções do molde como `##`.
- Cada subparte é um `#`, com as seções do molde como `##`. Só repita a seção que muda.

## Não contém

- As regras do processo inteiro (ordem, dependências, resultado final). Elas ficam em regras soltas na raiz do contexto.
- Repetição de outra parte. Aponte com link.
