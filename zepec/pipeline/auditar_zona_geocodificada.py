#!/usr/bin/env python3
"""
auditar_zona_geocodificada.py — GATE de proveniência das zonas obtidas por GEOCODIFICAÇÃO.

POR QUÊ (achado PU 23e, 2026-08-07):
  As 326 zonas carregadas com `fonte=GEOCODIFICACAO(Nominatim)+GeoSampa(Lei18177)+Q3`
  nasceram de um PONTO DE ENDEREÇO devolvido pelo Nominatim/OSM — não do lote.
  Depois daquela rodada o repo passou a ter `zepec/oficial/centroides_cedentes.csv`
  (CENTROIDE OFICIAL do lote, camada `geoportal:lote_cidadao` do GeoSampa, EPSG 31983).
  Onde as DUAS coisas existem dá para CONFERIR o ponto contra a fonte oficial: se o
  ponto geocodificado está longe do lote, a zona lida naquele ponto NÃO é a zona do lote.

REGRA (fail-closed, 1.3/1.7/1.8):
  ponto fora do município de São Paulo   -> zona NÃO PROVADA -> sai do SSOT
  dist(ponto_geocodificado, centroide_lote) > LIMIAR (default 500 m) -> NÃO PROVADA -> sai
  (500 m ≈ mais que uma quadra fiscal inteira de SP: a essa distância o ponto está,
   comprovadamente, noutra quadra — logo a zona lida não pertence ao lote. Limiar
   deliberadamente FROUXO: só corta o que é indiscutível; o duvidoso fica e é
   RECOLETADO pelo centroide oficial na rodada v5.)

O que sai do SSOT vira PENDÊNCIA declarada (entra em `alvos_zona_v5.csv`), nunca vira
zona chutada. Nada é inventado; nada é preenchido por vizinhança.

Entradas:
  zepec/oficial/zona_por_cedente.csv        (SSOT — só as linhas fonte=GEOCODIFICACAO)
  zepec/oficial/centroides_cedentes.csv     (centroide OFICIAL do lote, EPSG 31983)
  $HUB/tools/pu-geo/geocode_474.csv         (ponto geocodificado + x/y UTM23S da rodada v4)

Saídas:
  zepec/oficial/_auditoria_zona_geocodificada.csv   (uma linha por cedente conferível)
  patch em zepec/oficial/zona_por_cedente.csv       (só com --aplicar)

Uso:
  python3 zepec/pipeline/auditar_zona_geocodificada.py            # relatório (dry-run)
  python3 zepec/pipeline/auditar_zona_geocodificada.py --aplicar  # remove os reprovados
  ... --limiar 300                                                # limiar em metros
PU 23e · 2026-08-07.
"""
import argparse
import csv
import math
import os
import sys
from pathlib import Path

RAIZ = Path(os.environ.get("PU_REPO", Path(__file__).resolve().parents[2]))
HUB = Path(os.environ.get("HUB", "/home/user/portfolio-automacoes"))

SSOT = RAIZ / "zepec/oficial/zona_por_cedente.csv"
CENTROIDES = RAIZ / "zepec/oficial/centroides_cedentes.csv"
GEOCODE = HUB / "tools/pu-geo/geocode_474.csv"
OUT = RAIZ / "zepec/oficial/_auditoria_zona_geocodificada.csv"

MARCA_GEO = "GEOCODIFICACAO"
# Envelope do município de São Paulo (WGS84). Fonte: malha municipal IBGE (SP 3550308).
# Folga proposital nas bordas — serve só para pegar geocodificação em OUTRA CIDADE.
BBOX = {"lat_min": -24.02, "lat_max": -23.35, "lon_min": -46.85, "lon_max": -46.36}


