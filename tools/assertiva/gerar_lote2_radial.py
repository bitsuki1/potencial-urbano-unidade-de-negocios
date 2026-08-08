#!/usr/bin/env python3
"""
gerar_lote2_radial.py — LOTE 2 da Assertiva, RADIAL A PARTIR DO MARCO ZERO (decisão do dono,
2026-08-07: "pegue o marco zero como ponto central e vá alimentando os dados lateralmente...
sobrou, aumenta o raio; pode gastar até R$300").

Monta a fila de donos ÚNICOS ainda não consultados, ordenada pela distância do imóvel mais
próximo ao Marco Zero de São Paulo (Praça da Sé). 1 consulta por documento — nunca paga duas
vezes pelo mesmo dado. Fontes (todas já no repo, extração pura 1.2):
  • casos-reais/tdc/LISTA-VENDEDORES-ENRIQUECIDA.csv → proprietario_doc/proprietario (Fase A+B)
  • zepec/oficial/centroides_cedentes.csv → x,y (SIRGAS2000/UTM23S, EPSG:31983)
  • tools/assertiva/alvos_lote1_100.csv → exclusão (lote 1 já pago)
Exclui públicos (publico_privado='publico': Prefeitura/União etc. não são alvo comercial).
Saída: tools/assertiva/alvos_lote2_radial.csv (mesmo schema do lote 1 + dist_m; tier = faixa
de raio em km). O executor (extrair_lote.py --alvos) corta pelo --limite = controle de gasto.
"""
import csv
import math
from pathlib import Path

AQUI = Path(__file__).parent
RAIZ = AQUI.parent.parent

# Marco Zero (Praça da Sé) → UTM 23S EPSG:31983 (mesma projeção manual do geocodificar_474.js)
MZ_LAT, MZ_LON = -23.55049, -46.63394


def utm23s(lat, lon):
    a, f, k0 = 6378137.0, 1 / 298.257222101, 0.9996
    lon0 = math.radians(-45)
    e2 = f * (2 - f)
    ep2 = e2 / (1 - e2)
    la, lo = math.radians(lat), math.radians(lon)
    N = a / math.sqrt(1 - e2 * math.sin(la) ** 2)
    T = math.tan(la) ** 2
    C = ep2 * math.cos(la) ** 2
    A = math.cos(la) * (lo - lon0)
    M = a * ((1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 ** 3 / 256) * la
             - (3 * e2 / 8 + 3 * e2 * e2 / 32 + 45 * e2 ** 3 / 1024) * math.sin(2 * la)
             + (15 * e2 * e2 / 256 + 45 * e2 ** 3 / 1024) * math.sin(4 * la)
             - (35 * e2 ** 3 / 3072) * math.sin(6 * la))
    x = k0 * N * (A + (1 - T + C) * A ** 3 / 6
                  + (5 - 18 * T + T * T + 72 * C - 58 * ep2) * A ** 5 / 120) + 500000
    y = k0 * (M + N * math.tan(la) * (A * A / 2 + (5 - T + 9 * C + 4 * C * C) * A ** 4 / 24
              + (61 - 58 * T + T * T + 600 * C - 330 * ep2) * A ** 6 / 720)) + 10000000
    return x, y


def main():
    mzx, mzy = utm23s(MZ_LAT, MZ_LON)

    ponto = {}
    for r in csv.DictReader(open(RAIZ / "zepec/oficial/centroides_cedentes.csv", encoding="utf-8")):
        if r.get("x") and r.get("y"):
            ponto[r["sql_mestre"]] = (float(r["x"]), float(r["y"]))

    ja = {r["proprietario_doc"].strip()
          for r in csv.DictReader(open(AQUI / "alvos_lote1_100.csv", encoding="utf-8"))}

    donos = {}   # doc -> {nome, sqls[], dist}
    total = com_doc = publicos = 0
    for r in csv.DictReader(open(RAIZ / "casos-reais/tdc/LISTA-VENDEDORES-ENRIQUECIDA.csv",
                                 encoding="utf-8")):
        total += 1
        doc = "".join(c for c in (r.get("proprietario_doc") or "") if c.isdigit())
        if len(doc) not in (11, 14):
            continue          # sem documento válido (ou mascarado) → não tem como consultar
        com_doc += 1
        if (r.get("publico_privado") or "").strip().lower() == "publico":
            publicos += 1
            continue
        if doc in ja:
            continue
        sql = "".join(c for c in (r.get("sql") or "") if c.isdigit())[:10]
        d = donos.setdefault(doc, {"nome": (r.get("proprietario") or "").strip(),
                                   "sqls": [], "dist": None})
        if len(sql) == 10 and sql not in d["sqls"]:
            d["sqls"].append(sql)
        p = ponto.get(sql)
        if p:
            dist = math.hypot(p[0] - mzx, p[1] - mzy)
            if d["dist"] is None or dist < d["dist"]:
                d["dist"] = dist

    fila = sorted(donos.items(), key=lambda kv: (kv[1]["dist"] is None,
                                                 kv[1]["dist"] or 0.0))
    fonte = "IPTU 2026 + ZEPEC/DEUSO + Quadro 14 + FUNDURB (recortes oficiais)"
    out = AQUI / "alvos_lote2_radial.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["proprietario_doc", "proprietario", "fonte_nome", "tier", "sqls", "dist_m"])
        for doc, d in fila:
            faixa = "sem_ponto" if d["dist"] is None else str(int(d["dist"] // 1000))
            w.writerow([doc, d["nome"], fonte, faixa, ";".join(d["sqls"]),
                        "" if d["dist"] is None else f"{d['dist']:.0f}"])

    print(f"universo: {total} imóveis | {com_doc} com documento válido | públicos fora: {publicos}")
    print(f"fila radial: {len(fila)} donos únicos (lote 1 excluído: {len(ja)})")
    for km in (1, 2, 5, 10):
        n = sum(1 for _, d in fila if d["dist"] is not None and d["dist"] <= km * 1000)
        print(f"  até {km} km do Marco Zero: {n} donos")
    sem = sum(1 for _, d in fila if d["dist"] is None)
    print(f"  sem centroide (fim da fila): {sem}")


if __name__ == "__main__":
    main()
