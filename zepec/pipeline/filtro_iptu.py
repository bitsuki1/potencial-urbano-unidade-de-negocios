#!/usr/bin/env python3
"""
filtro_iptu.py — recorta o IPTU_2026 completo pelos SQLs dos cedentes ZEPEC.

Entrada: stdin = IPTU_2026.csv (separador ;, encoding latin-1, via Supabase Storage).
         cedentes_sqls.txt (mesmo diretório) = um SQL por linha.
Saída:   zepec/oficial/iptu2026_cedentes.csv (path canônico do pipeline).

Uso:  curl -sS "$URL_IPTU" | python3 zepec/pipeline/filtro_iptu.py

Corrigido E1 (2026-07-10): output path alinhado ao pipeline README + colunas por NOME.
"""
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
SQLS_FILE = Path(__file__).resolve().parent / "cedentes_sqls.txt"
SAIDA = RAIZ / "zepec" / "oficial" / "iptu2026_cedentes.csv"

COLUNAS_IPTU = {
    "sql": 0,
    "codlog": 5,
    "logradouro": 6,
    "numero": 7,
    "area_terreno": 14,
    "area_construida": 15,
    "v_venal_m2": 17,
    "uso": 22,
    "padrao": 23,
}

sqls = set(SQLS_FILE.read_text().split())
sqls.discard("0000000000")

SAIDA.parent.mkdir(parents=True, exist_ok=True)
w = csv.writer(open(SAIDA, "w", newline="", encoding="utf-8"))
w.writerow(["sql_mestre", "area_terreno", "area_construida", "v_venal_m2",
            "codlog", "uso", "padrao", "endereco"])

n = hit = 0
rd = csv.reader(
    (l.decode("latin-1", "replace") for l in sys.stdin.buffer),
    delimiter=";",
)
next(rd, None)

for r in rd:
    n += 1
    if len(r) < 24:
        continue
    sql = r[COLUNAS_IPTU["sql"]].split("-")[0]
    if sql in sqls:
        hit += 1
        end = f"{r[COLUNAS_IPTU['logradouro']].strip()}, {r[COLUNAS_IPTU['numero']].strip()}"
        w.writerow([
            sql,
            r[COLUNAS_IPTU["area_terreno"]],
            r[COLUNAS_IPTU["area_construida"]],
            r[COLUNAS_IPTU["v_venal_m2"]],
            r[COLUNAS_IPTU["codlog"]],
            r[COLUNAS_IPTU["uso"]],
            r[COLUNAS_IPTU["padrao"]],
            end,
        ])

sys.stderr.write(f"filtro_iptu: lidas={n} casadas={hit}\n")
