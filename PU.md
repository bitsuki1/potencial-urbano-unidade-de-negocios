# PU — Auditoria consolidada do Potencial Urbano (2026-06-20)

> Arquivo de auditoria nomeado **PU** (pedido do MOU). Ponto de entrada único da auditoria da sessão.
> **Zero-síntese.** Estado real canônico = `MANIFESTO.json` (números abaixo são medidos, não declarados).
> Detalhe por tema: `docs/AUDITORIA-PROFUNDA-2026-06-20.md` (1ª) · `docs/AUDITORIA-PROFUNDA-2-2026-06-20.md`
> (2ª) · `docs/AUDITORIA-FECHAMENTO-SESSAO-2026-06-20.md` (3ª) · `docs/RELATORIO-FINAL-SESSAO-2026-06-20.md`.
> Em divergência de número, vale o `MANIFESTO.json` + `python3 scripts/fechar-instancia.py`.

---

> **★ SUPERADO EM PARTE (2026-06-27).** Este laudo é de 2026-06-20. Mudou desde então: as contagens abaixo
> ("13 indexado", "1.246 chunks") estão **stale** — hoje são **17 leis / 1.571 chunks** (B-15 indexou as 4 IPTU;
> número vivo = `MANIFESTO.json`). O "**PRODUTO a ~0% / `tabelas/` vazio**" continua verdade NO MAIN, mas: (a) TDC
> foi **destravado no main** (consulta cita LPUOS 16.402 Art. 24); (b) o produto pleno (tabelas reais + E5) está
> **pronto e preso** na branch `project-audit-roadmap-2thi1g` (B-17, cross-repo). Estado canônico atual:
> `docs/AUDITORIA-PROFUNDA-2026-06-27.md` + `MANIFESTO.json` + `BACKLOG.md`.

## 0. VEREDITO (uma linha, honesto)
A **infraestrutura** (RAG + engine + anti-perda + decisões + beta) está **construída, auditada 3× e VERDE**;
o **PRODUTO** (lista de alvos por imóvel = o que dá dinheiro) está **a ~0%**; a **propagação ao escritório**
depende do maestro (3 depósitos não consumidos + 1 risco não-diferível parado).

## 1. AUDITORIA PROFUNDA — estado medido
- **Gate de fechamento VERDE** (`fechar-instancia.py` exit 0): evals 8/8 ativos · engine ok · sem stray tags ·
  MANIFESTO idempotente vs HEAD · backlog fresco.
- **Corpus:** `por_status_pipeline_ativos` = **{indexado: 13, bruto: 14, tagueado: 30}** · 59 itens · **1.246 chunks**.
- **Sync:** PU **0/0** · escritório **0/0** · 3 depósitos na caixa.
- **3 auditorias profundas** (lentes diferentes, D82) + **2 verificadores independentes** confirmaram: 8 furos
  de gate/CI (F-1..F-8) FECHADOS sob sabotagem; sem regressão; PU consistente.
- **Defeito mais grave (honestidade):** o "ladrão" que EU construí dava **FALSO-VERDE** — pego pela 2ª
  auditoria (lente diferente), corrigido (piso de evals ATIVOS), re-verificado por agente independente.

## 2. AUDITORIA DE DECISÕES (`CODEX §5` D-01..D-12) — cada uma × o código
**Zero contradições. Todas batem (verificado executável):**
| D | Confere? | Evidência |
|---|---|---|
| D-01..D-04 (pré-sessão) | ✅ vigentes | inteligência no engine · porta por endereço · oficialidade · nenhuma matriz canônica |
| D-05 RAG determinístico | ✅ | BM25 em `consultar/indexar`; 0 embeddings |
| D-06 guarda de verbatim | ✅ | 5 guardas em `fatiar.py` |
| D-07 re-ingestão interna | ✅ | `promover_entrada.py`; 13 indexadas |
| D-08 número no engine, não inventa | ✅ | `Decimal("0.5")` = **0 ocorrências** (HMP removido) |
| D-09 ladrão | ✅ | BACKLOG+hook+gate verde |
| D-10 gate ≠ verde com evals vazia | ✅ | `MIN_ITENS_ATIVOS` provado (flip→aguardando = VERMELHO) |
| D-11 decimal-BR + guardas + sufixo | ✅ | `_d('1,5')`=1.5 · `fp<0` levanta · regex `(\d+(?:-[A-Z])?)` |
| D-12 auditar com lente DIFERENTE | ✅ | aplicado 3× · reflete no BETA §3 |
CODEX unificado **v0.5**. Decisões subsumidas (não-críticas): BM25-vs-TF e gate-de-cobertura em D-05.

