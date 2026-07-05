# Como usar a ferramenta de cedentes ZEPEC (time comercial)
> PU 14 · 2026-06-28. Princípio: **só fato, sem juízo de valor**. As listas separam por ESTÁGIO e PROVA, não por "melhor/pior" — a priorização comercial é sua.

<!-- DISCLAIMER-BLOCO-INICIO -->
> **AVISO (M0 — texto canônico em `DISCLAIMER.md`; leia antes de usar qualquer número):** ferramenta de **decision-support, não parecer/laudo**. `preco_proxy_brl` é **proxy regulatório** (PCpt × V), não preço de mercado. Valor **venal (IPTU) ≠ outorga (Q14)**. O PCpt é **estimativa só p/ prospecção nova** — para o **já-declarado** (`regime_pcpt=JA_DECLARADO`) vale a **Declaração** (Art. 125 §1º I), não o número aqui. Divergência conhecida ≈1,66× (mediana) vs certidões (m² oficial vence). Conservação: só **Atestado** elegibiliza (Termo = PENDENTE). `V` do Q14 é **jan/2025**. Número nasce no engine, citado (1.3/1.7); onde a fonte não ampara, o campo diz **PENDENTE**.
<!-- DISCLAIMER-BLOCO-FIM -->

## Os 3 arquivos
| Arquivo | O que é | Quantos |
|---|---|---|
| **`lista_prospeccao.csv`** | **pronto para abordar** (`negociavel=sim`, identificável) | **2.740** |
| `fila_verificar.csv` | sinal sem prova **ou** transacionou sem SQL/dono — **conferir/identificar antes** | 1.578 |
| `zepec_cedentes.csv` | a base completa (1 linha por imóvel, todas as colunas) | 4.360 |
> Fora das listas: 42 imóveis `negociavel=nao` **com prova escrita** (esgotado/vedado por lei/coletivo).
> **Bem COLETIVO (2026-07-05, decisão do dono):** as 1.772 linhas idênticas "Luminárias Ornamentais da Light"
> (tombamento coletivo de postes, sem lote cadastral) viraram **1 linha `estado_venda=COLETIVO`**
> (`negociavel=nao` — não é imóvel comercializável). Os itens seguem íntegros em `zepec/limpo/zepec_unificada.csv`.
> Por isso a base caiu de 6.131 → 4.360 e a fila de verificação de 3.350 → 1.578 (menos ruído, mesmo fato).
> **Saldo por CONJUNTO (T11):** onde uma certidão cobre **lotes irmãos**, o m² transferido é do conjunto —
> a coluna `conjunto_certidao` marca os irmãos e o saldo individual fica em branco com a pendência declarando
> o **saldo do conjunto** (Σ PCpt − transferido). Não alocamos por lote o que a certidão não aloca.

## Os segmentos da lista de prospecção (fato, não ranking)
| Segmento | O que quer dizer |
|---|---|
| **INTACTO·com dono** (19) | declarou, **nunca vendeu**, e já sabemos o proprietário — o caso mais direto |
| INTACTO·sem dono (482) | declarou, nunca vendeu — falta achar o dono |
| TEM_SALDO·* (91) | já vendeu parte, **ainda resta** potencial |
| SO_ELEGIVEL·* (2.148) | tombado que **ainda não declarou** — pode entrar (precisa declarar antes) |

A ordem do arquivo segue o **estágio do funil** (INTACTO → TEM_SALDO → SO_ELEGIVEL), depois distrito. **Não é nota de qualidade.**

## Colunas
`segmento · estado_venda · nome_bem · endereco_mestre · distrito · proprietario · tipo_zepec · esfera · m2_ja_transferido · status_fundurb · intercorrencia_fundurb · data_ref · sql_mestre`

## Cuidados (o que a ferramenta NÃO afirma)
- **Preço:** não está aqui (decisão de pausar). Quando voltar, vem do engine (Codex Precificação).
- **Dono:** cobertura **parcial** (só 79 na base completa hoje; sobe com ITBI/IPTU no Supabase).
- **Liquidez (FUNDURB):** sinal hoje **INDETERMINADO** (semântica a confirmar na fonte SMUL).
- **`verificar` não é "não":** é "conferir" — nome de bairro/bem público é suspeita, não prova (não temos o dono para afirmar).

## Como é gerada
`python3 zepec/lista_prospeccao.py` (lê `zepec_cedentes.csv`). A base e a ferramenta: ver `zepec/HANDOFF-COMERCIAL-PU14-2026-06-28.md`.
