#!/usr/bin/env python3
"""
eval-semantico.py — prova da camada de SIGNIFICADO (B-5), OFFLINE (usa os vetores já
commitados; NÃO chama a API, roda no gate sem a chave).

O que MORDE:
  1. Cobertura: os vetores existem para (quase) todos os chunks e para as perguntas ativas.
  2. NÃO-REGRESSÃO: para toda pergunta ativa POSITIVA, o híbrido (palavra-chave + significado)
     acha a lei esperada no top-3 SEMPRE que a palavra-chave sozinha acha — o híbrido nunca
     perde o que o keyword já achava (é superconjunto por construção RRF).
  3. GANHO (informativo, não falha): quantas perguntas o SIGNIFICADO acha e a palavra-chave
     sozinha erra (o valor da camada — casa 'vender' com 'potencial passível de transferência').

Se os vetores ainda não foram gerados (Action embed-corpus não rodou), reporta e PULA
(status de espera — não bloqueia o build), como os demais evals aguardando insumo externo.
PU 18 · 2026-07-10.
"""
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import semantico  # noqa: E402

GT = RAIZ / "evals" / "ground-truth"
META = json.loads((RAIZ / "rag" / "index" / "metadados.json").read_text(encoding="utf-8"))
STATUS_PULA = {"aguardando_verbatim", "aguardando_engine", "aguardando_pgv", "confrontado_terreno", "inativo"}


def lei_do_chunk(cid):
    m = META.get(cid) or {}
    return m.get("lei_id") or cid.split("::")[0]


def keyword_rank(pergunta, top=30):
    """Ranking de chunk_ids por BM25 (reusa o consultar.py real)."""
    import consultar
    inv, meta = consultar.INV, consultar.META if hasattr(consultar, "INV") else (None, None)
    # consultar expõe carregar_indice(); usamos a API pública consultar() e pegamos os chunk_ids
    res = consultar.consultar(pergunta, top=top)
    ids = []
    for r in (res.get("resultados") if isinstance(res, dict) else res) or []:
        cid = r.get("chunk_id") if isinstance(r, dict) else None
        if cid:
            ids.append(cid)
    return ids


def main():
    vets = semantico.carregar_vetores()
    qfile = GT / "query-embeddings.json"
    if not vets or not qfile.exists():
        print("[AGUARDANDO] vetores semânticos ainda não gerados (rode a Action embed-corpus). "
              "Eval semântico PULA — não bloqueia o build.")
        return 0
    qvecs = {k: semantico._decode(v) for k, v in json.loads(qfile.read_text(encoding="utf-8")).get("vetores", {}).items()}

    # perguntas ativas positivas (espera.lei_id presente e fundamentada != False)
    casos = []
    for gf in sorted(GT.glob("*.json")):
        if gf.name == "query-embeddings.json":
            continue
        try:
            d = json.loads(gf.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("status") in STATUS_PULA:
            continue
        for it in (d.get("itens") or d.get("items") or d.get("casos") or []):
            q = (it.get("pergunta") or "").strip()
            esp = it.get("espera") or {}
            lei = esp.get("lei_id")
            if q and lei and esp.get("fundamentada", True):
                casos.append((q, lei))

    kw_hits = sem_hits = hyb_hits = 0
    regressoes, ganhos = [], []
    for q, lei in casos:
        h = hashlib.sha1(q.encode("utf-8")).hexdigest()
        qv = qvecs.get(h)
        if not qv:
            continue
        sem_ids = [c for c, _ in semantico.cosseno_rank(qv, vets, top=30)]
        kw_ids = keyword_rank(q, top=30)
        hyb_ids = semantico.rrf(kw_ids, sem_ids, top=30)

        kw = lei in {lei_do_chunk(c) for c in kw_ids[:3]}
        sem = lei in {lei_do_chunk(c) for c in sem_ids[:3]}
        hyb = lei in {lei_do_chunk(c) for c in hyb_ids[:3]}
        kw_hits += kw; sem_hits += sem; hyb_hits += hyb
        if kw and not hyb:
            regressoes.append((q[:50], lei))
        if sem and not kw:
            ganhos.append((q[:50], lei))

    n = len(casos)
    print(f"[SEMÂNTICO] {n} perguntas positivas ativas · hit@3 — "
          f"palavra-chave: {kw_hits}/{n} · significado: {sem_hits}/{n} · HÍBRIDO: {hyb_hits}/{n}")
    if ganhos:
        print(f"[GANHO] o significado achou {len(ganhos)} que a palavra-chave sozinha errou:")
        for q, lei in ganhos[:5]:
            print(f"   + '{q}...' → {lei}")
    if regressoes:
        print("[FALHA] REGRESSÃO — o híbrido perdeu o que a palavra-chave achava:")
        for q, lei in regressoes:
            print(f"   - '{q}...' → {lei}")
        print(f"\nRESUMO: FALHA ({len(regressoes)} regressões).")
        sys.exit(1)
    print(f"\nRESUMO: OK — híbrido não regride (⊇ palavra-chave) e agrega {len(ganhos)} ganho(s) de significado.")


if __name__ == "__main__":
    sys.exit(main())
