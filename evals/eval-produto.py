#!/usr/bin/env python3
"""
eval-produto.py — GATE do PRODUTO (T2/S2): golden-assert do engine de cedente sobre CEDENTES REAIS.

Fecha o furo "declarei ≠ provei" do CI (S2): o `consolidar.yml` não cobria `engines/**`/`zepec/**`
e nunca rodava o `pcpt.py` — sabotar um Fi da tabela Art. 24 (LPUOS) passava despercebido. Este eval:

  1. ANCORA NA LEI, não no engine. As faixas de Fi (LPUOS Art. 24, I–VII) estão hardcoded AQUI, como
     fonte independente. O `pcpt_m2` esperado é computado NESTE teste (área × CAbás × Fi_legal, Decimal),
     NÃO lido do engine nem do CSV — logo o teste NÃO é circular: se o engine (ou o produto) for
     sabotado, o valor esperado permanece o legal e a divergência FALHA o gate.
  2. Usa 7 CEDENTES REAIS (um por faixa I–VII), SQL + área verbatim de `zepec/ferramenta/
     zepec_cedentes_oficial.csv` (recorte oficial IPTU 2026). CAbás=1,0 nesses lotes (pcpt=área×Fi).
  3. Prova em DOIS pontos:
       (a) ENGINE — `pcpt_sem_doacao(area, cabas)` devolve o Fi legal da faixa E o pcpt legal;
       (b) PRODUTO ENTREGUE — a linha do SQL no CSV oficial carrega `fi_aplicado` == Fi legal
           (o produto que vai ao cliente não pode ter Fi drifted da lei).

  DoD (T2): sabotar 1 Fi no `engines/tdc/pcpt.py::FI_ZEPEC_ART24` faz ESTE gate FALHAR (provado:
  `docs/` / commit T2). Faixa I (1,2) sabotada p/ 1,5 ⇒ cedente 378 m² esperado 453,60 vira 567,00 ⇒ FALHA.

Uso:  python3 evals/eval-produto.py        # exit !=0 se qualquer golden divergir
PU 17 · 2026-07-03 (Fase 1, T2).
"""
import csv
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "engines" / "tdc"))
import pcpt as ENGINE  # noqa: E402

CSV_OFICIAL = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes_oficial.csv"
Q2 = Decimal("0.01")

# FONTE INDEPENDENTE (LPUOS Art. 24, I–VII): (limite_superior_m2 ou None, Fi_legal, inciso).
# Hardcoded AQUI de propósito — se alguém alterar a tabela do engine, este anchor NÃO muda e o gate acusa.
FAIXAS_LEGAIS = [
    (Decimal("500"),   Decimal("1.2"), "Art. 24, I"),
    (Decimal("2000"),  Decimal("1.0"), "Art. 24, II"),
    (Decimal("5000"),  Decimal("0.9"), "Art. 24, III"),
    (Decimal("10000"), Decimal("0.7"), "Art. 24, IV"),
    (Decimal("20000"), Decimal("0.5"), "Art. 24, V"),
    (Decimal("50000"), Decimal("0.2"), "Art. 24, VI"),
    (None,             Decimal("0.1"), "Art. 24, VII"),
]

def fi_legal(area: Decimal):
    for teto, fi, inc in FAIXAS_LEGAIS:
        if teto is None or area <= teto:
            return fi, inc
    raise AssertionError("área não resolvida nas faixas Art. 24")

# CEDENTES REAIS (SQL + área verbatim do recorte oficial IPTU 2026), um por faixa I–VII. CAbás=1,0.
GOLDEN = [
    {"sql": "0200670033", "area": "378",    "cabas": "1.0", "faixa": "I"},
    {"sql": "0090190006", "area": "1336",   "cabas": "1.0", "faixa": "II"},
    {"sql": "0100030026", "area": "4230",   "cabas": "1.0", "faixa": "III"},
    {"sql": "0090320447", "area": "5401",   "cabas": "1.0", "faixa": "IV"},
    {"sql": "0020400001", "area": "15035",  "cabas": "1.0", "faixa": "V"},
    {"sql": "0080390048", "area": "38990",  "cabas": "1.0", "faixa": "VI"},
    {"sql": "1672260004", "area": "288425", "cabas": "1.0", "faixa": "VII"},
]


