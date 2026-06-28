#!/usr/bin/env python3
"""
pcpt.py — Engine determinístico do POTENCIAL CONSTRUTIVO PASSÍVEL DE TRANSFERÊNCIA (lado CEDENTE).

Complementa oodc.py (lado receptor). Modela as DUAS vias de geração de TDC (achado do agente legal
2026-06-28: a via de doação estava fora do modelo):

  • SEM doação (Art. 125, Lei 16.050/2014): PCpt = Atc × CAbas × Fi, com Fi = 1 (FIXO na lei).
    O proprietário MANTÉM o imóvel (caso ZEPEC-BIR/ZEPAM, Art. 124 I–II).

  • COM doação (Art. 126/127): PCpt = Atc × CAmax × Fi(finalidade).
    O proprietário DOA o imóvel à PMSP (Art. 126: corredor/HIS/regularização/parque) e recebe potencial.
    Usa o coef. MÁXIMO e Fi até 2,0.

ATENÇÃO (universo): a via de doação atende um PÚBLICO DISJUNTO da lista ZEPEC — são doadores de
terreno comum (parques do Quadro 7, corredores, HIS/ZEIS), NÃO os tombados da nossa lista de cedentes.
Não confundir os dois universos.

Datas (entrada datada): CAbas/CAmax/V valem na DATA DE REFERÊNCIA — protocolo (Art. 125 §2º) na via
sem doação; data da doação (Art. 127 §3º) na via com doação. Renovação ZEPAM congela V antigo (Art.123 §5º).
O engine recebe esses valores como entrada (1.3 — não os inventa nem assume "hoje").

Princípios (iguais ao oodc.py):
- 1.3 — número E escolha de fator nascem AQUI; Atc/CAbas/CAmax/V são ENTRADAS; engine não inventa.
- 1.7 — cada resultado carrega `citacao` do dispositivo.
- DECIMAL exato (Decimal), nunca float, no valor em m². Entrada ambígua é REJEITADA, não adivinhada.

Fatores de incentivo à doação (Art. 127 §1º, incisos I–V; finalidades do Art. 126):
  I  corredores de ônibus ............ 2,0
  II HIS ............................. 1,9
  III regularização fundiária ........ 0,8
  IV parque (V ≤ R$2.000/m²) ......... 1,4   (Redação Lei 17.975/2023)
  V  parque (V > R$2.000/m²) ......... 1,0   — resolvido DENTRO do engine a partir de V.

LIMITE (Art. 124 §3º, por remissão Art.124 §5º): PCpt acima de 50.000 m² é transferido em 10 parcelas
anuais → o engine sinaliza `estoque_a_vista` vs `excedente_parcelado` (estoque não disponível à vista).

Uso:
    python3 engines/tdc/pcpt.py --demo     # exemplo trabalhado + auto-teste (gate)
PU 14 · 2026-06-28.
"""
import sys, re, argparse
from decimal import Decimal, ROUND_HALF_UP

LEI = "Lei Municipal SP nº 16.050/2014 (PDE)"
Q2 = Decimal("0.01")
LIMITE_PARCELAMENTO = Decimal("50000")   # Art. 124 §3º
V_LIMIAR_PARQUE = Decimal("2000")        # Art. 127 §1º IV/V (Quadro 14, R$/m²)

# Art. 127 §1º — fator de incentivo à doação (parque é resolvido por V, ver pcpt_com_doacao)
FI_DOACAO = {
    "corredor_onibus":        (Decimal("2.0"), "Art. 127 §1º, I"),
    "his":                    (Decimal("1.9"), "Art. 127 §1º, II"),
    "regularizacao_fundiaria":(Decimal("0.8"), "Art. 127 §1º, III"),
}

def _d(x, campo):
    """Parse para Decimal. BR (vírgula decimal) ou decimal puro. REJEITA ponto-milhar ambíguo."""
    s = str(x).strip()
    if ',' in s:                                   # BR: ponto=milhar, vírgula=decimal
        s2 = s.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(\.\d{3})+', s):    # ex.: "1.000" / "15.726" = ponto-milhar SEM decimal
        raise ValueError(f"{campo} ambíguo (ponto como milhar sem vírgula): {x!r} — use vírgula decimal ou ponto decimal sem milhar")
    else:
        s2 = s
    try:
        return Decimal(s2)
    except Exception:
        raise ValueError(f"{campo} inválido: {x!r}")

def _pos(d, campo):
    if d <= 0:
        raise ValueError(f"{campo} deve ser > 0 (recebido {d})")
    return d

def _estoque(pcpt):
    """Art. 124 §3º: acima de 50.000 m² o excedente sai em 10 parcelas anuais."""
    if pcpt <= LIMITE_PARCELAMENTO:
        return {"estoque_a_vista_m2": pcpt, "excedente_parcelado_m2": Decimal("0.00"), "parcelas_anuais": 0}
    exc = (pcpt - LIMITE_PARCELAMENTO).quantize(Q2)
    return {"estoque_a_vista_m2": LIMITE_PARCELAMENTO, "excedente_parcelado_m2": exc, "parcelas_anuais": 10,
            "obs_estoque": "Art. 124 §3º — excedente de 50.000 m² em 10 parcelas anuais"}

