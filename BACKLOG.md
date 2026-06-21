# BACKLOG — Potencial Urbano (determinações em aberto)

> **O "ladrão" do escritório aplicado aqui (mecanismo D83, importado em 2026-06-20).** Metáfora do
> MOU: o *ladrão* (extravasor da caixa d'água) captura o que escaparia. O modo de falha nº1 é
> *"uma instância recebe uma determinação, adia para 'a próxima janela', e ela CAI"* — some num
> registro que ninguém relê no boot. Este arquivo é a **fonte única do que falta executar no PU**,
> **surfaçado no boot** (`.claude/hooks/surface-backlog.sh`) e validado no fechamento
> (`python3 scripts/fechar-instancia.py` — GATE mecânico: *"declarei feito" ≠ "provei feito"*).
>
> **REGRA:** todo item adiado entra AQUI no mesmo instante, com uma **DoD (Definition of Done) =
> como PROVAR que foi feito** (mecânica, não "achei que fechei"). Resolvido → move para o rastro com
> a data. Se esta lista estiver desatualizada, o mecanismo falhou — corrigir antes de seguir.
>
> Prioridade: 🟥 produto/valor · 🟦 corpus/RAG · 🟨 higiene/governança · ⬜ qualidade.
> **Atualizado: 2026-06-21.**

## 🔴 ABERTAS

| # | Item | DoD (como PROVAR que foi feito) | Bloqueio |
|---|---|---|---|
| **B-1** 🟥 | **Ingerir as TABELAS Q14 + Quadro 3 → `tabelas/`** (combustível do engine; AUD-04). | `tabelas/q14-*.csv` e `tabelas/quadro3-ca-*.csv` no git, com proveniência; `engines/tdc/oodc.py` rodando sobre `V` (por SQL) e `CA_max` (por ZONA) REAIS de ≥1 imóvel — sem valores ilustrativos. | Drive (Q14/Quadro 3 lá; pedir via B-9) |
| **B-2** 🟥 | **1º JOIN do PRODUTO** — `IPTU_2026` (1 distrito) ⋈ LOTES (SQL/geo) ⋈ Q14 (valor) ⋈ zoneamento (CA) → engine → **1ª lista de alvos por imóvel**. | script de cruzamento (`engines/` ou `scripts/`) + saída com ≥N imóveis reais {SQL, valor, oportunidade TDC/IPTU, dono} no git (recorte leve) ou no Supabase `governanca` (bruto pesado fora do git). | B-1 + dados pesados (Drive→Supabase) |
| **B-3** 🟥 | **Completar tabelas Fs/Fp no `oodc.py`** (hoje PARCIAIS, só F-A/V3.1). | `FATOR_SOCIAL`/`FATOR_PLANEJAMENTO` completos, cada faixa com citação do quadro-fonte; `_autoteste()` estendido cobrindo HIS/HMP/R e as faixas de Fp; gate verde. | B-1 (quadros) |
| **B-4** 🟦 | **Re-ingerir as 14 leis MUNICIPAIS em verbatim integral** (só resumo WebSearch hoje). | cada `.md` com `## Texto integral (verbatim)` + `.json confianca:alta` + fatiada/indexada; rodar `python3 scripts/promover_entrada.py <id>` quando o cru chegar a `_entrada/`. MANIFESTO: `indexado` sobe de 13. | cru NÃO está local — Drive (B-9) |
| **B-5** 🟦 | **Camada semântica (embeddings) + filtro por `tema`** no `consultar.py` (resolve a vacina *match lexical ≠ relevância semântica*). | consulta "direito de construir" deixa de citar Lei 4.591/1964 Art. 68 (match lexical) — ou recusa, ou cita o dispositivo TDC real; novo eval de "armadilha lexical" como gate. | nenhum (trabalho local) |
| **B-6** 🟦 | **Grafo de remissões / vigência por remissão** (limite declarado do tier keyword). | consulta "a partir de quando vale o art. 3?" cita o **Art. 11** (que fixa 1/jan/1969), não o Art. 3; eval do tipo data-por-remissão vira positivo. | nenhum (local) |
| **B-7** 🟦 | **Vigência municipal DATADA (1.6) + campo `verbatim_integral` no schema/MANIFESTO** (AUD-07/AUD-17). | 15 municipais com `vigencia.inicio` (e `fim/revogada_por` na cadeia 12.350/1997←17.844/2022); `consolidar.py` populando `verbatim_integral:true/false` pelo marcador do `.md`. | nenhum (local) |
| **B-8** 🟨 | **AUD-02 — conflito de IDs canônicos do Drive ANTES de qualquer DELETE** (risco de perder ~3 GB). | docs antigos (`docs/PLANO-SANEAMENTO-E-DECISOES.md`, `docs/INVENTARIO-DRIVE-*.md`) marcados **SUPERADOS** por `SANEAMENTO-DUPLICATAS-2026-06-20`; antes do `DRY_RUN=false`, cada ID "manter" conferido por `get_file_metadata`. | lane do Drive (NÃO tocar — relayar via B-9) |
| **B-9** 🟨 | **PEDIDO AO DRIVE** consolidando o que depende do Drive: Q14+Quadro 3 (B-1), cru verbatim das 14 municipais (B-4), e o alerta AUD-02 (B-8). | arquivo de pedido depositado no canal do escritório para o MOU relayar à lane do Drive; referência cruzada anotada aqui. | canal: a definir com o MOU (cerca: `caixa-de-entrada/drive/**` é lane do Drive) |
| **B-10** ⬜ | **Auditar o MÉRITO JURÍDICO das teses** (ponto cego DECLARADO da auditoria profunda — só proveniência/fidelidade foi auditada, não o conteúdo jurídico). | revisão tema-a-tema das 32 jurisprudências + leis-chave, com citação verificada e registro dialético; vacinas gravadas. | nenhum (precisa de tempo/expertise) |
| **B-11** 🟦 | **Chunker (2ª auditoria, L1) — PARCIAL.** ✅ (a) sufixo `(\d+(?:-[A-Z])?)` capturado + (b-parcial) guarda de redação entre aspas — "Art. 156-A" agora rotula certo; rótulos duplicados 409→**280**. RESTA: (c) **vigência POR CHUNK** em texto compilado (redação "Redação dada por"/"Revogado" — os 280 restantes; 1.6) e (d) preâmbulo com boilerplate → `tipo:"contexto-nao-citavel"`. | os 280 rótulos duplicados restantes (redação compilada) marcados por vigência (vigente/revogado); `consultar.py` não devolve redação revogada como vigente; eval de redação-compilada. | nenhum (local) |
| **B-12** 🟥 | **Engine (2ª auditoria, E-03..E-07) — PARCIAL.** ✅ decimal BR em `_d` ("1,5"→1.5) + guardas Fp>0/Fs≥0 + docstring corrigido + testes. RESTA: guarda de DECIMAL(10,3) TOTAL (decidir se aplica ao R$ OODC ou só ao m² PC — `precision_decimal_utxo`); separar a trava FATAL_ERROR (COMAER/CONPRESP) num campo próprio; citação por DISPOSITIVO (art. 128 PDE), não pela lei inteira. | OODC que estoura o tipo decidido LEVANTA; FATAL em campo próprio; citação aponta artigo. | parcialmente B-1 |
| **B-13** 🟨 | **Endurecer GATE/CI (2ª auditoria, F-3..F-8) — ✅ FEITO.** F-3 stray-tag scan estendido (evals/tabelas/tese/extracao + .csv); F-4 `check_pushed` + docstring de escopo honesto; F-5 regex do backlog ancorada ao header; F-6 CI roda evals+engine ANTES de commitar; F-7 `git diff HEAD`; F-8 wrapper do hook resiliente. | — (resolvido) | — |
| **B-14** 🟨 | **Dívida de propagação (2ª auditoria, Lente 4) — ✅ FEITO (PU).** `_PROCESSADOS.md` (→indexado), `HANDOFF:33` (→indexado), banners SUPERADO em ACIONABILIDADE/catalogo-README/CONSOLIDACAO, "15→14" em PROXIMA, +2 scripts no README, CODEX unificado v0.5. RESTA só o `DO_ESCRITORIO.md` ("15 municipais") — **doc do escritório**, sinalizado no depósito p/ o maestro. | — (resolvido no PU; DO_ESCRITORIO é do escritório) | — |

## ✅ RESOLVIDAS RECENTES (rastro)
- **2026-06-20 — 3ª auditoria (FECHAMENTO da sessão).** `docs/AUDITORIA-FECHAMENTO-SESSAO-2026-06-20.md` + 2 verificadores independentes (gate/CI sob teste adversarial = 8 furos F-1..F-8 FECHADOS, sem regressão; completude = PU consistente, gate verde). Lavrados **D-10..D-12** no CODEX (fecha o F6 — decisão sem registro); banner SUPERADO no doc stale que o B-14 perdeu (A-6); **depósito #3** ao escritório corrige o #2 stale. Pendência só do maestro (triar/relayar Drive/atualizar MAPA).
- **2026-06-20 — 2ª auditoria + correções (eu tenho a caneta no projeto).** Laudo `docs/AUDITORIA-PROFUNDA-2-2026-06-20.md`. Corrigidos: gate falso-verde (F-1/F-2, piso de evals ATIVOS); valor inventado HMP=0,5; **B-13 inteiro** (gate/CI endurecido); **B-14 inteiro** (8 docs stale saneados, exceto DO_ESCRITORIO=escritório); **B-11 parcial** (sufixo -A/-B + redação-aspas; 409→280 dups); **B-12 parcial** (decimal BR + guardas de sinal). Resta: B-11(c/d) vigência-por-chunk + B-12 (decimal-total/FATAL/citação-dispositivo).
- **2026-06-20 — Esteira RAG construída e provada fim-a-fim** (`scripts/fatiar+indexar+consultar`, evals, gate 1.7). `rag/` saiu de 0%.
- **2026-06-20 — 13 leis verbatim/indexadas** (12 federais via `promover_entrada.py` + 7.228/1968), 1.246 dispositivos. Destrave AUD-01.
- **2026-06-20 — Engine TDC vira código** (`engines/tdc/oodc.py`, determinístico, 1.3). Destrave AUD-03/08/09.
- **2026-06-20 — Material IRRF/Tema 1130 removido** (cumpre a vacina). Destrave AUD-04.
- **2026-06-20 — Auditoria profunda** (`docs/AUDITORIA-PROFUNDA-2026-06-20.md`, 4 lentes + Supabase vivo) + ~10 correções de código/corpus.

---
> **Ao FECHAR a sessão:** `python3 scripts/fechar-instancia.py` — o GATE mecânico. Sai 0 = verde (pode
> fechar). Sai 1 = pendência → resolva ANTES de declarar "fechado". E atualize a data acima + mova o
> que ficou pronto para o rastro. Estado completo: `PROXIMA-INSTANCIA.md` + `HANDOFF-E-PENDENCIAS.md`.
