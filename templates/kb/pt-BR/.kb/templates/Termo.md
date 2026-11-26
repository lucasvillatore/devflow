# Molde: Termo

## O que é

O significado de um termo do negócio. Não contém regras.

## Onde fica

- Usado num contexto só: `Contextos de negócio/<Contexto>/Glossário/<Termo>.md`.
- Usado em mais de um contexto: sobe para `Glossário/<Termo>.md`, na raiz.
- Mesma palavra com significados diferentes: cada contexto tem o seu arquivo.
- Termo ainda sem arquivo: listado em "A definir" no `index.md` do glossário.

## Seções

- `# Definição`: uma frase que diz o que o termo é.
- Quando há variações: um `##` por grupo, com uma frase que explica o grupo, e cada variação em bloco Nome/Descrição. Ver `style.md`.
- `# Exemplo`: uma frase que explica como ler os diagramas e um `##` por cenário.

## Não contém

- Regras, tabelas, "Evitar".
- Links para quem usa o termo (veja os backlinks). Uma variação pode apontar para o documento que ela nomeia.
