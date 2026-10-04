# Unidades e módulos — VibeCode

Fonte oficial das lições do aplicativo VibeCode, de **Emanuel Bonfim**.

[Ver o catálogo completo](content/catalog.json) · [Guia para adicionar unidades](content/README.md) · [Aplicativo e APK](https://github.com/emanoelb5-lgtm/Vibecode-/releases/latest)

As unidades **1.1 — Informação e representação digital**, **1.2 — Lógica digital** e **1.3 — Arquitetura de computadores** já estão disponíveis: **96 lições**, com textos, exemplos, guias de prática, questões comentadas e glossário. O catálogo mantém a trilha dos cinco módulos e das 31 unidades da ementa.

| Unidade | Lições | Capítulos | Revisão | Glossário |
|---|---:|---:|---:|---:|
| 1.1 — Informação e representação digital | 32 | 7 | 32 questões | 45 termos |
| 1.2 — Lógica digital | 32 | 7 | 32 questões | 40 termos |
| 1.3 — Arquitetura de computadores | 32 | 7 | 32 questões | 48 termos |

A unidade 1.3 foi publicada no **conteúdo versão 4**, sem alterar o APK. Ela usa uma CPU fictícia com regras explícitas para acompanhar busca, decodificação, execução, registradores e memória.

| Capítulo da unidade 1.3 | Lições |
|---|---:|
| Uma máquina de programa armazenado | 4 |
| Por dentro da CPU | 5 |
| Buscar, decodificar e executar | 5 |
| Memória e hierarquia | 6 |
| Barramentos e transferências | 4 |
| Entrada, saída e interrupções | 5 |
| 32/64 bits e conjuntos de instruções | 3 |

Para baixar agora no celular com o APK 0.4.0, abra **Preferências → Verificar agora**. Depois vá a **Trilha → Módulo 1 → Arquitetura de computadores**. A atualização mantém anotações, favoritos e progresso.

O **VibeCode v0.4.0** consulta este repositório público automaticamente, sem login ou token. Depois do download, as lições ficam disponíveis offline. Anotações, favoritos e progresso permanecem no aparelho.

Para acrescentar uma unidade, edite **`content/catalog.json`**, aumente **`contentVersion`**, preserve os IDs já publicados e envie a alteração à branch **`main`**. O aplicativo encontra a nova versão ao abrir ou nas consultas em segundo plano. Também é possível usar **Preferências → Verificar agora**. Não é preciso gerar outro APK para acrescentar textos, exemplos, guias, questões ou capítulos no formato atual.

A ação [Validar catálogo](.github/workflows/conteudo.yml) verifica o arquivo e a preservação das unidades e lições antes de disponibilizar o pacote como artefato de verificação. O aplicativo também valida cada download antes de instalá-lo.

Endereço usado pelo aplicativo:
`https://raw.githubusercontent.com/emanoelb5-lgtm/Unidades-e-m-dulos-/main/content/catalog.json`

O código Android e os APKs continuam no repositório [Vibecode-](https://github.com/emanoelb5-lgtm/Vibecode-).
