# Organizar a "01 — _entrada" — 2026-07-04 (PU 17)
> Pedido do dono: "várias lentes entram nos documentos, identificam e movem para as pastas certas — tudo, sem exceção, na pasta do Potencial Urbano" (link = raiz `1BrM6q36…`).

## O que foi feito
1. **Enumeração completa** da zona de despejo `01 — _entrada` (`1grhqYgttj7…`): **1.360 arquivos** (bem mais que os 868 do plano de 18/06 — o dono adicionou muitos desde então, ex.: 90 distritos de shapefiles SIRGAS, decretos/leis/acórdãos novos, quadros PDE, oráculos).
2. **Classificação por lentes de IA** (proveniência D-DONO-4 + doutrina 1.1): cada arquivo → pasta temática. 822 reaproveitaram o `de-para-final.csv`; 538 novos foram classificados por regra (leis→02, jurisprudência→2.6, doutrina→2.7, tabelas/quadros→03, shapefiles/zoneamento→05, oráculos/manifestos/logs/IA→00).
3. **Verificação estrutural (3 lentes):** as pastas-alvo 00–05 estão **VAZIAS** — o script de organização de 18/06 (`Arrumar-Drive-PotencialUrbano.gs`) **nunca foi executado**. Por isso tudo continua na `_entrada`.

## Distribuição final (1.360 arquivos)
| Destino | Qtd |
|---|---|
| `05 — Geo / Mapas` (shapefiles SIRGAS/ZEPEC, zoneamento) | 666 |
| `02 — Leis & Jurisprudência` (2.1–2.7: leis, decretos, acórdãos, doutrina) | 468 |
| `03 — Tabelas & Engines` (Quadros PDE, Q14, notebooks, sócios/empresas) | 166 |
| `00 — Governança & Índice` (oráculos, manifestos, logs, relatórios NOSSOS, LOTES_IA não-confiável) | 54 |
| `99 — Inbox / Triagem` (6 ambíguos — triagem manual, nunca perdidos) | 6 |

## Como executar (o conector do Drive NÃO move — o Apps Script move de verdade)
1. `script.google.com` → Novo projeto → cole **`Organizar-Entrada-2026-07-04.gs`** inteiro.
2. Deixe `DRY_RUN = true`. Rode `organizarEntrada` (autorize o Drive). Confira o log.
3. Aprovou? Troque `DRY_RUN = false` e rode de novo — **move de verdade, sem duplicar**. Se pausar por tempo, rode de novo (retoma).

## Doutrina respeitada
- **Move, não copia** (`file.moveTo`) — não cria duplicata (evita o modo de falha V-3).
- **Nada se descarta:** os 6 ambíguos e os NOSSO/não-confiáveis (LOTES_IA) vão para 00/99, não pra lixeira.
- **Fora de escopo preservado:** financeiro/BNDES/Keepee que apareceram na `_entrada` foram para 00 (não descartados, mas fora do corpus).
- **de-para completo auditável:** `de-para-COMPLETO-2026-07-04.csv` (fileId · título · destino · folderId).

## Pendência conhecida
- O lago legado **`TODOS TDC`** (março/2026, ~1.000+ arquivos aninhados com 3 cemitérios de duplicatas) NÃO entra neste script — é um saneamento à parte (usar `Sanear-Duplicatas-*.gs`). Escopo desta rodada = só a `_entrada`, conforme o link do dono.
