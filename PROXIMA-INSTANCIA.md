# PRÓXIMA INSTÂNCIA — o que fazer (Potencial Urbano)

> Handoff sem perdas — Escritório do MOU (PMO), 2026-06-20. Estado pós-auditoria triplo-limpo.
> Retome por aqui + `HANDOFF-E-PENDENCIAS.md` + `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md`.
> SSOT do estado de cada item = `MANIFESTO.json` (agora VIVO, gerado por `scripts/consolidar.py`).
> Doutrina: zero-compressão · dialético · agnosticismo · nada se descarta. Não AFINAR sem destravar.

## Estado em 2026-06-20 (verificado)
- **Corpus:** 59 itens — 27 leis (12 federais `bruto` verbatim + 15 municipais-SP) + 32 jurisprudências (`tagueado`). 57 no escopo + 2 fora (`stf-tema-1020`=ISS, `stj-resp-1658054`=previdenciário).
- **MANIFESTO.json:** vivo e idempotente; Action `consolidar.yml` ligada (regenera a cada push, sem loop).
- **Supabase** `potencial-urbano-iptu-tdc` (`csnalylpvysjvejgsymr`, sa-east-1): só `governanca` (de_para, registro_decisoes — vazios) + `public`/PostGIS. Schemas dos artefatos NÃO criados (de propósito, RO-23).
- **Drive:** inventariado; ~16–20 GB de duplicatas mapeadas, executor de exclusão pronto (decisão MOU: EXCLUIR).

## PENDÊNCIAS (prioridade ↓)

### P1 — Executar a exclusão das duplicatas no Drive (decisão MOU tomada: EXCLUIR)
- Rodar `drive-arrumacao/Sanear-Duplicatas-PotencialUrbano.gs` (Apps Script): `DRY_RUN=true` → conferir Logs → `DRY_RUN=false` → executa (lixeira, recuperável ~30d).
- **O MCP do Drive desta sessão NÃO apaga** — execução é 1 clique no Apps Script da conta do MOU. Mapa+ids: `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md`.
- VACINA: o script só apaga se a cópia canônica existir; Fase 2 só duplicata exata (nome+tamanho). Conferir que SIRGAS_SHP_LOTES (geometrias + `.prj`) ficou com ≥1 cópia.
- Depois: re-rodar o catálogo do Drive e atualizar `docs/INVENTARIO-DRIVE-*.md` (IDs sobreviventes; a árvore foi achatada — os docs de 2026-06-18 descrevem estrutura que não existe mais).

### P2 — Re-ingerir as 14 leis municipais-SP em VERBATIM (lacuna probatória real)
- Hoje são RESUMOS de WebSearch (`confianca: baixa`) — ferem Princípio 1.7 (citação) e 1.2 (extração pura). Ver `MANIFESTO.json` campo `alertas.itens_nao_verbatim_*`.
- Fonte: os PDFs já estão no Drive (catalogo `inventario/catalogo-juridico-drive.csv`) — é **re-ingestão interna, não captura externa**. (Neste ambiente o egress p/ `.gov.br` é bloqueado; usar o Drive como fonte.)
- IDs das 14: 10235-1986, 10365-1987, 11152-1991, 11338-1992, 12350-1997, 13250-2001, 13475-2002, 14865-2008, 15044-2009, 16050-2014, 17202-2019, 17577-2021, 17759-2022, 17844-2022.

### P3 — Decidir/segregar os 2 itens fora de escopo (decisão MOU)
- `stf-tema-1020` (é ISS, não IPTU) → realocar para corpus ISS ou remover. `stj-resp-1658054` (previdenciário; nº do REsp NÃO verificado) → confirmar o número ou arquivar como ponto cego. Ambos já sinalizados no MANIFESTO; falta a decisão.

### P4 — Decisão do MOU: por qual base começar — IPTU ou TDC (D-PU-3)
- Define a ordem do pipeline e onde concentrar ground-truth. Recomendação do escritório: a de maior volume/urgência (o MOU define).

### P5 — Avançar a esteira (trabalho dos Gens — AFINAR, só após P1–P2)
- Fatiamento estrutural (`bruto/tagueado → fatiado → indexado`): chunking por dispositivo (CLAUDE.md 2.5), popular `rag/chunks` + `rag/index`.
- Criar os schemas dos 4 artefatos + geo + rag no Supabase (só após organização aprovada, RO-23) e estender `consolidar.yml` p/ índice RAG + mestres de tese.
- Engines determinísticos (IPTU progressivo, valuation TDC) — número nasce no engine (1.3).

### P6 — Segurança Supabase (decisão MOU)
- Advisory: RLS off em `public.spatial_ref_sys` (tabela de sistema PostGIS, sem dado). Habilitar sem policy quebra PostGIS. Decisão do operador; se habilitar, criar policy de leitura.

### P7 — Escritório: ratificar o D73 (cross-repo, não-clicável aqui)
- No repo `escritorio-do-mou`, branch da sessão: depósito `caixa-de-entrada/20260620_maestro_D73-e-auditoria-triplo-limpo.md` traz os trechos prontos para oficializar o D73 em `ESTADO_IMPLANTACAO.md`, `AGENDA_MOU.md` e portar os hooks ao template de entrada. Aplicar quando a instância-maestro com a "caneta" assumir.

## Mapa de arquivos-chave (pontos de entrada)
- `MANIFESTO.json` (estado) · `scripts/consolidar.py` · `.github/workflows/consolidar.yml`
- `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md` (o que mudou e por quê)
- `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md` + `Sanear-Duplicatas-PotencialUrbano.gs`
- `HANDOFF-E-PENDENCIAS.md` · `CODEX-DO-PROJETO.md §ESTADO` · `DO_ESCRITORIO.md` (canal do escritório)
