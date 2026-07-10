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
