# Auditoria de FECHAMENTO da sessão — Potencial Urbano — 2026-06-20

> **Para a PRÓXIMA INSTÂNCIA: comece por aqui + `BACKLOG.md` + `PROXIMA-INSTANCIA.md`.**
> 3ª auditoria da sessão (triplo-limpo, RO-24), com lentes DIFERENTES das 2 anteriores (D82):
> (i) **conversa × documento** (feita pelo orquestrador, que viveu a conversa); (ii) **re-verificação
> adversarial do gate/CI** pós-correções; (iii) **completude do handoff/decisões/beta + estado do maestro**.
> Zero-síntese. Cada conciliação é provisória. Estado real canônico = `MANIFESTO.json`.

---

## 1. O QUE A SESSÃO FEZ (arco completo, na ordem — conversa × commits, nada perdido)
Sessão do **orquestrador do Potencial Urbano** (caneta no PROJETO; no escritório só DEPOSITA). 15 commits
no PU + 2 no escritório, todos pushados. Arco:

| # | Commit (PU) | O quê |
|---|---|---|
| 1 | `d4bab93` | **Esteira RAG** construída e provada fim-a-fim (`fatiar→indexar→consultar→evals`). `rag/` saiu de 0%. |
| 2 | `e679c1d` | **1ª auditoria profunda** (4 lentes: corpus·código·dado/produto·doutrina + Supabase vivo). 20 achados (AUD-01..20). |
| 3 | `f6a59c9` | **3 destraves:** 12 federais → verbatim/indexadas (`promover_entrada.py`); engine `oodc.py`; remoção IRRF/Tema 1130. |
| 4 | `ed63196` | CI regenerou MANIFESTO/índice (`[skip ci]`). |
| 5 | `f0bb2fb` | **"Ladrão"** (mecanismo anti-perda D83) adotado: `BACKLOG.md` + hook de boot + `fechar-instancia.py`. |
| 6 | `917977c` | Gate pegou na estreia uma não-idempotência (consolidar contava `.pyc`). |
| 7 | `1ca9077` | **BETA-CONTINUO + DECISÕES** D-05..D-09. |
| 8 | `622bde2` | **2ª auditoria profunda** (lentes diferentes) + corrige gate falso-verde + valor inventado. |
| 9 | `25f80fe` | **B-11..B-14** executados (chunker, engine, gate/CI, dívida de propagação). |
| + | (este doc) | **3ª auditoria (fechamento)** + D-10..D-12 + banner stale faltante. |

No escritório (branch `claude/potencial-urbano-setup-t8irkf`): `8199a2d` depósito #1, `f18d23c` depósito #2.

## 2. ESTADO ATUAL VERIFICADO (não declarado — medido)
- **Corpus:** 59 itens. `MANIFESTO.resumo.por_status_pipeline_ativos` = **{indexado: 13, bruto: 14, tagueado: 30}**.
  13 leis verbatim/indexadas (12 federais + 7.228/1968 municipal); **14 municipais** ainda só resumo (B-4);
  32 jurisprudências verbatim (30 em-escopo `tagueado` + 2 fora-de-escopo). **1.246 chunks** (`find rag/chunks -name '*.json'` = 1246, real).
- **Engine:** `engines/tdc/oodc.py` (OODC/geração/recepção/travas, determinístico, auto-teste no CI). `engines.arquivos=11`.
- **Ladrão:** `BACKLOG.md` (header `Atualizado: 2026-06-20`) + hook + `fechar-instancia.py` → **gate exit 0 (VERDE)**.
- **Scripts:** `_texto, consolidar, consultar, fatiar, fechar-instancia, indexar, promover_entrada` (7).
- **Sync:** PU e escritório **0/0** com origin. Sem stray tags no corpus.

## 3. RESULTADO DAS 2 RE-VERIFICAÇÕES INDEPENDENTES (lentes ii e iii)
**Lente ii — gate/CI sob teste adversarial (cópia /tmp, repo restaurado):** os **8 furos F-1..F-8 estão
FECHADOS**, comprovado: rebaixar/deletar o ground-truth ativo ou zerar o índice → gate VERMELHO (piso de
evals ATIVOS); stray-tag pega ground-truth/tabelas/tese/csv; backlog-fresh ancorado ao header; CI roda
gates ANTES de commitar; manifesto vs HEAD; hook resiliente. **Sem regressão** da passada de 184 arquivos
(idempotente 2×; evals 8/8; engine ok). B-11/B-12 parciais batem (156-A correto; dups 409→280; `_d('1,5')`=1.5).

