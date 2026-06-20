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
| D1 | **Saneamento de duplicatas no Drive (~16–20 GB)** | decisão MOU aberta EXCLUIR×MOVER (`PLANO-SANEAMENTO D-2`) + RO-09 + irreversível | `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md` (ids + manter/remover) |
| D2 | **Re-ingerir 14 municipais-SP verbatim** dos PDFs do Drive (hoje resumos `confianca:baixa`) | é AFINAR (trabalho de Gen Técnico-RAG), não arrumação; egress p/ `.gov.br` bloqueado neste ambiente | `MANIFESTO.json alertas` + Lote 2 de `docs/PROMPTS-EXTRACAO-EXTENSAO.md` |
| D3 | **Realocar/validar os 2 fora-de-escopo** (tema-1020→ISS; verificar nº REsp 1658054) | decisão do MOU (D24 ponto cego declarado) | sinalizado no MANIFESTO |
| D4 | Fatiamento→indexação (rag/) + criar schemas dos artefatos no Supabase | AFINAR; só após organização aprovada (RO-23) | pipeline Partes 2–3 |
| D5 | RLS desabilitado em `public.spatial_ref_sys` (tabela de sistema PostGIS) | decisão de segurança do operador; habilitar sem policy quebra PostGIS | advisory reportado ao MOU |

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
