#!/usr/bin/env python3
"""
indexar.py — Constrói o índice de RAG a partir dos chunks (CLAUDE.md 2.6).

Lê:  rag/chunks/<lei_id>/*.json   (saída do fatiar.py)
Escreve:
    rag/index/chunks.json     — store: chunk_id -> chunk completo (para a consulta citar)
    rag/index/invertido.json  — índice invertido token -> {chunk_id: tf}, + df e N (p/ TF-IDF)
    rag/index/metadados.json   — por chunk: lei_id, tema, jurisdicao, vigencia (filtro pré-busca 2.6)

Determinístico, stdlib-only, SEM LLM e SEM embeddings (1.3/1.4): o retrieval híbrido aqui é
filtro-por-metadado + keyword (TF-IDF). A camada semântica (embeddings) é uma extensão FUTURA,
plugável neste mesmo índice — fica explicitamente como gancho, não implementada às cegas.

Atualiza status_pipeline das leis indexadas: fatiado -> indexado.

Trazido pela instância orquestradora do Potencial Urbano — 2026-06-20.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _texto import tokenizar  # noqa: E402  (tokenização canônica compartilhada)

RAIZ = Path(__file__).resolve().parent.parent
CHUNKS_DIR = RAIZ / "rag" / "chunks"
INDEX_DIR = RAIZ / "rag" / "index"


def carregar_chunks():
    chunks = []
    if CHUNKS_DIR.exists():
        for jpath in sorted(CHUNKS_DIR.rglob("*.json")):
            chunks.append(json.loads(jpath.read_text(encoding="utf-8")))
    return chunks


def main():
    chunks = carregar_chunks()
    if not chunks:
        print("indexar: nenhum chunk em rag/chunks/ — rode fatiar.py antes.", file=sys.stderr)
        # ainda assim escreve índices vazios (idempotência)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    store = {}
    metadados = {}
    invertido = {}   # token -> {chunk_id: tf}
    df = {}          # token -> nº de chunks que o contêm
    doclen = {}      # chunk_id -> nº de tokens (para normalização de tamanho BM25)

    for c in chunks:
        cid = c["chunk_id"]
        store[cid] = c
        metadados[cid] = {
            "lei_id": c.get("lei_id"),
            "tipo_dispositivo": c.get("tipo_dispositivo"),
            "rotulo": c.get("rotulo"),
            "tema": c.get("tema", []),
            # Separação TDC×IPTU: domínio como FACETA filtrável (não texto). O filtro pré-busca (2.6)
            # inclui sempre 'compartilhado' nas consultas dos dois domínios — ver consultar.filtrar().
            "dominio": c.get("dominio", []),
            "dominio_primario": c.get("dominio_primario"),
            "jurisdicao": c.get("jurisdicao"),
            "vigencia": (c.get("citacao") or {}).get("vigencia", {}),
            # B-11c: vigência por dispositivo (revogado/compilado/original) p/ o filtro pré-busca (2.6).
            "vigencia_dispositivo": c.get("vigencia_dispositivo", {"status": "original"}),
            # B-11d: dispositivo citável (preâmbulo/boilerplate = não-citável) p/ o filtro pré-busca.
            "citavel": c.get("citavel", True),
        }
        # indexa texto + rótulo + temas (o nº do artigo e os temas devem ser buscáveis)
        campo = " ".join([
            c.get("texto", ""), c.get("rotulo", ""),
            " ".join(c.get("tema", []) or []), c.get("ementa", "") or "",
        ])
        tokens = tokenizar(campo)
        doclen[cid] = len(tokens)
        tf = {}
        for tok in tokens:
            tf[tok] = tf.get(tok, 0) + 1
        for tok, n in tf.items():
            invertido.setdefault(tok, {})[cid] = n
            df[tok] = df.get(tok, 0) + 1

    N = len(store)
    avgdl = (sum(doclen.values()) / N) if N else 0
    # avgdl/doclen alimentam a normalização BM25 do consultar.py — sem isso, artigos longos
    # (muito texto citado) vencem por TF bruto, não por relevância.
    saida_invertido = {"N": N, "avgdl": avgdl, "df": df, "doclen": doclen, "postings": invertido}

    (INDEX_DIR / "chunks.json").write_text(
        json.dumps(store, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (INDEX_DIR / "metadados.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (INDEX_DIR / "invertido.json").write_text(
        json.dumps(saida_invertido, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # status_pipeline: fatiado/tagueado/validado -> indexado para as leis que têm chunks
    # RAG-01 (auditoria 2026-07-10): a guarda anterior só promovia "fatiado", silenciando
    # leis que passaram por tagueamento mas nunca voltaram a "fatiado" — 4 leis ficavam presas.
    leis_indexadas = sorted({c.get("lei_id") for c in chunks})
    promovidas = []
    for lei_id in leis_indexadas:
        for jpath in (RAIZ / "leis").rglob(f"{lei_id}.json"):
            meta = json.loads(jpath.read_text(encoding="utf-8"))
            if meta.get("status_pipeline") in ("fatiado", "tagueado", "validado"):
                meta["status_pipeline"] = "indexado"
                jpath.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
                promovidas.append(lei_id)

    print(f"indexar: {N} chunks indexados, {len(df)} tokens, "
          f"{len(leis_indexadas)} leis -> rag/index/")
    if promovidas:
        print(f"  promovidas a 'indexado': {', '.join(promovidas)}")
    if leis_indexadas:
        print(f"  leis: {', '.join(leis_indexadas)}")


if __name__ == "__main__":
    main()
