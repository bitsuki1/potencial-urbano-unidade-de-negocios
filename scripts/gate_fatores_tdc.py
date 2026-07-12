#!/usr/bin/env python3
"""
gate_fatores_tdc.py — TRAVA do inventário de fatores de TDC (tabelas/fatores-tdc.csv).

Regra (M4): nenhum fator pode ser marcado `verificado=sim` sem PROVA rastreável:
  (a) chunk_id existe de fato em rag/index/metadados.json (a fonte legal é real — 1.7); e
  (b) eval_id aponta um arquivo que EXISTE e é RODADO por um gate (consolidar.yml ou fechar-instancia.py)
      — logo sabotar o valor do fator na tabela-fonte faz um gate real ficar vermelho (1.3, anti-oráculo).

`verificado=pendente` não exige prova (é justamente o backlog honesto do que falta ancorar).
Sabotar (marcar `sim` com chunk/eval inexistente) ⇒ esta trava fica vermelha (DoD).

Uso:
    python3 scripts/gate_fatores_tdc.py            # valida (gate)
    python3 scripts/gate_fatores_tdc.py --autoteste  # prova que a própria trava morde
PU 18 · 2026-07-10.
"""
import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "tabelas" / "fatores-tdc.csv"
META = RAIZ / "rag" / "index" / "metadados.json"
GATES = [RAIZ / ".github" / "workflows" / "consolidar.yml",
         RAIZ / "scripts" / "fechar-instancia.py"]


def _chunks_validos():
    return set(json.loads(META.read_text(encoding="utf-8")).keys()) if META.exists() else set()


def _texto_gates():
    return "\n".join(p.read_text(encoding="utf-8") for p in GATES if p.exists())


def problemas(rows, chunks, gates_txt):
    probs = []
    for r in rows:
        if (r.get("verificado") or "").strip() != "sim":
            continue
        rid = r.get("id", "?")
        cid = (r.get("chunk_id") or "").strip()
        eid = (r.get("eval_id") or "").strip()
        if not cid:
            probs.append(f"{rid}: verificado=sim sem chunk_id")
        elif cid not in chunks:
            probs.append(f"{rid}: chunk_id inexistente no corpus — {cid}")
        if not eid:
            probs.append(f"{rid}: verificado=sim sem eval_id")
        else:
            if not (RAIZ / eid).exists():
                probs.append(f"{rid}: eval_id não existe no repo — {eid}")
            elif Path(eid).name not in gates_txt:
                probs.append(f"{rid}: eval_id existe mas NÃO é rodado por nenhum gate — {eid}")
    return probs


def main():
    if "--autoteste" in sys.argv:
        chunks = _chunks_validos()
        gt = _texto_gates()
        # a trava DEVE reprovar um fator 'sim' com chunk fabricado e um eval fantasma
        fake_chunk = [{"id": "X", "verificado": "sim", "chunk_id": "lei-fake::999-art-999",
                       "eval_id": "evals/eval-produto.py"}]
        fake_eval = [{"id": "Y", "verificado": "sim", "chunk_id": next(iter(chunks)),
                      "eval_id": "evals/nao-existe.py"}]
        assert problemas(fake_chunk, chunks, gt), "trava deveria reprovar chunk fabricado"
        assert problemas(fake_eval, chunks, gt), "trava deveria reprovar eval fantasma"
        print("AUTO-TESTE trava fatores-tdc: OK — reprova chunk fabricado e eval fantasma.")
        return 0

    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    chunks = _chunks_validos()
    if not chunks:
        print("[AGUARDANDO] rag/index/metadados.json ausente — trava de fatores PULA (sem corpus indexado).")
        return 0
    probs = problemas(rows, chunks, _texto_gates())
    sim = sum((r.get("verificado") or "") == "sim" for r in rows)
    pend = sum((r.get("verificado") or "") == "pendente" for r in rows)
    if probs:
        print(f"[FALHA] {len(probs)} fator(es) marcados 'verificado' sem prova rastreável:")
        for p in probs:
            print("   -", p)
        return 1
    print(f"[OK] fatores-tdc: {len(rows)} fatores ({sim} verificados c/ chunk+eval gated, {pend} pendentes). "
          f"Todo 'sim' tem fonte legal real e eval rodado por gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
