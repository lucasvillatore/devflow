# Molde: Regra de negócio

## O que é

Uma política do negócio e a consequência prática dela. Trata de um assunto só.

## Onde fica

Solta na raiz do contexto que ela restringe: `Contextos de negócio/<Contexto>/<Nome da regra>.md`. Nunca dentro de uma jornada. Listada na seção "Regras" do `index.md` do contexto.

## Nome

Diz a política, não o caso nem o momento técnico. Bom: "Prazo de entrega mínimo". Ruim: "Prazo zero na atualização".

## Seções

- `# Regra`: de uma a três frases, ou uma lista curta. A política primeiro, o efeito depois. Pode ter `##` para um subgrupo (ex.: `## Gatilho`) e `## A confirmar` para comportamento sem decisão.
- `# Exemplo`: uma frase que explica como ler os diagramas e um `##` por cenário, cada um com uma frase e um diagrama. Ver `diagrams.md`.

## Não contém

- Link para jornada. Para saber onde a regra vale, veja os backlinks.
- Citations, "Onde vale", tabelas.

## Exemplo bom

```markdown
---
type: Regra de negócio
title: Uma análise por pedido
description: Define quantas análises um mesmo pedido pode ter em andamento.
tags: [pedido]
status: ativo
timestamp: 2026-01-15
---

# Regra

Cada pedido é analisado individualmente e tem no máximo uma análise em andamento. Um novo pedido de análise para um pedido que ainda está sendo analisado é recusado.

# Exemplo

## Pedido durante a análise

O pedido 123 aguarda o resultado da análise de crédito. Chega um novo pedido de análise para o pedido 123. O novo pedido é recusado.

(diagrama mermaid)
```
