# tabelas/ — Artefato **TABELA / VALOR** (RO-03, princípio 1.1)

> **O que mora aqui:** os DADOS NUMÉRICOS extraídos das leis (alíquotas, índices, faixas, valor venal, CA por zona).
> Tabela **é dado e SAI do texto da lei** (1.1) — nunca fica dentro do `.md` da norma. Vira **input do engine** (`engines/`).
> **Hoje: VAZIO.** Espera o Q14 (valor venal `V` por SQL) e o Quadro 3 (CA por zona) — combustível do engine (B-1), que vêm do Drive (B-9, GO do MOU dado).

## Formato (2.2)
- **`.csv` por tabela** — uma tabela por arquivo, cabeçalho explícito, UTF-8. CSV porque é input determinístico de engine.
- **Decimal:** guardar como o engine espera. O `oodc.py` parseia decimal-BR (vírgula), mas **prefira ponto** no CSV limpo e documente a convenção no cabeçalho de proveniência.

## Convenção de ENTRADA (quando o dado descer do Drive)
Cada `.csv` nasce com um bloco de **proveniência** (comentário no topo ou um `<id>.fonte.json` ao lado):
- `origem` (fileId do Drive + nome), `data_extracao`, `dispositivo_legal` de origem (qual lei/quadro), `hash`, `ocr: true/false`.
- Nomes sugeridos (casam com a DoD do B-1): `q14-valor-venal-<anoref>.csv`, `quadro3-ca-<zona|ano>.csv`.
- **Número nasce aqui como DADO, nunca inventado** (D-08/RO-04): se um valor não veio da fonte, fica em branco — o engine levanta, não chuta.

## Quem usa
`engines/tdc/oodc.py` consome `V` (Q14, por SQL) e `CA_max` (Quadro 3, por ZONA). Sem estes CSVs o engine roda só no auto-teste, não em imóvel real.
