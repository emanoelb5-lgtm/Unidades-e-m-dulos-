# Unidades e módulos — VibeCode

Fonte oficial das lições do aplicativo VibeCode, de **Emanuel Bonfim**.

[Ver o catálogo completo](content/catalog.json) · [Guia para adicionar unidades](content/README.md) · [Aplicativo e APK](https://github.com/emanoelb5-lgtm/Vibecode-/releases/latest)

As unidades **1.1 — Informação e representação digital** e **1.2 — Lógica digital** já estão disponíveis: **64 lições**, com textos, exemplos, guias de prática, questões comentadas e glossário. O catálogo mantém a trilha dos cinco módulos e das 31 unidades da ementa.

| Unidade | Lições | Capítulos | Revisão | Glossário |
|---|---:|---:|---:|---:|
| 1.1 — Informação e representação digital | 32 | 7 | 32 questões | 45 termos |
| 1.2 — Lógica digital | 32 | 7 | 32 questões | 40 termos |

O **VibeCode v0.4.0** consulta este repositório público automaticamente, sem login ou token. Depois do download, as lições ficam disponíveis offline. Anotações, favoritos e progresso permanecem no aparelho.

Para acrescentar uma unidade, edite **`content/catalog.json`**, aumente **`contentVersion`**, preserve os IDs já publicados e envie a alteração à branch **`main`**. O aplicativo encontra a nova versão ao abrir ou nas consultas em segundo plano. Também é possível usar **Preferências → Verificar agora**. Não é preciso gerar outro APK para acrescentar textos, exemplos, guias, questões ou capítulos no formato atual.

A ação [Validar catálogo](.github/workflows/conteudo.yml) verifica o arquivo e a preservação das unidades e lições antes de disponibilizar o pacote como artefato de verificação. O aplicativo também valida cada download antes de instalá-lo.

Endereço usado pelo aplicativo:
`https://raw.githubusercontent.com/emanoelb5-lgtm/Unidades-e-m-dulos-/main/content/catalog.json`

O código Android e os APKs continuam no repositório [Vibecode-](https://github.com/emanoelb5-lgtm/Vibecode-).
