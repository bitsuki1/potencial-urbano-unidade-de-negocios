# Relatório — Catálogo da pasta POTENCIAL URBANO do Drive (PU 19, 2026-07-12)

> Missão do dono: catalogar, organizar, taguear e ler TODO o drive de PU = a pasta **POTENCIAL URBANO**
> (`1BrM6q36…`) dentro de PORTFÓLIO DO MOU. Feito por trabalhadores TRAVADOS (sem spawn, sequenciais).
> Mestre: `inventario/CATALOGO-DRIVE-PU-2026-07-12.csv` (uma linha por arquivo, dedup por drive_id).

## Números (33.138 arquivos únicos)
- **Já no índice antigo:** 218 · **Novos (não-indexados):** 32.920.
- **Por tema:** GEO **16.725** (½!) · OUTRO 13.781 · JURÍDICO 1.593 · TDC 601 · GOVERNANÇA 395 · IPTU 43.
- **Por tipo:** OUTRO 18.732 (imagens extraídas + chunks .md) · TABELA 5.473 · GEO_SHP 3.708 · PDF 2.581 · LEI 813 · DECRETO 560 · PORTARIA 201 · JURISPRUDÊNCIA 87 · CODEX 146 · AUDITORIA 139.

## Onde estão (subpastas de POTENCIAL URBANO)
- **Raiz (despejo):** 73 · **00 Governança:** 52 · **03 Tabelas & Engines:** 166 (já indexadas) · **04 Tese:** vazia.
- **`TODOS TDC` (DataLake medallion):** o grosso — BRONZE (RAW 267 · OFICIAL 1.540 · NÃO_OFICIAL vazio · CRIADOS 58) · SILVER 3.608 · INBOX 264 · ORIGINAIS 62 · CRIADOS06 14 · PASTA_UNICA 351 · **DataLake_TDC e IPTU (clone aninhado) 25.957** (12.785 imagens + 4.879 chunks .md + 2.896 tabelas) · 3 pastas de descarte.

## Achados de organização
- **Metade do lake é GEO** (shapefiles fragmentados + 12.785 imagens extraídas) — ruído para o RAG.
- **`DataLake_TDC e IPTU` é um CLONE aninhado** do medallion inteiro (tem seu próprio BRONZE/SILVER/99_LIXEIRA) — fonte enorme de duplicação.
- **9.616 candidatos à pasta APAGAR:** 3.600 em pastas de descarte (99_LIXEIRA/QUARENTENA/PARA_DELETAR, top-level + clone) + 6.016 duplicatas fortes (mesmo nome+tamanho).
- **Bug do conector Drive:** a busca do MCP re-serve páginas sobrepostas (sem orderBy estável) — todos os workers deduplicaram por id; pode restar resíduo não-alcançável em pastas gigantes (ex.: Imagens_Extraidas 12.785+).

## Camada de valor (a fração que importa para o RAG/engines)
- **SILVER/Legislacao_Urbanistica** + **BRONZE_OFICIAL** + **ORIGINAIS**: leis/decretos/portarias/tabelas OFICIAIS (LPUOS, PDE Quadros, Estatuto da Cidade, Decreto 57.536, Lei 17.844, portarias SMUL). ~2.850 OFICIAIS no total.
- É essa fração (não os 16.725 GEO nem as 12.785 imagens) que vale confrontar com o nosso corpus `leis/` e ingerir o que faltar.
