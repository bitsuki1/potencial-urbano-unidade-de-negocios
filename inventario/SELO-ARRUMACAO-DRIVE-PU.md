# SELO — Arrumação do Drive PU CONCLUÍDA (POTENCIAL URBANO) · 2026-07-12
> Pedido do MOU: "deixar perfeitamente arrumado, nada órfão, nada duplicado, tudo em pasta, catalogado e
> tagueado, duplicatas numa pasta só". EXECUTADO em modo autônomo (robô/conta de serviço, MOVE não apaga).
> Prova real (read-only via SA): run selo `29211180386` — **SELO: OK — 0 órfão na raiz**.

## Resultado da execução (run real `29208161824`, ~1h02m, erros=0)
| Métrica | Valor |
|---|---:|
| movidos p/ o devido lugar (keepers/resgate/órfãos → canônico e 99) | **2.417** |
| já-no-lugar (idempotente — duplicatas já na APAGAR da sessão anterior) | 7.364 |
| já na lixeira do Drive (pulados) | 1.300 |
| ficaram no `90` sem mover (SO_IDEIA já dentro do DataLake renomeado) | **22.057** |
| ERROS | **0** |

## Topo real de POTENCIAL URBANO depois (prova SA, filhos diretos)
| Pasta | Filhos diretos | Papel |
|---|---:|---|
| `00 — Governança & Índice` | ~64 | índice/catálogo/governança |
| `01 — _entrada (despejo IPTU+TDC)` | 0 | zona de despejo do bruto novo |
| `02 — Leis & Jurisprudência` | ~1.422 | corpus oficial auditável (fonte do RAG) |
| `03 — Tabelas & Engines` | ~140 | tabelas → input de engine |
| `04 — Tese (Antítese/Vacina)` | 0 | camada de tese (a povoar) |
| `05 — Geo` | **0 — VAZIA** | duplicata do 05; esvaziada (o MOU pode excluir) |
| `05 — Geo / Mapas` | 1.177 | geo/mapas consolidado |
| `90 — Material bruto (só ideias)` | 211 diretos + 15 subpastas | DataLake `TODOS TDC` renomeado; 22.057 fragmentos aninhados (o MOU revê 1-a-1) |
| `99 — APAGAR (duplicados e descarte)` | 7.307 | pasta ÚNICA de lixo; o MOU exclui quando quiser |
| `99 — DUPLICATAS-A-EXCLUIR` | **0 — VAZIA (fundida)** | 2ª lixeira esvaziada dentro da única APAGAR |

## Selo (as garantias que o MOU pediu)
- ✅ **0 órfão na raiz** — nenhum arquivo solto; tudo em pasta (prova SA).
- ✅ **Uma pasta de lixo só** — `99 — APAGAR`; a 2ª lixeira (`99 — DUPLICATAS-A-EXCLUIR`) foi fundida e está vazia.
- ✅ **Nada oficial no lixo** — norma oficial não-duplicada foi PROTEGIDA (correção do MOU "TODOS TDC não é só não-auditável"); 396 resgatadas + keepers ao canônico.
- ✅ **Não-auditável isolado** — 22.057 fragmentos (só-ideias) guardados no `90`, fora do canônico (o MOU olha 1-a-1 depois).
- ✅ **Catalogado e tagueado** — de-para completo `inventario/drive-pu/ARRUMAR-DE-PARA.csv` (33.138 linhas: id → destino → motivo → tema/tipo).
- ✅ **Reversível** — tudo foi MOVE, não delete; o MOU decide o que excluir na `99`.

## Pendências mínimas (decisão do MOU)
- `05 — Geo` (vazia) e `99 — DUPLICATAS-A-EXCLUIR` (vazia) podem ser **excluídas** pelo MOU (o robô SA não
  apaga pasta de outro dono). São 2 pastas vazias — cosmético.
- `04 — Tese` e `01 — _entrada` vazias por ora (a povoar conforme o trabalho).

## Rastro (ativos)
`scripts/gerar_arrumar_de_para.py` · `scripts/mover_por_destino_sa.py` · `scripts/selo_arrumacao_sa.py` ·
`.github/workflows/arrumar-drive.yml` (ações: arrumar | selo) · `inventario/ROADMAP-ARRUMACAO-DRIVE-PU.md`.