## 3. AUDITORIA DE BETA-CONTÍNUO (`BETA-CONTINUO.md`)
- **Completo (§3):** esteira RAG · promotor de verbatim · engine-como-código · ladrão · auditoria por lentes diferentes.
- **Consistente com o SSOT:** a vacina "lente DIFERENTE" do BETA tem o D-12 correspondente no CODEX.
- **§4 Supabase ainda VERDADEIRO** (MCP): só `governanca` (`de_para`=0, `registro_decisoes`=0) + `public`/PostGIS;
  4 artefatos+geo+rag NÃO criados (RO-23).

## 4. AUDITORIA COMPLETA — o que funciona E o que NÃO (honestidade total)
**FUNCIONA (provado):** RAG fim-a-fim com citação (1.7) · 13 leis verbatim · engine TDC determinístico (1.3)
auto-testado · anti-perda com gate honesto · CI que testa antes de publicar · 12 decisões rastreáveis · doutrina 1.1–1.7 intacta.

**NÃO está pronto / NÃO funciona:**
1. **PRODUTO a ~0%** — lista de alvos por imóvel (IPTU 2026 × dono × ITBI × valor) não existe; `tabelas/` vazio (B-1/B-2).
2. **Chunker: 280 rótulos duplicados** (redação compilada) — vigência-por-chunk pendente (B-11); o sufixo "-A/-B" já foi corrigido.
3. **Engine sem combustível:** `V`/`CA_max` (Q14/Quadro 3) no Drive, não ingeridos (B-1).
4. **14 das 15 municipais não-verbatim** (B-4, Drive).
5. **MAESTRO não consumiu nada:** 3 depósitos só na branch; `MAPA-DA-UNIDADE` do portfólio mostra o PU pré-sessão.
6. **Risco NÃO-DIFERÍVEL parado:** AUD-02 — IDs canônicos do Drive trocados (DELETE errado de ~3 GB).
7. **Depósitos ficaram stale 2× na sessão** (corrigido com #2 e #3) — F1 batendo no próprio trabalho.

## 5. O QUE A PRÓXIMA INSTÂNCIA FAZ (com DoD em `BACKLOG.md`)
- **Destrave de VALOR:** B-1 (tabelas Q14/Quadro 3 → engine dá número real → 1ª lista de alvos) — depende do Drive.
- **Dívidas de qualidade (caneta no projeto):** B-11 (vigência-por-chunk), B-12 (DECIMAL-total/citação-artigo), B-5/B-6 (semântica/remissões), B-7, B-10.
- **Só o maestro:** triar os 3 depósitos · relayar AUD-02 + pedido ao Drive · atualizar `MAPA-DA-UNIDADE`/`DO_ESCRITORIO`.

## 6. ÍNDICE DE TUDO (nada se perde)
**Código:** `scripts/{fatiar,indexar,consultar,_texto,consolidar,promover_entrada,fechar-instancia}.py` · `engines/tdc/oodc.py`.
**Corpus:** `leis/federal/`(12) + `leis/municipal-sp/7228` verbatim · `rag/chunks/`(1.246) · `rag/index/`.
**Estado:** `MANIFESTO.json` · `BACKLOG.md`(B-1..B-14) · `PROXIMA-INSTANCIA.md` · `HANDOFF-E-PENDENCIAS.md`.
**Decisões/beta:** `CODEX-DO-PROJETO.md §5`(D-01..D-12, v0.5) · `BETA-CONTINUO.md`.
**Auditorias:** os 4 docs em `docs/` (ver cabeçalho) + este `PU.md`.
**Depósitos (escritório, branch `claude/potencial-urbano-setup-t8irkf`):** `caixa-de-entrada/20260620_potencial-urbano_{auditoria-destraves-ladrao,ATUALIZACAO-2a-auditoria,FECHAMENTO-3a-auditoria}.md`.
