# Molde: Jornada

## O que é

O caminho que uma **pessoa** percorre até um objetivo de negócio, do início ao fim. Um processo que o negócio executa sozinho (ex.: aprovação de pedido, faturamento) não é jornada: é um contexto. A jornada aponta para o índice do contexto.

## Onde fica

`Jornadas/<Nome da jornada>.md`. O nome é o objetivo de negócio. O `Jornadas/index.md` agrupa por quem percorre o caminho.

## Seções

- `# Objetivo`: uma ou duas frases. Quem percorre o caminho e o que quer conseguir.
- `# Fluxo` (opcional): só quando há ramificação real. Ver `diagrams.md`.
- `# Passos`: lista numerada, na ordem. Cada passo tem uma frase e no máximo um link, para uma regra ou para o índice de um contexto.
- `# Desvios` (quando existe): um item por desvio, com o link da regra que vale nele.
- `# Em aberto` (quando falta algo): todas as lacunas, uma por item.

Em `rascunho`, só `# Objetivo` é obrigatório.

## Não contém

- O texto de uma regra ou o conteúdo de um processo. Só o link.
- Nome de sistema.

## Exemplo bom

```markdown
---
type: Jornada
title: Compra com retirada na loja
description: Caminho do cliente desde a escolha do produto até a retirada na loja física.
tags: [compra, retirada]
status: rascunho
timestamp: 2026-01-15
---

# Objetivo

O cliente compra pelo site e quer retirar o produto numa loja física.

# Passos

1. O cliente escolhe o produto e a loja de retirada.
2. O pedido passa pela [Aprovação de pedido](../Contextos%20de%20neg%C3%B3cio/Aprova%C3%A7%C3%A3o%20de%20pedido/index.md).
3. O cliente retira o produto na loja.

# Desvios

- **Produto sem estoque na loja:** o pedido é transferido. Vale o [Prazo de transferência entre lojas](../Contextos%20de%20neg%C3%B3cio/Estoque/Prazo%20de%20transfer%C3%AAncia%20entre%20lojas.md).

# Em aberto

- Como o cliente fica sabendo que o produto chegou na loja.
```
