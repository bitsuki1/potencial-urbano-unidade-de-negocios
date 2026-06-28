# Sensor de liquidez FUNDURB — janela de mercado (sinal comercial)
> Gerado por `zepec/liquidez.py`. **JANELA: INDETERMINADO** — semântica das colunas do bruto a confirmar (ver abaixo).

**Período mais recente:** Dez-24 a Nov -25
**Fatos crus (sem juízo):**
- "base do período" (col 5% FUNDURB do bruto, **ambígua**): R$ 77.764.352,40
- Somatória TDC **acumulada all-time** (não é a janela): R$ 42.190.972,12
- Soma dos valores efetivamente transferidos NESTE período: R$ 0.00

**Por que INDETERMINADO** (achado do escrutínio 2026-06-28):
1. A somatória é acumulada (cresce sem resetar) → não dá o "transferido na janela de 12m".
2. A coluna "5% FUNDURB (período)" traz ~R$50-77M — parece a **arrecadação**, não os 5%; o teto real (~5%) seria ~R$2,5-3,9M.
→ Comparar os dois daria sinal INVERTIDO. **Não emitimos verde/vermelho sobre isso.**

**Para destravar (passo do MOU):** confirmar na fonte SMUL/PDF qual coluna é o **teto de transferência** e se a somatória reseta por período. Aí o sinal vira confiável.