**Lente iii — completude/handoff:** estado interno do PU **consistente** e os 3 docs de estado + MANIFESTO
**concordam** nos números. A próxima instância do PU **entra bem**. Os problemas estão na PROPAGAÇÃO ao
escritório e no registro de decisões — corrigidos abaixo (§4) ou endereçados ao maestro (§5).

## 4. ACHADOS DA 3ª AUDITORIA E O QUE FOI CORRIGIDO AGORA
- **A-4/A-5 (F6 — decisão sem registro) → CORRIGIDO:** as decisões das correções não eram D-NN. Lavrados
  **D-10** (gate não passa verde com evals esvaziada — a vacina do falso-verde), **D-11** (decimal-BR +
  guardas no engine; sufixo/aspas no chunker), **D-12** (RO-24 reforçado: auditar com lente DIFERENTE).
- **A-6 (resíduo stale que o B-14 perdeu) → CORRIGIDO:** banner SUPERADO em `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md`
  (dizia "NENHUMA das 27 verbatim / 15 municipais"). **Vacina:** dívida de propagação varre-se por `grep`
  mecânico de TODOS os docs, não pelos que vêm à memória (foi exatamente o que o B-14 falhou).
- **Verificação mecânica final:** nenhuma afirmação stale VIVA resta no PU (todas sob banner/antítese/nota).

## 5. PENDÊNCIAS — o que a PRÓXIMA INSTÂNCIA faz (com DoD em `BACKLOG.md`)
### No PROJETO (tem a caneta):
- **B-11(c)/(d)** — vigência POR CHUNK no texto compilado (os 280 rótulos duplicados restantes = redação
  "Redação dada/Revogado"; 1.6) + preâmbulo boilerplate `não-citável`. **B-12** — guarda DECIMAL(10,3)
  total + FATAL_ERROR em campo próprio + citação por DISPOSITIVO.
- **B-5/B-6** — camada semântica (embeddings) + filtro por tema (resolve "direito de construir" → Lei 4.591);
  grafo de remissões. **B-7** — vigência municipal datada + flag `verbatim_integral`. **B-10** — mérito jurídico.
### Bloqueado no DRIVE (precisa do maestro relayar):
- **B-1** Q14/Quadro 3 (combustível do engine) · **B-4** cru das 14 municipais · **B-2/B-3** produto/tabelas.
### NÃO-DIFERÍVEL (risco) — só o maestro/Drive:
- **B-8 / AUD-02** — IDs canônicos do Drive TROCADOS entre 2 planos de saneamento (risco de DELETE errado, ~3 GB).

## 6. ESTADO DO MAESTRO / CAIXA (verificado em origin/main) — ELE AINDA NÃO FEZ
- **Os 2 depósitos NÃO foram consumidos:** existem só na branch `claude/potencial-urbano-setup-t8irkf`, **não em
  `origin/main`**; `caixa-de-entrada/processados/` sem entrada do PU. (Assíncrono por desenho D39/D40 — esperado.)
- **`portfolio/potencial-urbano/MAPA-DA-UNIDADE.md` (origin/main) está STALE** (pré-sessão: "27 bruto, 15
  municipais, RAG não existe") — só atualiza quando o maestro triar.
- **Depósito #2 ficou STALE** (diz "B-13/B-14 EM ABERTO", mas foram FEITOS no `25f80fe`). → **corrigido com o
  depósito #3** (`...FECHAMENTO-3a-auditoria.md`) nesta passada.
- **Para o maestro (relay):** consumir os 3 depósitos · relayar AUD-02 (§A) + pedido ao Drive (§B) ·
  atualizar `MAPA-DA-UNIDADE.md` e `DO_ESCRITORIO.md` ("15"→"14 municipais").

## 7. DOUTRINA / DECISÕES / BETA (estado de fechamento)
- **Decisões:** `CODEX-DO-PROJETO.md §5` = **D-01..D-12** (D-05..D-09 da sessão; D-10..D-12 desta auditoria). CODEX unificado **v0.5**.
- **Beta-contínuo:** `BETA-CONTINUO.md §3` tem os protocolos reutilizáveis (esteira RAG · promotor de verbatim ·
  engine-como-código · ladrão · auditoria por lentes diferentes). Cross-pollination depositada ao escritório.
- **Vacinas vivas:** "Tema 1130 IRRF ≠ PU" · "número nasce no engine (1.3)" · "citação obrigatória (1.7)" ·
  "um `.md` dizer 403 ≠ verbatim inexistente" (D-07) · "match lexical ≠ semântico" · "gate verde ≠ tudo certo" (D-10) ·
  "auditar com lente DIFERENTE" (D-12) · "dívida de propagação varre-se por grep, não por memória" (A-6).
- **Princípios 1.1–1.7:** nenhum violado pelo estado final (os defeitos achados foram corrigidos ou backlogados com DoD).
