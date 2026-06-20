# Auditoria triplo-limpo — fechamento (Potencial Urbano)

> Escritório do MOU (PMO) — 2026-06-20. Varredura de saturação (RO-24) em 4 lentes
> paralelas (corpus · docs · Drive · banco) + verificação determinística. Objetivo:
> deixar o registro **honesto e consistente** antes de avançar (D27/RO-23), sem AFINAR
> (o trabalho dos Gens). Tudo aqui é arrumação/saneamento.

## Lentes aplicadas
1. **Corpus** (`leis/` × `jurisprudencia/` × `_entrada/misto/` × `MANIFESTO.json`).
2. **Docs** (cruzamento de 19 documentos).
3. **Drive** (MCP single-level — inventário + duplicatas).
4. **Banco** (Supabase MCP — `list_tables`).

## Achados → ação (FEITO nesta auditoria)
| # | Achado | Severidade | Ação |
|---|---|---|---|
| 1 | `MANIFESTO.json` VAZIO (`itens: []`) — SSOT do estado mentindo por omissão; `consolidar.yml` nunca existiu | ALTA | **Criado `scripts/consolidar.py` + `.github/workflows/consolidar.yml`**; MANIFESTO regenerado (59 itens, vivo) |
| 2 | `status_pipeline: "processado"` em 32 jurisprudências = valor FORA do vocabulário canônico (`bruto→fatiado→tagueado→validado→indexado`) | ALTA | **Corrigido p/ `tagueado`** (tem metadados, ainda não indexado) nos 32 JSONs + nota no HANDOFF |
| 3 | 2 itens fora de escopo (`stf-tema-1020`=ISS, `stj-resp-1658054`=previdenciário) contavam como corpus IPTU | MÉDIA | **Segregados no MANIFESTO** (campo `fora_de_escopo` + `alertas`); contam à parte (57 no escopo, 2 fora) |
| 4 | `DO_ESCRITORIO.md` congelado em "tudo vazio (2026-06-18)" — falso após carga; violava o próprio PRINCÍPIO-DOCUMENTO-VIVO | CRÍTICA | **Tabela reescrita** como ponteiros (não cópia de estado volátil) + linha Supabase |
| 5 | Supabase: docs diziam "6 schemas / 4 artefatos + geo + governanca criados" — FALSO (só `governanca` + `public`) | ALTA | **Corrigido** em `CODEX §6/§ESTADO` e `BETA-CONTINUO §4` (VACINA datada) |
| 6 | Contradição "acervo COMPLETO, nenhuma captura" × "capturar 12+14 leis" | ALTA | **Conciliado**: fonte no Drive (ok) ≠ ingestão no repo; 12 federais já verbatim (upload MOU), 14 municipais ainda resumos a re-ingerir |
| 7 | `HANDOFF §3` "capturar 12 federais (não estão no despejo)" — stale (chegaram no upload) | MÉDIA | **Marcado FEITO** |
| 8 | `CONSOLIDACAO:19` "~40 leis" | BAIXA | **Corrigido p/ 27 (12+15)** |
| 9 | `extracao/gems/gen3-iptu.md` ≡ `gen3-governanca.md` (byte-idênticos, RO-19) | MÉDIA | **VACINA inline** apontando canônico (preservado, RO-09) |
| 10 | `_entrada/misto/` com 24 crus já processados (zona de despejo não contabilizada) | BAIXA | **Marker `_PROCESSADOS.md`** (cru→destino); preservados (são verbatim de proveniência; STF difere de `_capturas/`) |

## Achados → DEFERIDO (com motivo) — não executado aqui
| # | Achado | Por que não agora | Onde está pronto |
|---|---|---|---|
| D1 | **Saneamento de duplicatas no Drive (~16–20 GB)** | **Decisão MOU tomada (2026-06-20): EXCLUIR.** Execução não-automatizável daqui (MCP do Drive sem delete) | Executor pronto: `drive-arrumacao/Sanear-Duplicatas-PotencialUrbano.gs` (rodar no Apps Script da conta) + mapa `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md` |
| D2 | **Re-ingerir 14 municipais-SP verbatim** dos PDFs do Drive (hoje resumos `confianca:baixa`) | é AFINAR (trabalho de Gen Técnico-RAG), não arrumação; egress p/ `.gov.br` bloqueado neste ambiente | `MANIFESTO.json alertas` + Lote 2 de `docs/PROMPTS-EXTRACAO-EXTENSAO.md` |
| D3 | **Realocar/validar os 2 fora-de-escopo** (tema-1020→ISS; verificar nº REsp 1658054) | decisão do MOU (D24 ponto cego declarado) | sinalizado no MANIFESTO |
| D4 | Fatiamento→indexação (rag/) + criar schemas dos artefatos no Supabase | AFINAR; só após organização aprovada (RO-23) | pipeline Partes 2–3 |
| D5 | RLS off em `public.spatial_ref_sys` (sistema PostGIS) | **CORREÇÃO 2026-06-20:** `ENABLE RLS` é BLOQUEADO (tabela do `supabase_admin`; somos role `postgres`). Fix real = remover `public` dos Exposed schemas (Dashboard); dado real vive em `governanca`. Ação física do MOU (escritório M-41) | advisory reportado; remediação corrigida |

