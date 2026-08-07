#!/usr/bin/env python3
"""
completar_minmax_suplemento.py — complemento CIRÚRGICO das colunas MENOR/MAIOR (decisão do dono
2026-08-07) nas 171 linhas do suplemento-455 (RECUPERAVEL_COM_AREA), que a rodada original criou
ANTES das colunas existirem e que a trava inviolável do suplemento impede de re-tocar.

O que faz (e SÓ isso): para linhas `estado_triagem=RECUPERAVEL_COM_AREA` com `v_outorga_max_q14`
preenchido e `v_outorga_min_q14` vazio, preenche as 4 colunas novas a partir do Quadro 14/2026
oficial (min/max das faces do SQ) e do saldo já calculado — MESMA regra do `_precificar` do gerador
(cap 50.000 m²; Dec. 57.536/2016 Art. 3º IV p/ o MAIOR). Nenhuma outra célula muda (verificação
campo-a-campo ao final, mesmo espírito da trava do suplemento).
"""
import csv
import statistics
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FERR = AQUI / "ferramenta" / "zepec_cedentes_oficial.csv"
NOVAS = ("v_outorga_min_q14", "v_outorga_max_q14", "preco_proxy_menor_brl", "preco_proxy_maior_brl")
CAP = Decimal("50000")


def main():
    q14_por_sq = defaultdict(list)
    for r in csv.DictReader(open(AQUI / "oficial/q14_cedentes_2026_oficial.csv", encoding="utf-8")):
        q14_por_sq[r["sq"]].append(Decimal(r["valor_m2_brl"]))
    q14_min = {sq: min(v) for sq, v in q14_por_sq.items()}
    q14_max = {sq: max(v) for sq, v in q14_por_sq.items()}

    rows = list(csv.DictReader(open(FERR, encoding="utf-8")))
    campos = list(rows[0].keys())
    antes = [{k: v for k, v in r.items() if k not in NOVAS} for r in rows]

    n = 0
    for r in rows:
        if r.get("estado_triagem") != "RECUPERAVEL_COM_AREA":
            continue
        if not r.get("v_outorga_max_q14") or r.get("v_outorga_min_q14"):
            continue
        sq6 = r["sql_mestre"][:6]
        if sq6 not in q14_min:
            continue
        vmin, vmax = q14_min[sq6], q14_max[sq6]
        r["v_outorga_min_q14"] = str(vmin)
        r["v_outorga_max_q14"] = str(vmax)
        saldo = Decimal(r["saldo_pcpt_m2"]) if (r.get("saldo_pcpt_m2") or "").strip() else None
        if saldo and saldo > 0:
            base = min(saldo, CAP)
            r["preco_proxy_menor_brl"] = str((base * vmin).quantize(Decimal("0.01")))
            r["preco_proxy_maior_brl"] = str((base * vmax).quantize(Decimal("0.01")))
        n += 1

    depois = [{k: v for k, v in r.items() if k not in NOVAS} for r in rows]
    assert antes == depois, "TRAVA: célula fora das 4 colunas novas mudou — abortando sem gravar"

    with FERR.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(rows)
    print(f"complemento min/max: {n} linhas do suplemento preenchidas (só as 4 colunas novas)")


if __name__ == "__main__":
    main()
