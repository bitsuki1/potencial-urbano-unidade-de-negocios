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
> **Estratégia de entregas (lente de loop de IA) que SEQUENCIA estas ABERTAS em ondas:** `ESTRATEGIA-DE-ENTREGAS-PU.md`
> (PU 15, 2026-07-01). Separa **Classe LOCAL** — o loop de IA destrava sozinho, roda já: B-3·B-5·B-6·B-7·B-10·B-11c·B-12 —
> da **Classe EXTERNA** — pedido único ao MOU: B-1·B-2·B-4·B-9·B-17 + dado pesado/geo/FUNDURB/despausar-preço.
> **Substância das ABERTAS INALTERADA** (esta linha só as agrupa por quem destrava).
> **Atualizado: 2026-07-01** (PU 15 — estratégia de entregas; ABERTAS reconferidas, substância INALTERADA). _Histórico: 2026-06-28 regularização do Escritório; 2026-06-27 auditoria profunda (B-15..B-19, `docs/AUDITORIA-PROFUNDA-2026-06-27.md`)._

## 🔴 ABERTAS

> **★ PAGOS nesta sessão (2026-06-27, pague-tudo):** B-15 ✅ (indexei de verdade as 4 IPTU → 17 leis/1.571
> chunks; "indexado" virou prova), B-16 ✅ (MANIFESTO honesto), B-18 ✅ (gates concordam), B-19 ✅ (hook não
> suja/duplica), B-12(c/d) ✅ (FATAL + citação por dispositivo) — ver rastro. **Destrave de bônus:** indexar a
> LPUOS 16.402 ligou TDC no main (eval `tdc-potencial-construtivo-lpuos` verde). **ABERTOS:** B-17 (produto
> preso na branch — cross-repo/MOU), B-11(c) (vigência-por-chunk), e os dependentes de Drive (B-1..B-4, B-9).

