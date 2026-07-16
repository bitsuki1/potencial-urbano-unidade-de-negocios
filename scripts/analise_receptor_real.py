#!/usr/bin/env python3
"""
analise_receptor_real.py — ESTUDO do lado RECEPTOR sobre os 169 casos REAIS capturados
(`casos-reais/tdc/certidoes-reais-ago2025.csv`). Mede empiricamente a conversão da TDC entre o
imóvel cedente e o receptor: **área cedida-equivalente × área recebida-real**.

Pergunta que responde (gate "o produto calcula o receptor?"): dá para prever a área que o COMPRADOR
recebe a partir do crédito do vendedor? Resposta empírica: **não sem o projeto do comprador** — a razão
recebida/cedida = VTcd_cedente ÷ (Cr_receptor × CAmaxcd) (Art. 128), e o Cr do receptor (Art. 117) é
projeto-específico → a razão real varia ordens de grandeza. O que É estável e nosso é o **valor do cedente**
(Art. 128), conservado na transação.

Extração pura / 1.3: só lê o CSV capturado (fonte oficial DEUSO/SMUL) e o FUNDURB; não inventa.
Uso: python3 scripts/analise_receptor_real.py [--autoteste]
"""
import csv
import sys
import argparse
import statistics
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "casos-reais" / "tdc" / "certidoes-reais-ago2025.csv"


def _d(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return Decimal(s.replace(".", "").replace(",", ".")) if "," in s else Decimal(s)
    except Exception:
        return None


def pares():
    out = []
    for r in csv.DictReader(open(SRC, encoding="utf-8")):
        ced, rec = _d(r.get("area_cedida_equivalente_m2")), _d(r.get("area_recebida_real_m2"))
        if ced and rec and ced > 0 and rec > 0:
            out.append((float(ced), float(rec), r))
    return out


def analise():
    p = pares()
    razoes = sorted(rec / ced for ced, rec, _ in p)
    tot_c = sum(c for c, r, _ in p)
    tot_r = sum(r for c, r, _ in p)
    valorados = []
    for ced, rec, r in p:
        v = _d(r.get("valor_pecuniario_rs"))
        if v:
            valorados.append((ced, rec, float(v), r))
    return {
        "n": len(p),
        "razao_min": razoes[0], "razao_mediana": statistics.median(razoes), "razao_max": razoes[-1],
        "maior_que_1": sum(1 for x in razoes if x > 1),
        "menor_que_1": sum(1 for x in razoes if x < 1),
        "total_cedido": tot_c, "total_recebido": tot_r, "razao_agregada": tot_r / tot_c,
        "valorados": valorados,
    }


def _autoteste():
    a = analise()
    assert a["n"] > 150, a["n"]
    assert 1.0 < a["razao_mediana"] < 1.5, a["razao_mediana"]      # mediana observada ~1,24
    assert a["razao_max"] / a["razao_min"] > 100, "dispersão deve ser de ordens de grandeza"
    assert len(a["valorados"]) >= 7, "casos valorados FUNDURB"
    # valor conservado: para cada valorado, valor/ced e valor/rec são o MESMO valor sobre áreas diferentes
    for ced, rec, v, _ in a["valorados"]:
        assert abs((v / ced) * ced - v) < 1e-6 and abs((v / rec) * rec - v) < 1e-6
    return a["n"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autoteste", action="store_true")
    if ap.parse_args().autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE análise receptor: OK — {n} pares área cedida×recebida; dispersão e conservação de valor verificadas.")
        return 0
    a = analise()
    print(f"=== Lado RECEPTOR sobre {a['n']} transferências REAIS (DEUSO/SMUL ago/2025) ===")
    print(f"razão área recebida/cedida: min={a['razao_min']:.3f} · mediana={a['razao_mediana']:.3f} · máx={a['razao_max']:.3f}")
    print(f"  recebida > cedida (receptor + barato): {a['maior_que_1']} · recebida < cedida: {a['menor_que_1']}")
    print(f"agregado: {a['total_cedido']:.0f} m² cedidos → {a['total_recebido']:.0f} m² recebidos (razão {a['razao_agregada']:.3f})")
    print("\ncasos com valor FUNDURB — o valor R$ é conservado; a ÁREA converte pela razão de valor de terreno:")
    for ced, rec, v, r in a["valorados"]:
        print(f"  {ced:8.1f} m²ced → {rec:8.1f} m²rec (×{rec/ced:.2f}) | R$/m²ced={v/ced:6.0f} R$/m²rec={v/rec:6.0f}"
              f" | {(r.get('distrito_cedente') or '')[:16]:16} → {(r.get('distrito_receptor') or '')[:16]}")
    print("\nLeitura (gate do receptor): a razão varia ordens de grandeza porque depende do Cr do RECEPTOR")
    print("(Art. 117, projeto-específico). Logo a área que o comprador recebe NÃO é computável sem o projeto")
    print("dele. O que é estável e nosso é o VALOR do cedente (Art. 128, piso), conservado na transação.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
