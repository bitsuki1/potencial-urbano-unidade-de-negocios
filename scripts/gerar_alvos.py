#!/usr/bin/env python3
"""
gerar_alvos.py — ESTÁGIO DE SAÍDA DO PRODUTO (H3/E5): dado um lote de imóveis
{sql, codlog, zona, area_adicional, fp, fs}, produz a LISTA DE ALVOS por imóvel com o
valor da Outorga Onerosa (OODC) calculado pelo engine determinístico (1.3) + citação.

É o último elo da esteira: o JOIN espacial (IPTU 2026 × LOTES/geo × Q14 × zoneamento) entrega
a tabela de entrada; este script roda o engine linha a linha e ordena por oportunidade. Funciona
HOJE sobre o V (Quadro 14) e CA_max (Quadro 3) REAIS — não espera o banco. Quando o JOIN grande
existir, é só apontar --entrada para a saída dele (mesmo schema).

NUNCA inventa V/CA_max (1.3/RO-04): linha sem dado de tabela é REPORTADA, não preenchida.

Uso:
    python3 scripts/gerar_alvos.py --entrada evals/ground-truth/amostra-alvos.csv [--saida alvos.csv]
Trazido pelo orquestrador do PU — 2026-06-24 (prepara H3; estágio E5).
"""
import csv, sys, argparse
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "engines" / "tdc"))
import oodc as E  # engine determinístico

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True, help="CSV com colunas: sql,codlog,zona,area_adicional,fp,fs[,dono,endereco]")
    ap.add_argument("--saida", default=None, help="CSV de saída (default: stdout-resumo + alvos-<entrada>)")
    a = ap.parse_args()
    linhas = [l for l in Path(a.entrada).read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    rows = list(csv.DictReader(linhas))
    alvos, faltas = [], []
    for r in rows:
        try:
            res = E.oodc_por_imovel(r["sql"], r["codlog"], r["zona"],
                                    r["area_adicional"], r.get("fp","1.0"), r.get("fs","1.0"))
            fd = res["fonte_dados"]
            alvos.append({
                "sql": r["sql"], "codlog": r["codlog"], "zona": r["zona"],
                "dono": r.get("dono",""), "endereco": r.get("endereco",""),
                "V_m2_brl": fd["V_q14_brl"], "ca_max": fd["ca_max_q3"],
                "area_adicional": r["area_adicional"], "oodc_brl": str(res["valor"]),
                "memoria": res["memoria_calculo"],
                "citacao": res["citacao"]["dispositivo"] + " | " + fd["proveniencia"],
            })
        except Exception as ex:
            faltas.append({"sql": r.get("sql"), "codlog": r.get("codlog"), "zona": r.get("zona"), "motivo": str(ex)})
    alvos.sort(key=lambda x: float(x["oodc_brl"]), reverse=True)   # maior oportunidade primeiro
    saida = Path(a.saida) if a.saida else Path(a.entrada).with_name("alvos-" + Path(a.entrada).name)
    with saida.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sql","codlog","zona","dono","endereco","V_m2_brl","ca_max","area_adicional","oodc_brl","memoria","citacao"])
        w.writeheader(); w.writerows(alvos)
    print(f"gerar_alvos: {len(alvos)} alvos calculados, {len(faltas)} sem dado de tabela. Saída: {saida}")
    for al in alvos[:5]:
        print(f"  R$ {float(al['oodc_brl']):>14,.2f}  SQ {al['sql']}/{al['codlog']} zona {al['zona']:6} V={al['V_m2_brl']}  {al['dono']}")
    for fa in faltas[:5]:
        print(f"  [FALTA] SQ {fa['sql']}/{fa['codlog']} zona {fa['zona']}: {fa['motivo']}")

if __name__ == "__main__":
    main()
