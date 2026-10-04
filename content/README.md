# Adicionar lições e unidades

`catalog.json` é o catálogo completo consumido pelo VibeCode v0.4.0. O aplicativo consulta a branch `main` deste repositório público, sem autenticação.

1. Mantenha `schemaVersion: 1` e aumente `contentVersion` ao modificar o conteúdo.
2. Acrescente a unidade em `units`, usando o ID que já aparece no módulo correspondente em `modules`. Preserve todas as unidades e lições publicadas.
3. Use IDs únicos e estáveis. Eles ligam cada lição às anotações, favoritos e conclusão no celular.
4. Inclua título, subtítulo, minutos sugeridos, objetivos, blocos, guia e uma pergunta de compreensão em cada lição.
5. Inclua capítulos, revisão comentada, glossário e referências HTTPS.
6. Execute `python tools/validate_catalog.py` e faça commit em `main`. A ação do GitHub verifica também a continuidade com o catálogo anterior.

Os blocos aceitos são `text`, `example`, `callout` e `practice`. Cada bloco tem `kind`, `title` e `text`. Escreva uma ideia por lição e mantenha a sequência conceito → exemplo → previsão → prática → explicação própria.

O leitor organiza os campos automaticamente:

| Etapa | Campos |
|---|---|
| Aprenda | Blocos `text` e `callout` |
| Exemplo | Blocos `example` |
| Pratique | Blocos `practice` e `guide` |
| Confira | Pergunta `check` |
| Conclua | `objectives` e marcação de conclusão |

Cada capítulo contém `id`, `title`, `description` e `lessonIds`. Os capítulos devem cobrir todas as lições uma vez, na ordem da unidade.

As questões usam `prompt`, `choices`, `correct` e `explanation`; `correct` começa em zero. Na revisão, inclua também `id` e `lessonId`, que deve existir na mesma unidade. Cada lição deve ter pelo menos uma questão de revisão correspondente.

`assessmentVersion` começa em 1. Aumente quando substituir ou ampliar substancialmente a revisão de uma unidade. Não reduza essa versão.

O campo opcional `lab` pode abrir um laboratório existente: Bits, Bases, Sinal, Precisão, Texto, Cores ou Mídia. Novos tipos de laboratório e mudanças no formato do conteúdo exigem código Android; novas lições no formato atual chegam sem outra instalação.

O pacote deve ter até 2 MB. O aplicativo recusa downloads inválidos e atualizações que removam unidades, lições ou versões de revisão existentes. Sem internet, usa o último conteúdo válido salvo no aparelho. As consultas automáticas ao abrir respeitam um intervalo mínimo de uma hora; em segundo plano, são previstas a cada seis horas conforme conexão e bateria. A opção **Verificar agora** permite consultar imediatamente.

Para importar manualmente, baixe o arquivo JSON e abra **Preferências → Importar arquivo**. O catálogo contém as unidades anteriores e a nova unidade, e não apenas o trecho acrescentado.
