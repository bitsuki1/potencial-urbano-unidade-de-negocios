# Caça a ganhos de engine no garimpo do Drive (PU 19 · 2026-07-12)

> Do catálogo do Drive (33.138 → 460 úteis → 48 normas oficiais faltantes), triagem das 48 por
> impacto em input de engine. Doutrina: só entra ganho com verbatim + rastreável (1.3).

## ✅ GANHO APLICADO (em produção)
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
4. **Série de reajustes do Quadro 14** (Decretos 59.166/2019, 62.135/2022, 63.108/2023, 63.999/2024
   +4,5%, 64.884/2025 +7,18%): a cadeia anual que audita o VTcd — vale ingerir para a série histórica
   rastreável (hoje usamos o ano-ref 2026; a série dá a auditoria de cada elo). 59.166/62.135/63.108
   NÃO estão no GAP das 48 (só aparecem como remissão) — capturar do portal.

## Resto das 48
Baixa relevância de engine (PIUs/OUC específicas, procedimentos, GIS, ITBI, REURB, segurança hídrica,
dark kitchens) ou 10 com ficha truncada no Drive (re-capturar do portal). Detalhe na triagem.

## Veredito da caça
1 ganho concreto aplicado + 1 auditoria de fórmula confirmada + 4 leads mapeados. O grosso do valor
dos motores JÁ está capturado; o que resta são refinamentos do lado receptor (que não mexem no preço
do cedente) e a série histórica de reajustes (auditoria, não mudança de número vigente).