def ler(p):
    with open(p, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true", help="remove do SSOT as linhas reprovadas")
    ap.add_argument("--limiar", type=float, default=500.0, help="distância máxima em metros (default 500)")
    args = ap.parse_args()

    for p in (SSOT, CENTROIDES, GEOCODE):
        if not p.exists():
            print(f"GATE VERMELHO: ausente {p}", file=sys.stderr)
            return 2

    ssot = ler(SSOT)
    cen = {r["sql_mestre"]: r for r in ler(CENTROIDES)}
    geo = {r["sql_mestre"]: r for r in ler(GEOCODE)}

    linhas = []
    reprovados = set()
    conferiveis = 0
    for r in ssot:
        if MARCA_GEO not in r["fonte"]:
            continue
        sql = r["sql_mestre"]
        g = geo.get(sql)
        if not g:
            linhas.append([sql, r["zona"], "", "", "", "SEM_ORIGEM", "linha GEOCODIFICACAO sem par em geocode_474.csv"])
            continue
        lat = g["lat"].strip()
        lon = g["lon"].strip()
        fora_bbox = ""
        if lat and lon:
            la, lo = float(lat), float(lon)
            fora_bbox = "1" if not (BBOX["lat_min"] <= la <= BBOX["lat_max"]
                                    and BBOX["lon_min"] <= lo <= BBOX["lon_max"]) else ""
        c = cen.get(sql, {})
        dist = ""
        if c.get("x") and g.get("x_utm23s"):
            dist = math.hypot(float(g["x_utm23s"]) - float(c["x"]), float(g["y_utm23s"]) - float(c["y"]))
            conferiveis += 1

        if fora_bbox:
            veredito, motivo = "REPROVADO", "ponto geocodificado FORA do município de São Paulo (bbox IBGE 3550308)"
        elif dist != "" and dist > args.limiar:
            veredito, motivo = "REPROVADO", f"ponto a {dist:.0f} m do centroide OFICIAL do lote (limiar {args.limiar:.0f} m)"
        elif dist == "":
            veredito, motivo = "NAO_CONFERIVEL", "lote sem centroide oficial (sem_lote em lote_cidadao) — nada para confrontar"
        else:
            veredito, motivo = "APROVADO", f"ponto a {dist:.0f} m do centroide oficial do lote"

        if veredito == "REPROVADO":
            reprovados.add(sql)
        linhas.append([sql, r["zona"], g.get("endereco", ""),
                       "" if dist == "" else f"{dist:.0f}", fora_bbox, veredito, motivo])

    linhas.sort(key=lambda x: (x[5] != "REPROVADO", -(float(x[3]) if x[3] else 0)))
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sql_mestre", "zona_no_ssot", "endereco_geocodificado",
                    "dist_ao_centroide_oficial_m", "fora_do_municipio", "veredito", "motivo"])
        w.writerows(linhas)

    from collections import Counter
    c = Counter(x[5] for x in linhas)
    print("=== AUDITORIA DAS ZONAS GEOCODIFICADAS ===")
    print(f"linhas com fonte {MARCA_GEO} no SSOT: {len(linhas)}")
    print(f"  conferíveis contra centroide oficial: {conferiveis}")
    for k, v in c.most_common():
        print(f"  {k:15s}: {v}")
    print(f"limiar aplicado: {args.limiar:.0f} m")
    print("REPROVADOS (saem do SSOT — viram pendência declarada):")
    for x in linhas:
        if x[5] == "REPROVADO":
            print(f"  {x[0]} | zona={x[1]:<12} | {x[2]:<32} | {x[6]}")
    print(f"auditoria: {OUT.relative_to(RAIZ)}")

    if not args.aplicar:
        print("\n(dry-run — nada tocado no SSOT. Rode com --aplicar para remover os REPROVADOS.)")
        return 0

    if not reprovados:
        print("\nnada a remover.")
        return 0

    with open(SSOT, encoding="utf-8") as fh:
        rd = csv.reader(fh)
        header = next(rd)
        rows = [r for r in rd if r and r[0] not in reprovados]
    with open(SSOT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"\nSSOT: {len(ssot)} -> {len(rows)} linhas ({len(reprovados)} removidas, fail-closed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
