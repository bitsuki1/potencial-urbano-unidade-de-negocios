#!/usr/bin/env python3
"""
backfill_hash.py — AUD-A10: preenche `fonte.hash` (sha256) nos .json do corpus (leis/ + jurisprudencia/).

O Gate 1 do pipeline (Parte 3: "hash confere") nunca teve como rodar: `fonte.hash` era null em 100%
do corpus. Este script preenche, de forma IDEMPOTENTE e honesta sobre O QUE está sendo hasheado:

  - Se `fonte.path` existe localmente (o CRU da ingestão, ex.: `_entrada/misto/*.txt`):
      hash do PRÓPRIO CRU  ->  fonte.hash_alvo = fonte.path
  - Senão (cru não está local — municipais `bruto` e juris capturadas; B-4/B-9):
      hash do .md do corpus (a NOSSA transcrição)  ->  fonte.hash_alvo = <corpus .md>
      + fonte.hash_nota declarando que é a transcrição, não o cru.

A VERIFICAÇÃO contínua ("hash confere") mora em scripts/consolidar.py, que recomputa e FALHA
em divergência ou hash nulo. Rode este backfill de novo só quando o alvo mudar DE PROPÓSITO
(re-ingestão) — mudança não-intencional deve FALHAR o gate, não ser re-carimbada.

Uso: python3 scripts/backfill_hash.py [--check]   # --check: só reporta, não escreve
PU 18 · 2026-07-05 (AUD-A10).
"""
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def sha256_de(p: Path) -> str:
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def main(check=False):
    alterados, ja_ok, sem_alvo = [], [], []
    arquivos = sorted(list((RAIZ / "leis").rglob("*.json")) + list((RAIZ / "jurisprudencia").glob("*.json")))
    for jp in arquivos:
        if "_capturas" in jp.parts:
            continue
        d = json.loads(jp.read_text(encoding="utf-8"))
        fonte = d.setdefault("fonte", {})
        cru = RAIZ / fonte["path"] if fonte.get("path") else None
        md = jp.with_suffix(".md")
        if cru and cru.exists():
            alvo, nota = cru, None
        elif md.exists():
            alvo = md
            nota = "hash da transcrição do corpus (.md) — cru ausente localmente (B-4/B-9); trocar pelo hash do cru quando ele chegar"
        else:
            sem_alvo.append(jp.name)
            continue
        h = sha256_de(alvo)
        alvo_rel = str(alvo.relative_to(RAIZ))
        if fonte.get("hash") == h and fonte.get("hash_alvo") == alvo_rel:
            ja_ok.append(jp.name)
            continue
        fonte["hash"] = h
        fonte["hash_alvo"] = alvo_rel
        if nota:
            fonte["hash_nota"] = nota
        else:
            fonte.pop("hash_nota", None)
        alterados.append(jp.name)
        if not check:
            jp.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    verbo = "a preencher" if check else "preenchidos"
    print(f"backfill_hash (AUD-A10): {len(alterados)} {verbo} · {len(ja_ok)} já corretos · {len(sem_alvo)} SEM ALVO")
    if sem_alvo:
        print(f"  SEM ALVO (nem fonte.path nem .md): {sem_alvo}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main(check="--check" in sys.argv)
