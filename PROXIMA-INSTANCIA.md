# PRÓXIMA INSTÂNCIA — o que fazer (Potencial Urbano)

> **★ HANDOFF 2026-06-27 (2 acionamentos — PU 12).** Laudo: `docs/AUDITORIA-PROFUNDA-2026-06-27.md`.
> **Acionamento 1:** pacote de padronização do escritório (caixas v2, REGISTRO/ATA, D128, D119/D120, handoff)
> **consolidado ao `main`** (gate D141) + auditoria 3-lentes + depósito.
> **Acionamento 2 (3 auditorias + PAGUE-TUDO):** PAGOS com gate VERDE — **B-15** (indexei de verdade as 4 leis
> IPTU → **17 leis / 1.571 chunks**; `indexado` virou prova), **B-16** (MANIFESTO honesto), **B-18** (os 2 gates
> concordam), **B-19** (hook não suja/duplica), **B-12(c/d)** (trava FATAL + citação por dispositivo). **Destrave
> de bônus:** indexar a LPUOS 16.402 **ligou TDC no main** (eval `tdc-potencial-construtivo-lpuos` verde, Art. 24).
> Decisões **D-13..D-17** no CODEX §5. **Gate `fechar-instancia.py` = VERDE (exit 0).**
> **ABERTOS (próximos):** **B-17** (cross-repo/MOU — **produto pronto preso na branch `project-audit-roadmap-2thi1g`**:
> tabelas reais + engine sobre imóvel real + E5; PR ao main + conflito leis 16.050/17.844 → aceitar verbatim;
> depositado em `caixa-de-saida/para-escritorio/`); **B-11(c)** vigência-por-chunk; **B-1..B-4/B-9** (Drive).
> **Pauta MR-14 (frentes A/B/C/D):** deliberação respondida na caixa-de-saída — **aguarda o MOU consolidar**.
>
> **★ HANDOFF 2026-06-20 (fim da instância de auditoria):** 2 auditorias profundas rodadas. A 1ª
> destravou 12 federais verbatim + engine + ladrão. A **2ª** (`docs/AUDITORIA-PROFUNDA-2-2026-06-20.md`,
> 4 lentes: verbatim·engine·gates·propagação) auditou a superfície nova. Verdict: texto verbatim FIEL,
> matemática do engine CORRETA, mas 3 defeitos sérios — **2 corrigidos na hora** (gate dava FALSO-VERDE →
> piso de evals; engine inventava HMP=0,5 → removido) e o resto em **B-11..B-14** do `BACKLOG.md` com DoD.
> **Comece pelo `BACKLOG.md` (B-11 chunker/citação 1.7 e B-13 endurecer o gate são os mais urgentes).**
>
> **★ BACKLOG + "ladrão" anti-perda (D83, 2026-06-20):** o que falta executar vive em `BACKLOG.md`
> (cada item com DoD = prova mecânica), **surfaçado no boot** (`.claude/hooks/surface-backlog.sh`).
> **Ao fechar, rode `python3 scripts/fechar-instancia.py`** — o GATE mecânico ("declarei feito" ≠
> "provei feito"). Todo trabalho adiado entra no BACKLOG no mesmo instante, ou ele CAI na troca de instância.


> Handoff sem perdas — Escritório do MOU (PMO), 2026-06-20. Estado pós-auditoria triplo-limpo.
> Retome por aqui + `HANDOFF-E-PENDENCIAS.md` + `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md`.
> SSOT do estado de cada item = `MANIFESTO.json` (agora VIVO, gerado por `scripts/consolidar.py`).
> Doutrina: zero-compressão · dialético · agnosticismo · nada se descarta. Não AFINAR sem destravar.

