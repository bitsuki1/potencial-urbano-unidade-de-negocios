#!/usr/bin/env python3
"""
embed_corpus.py — camada semântica (B-5): embute os chunks do corpus + as perguntas dos
ground-truth ATIVOS via Gemini (gemini-embedding-001, dim 768, normalizado), para o
retrieval híbrido (2.6: metadado → keyword → SEMÂNTICO).

RODA NA ACTION (embed.yml), que injeta GEMINI_API_KEY do segredo — a chave nunca sai do
servidor (doutrina de segredos). Saídas versionadas (o eval roda OFFLINE, sem chave):
  - rag/index/embeddings.json           : { chunk_id: base64(float32[768] normalizado) }
  - evals/ground-truth/query-embeddings.json : { sha1(pergunta): base64(...) }

taskType assimétrico: RETRIEVAL_DOCUMENT nos chunks, RETRIEVAL_QUERY nas perguntas
(melhora o casamento pergunta↔dispositivo). Determinístico: mesmo texto → mesmo vetor.
PU 18 · 2026-07-10 — B-5 destravado (chave Gemini confirmada no repo).
"""
import base64
import hashlib
import json
import math
import os
import struct
import sys
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CHUNKS_DIR = RAIZ / "rag" / "chunks"
GT_DIR = RAIZ / "evals" / "ground-truth"
OUT_CHUNKS = RAIZ / "rag" / "index" / "embeddings.json"
OUT_QUERIES = GT_DIR / "query-embeddings.json"

MODEL = "models/gemini-embedding-001"
DIM = 768
API = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:batchEmbedContents"
KEY = os.environ.get("GEMINI_API_KEY", "")
BATCH = 50
STATUS_PULA = {"aguardando_verbatim", "aguardando_engine", "aguardando_pgv", "confrontado_terreno", "inativo"}


def _norm(v):
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def _b64(v):
    return base64.b64encode(struct.pack(f"<{len(v)}f", *v)).decode("ascii")


def _post(reqs, task):
    body = json.dumps({"requests": [
        {"model": MODEL, "content": {"parts": [{"text": t}]},
         "taskType": task, "outputDimensionality": DIM} for t in reqs]}).encode()
    req = urllib.request.Request(f"{API}?key={KEY}", data=body,
                                 headers={"Content-Type": "application/json"})
    for tent in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read())
            return [_norm(e["values"]) for e in data["embeddings"]]
        except Exception as ex:
            if tent == 4:
                raise
            time.sleep(2 ** tent)


def embutir(pares, task, rotulo):
    """pares = [(chave, texto)]; devolve {chave: b64}."""
    out = {}
    total = len(pares)
    for i in range(0, total, BATCH):
        lote = pares[i:i + BATCH]
        vecs = _post([t for _, t in lote], task)
        for (chave, _), v in zip(lote, vecs):
            out[chave] = _b64(v)
        print(f"  {rotulo}: {min(i + BATCH, total)}/{total}", file=sys.stderr)
    return out


def main():
    if not KEY:
        sys.exit("SEM GEMINI_API_KEY — rode via embed.yml (Action).")

    # 1) chunks (RETRIEVAL_DOCUMENT) — texto de cada dispositivo citável
    chunks = []
    for jf in sorted(CHUNKS_DIR.rglob("*.json")):
        d = json.loads(jf.read_text(encoding="utf-8"))
        txt = (d.get("texto") or "").strip()
        if txt and d.get("chunk_id"):
            chunks.append((d["chunk_id"], txt[:8000]))
    print(f"chunks a embutir: {len(chunks)}", file=sys.stderr)
    emb_chunks = embutir(chunks, "RETRIEVAL_DOCUMENT", "chunks")
    OUT_CHUNKS.write_text(json.dumps({"_model": MODEL, "_dim": DIM, "vetores": emb_chunks},
                                     ensure_ascii=False), encoding="utf-8")

    # 2) perguntas dos ground-truth ATIVOS (RETRIEVAL_QUERY)
    perguntas = []
    for gf in sorted(GT_DIR.glob("*.json")):
        if gf.name == "query-embeddings.json":
            continue
        try:
            d = json.loads(gf.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("status") in STATUS_PULA:
            continue
        for it in (d.get("itens") or d.get("items") or d.get("casos") or []):
            q = (it.get("pergunta") or it.get("query") or it.get("consulta") or "").strip()
            if q:
                perguntas.append((hashlib.sha1(q.encode("utf-8")).hexdigest(), q))
    print(f"perguntas a embutir: {len(perguntas)}", file=sys.stderr)
    emb_q = embutir(perguntas, "RETRIEVAL_QUERY", "perguntas")
    OUT_QUERIES.write_text(json.dumps({"_model": MODEL, "_dim": DIM, "vetores": emb_q},
                                      ensure_ascii=False), encoding="utf-8")
    print(f"OK — {len(emb_chunks)} chunks + {len(emb_q)} perguntas embutidos.", file=sys.stderr)


if __name__ == "__main__":
    main()
