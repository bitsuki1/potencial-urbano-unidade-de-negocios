#!/usr/bin/env python3
"""
eval-art128.py — PROVA do motor do preço legal (engines/tdc/art128.py), Art. 128 do PDE.

O que MORDE (gate HARD — falha o build):
  1. ÂNCORA VERBATIM + MUTAÇÃO: recomputa a equação do Art. 128 de forma INDEPENDENTE do engine
     (numerador = PCpt×VTcd; referência = numerador ÷ CAmaxcd) e exige igualdade EXATA. Ancora o §1º
     (CAmaxcd=4 na via-125) de forma independente: se alguém trocar a constante no engine, ISTO falha.
  2. IDENTIDADE ALGÉBRICA em DADOS REAIS: passa TODOS os cedentes reais com saldo+VTcd (do entregável
     zepec_cedentes_oficial.csv) pelo engine e exige numerador = saldo×VTcd e referência = numerador/4
     (Decimal exato) — prova que o engine roda sem erro nos valores de produção (parse, magnitude, esquina).

O que é CONTEXTO (informativo, NÃO falha — honestidade 1.7, sem falsa precisão):
  3. FUNDURB: os valores pecuniários REAIS de TDC (zepec/limpo/fundurb_processos.csv) dão a BANDA de
     ordem de grandeza. NÃO existe gabarito por-cedente do PCr em R$ (o DOC prova PCpt em m² — vide
     eval-formula-zepec; o FUNDURB é agregado por processo/período). Isto é declarado, não escondido.

PU 18 · 2026-07-10.
"""
import csv
import sys
import statistics
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "engines" / "tdc"))
import art128  # noqa: E402

Q2 = Decimal("0.01")
OFICIAL = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes_oficial.csv"
FUNDURB = RAIZ / "zepec" / "limpo" / "fundurb_processos.csv"

# CAmaxcd da via-125 ancorado AQUI, independente do engine (verbatim Art. 128 §1º). Mutação no engine ⇒ falha.
CAMAXCD_VERBATIM = Decimal("4")


def _brl(s):
    """Parse número BR/US para Decimal; None se ilegível/ambíguo (a prova SALTA, não quebra)."""
    try:
        return art128._d(s, "x")
    except Exception:
        return None


def gate_ancora_verbatim():
    """(1) Recomputa o Art. 128 independente do engine e confere igualdade + o §1º=4."""
    falhas = []
    # exemplo trabalhado: PCpt=717,60 m² (gab.006 real), VTcd=2.819,20 R$/m² (Quadro 14)
    P, Vt = Decimal("717.60"), Decimal("2819.20")
    num_esp = (P * Vt).quantize(Q2, ROUND_HALF_UP)
    ref_esp = (num_esp / CAMAXCD_VERBATIM).quantize(Q2, ROUND_HALF_UP)
    got = art128.referencia_art128("717.60", "2819.20")
    if got["numerador_brl"] != str(num_esp):
        falhas.append(f"numerador: engine={got['numerador_brl']} ≠ verbatim={num_esp}")
    if got["referencia_brl"] != str(ref_esp):
        falhas.append(f"referência: engine={got['referencia_brl']} ≠ verbatim={ref_esp}")
    if got["camaxcd"] != str(CAMAXCD_VERBATIM):
        falhas.append(f"CAmaxcd (§1º via-125): engine={got['camaxcd']} ≠ 4 (Art. 128 §1º verbatim)")
    # mutação: a razão numerador/referência TEM de ser CAmaxcd (=4). Se o engine dividir por outra coisa, cai.
    if Decimal(got["numerador_brl"]) != (Decimal(got["referencia_brl"]) * CAMAXCD_VERBATIM):
        falhas.append("invariante numerador = referência × CAmaxcd violada")
    # §2º IPCA independente: 2819,20 × 1,0873 = 3065,52 (HALF_UP)
    ip = art128.referencia_art128("717.60", "2819.20", ipca_fator="1.0873")
    vtc_esp = (Vt * Decimal("1.0873")).quantize(Q2, ROUND_HALF_UP)
    if ip["vtcd_corrigido_m2"] != str(vtc_esp):
        falhas.append(f"§2º IPCA: engine={ip['vtcd_corrigido_m2']} ≠ {vtc_esp}")
    return falhas


