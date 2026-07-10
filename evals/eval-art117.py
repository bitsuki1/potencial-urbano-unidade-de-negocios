#!/usr/bin/env python3
"""
eval-art117.py — prova da CONTRAPARTIDA da outorga onerosa (Art. 117 do PDE), VERBATIM.

O que MORDE (gate HARD):
  1. ÂNCORA VERBATIM (mutação-sensível): recomputa C = (At/Ac)×V×Fs×Fp de forma INDEPENDENTE do engine
     e exige igualdade EXATA com oodc.contrapartida_art117. Se alguém mudar a fórmula no engine, cai.
  2. RECONCILIAÇÃO: a forma por-m² do caput e o TOTAL do §1º são a MESMA família — quando Ac = CA_max×At,
     contrapartida_art117(...)['total'] == outorga_onerosa(...)['valor'] (a "vacina" antiga que dizia o
     Art. 117 "sem fonte" está falsificada pelo verbatim `122__art-117.json`).
  3. CITAÇÃO: o resultado aponta o Art. 117 (1.7).
PU 18 · 2026-07-10.
"""
import sys
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "engines" / "tdc"))
import oodc  # noqa: E402

CHUNK = RAIZ / "rag" / "chunks" / "lei-municipal-saopaulo-16050-2014" / "122__art-117.json"


def main():
    print("═══ PROVA art117 (contrapartida da outorga onerosa, PDE) ═══")
    falhas = []

    # 1) âncora verbatim independente: C = (At/Ac)×V×Fs×Fp
    At, Ac, V, Fs, Fp = Decimal("500"), Decimal("2000"), Decimal("3106"), Decimal("1.0"), Decimal("1.2")
    esp = oodc._q((At / Ac) * V * Fs * Fp)
    got = oodc.contrapartida_art117("500", "2000", "3106", "1.0", "1.2")
    if got["valor_por_m2"] != esp:
        falhas.append(f"C por m²: engine {got['valor_por_m2']} ≠ verbatim {esp}")
    if "117" not in got["citacao"]["dispositivo"]:
        falhas.append("citação não aponta o Art. 117")

    # 2) reconciliação com a fórmula legada (§1º total): Ac = CA_max × At → total == outorga_onerosa
    CAm, aa = Decimal("4"), Decimal("1000")
    c = oodc.contrapartida_art117("500", str(CAm * At), "3106", "1.0", "1.2", potencial_adicional=str(aa))
    oo = oodc.outorga_onerosa(str(aa), str(CAm), "1.2", "1.0", "3106")
    if c["total"] != oo["valor"]:
        falhas.append(f"identidade §1º quebrada: art117.total {c['total']} ≠ OODC {oo['valor']}")

    # 3) o verbatim está indexado (fonte real da citação)
    if not CHUNK.exists():
        falhas.append("chunk 122__art-117.json ausente — a citação perderia a fonte")

    if falhas:
        print("[FALHA]")
        for f in falhas:
            print("   -", f)
        print(f"\nRESUMO: FALHA ({len(falhas)}).")
        return 1
    print(f"[PASS] C=(At/Ac)×V×Fs×Fp reproduz o verbatim (mutação-sensível); C por m² = {got['valor_por_m2']}.")
    print(f"[PASS] reconciliação: quando Ac=CA_max×At, total §1º == outorga_onerosa ({c['total']}).")
    print("\nRESUMO: OK — Art. 117 provado verbatim + reconciliado com a fórmula legada (§1º total).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