## Estado em 2026-06-20 (verificado, pós-auditoria profunda)
- **Corpus:** 59 itens — 27 leis + 32 jurisprudências verbatim (`tagueado`). 57 no escopo + 2 fora. Das 27 leis: **13 `indexado`** (12 federais re-ingeridas VERBATIM de `_entrada/misto/` + a 7.228/1968 municipal) e **14 `bruto`** (municipais ainda só resumo WebSearch — ver P2). **1.246 dispositivos** em `rag/chunks/`.
- **★ AUDITORIA PROFUNDA (2026-06-20):** laudo dialético em `docs/AUDITORIA-PROFUNDA-2026-06-20.md` (4 lentes adversariais + Supabase vivo). 3 destraves EXECUTADOS (AUD-01 federais verbatim; AUD-04 remoção IRRF/Tema 1130; AUD-03/08/09 engine `engines/tdc/oodc.py`) + ~10 correções de código/corpus. Pendências CRÍTICAS abertas: **AUD-02** (IDs canônicos do Drive trocados — risco de DELETE errado, lane do Drive) e **AUD-03** (tabelas `tabelas/` vazias = combustível do engine).
- **Engine TDC:** `engines/tdc/oodc.py` — Fórmula Mestra (OODC/geração/recepção/travas) agora é CÓDIGO determinístico (1.3), auto-testado no CI. Falta `V`/`CA_max` (tabelas Q14/Quadro 3, ainda no Drive).
- **★ A ESTEIRA RAG EXISTE E FOI PROVADA FIM-A-FIM (2026-06-20).** Antes `rag/` estava a 0%. Agora há tubo determinístico: `scripts/fatiar.py` (chunking por dispositivo 2.5) → `scripts/indexar.py` (índice invertido BM25 + metadados 2.6) → `scripts/consultar.py` (retrieval híbrido com **citação obrigatória 1.7**, gate de cobertura para NÃO-FUNDAMENTADA) → `evals/rodar-evals.py` (gate = citação correta, Parte 3). **6/6 evals ATIVOS passam** sobre a Lei 7.228/1968; 3 evals de TDC ficam como spec `aguardando_verbatim` (ver P5). Sem LLM, sem embeddings, stdlib-only (1.3/1.4). Doc: `scripts/README.md`.
- **MANIFESTO.json:** vivo e idempotente; Action `consolidar.yml` AGORA roda a cadeia inteira (fatiar→indexar→consolidar→**evals como gate**) a cada push, sem loop.
- **Supabase** `potencial-urbano-iptu-tdc` (`csnalylpvysjvejgsymr`, sa-east-1): só `governanca` (de_para, registro_decisoes — vazios) + `public`/PostGIS. Schemas dos artefatos NÃO criados (de propósito, RO-23).
- **Drive:** inventariado; ~16–20 GB de duplicatas mapeadas, executor de exclusão pronto (decisão MOU: EXCLUIR).

## PENDÊNCIAS (prioridade ↓)

> ★ **DESTRAVE-MESTRE — PARCIALMENTE FEITO (2026-06-20, instância orquestradora PU).** A fatia vertical foi construída: o **TUBO** (re-ingestão verbatim → fatiar → indexar → consultar com citação → eval) existe e foi **provado fim-a-fim** sobre a Lei 7.228/1968 (6/6 evals ATIVOS verdes). O que prova: o tubo funciona, é barato (determinístico) e já se sabe ONDE ele quebra (ver "Onde o tubo quebra" abaixo).
> **O QUE FALTA para a fatia ser de PRODUTO (TDC):** a 7.228/1968 é tributária-municipal (IPTU-adjacente), **não TDC** — foi a única lei com verbatim DISPONÍVEL no ambiente (`_entrada/misto/`). O corpus TDC (PDE 16.050/2014 etc.) segue **não-verbatim**, então a guarda-de-verbatim do `fatiar.py` corretamente o recusa. **Bloqueio real e único:** re-ingerir VERBATIM ≥1 norma de TDC. Egress p/ `.gov.br` = HTTP 403 e o Drive é lane exclusiva (cerca) → **esta instância não conseguiu obter verbatim TDC**. Assim que ele chegar, é rodar `fatiar`+`indexar` e os 3 evals `tdc-produto-pendente.json` viram o gate de aceite do produto — zero código novo.
> **Onde o tubo quebra (achados da prova):** (a) TF bruto deixa artigo longo mascarar o relevante → resolvido com **BM25**; (b) match genérico fundamentaria falso-positivo → resolvido com **gate de cobertura** (NÃO-FUNDAMENTADA <34%); (c) **limite declarado do tier keyword**: data-de-vigência por remissão entre artigos (ex.: "a partir de quando vale o art. 3?") exige **grafo de remissões / camada semântica** — extensão futura, vacina gravada em `evals/ground-truth/iptu-7228-1968.json`.
> **Ordem honesta (D26):** P2(verbatim TDC)→(roda o tubo, já pronto)→P5(engines/semântico) é o caminho de PRODUTO. **P1 (Drive), P3 (fora-escopo), P6 (RLS) são HIGIENE — rodam em paralelo, não bloqueiam, não lideram a fila.**

### P1 — Executar a exclusão das duplicatas no Drive (decisão MOU tomada: EXCLUIR)
- Rodar `drive-arrumacao/Sanear-Duplicatas-PotencialUrbano.gs` (Apps Script): `DRY_RUN=true` → conferir Logs → `DRY_RUN=false` → executa (lixeira, recuperável ~30d).
- **O MCP do Drive desta sessão NÃO apaga** — execução é 1 clique no Apps Script da conta do MOU. Mapa+ids: `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md`.
- VACINA: o script só apaga se a cópia canônica existir; Fase 2 só duplicata exata (nome+tamanho). Conferir que SIRGAS_SHP_LOTES (geometrias + `.prj`) ficou com ≥1 cópia.
- Depois: re-rodar o catálogo do Drive e atualizar `docs/INVENTARIO-DRIVE-*.md` (IDs sobreviventes; a árvore foi achatada — os docs de 2026-06-18 descrevem estrutura que não existe mais).

