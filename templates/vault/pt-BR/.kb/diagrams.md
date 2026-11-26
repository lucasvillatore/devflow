# Diagramas

## Regras

- Use mermaid `flowchart LR`.
- Cada caixinha mostra o nome e o estado ou o papel no próprio texto: `rev[Revisão<br/>desconsiderada]`.
- Antes dos cenários, uma frase explica como ler as setas. Exemplo: "A seta mostra o caminho do pedido até o resultado."
- Cada cenário é um `##` com uma frase e um diagrama.
- Uma jornada só tem diagrama quando o caminho tem ramificação real. Linha contínua é o caminho normal, linha tracejada (`-.->`) é um desvio.
- Sem losangos de decisão interna de sistema.

## Cores por estado

Declare só as classes usadas no diagrama.

```
classDef ok fill:#d9f2e3,stroke:#1d7a46,color:#14301f
classDef bad fill:#fbe0dd,stroke:#b3261e,color:#3d1e1b
classDef wait fill:#fbeedf,stroke:#b4570e,color:#3a2817
classDef info fill:#e8eefb,stroke:#2456c9,color:#14213d
classDef skip fill:#eceef2,stroke:#5d6779,color:#1b2230,stroke-dasharray: 4 3
```

- `ok`: aprovado, concluído, fim feliz.
- `bad`: reprovado, recusado, erro.
- `wait`: aguardando ou processo em andamento. Acrescente `stroke-dasharray: 4 3` quando é pendência.
- `info`: passo, informação, em andamento.
- `skip`: desconsiderado, não pedido.
