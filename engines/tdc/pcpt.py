#!/usr/bin/env python3
"""
pcpt.py — Engine determinístico do POTENCIAL CONSTRUTIVO PASSÍVEL DE TRANSFERÊNCIA (lado CEDENTE).

Complementa oodc.py (lado receptor). Modela as DUAS vias de geração de TDC (achado do agente legal
2026-06-28: a via de doação estava fora do modelo):

  • SEM doação (Art. 125, Lei 16.050/2014): PCpt = Atc × CAbas × Fi, com Fi ESCALONADO pela ÁREA do
    lote (LPUOS Lei 16.402/2016, Art. 24, I–VII: 1,2 / 1,0 / 0,9 / 0,7 / 0,5 / 0,2 / 0,1) — NÃO é fixo
    em 1 (correção 2026-07-02; a doutrina "Fi=1,0 estático" era stale — ver auditoria A-02 2026-07-05).
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

# ★ CORREÇÃO 2026-07-02 (loop de melhoria, lente jurídica — VERIFICADO no verbatim indexado da LPUOS):
# o Fi da via SEM doação (novas declarações ZEPEC) NÃO é 1 fixo. A LPUOS Lei 16.402/2016, Art. 24,
# ESCALONA o Fi pela ÁREA DO LOTE (incisos I–VII). Usar Fi=1 p/ todos subestimava lotes ≤500m² em 20%
# e INFLAVA lotes >50.000m² em 10×. Faixas (limite superior INCLUSIVO, "até X"):
LEI_LPUOS = "Lei Municipal SP nº 16.402/2016 (LPUOS)"
FI_ZEPEC_ART24 = [   # (limite_superior_m2 ou None=infinito, Fi, inciso)
    (Decimal("500"),   Decimal("1.2"), "Art. 24, I"),
    (Decimal("2000"),  Decimal("1.0"), "Art. 24, II"),
    (Decimal("5000"),  Decimal("0.9"), "Art. 24, III"),
    (Decimal("10000"), Decimal("0.7"), "Art. 24, IV"),
    (Decimal("20000"), Decimal("0.5"), "Art. 24, V"),
    (Decimal("50000"), Decimal("0.2"), "Art. 24, VI"),
    (None,             Decimal("0.1"), "Art. 24, VII"),
]

def fi_zepec_por_area(atc):
    """Fi da via sem-doação p/ NOVAS declarações ZEPEC, escalonado pela área do lote
    (LPUOS Art. 24, I–VII). Devolve (Fi, inciso). O engine escolhe o fator (1.3)."""
    A = _pos(_d(atc, "atc"), "atc")
    for teto, fi, inciso in FI_ZEPEC_ART24:
        if teto is None or A <= teto:
            return fi, inciso
    raise AssertionError("faixa Art. 24 não resolvida")  # inalcançável

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

def pcpt_sem_doacao(atc, cabas, fi=None):
    """Art. 125 (PDE): PCpt = Atc × CAbas × Fi. O dono mantém o imóvel.
    Fi: por PADRÃO é resolvido AQUI pelo Art. 24 da LPUOS (escalonado pela área do lote,
    caso das NOVAS declarações ZEPEC — correção 2026-07-02; antes usava 1 fixo, ERRADO).
    `fi` explícito sobrepõe (ex.: declaração antiga emitida sob outro fator — informar o da certidão)."""
    A = _pos(_d(atc, "atc"), "atc"); C = _pos(_d(cabas, "cabas"), "cabas")
    if fi is None:
        F, inciso = fi_zepec_por_area(A)
        disp = f"Art. 125 (PDE) c/c LPUOS {inciso}"
        fonte = f"{LEI}; {LEI_LPUOS}"
    else:
        F = _pos(_d(fi, "fi"), "fi")
        disp, fonte = "Art. 125 (PDE); Fi informado pelo chamador", LEI
    pcpt = (A * C * F).quantize(Q2, ROUND_HALF_UP)
    return {"via": "sem_doacao", "valor_m2": pcpt, "fi": str(F),
            "memoria_calculo": f"PCpt = Atc({A}) × CAbas({C}) × Fi({F}) = {pcpt} m²",
            "citacao": {"dispositivo": disp, "fonte": fonte}, **_estoque(pcpt)}

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
    s = pcpt_sem_doacao(atc, cabas);                       assert s["valor_m2"] == Decimal("1000.00"), s  # faixa II Fi=1,0
    d = pcpt_com_doacao(atc, camax, "his");                assert d["valor_m2"] == Decimal("7600.00"), d
    d2 = pcpt_com_doacao(atc, camax, "corredor_onibus");   assert d2["valor_m2"] == Decimal("8000.00"), d2
    reg = pcpt_com_doacao(atc, camax, "regularizacao_fundiaria"); assert reg["valor_m2"] == Decimal("3200.00"), reg  # Fi<1
    pba = pcpt_com_doacao(atc, camax, "parque", v="1500"); assert pba["valor_m2"] == Decimal("5600.00"), pba          # Fi 1,4
    pal = pcpt_com_doacao(atc, camax, "parque", v="3000"); assert pal["valor_m2"] == Decimal("4000.00"), pal          # Fi 1,0
    # ★ Fi ESCALONADO (LPUOS Art. 24, correção 2026-07-02) — uma prova por faixa/borda:
    assert pcpt_sem_doacao("400", "1.0")["valor_m2"] == Decimal("480.00")        # I: ≤500 → 1,2
    assert pcpt_sem_doacao("500", "1.0")["valor_m2"] == Decimal("600.00")        # borda: 500 é "até 500" → 1,2
    assert pcpt_sem_doacao("501", "1.0")["valor_m2"] == Decimal("501.00")        # II: 1,0
    assert pcpt_sem_doacao("3000", "1.0")["valor_m2"] == Decimal("2700.00")      # III: 0,9
    assert pcpt_sem_doacao("8000", "1.0")["valor_m2"] == Decimal("5600.00")      # IV: 0,7
    assert pcpt_sem_doacao("15000", "1.0")["valor_m2"] == Decimal("7500.00")     # V: 0,5
    assert pcpt_sem_doacao("30000", "1.0")["valor_m2"] == Decimal("6000.00")     # VI: 0,2
    assert pcpt_sem_doacao("444030", "1.0")["valor_m2"] == Decimal("44403.00")   # VII: 0,1 (caso real Philipe Pinel)
    s24 = pcpt_sem_doacao("444030", "1.0"); assert "Art. 24, VII" in s24["citacao"]["dispositivo"], s24  # cita o inciso
    # `fi` explícito sobrepõe (declaração antiga com fator da certidão)
    assert pcpt_sem_doacao("444030", "1.0", fi="1")["valor_m2"] == Decimal("444030.00")
    # Decimal exato (3333.33 → faixa III, Fi=0,9)
    assert pcpt_sem_doacao("3333.33", "0.1")["valor_m2"] == Decimal("300.00")
    # parse BR (520,59 > 500 → faixa II, Fi=1,0)
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
