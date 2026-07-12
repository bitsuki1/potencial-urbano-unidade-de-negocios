# CODEX DE PRECIFICAÇÃO TDC (conversão para R$)
> ▶️ **DESPAUSADO / ATIVO (decisão do MOU, 2026-07-10: "vamos começar a trabalhar isso").** O preço legal FOI CONSTRUÍDO: **`engines/tdc/art128.py`** (numerador PCpt×VTcd + referência ÷CAmaxcd=4 §1º + §2º IPCA) + prova **`evals/eval-art128.py`**, no gate. Entra no produto pelo **dossiê** (`gerar_dossie.py`) e na **lista/planilha** (coluna `preco_legal_ref_brl`). Escopo: só o VENDEDOR (o Cr do receptor cancela; D-DONO-15); a MARGEM é do usuário (D-DONO-7).
> _(Histórico: PARADO 2026-06-28 → DESPAUSADO 2026-07-10. Nada se descarta — a seção 1 abaixo guarda o que se aprendeu no período parado.)_
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

## 4 — O que faltaria fazer (quando despausar) — ✅ FEITO (2026-07-10)
- ✅ Engine `engines/tdc/art128.py` com `CAmaxcd=4` condicionado à via 125 (§1º) + **IPCA** (§2º, série IBGE/SIDRA 1737 em `tabelas/ipca-numero-indice-ibge.csv`).
- ✅ Cruzar V (Q14) × PCpt → valor por imóvel (com selo de estimativa): no **dossiê** e na coluna `preco_legal_ref_brl` da lista (3.334 imóveis; ressalva de estimativa no já-declarado).
- ✅ Validar contra os comparáveis do FUNDURB: `eval-art128.py` usa `valor_pecuniario_rs` como **banda de sanidade** (honesto: não há gabarito por-cedente do PCr em R$).
- ⏳ Resta só a série IPCA para os **605 já-declarados** exigir o VTcd histórico da Declaração (o motor já corrige; falta o dado do VTcd na data de referência).

> **Nota de liquidez (vem do Comercial):** consultar a janela/estoque do FUNDURB **antes** de sugerir venda é passo COMERCIAL (sensor de liquidez), não cálculo de preço — fica no Codex Comercial.

## 5 — ⚠️ Ressalva de semântica FUNDURB (achado do escrutínio 2026-06-28)
O `fundurb_processos.csv` tem rótulos a confirmar na fonte SMUL antes de usar como teto/liquidez:
- `somatoria_tdc_acum_rs` = **acumulado all-time** (não a janela rolante de 12m).
- `base_periodo_rs` (col "5% FUNDURB (período)") parece a **arrecadação** (~R$50-77M), não os 5%; teto real ~5% disso (~R$2,5-3,9M).
- Por isso o sensor de liquidez (`zepec/liquidez.py`) reporta **INDETERMINADO** — não emite verde/vermelho sobre dado ambíguo. Destrava confirmando as colunas na fonte.
