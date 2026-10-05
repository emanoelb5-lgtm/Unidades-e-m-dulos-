# Adicionar lições e unidades

`catalog.json` é o catálogo completo consumido pelo VibeCode v0.5.0. O aplicativo consulta a branch `main` deste repositório público, sem autenticação.

1. Mantenha `schemaVersion: 1` e aumente `contentVersion` ao modificar o conteúdo.
2. Acrescente a unidade em `units`, usando o ID que já aparece no módulo correspondente em `modules`. Preserve todas as unidades e lições publicadas.
3. Use IDs únicos e estáveis. Eles ligam cada lição às anotações, favoritos e conclusão no celular.
4. Inclua título, subtítulo, minutos sugeridos, objetivos, blocos, guia, uma atividade interativa e uma pergunta de compreensão em cada lição.
5. Inclua capítulos, revisão comentada, glossário e referências HTTPS.
6. Execute `python tools/validate_catalog.py` e faça commit em `main`. A ação do GitHub verifica também a continuidade com o catálogo anterior.

Os blocos aceitos são `text`, `example`, `callout` e `practice`. Cada bloco tem `kind`, `title` e `text`. Escreva uma ideia por lição e mantenha a sequência conceito → exemplo → prática no aplicativo → correção.

O leitor organiza os campos automaticamente:

| Etapa | Campos |
|---|---|
| Aprenda | Blocos `text` e `callout` |
| Exemplo | Blocos `example` |
| Pratique | Objeto `activity`: controles, dica, verificação e feedback |
| Confira | Pergunta `check` |
| Conclua | `objectives` e marcação de conclusão |

Cada capítulo contém `id`, `title`, `description` e `lessonIds`. Os capítulos devem cobrir todas as lições uma vez, na ordem da unidade.

As questões usam `prompt`, `choices`, `correct` e `explanation`; `correct` começa em zero. Na revisão, inclua também `id` e `lessonId`, que deve existir na mesma unidade. Cada lição deve ter pelo menos uma questão de revisão correspondente.

`assessmentVersion` começa em 1. Aumente quando substituir ou ampliar substancialmente a revisão de uma unidade. Não reduza essa versão.

O campo opcional `lab` mantém compatibilidade com leitores antigos. No leitor v0.5.0, a atividade ocorre na própria lição; não precisa abrir outra tela. Novos tipos de laboratório e mudanças no formato do conteúdo exigem código Android; novas lições no formato atual chegam sem outra instalação.

O pacote deve ter até 2 MB. O aplicativo recusa downloads inválidos e atualizações que removam unidades, lições ou versões de revisão existentes. Sem internet, usa o último conteúdo válido salvo no aparelho. As consultas automáticas ao abrir respeitam um intervalo mínimo de uma hora; em segundo plano, são previstas a cada seis horas conforme conexão e bateria. A opção **Verificar agora** permite consultar imediatamente.

Para importar manualmente, baixe o arquivo JSON e abra **Preferências → Importar arquivo**. O catálogo contém as unidades anteriores e a nova unidade, e não apenas o trecho acrescentado.

## Atividades no conteúdo versão 5

Mantenha `interactivePractice: true` na raiz. **Todas as lições precisam de `activity`.** Não peça atividades em papel, outro aplicativo, pesquisa externa ou explicação oral. Cada comando deve indicar um controle disponível na própria prática. O caderno é opcional e também fica no aplicativo.

Cada atividade possui `id` único e estável, `revision` inteiro positivo, `type`, `title`, `prompt`, `hint` e `success`. Preserve o ID; aumente `revision` quando mudar a tarefa ou o gabarito. Isso inicia uma nova prática sem apagar notas, favoritos, conclusões anteriores ou resultados de revisão. Aumente também `contentVersion` a cada alteração publicada.

| Tipo | Campos e funcionamento |
|---|---|
| `fields` | `fields`: de 1 a 8 campos com `id`, `label`, `kind`, `answer`, `explanation` e unidade opcional `unit`. `number` usa resposta decimal como string, com ponto no JSON; o aluno pode digitar ponto ou vírgula. `choice` inclui `choices` e `answer` como string do índice correto, começando em zero. |
| `order` | `items`: 3 a 8 passos apresentados fora de ordem. `correct` contém todos os índices na ordem correta, uma vez cada. O aluno monta e pode ajustar a sequência. |
| `bits` | `width`: 4 ou 8. `target`: padrão inteiro sem sinal que deve ser montado. `signed`: indica interpretação em complemento de dois. Por exemplo, −5 em 8 bits usa `target: 251`. |
| `logic` | `gate`: AND, OR, NOT, XOR, NAND, NOR, NOT_AND, AND_OR, HALF_ADD, FULL_ADD ou MUX. `cases`: sequências de entradas como "00" e "11". O circuito ao vivo calcula a saída; o aluno preenche a tabela. Somadores usam saída CS de dois bits. |
| `state` | `machine`: SR, D, T, REGISTER4, TOGGLE ou COUNTER2. `start` é o estado inicial; `events` contém de 2 a 8 objetos com `label` e `inputs`. O aluno prevê e aplica cada evento. SR usa [S,R] e proíbe [1,1]; D usa [D,borda]; T/TOGGLE usam [entrada]; REGISTER4 usa [D,load]; COUNTER2 usa []. |
| `cpu` | `program`: de 2 a 16 instruções. `registers`: quatro valores de 0 a 255. `memory`: até 8 pares `address`/`value`. Inclui `fields` de resultado, como em `fields`. O aluno busca, decodifica e executa até HALT, depois verifica as respostas. |
| `color` | `target`: [R,G,B], cada canal de 0 a 255. O aluno altera os controles e vê a cor mudar. |

Para `cpu`, LOAD usa `dst` e `address`; STORE usa `a` (registrador fonte) e `address`; ADD usa `dst`, `a` e `b`; JMP usa `address`; JZ usa `a` e `address`; HALT usa apenas `op`. Os índices de registrador são de 0 a 3. Os saltos precisam apontar para instruções do programa; a execução deve terminar em até 64 instruções. Os dados não podem ocupar os bytes do programa. Use campos de resultado cujos gabaritos coincidam com a execução.

As instruções pertencem à CPU fictícia do curso: quatro bytes por instrução, R0 a R3 de 8 bits, endereços de byte de 0 a 255 e ADD conservando os oito bits inferiores. HALT conserva o PC. O endereço 240 fornece a entrada numérica fictícia e 241 recebe o indicador de saída. Não apresente esse formato como ARM, x86 ou RISC-V.

Os sete tipos já suportados podem ser usados em novas lições sem recompilar o APK. Tipos diferentes exigem novo código Android. Os validadores e o leitor recusam atividades desconhecidas ou incompletas. No conteúdo 5, os 96 IDs de lição, capítulos e gabaritos das revisões anteriores foram preservados.