| # | Item | DoD (como PROVAR que foi feito) | Bloqueio |
|---|---|---|---|
| **B-17** 🟥 | **Consolidar o PRODUTO preso na branch `project-audit-roadmap-2thi1g`** ao main (B-1 fechado, TDC verbatim 19×13, engine sobre dado real, E5 provado — ~742 arquivos). | PR `project-audit-roadmap` → main MERGE (resolver conflito leis 16.050/17.844 = aceitar versão verbatim da branch); MANIFESTO regenerado; produto deixa de ser "0%" no SSOT. **Cross-repo: decisão do MOU** (main protegido) — depositado em `caixa-de-saida/para-escritorio/2026-06-27_*`. | escritório/MOU (PR a main protegido) |
| **B-1** 🟥 | **Ingerir as TABELAS Q14 + Quadro 3 → `tabelas/`** (combustível do engine; AUD-04). **[FEITO na branch órfã — ver B-17; falta chegar ao main.]** | `tabelas/q14-*.csv` e `tabelas/quadro3-ca-*.csv` no git, com proveniência; `engines/tdc/oodc.py` rodando sobre `V` (por SQL) e `CA_max` (por ZONA) REAIS de ≥1 imóvel — sem valores ilustrativos. | Drive (Q14/Quadro 3 lá; pedir via B-9) — **ou consolidar B-17** |
| **B-2** 🟥 | **1º JOIN do PRODUTO** — `IPTU_2026` (1 distrito) ⋈ LOTES (SQL/geo) ⋈ Q14 (valor) ⋈ zoneamento (CA) → engine → **1ª lista de alvos por imóvel**. | script de cruzamento (`engines/` ou `scripts/`) + saída com ≥N imóveis reais {SQL, valor, oportunidade TDC/IPTU, dono} no git (recorte leve) ou no Supabase `governanca` (bruto pesado fora do git). | B-1 + dados pesados (Drive→Supabase) |
| **B-20** 🟥 | **Frente COMERCIAL — lista de cedentes ZEPEC + ferramenta.** Direção MOU 2026-06-28: AGNÓSTICO, sem preço. **MUITO FEITO (sessão PU 14):** 4 planilhas ZEPEC puxadas verbatim → base unificada `zepec/limpo/zepec_unificada.csv` (7.175 linhas, SQL_MESTRE/endereço/datas padronizados) → **ferramenta** `zepec/ferramenta/zepec_cedentes.csv` (6.131 imóveis: estado_venda·certeza·negociável·dono·m²·FUNDURB). **3 codexes** separados (Comercial/Cálculos/Precificação). **Engine cedente** `engines/tdc/pcpt.py` (2 vias, Art.125/127). **Escrutínio por agentes** (várias rodadas triplo-limpo) corrigiu bugs silenciosos (multi-lote, dono OODC, sensor liquidez invertido). | **Aberto:** (a) dono em escala = **Supabase ITBI/IPTU** (pesado, infra/MOU); (b) **Atc do IPTU** destrava o engine de preço (Codex Precificação, PARADO por ora); (c) **resolver SQL dos 1.791 sem cadastro** (geo); (d) **confirmar semântica FUNDURB** (teto/somatória) na fonte SMUL; (e) vias 2-6 de expansão (Quadro 7 parques já extraído: `tabelas/quadro7-parques.csv`, 147 propostos). | local: feito o grosso · Drive/Supabase: dono+Atc em escala (B-9) · fonte SMUL: semântica FUNDURB |
| **B-3** 🟥 | **Completar tabelas Fs/Fp no `oodc.py`** (hoje PARCIAIS, só F-A/V3.1). | `FATOR_SOCIAL`/`FATOR_PLANEJAMENTO` completos, cada faixa com citação do quadro-fonte; `_autoteste()` estendido cobrindo HIS/HMP/R e as faixas de Fp; gate verde. | B-1 (quadros) |
| **B-4** 🟦 | **Re-ingerir as 14 leis MUNICIPAIS em verbatim integral** (só resumo WebSearch hoje). | cada `.md` com `## Texto integral (verbatim)` + `.json confianca:alta` + fatiada/indexada; rodar `python3 scripts/promover_entrada.py <id>` quando o cru chegar a `_entrada/`. MANIFESTO: `indexado` sobe de 13. | cru NÃO está local — Drive (B-9) |
| **B-5** 🟦 | **Camada semântica (embeddings) + filtro por `tema`** no `consultar.py` (resolve a vacina *match lexical ≠ relevância semântica*). | consulta "direito de construir" deixa de citar Lei 4.591/1964 Art. 68 (match lexical) — ou recusa, ou cita o dispositivo TDC real; novo eval de "armadilha lexical" como gate. | nenhum (trabalho local) |
| **B-6** 🟦 | **Grafo de remissões / vigência por remissão** (limite declarado do tier keyword). | consulta "a partir de quando vale o art. 3?" cita o **Art. 11** (que fixa 1/jan/1969), não o Art. 3; eval do tipo data-por-remissão vira positivo. | nenhum (local) |
| **B-7** 🟦 | **Vigência municipal DATADA (1.6) + `verbatim_integral` — ✅ FEITO na parte LOCAL (PU 15, 2026-07-01).** ✅ `consolidar.py` deriva `verbatim_integral` do marcador do `.md` (19 verbatim) + resumo/alerta no MANIFESTO. ✅ 7.228/1968 datada por Art. 11 (`inicio:1968-12-12`; efeito Art. 3º→1969-01-01, que também alimenta B-6). ✅ **todas as 19 verbatim/indexadas agora têm `vigencia.inicio`** (alerta `indexado_verbatim_sem_vigencia_datada` = vazio). RESTA: datar as **13 municipais `bruto`** — depende do verbatim do Drive (B-4); datar de resumo = inventar. | 19 verbatim datadas (alerta vazio); consolidar populando `verbatim_integral`. Provado no MANIFESTO. | resíduo (13 municipais) = Drive (B-4) |
| **B-21** 🟦 | **Construir jurisprudência de TDC** (achado B-10: corpus é TDC-cego — 0/32 tratam de TDC, VERIFICADO, apesar de TDC ser a base prioritária do MOU). | capturar acórdãos/temas STF/STJ/TJSP sobre outorga onerosa / solo criado / potencial construtivo / TDC → `jurisprudencia/` verbatim + fatiado/indexado; ≥1 eval de tese TDC-jurisprudencial verde. | captura (egress .gov.br=403 / Drive) |
| **B-22** 🟨 | **Sincronizar notas de confiança `.md` ↔ `.json`** (achado B-10: vários `.md` mantêm "confiança média/confirmar" que o `.json` já resolveu via `verificacao_verbatim` — Tema 94/155, REsp 1202136/1645832; consumidor do RAG que lê só um subestima/superestima). | cada par com nota de confiança coerente entre `.md` e `.json`; sem regressão de eval. | nenhum (local) |
| **B-8** 🟨 | **AUD-02 — conflito de IDs canônicos do Drive ANTES de qualquer DELETE** (risco de perder ~3 GB). | docs antigos (`docs/PLANO-SANEAMENTO-E-DECISOES.md`, `docs/INVENTARIO-DRIVE-*.md`) marcados **SUPERADOS** por `SANEAMENTO-DUPLICATAS-2026-06-20`; antes do `DRY_RUN=false`, cada ID "manter" conferido por `get_file_metadata`. | lane do Drive (NÃO tocar — relayar via B-9) |
| **B-9** 🟨 | **PEDIDO AO DRIVE** consolidando o que depende do Drive: Q14+Quadro 3 (B-1), cru verbatim das 14 municipais (B-4), e o alerta AUD-02 (B-8). | arquivo de pedido depositado no canal do escritório para o MOU relayar à lane do Drive; referência cruzada anotada aqui. | canal: a definir com o MOU (cerca: `caixa-de-entrada/drive/**` é lane do Drive) |
| **B-10** ⬜ | **Auditar o MÉRITO JURÍDICO das teses — ✅ FEITO (PU 15, 2026-07-01).** Lente Gen Advogado revisou as 32 tema-a-tema (holding × uso × citação), com 6 fichas dialéticas (tese·antítese·vacina) e verificação adversarial (D-12) das 3 afirmações centrais. Laudo: `docs/AUDITORIA-MERITO-JURIDICO-B10-2026-07-01.md`. **Achados:** 27 SUSTENTAM · 2 stubs não-verificados (262/399, NÃO citar) · 2 fora-de-escopo confirmados. **Maior achado → B-21** (corpus é TDC-cego: 0/32 tratam de TDC, VERIFICADO). **Dessincronização .md/.json → B-22.** | — (resolvido; gerou B-21/B-22) | — |
| **B-11** 🟦 | **Chunker — ✅ (c) FEITO (PU 15, 2026-07-01); resta só (d).** ✅ (a) sufixo -A/-B; (b) guarda de redação entre aspas. ✅ **(c) VIGÊNCIA POR CHUNK (1.6):** `fatiar.py` marca cada dispositivo `revogado`/`compilado`/`original` (revogação INTEGRAL só quando abre "(Revogado ...)"/"Revogado pela Lei" — exclui a cláusula "Revogadas as disposições em contrário"); `indexar.py` carrega no metadado; `consultar.py` EXCLUI revogados por padrão (flag `--incluir-revogado` p/ consulta histórica, sempre flagada). **Defeito real corrigido:** PDE 16.050 Art. 148 (revogado pela Lei 17.975/2023) vinha no TOPO como vigente. RESTA (d): preâmbulo boilerplate → `tipo:"contexto-nao-citavel"`. | **Provado:** eval `vigencia-por-chunk.json` (2 itens ATIVOS verdes) — topo deixa de ser o Art. 148 revogado; compilado segue servido como vigente. | resíduo (d) = local |
| **B-12** 🟥 | **Engine — ✅ FECHADO (resíduo pago PU 15, 2026-07-01).** ✅ decimal BR + guardas Fp>0/Fs≥0; ✅ (c) trava FATAL; ✅ (d) citação por DISPOSITIVO. ✅ **(e) guarda DECIMAL(10,3) TOTAL — DECISÃO:** o `[10,3]` é a precisão do **UTXO** = m² de potencial (PC_pt/PC_r, fisicamente limitado); PC que estoura o tipo **LEVANTA** (`_q_utxo`). O **R$ da OODC é MONETÁRIO**, NÃO se sujeita ao teto (passa de 10^7 legítimo). | `_autoteste` verde: PC 10^7 LEVANTA · PC 9.999.999 ok · R$ OODC 25.000.000 calcula (não levanta). Provado. | — (resolvido) |
| **B-13** 🟨 | **Endurecer GATE/CI (2ª auditoria, F-3..F-8) — ✅ FEITO.** F-3 stray-tag scan estendido (evals/tabelas/tese/extracao + .csv); F-4 `check_pushed` + docstring de escopo honesto; F-5 regex do backlog ancorada ao header; F-6 CI roda evals+engine ANTES de commitar; F-7 `git diff HEAD`; F-8 wrapper do hook resiliente. | — (resolvido) | — |
| **B-14** 🟨 | **Dívida de propagação (2ª auditoria, Lente 4) — ✅ FEITO (PU).** `_PROCESSADOS.md` (→indexado), `HANDOFF:33` (→indexado), banners SUPERADO em ACIONABILIDADE/catalogo-README/CONSOLIDACAO, "15→14" em PROXIMA, +2 scripts no README, CODEX unificado v0.5. RESTA só o `DO_ESCRITORIO.md` ("15 municipais") — **doc do escritório**, sinalizado no depósito p/ o maestro. | — (resolvido no PU; DO_ESCRITORIO é do escritório) | — |

