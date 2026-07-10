#!/usr/bin/env python3
"""Preenche o CAbás dos cedentes sob selo ZEPEC a partir da ZONA-BASE puxada do GeoSampa WFS.

Entrada:
  - zonas WFS: tools/geosampa/zonas_377.csv do hub (sql_mestre,zona_v3,zona_18177,status).
    zona_18177 = zoneamento ATUAL (Lei 16.402/2016 + 18.177/2024) -> tem CAbás no Quadro 3.
    zona_v3    = zoneamento ANTIGO (Lei 13.885/2004) -> só referência histórica.
  - Quadro 3: tabelas/quadro3-ca-por-zona.csv (zona -> ca_basico).
Saída:
  - zepec/oficial/zona_base_cedente.csv : SSOT da resolução (selo + zona-base + CAbás + fonte).
  - patch em zepec/oficial/zona_por_cedente.csv : para os alvos, zona<-zona-base, ca_basico<-mapeado,
    fonte cita 'GeoSampa WFS ... sob selo ZEPEC'. (número nasce de fonte determinística — 1.3/1.7.)
Uso: PU_REPO=. HUB=/workspace/portfolio-automacoes python3 scripts/preencher_cabas_do_wfs.py
"""
import csv, os, sys

REPO = os.environ.get("PU_REPO", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HUB = os.environ.get("HUB", "/workspace/portfolio-automacoes")
# Preferir o arquivo reconstruído da rodada BOA (run #7), no repo do PU; senão o do hub.
_LOCAL = os.path.join(REPO, "zepec/oficial/zonas_377_geosampa.csv")
WFS = os.environ.get("WFS_CSV") or (_LOCAL if os.path.exists(_LOCAL) else os.path.join(HUB, "tools/geosampa/zonas_377.csv"))
Q3 = os.path.join(REPO, "tabelas/quadro3-ca-por-zona.csv")
ZPC = os.path.join(REPO, "zepec/oficial/zona_por_cedente.csv")
OUT_BASE = os.path.join(REPO, "zepec/oficial/zona_base_cedente.csv")

def norm(z):
    return (z or "").strip()

# Quadro 3: zona -> (ca_basico, ca_max) (string BR, ex "1", "0,1", "2")
q3 = {}
with open(Q3) as f:
    for r in csv.reader(f):
        if not r or r[0].startswith("#") or r[0] == "zona":
            continue
        if len(r) >= 4:
            q3[norm(r[0]).upper()] = (norm(r[2]), norm(r[3]))

def camax_de(zona):
    v = q3.get(norm(zona).upper())
    return v[1] if v and v[1].upper() != "NA" else ""

def cabas_de(zona):
    z = norm(zona).upper()
    if not z or z in ("PRAÇA/CANTEIRO", "PRACA/CANTEIRO"):
        return "", "zona nao-edificavel/publica (sem CAbás; item coletivo)"
    if z == "ZOE":
        return "", "ZOE (Zona de Ocupação Especial): regime PRÓPRIO — CAbás definido por lei/plano específico do perímetro, NÃO pelo Quadro 3. Buscar o ato do ZOE."
    v = q3.get(z)
    if v is None:
        return "", f"zona '{zona}' fora do Quadro 3 (verificar)"
    if v[0].upper() == "NA":
        return "", f"zona '{zona}' com CAbás NA no Quadro 3"
    return v[0], ""

if not os.path.exists(WFS):
    print("ERRO: zonas_377.csv ainda não disponível em", WFS, file=sys.stderr); sys.exit(2)

# lê as zonas WFS
wfs = {}
with open(WFS) as f:
    for r in csv.DictReader(f):
        sql = norm(r.get("sql_mestre"))
        if len(sql) == 10:
            wfs[sql] = {"zona_v3": norm(r.get("zona_v3")), "zona_18177": norm(r.get("zona_18177")),
                        "na_aiu_sce": norm(r.get("na_aiu_sce")), "status": norm(r.get("status"))}

# monta a resolução (zona-base atual = zona_18177; fallback v3 se 18177 vazio)
base_rows = []
resolvidos = {}
for sql, d in sorted(wfs.items()):
    zbase = d["zona_18177"] or d["zona_v3"]
    cab, nota = cabas_de(zbase)
    cmax = camax_de(zbase)
    sce = d.get("na_aiu_sce", "")  # '1'/'0'/'?' do GeoSampa (perímetro AIU-SCE)
    if d.get("status") == "sem_lote":
        nota = "lote NÃO resolvido no GeoSampa (extinto/remembrado/condomínio) — reconsultar por matrícula/endereço"
    elif zbase in ("Praça/Canteiro", "Praca/Canteiro"):
        nota = "bem COLETIVO/público (praça/canteiro) — não-comercializável (G3, D-DONO-11)"
    resolvidos[sql] = (zbase, cab, nota, sce)
    base_rows.append([sql, "ZEPEC_APC", zbase, d["zona_v3"], cab, cmax, sce, nota,
                      "GeoSampa WFS perimetro_zona_lei_18177_24 + perímetro AIU-SCE (sob selo ZEPEC_APC)"])

with open(OUT_BASE, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["sql_mestre", "zona_selo", "zona_base_atual", "zona_base_2004", "ca_basico", "ca_max", "na_aiu_sce", "nota", "fonte"])
    w.writerows(base_rows)

# patch no zona_por_cedente.csv: para os alvos, zona<-zona-base atual, ca_basico<-mapeado
patched = 0
com_cabas = 0
rows = []
with open(ZPC) as f:
    rd = csv.reader(f)
    header = next(rd)
    if "na_aiu_sce" not in header:
        header = header + ["na_aiu_sce"]
    ncol = len(header)
    rows.append(header)
    for r in rd:
        if not r:
            continue
        while len(r) < ncol:  # garante a coluna nova
            r.append("")
        sql = norm(r[0])
        if sql in resolvidos:
            zbase, cab, nota, sce = resolvidos[sql]
            if zbase:
                r[1] = zbase
                r[2] = cab
                r[3] = "GeoSampa WFS (zona-base sob selo ZEPEC_APC)"
                r[ncol - 1] = sce
                patched += 1
                if cab:
                    com_cabas += 1
        rows.append(r)

with open(ZPC, "w", newline="") as f:
    csv.writer(f).writerows(rows)

# resumo
from collections import Counter
zc = Counter(v[0] for v in resolvidos.values())
sem = sum(1 for v in resolvidos.values() if not v[0])
sce_sim = sum(1 for v in resolvidos.values() if v[3] == "1")
print("=== RESULTADO ===")
print("alvos lidos (WFS):", len(wfs))
print("patch em zona_por_cedente:", patched, "| com CAbás:", com_cabas)
print("sem zona-base (sem_lote/vazio):", sem)
print("SSOT:", OUT_BASE)
print("na_aiu_sce=1 (FSCE aplicável):", sce_sim)
print("TOP zonas-base:", zc.most_common(12))
print("gabarito 0010800016 ->", resolvidos.get("0010800016"))
