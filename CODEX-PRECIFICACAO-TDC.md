# CODEX DE PRECIFICAÇÃO TDC (conversão para R$)
> ⏸️ **PARADO (decisão do MOU, 2026-06-28): não trabalhar preço agora.** Este codex existe só para **guardar o que já aprendemos** sobre R$ — nada se descarta (doutrina). Quando o foco voltar para preço, parte-se daqui.
> Irmãos: `CODEX-COMERCIAL-TDC.md` (foco ativo) · `CODEX-CALCULOS-TDC.md` (potencial em m²).
> **Linha que separa:** Cálculos = *quanto potencial* (m²). Precificação = *quanto dinheiro* (R$). Aqui é só R$.

## 1 — O que sabemos sobre o R$ (parkado)
- **V (Quadro 14)** = valor do m² do terreno → `tabelas/q14-valor-terreno.csv` (já em mãos). É o insumo de preço por SQL.
- **Valor do crédito (proxy do cedente):** `valor ≈ PCpt × V`. **É proxy, não o preço final.**
- **Preço real do receptor (Art. 128):** `PCr = (PCpt × VTcd) / (Cr × CAmaxcd)`, com **CAmaxcd = 4 fixo SÓ na via sem-doação (Art. 125)**; na doação o CAmaxcd é o real do terreno. Correção **IPCA**. V vale na **data de referência**.
- **Preço de mercado livre** (o que o receptor paga ao cedente) **não é publicado** — só temos o regulatório.

## 2 — FUNDURB em R$ (teto e fila)
- **Teto de 5% (Art. 24 §5º LPUOS):** o pecuniário total transferido em 12 meses ≤ 5% da arrecadação do FUNDURB no período. Ref. 2024: arrecadação ≈ R$ 43,4 Mi → teto ≈ R$ 7,8 Mi.
- **Valor pecuniário regulatório** por processo → `zepec/limpo/fundurb_processos.csv` (`valor_pecuniario_rs`, `teto_5pct_rs`, `somatoria_tdc_rs`). **≠ preço de mercado.**
- O teto só recai sobre declarações **pós-2016**.

## 3 — Resoluções de preço (realocadas do Comercial)
| # | Decisão |
|---|---|
| R16 | **`valor = PCpt × V` é PROXY**, não preço final. Crédito recebido segue **Art. 128** (CAmaxcd=4 só via 125, IPCA); V na data de protocolo (Art. 125 §2º). ESGOTADO é temporal (renovação Art. 123 §5º / 129 §2º) |
| R17 | **FUNDURB `valor_pecuniario_rs` é REGULATÓRIO, não de mercado** (Art. 24 §5º). (a) declaração pré-2016 fora do teto = vantagem de liquidez; (b) "Indeferido" muitas vezes por saturação do teto, não defeito |

## 4 — O que faltaria fazer (quando despausar)
- Engine `art128.py` (preço-receptor) com `CAmaxcd=4` condicionado à via 125 + IPCA.
- Cruzar V (Q14) × PCpt do engine cedente → valor estimado por imóvel (com selo de estimativa).
- Validar contra os comparáveis regulatórios da fila FUNDURB.

> **Nota de liquidez (vem do Comercial):** consultar a janela/estoque do FUNDURB **antes** de sugerir venda é passo COMERCIAL (sensor de liquidez), não cálculo de preço — fica no Codex Comercial.