### P2 — Re-ingerir as LEIS em VERBATIM INTEGRAL (lacuna probatória — pré-requisito do RAG)
- **FEITO: 13 leis verbatim/indexadas** — `7228-1968` (municipal) + **12 federais** (re-ingeridas de `_entrada/misto/` via `scripts/promover_entrada.py`, destrave AUD-01). **Faltam 14 MUNICIPAIS** ainda `bruto`/não-verbatim (só resumo WebSearch); a guarda do `fatiar.py` as recusa até virarem verbatim. Para essas, o cru NÃO está local — precisa do Drive (ver abaixo). Use o MESMO `promover_entrada.py` quando o cru chegar a `_entrada/`.
- **Prioridade (D-PU-3 = TDC):** re-ingerir PRIMEIRO o corpus TDC verbatim (PDE 16.050/2014 e correlatas) — é o que destrava a fatia de PRODUTO (os 3 evals `tdc-produto-pendente.json` já esperam por ele). As demais municipais/federais vêm depois.
- Fonte: PDFs no Drive (catálogo `inventario/catalogo-juridico-drive.csv`) — **re-ingestão interna**. **MAS:** neste ambiente o egress p/ `.gov.br` deu 403 E o Drive é **lane exclusiva** (cerca anti-conflito) → para obter verbatim do Drive, **abrir pedido ao Drive** (`escritorio-do-mou/caixa-de-entrada/drive/PEDIDOS-AO-DRIVE.md`) OU rodar de ambiente com egress liberado. **Padrão de re-ingestão já provado:** salvar o cru em `_entrada/`, escrever `leis/<id>.md` com cabeçalho `## Texto integral (verbatim)` + `.json` `confianca:"alta"`, rodar `scripts/fatiar.py`.
- **Gatilho V-2:** ao re-ingerir em lote, avaliar Gemini (contexto grande) p/ enumerar/puxar os links do corpus do Drive de uma vez.
- IDs municipais (1 feita ✅, **14 a re-ingerir**): 7228-1968 ✅ · pendentes → 10235-1986, 10365-1987, 11152-1991, 11338-1992, 12350-1997, 13250-2001, 13475-2002, 14865-2008, 15044-2009, 16050-2014, 17202-2019, 17577-2021, 17759-2022, 17844-2022.

### P3 — Decidir/segregar os 2 itens fora de escopo (decisão MOU)
- `stf-tema-1020` (é ISS, não IPTU) → realocar para corpus ISS ou remover. `stj-resp-1658054` (previdenciário; nº do REsp NÃO verificado) → confirmar o número ou arquivar como ponto cego. Ambos já sinalizados no MANIFESTO; falta a decisão.

### P4 — Base inicial = TDC ✅ (decidido pelo MOU)
- **RESOLVIDO 2026-06-20:** o MOU confirmou **a base inicial é TDC**. O pipeline começa por TDC; o ground-truth e a validação concentram em TDC primeiro; IPTU vem depois (o pipeline replica). Encerra a divergência M-24/M-49. (D-PU-3 = TDC.)

### P5 — Avançar a esteira (trabalho dos Gens)
- [x] **Fatiamento estrutural + índice RAG + consulta com citação — FEITO** (`scripts/fatiar.py`, `indexar.py`, `consultar.py`, `evals/`). Chunking por dispositivo (2.5), retrieval híbrido (2.6), gate 1.7. `consolidar.yml` estendido p/ rodar a cadeia + evals como gate. Doc: `scripts/README.md`.
- [ ] **Replicar o tubo ao corpus TDC** assim que o verbatim chegar (P2): zero código novo — `fatiar`+`indexar`, e os evals `tdc-produto-pendente.json` viram aceite.
- [ ] **Camada semântica (embeddings) + grafo de remissões** — extensão plugável no mesmo índice; destrava perguntas que o keyword puro não resolve (vacina em `evals/ground-truth/iptu-7228-1968.json`).
- [ ] Criar os schemas dos 4 artefatos + geo + rag no Supabase (só após organização aprovada, RO-23) e estender `consolidar.yml` p/ mestres de tese.
- [ ] Engines determinísticos (IPTU progressivo, valuation TDC) — número nasce no engine (1.3).

