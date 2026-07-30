#!/usr/bin/env python3
"""
carregar_tabelas_supabase.py — Loader determinístico e IDEMPOTENTE das tabelas de
referência do Motor 3 (dados legais, SEM PII) para o Postgres do Supabase
(projeto potencial-urbano-iptu-tdc, schema `motor3`).

Por que existe (C1 — migração motor-a-motor): o Motor 3 é a base de DADOS legal
(1.1 — tabela é dado, sai do texto; 1.3 — número nasce no engine, aqui só é
ARMAZENADO, rastreável ao dispositivo/lei). A fonte primária é `tabelas/*.csv`
do repo; este loader espelha CADA CSV em `motor3.t_<nome>` sem interpretar nada.

Fronteira de PII: este loader carrega SÓ as tabelas legais de referência (fatores,
faixas, Q14 de valor de terreno — dado público). NÃO toca cedentes (nome/CPF) —
esses são Motor 4 e só entram sob consentimento do dono (gate de PII).

Credencial (postura do cofre D106): a connection string do Postgres NÃO vive no
git — é lida do ambiente `SUPABASE_DB_URL` (GitHub Secret / painel Supabase →
Settings → Database → Connection string, modo `session`/`transaction`). As chaves
de poder total ficam fora do repo (cofre §Supabase).

Idempotente: para cada tabela, TRUNCATE + INSERT (recria o conteúdo a partir do
CSV a cada corrida). O schema (DDL) é criado pelas migrações do Supabase; aqui só
o DADO. As 4 tabelas-núcleo (iptu_aliquota_base/…_faixa/isencao_faixa/
atualizacao_anual) têm schema próprio e já foram carregadas via MCP — este loader
cuida das 15 tabelas genéricas `t_<nome>` (row_id identity + colunas do CSV).

Uso:
  SUPABASE_DB_URL='postgresql://...' python3 scripts/carregar_tabelas_supabase.py
  SUPABASE_DB_URL='postgresql://...' python3 scripts/carregar_tabelas_supabase.py --dry-run
"""
import csv
import os
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TABELAS = RAIZ / "tabelas"

# As 4 tabelas-núcleo têm schema bespoke e já foram carregadas (via MCP). Aqui, as genéricas.
NUCLEO_JA_CARREGADO = {
    "iptu-aliquota-base",
    "iptu-aliquotas-faixa",
    "iptu-isencao-faixa",
    "iptu-atualizacao-anual",
}

NUM = re.compile(r"^[+-]?\d+(\.\d+)?$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def ler_csv(path: Path):
    with open(path, encoding="utf-8") as f:
        rd = csv.reader(l for l in f if not l.lstrip().startswith("#"))
        linhas = list(rd)
    return linhas[0], linhas[1:]


def infer(vals):
    xs = [v for v in vals if v.strip() != ""]
    if not xs:
        return "text"
    if all(DATE.match(v) for v in xs):
        return "date"
    if all(NUM.match(v.replace("+", "")) for v in xs):
        return "numeric"
    return "text"


def sqlname(fn):  # nome do CSV -> nome da tabela
    return "t_" + fn.replace("-", "_")


def main(argv):
    dry = "--dry-run" in argv
    url = os.environ.get("SUPABASE_DB_URL")
    if not url and not dry:
        print("ERRO: defina SUPABASE_DB_URL (connection string do Postgres do Supabase).", file=sys.stderr)
        return 2

    alvos = []
    for csvf in sorted(TABELAS.glob("*.csv")):
        base = csvf.stem
        if base in NUCLEO_JA_CARREGADO:
            continue
        hdr, rows = ler_csv(csvf)
        types = [infer([r[i] if i < len(r) else "" for r in rows]) for i in range(len(hdr))]
        alvos.append((base, sqlname(base), hdr, types, rows))

    print(f"tabelas a carregar (genéricas Motor 3, sem PII): {len(alvos)}")
    for base, tn, hdr, types, rows in alvos:
        print(f"  motor3.{tn:34s} <- tabelas/{base}.csv  ({len(rows)} linhas)")

    if dry:
        print("DRY-RUN: nada gravado.")
        return 0

    import psycopg  # psycopg3

    total = 0
    with psycopg.connect(url, autocommit=False) as conn:
        with conn.cursor() as cur:
            for base, tn, hdr, types, rows in alvos:
                cur.execute(f"truncate table motor3.{tn} restart identity;")
                collist = ", ".join(f'"{c}"' for c in hdr)
                placeholders = ", ".join(["%s"] * len(hdr))
                sql = f"insert into motor3.{tn} ({collist}) values ({placeholders})"
                data = []
                for r in rows:
                    vals = []
                    for i in range(len(hdr)):
                        v = r[i] if i < len(r) else ""
                        v = v.strip()
                        if v == "":
                            vals.append(None)
                        elif types[i] == "numeric":
                            vals.append(v.replace("+", ""))
                        else:
                            vals.append(v)
                    data.append(vals)
                cur.executemany(sql, data)
                print(f"  OK  motor3.{tn}: {len(data)} linhas")
                total += len(data)
        conn.commit()
    print(f"FIM: {total} linhas carregadas em {len(alvos)} tabelas do Motor 3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
