#!/usr/bin/env python3
"""
carregar_tabelas_supabase.py — Loader determinístico e IDEMPOTENTE das tabelas de
referência do Motor 3 (dados legais, SEM PII) para o Postgres do Supabase
(projeto potencial-urbano-iptu-tdc, schema `motor3`).

Por que existe (C1 — migração motor-a-motor): o Motor 3 é a base de DADOS legal
(1.1 — tabela é dado, sai do texto; 1.3 — número nasce no engine, aqui só é
ARMAZENADO, rastreável ao dispositivo/lei). A fonte primária é `tabelas/*.csv`
do repo; este loader espelha CADA CSV em `motor3.t_<nome>` sem interpretar nada.

Fronteira de PII: carrega as tabelas legais (Motor 3, sem PII) E os cedentes
(Motor 4) — estes só porque o dono CONSENTIU a migração (2026-07-30). Os cedentes
vêm de zepec/oficial/ (fonte primária; 1.8) e vão para o schema motor4 com RLS
só-dono. Rode com `--sem-cedentes` para carregar apenas o Motor 3. Como a carga roda
por este loader (via SUPABASE_DB_URL), o dado sensível NÃO passa pelo contexto do LLM.

Credencial (postura do cofre D106): a connection string do Postgres NÃO vive no
git — é lida do ambiente `SUPABASE_DB_URL` (GitHub Secret / painel Supabase →
Settings → Database → Connection string, modo `session`/`transaction`). As chaves
de poder total ficam fora do repo (cofre §Supabase).

Idempotente: para cada tabela, TRUNCATE + INSERT (recria o conteúdo a partir do
CSV a cada corrida). O schema (DDL) é criado pelas migrações do Supabase; aqui só
o DADO. As 4 tabelas-núcleo (iptu_aliquota_base/…_faixa/isencao_faixa/
atualizacao_anual) têm schema próprio e já foram carregadas via MCP — este loader
cuida das 15 tabelas genéricas `t_<nome>` (row_id identity + colunas do CSV).

Motor 1 (RAG): além das tabelas, este loader também carrega o corpus indexado em
`motor1.chunks` (rag/index/chunks.json + embeddings.json → texto + metadados de
filtro + vetor pgvector 768d, modelo gemini-embedding-001). SEM PII (texto
normativo). Desligue com `--sem-motor1`.

Uso:
  SUPABASE_DB_URL='postgresql://...' python3 scripts/carregar_tabelas_supabase.py
  SUPABASE_DB_URL='postgresql://...' python3 scripts/carregar_tabelas_supabase.py --dry-run
  Flags: --sem-cedentes (pula Motor 4)  ·  --sem-motor1 (pula o corpus RAG)
"""
import base64
import csv
import json
import os
import re
import struct
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TABELAS = RAIZ / "tabelas"
RAG_INDEX = RAIZ / "rag" / "index"

# As 4 tabelas-núcleo têm schema bespoke e já foram carregadas (via MCP). Aqui, as genéricas.
NUCLEO_JA_CARREGADO = {
    "iptu-aliquota-base",
    "iptu-aliquotas-faixa",
    "iptu-isencao-faixa",
    "iptu-atualizacao-anual",
}