def gate_identidade_reais():
    """(2) Todos os cedentes reais com saldo+VTcd passam pelo engine e batem a identidade EXATA."""
    if not OFICIAL.exists():
        return ["ausente: zepec_cedentes_oficial.csv (rode enriquecer_oficial.py)"], 0, []
    falhas, refs = [], []
    n_ok = n_skip = 0
    for r in csv.DictReader(open(OFICIAL, encoding="utf-8")):
        saldo = _brl(r.get("saldo_pcpt_m2"))
        vtcd = _brl(r.get("v_outorga_m2_q14"))
        if saldo is None or vtcd is None or saldo <= 0 or vtcd <= 0:
            n_skip += 1
            continue
        esq = bool(_brl(r.get("v_outorga_max_q14")) and _brl(r.get("v_outorga_max_q14")) > vtcd)
        out = art128.referencia_art128(str(saldo), str(vtcd), esquina=esq)
        num_esp = (saldo * vtcd).quantize(Q2, ROUND_HALF_UP)
        ref_esp = (num_esp / CAMAXCD_VERBATIM).quantize(Q2, ROUND_HALF_UP)
        if out["numerador_brl"] != str(num_esp) or out["referencia_brl"] != str(ref_esp):
            falhas.append(f"{r.get('sql_mestre','?')}: engine {out['numerador_brl']}/{out['referencia_brl']} "
                          f"≠ {num_esp}/{ref_esp}")
            if len(falhas) > 5:
                break
        else:
            n_ok += 1
            refs.append(ref_esp)
    if n_ok == 0 and not falhas:
        falhas.append("nenhum cedente com saldo+VTcd — o produto não tem insumo p/ o preço (verificar pipeline)")
    return falhas, n_ok, refs


def contexto_fundurb(refs):
    """(3) Banda de ordem de grandeza vs valores pecuniários REAIS de TDC (FUNDURB) — informativo."""
    if not FUNDURB.exists():
        print("[CONTEXTO] fundurb_processos.csv ausente — sem banda de comparação.")
        return
    vals = []
    for r in csv.DictReader(open(FUNDURB, encoding="utf-8")):
        v = _brl(r.get("valor_pecuniario_rs"))
        if v and v > 0:
            vals.append(v)
    if vals:
        print(f"[CONTEXTO] FUNDURB — {len(vals)} processos reais de TDC; valor pecuniário por processo: "
              f"R$ {min(vals):,.2f} … R$ {max(vals):,.2f} (mediana R$ {statistics.median(vals):,.2f}).")
    if refs:
        print(f"[CONTEXTO] Referência (Art.128 ÷CAmaxcd) dos cedentes reais: "
              f"R$ {min(refs):,.2f} … R$ {max(refs):,.2f} (mediana R$ {statistics.median(refs):,.2f}).")
    print("[CONTEXTO] NÃO há gabarito por-cedente do PCr em R$ (o DOC prova PCpt em m² — eval-formula-zepec; "
          "o FUNDURB é agregado por processo). Banda = sanidade de ordem de grandeza, não igualdade.")


def gate_ipca():
    """(1b) §2º — a correção do VTcd bate a série IBGE/SIDRA 1737 (âncora do dono: jun/26÷jan/20 ≈ 1,4353)."""
    falhas = []
    serie = art128.carregar_ipca()
    f, fim = art128.fator_ipca("2020-01", "2026-07", serie=serie)   # protocolo jul/26 → fim jun/26
    if fim != "2026-06":
        falhas.append(f"§2º mês-fim: {fim} ≠ 2026-06 (mês anterior ao protocolo, disponível)")
    if f != serie["2026-06"] / serie["2020-01"]:
        falhas.append("§2º fator ≠ índice[2026-06]÷índice[2020-01]")
    if abs(f - Decimal("1.4353")) > Decimal("0.001"):
        falhas.append(f"§2º fator {f} fora da âncora IBGE ~1,4353")
    return falhas, f


