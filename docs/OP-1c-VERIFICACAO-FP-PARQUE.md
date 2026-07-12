# OP-1c — Verificação do limiar do Fp/Fi de parque (Art. 127 §1º) · FEITO (PU 19, 2026-07-12)

> Lead do garimpo M6 (PU 18): "Lei 17.975/2023 art. 50 deu NR ao Art. 127 §1º (parque): 1,4 se Quadro 14
> ≤ R$ 2.000/m², 1,0 se >; Dec. 64.884/2025 fixa a referência em **R$ 2.352,06/m²** → conferir `fp.py`."

## 1. O que a conferência achou (2 correções ao próprio lead)
1. **Arquivo errado no lead.** O limiar do parque **NÃO mora em `engines/tdc/fp.py`** — `fp.py` é o **Fator de
   Planejamento (Fp) do Quadro 6** da Outorga Onerosa (OODC), por macroárea/uso; outro fator. O incentivo do
   **Art. 127 §1º IV/V** (via COM doação) vive em **`engines/tdc/pcpt.py`** + `tabelas/fi-incentivo-doacao.csv`.
2. **Estava no valor-base de 2014.** O limiar era o hardcode `V_LIMIAR_PARQUE = Decimal("2000")` — o valor
   original do Art. 127, SEM a atualização de 2026 que o Decreto 64.884/2025 exige ("observadas as atualizações
   subsequentes"). Comparar um V do Quadro 14 **2026** (pós +7,18%, OP-1a) contra um limiar **2014** é
   inconsistência de vintage (1.6): um parque com V entre R$ 2.000 e R$ 2.352,06 caía indevidamente no Fi 1,0.

## 2. Fonte oficial (1.3 — número nunca inventado)
Antes de tocar o engine, o valor foi capturado **verbatim da fonte oficial** (não das notas internas que só
diziam "verificar"). Decreto 64.884/2025, **Art. 3º** (legislacao.prefeitura.sp.gov.br/decreto-64884-de-29-de-dezembro-de-2025,
captura 2026-07-12, confirmada com prompt neutro sem induzir o número):

> "Para os fins previstos no artigo 127 da Lei nº 16.050, de 2014, o valor de referência aplicável ao fator de
> incentivo da Transferência do Direito de Construir na implantação de parques, mencionado nos incisos IV e V do
> § 1º do referido artigo, **fica atualizado para R$ 2.352,06/m²** (dois mil, trezentos e cinquenta e dois reais
> e seis centavos por metro quadrado)."

O numeral e o valor por extenso batem — é o Art. 127, incisos IV e V — sem ambiguidade.

## 3. O que foi feito (fix rastreável, table-driven, vintage-aware)
- **Nova tabela** `tabelas/limiar-parque-art127.csv` — limiar por vintage, cada linha com norma-fonte:
  `2014 → R$ 2.000,00` (Lei 16.050/2014 c/c Lei 17.975/2023) · `2026 → R$ 2.352,06` (Dec. 64.884/2025 Art. 3º).
  O verbatim do Art. 3º está no cabeçalho do CSV.
- **`pcpt.py`**: removido o hardcode `V_LIMIAR_PARQUE=2000`; `limiar_parque(ano_ref=None)` lê a tabela e
  devolve o limiar da vintage pedida (**default = a mais recente, 2026**). `pcpt_com_doacao(..., ano_ref=None)`
  compara V com o limiar da MESMA vintage e **cita o limiar aplicado** na saída (1.7).
- **Prova (gate):** no auto-teste do `pcpt.py`, `V=2200` (entre R$ 2.000 e R$ 2.352,06) ⇒ **2026 → Fi 1,4**
  (V≤limiar) e **2014 → Fi 1,0** (V>limiar): a vintage decide. `limiar_parque(2026)=2.352,06`,
  `limiar_parque(2014)=2.000,00`; vintage inexistente = fail-closed. Sabotar a tabela ⇒ o gate FALHA.

## 4. Impacto no produto (honestidade 1.7)
**Nenhum número do entregável atual muda.** A via de parque é **COM doação (Art. 126/127)** — atende um público
**DISJUNTO** da lista ZEPEC-BIR (nossos cedentes são via Art. 125, SEM doação — `pcpt.py` já documenta isso).
O fix é **correção de completude** do motor (fica certo para quando a via de doação for exercida com V de 2026),
não uma mudança de preço da prospecção. É "condição melhor" latente do lado doador/comprador.

## 5. Resíduo (opcional)
Ingerir o **Decreto 64.884/2025** no corpus (`leis/`) para citação RAG plena — hoje o decreto é fonte de
**Tabela/Valor** (o reajuste +7,18% da OP-1a e o limiar R$ 2.352,06 desta OP-1c), ambos já capturados como DADO
com verbatim. A ingestão normativa é baixa prioridade (é decreto de valores, não prosa normativa).
