# ESTADO — Potencial Urbano (porta de entrada única)

> **Você está aqui.** Esta é a ÚNICA porta de entrada do projeto. Antes havia 6+ documentos de estado
> sobrepostos (auditorias datadas, handoffs, consolidações) e ninguém sabia qual era a verdade.
> Organizado em 2026-06-21 (chapéu PU): os snapshots datados foram para `docs/_arquivo/` (nada se apaga);
> aqui ficam só os **ponteiros vivos**. Não copio número volátil — leia no SSOT real.

## Ordem de leitura (3 passos)
1. **Este arquivo** — onde estou e pra onde aponto.
2. **`CODEX-DO-PROJETO.md`** — as regras invioláveis (RO-01..RO-15) e as decisões (D-01..D-13). É a constituição.
3. **`BACKLOG.md`** — o que FALTA fazer, com prova de "feito" (DoD). É a lista viva, surfaçada no boot.

## Onde está cada verdade (ponteiros — não copiar número aqui)
| O que | Onde (SSOT) |
|---|---|
| **Regras + decisões** | `CODEX-DO-PROJETO.md` |
| **O que falta fazer (vivo)** | `BACKLOG.md` |
| **Estado de cada lei/jurisprudência** (contagem real) | `MANIFESTO.json` (gerado por `scripts/consolidar.py`) |
| **Constituição técnica** (princípios 1.1–1.7, arquitetura, Gens) | `CLAUDE.md` + `PROJETO-RAG-JURIDICO-IPTU-TDC.md` |
| **Como a esteira RAG funciona** (código) | `scripts/README.md` |
| **Método/stack reutilizável** | `BETA-CONTINUO.md` |
| **Diretrizes do escritório (PMO)** | `DO_ESCRITORIO.md` |
| **Detalhe de retomada + vacinas + mapa de arquivos** | `HANDOFF-E-PENDENCIAS.md` · `PROXIMA-INSTANCIA.md` (secundários) |
| **História: auditorias datadas, relatórios, consolidações** | `docs/_arquivo/` (snapshots; não são estado vivo) |
| **Itens fora do foco IPTU/TDC** (preservados) | `jurisprudencia/_correlatos/` |

## Estado atual em 1 frase (honesto)
Infra (RAG determinístico + engine TDC + anti-perda + gate) **construída, auditada e verde**; o **PRODUTO**
(lista de alvos por imóvel) ainda **não saiu** — destrava quando os dados do Drive (Q14/Quadro 3/PDE verbatim)
descerem (B-9, GO do MOU dado 2026-06-21). Ritmo de trabalho: **D-13** — um artefato de cada vez, com tese, e o MOU escrutina.

## Ao fechar uma sessão
`python3 scripts/fechar-instancia.py` — o gate mecânico ("declarei feito" ≠ "provei feito"). Sai 0 = verde.
