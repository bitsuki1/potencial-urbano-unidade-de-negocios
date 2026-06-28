# Como usar a ferramenta de cedentes ZEPEC (time comercial)
> PU 14 · 2026-06-28. Princípio: **só fato, sem juízo de valor**. As listas separam por ESTÁGIO e PROVA, não por "melhor/pior" — a priorização comercial é sua.

## Os 3 arquivos
| Arquivo | O que é | Quantos |
|---|---|---|
| **`lista_prospeccao.csv`** | **pronto para abordar** (`negociavel=sim`) | **2.750** |
| `fila_verificar.csv` | tem sinal mas falta prova — **conferir antes** (não descartar) | 3.340 |
| `zepec_cedentes.csv` | a base completa (todos os 6.131, todas as colunas) | 6.131 |
> Fora das listas: 41 imóveis `negociavel=nao` **com prova escrita** (esgotado/vedado por lei).

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
- **Dono:** cobertura **parcial** (só 79 hoje; sobe com ITBI/IPTU no Supabase).
- **Liquidez (FUNDURB):** sinal hoje **INDETERMINADO** (semântica a confirmar na fonte SMUL).
- **`verificar` não é "não":** é "conferir" — nome de bairro/bem público é suspeita, não prova (não temos o dono para afirmar).

## Como é gerada
`python3 zepec/lista_prospeccao.py` (lê `zepec_cedentes.csv`). A base e a ferramenta: ver `zepec/HANDOFF-COMERCIAL-PU14-2026-06-28.md`.
