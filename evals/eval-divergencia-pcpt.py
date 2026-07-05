#!/usr/bin/env python3
"""
eval-divergencia-pcpt.py — SURFAÇA a divergência PCpt-estimado × certidões reais (M0 / Legal-tech L4).

O piso de credibilidade (M0) exige NUNCA esconder que a estimativa de PCpt (Fi escalonado, Art. 24)
diverge do m² efetivamente transferido nas certidões. Este eval mede a divergência sobre os pares reais
(cedentes com `pcpt_m2` E `m2_ja_transferido`) e GATEIA duas coisas:

  1. A divergência é SURFAÇADA, não escondida: exige um nº mínimo de pares medidos (some se alguém
     "limpar" os pares para o número ficar bonito).
  2. Toda linha divergente é FLAGADA (T3): 100% dos pares carregam `qualidade_estimativa=PENDENTE_FI_DECLARADO`
     — o já-declarado nunca apresenta a estimativa como valor firme. Se a flag do T3 regredir, ESTE gate cai.

Medição honesta (2026-07-04): 55 pares · mediana transferido/PCpt ≈ 1,66 · 35/55 com transferido > PCpt.
Interpretação (M0): onde há certidão, o m² OFICIAL vence a estimativa; o PCpt é confiável só p/ prospecção nova.

Uso:  python3 evals/eval-divergencia-pcpt.py     # exit !=0 se a divergência deixar de ser surfaçada/flagada
PU 17 · 2026-07-04 (M0).
"""
import csv
import sys
from decimal import Decimal
from pathlib import Path
from statistics import median

RAIZ = Path(__file__).resolve().parent.parent
CSV_OFICIAL = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes_oficial.csv"
MIN_PARES = 50          # piso de cobertura: a divergência TEM de ser medida sobre dado real (não escondida)
FLAG_ESPERADA = "PENDENTE_FI_DECLARADO"


def _dec_br(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return Decimal(s.replace(".", "").replace(",", ".")) if "," in s else Decimal(s)
    except Exception:
        return None


def main():
    if not CSV_OFICIAL.exists():
        print(f"GATE VERMELHO: {CSV_OFICIAL.relative_to(RAIZ)} ausente.", file=sys.stderr)
        sys.exit(1)
    rows = list(csv.DictReader(open(CSV_OFICIAL, encoding="utf-8")))
    pares = []
    nao_flagados = 0
    for r in rows:
        P = _dec_br(r.get("pcpt_m2")); T = _dec_br(r.get("m2_ja_transferido"))
        if P and T and P > 0 and T > 0:
            pares.append(float(T / P))
            if (r.get("qualidade_estimativa") or "").strip() != FLAG_ESPERADA:
                nao_flagados += 1

    print("=== eval-divergência PCpt × certidões (M0 — surfaçar, não esconder) ===")
    print(f"  pares (pcpt E transferido): {len(pares)}")
    if pares:
        print(f"  mediana transferido/PCpt : {median(pares):.3f}")
        print(f"  transferido > PCpt       : {sum(1 for x in pares if x > 1)}/{len(pares)}")
    print(f"  pares NÃO flagados ({FLAG_ESPERADA}): {nao_flagados}")

    falhas = []
    if len(pares) < MIN_PARES:
        falhas.append(f"só {len(pares)} pares (< {MIN_PARES}) — divergência não está sendo medida/surfaçada")
    if nao_flagados:
        falhas.append(f"{nao_flagados} par(es) divergente(s) SEM flag {FLAG_ESPERADA} (T3 regrediu — estimativa "
                      "apresentada como valor firme)")
    if falhas:
        print("GATE VERMELHO: " + " ; ".join(falhas), file=sys.stderr)
        sys.exit(1)
    print(f"\nOK — divergência surfaçada ({len(pares)} pares) e 100% flagada. Onde há certidão, o m² oficial vence.")
    sys.exit(0)


if __name__ == "__main__":
    main()