## Verificação determinística (passes limpos)
- `python3 -m json.tool` em todos os 59 JSONs + `MANIFESTO.json` → **0 malformado**.
- `grep '"status_pipeline": "processado"'` → **0** (enum ilegal eliminado).
- `scripts/consolidar.py` idempotente (rodado 2× → mesmo resultado: 59/57/2).
- Pares `.md`↔`.json` → **0 órfão**. Naming consistente. **0 duplicata real** no repo (gen3 sinalizado).
- Refs de estrutura citadas nos docs reconferidas; `consolidar.yml` e `evals/ground-truth/` agora existem.

## O que continua SÓLIDO (não tocado)
Integridade de pares, rastreabilidade verbatim em `_capturas/`, honestidade dialética
dos itens fora-de-escopo e das municipais não-verbatim (todos com VACINA/aviso), engines/oráculos.
O corpus **não estava corrompido** — estava com o manifesto desligado, um enum ilegal,
e docs de estado defasados. Tudo isso saneado.

---

## Rodada 2 — re-auditoria adversarial (mesmo dia, pós-correções)
3 lentes frescas re-rodadas para caçar defeitos introduzidos PELAS próprias correções. Acharam **4 defeitos reais + 1 de clareza** — todos corrigidos:

| # | Defeito (introduzido na rodada 1) | Correção |
|---|---|---|
| R2-1 | `DO_ESCRITORIO.md` ANTÍTESE ainda dizia "Action que ainda não existe" — contradizia a tabela (LIGADA) editada no mesmo arquivo | ANTÍTESE/CONCILIAÇÃO reescritas (Action existe; bloqueio agora é interno) |
| R2-2 | `HANDOFF:6` (convenção) e `docs/PROMPTS-EXTRACAO-EXTENSAO.md:146` ainda usavam o enum morto `processado` (o grep da rodada 1 só varreu JSONs) | trocados p/ vocabulário canônico / `tagueado` |
| R2-3 | `HANDOFF:22` "+ 4 com `revisao_pendente`" — número inventado; só **1** (`stj-resp-1658054`) | corrigido p/ 1 |
| R2-4 | `jurisprudencia/stj-resp-1658054.json` `verificacao_verbatim` (prosa) ainda citava `status_pipeline=processado` após o campo virar `tagueado` | prosa atualizada |
| R2-5 (clareza) | `MANIFESTO.json` `por_status` somava 57 (só ativos) sem rótulo | chave renomeada `por_status_pipeline_ativos` + `_nota` no resumo |

**Verificado LIMPO na rodada 2:** idempotência do `consolidar.py` (0 diff em 2 runs), sem risco de loop na Action (bot commita só `MANIFESTO.json`, fora dos paths vigiados, + `[skip ci]`), 0 JSON malformado, 0 órfão, marker `_PROCESSADOS.md` correto, staging (leis `bruto` / juris `tagueado`) defensável e não-mentiroso, Supabase consistente, 0 ref quebrada. Constituição (`CLAUDE.md`/`PROJETO-RAG`) tem comentário `(a ligar)` desatualizado — **não editada** (requer aval do MOU; estado-verdade vive no MANIFESTO+DO_ESCRITORIO).

> **Convergência:** rodada 1 achou ~10 defeitos; rodada 2 achou 5 (resíduos das próprias correções), corrigidos.

## Rodada 3 — convergência CONFIRMADA (2026-06-20)
2 lentes frescas (PU corpus+docs adversarial; escritório) → **veredito: CONVERGIU LIMPO** nos dois repos. Verificado: 0 uso vivo do enum `processado` (só notas históricas/auditoria), `consolidar.py` idempotente (0 diff em 2 runs), `por_status_pipeline_ativos`+`_nota` corretos, `revisao_pendente`=1 (stj-resp-1658054, prosa coerente), contagens 27/32/59/57/2 batem em todos os docs, 0 contradição (nenhum doc afirma "Action não existe"/"skeleton vazio"/"6 schemas"/"tudo vazio"/"~40 leis" como estado atual), 64 JSONs válidos, 0 órfão, refs novas existem, 0 regressão da rodada 2.
**Esteira de auditoria fechada: R1 → R2 → R3 limpa.** O registro do projeto está honesto e consistente; o que resta é trabalho de esteira (AFINAR) e decisões do MOU — tudo em `PROXIMA-INSTANCIA.md`.
