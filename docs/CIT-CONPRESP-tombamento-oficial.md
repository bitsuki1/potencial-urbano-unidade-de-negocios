# CIT / CONPRESP — camada oficial de tombamento dos cedentes (Art. 129 PDE)

> Base OFICIAL do tombamento que fundamenta a TDC de imóvel de interesse de preservação (Art. 129 da
> Lei 16.050/2014 — PDE). Fonte primária: **CIT (Cadastro de Imóveis Tombados)** da Prefeitura de SP,
> consultado **por SQL** no runner `brasil` (IP-BR) via a Action `cit-batch` do hub `portfolio-automacoes`.
> Extração VERBATIM (1.3/1.7); nada inventado (1.8). Atualizado 2026-07-19 (PU 22) — cobertura TOTAL.

## O que é
Para cada SQL de cedente ZEPEC, o CIT devolve o **nível de preservação** oficial e os **atos de tombamento**
(Resoluções CONPRESP/CONDEPHAAT) — que são a **citação da base legal** do tombamento. Isso confirma (ou
corrige) o `tipo_zepec` que vinha de outra origem e dá o dispositivo que sustenta o Art. 129.

- **Fonte verbatim:** `zepec/oficial/cit-tombamento.csv` (4.292 SQLs, **0 erro**; colunas: sql,
  nivel_preservacao, atos_tombamento, denominacao, endereco_oficial, subprefeitura, situacao, erro).
- **Camada joinada:** `zepec/oficial/conservacao_cedentes.csv` (por sql_mestre; gerada por
  `zepec/pipeline/ingerir_cit_conservacao.py`).
- **No produto:** `zepec/enriquecer_oficial.py` acrescenta as colunas `cit_nivel_preservacao`,
  `cit_atos_tombamento` (citação) e `cit_reconciliacao` a cada cedente enriquecido.

## Cobertura (4.360 cedentes)
| Reconciliação CIT × `tipo_zepec` | Qtde | Leitura |
|---|---:|---|
| **CONFIRMA** (CIT bate o nosso rótulo) | 3.960 | tombamento oficial confirmado, com citação da Resolução |
| **DIVERGE** (CIT × `tipo_zepec`) | 32 | CIT diz `NÃO TOMBADO/NÃO CONSTA` onde tínhamos protegido — **revisar** (o CIT é primário, 1.8) |
| **SEM_DADO** (CIT sem retorno para o SQL) | 300 | fica `SEM_DADO` — nada inventado |
| **SEM_CIT** (SQL fora do lote consultado) | 68 | 1 cedente sem SQL no lote + margens |

## Distribuição do nível oficial (nos cedentes)
| Nível de preservação (CIT) | Qtde |
|---|---:|
| TOMBADO | 2.928 |
| EM PROCESSO DE TOMBAMENTO | 539 |
| TOMBADO — PRESERVAÇÃO DE FACHADAS E VOLUMETRIA | 339 |
| SEM_DADO | 300 |
| TOMBADO — PRESERVAÇÃO TOTAL | 128 |
| NÃO TOMBADO/NÃO CONSTA | 32 |
| ENVOLTÓRIA DE IMÓVEL TOMBADO | 15 |
| AMBIENTAL | 3 |
| TOMBADO — PRESERVAÇÃO VOLUMÉTRICA | 3 |
| ENVOLTÓRIA SÓ CONPRESP / SÓ CONDEPHAAT | 2 + 2 |
| TOMBADO SÓ IPHAN | 1 |

## Regras honradas
- **1.3/1.7 — citação:** o `cit_atos_tombamento` traz as Resoluções (ex.: `RES. 28/18`, `RES. 11/11`) que
  são o dispositivo do tombamento; 3.945 cedentes carregam essa citação.
- **1.8 — nada torto:** o CIT é a fonte primária e **não sobrescreve** o `tipo_zepec` — a saída
  **reconcilia** e surfaça as **32 divergências** para revisão humana; `SEM_DADO` permanece `SEM_DADO`.
- **Nível ≠ elegibilidade automática:** o nível é o FATO oficial; a elegibilidade à TDC do Art. 129 (e a
  vedação do Art. 124 §2º a imóvel tombado com incentivo) é aplicada pelo engine, não presumida aqui.

## Reproduzir
```
# no hub portfolio-automacoes (runner brasil): Action cit-batch (MAX=0) -> tools/cit/out/CIT-tombamento.csv
cp <hub>/tools/cit/out/CIT-tombamento.csv zepec/oficial/cit-tombamento.csv
python3 zepec/pipeline/ingerir_cit_conservacao.py     # -> conservacao_cedentes.csv
python3 zepec/enriquecer_oficial.py                   # acrescenta cit_* ao produto
```
