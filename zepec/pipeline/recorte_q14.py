#!/usr/bin/env python3
"""
recorte_q14.py — recorta o Quadro 14 (valores de outorga por m²) pelos SQs dos cedentes ZEPEC.

Entrada: stdin = Atualizacao_Q14_anoref2025.csv (separador ; ou ,, via Supabase Storage).
         cedentes_sqls.txt (mesmo diretório) = um SQL por linha.
Saída:   zepec/oficial/q14_cedentes_2025.csv (path canônico do pipeline).

O recorte usa os primeiros 6 dígitos do SQL (setor+quadra = SQ) como chave de cruzamento,
porque o Q14 é indexado por SQ (não por lote individual).

Uso:  curl -sS "$URL_Q14" | python3 zepec/pipeline/recorte_q14.py

Criado E1 (2026-07-10): script que antes existia só em sessão efêmera (C9/MOTOR-2-ESTRATEGIA).
"""
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
SQLS_FILE = Path(__file__).resolve().parent / "cedentes_sqls.txt"
SAIDA = RAIZ / "zepec" / "oficial" / "q14_cedentes_2025.csv"

sqs = {sql[:6] for sql in SQLS_FILE.read_text().split() if sql != "0000000000"}

SAIDA.parent.mkdir(parents=True, exist_ok=True)
w = csv.writer(open(SAIDA, "w", newline="", encoding="utf-8"))
w.writerow(["sq", "codlog", "valor_m2_brl"])

n = hit = 0
delim = None
for raw_line in sys.stdin.buffer:
    line = raw_line.decode("utf-8", "replace")
    if delim is None:
        delim = ";" if ";" in line else ","
        continue  # skip header

    parts = line.strip().split(delim)
    n += 1
    if len(parts) < 3:
        continue
    sq = parts[0].strip().replace(".", "").replace("-", "")[:6]
    if sq in sqs:
        hit += 1
        codlog = parts[1].strip().replace(".", "").replace("-", "")
        valor = parts[2].strip().replace(",", ".")
        w.writerow([sq, codlog, valor])

sys.stderr.write(f"recorte_q14: lidas={n} casadas={hit} (SQs={len(sqs)})\n")
