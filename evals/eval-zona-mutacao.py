#!/usr/bin/env python3
"""
eval-zona-mutacao.py — GATE de mutação do Motor do Mapa (G6): zona sabotada DEVE divergir.

Prova em DOIS pontos:
  (a) REGRESSÃO — zona e CAbás do pipeline (zona_por_cedente.csv) batem no gabarito (Quadro 3);
  (b) MUTAÇÃO   — injetar uma zona sabotada produz CAbás DIFERENTE do certo (o teste DETECTA).

Se o pipeline produzir a zona errada para um cedente, a FASE 1 falha (regressão).
Se o Quadro 3 for alterado de modo que a sabotagem pare de ser detectável, a FASE 2 falha (mutação).

DoD (G6): sabotar a zona de 0010870001 de ZEPAM (CAbás=0,1) para ZC (CAbás=1) faz FASE 1 FALHAR.

Uso:  python3 evals/eval-zona-mutacao.py   # exit !=0 se qualquer assert falhar
PU 18 · 2026-07-10.
"""
import csv
import json
import sys
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ZONA_CSV = RAIZ / "zepec" / "oficial" / "zona_por_cedente.csv"
QUADRO3 = RAIZ / "tabelas" / "quadro3-ca-por-zona.csv"
GABARITO = RAIZ / "evals" / "ground-truth" / "gabaritos" / "zona-mutacao-g6.json"


def carregar_quadro3():
    q3 = {}
    with open(QUADRO3, encoding="utf-8") as fh:
        linhas = [l for l in fh if not l.startswith("#")]
    for r in csv.DictReader(linhas):
        ca = r["ca_basico"].strip().replace(",", ".")
        q3[r["zona"].strip()] = ca
    return q3


def carregar_zona_csv():
    idx = {}
    with open(ZONA_CSV, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            ca = r["ca_basico"].strip().replace(",", ".")
            idx[r["sql_mestre"].strip()] = {"zona": r["zona"].strip(), "ca_basico": ca}
    return idx


def main():
    if not ZONA_CSV.exists():
        print(f"GATE VERMELHO: {ZONA_CSV.relative_to(RAIZ)} ausente.", file=sys.stderr)
        sys.exit(1)
    if not GABARITO.exists():
        print(f"GATE VERMELHO: {GABARITO.relative_to(RAIZ)} ausente.", file=sys.stderr)
        sys.exit(1)

    gab = json.loads(GABARITO.read_text(encoding="utf-8"))
    dados = carregar_zona_csv()
    q3 = carregar_quadro3()

    falhas = 0
    n_checks = 0

    print("=== eval-zona-mutacao (G6): teste de mutação do Motor do Mapa ===")
    for caso in gab["casos"]:
        sql = caso["sql_mestre"]
        zona_certa = caso["zona_certa"]
        ca_certo = caso["ca_basico_certo"]

        real = dados.get(sql)
        if real is None:
            print(f"  [FALHA] {sql}: ausente no zona_por_cedente.csv")
            falhas += 1
            n_checks += 1
            continue

        detalhes = []

        # FASE 1 — regressão: pipeline bate no gabarito
        if real["zona"] != zona_certa:
            detalhes.append(f"F1 zona={real['zona']} != gabarito {zona_certa}")
        if real["ca_basico"] != ca_certo:
            detalhes.append(f"F1 ca_basico={real['ca_basico']} != gabarito {ca_certo}")

        # FASE 2 — mutação: zona sabotada produz CAbás diferente
        zona_sab = caso["zona_sabotada"]
        ca_sab = q3.get(zona_sab, "")
        if not ca_sab or ca_sab == "NA":
            detalhes.append(f"F2 zona sabotada {zona_sab} sem CAbás no Quadro 3")
        elif ca_sab == ca_certo:
            detalhes.append(f"F2 mutação fraca: {zona_sab} tem mesmo CAbás={ca_sab} que {zona_certa}")
        # else: mutation detected — sabotaged zone has different CAbás

        status = "PASS" if not detalhes else "FALHA"
        if detalhes:
            falhas += 1
            print(f"  [{status}] {sql} ({zona_certa} CAbás={ca_certo}): " + " ; ".join(detalhes))
        else:
            print(f"  [{status}] {sql} ({zona_certa} CAbás={ca_certo}): "
                  f"F1 ok, F2 mutação {zona_sab}→CAbás={ca_sab} detectável")
        n_checks += 1

    # Não-vácuo: pelo menos 3 casos devem existir no gabarito
    if len(gab["casos"]) < 3:
        print(f"  [FALHA] não-vácuo: {len(gab['casos'])} casos no gabarito (mínimo 3)")
        falhas += 1
    else:
        print(f"  [PASS ] não-vácuo: {len(gab['casos'])} casos no gabarito")
    n_checks += 1

    print(f"\nRESUMO: {n_checks-falhas}/{n_checks} PASS, {falhas} falha(s).")
    if falhas:
        print("GATE VERMELHO: zona do pipeline divergiu do gabarito Quadro 3 (G6).", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
