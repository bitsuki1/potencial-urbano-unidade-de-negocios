#!/usr/bin/env python3
"""
art128.py — Engine determinístico do VALOR DE REFERÊNCIA LEGAL do potencial do CEDENTE (lado VENDEDOR),
segundo o Art. 128 da Lei 16.050/2014 (PDE). Complementa pcpt.py (que produz o PCpt) e é o motor do
"preço LEGAL" (D-DONO-7/15: preço é saída de engine rastreável ao artigo; a MARGEM é do usuário —
este engine NÃO define preço de venda, só a referência regulatória).

────────────────────────────────────────────────────────────────────────────────────────────────────
FÓRMULA (Art. 128, VERBATIM — rag/chunks/lei-municipal-saopaulo-16050-2014/133__art-128.json):

    PCr = (PCpt × VTcd) / (Cr × CAmaxcd)

    PCr     – potencial construtivo equivalente a ser recebido no imóvel RECEPTOR (m²);
    PCpt    – potencial construtivo passível de transferência do CEDENTE (m²) — vem do pcpt.py (Art. 125);
    VTcd    – valor unitário (R$/m²) do terreno CEDENTE, Cadastro de Valor de Terreno p/ Outorga Onerosa
              (= Quadro 14), vigente na data de referência;
    Cr      – valor unitário (R$/m²) da contrapartida da outorga onerosa no imóvel RECEPTOR (Art. 117);
    CAmaxcd – coef. de aproveitamento máximo do imóvel cedente.
      §1º — quando o PCpt foi originado no Art. 125 (SEM doação — NOSSO universo), CAmaxcd = 4 (quatro).
      §2º — o VTcd é corrigido pelo IPCA acumulado entre o mês seguinte ao mês de referência da Declaração
            e o último mês anterior ao protocolo do pedido de Certidão de Transferência.

────────────────────────────────────────────────────────────────────────────────────────────────────
ESCOPO VENDEDOR (D-DONO-15) — o que este engine PODE e o que NÃO faz:

  O único dado do RECEPTOR na equação é o Cr. Mas o VALOR ECONÔMICO que o potencial do vendedor
  representa é PCr × Cr (a outorga que o comprador DEIXA de pagar ao Município ao comprar via TDC):

      PCr × Cr = (PCpt × VTcd) / CAmaxcd          ← o Cr CANCELA algebricamente.

  Logo, a REFERÊNCIA regulatória do potencial do vendedor é (PCpt × VTcd) / CAmaxcd — receptor-INDEPENDENTE,
  100% rastreável a Art. 128 caput + §1º. Este engine entrega OS DOIS números (decisão do dono 2026-07-10,
  "mostrar os dois"), cada um citado:

    • numerador_brl  = PCpt × VTcd                (bruto — potencial avaliado pelo terreno cedente)
    • referencia_brl = (PCpt × VTcd) / CAmaxcd    (referência que independe do comprador; Cr cancela)

  O PCr em si (m² no receptor) e o Cr NÃO são calculados aqui — são do lado comprador (fora de escopo).

Princípios (iguais a pcpt.py):
  1.1 — VTcd/CAmaxcd são DADO extraído da lei (§1º) ou ENTRADA (Quadro 14); o engine não inventa tabela.
  1.3 — número nasce AQUI; PCpt/VTcd/fator IPCA são ENTRADAS; o engine não adivinha "hoje" nem a série IPCA.
  1.7 — cada linha do memorial carrega o dispositivo e a fonte.
  Decimal exato (nunca float); entrada ambígua é REJEITADA, não adivinhada.

Uso:
    python3 engines/tdc/art128.py --demo     # exemplo trabalhado + auto-teste (gate)
PU 18 · 2026-07-10.
"""
import re
import argparse
from decimal import Decimal, ROUND_HALF_UP