## ✅ RESOLVIDAS RECENTES (rastro)
- **2026-06-27 — pague-tudo (3 auditorias: profunda·beta·decisões).** Laudo `docs/AUDITORIA-PROFUNDA-2026-06-27.md`.
  **B-15** (rótulo `indexado` falso): indexei DE VERDADE as 4 leis IPTU (16402/16642/17733/decreto-57443) →
  17 leis / 1.571 chunks; **destrave de bônus:** LPUOS 16.402 ligou TDC no main (eval `tdc-potencial-construtivo-lpuos`
  verde, Art. 24 cobertura 86%). **NV-1:** `consolidar.py` deriva `indexado` do índice + alerta `indexado_sem_chunks`.
  **B-16:** MANIFESTO honesto (63 itens, 31 leis, indexado 17). **B-18:** `gate-fechamento.sh` checa idempotência
  do MANIFESTO (fim do falso-verde F-1; os dois gates concordam). **B-19 (H-1/H-2):** hook deduplica por branch
  em qualquer estado (não suja/duplica). **NV-2:** hook aborta auto-consolidação ao main se MANIFESTO não-idempotente.
  **B-12(c/d):** trava FATAL de gabarito em campo próprio + executada; citação por dispositivo (D-17). Decisões
  **D-13..D-17** lavradas no CODEX §5; §ESTADO e BETA-CONTINUO atualizados.
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
