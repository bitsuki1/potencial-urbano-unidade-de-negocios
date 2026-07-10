#!/usr/bin/env python3
"""Gate de regressão da ZONA-BASE/CAbás resolvidos do GeoSampa (2026-07-08).
FALHA (exit 1) se a resolução do gabarito regredir ou se a cobertura de CAbás cair muito.
Fonte: zepec/oficial/zona_base_cedente.csv (gerado por scripts/preencher_cabas_do_wfs.py)."""
import csv, os, sys
base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "zepec", "oficial", "zona_base_cedente.csv")
rows = list(csv.DictReader(open(base, encoding="utf-8")))
by = {r["sql_mestre"]: r for r in rows}
erros = []
# 1) gabarito 006: 0010800016 -> zona-base ZC, CAbás 1
g = by.get("0010800016")
if not g or g.get("zona_base_atual") != "ZC" or g.get("ca_basico") not in ("1", "1.0"):
    erros.append(f"gabarito 0010800016 esperava ZC/CAbás=1, veio {g and (g.get('zona_base_atual'), g.get('ca_basico'))}")
# 2) cobertura mínima de CAbás (fill do GeoSampa) — guarda contra rodada throttled
com_cabas = sum(1 for r in rows if (r.get("ca_basico") or "").strip())
if com_cabas < 300:
    erros.append(f"cobertura CAbás caiu para {com_cabas} (<300) — rodada GeoSampa possivelmente throttled")
if erros:
    print("EVAL ZONA/CAbás FALHOU:"); [print(" -", e) for e in erros]; sys.exit(1)
print(f"EVAL ZONA/CAbás OK: gabarito 0010800016=ZC/1; {com_cabas} cedentes com CAbás.")
