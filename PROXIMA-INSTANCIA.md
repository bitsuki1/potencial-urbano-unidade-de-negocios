# PRÓXIMA INSTÂNCIA — o que fazer (Potencial Urbano)

> Handoff sem perdas — Escritório do MOU (PMO), 2026-06-20. Estado pós-auditoria triplo-limpo.
> Retome por aqui + `HANDOFF-E-PENDENCIAS.md` + `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md`.
> SSOT do estado de cada item = `MANIFESTO.json` (agora VIVO, gerado por `scripts/consolidar.py`).
> Doutrina: zero-compressão · dialético · agnosticismo · nada se descarta. Não AFINAR sem destravar.

## Estado em 2026-06-20 (verificado)
- **Corpus:** 59 itens — 27 leis (12 federais + 15 municipais, todas `bruto`; **articulado integral NÃO é verbatim** — ementa + dispositivo-chave + síntese, ver P2) + 32 jurisprudências verbatim (`tagueado`). 57 no escopo + 2 fora (`stf-tema-1020`=ISS, `stj-resp-1658054`=previdenciário).
- **MANIFESTO.json:** vivo e idempotente; Action `consolidar.yml` ligada (regenera a cada push, sem loop).
- **Supabase** `potencial-urbano-iptu-tdc` (`csnalylpvysjvejgsymr`, sa-east-1): só `governanca` (de_para, registro_decisoes — vazios) + `public`/PostGIS. Schemas dos artefatos NÃO criados (de propósito, RO-23).
- **Drive:** inventariado; ~16–20 GB de duplicatas mapeadas, executor de exclusão pronto (decisão MOU: EXCLUIR).

## PENDÊNCIAS (prioridade ↓)

> ★ **DESTRAVE-MESTRE (auditoria Acionabilidade 2026-06-20):** o FIM do projeto é "responder consulta jurídica COM CITAÇÃO" (1.7) e ele está a **0%** (`rag/` vazio). O passo que mais destrava NÃO é P1. É uma **FATIA VERTICAL FINA de TDC**: pegar **1 lei municipal-SP**, re-ingerir verbatim → fatiar por dispositivo → indexar → **responder 1 consulta TDC com citação** contra ground-truth. Prova o tubo inteiro barato, entrega o 1º valor de PRODUTO (não mais saneamento) e revela onde o tubo quebra antes de investir nas 27 leis.
> **Ordem honesta (D26):** P2→(fatia)→P5 é o caminho de PRODUTO. **P1 (Drive), P3 (fora-escopo), P6 (RLS) são HIGIENE — rodam em paralelo, não bloqueiam, não lideram a fila.**

### P1 — Executar a exclusão das duplicatas no Drive (decisão MOU tomada: EXCLUIR)
- Rodar `drive-arrumacao/Sanear-Duplicatas-PotencialUrbano.gs` (Apps Script): `DRY_RUN=true` → conferir Logs → `DRY_RUN=false` → executa (lixeira, recuperável ~30d).
- **O MCP do Drive desta sessão NÃO apaga** — execução é 1 clique no Apps Script da conta do MOU. Mapa+ids: `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md`.
- VACINA: o script só apaga se a cópia canônica existir; Fase 2 só duplicata exata (nome+tamanho). Conferir que SIRGAS_SHP_LOTES (geometrias + `.prj`) ficou com ≥1 cópia.
- Depois: re-rodar o catálogo do Drive e atualizar `docs/INVENTARIO-DRIVE-*.md` (IDs sobreviventes; a árvore foi achatada — os docs de 2026-06-18 descrevem estrutura que não existe mais).

### P2 — Re-ingerir as 27 LEIS em VERBATIM INTEGRAL (lacuna probatória — pré-requisito do RAG)
- **NENHUMA das 27 leis tem o articulado INTEGRAL verbatim** (planalto/espelhos deram HTTP 403): cada `.md` tem ementa + dispositivos-chave + síntese, com o aviso "Texto INTEGRAL não baixado". As 4 federais `confianca:alta` têm só o ARTIGO-CHAVE verbatim; o resto é síntese. (As 32 jurisprudências — súmulas/teses curtas — SIM são verbatim.) Re-ingerir o texto integral das **27 leis** (12 federais + 15 municipais) é pré-requisito para o RAG citar (Princípio 1.7/1.2). Ver `MANIFESTO.json` `alertas.itens_confianca_baixa_ou_media_a_revisar`.
- Fonte: os PDFs já estão no Drive (catalogo `inventario/catalogo-juridico-drive.csv`) — é **re-ingestão interna, não captura externa**. (Neste ambiente o egress p/ `.gov.br` é bloqueado; usar o Drive como fonte.) **Atalho p/ `7228-1968`:** o cru verbatim (~13,8 KB) já está em `_entrada/misto/lei-municipal-saopaulo-7228-1968.txt` — re-ingerir desse local, não precisa do Drive.
- IDs das 15: 7228-1968, 10235-1986, 10365-1987, 11152-1991, 11338-1992, 12350-1997, 13250-2001, 13475-2002, 14865-2008, 15044-2009, 16050-2014, 17202-2019, 17577-2021, 17759-2022, 17844-2022.

