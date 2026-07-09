#!/usr/bin/env python3
"""
resolver_zona_geosampa.py — preenche CAbás dos cedentes ZEPEC sem zona-base.

Fontes (cadeia rastreável):
  1. GeoSampa SISZON (Lei 18.177/2024 + v3) — zona-base sob o selo, por SQL
     hub: portfolio-automacoes/tools/geosampa/zonas_377.csv
  2. Quadro 3 da LPUOS (Lei 16.402/2016) — CAbás por zona
     tabelas/quadro3-ca-por-zona.csv
  3. Quadro 2A do PDE — CAbás por macroárea (para ZOE: CAbás=1)

Lê:  zepec/oficial/zona_por_cedente.csv   (SSOT das zonas por cedente)
Grava: mesmo arquivo, com ca_basico preenchido onde antes era vazio.

Princípio 1.3: número nasce da tabela (Quadro 3), não do LLM.
"""
import csv, os, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
HUB = REPO.parent / "portfolio-automacoes"

ZONAS_GEO = HUB / "tools/geosampa/zonas_377.csv"
QUADRO3 = REPO / "tabelas/quadro3-ca-por-zona.csv"
ZONA_CSV = REPO / "zepec/oficial/zona_por_cedente.csv"

def carregar_quadro3():
    """zona → ca_basico (string, formato BR '0,6' ou '1')."""
    m = {}
    with open(QUADRO3, encoding="utf-8") as f:
        lines = [l for l in f if not l.startswith("#")]
    for r in csv.DictReader(lines):
        z = r["zona"].strip()
        cab = r["ca_basico"].strip()
        if z and cab and cab != "NA":
            m[z] = cab
    # ZOE: CAbás = 1 (Quadro 2A — consistente com os 77 já resolvidos no overlay_zona.py)
    m["ZOE"] = "1"
    return m

def carregar_geosampa():
    """sql_mestre → {zona_v3, zona_18177, status}."""
    g = {}
    with open(ZONAS_GEO, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sql = r["sql_mestre"].strip()
            if sql:
                g[sql] = {
                    "zona_v3": r.get("zona_v3", "").strip(),
                    "zona_18177": r.get("zona_18177", "").strip(),
                    "status": r.get("status", "").strip(),
                }
    return g

def resolver(zona_18177, zona_v3, q3):
    """Retorna (zona_usada, ca_basico, fonte) ou (None, None, None)."""
    # 1ª tentativa: zona_18177 no Quadro 3
    if zona_18177 and zona_18177 in q3 and zona_18177 != "Praça/Canteiro":
        return zona_18177, q3[zona_18177], f"GeoSampa(Lei18177→{zona_18177})+Q3"

    # 2ª tentativa: zona_v3 no Quadro 3
    if zona_v3 and zona_v3 in q3:
        return zona_v3, q3[zona_v3], f"GeoSampa(v3→{zona_v3})+Q3"

    # 3ª tentativa: zona_v3 é subdivião nova (ZCP-a, ZM-1 etc.) → CAbás=1 (PDE Art.14 §1º)
    # PDE Art.14 §1º: "Os coeficientes de aproveitamento básico são iguais a 1 em todo o Município"
    # Exceções explícitas do Quadro 3: ZEPAM(0.1), ZPDSr(0.2), AC-1(0.6), AC-2(0.4), AVP-1(NA)
    zonas_excecao = {"ZEPAM", "ZPDSr", "AC-1", "AC-2", "AVP-1"}
    if zona_v3 and zona_v3 not in zonas_excecao:
        return zona_v3, "1", f"GeoSampa(v3→{zona_v3})+PDE_Art14§1"

    # fallback: zona_18177 = Praça/Canteiro sem zona_v3 → irresolvível
    return None, None, None

def main():
    q3 = carregar_quadro3()
    geo = carregar_geosampa()

    with open(ZONA_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    campos = rows[0].keys() if rows else ["sql_mestre", "zona", "ca_basico", "fonte"]

    stats = {"ja_tinha": 0, "resolvido": 0, "sem_lote": 0, "irresolvivel": 0, "sem_geo": 0}
    for r in rows:
        sql = r["sql_mestre"].strip()
        cab_atual = r.get("ca_basico", "").strip()

        if cab_atual:
            stats["ja_tinha"] += 1
            continue

        g = geo.get(sql)
        if not g:
            stats["sem_geo"] += 1
            continue

        if g["status"] != "ok":
            stats["sem_lote"] += 1
            continue

        zona_usada, cab, fonte = resolver(g["zona_18177"], g["zona_v3"], q3)
        if zona_usada:
            r["zona"] = zona_usada
            r["ca_basico"] = cab.replace(",", ".")  # normaliza decimal BR→ponto
            r["fonte"] = fonte
            stats["resolvido"] += 1
        else:
            stats["irresolvivel"] += 1

    with open(ZONA_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(rows)

    print("=== resolver_zona_geosampa ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    total_cab = sum(1 for r in rows if r.get("ca_basico", "").strip())
    print(f"  ca_basico total: {total_cab}/{len(rows)}")
    return 0 if stats["resolvido"] > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
