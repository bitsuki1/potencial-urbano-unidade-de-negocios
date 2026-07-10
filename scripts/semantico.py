#!/usr/bin/env python3
"""
semantico.py — camada de SIGNIFICADO do retrieval híbrido (2.6, etapa 3).
Lê os vetores de rag/index/embeddings.json (gerados por embed_corpus.py na Action) e
ranqueia chunks por similaridade de cosseno com um vetor de consulta. Também combina o
ranking semântico com o de palavra-chave (BM25) por Reciprocal Rank Fusion (RRF).

stdlib-only, determinístico, SEM chamar API (os vetores já vêm prontos) — o gate roda
offline. O único passo que usa a chave Gemini é o embed_corpus.py (na Action).
PU 18 · 2026-07-10 — B-5.
"""
import base64
import json
import struct
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EMB_CHUNKS = RAIZ / "rag" / "index" / "embeddings.json"


def _decode(b64):
    raw = base64.b64decode(b64)
    return struct.unpack(f"<{len(raw)//4}f", raw)


def carregar_vetores(path=EMB_CHUNKS):
    """{chunk_id: tuple(float)} — vazio se o arquivo ainda não foi gerado."""
    if not Path(path).exists():
        return {}
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return {k: _decode(v) for k, v in d.get("vetores", {}).items()}


def cosseno_rank(qvec, vetores, top=None):
    """Ranqueia chunk_ids por produto interno (vetores já normalizados = cosseno).
    Devolve [(chunk_id, score)] decrescente."""
    q = qvec
    escores = [(cid, sum(a * b for a, b in zip(q, v))) for cid, v in vetores.items()]
    escores.sort(key=lambda t: t[1], reverse=True)
    return escores[:top] if top else escores


def rrf(*rankings, k=60, top=None):
    """Reciprocal Rank Fusion de várias listas ordenadas de chunk_ids.
    score(c) = Σ 1/(k + posição_c_no_ranking). Robusto a escalas diferentes (BM25 × cosseno)."""
    agg = {}
    for r in rankings:
        for pos, cid in enumerate(r):
            agg[cid] = agg.get(cid, 0.0) + 1.0 / (k + pos + 1)
    out = sorted(agg.items(), key=lambda t: t[1], reverse=True)
    return [c for c, _ in (out[:top] if top else out)]


def query_vec(sha1_or_map, mapa_perguntas):
    """Helper: recupera o vetor de uma pergunta pelo sha1 (do query-embeddings.json)."""
    return mapa_perguntas.get(sha1_or_map)


MODEL = "models/gemini-embedding-001"
DIM = 768


def embed_query(texto):
    """Embute UMA pergunta ao vivo (RETRIEVAL_QUERY) via Gemini — SÓ se GEMINI_API_KEY estiver
    no ambiente. Devolve vetor normalizado ou None (queda graciosa: sem chave → sem semântico,
    o retrieval segue keyword-only). Nunca é chamado no gate (que roda sem a chave)."""
    import os
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    import json as _j
    import math as _m
    import urllib.request as _u
    body = _j.dumps({"model": MODEL, "content": {"parts": [{"text": texto[:8000]}]},
                     "taskType": "RETRIEVAL_QUERY", "outputDimensionality": DIM}).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:embedContent?key={key}"
    try:
        with _u.urlopen(_u.Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=30) as r:
            v = _j.loads(r.read())["embedding"]["values"]
        n = _m.sqrt(sum(x * x for x in v)) or 1.0
        return [x / n for x in v]
    except Exception:
        return None