def _csv_por_sql():
    if not CSV_OFICIAL.exists():
        return None
    idx = {}
    with open(CSV_OFICIAL, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            idx[r["sql_mestre"].strip()] = r
    return idx


def main():
    csv_idx = _csv_por_sql()
    if csv_idx is None:
        print(f"GATE VERMELHO: {CSV_OFICIAL.relative_to(RAIZ)} ausente — produto não pode ser provado.",
              file=sys.stderr)
        sys.exit(1)

    falhas = 0
    print("=== eval-produto (T2): golden-assert do engine de cedente sobre cedentes REAIS ===")
    for g in GOLDEN:
        area = Decimal(g["area"]); cabas = Decimal(g["cabas"])
        fi_esp, inc = fi_legal(area)
        pcpt_esp = (area * cabas * fi_esp).quantize(Q2, ROUND_HALF_UP)   # ANCORA na lei, não no engine

        detalhes = []
        # (a) ENGINE
        e = ENGINE.pcpt_sem_doacao(g["area"], g["cabas"])
        if Decimal(e["fi"]) != fi_esp:
            detalhes.append(f"engine Fi={e['fi']} != legal {fi_esp} ({inc})")
        if e["valor_m2"] != pcpt_esp:
            detalhes.append(f"engine pcpt={e['valor_m2']} != legal {pcpt_esp}")
        # (b) PRODUTO ENTREGUE (CSV oficial) — Fi E o NÚMERO que vai ao cliente (pcpt_m2).
        row = csv_idx.get(g["sql"])
        if row is None:
            detalhes.append(f"SQL {g['sql']} ausente no CSV oficial")
        else:
            fi_ap = (row.get("fi_aplicado") or "").strip()
            if fi_ap and Decimal(fi_ap) != fi_esp:
                detalhes.append(f"produto fi_aplicado={fi_ap} != legal {fi_esp}")
            # A-03 (auditoria 2026-07-05): gatear o PCpt ENTREGUE. Recomputa do PRÓPRIO CSV
            # (área × CAbás × Fi_legal) e compara ao pcpt_m2 gravado — sabotar pcpt_m2 no CSV FALHA aqui.
            pcpt_ent = (row.get("pcpt_m2") or "").strip()
            area_csv = (row.get("area_terreno_m2") or "").strip()
            cabas_csv = (row.get("ca_basico") or "").strip()
            if pcpt_ent and area_csv and cabas_csv:
                pcpt_csv_esp = (Decimal(area_csv) * Decimal(cabas_csv) * fi_esp).quantize(Q2, ROUND_HALF_UP)
                if Decimal(pcpt_ent) != pcpt_csv_esp:
                    detalhes.append(f"produto pcpt_m2={pcpt_ent} != {pcpt_csv_esp} "
                                    f"(área {area_csv}×CAbás {cabas_csv}×Fi {fi_esp} do próprio CSV)")

        status = "PASS" if not detalhes else "FALHA"
        if detalhes:
            falhas += 1
        print(f"  [{status}] {g['sql']} faixa {inc} (área {area} m²): "
              + (f"Fi={fi_esp} pcpt={pcpt_esp} m²" if not detalhes else " ; ".join(detalhes)))

    print(f"\nRESUMO: {len(GOLDEN)-falhas}/{len(GOLDEN)} PASS, {falhas} falha(s).")
    if falhas:
        print("GATE VERMELHO: engine/produto divergiu do Fi legal (Art. 24 LPUOS). "
              "Um Fi sabotado ou o produto com Fi drifted da lei quebra aqui (T2).", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
