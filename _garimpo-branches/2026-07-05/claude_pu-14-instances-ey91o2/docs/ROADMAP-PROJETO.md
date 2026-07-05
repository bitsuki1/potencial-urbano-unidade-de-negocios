# ROADMAP — Potencial Urbano (RAG Jurídico IPTU/TDC)
> Visão do projeto inteiro. PU 14 · 2026-06-29. Estado vive no git; isto é o mapa.
> Decisão do MOU: **base inicial = TDC** (IPTU vem depois). 4 artefatos (1.1): Lei · Tabela · Fórmula/Engine · Tese.

## As 6 frentes — onde estamos
| Frente | Estado | O que falta |
|---|---|---|
| **A. Corpus RAG** (leis/juris) | 🟢 esteira determinística provada; 19 leis indexadas; TDC ligado | B-4 (verbatim 14 municipais), B-5 (semântica/embeddings), B-6 (grafo remissões), B-7 (vigência datada), B-11(c) (vigência por chunk), B-10 (auditar **mérito jurídico** das teses) |
| **B. Engines/Cálculos** | 🟢 OODC + PCpt (2 vias, Fi-área) | B-3 (completar Fs/Fp), B-12 (guarda decimal total), **rodar R14** (validar PCpt vs m² real), `art128.py` (preço) |
| **C. Produto/dados** (JOIN IPTU×lotes×tabelas) | 🟡 provado em branch; Q14/Q3 no main | **B-17** (consolidar produto ao main — decisão MOU), B-1/B-2, **Supabase** (IPTU/ITBI/sócios/geo) |
| **D. Frente Comercial TDC** (cedente) | 🟢 **núcleo local terminado** | dono/Atc/preço (Supabase), geo (1.791 SQL + perímetros vias 2-6), semântica FUNDURB (SMUL) |
| **E. Lado IPTU** | 🔴 mal começado (TDC primeiro) | toda a frente IPTU |
| **F. Governança/Drive** | 🟢 gate/CI endurecidos | B-8 (saneamento Drive), B-9 (pedido consolidado ao Drive) |

## Os 3 destravadores (liberam quase tudo)
1. **B-17** — consolidar o produto da branch ao `main` (PR a branch protegida = **decisão do MOU**).
2. **Supabase (B-9 + carga pesada)** — IPTU/ITBI/sócios/geo. Destrava dono, Atc, preço, vias de expansão e o JOIN do produto **de uma vez**.
3. **Retomar o preço** — Codex de Precificação pronto; precisa de Atc.

## Sequência macro
**TDC** (corpus✅ + engines✅ + comercial✅ → falta Supabase+preço) → **IPTU** (a outra metade, a abrir) → **integração IPTU×TDC** (produto final: por imóvel, oportunidade de TDC **e** de IPTU, com citação).

## Próximos passos concretos (ordem sugerida)
1. **Validar o engine (R14)** — script que cruza `pcpt` (com Fi-área e Atc) contra os 167 m² transferidos. *Bloqueado por Atc.*
2. **Supabase** — subir IPTU (Atc + endereço/uso) + ITBI (dono/matrícula) + geo. Destrava D inteira.
3. **Confirmar semântica FUNDURB** na SMUL → liga o sensor de liquidez.
4. **B-17 ao main** — decisão do MOU.
5. **Abrir a frente IPTU** (a metade ainda não tocada).

## Pendências por bloqueio
- **Local (dá para fazer já):** regenerar números do dado (script), precedência do conflito de dono (1.287), auditar MEGA_PLANILHA, B-5/B-6/B-7/B-11 (RAG).
- **Drive/Supabase (B-9):** Atc, dono em escala, geo, perímetros vias 2-6.
- **MOU/decisão:** B-17 (PR ao main), retomar preço.
- **Fonte externa (SMUL):** semântica FUNDURB.
