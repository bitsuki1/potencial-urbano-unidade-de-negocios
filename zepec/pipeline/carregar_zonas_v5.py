#!/usr/bin/env python3
"""
carregar_zonas_v5.py — consome o resultado da rodada v5 do hub e atualiza o SSOT das zonas.

Entrada : $HUB/tools/pu-geo/zonas_v5.csv
          (sql_mestre,x_utm23s,y_utm23s,origem_ponto,zona_v3,zona_18177,status)
Saída   : patch em zepec/oficial/zona_por_cedente.csv  (só com --aplicar)
          zepec/oficial/_pendencias_zona.csv regravado pelo gerar_alvos_zona_v5.py depois.

REGRA DE ENTRADA NO SSOT (fail-closed, 1.3/1.7):
  entra   -> status=ok_vigente_18177 E a zona tem CAbás no Quadro 3 (Lei 16.402/2016)
  NÃO entra -> status=so_v3_ainda      (camada ANTIGA 13.885/2004 — rótulo fora do Quadro 3)
               status=ponto_sem_zona   (nenhuma feição no ponto)
               status=sem_ponto_de_partida
               zona ZOE                (regime PRÓPRIO: CAbás vem do ato do perímetro, não do Q3)
               zona Praça/Canteiro     (bem público não-edificável)
               zona com CAbás 'NA' no Quadro 3
  Tudo que não entra fica declarado como pendência COM MOTIVO — nunca chutado.

Proveniência gravada no campo `fonte`:
  GeoSampa(Lei18177→<ZONA>)+Q3[ponto=<origem>]
  onde <origem> = centroide_lote_cidadao (centroide OFICIAL do lote) ou nominatim_v5 (endereço).

Uso:
  python3 zepec/pipeline/carregar_zonas_v5.py             # relatório (dry-run)
  python3 zepec/pipeline/carregar_zonas_v5.py --aplicar   # grava no SSOT
PU 23e · 2026-08-07.
"""
import argparse
import csv
import os
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(os.environ.get("PU_REPO", Path(__file__).resolve().parents[2]))
HUB = Path(os.environ.get("HUB", "/home/user/portfolio-automacoes"))

SSOT = RAIZ / "zepec/oficial/zona_por_cedente.csv"
QUADRO3 = RAIZ / "tabelas/quadro3-ca-por-zona.csv"
RESULTADO = HUB / "tools/pu-geo/zonas_v5.csv"

SEM_CA_POR_REGIME = {
    "ZOE": "ZOE tem regime PRÓPRIO — CAbás definido pelo ato/plano do perímetro, não pelo Quadro 3",
    "PRAÇA/CANTEIRO": "bem público não-edificável (praça/canteiro) — sem CAbás",
    "PRACA/CANTEIRO": "bem público não-edificável (praça/canteiro) — sem CAbás",
}


def quadro3():
    q3 = {}
    with open(QUADRO3, encoding="utf-8") as fh:
        linhas = [l for l in fh if not l.startswith("#")]
    for r in csv.DictReader(linhas):
        q3[r["zona"].strip().upper()] = r["ca_basico"].strip()
    return q3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()

    if not RESULTADO.exists():
        print(f"GATE: {RESULTADO} ainda não existe — rode o workflow `pu-zona-v5` do hub "
              f"(Actions -> pu-zona-v5 -> Run workflow) e traga o CSV.", file=sys.stderr)
        return 2

    q3 = quadro3()
    with open(RESULTADO, encoding="utf-8") as fh:
        res = list(csv.DictReader(fh))
    with open(SSOT, encoding="utf-8") as fh:
        rd = csv.reader(fh)
        header = next(rd)
        rows = [r for r in rd if r]
    idx = {r[0]: i for i, r in enumerate(rows)}
    ncol = len(header)

    entram, recusas = {}, []
    for r in res:
        sql, z = r["sql_mestre"].strip(), r["zona_18177"].strip()
        if r["status"] != "ok_vigente_18177" or not z:
            recusas.append((sql, r["status"], f"sem zona na camada vigente (v3='{r['zona_v3']}')"))
            continue
        zu = z.upper()
        if zu in SEM_CA_POR_REGIME:
            recusas.append((sql, "zona_sem_ca_por_regime", SEM_CA_POR_REGIME[zu]))
            continue
        ca = q3.get(zu)
        if ca is None:
            recusas.append((sql, "zona_fora_do_quadro3", f"zona '{z}' não consta no Quadro 3 da Lei 16.402/2016"))
            continue
        if ca.upper() == "NA":
            recusas.append((sql, "cabas_NA_no_quadro3", f"zona '{z}' com CAbás 'NA' no Quadro 3"))
            continue
        entram[sql] = (z, ca, f"GeoSampa(Lei18177→{z})+Q3[ponto={r['origem_ponto']}]")

    novos = [s for s in entram if s not in idx]
    atualiza = [s for s in entram if s in idx]

    print("=== CARGA v5 NO SSOT DE ZONA ===")
    print("linhas no resultado do hub:", len(res))
    print("aprovadas (camada vigente + Quadro 3):", len(entram),
          f"({len(novos)} novas, {len(atualiza)} substituem linha existente)")
    print("recusadas (pendência declarada):", len(recusas))
    for k, v in Counter(x[1] for x in recusas).most_common():
        print(f"  {k:26s}: {v}")
    print("zonas aprovadas:", Counter(v[0] for v in entram.values()).most_common())

    if not args.aplicar:
        print("\n(dry-run — nada gravado. Rode com --aplicar.)")
        return 0

    for sql, (z, ca, fonte) in entram.items():
        if sql in idx:
            r = rows[idx[sql]]
            while len(r) < ncol:
                r.append("")
            r[1], r[2], r[3] = z, ca, fonte
        else:
            nova = [sql, z, ca, fonte] + [""] * (ncol - 4)
            rows.append(nova)
    rows.sort(key=lambda r: r[0])
    with open(SSOT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"\nSSOT gravado: {len(rows)} linhas.")
    print("PRÓXIMO: python3 zepec/enriquecer_oficial.py && python3 zepec/funil.py && "
          "python3 evals/eval-zona-mutacao.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
