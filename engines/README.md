# engines/ — Artefato **FÓRMULA / ENGINE** (RO-03, princípio 1.1)

> **O que mora aqui:** o **cálculo determinístico** (valuation TDC, IPTU progressivo). É CÓDIGO, não prosa.
> **Número nasce no engine, nunca no LLM** (1.3/RO-04). Cada resultado carrega memória de cálculo + citação ao dispositivo de origem.
> Fórmula **NUNCA mora dentro do corpus de leis** (1.1) — a lei é texto (RAG), a fórmula é função pura aqui.

## Conteúdo (o que é o quê — não confundir)
| Caminho | Natureza | Status |
|---|---|---|
| `tdc/oodc.py` | **O ENGINE** (executável, determinístico, auto-testado no CI) — OODC/geração/recepção/travas TDC. | ativo, verde |
| `tdc/motor00/*.json` | Constantes/travas operacionais que o engine lê (fonte única de parâmetro). | ativo |
| `tdc/oraculos/*.md` | **LEGADO** (matrizes v3/v4, "Conhecimento Mestre"). É **insumo de escrutínio** p/ o Codex Mestre (RO-16), **NÃO** é engine nem fonte da verdade. Candidato a mover p/ `_legado/`. | legado/insumo |
| `iptu/` | Engine do IPTU progressivo. | **vazio** — a forjar (IPTU vem depois do TDC, decisão MOU) |
| `FORMULAS-CONSOLIDADAS.md` | Consolidação das fórmulas em PROSA (proveniência/legibilidade humana). **Referência, não executada** — quem calcula é `oodc.py` (D-08). | referência |

## Convenção
- Toda fórmula nova entra como **função pura** (entrada→saída, sem rede, sem LLM), com `_autoteste()` e citação do dispositivo.
- Insumo de tabela ausente (`V`/`CA_max`) = **entrada obrigatória** vinda de `tabelas/`, nunca inventada (D-08): o engine LEVANTA se faltar.
