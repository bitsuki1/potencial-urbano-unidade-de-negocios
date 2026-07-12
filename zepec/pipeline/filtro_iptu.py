#!/usr/bin/env python3
"""
filtro_iptu.py — recorta o IPTU_2026 completo pelos SQLs dos cedentes ZEPEC.

Entrada: stdin = IPTU_2026.csv (separador ';', do Supabase Storage bucket dados-produto).
         cedentes_sqls.txt (mesmo diretório) = um SQL por linha (10 dígitos).
Saída:   zepec/oficial/iptu2026_cedentes.csv (path canônico do pipeline).

Uso:  curl -sS "$URL_ASSINADA_IPTU" | python3 zepec/pipeline/filtro_iptu.py

CORREÇÃO 2026-07-10 (PU 18): o mapa de colunas foi refeito contra o CABEÇALHO REAL do
arquivo (29 colunas). O extrator antigo rotulava a coluna 17 como `v_venal_m2`, mas ela é
**VALOR DO M2 DO TERRENO** — bug provado 3905/3905. Aproveitando, passam a ser extraídas as
colunas que faltavam para o motor IPTU confrontar o valor venal: valor m² de construção (18),
ano da construção (19), fator de obsolescência oficial (25), tipo de terreno (24), esquinas
(12) e fração ideal (13). O arquivo é UTF-8 (texto com acento vinha como mojibake sob latin-1;
`_fix` repara). Encoding e cabeçalho descobertos na extração via Edge Function de uso único.
"""
import csv
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
SQLS_FILE = Path(__file__).resolve().parent / "cedentes_sqls.txt"
SAIDA = RAIZ / "zepec" / "oficial" / "iptu2026_cedentes.csv"

# índice REAL das colunas no cabeçalho oficial do IPTU_2026.csv (0-based)
COL = {
    "sql": 0,               # NUMERO DO CONTRIBUINTE
    "codlog": 5,            # CODLOG DO IMOVEL
    "logradouro": 6,
    "numero": 7,
    "esquinas": 12,         # QUANTIDADE DE ESQUINAS/FRENTES
    "fracao_ideal": 13,     # FRACAO IDEAL
    "area_terreno": 14,     # AREA DO TERRENO (Atc)
    "area_construida": 15,  # AREA CONSTRUIDA
    "valor_m2_terreno": 17,     # VALOR DO M2 DO TERRENO (era mal-rotulado v_venal_m2)
    "valor_m2_construcao": 18,  # VALOR DO M2 DE CONSTRUCAO
    "ano_construcao": 19,       # ANO DA CONSTRUCAO CORRIGIDO
    "uso": 22,              # TIPO DE USO DO IMOVEL
    "padrao": 23,           # TIPO DE PADRAO DA CONSTRUCAO
    "tipo_terreno": 24,     # TIPO DE TERRENO (Normal/De esquina/interno/fundos/encravado)
    "fator_obs": 25,        # FATOR DE OBSOLESCENCIA (aplicado pela Prefeitura)
}


def _fix(s):
    """Repara mojibake (UTF-8 lido como latin-1); ASCII intacto."""
    try:
        return s.encode("latin-1").decode("utf-8")
    except Exception:
        return s


def _sql10(s):
    return re.sub(r"\D", "", s)[:10]


sqls = {_sql10(x) for x in SQLS_FILE.read_text().split()}
sqls.discard("0000000000")

SAIDA.parent.mkdir(parents=True, exist_ok=True)
w = csv.writer(open(SAIDA, "w", newline="", encoding="utf-8"))
w.writerow(["sql_mestre", "area_terreno", "area_construida", "valor_m2_terreno",
            "valor_m2_construcao", "ano_construcao", "fator_obsolescencia_oficial",
            "tipo_terreno", "esquinas_frentes", "fracao_ideal", "codlog", "uso", "padrao", "endereco"])

rd = csv.reader((l.decode("utf-8", "replace") for l in sys.stdin.buffer), delimiter=";")
next(rd, None)
n = hit = 0
for r in rd:
    n += 1
    if len(r) < 26:
        continue
    if _sql10(r[COL["sql"]]) in sqls:
        hit += 1
        end = f"{_fix(r[COL['logradouro']]).strip()}, {r[COL['numero']].strip()}"
        w.writerow([
            _sql10(r[COL["sql"]]), r[COL["area_terreno"]], r[COL["area_construida"]],
            r[COL["valor_m2_terreno"]], r[COL["valor_m2_construcao"]], r[COL["ano_construcao"]],
            r[COL["fator_obs"]], _fix(r[COL["tipo_terreno"]]), r[COL["esquinas"]],
            r[COL["fracao_ideal"]], r[COL["codlog"]], _fix(r[COL["uso"]]), _fix(r[COL["padrao"]]), end,
        ])
sys.stderr.write(f"filtro_iptu: lidas={n} casadas={hit}\n")