LEI = "Lei Municipal SP nº 16.050/2014 (PDE)"
DEC_ESQUINA = "Decreto Municipal SP nº 57.536/2016, Art. 3º, IV"   # regra da esquina (MAX Quadro 14)
QUADRO14 = "Quadro 14 do PDE (Cadastro de Valor de Terreno para fins de Outorga Onerosa)"
Q2 = Decimal("0.01")
CAMAXCD_VIA125 = Decimal("4")     # Art. 128 §1º — origem no Art. 125 (sem doação): CAmaxcd = 4 (fixo)


def _d(x, campo):
    """Parse para Decimal. BR (vírgula decimal) ou decimal puro. REJEITA ponto-milhar ambíguo (igual pcpt.py)."""
    s = str(x).strip()
    if ',' in s:                                   # BR: ponto=milhar, vírgula=decimal
        s2 = s.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(\.\d{3})+', s):    # "1.000"/"15.726" = ponto-milhar SEM decimal → ambíguo
        raise ValueError(f"{campo} ambíguo (ponto como milhar sem vírgula): {x!r} — use vírgula decimal ou ponto decimal sem milhar")
    else:
        s2 = s
    try:
        return Decimal(s2)
    except Exception:
        raise ValueError(f"{campo} inválido: {x!r}")


def _pos(dv, campo):
    if dv <= 0:
        raise ValueError(f"{campo} deve ser > 0 (recebido {dv})")
    return dv


def _camaxcd(via, camaxcd):
    """CAmaxcd + citação. via '125' (sem doação) ⇒ 4 fixo (§1º). via '127' (com doação) ⇒ CAmax real (entrada)."""
    if via == "125":
        if camaxcd is not None and _d(camaxcd, "camaxcd") != CAMAXCD_VIA125:
            raise ValueError("via 125: CAmaxcd é fixo em 4 por força do Art. 128 §1º — não sobreponha")
        return CAMAXCD_VIA125, "Art. 128 §1º (PCpt originado no Art. 125 — sem doação): CAmaxcd = 4"
    if via == "127":
        if camaxcd is None:
            raise ValueError("via 127 (com doação) exige CAmaxcd do imóvel cedente vigente na data de referência (Art. 128 caput)")
        return _pos(_d(camaxcd, "camaxcd"), "camaxcd"), "Art. 128 caput: CAmaxcd do imóvel cedente (data de referência/doação)"
    raise ValueError(f"via inválida: {via!r}; use '125' (sem doação) ou '127' (com doação)")


def corrigir_vtcd_ipca(vtcd, ipca_fator, ipca_fonte=None):
    """Art. 128 §2º — corrige o VTcd pelo IPCA acumulado (mês seguinte ao mês de referência → mês anterior
    ao protocolo da Certidão). O `ipca_fator` (ex.: 1.0873 p/ +8,73%) é ENTRADA — o engine NÃO computa a
    série IBGE (1.3). Devolve (VTcd_corrigido, nota). ipca_fator None ⇒ sem correção (prospecção: sem data
    de referência protocolada, usa o Quadro 14 vigente — §2º N/A)."""
    Vt = _pos(_d(vtcd, "vtcd"), "vtcd")
    if ipca_fator is None:
        return Vt, ("sem correção IPCA — prospecção sem data de referência protocolada: usa o Quadro 14 "
                    "vigente (Art. 125 §2º); §2º do Art. 128 N/A até haver Declaração protocolada")
    f = _pos(_d(ipca_fator, "ipca_fator"), "ipca_fator")
    Vtc = (Vt * f).quantize(Q2, ROUND_HALF_UP)
    nota = f"VTcd × IPCA({f}) = R$ {Vtc}/m² (Art. 128 §2º)" + (f" — fonte: {ipca_fonte}" if ipca_fonte else "")
    return Vtc, nota