def pcpt_sem_doacao(atc, cabas):
    """Art. 125: PCpt = Atc × CAbas × Fi (Fi=1, FIXO na lei). O dono mantém o imóvel."""
    A = _pos(_d(atc, "atc"), "atc"); C = _pos(_d(cabas, "cabas"), "cabas")
    pcpt = (A * C * Decimal("1")).quantize(Q2, ROUND_HALF_UP)
    return {"via": "sem_doacao", "valor_m2": pcpt,
            "memoria_calculo": f"PCpt = Atc({A}) × CAbas({C}) × Fi(1) = {pcpt} m²",
            "citacao": {"dispositivo": "Art. 125", "fonte": LEI}, **_estoque(pcpt)}

def pcpt_com_doacao(atc, camax, finalidade, v=None):
    """Art. 126/127: PCpt = Atc × CAmax × Fi(finalidade). O dono DOA o imóvel.
    finalidade ∈ {corredor_onibus, his, regularizacao_fundiaria, parque}. Para 'parque', V é obrigatório
    e o fator (1,4 ≤R$2.000 / 1,0 >R$2.000) é resolvido AQUI (1.3), não pelo chamador."""
    A = _pos(_d(atc, "atc"), "atc"); C = _pos(_d(camax, "camax"), "camax")
    if finalidade == "parque":
        if v is None:
            raise ValueError("finalidade 'parque' exige V (valor do terreno, Quadro 14) para escolher o Fi (Art.127 §1º IV/V)")
        V = _pos(_d(v, "v"), "v")
        if V <= V_LIMIAR_PARQUE: F, disp = Decimal("1.4"), "Art. 127 §1º, IV (Lei 17.975/2023)"
        else:                    F, disp = Decimal("1.0"), "Art. 127 §1º, V (Lei 17.975/2023)"
    elif finalidade in FI_DOACAO:
        F, disp = FI_DOACAO[finalidade]
    else:
        raise ValueError(f"finalidade inválida: {finalidade!r}; use {list(FI_DOACAO)+['parque']}")
    pcpt = (A * C * F).quantize(Q2, ROUND_HALF_UP)
    return {"via": "com_doacao", "finalidade": finalidade, "valor_m2": pcpt,
            "memoria_calculo": f"PCpt = Atc({A}) × CAmax({C}) × Fi({F}) = {pcpt} m²",
            "citacao": {"dispositivo": f"Art. 126/127 e {disp}", "fonte": LEI}, **_estoque(pcpt)}

def _autoteste():
    atc, cabas, camax = "1000", "1.0", "4.0"
    s = pcpt_sem_doacao(atc, cabas);                       assert s["valor_m2"] == Decimal("1000.00"), s
    d = pcpt_com_doacao(atc, camax, "his");                assert d["valor_m2"] == Decimal("7600.00"), d
    d2 = pcpt_com_doacao(atc, camax, "corredor_onibus");   assert d2["valor_m2"] == Decimal("8000.00"), d2
    reg = pcpt_com_doacao(atc, camax, "regularizacao_fundiaria"); assert reg["valor_m2"] == Decimal("3200.00"), reg  # Fi<1
    pba = pcpt_com_doacao(atc, camax, "parque", v="1500"); assert pba["valor_m2"] == Decimal("5600.00"), pba          # Fi 1,4
    pal = pcpt_com_doacao(atc, camax, "parque", v="3000"); assert pal["valor_m2"] == Decimal("4000.00"), pal          # Fi 1,0
    # Decimal exato
    assert pcpt_sem_doacao("3333.33", "0.1")["valor_m2"] == Decimal("333.33")
    # parse BR
    assert pcpt_sem_doacao("520,59", "1,0")["valor_m2"] == Decimal("520.59")
    # >50.000 m² -> parcelamento (Art.124 §3º): 20000 × 4 × 2 = 160000
    big = pcpt_com_doacao("20000", "4.0", "corredor_onibus")
    assert big["estoque_a_vista_m2"] == Decimal("50000") and big["excedente_parcelado_m2"] == Decimal("110000.00"), big
    # rejeições
    for bad in [("1.000","1.0"), ("-50","1.0"), ("1000","0")]:
        try: pcpt_sem_doacao(*bad); raise AssertionError(f"deveria rejeitar {bad}")
        except ValueError: pass
    try: pcpt_com_doacao(atc, camax, "parque"); raise AssertionError("parque sem V deveria falhar")
    except ValueError: pass
    try: pcpt_com_doacao(atc, camax, "xpto"); raise AssertionError("finalidade invalida deveria falhar")
    except ValueError: pass
    return s, d, d2, pba

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--demo", action="store_true"); ap.parse_args()
    s, d, d2, pba = _autoteste()
    print("AUTO-TESTE: OK (gate verde — inclui parque, Fi<1, parse BR, >50k parcelado, rejeições)\n")
    print("Exemplo (Atc=1000 m², CAbas=1,0, CAmax=4,0):")
    print(f"  SEM doação (Art.125):           {s['memoria_calculo']}")
    print(f"  COM doação HIS (Art.127):       {d['memoria_calculo']}")
    print(f"  COM doação corredor (Art.127):  {d2['memoria_calculo']}")
    print(f"  COM doação parque V=1500 (≤2k): {pba['memoria_calculo']}")
    print(f"\n  -> via de doação gera até {d2['valor_m2']/s['valor_m2']:.0f}× mais potencial (mas o dono PERDE o imóvel).")
    print("\nFatores de incentivo (Art. 127 §1º):")
    for k,(fi,disp) in FI_DOACAO.items(): print(f"  {k:26} Fi={fi}  [{disp}]")
    print(f"  {'parque':26} Fi=1,4 se V≤R$2.000 senão 1,0  [Art.127 §1º IV/V]")
