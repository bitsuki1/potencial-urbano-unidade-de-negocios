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
GOLDEN_CSV = RAIZ / "evals" / "ground-truth" / "golden-cedentes-sem-pii.csv"
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
    n_checks = 0
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
        n_checks += 1
        print(f"  [{status}] {g['sql']} faixa {inc} (área {area} m²): "
              + (f"Fi={fi_esp} pcpt={pcpt_esp} m²" if not detalhes else " ; ".join(detalhes)))

    # T9 — parcelamento Art. 124 §3º (>50.000 m² → 10 parcelas anuais). O engine já prova o caso >50k
    # no autoteste (não-vácuo); AQUI o invariante de PRODUTO: nenhuma linha entregue com PCpt > 50.000
    # pode sair sem `parcelas_anuais=10` + pendência citando o Art. 124 §3º. Cobertura declarada (sem
    # cap silencioso): hoje 0 cedentes reais >50k — o check guarda a regressão quando a cobertura crescer.
    LIMITE = Decimal("50000")
    grandes = [r for r in csv_idx.values() if (r.get("pcpt_m2") or "").strip() and Decimal(r["pcpt_m2"]) > LIMITE]
    t9_falhas = [r["sql_mestre"] for r in grandes
                 if (r.get("parcelas_anuais") or "").strip() != "10" or "Art.124 §3º" not in (r.get("pendencia_calculo") or "")]
    print(f"  [{'PASS' if not t9_falhas else 'FALHA'}] T9 parcelamento Art.124 §3º: "
          f"{len(grandes)} linha(s) com PCpt>50.000 m² no produto; sem flag = {len(t9_falhas)}")
    if t9_falhas:
        falhas += 1
        print(f"    SQLs sem parcelamento flagado: {t9_falhas[:10]}", file=sys.stderr)
    n_checks += 1

    # L-T9-2: não-vácuo — pelo menos 1 linha com PCpt > 50k deve existir (senão o check acima é vácuo).
    if not grandes:
        print("  [FALHA] T9 não-vácuo: 0 linhas com PCpt > 50.000 m² — check é vácuo (L-T9-2)")
        falhas += 1
    else:
        print(f"  [PASS ] T9 não-vácuo: {len(grandes)} linha(s) > 50k confirmam check ativo (L-T9-2)")
    n_checks += 1

    # L-T11-2: integridade de conjuntos — membros NÃO têm saldo/preço individual (saldo é do conjunto).
    conj_members = [r for r in csv_idx.values() if (r.get("conjunto_certidao") or "").strip()]
    conj_bad = [r["sql_mestre"] for r in conj_members
                if (r.get("saldo_pcpt_m2") or "").strip() or (r.get("preco_proxy_brl") or "").strip()]
    print(f"  [{'PASS' if not conj_bad else 'FALHA'}] T11 conjuntos: "
          f"{len(conj_members)} membros, {len(conj_bad)} com saldo/preço individual (deve ser 0)")
    if conj_bad:
        falhas += 1
        print(f"    SQLs com saldo/preço espúrio: {conj_bad[:10]}", file=sys.stderr)
    n_checks += 1

    # L-T11-3: fixture com os conjuntos REAIS — exercita os conjuntos do CSV oficial.
    # Agrupa por conjunto_certidao e verifica: (1) não-vácuo (>=3 conjuntos),
    # (2) integridade do agrupamento, (3) membros de multi-membro sem saldo/preço individual.
    conj_grupos = {}
    for r in csv_idx.values():
        c = (r.get("conjunto_certidao") or "").strip()
        if c:
            conj_grupos.setdefault(c, []).append(r)

    t11_3_falhas = []
    # (1) não-vácuo: pelo menos 3 conjuntos reais devem existir no CSV
    if len(conj_grupos) < 3:
        t11_3_falhas.append(f"apenas {len(conj_grupos)} conjuntos encontrados (mínimo 3)")
    # Para cada conjunto:
    for nome_conj, membros in sorted(conj_grupos.items()):
        # (2) todos os membros compartilham o mesmo conjunto_certidao (integridade do agrupamento)
        vals_conj = set((m.get("conjunto_certidao") or "").strip() for m in membros)
        if len(vals_conj) != 1:
            t11_3_falhas.append(f"{nome_conj}: membros com conjunto_certidao divergente ({vals_conj})")
        # (3) multi-membro: nenhum membro individual tem saldo/preço preenchido
        if len(membros) > 1:
            for m in membros:
                s = (m.get("saldo_pcpt_m2") or "").strip()
                p = (m.get("preco_proxy_brl") or "").strip()
                if s or p:
                    t11_3_falhas.append(
                        f"{nome_conj}/{m['sql_mestre']}: saldo/preço individual "
                        f"preenchido em conjunto multi-membro")

    print(f"  [{'PASS ' if not t11_3_falhas else 'FALHA'}] T11 conjuntos reais: "
          f"{len(conj_grupos)} conjuntos exercitados (L-T11-3)")
    if t11_3_falhas:
        falhas += 1
        for msg_f in t11_3_falhas[:10]:
            print(f"    {msg_f}", file=sys.stderr)
    n_checks += 1

    # L-T4-5: não-vácuo vedação Art. 124 §2 — pelo menos 1 vedada bloqueada deve existir.
    vedadas = [r for r in csv_idx.values() if "Art. 124 §2" in (r.get("pendencia_calculo") or "")]
    if not vedadas:
        print("  [FALHA] T8 vedação não-vácuo: 0 vedadas Art.124§2 no produto (L-T4-5)")
        falhas += 1
    else:
        print(f"  [PASS ] T8 vedação não-vácuo: {len(vedadas)} vedadas bloqueadas (L-T4-5)")
    n_checks += 1

    # L-T2-2/T3: regime PCpt — todo JA_DECLARADO deve ter qualidade_estimativa=PENDENTE_FI_DECLARADO
    ja_decl = [r for r in csv_idx.values() if (r.get("regime_pcpt") or "").strip() == "JA_DECLARADO"]
    ja_bad = [r["sql_mestre"] for r in ja_decl
              if (r.get("qualidade_estimativa") or "").strip() != "PENDENTE_FI_DECLARADO"]
    if ja_bad:
        print(f"  [FALHA] T3 regime: {len(ja_bad)} JA_DECLARADO sem PENDENTE_FI_DECLARADO (L-T2-2)")
        falhas += 1
    elif not ja_decl:
        print("  [FALHA] T3 regime não-vácuo: 0 JA_DECLARADO no produto (L-T2-2)")
        falhas += 1
    else:
        print(f"  [PASS ] T3 regime: {len(ja_decl)} JA_DECLARADO todos com PENDENTE_FI_DECLARADO (L-T2-2)")
    n_checks += 1

    # L-T2-2/T4: conservação Art.129 — coluna populada; não-vácuo (≥1 ELEGIVEL + ≥1 PENDENTE).
    cons_vals = [(r.get("elegibilidade_conservacao") or "").strip() for r in csv_idx.values()]
    cons_vazio = sum(1 for v in cons_vals if not v)
    cons_elegivel = sum(1 for v in cons_vals if v == "ELEGIVEL")
    cons_pendente = sum(1 for v in cons_vals if v == "PENDENTE_CONSERVACAO")
    if cons_vazio:
        print(f"  [FALHA] T4 conservação: {cons_vazio} linhas sem elegibilidade_conservacao (L-T2-2)")
        falhas += 1
    elif cons_elegivel == 0 or cons_pendente == 0:
        print(f"  [FALHA] T4 conservação não-vácuo: ELEGIVEL={cons_elegivel} PENDENTE={cons_pendente} (L-T2-2)")
        falhas += 1
    else:
        print(f"  [PASS ] T4 conservação: {cons_elegivel} ELEGIVEL, {cons_pendente} PENDENTE, sem vazio (L-T2-2)")
    n_checks += 1

    # L-T2-3: golden SEM-PII — fixture versionada deve existir e concordar com FAIXAS_LEGAIS.
    if not GOLDEN_CSV.exists():
        print("  [FALHA] L-T2-3: golden-cedentes-sem-pii.csv ausente (fixture SEM-PII não versionada)")
        falhas += 1
    else:
        golden_rows = list(csv.DictReader(open(GOLDEN_CSV, encoding="utf-8")))
        t23_bad = []
        for gr in golden_rows:
            area_g = Decimal(gr["area_terreno_m2"])
            fi_g = Decimal(gr["fi_legal"])
            pcpt_g = Decimal(gr["pcpt_esperado_m2"])
            fi_esp_g, _ = fi_legal(area_g)
            pcpt_esp_g = (area_g * Decimal(gr["ca_basico"]) * fi_esp_g).quantize(Q2, ROUND_HALF_UP)
            if fi_g != fi_esp_g:
                t23_bad.append(f"{gr['sql_mestre']}: fi={fi_g} != legal {fi_esp_g}")
            if pcpt_g != pcpt_esp_g:
                t23_bad.append(f"{gr['sql_mestre']}: pcpt={pcpt_g} != legal {pcpt_esp_g}")
        if t23_bad:
            print(f"  [FALHA] L-T2-3: golden SEM-PII diverge da lei: {t23_bad[:5]}")
            falhas += 1
        else:
            print(f"  [PASS ] L-T2-3: golden SEM-PII ({len(golden_rows)} cedentes) concorda com FAIXAS_LEGAIS")
    n_checks += 1

    print(f"\nRESUMO: {n_checks-falhas}/{n_checks} PASS, {falhas} falha(s).")
    if falhas:
        print("GATE VERMELHO: engine/produto divergiu do Fi legal (Art. 24 LPUOS). "
              "Um Fi sabotado ou o produto com Fi drifted da lei quebra aqui (T2).", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