def referencia_art128(pcpt, vtcd, via="125", ipca_fator=None, ipca_fonte=None, camaxcd=None, esquina=False):
    """Valor de referência LEGAL do potencial do cedente (Art. 128). Entradas (1.3):
      pcpt   — potencial vendável (m²), saída do pcpt.py / saldo líquido;
      vtcd   — valor do m² do terreno cedente (Quadro 14), R$/m²;
      via    — '125' (sem doação, CAmaxcd=4 §1º) | '127' (com doação, CAmaxcd real);
      ipca_fator — fator IPCA acumulado (§2º) ou None (prospecção → sem correção);
      esquina — True se o VTcd já é o MAIOR do Quadro 14 da quadra (Decreto 57.536/2016 Art. 3º IV).
    Devolve OS DOIS números (numerador bruto e ÷CAmaxcd), o memorial auditável e a citação."""
    P = _pos(_d(pcpt, "pcpt"), "pcpt")                    # m²
    Vt = _pos(_d(vtcd, "vtcd"), "vtcd")                   # R$/m² (Quadro 14, face)
    ca, ca_disp = _camaxcd(via, camaxcd)
    Vtc, ipca_nota = corrigir_vtcd_ipca(Vt, ipca_fator, ipca_fonte)

    numerador = (P * Vtc).quantize(Q2, ROUND_HALF_UP)     # R$ — Art. 128 caput (numerador)
    referencia = (numerador / ca).quantize(Q2, ROUND_HALF_UP)   # R$ — ÷CAmaxcd (Cr cancela; §1º)

    disp_vtcd = f"Art. 128 caput; valor do {QUADRO14}"
    if esquina:
        disp_vtcd += f"; {DEC_ESQUINA} (maior valor da quadra — lote de esquina)"
    memorial = [
        {"linha": "PCpt — potencial vendável", "valor": f"{P} m²",
         "dispositivo": "Art. 125 (PDE) — entrada (engine pcpt.py: Atc×CAbás×Fi×FSCE)", "fonte": LEI},
        {"linha": "VTcd — valor do m² do terreno cedente", "valor": f"R$ {Vt}/m²",
         "dispositivo": disp_vtcd, "fonte": QUADRO14},
        {"linha": "VTcd corrigido (§2º IPCA)", "valor": f"R$ {Vtc}/m²",
         "dispositivo": "Art. 128 §2º", "fonte": ipca_nota},
        {"linha": "CAmaxcd", "valor": str(ca),
         "dispositivo": ca_disp, "fonte": LEI},
        {"linha": "Numerador = PCpt × VTcd (bruto)", "valor": f"R$ {numerador}",
         "dispositivo": "Art. 128 caput — numerador da equação de PCr", "fonte": LEI},
        {"linha": "Referência = Numerador ÷ CAmaxcd", "valor": f"R$ {referencia}",
         "dispositivo": "Art. 128 §1º — equivale a PCr×Cr; o Cr do receptor CANCELA (independe do comprador)",
         "fonte": LEI},
    ]
    memoria = (f"N = PCpt({P}) × VTcd({Vtc}) = R$ {numerador}  |  "
               f"VR = N ÷ CAmaxcd({ca}) = R$ {referencia}")
    disp = "Art. 128 (PDE), caput e §1º" + ("; §2º (IPCA)" if ipca_fator is not None else "")
    return {
        "via": via, "pcpt_m2": str(P), "vtcd_m2": str(Vt), "vtcd_corrigido_m2": str(Vtc),
        "camaxcd": str(ca), "esquina": bool(esquina),
        "numerador_brl": str(numerador),      # PCpt × VTcd
        "referencia_brl": str(referencia),    # ÷ CAmaxcd (Cr cancela)
        "memoria_calculo": memoria,
        "memorial": memorial,
        "citacao": {"dispositivo": disp, "fonte": LEI},
    }