# Motor 4 — CEDENTES (migração CONSENTIDA pelo dono 2026-07-30). Fonte primária = zepec/oficial/
# (1.8: o derivado zepec/ferramenta/ NÃO é fonte). Chave canônica = sql_mestre. Colunas text no schema
# motor4 (RLS só-dono). Só entra aqui o que o dono consentiu; a carga real roda pelo loader (via secret),
# então o dado sensível NÃO passa pelo contexto do assistente.
CEDENTES_OFICIAL = {
    "zepec/oficial/q14_cedentes_2026_oficial.csv": "motor4.c_q14_cedentes_2026_oficial",
    "zepec/oficial/iptu2026_cedentes.csv": "motor4.c_iptu2026_cedentes",
    "zepec/oficial/zona_por_cedente.csv": "motor4.c_zona_por_cedente",
    "zepec/oficial/conservacao_cedentes.csv": "motor4.c_conservacao_cedentes",
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


# ---- Motor 1 (RAG do corpus): chunks + embeddings -> motor1.chunks ----
_JSONB_COLS = ("caminho_hierarquico", "vigencia_dispositivo", "citacao", "tema", "dominio")
_TEXT_COLS = ("lei_id", "tipo_dispositivo", "rotulo", "numero", "header_raw",
              "texto", "dominio_primario", "jurisdicao", "ementa")


def _emb_para_vetor(b64):
    """base64 (float32 little-endian) -> literal pgvector '[..]' ou None."""
    if not b64:
        return None
    raw = base64.b64decode(b64)
    n = len(raw) // 4
    arr = struct.unpack(f"<{n}f", raw)
    return "[" + ",".join(repr(x) for x in arr) + "]"


def _contar_motor1():
    chunks = json.loads((RAG_INDEX / "chunks.json").read_text(encoding="utf-8"))
    emb = json.loads((RAG_INDEX / "embeddings.json").read_text(encoding="utf-8"))
    vet = emb.get("vetores", {})
    return len(chunks), len(vet), emb.get("_dim")


def carregar_motor1(cur):
    """TRUNCATE + INSERT dos chunks do corpus (rag/index/chunks.json + embeddings.json)."""
    chunks = json.loads((RAG_INDEX / "chunks.json").read_text(encoding="utf-8"))
    vet = json.loads((RAG_INDEX / "embeddings.json").read_text(encoding="utf-8")).get("vetores", {})
    cols = ["chunk_id"] + list(_TEXT_COLS) + ["citavel"] + list(_JSONB_COLS) + ["embedding"]
    collist = ", ".join(f'"{c}"' for c in cols)
    ph = ", ".join(["%s"] * (len(cols) - 1)) + ", %s::vector"  # última = embedding
    sql = f"insert into motor1.chunks ({collist}) values ({ph})"
    cur.execute("truncate table motor1.chunks;")
    data = []
    for cid, ch in chunks.items():
        vals = [cid]
        for c in _TEXT_COLS:
            v = ch.get(c)
            vals.append(v if isinstance(v, str) else (None if v is None else str(v)))
        cit = ch.get("citavel")
        vals.append(bool(cit) if cit is not None else None)
        for c in _JSONB_COLS:
            v = ch.get(c)
            vals.append(json.dumps(v, ensure_ascii=False) if v is not None else None)
        vals.append(_emb_para_vetor(vet.get(cid)))
        data.append(vals)
    cur.executemany(sql, data)
    com_emb = sum(1 for cid in chunks if vet.get(cid))
    print(f"  OK  motor1.chunks: {len(data)} chunks ({com_emb} com embedding)")
    return len(data)


def _conectar(url):
    """Conecta ao Postgres do Supabase. O pooler (Supavisor) fica em fleets
    regionais (`aws-0-<regiao>` / `aws-1-<regiao>`); um projeto só existe em UM
    deles. Se o host informado for o fleet errado, o pooler recusa com
    'tenant/user ... not found' (não é senha errada). Nesse caso trocamos
    aws-0<->aws-1 e reconectamos sozinhos — assim o loader se recupera de um
    host de pooler defasado no secret, sem intervenção manual.
    """
    import re as _re
    import psycopg  # psycopg3

    candidatos = [url]
    m = _re.search(r"aws-(\d)-", url)
    if m:
        alt = "0" if m.group(1) != "0" else "1"
        candidatos.append(_re.sub(r"aws-\d-", f"aws-{alt}-", url, count=1))
    ultimo = None
    for i, u in enumerate(candidatos):
        try:
            conn = psycopg.connect(u, autocommit=False)
            if i > 0:
                hm = _re.search(r"@([^:/]+)", u)
                print(f"  (reconectado pelo fleet alternado do pooler: {hm.group(1) if hm else '?'})")
            return conn
        except psycopg.OperationalError as e:
            ultimo = e
            msg = str(e).lower()
            if "not found" in msg or "enotfound" in msg or "tenant" in msg:
                continue  # provável fleet errado — tenta o alternado
            raise
    raise ultimo


def main(argv):
    dry = "--dry-run" in argv
    url = os.environ.get("SUPABASE_DB_URL")
    if not url and not dry:
        print("ERRO: defina SUPABASE_DB_URL (connection string do Postgres do Supabase).", file=sys.stderr)
        return 2

    incluir_cedentes = "--sem-cedentes" not in argv
    # alvo = (rótulo_fonte, alvo_schema_tabela, hdr, types, rows)
    alvos = []
    for csvf in sorted(TABELAS.glob("*.csv")):
        base = csvf.stem
        if base in NUCLEO_JA_CARREGADO:
            continue
        hdr, rows = ler_csv(csvf)
        types = [infer([r[i] if i < len(r) else "" for r in rows]) for i in range(len(hdr))]
        alvos.append((f"tabelas/{base}.csv", f"motor3.{sqlname(base)}", hdr, types, rows))

    # Motor 4 — cedentes (consentido). Todas as colunas são text no schema; passamos strings.
    if incluir_cedentes:
        for relpath, alvo in CEDENTES_OFICIAL.items():
            csvf = RAIZ / relpath
            if not csvf.exists():
                print(f"AVISO: {relpath} não encontrado — pulando.")
                continue
            hdr, rows = ler_csv(csvf)
            types = ["text"] * len(hdr)  # motor4 é text-only (preserva o dado exato)
            alvos.append((relpath, alvo, hdr, types, rows))

    incluir_motor1 = "--sem-motor1" not in argv
    print(f"alvos a carregar: {len(alvos)}  (Motor 3 sem PII + Motor 4 cedentes {'INCLUÍDOS' if incluir_cedentes else 'EXCLUÍDOS'})")
    for fonte, alvo, hdr, types, rows in alvos:
        print(f"  {alvo:40s} <- {fonte}  ({len(rows)} linhas)")
    if incluir_motor1:
        nch, nemb, dim = _contar_motor1()
        print(f"  motor1.chunks                            <- rag/index/chunks.json + embeddings.json  ({nch} chunks, {nemb} c/ embedding dim {dim})")

    if dry:
        print("DRY-RUN: nada gravado.")
        return 0

    total = 0
    with _conectar(url) as conn:
        with conn.cursor() as cur:
            for fonte, alvo, hdr, types, rows in alvos:
                cur.execute(f"truncate table {alvo} restart identity;")
                collist = ", ".join(f'"{c}"' for c in hdr)
                placeholders = ", ".join(["%s"] * len(hdr))
                sql = f"insert into {alvo} ({collist}) values ({placeholders})"
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
                print(f"  OK  {alvo}: {len(data)} linhas")
                total += len(data)
            if incluir_motor1:
                total += carregar_motor1(cur)
        conn.commit()
    print(f"FIM: {total} linhas carregadas ({len(alvos)} tabelas Motor 3/4"
          f"{' + motor1.chunks' if incluir_motor1 else ''}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