def gate_max():
    """(1c) OP-1b — MAX(A piso vigente ; B Declaração×IPCA §2º): recomputa AMBAS as bases independente do
    engine e exige que o MAX escolha a maior, com a base vencedora citada. Mutação-sensível: se o engine
    devolver a menor (ou trocar as bases), ISTO cai."""
    falhas = []
    serie = art128.carregar_ipca()
    P = Decimal("717.60")
    # (B) VENCE — VTcd_decl 1500 corrigido de jan/2014 supera o piso vigente 2819,20.
    fB, _ = art128.fator_ipca("2014-01", "2026-07", serie=serie)
    vtcB = (Decimal("1500") * fB).quantize(Q2, ROUND_HALF_UP)
    refA = ((P * Decimal("2819.20")).quantize(Q2, ROUND_HALF_UP) / CAMAXCD_VERBATIM).quantize(Q2, ROUND_HALF_UP)
    refB = ((P * vtcB).quantize(Q2, ROUND_HALF_UP) / CAMAXCD_VERBATIM).quantize(Q2, ROUND_HALF_UP)
    esperado = max(refA, refB)
    got = art128.referencia_max_art128(str(P), "2819.20", vtcd_declaracao="1500",
                                       mes_ref="2014-01", mes_protocolo="2026-07")
    if got["referencia_max_brl"] != str(esperado):
        falhas.append(f"MAX: engine={got['referencia_max_brl']} ≠ verbatim max({refA},{refB})={esperado}")
    if got["base_vencedora"] != ("B" if refB >= refA else "A"):
        falhas.append(f"base vencedora: engine={got['base_vencedora']} ≠ esperado={'B' if refB>=refA else 'A'}")
    if len(got["cenarios"]) != 2:
        falhas.append("MAX não expôs os DOIS cenários (piso+teto lado a lado, 1.3)")
    # (A) VENCE — VTcd_decl baixo (500) mesmo corrigido não alcança o piso.
    got2 = art128.referencia_max_art128(str(P), "2819.20", vtcd_declaracao="500",
                                        mes_ref="2014-01", mes_protocolo="2026-07")
    if got2["base_vencedora"] != "A":
        falhas.append(f"piso deveria vencer VTcd_decl baixo: engine={got2['base_vencedora']}")
    return falhas, esperado


def main():
    print("═══ PROVA art128 (preço legal, Art. 128 PDE) ═══")
    falhas1 = gate_ancora_verbatim()
    falhas1b, fipca = gate_ipca()
    falhas1c, refmax = gate_max()
    falhas2, n_ok, refs = gate_identidade_reais()

    if falhas1:
        print("[FALHA] âncora verbatim / §1º / §2º:")
        for f in falhas1:
            print("   -", f)
    else:
        print("[PASS] âncora VERBATIM: numerador, ÷CAmaxcd(§1º=4) e §2º IPCA reproduzem o Art. 128 (mutação-sensível).")

    if falhas1b:
        print("[FALHA] §2º IPCA (série IBGE/SIDRA 1737):")
        for f in falhas1b:
            print("   -", f)
    else:
        print(f"[PASS] §2º IPCA: correção da série IBGE/SIDRA 1737 confere (jun/2026÷jan/2020 = {fipca:.4f} ≈ 1,4353).")

    if falhas1c:
        print("[FALHA] MAX(A piso ; B §2º) — OP-1b:")
        for f in falhas1c:
            print("   -", f)
    else:
        print(f"[PASS] MAX(A vigente ; B Declaração×IPCA §2º): o engine escolhe a maior base citada "
              f"(teto § 2º R$ {refmax:,.2f}); piso vence quando o VTcd declarado é baixo (mutação-sensível).")

    if falhas2:
        print("[FALHA] identidade em dados reais:")
        for f in falhas2:
            print("   -", f)
    else:
        print(f"[PASS] IDENTIDADE em dados reais: {n_ok} cedentes reais passam pelo engine com "
              f"numerador=saldo×VTcd e referência=÷4 EXATOS (sem erro de parse/magnitude).")

    contexto_fundurb(refs)

    if falhas1 or falhas1b or falhas1c or falhas2:
        print(f"\nRESUMO: FALHA ({len(falhas1)+len(falhas1b)+len(falhas1c)+len(falhas2)} problema(s)).")
        return 1
    print(f"\nRESUMO: OK — Art. 128 provado verbatim + §2º IPCA (série IBGE) + MAX(A;B) OP-1b + "
          f"{n_ok} cedentes reais; FUNDURB como banda.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