### P6 — Segurança Supabase (ação física do MOU — não dá pra fazer por SQL)
- Advisory: `public.spatial_ref_sys` com RLS off (tabela de sistema do PostGIS, dado público).
- **CORREÇÃO 2026-06-20 (auditoria):** `ALTER TABLE ... ENABLE RLS` é **BLOQUEADO** — a tabela pertence ao `supabase_admin` e nós (e o SQL Editor do Studio) somos role `postgres` não-superuser. **NÃO é "habilitar RLS com policy".** O **fix real e limpo** (sem superuser): **Dashboard → Project Settings → API → Exposed schemas → remover `public`** (manter `graphql_public`; incluir `governanca` se o app consumir via REST). Todo o dado real do PU vive em `governanca` (RLS deny-all, 0 linhas), então tirar `public` da API fecha a porta sem perder nada. Cross-ref escritório **M-41** (passo a passo). As extensões PostGIS no `public` + `st_estimatedextent` (WARN) ficam intactas de propósito (mexer arrisca o geoprocessamento).

### P7 — Escritório: ratificar o D73 → ✅ FEITO (oficializado como D78)
- O escritório oficializou em produção: o D73 virou **D78** (renumerado por colisão), os hooks foram portados ao template de entrada, e o portfólio do PU foi reconciliado (corpus 59, Supabase próprio, D79 Drive=EXCLUIR, D80 entrada formal proposta). Nada pendente aqui do lado do escritório.

## Vacinas operacionais (recuperadas do chat — auditoria 2026-06-20)
- **V-1 — captura em LOTE que para no 1º item.** A extensão de captura do Drive/jurisprudência parava no primeiro item → capturas incompletas. Ao capturar em lote, CONFERIR que veio tudo, não só o 1º (casa com D24).
- **V-2 — Gemini (contexto grande) para enumerar/puxar os links do corpus inteiro do Drive.** Caminho cogitado e **adiado** — avaliar nesta unidade; não perder a ideia.
- **V-3 — a duplicação do Drive tem CAUSA-RAIZ: upload de máquinas diferentes.** Os ~16–20 GB vieram de uploads repetidos de máquinas distintas. Só excluir (P1/D79) não impede repetir: precisa de **ponto único de upload + dedup no momento do upload**.

## Pontos cegos DECLARADOS (auditoria da CONVERSA, 2026-06-20) — o que NÃO foi auditado
> Honestidade D24: declarar o que ficou de fora vale mais que fingir cobertura.
- **DIMENSÃO DADO/PRODUTO não auditada (a maior).** Todas as auditorias miraram o **corpus jurídico** (artefato Lei/RAG). **Tabela, Fórmula/engine e a base de imóveis ficaram quase intocadas.** O produto real (CODEX Fase 2/3) é cruzar **IPTU 2026 (~1M linhas) × proprietários × ITBI × SQL/endereço**. Os CSVs pesados (`socios`, `IPTU_2026`, `holdings`, série `ITBI`) — os mesmos cujas duplicatas o D79 vai apagar no Drive — **nunca foram auditados/ingeridos/validados**. 3 dos 4 artefatos seguem sem varredura.
- **OCR / legibilidade dos PDFs (gap no P2).** A re-ingestão verbatim das 27 leis assume PDFs de TEXTO. Não verificamos se os PDFs do Drive são texto ou IMAGEM. Se imagem, precisa OCR (RO-13) ANTES de re-ingerir — senão a "re-ingestão" traz lixo de novo.
- **V-2 (Gemini p/ corpus) — agora é TAREFA com gatilho:** ao ir re-ingerir as 27 leis, AVALIAR usar Gemini (contexto grande) para enumerar/puxar os links do corpus do Drive de uma vez. Dono: a instância que rodar o P2.

## Mapa de arquivos-chave (pontos de entrada)
- **Esteira RAG (NOVO 2026-06-20):** `scripts/README.md` (visão) · `scripts/fatiar.py` · `scripts/indexar.py` · `scripts/consultar.py` · `scripts/_texto.py` · `scripts/promover_entrada.py` (promove cru de `_entrada/`→verbatim) · `evals/rodar-evals.py` · `evals/ground-truth/*.json` · artefatos em `rag/chunks/` + `rag/index/`.
- **Engine TDC (NOVO 2026-06-20):** `engines/tdc/oodc.py` (OODC/geração/recepção/travas, determinístico) · `docs/AUDITORIA-PROFUNDA-2026-06-20.md` (laudo).
- `MANIFESTO.json` (estado) · `scripts/consolidar.py` · `.github/workflows/consolidar.yml`
- `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md` (o que mudou e por quê)
- `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md` + `Sanear-Duplicatas-PotencialUrbano.gs`
- `HANDOFF-E-PENDENCIAS.md` · `CODEX-DO-PROJETO.md §ESTADO` · `DO_ESCRITORIO.md` (canal do escritório)
