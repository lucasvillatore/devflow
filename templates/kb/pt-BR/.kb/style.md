# Estilo de escrita

## Regras

- **Política primeiro, efeito depois.** Exemplo: "O prazo de entrega é sempre de pelo menos 1 dia. Um prazo zero informado pelo fornecedor é desconsiderado."
  - Nunca use "Se X, o sistema faz Y". Esse formato descreve o mecanismo, não a decisão de negócio.
- **Língua do negócio.** Nada de nome de sistema, serviço, fila, endpoint, tabela, classe ou formato de dado.
  - Teste: se o sistema for reescrito amanhã em outra tecnologia, a frase continua verdadeira?
  - Um fornecedor externo pode aparecer como exemplo, entre parênteses.
- **Frases curtas, uma ideia por frase, voz ativa.**
- **Um nome para cada coisa.** Use sempre o termo do glossário.
- **A description do frontmatter diz do que o documento trata.** Ela não repete o conteúdo.
- **Comportamento que ninguém decidiu** entra numa seção ou item "A confirmar", nunca como regra.
- **Sem avisos de nível**, como "visão de alto nível". A base é sempre de alto nível.

## Blocos Nome/Descrição

- Use só para **valores e estados** (ex.: aprovado, recusado, em análise).
- Nunca use para comportamento, impacto, campos ou pontos de atenção. Esses vão em lista ou em texto corrido.
- Formato, com os rótulos em negrito:

```
**Nome:** Aprovado
**Descrição:** A análise terminou sem encontrar problema no pedido.
```

- **Estados não terminais vêm sempre antes dos terminais.** Os grupos se chamam "Status não terminais" e "Status terminais", ou "Estados não terminais" e "Estados terminais" nos termos.

## Formato

- **Sem tabelas** em termos, regras e partes do processo.
- **Links sempre para o arquivo**, nunca para um título (`arquivo.md#titulo`).
- **Links relativos em markdown**, com espaços codificados (`%20`).
- **Sem seções Citations nem "Onde vale".** Para saber onde uma regra vale, veja os backlinks.
- **Frontmatter:** um texto sem aspas não pode conter ": " (dois-pontos seguido de espaço). Isso quebra o YAML.
