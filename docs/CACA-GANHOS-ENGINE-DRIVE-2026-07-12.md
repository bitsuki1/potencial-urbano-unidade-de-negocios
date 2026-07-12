# Caça a ganhos de engine no garimpo do Drive (PU 19 · 2026-07-12)

> Do catálogo do Drive (33.138 → 460 úteis → 48 normas oficiais faltantes), triagem das 48 por
> impacto em input de engine. Doutrina: só entra ganho com verbatim + rastreável (1.3).

## ✅ GANHOS APLICADOS (em produção)
- **★ MAIOR GANHO — Série de reajuste do Quadro 14 → VTcd/V VIGENTE por vintage.** O V (valor do terreno
  cedente, Art. 128; e V da OODC, Art. 117) estava **CONGELADO na base 2014** (`q14-valor-terreno.csv`);
  um cálculo para fato gerador recente subavaliava o terreno em **~26%** (fator 2026 = 1,2595). Capturada
  verbatim (portal oficial) a cadeia de reajustes do Quadro 14, Art. 1º de cada decreto:
  base 2014 → **59.166/2019 (+2%, ef.2020)** → **62.135/2022 (+5%, ef.2023)** → **63.108/2023 (+5%, ef.2024)**
  → **63.999/2024 (+4,5%, ef.2025)** → **64.884/2025 (+7,18%, ef.2026)**.
  `tabelas/q14-reajuste-anual.csv` + `art128.py` (`fator_reajuste_q14`/`vtcd_vigente`) + `oodc.py`
  (`oodc_por_imovel(ano_ref=...)`, com `aviso_vintage` quando o V fica na base 2014). **PROVA DE BATER O
  PONTO:** base R$ 3.106,00 (SQL 001003) × fator 2024 (1,12455) = **R$ 3.492,85** = valor nominal oficial
  da **Portaria SMUL nº 19/2024**. Autoteste (gate) trava a prova. PR #43.
- **Limiar Fi de parque (Art. 127 §1º IV/V), vintage 2025 = R$ 2.194,50/m²** — Decreto 63.999/2024, Art. 3º.
  Faltava na tabela (só 2014 e 2026); o engine falhava p/ ano-ref 2025. Cadeia completa 2014→2025→2026.
  `tabelas/limiar-parque-art127.csv` + `pcpt.py` (gate verde). PR #42.

## ✅ AUDITORIA CONFIRMADA (selo — nossos motores batem a norma oficial)
- **Decreto 63.504/2024** (regulamento da OODC): a fórmula oficial da contrapartida
  **`C = (At/Ac)·V·Fp·Fs`** (Art. 117 PDE) bate EXATAMENTE o Cr do nosso `art128.py`;
  V=Quadro 14, Fp=Quadro 6, Fs=Quadro 5+art.79 — todos como já temos. Nenhuma divergência.

## 💡 LEADS (registrados, NÃO aplicados — precisam de dado/decisão)
1. **Fp = 2 nas ZEM/ZEMP** (art. 8 LPUOS, confirmado no Dec. 63.504/2024): override por ZONA que o
   `fp.py` (que só conhece macroárea) não modela. **Lado receptor** (OODC); no preço do cedente o Fp/Cr
   **cancela** (Art. 128) — sem impacto no produto do vendedor. Aplicar só se/quando o motor receptor
   precisar, e requer o dado de zona (ZEM/ZEMP) por lote.
2. **+5% sobre a área a regularizar** (Art. 115 §2º / 117 §8º PDE; Dec. 63.504/2024): sobretaxa da OODC
   em regularização — o `oodc.py` não trata o caso regularização. Lead receptor.
3. **Renda HIS/HMP por ano** (Dec. 61.218/2022: HIS1 R$3.636 / HIS2 R$7.272 / HMP R$12.120; Dec.
   62.175/2023: R$3.906 / R$7.812 / R$13.020): alimentam a CLASSIFICAÇÃO HIS1/HIS2/HMP que seleciona o
   Fs no Quadro 5. Se o motor de Fs precisar da faixa de renda vigente por ano, viram tabela de input.
4. ~~Série de reajustes do Quadro 14~~ → **CAPTURADO E APLICADO** (ver GANHOS APLICADOS, o ★ maior ganho).

## 🔎 As 10 fichas IPTU truncadas (re-capturadas do portal oficial — laço fechado)
Todas na pasta `Documentos Novos/.../IPTU/dados_pericia` (dataset de perícia). Lidas verbatim no portal:
- **Decreto 58.592/2018** — **É a atualização monetária anual do IPTU**: Art. 1º atualiza em **+3,5% p/ o
  exercício de 2019** os valores unitários de construção e terreno (PGV) e os valores venais de referência.
  Confirma que o IPTU tem a MESMA mecânica de vintage do Quadro 14. **Não vira ganho-número imediato** no
  motor de IPTU: a tabela de construção já está em 2026 (Lei 18.330/2025), o PGV é *entrada* por consulta
  (não há base congelada a rolar) e a atualização das faixas da Lei 15.889/2013 é questão legal separada.
  → Vira a semente da **série de atualização anual do IPTU** (trilha IPTU, diferida — ver BACKLOG).
- **Decreto 63.698/2024** — **Consolidação das Leis Tributárias do Município** (compilação de 20 matérias,
  incl. IPTU). Sem parâmetro novo, mas **corpus RAG de alto valor** (código tributário consolidado).
- **Lei 17.092/2019** — remissão de créditos 2014-2018 + mudança na *aplicação* de descontos (a partir de
  2020, §2º-A) + isenção de templos + transferência de crédito em desdobro. Sem alíquota/faixa nova (regra).
- **Decreto 56.954/2016** — institui a DTOL (Declaração Tributária de Obra Licenciada). Procedimental, sem número.
- **Leis 11.308/1992, 11.614/1994, 13.698/2003, 13.776/2004, 14.089/2005** — normas de IPTU **anteriores** à
  estrutura vigente (Lei 10.235/1986 red. 11.152/1991 + 15.889/2013). Superadas p/ cálculo ATUAL, mas são o
  **corpus histórico (vintage, 1.6)** que a perícia precisa para o fato gerador daqueles anos (trilha IPTU).

**Conclusão IPTU:** nenhum ganho-número imediato do lado TDC (são todas IPTU); confirmada a mecânica de
atualização anual (semente de série) + corpus de perícia histórica. Fica proposto como workstream IPTU (diferido).

## Resto das 48
Baixa relevância de engine (PIUs/OUC específicas, procedimentos, GIS, ITBI, REURB, segurança hídrica,
dark kitchens). Detalhe na triagem.

## Veredito da caça — ENCERRADA
**2 ganhos concretos aplicados** (★ série Q14 → VTcd vigente nos DOIS motores, + limiar de parque 2025) +
**1 auditoria de fórmula confirmada** (Dec. 63.504/2024) + leads receptor-side que **cancelam** no preço do
cedente + as 10 fichas IPTU caracterizadas (corpus + semente de série, trilha diferida). O maior buraco real
do lado TDC — o V congelado em 2014 — **foi tapado** e provado contra dado oficial (Portaria SMUL 19/2024).
O que resta é trilha IPTU (diferida) e refinamentos receptor-side (fora do preço do vendedor).
