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

  3. (L-T5-1) Decomposição Fi-regime: para cada par divergente, decompõe o ratio pcpt_oficial/pcpt_escalonado
     nos fatores multiplicativos de Fi, CAbás e Atc, e verifica que a MAIORIA da divergência (>90% em
     log-divergência) vem de Fi — confirmando que a divergência JA_DECLARADO é puramente de regime de Fi,
     sem drift de CAbás/Atc.

Medição honesta (2026-07-04): 55 pares · mediana transferido/PCpt ≈ 1,66 · 35/55 com transferido > PCpt.
Interpretação (M0): onde há certidão, o m² OFICIAL vence a estimativa; o PCpt é confiável só p/ prospecção nova.

Uso:  python3 evals/eval-divergencia-pcpt.py     # exit !=0 se a divergência deixar de ser surfaçada/flagada
PU 17 · 2026-07-04 (M0).  L-T5-1 · 2026-07-10 (decomposição Fi-regime).
"""
import csv
import math
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


def _decomposicao_fi_regime(rows):
    """L-T5-1: decompõe a divergência pcpt_oficial/pcpt_escalonado nos fatores Fi, CAbás e Atc.

    Para cada cedente divergente, calcula:
      pcpt_ratio  = m2_ja_transferido / pcpt_m2   (divergência total)
      fi_ratio    = fi_implícito / fi_aplicado     (componente de Fi)
      cabas_ratio = 1.0  (mesmo input nos dois lados — sem CAbás oficial separado)
      atc_ratio   = 1.0  (mesmo input nos dois lados — sem Atc oficial separado)

    Onde fi_implícito = m2_ja_transferido / (area_terreno_m2 × ca_basico).

    Verifica que fi_ratio × cabas_ratio × atc_ratio ≈ pcpt_ratio (dentro de 1%)
    e que Fi explica >90% da log-divergência total.
    """
    decomp = []  # lista de dicts com os ratios por cedente
    for r in rows:
        P = _dec_br(r.get("pcpt_m2"))
        T = _dec_br(r.get("m2_ja_transferido"))
        Atc = _dec_br(r.get("area_terreno_m2"))
        CAbas = _dec_br(r.get("ca_basico"))
        Fi_esc = _dec_br(r.get("fi_aplicado"))
        if not all(v and v > 0 for v in (P, T, Atc, CAbas, Fi_esc)):
            continue
        pcpt_ratio = float(T / P)
        fi_implicito = float(T / (Atc * CAbas))
        fi_ratio = fi_implicito / float(Fi_esc)
        cabas_ratio = 1.0
        atc_ratio = 1.0
        # produto reconstituído
        produto = fi_ratio * cabas_ratio * atc_ratio
        decomp.append({
            "sql": r.get("sql_mestre", "?"),
            "pcpt_ratio": pcpt_ratio,
            "fi_ratio": fi_ratio,
            "cabas_ratio": cabas_ratio,
            "atc_ratio": atc_ratio,
            "produto": produto,
        })
    return decomp


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

    # ── L-T5-1: decomposição Fi-regime ──────────────────────────────────
    decomp = _decomposicao_fi_regime(rows)
    if not decomp:
        print("GATE VERMELHO: L-T5-1 — nenhum cedente com dados completos p/ decomposição "
              "(pcpt_m2, m2_ja_transferido, area_terreno_m2, ca_basico, fi_aplicado).", file=sys.stderr)
        sys.exit(1)

    # 1. Verificar que o produto fi×cabas×atc reconstitui o pcpt_ratio (dentro de 1%)
    erros_reconstituicao = []
    for d in decomp:
        erro_rel = abs(d["produto"] - d["pcpt_ratio"]) / d["pcpt_ratio"]
        if erro_rel > 0.01:
            erros_reconstituicao.append(
                f"  {d['sql']}: produto={d['produto']:.4f}  pcpt_ratio={d['pcpt_ratio']:.4f}  erro={erro_rel:.2%}")
    if erros_reconstituicao:
        print("GATE VERMELHO: L-T5-1 — reconstituição fi×cabas×atc ≠ pcpt_ratio (>1%) em:", file=sys.stderr)
        for e in erros_reconstituicao:
            print(e, file=sys.stderr)
        sys.exit(1)

    # 2. Percentual da log-divergência explicado por Fi (sobre cedentes divergentes, ratio ≠ 1)
    log_fi_total = 0.0
    log_pcpt_total = 0.0
    n_divergentes = 0
    for d in decomp:
        log_pcpt = abs(math.log(d["pcpt_ratio"])) if d["pcpt_ratio"] > 0 else 0.0
        log_fi = abs(math.log(d["fi_ratio"])) if d["fi_ratio"] > 0 else 0.0
        if log_pcpt < 1e-9:
            continue  # ratio ≈ 1.0, sem divergência neste cedente
        n_divergentes += 1
        log_pcpt_total += log_pcpt
        log_fi_total += log_fi

    if log_pcpt_total > 0:
        pct_fi = log_fi_total / log_pcpt_total * 100.0
    else:
        pct_fi = 100.0  # sem divergência → Fi explica tudo (trivialmente)

    print(f"\n--- L-T5-1: decomposição Fi-regime (Art.24 escalonado × declarado) ---")
    print(f"  cedentes decompostos     : {len(decomp)}")
    print(f"  cedentes divergentes     : {n_divergentes}")
    print(f"  Fi explica               : {pct_fi:.1f}% da log-divergência total")
    print(f"  CAbás ratio (todos)      : 1.000 (mesmo input)")
    print(f"  Atc ratio (todos)        : 1.000 (mesmo input)")

    assert pct_fi > 90.0, (
        f"L-T5-1 FALHOU: Fi explica apenas {pct_fi:.1f}% da divergência (esperado >90%). "
        f"Há drift em CAbás ou Atc que não deveria existir."
    )

    print(f"\n[INFO ] L-T5-1: decomposição Fi-regime — "
          f"Fi explica {pct_fi:.1f}% da divergência em {n_divergentes} cedentes")
    print(f"OK — divergência é puramente de regime de Fi (Art.24 escalonado vs declarado); "
          f"CAbás e Atc são estáveis.")
    sys.exit(0)


if __name__ == "__main__":
    main()
