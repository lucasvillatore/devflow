# Checklist de revisão

O revisor confere cada item e aponta o arquivo, a linha e a correção sugerida.

## Estrutura

- [ ] O frontmatter tem todos os campos obrigatórios, e o `type` existe na configuração.
- [ ] As seções seguem o molde do tipo, na ordem.
- [ ] O documento está na pasta certa: jornada em `Jornadas/`, regra solta na raiz do contexto, termo no `Glossário/`, parte do processo na pasta de partes.
- [ ] O documento está listado no `index.md` da pasta, com a mesma description do frontmatter.

## Conteúdo

- [ ] Cada informação tem um único dono. Nada repete o que já está em outro documento: aponte com link.
- [ ] Nenhum comportamento sem decisão de negócio aparece como regra. Ele está em "A confirmar".
- [ ] Nada contradiz outro documento da base.
- [ ] Os exemplos são concretos, com valores, e mostram cenários diferentes.

## Escrita

- [ ] A política vem primeiro. Nenhuma frase "Se X, o sistema faz Y".
- [ ] Nenhum nome de sistema, serviço, fila, endpoint, tabela ou classe.
- [ ] A description não repete o conteúdo.
- [ ] Blocos Nome/Descrição só para valores e estados. Não terminais antes dos terminais.
- [ ] Sem tabelas, sem links com `#`, sem Citations, sem "Onde vale".

## Nomes

- [ ] O nome do arquivo é nome de negócio, com a primeira letra maiúscula, espaços e acentos.
- [ ] O nome de uma regra diz a política.
- [ ] Nenhuma pasta tem nome de sistema.

## Jornada

- [ ] Uma pessoa percorre o caminho. Um processo que o negócio executa sozinho é contexto, não jornada.
- [ ] Cada passo tem uma frase e no máximo um link.
- [ ] Todas as lacunas estão em "Em aberto".