def _autoteste():
    # Constante legal ancorada de forma independente (verbatim §1º): via-125 ⇒ CAmaxcd = 4.
    assert CAMAXCD_VIA125 == Decimal("4")

    # Caso limpo: PCpt=1000 m², VTcd=3000 R$/m² → N=3.000.000; VR=N/4=750.000.
    r = referencia_art128("1000", "3000")
    assert r["numerador_brl"] == "3000000.00", r
    assert r["referencia_brl"] == "750000.00", r
    assert r["camaxcd"] == "4", r
    assert "§1º" in r["memorial"][-1]["dispositivo"], r

    # §2º IPCA: VTcd 3000 × 1,10 = 3300 → N=3.300.000; VR=825.000.
    ri = referencia_art128("1000", "3000", ipca_fator="1.10", ipca_fonte="IBGE/SIDRA 1737")
    assert ri["vtcd_corrigido_m2"] == "3300.00", ri
    assert ri["numerador_brl"] == "3300000.00" and ri["referencia_brl"] == "825000.00", ri
    assert "§2º" in ri["citacao"]["dispositivo"], ri

    # via 127 (com doação): CAmaxcd real (=2) entra na conta; N igual, VR=N/2.
    r7 = referencia_art128("1000", "3000", via="127", camaxcd="2")
    assert r7["referencia_brl"] == "1500000.00", r7

    # regra da esquina anotada na citação do VTcd
    re_ = referencia_art128("1000", "3000", esquina=True)
    assert "57.536/2016" in re_["memorial"][1]["dispositivo"], re_

    # Decimal exato + parse BR (VTcd "2.819,20" = 2819,20): 717,60 × 2819,20 = 2.023.057,92; /4 = 505.764,48
    rb = referencia_art128("717,60", "2.819,20")
    assert rb["numerador_brl"] == "2023057.92", rb
    assert rb["referencia_brl"] == "505764.48", rb

    # rejeições (fail-closed)
    casos_ruins = [
        {"pcpt": "0", "vtcd": "3000"},           # PCpt <= 0
        {"pcpt": "1000", "vtcd": "-1"},          # VTcd <= 0
        {"pcpt": "1000", "vtcd": "3000", "via": "999"},        # via inválida
        {"pcpt": "1000", "vtcd": "3000", "via": "127"},        # via 127 sem CAmaxcd
        {"pcpt": "1000", "vtcd": "3000", "via": "125", "camaxcd": "3"},  # via 125 não aceita CAmaxcd≠4
        {"pcpt": "1.000", "vtcd": "3000"},       # ponto-milhar ambíguo
    ]
    for bad in casos_ruins:
        try:
            referencia_art128(**bad); raise AssertionError(f"deveria rejeitar {bad}")
        except ValueError:
            pass
    return r, ri


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.parse_args()
    r, ri = _autoteste()
    print("AUTO-TESTE art128: OK (gate verde — numerador, ÷CAmaxcd, §1º=4, §2º IPCA, via 127, parse BR, rejeições)\n")

    # Exemplo trabalhado end-to-end: parte de um cedente real (via pcpt.py) e chega ao valor de referência.
    print("Exemplo trabalhado (cedente ZEPEC-BIR, Setor Central — via Art. 125, sem doação):")
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import pcpt
        p = pcpt.pcpt_sem_doacao("299", "1.0", setor_central=True)   # gab.006: 299×1×1,2×2 = 717,60 m²
        pcpt_m2 = p["valor_m2"]
        print(f"  1) {p['memoria_calculo']}   [{p['citacao']['dispositivo']}]")
    except Exception as e:
        pcpt_m2 = "717.60"
        print(f"  1) PCpt = 717,60 m² (pcpt.py indisponível no demo: {e})")
    ref = referencia_art128(str(pcpt_m2), "2819,20", esquina=False)
    print(f"  2) VTcd = R$ 2.819,20/m² (Quadro 14, face da quadra)")
    print(f"  3) {ref['memoria_calculo']}")
    print("\n  Memorial auditável (cada linha → dispositivo → fonte):")
    for ln in ref["memorial"]:
        print(f"     • {ln['linha']:38} {ln['valor']:>18}   [{ln['dispositivo']}]")
    print(f"\n  → Referência que INDEPENDE do comprador (Cr cancela): R$ {ref['referencia_brl']}")
    print(f"  → Numerador bruto (potencial × terreno):              R$ {ref['numerador_brl']}")
    print("  (Preço LEGAL de referência — a MARGEM é do usuário; este engine não define preço de venda.)")
