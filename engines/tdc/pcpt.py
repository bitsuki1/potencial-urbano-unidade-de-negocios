#!/usr/bin/env python3
"""
pcpt.py — Engine determinístico do POTENCIAL CONSTRUTIVO PASSÍVEL DE TRANSFERÊNCIA (lado CEDENTE).

Complementa oodc.py (lado receptor). Modela as DUAS vias de geração de TDC (achado do agente legal
2026-06-28: a via de doação estava fora do modelo):

  • SEM doação (Art. 125, Lei 16.050/2014): PCpt = Atc × CAbas × Fi, com Fi = 1.
    O proprietário MANTÉM o imóvel (caso ZEPEC-BIR/ZEPAM). Usa o coef. BÁSICO.

  • COM doação (Art. 127): PCpt = Atc × CAmax × Fi(finalidade).
    O proprietário DOA o imóvel à PMSP e recebe potencial. Usa o coef. MÁXIMO e Fi até 2,0.

Princípios (iguais ao oodc.py):
- 1.3 — número nasce AQUI; Atc (área terreno, IPTU/cadastro), CAbas/CAmax (Quadro 3) e V (Quadro 14)
  são ENTRADAS; o engine NÃO os inventa.
- 1.7 — cada resultado carrega `citacao` do dispositivo.
- DECIMAL exato (Decimal), nunca float, no valor em m².

Fatores de incentivo à doação (Art. 127 §1º, incisos I–V):
  I  corredores de ônibus ............ 2,0
  II HIS ............................. 1,9
  III regularização fundiária ........ 0,8
  IV parque (V ≤ R$2.000/m²) ......... 1,4   (Redação Lei 17.975/2023)
  V  parque (V > R$2.000/m²) ......... 1,0

Uso:
    python3 engines/tdc/pcpt.py --demo     # exemplo trabalhado + auto-teste (gate)
PU 14 · 2026-06-28.
"""
import sys, argparse
from decimal import Decimal, ROUND_HALF_UP

LEI = "Lei Municipal SP nº 16.050/2014 (PDE)"
Q2 = Decimal("0.01")

# Art. 127 §1º — fator de incentivo à doação por finalidade
FI_DOACAO = {
    "corredor_onibus":        (Decimal("2.0"), "Art. 127 §1º, I"),
    "his":                    (Decimal("1.9"), "Art. 127 §1º, II"),
    "regularizacao_fundiaria":(Decimal("0.8"), "Art. 127 §1º, III"),
    "parque_v_ate_2000":      (Decimal("1.4"), "Art. 127 §1º, IV (Lei 17.975/2023)"),
    "parque_v_acima_2000":    (Decimal("1.0"), "Art. 127 §1º, V (Lei 17.975/2023)"),
}

def _d(x, campo):
    try: return Decimal(str(x).replace(".", "").replace(",", ".")) if ("," in str(x)) else Decimal(str(x))
    except Exception: raise ValueError(f"{campo} inválido: {x!r}")

def pcpt_sem_doacao(atc, cabas, fi="1"):
    """Art. 125: PCpt = Atc × CAbas × Fi (Fi=1). O dono mantém o imóvel."""
    A, C, F = _d(atc, "atc"), _d(cabas, "cabas"), _d(fi, "fi")
    pcpt = (A * C * F).quantize(Q2, ROUND_HALF_UP)
    return {"via": "sem_doacao", "valor_m2": pcpt,
            "memoria_calculo": f"PCpt = Atc({A}) × CAbas({C}) × Fi({F}) = {pcpt} m²",
            "citacao": {"dispositivo": "Art. 125", "fonte": LEI}}

def pcpt_com_doacao(atc, camax, finalidade):
    """Art. 127: PCpt = Atc × CAmax × Fi(finalidade). O dono DOA o imóvel."""
    if finalidade not in FI_DOACAO:
        raise ValueError(f"finalidade inválida: {finalidade!r}; use {list(FI_DOACAO)}")
    A, C = _d(atc, "atc"), _d(camax, "camax")
    F, disp = FI_DOACAO[finalidade]
    pcpt = (A * C * F).quantize(Q2, ROUND_HALF_UP)
    return {"via": "com_doacao", "finalidade": finalidade, "valor_m2": pcpt,
            "memoria_calculo": f"PCpt = Atc({A}) × CAmax({C}) × Fi({F}) = {pcpt} m²",
            "citacao": {"dispositivo": f"Art. 127 e {disp}", "fonte": LEI}}

def _autoteste():
    # Mesmo terreno, a via muda DRAMATICAMENTE o potencial gerado (ilustra a alavanca).
    atc, cabas, camax = "1000", "1.0", "4.0"
    s = pcpt_sem_doacao(atc, cabas)
    assert s["valor_m2"] == Decimal("1000.00"), s
    d = pcpt_com_doacao(atc, camax, "his")           # 1000 × 4.0 × 1.9
    assert d["valor_m2"] == Decimal("7600.00"), d
    d2 = pcpt_com_doacao(atc, camax, "corredor_onibus")  # 1000 × 4.0 × 2.0
    assert d2["valor_m2"] == Decimal("8000.00"), d2
    # Decimal exato (sem ruído de float): 0.1 três vezes
    assert pcpt_sem_doacao("3333.33", "0.1")["valor_m2"] == Decimal("333.33")
    return s, d, d2

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.parse_args()
    s, d, d2 = _autoteste()
    print("AUTO-TESTE: OK (gate verde)\n")
    print("Exemplo (Atc=1000 m², CAbas=1,0, CAmax=4,0):")
    print(f"  SEM doação (Art.125):        {s['memoria_calculo']}")
    print(f"  COM doação HIS (Art.127):    {d['memoria_calculo']}")
    print(f"  COM doação corredor (Art.127): {d2['memoria_calculo']}")
    print(f"\n  -> a via de doação gera {d2['valor_m2']/s['valor_m2']:.0f}× mais potencial (mas o dono PERDE o imóvel).")
    print("\nFatores de incentivo (Art. 127 §1º):")
    for k,(f,disp) in FI_DOACAO.items(): print(f"  {k:26} Fi={f}  [{disp}]")