### P3 — Decidir/segregar os 2 itens fora de escopo (decisão MOU)
- `stf-tema-1020` (é ISS, não IPTU) → realocar para corpus ISS ou remover. `stj-resp-1658054` (previdenciário; nº do REsp NÃO verificado) → confirmar o número ou arquivar como ponto cego. Ambos já sinalizados no MANIFESTO; falta a decisão.

### P4 — Base inicial = TDC ✅ (decidido pelo MOU)
- **RESOLVIDO 2026-06-20:** o MOU confirmou **a base inicial é TDC**. O pipeline começa por TDC; o ground-truth e a validação concentram em TDC primeiro; IPTU vem depois (o pipeline replica). Encerra a divergência M-24/M-49. (D-PU-3 = TDC.)

### P5 — Avançar a esteira (trabalho dos Gens — AFINAR, só após P1–P2)
- Fatiamento estrutural (`bruto/tagueado → fatiado → indexado`): chunking por dispositivo (CLAUDE.md 2.5), popular `rag/chunks` + `rag/index`.
- Criar os schemas dos 4 artefatos + geo + rag no Supabase (só após organização aprovada, RO-23) e estender `consolidar.yml` p/ índice RAG + mestres de tese.
- Engines determinísticos (IPTU progressivo, valuation TDC) — número nasce no engine (1.3).

### P6 — Segurança Supabase (ação física do MOU — não dá pra fazer por SQL)
- Advisory: `public.spatial_ref_sys` com RLS off (tabela de sistema do PostGIS, dado público).
- **CORREÇÃO 2026-06-20 (auditoria):** `ALTER TABLE ... ENABLE RLS` é **BLOQUEADO** — a tabela pertence ao `supabase_admin` e nós (e o SQL Editor do Studio) somos role `postgres` não-superuser. **NÃO é "habilitar RLS com policy".** O **fix real e limpo** (sem superuser): **Dashboard → Project Settings → API → Exposed schemas → remover `public`** (manter `graphql_public`; incluir `governanca` se o app consumir via REST). Todo o dado real do PU vive em `governanca` (RLS deny-all, 0 linhas), então tirar `public` da API fecha a porta sem perder nada. Cross-ref escritório **M-41** (passo a passo). As extensões PostGIS no `public` + `st_estimatedextent` (WARN) ficam intactas de propósito (mexer arrisca o geoprocessamento).

### P7 — Escritório: ratificar o D73 → ✅ FEITO (oficializado como D78)
- O escritório oficializou em produção: o D73 virou **D78** (renumerado por colisão), os hooks foram portados ao template de entrada, e o portfólio do PU foi reconciliado (corpus 59, Supabase próprio, D79 Drive=EXCLUIR, D80 entrada formal proposta). Nada pendente aqui do lado do escritório.

## Vacinas operacionais (recuperadas do chat — auditoria 2026-06-20)
- **V-1 — captura em LOTE que para no 1º item.** A extensão de captura do Drive/jurisprudência parava no primeiro item → capturas incompletas. Ao capturar em lote, CONFERIR que veio tudo, não só o 1º (casa com D24).
- **V-2 — Gemini (contexto grande) para enumerar/puxar os links do corpus inteiro do Drive.** Caminho cogitado e **adiado** — avaliar nesta unidade; não perder a ideia.
- **V-3 — a duplicação do Drive tem CAUSA-RAIZ: upload de máquinas diferentes.** Os ~16–20 GB vieram de uploads repetidos de máquinas distintas. Só excluir (P1/D79) não impede repetir: precisa de **ponto único de upload + dedup no momento do upload**.

## Mapa de arquivos-chave (pontos de entrada)
- `MANIFESTO.json` (estado) · `scripts/consolidar.py` · `.github/workflows/consolidar.yml`
- `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md` (o que mudou e por quê)
- `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md` + `Sanear-Duplicatas-PotencialUrbano.gs`
- `HANDOFF-E-PENDENCIAS.md` · `CODEX-DO-PROJETO.md §ESTADO` · `DO_ESCRITORIO.md` (canal do escritório)
