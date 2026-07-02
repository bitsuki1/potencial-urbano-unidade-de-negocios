#!/usr/bin/env python3
"""
enriquecer_oficial.py — Enriquece a FERRAMENTA (todos os cedentes) com a camada OFICIAL (Fase A, D-DONO-6).

Junta, por SQL, a base `zepec/ferramenta/zepec_cedentes.csv` (6.131 imóveis) com:
  - `zepec/oficial/iptu2026_cedentes.csv`  -> Atc (área do terreno), área construída, valor venal m², uso (IPTU 2026, oficial)
  - `zepec/oficial/q14_cedentes_2025.csv`  -> V de outorga do m² (Quadro 14 jan/2025, oficial), casado por (SQ, Codlog do IPTU)

Saída: `zepec/ferramenta/zepec_cedentes_oficial.csv` — a ferramenta completa + colunas oficiais.
Agnóstico (R2): só fato, sem juízo. O POTENCIAL (PCpt = Atc × CAbás × Fi) NÃO é calculado aqui:
falta o CAbás (zona por lote — zoneamento ainda não carregado). Nenhum número é inventado (1.3);
a coluna `pendencia_calculo` declara exatamente o que falta por imóvel.

Vacina (dois "V"): v_venal_m2_iptu (planta genérica IPTU) ≠ v_outorga_m2_q14 (Quadro 14). Não intercambiar.
"""
import csv
from pathlib import Path

AQUI = Path(__file__).resolve().parent

def norm_codlog(c):
    return (c or "").replace("-", "").strip()

def main():
    iptu = {}
    for r in csv.DictReader(open(AQUI / "oficial/iptu2026_cedentes.csv", encoding="utf-8")):
        iptu[r["sql_mestre"]] = r

    q14 = {}
    for r in csv.DictReader(open(AQUI / "oficial/q14_cedentes_2025.csv", encoding="utf-8")):
        q14[(r["sq"], norm_codlog(r["codlog"]))] = r["valor_m2_brl"]

    rows = list(csv.DictReader(open(AQUI / "ferramenta/zepec_cedentes.csv", encoding="utf-8")))
    extras = ["area_terreno_m2", "area_construida_m2", "v_venal_m2_iptu",
              "v_outorga_m2_q14", "uso_iptu", "cobertura_oficial", "pendencia_calculo"]
    campos = list(rows[0].keys()) + extras

    n_area = n_v = 0
    out = AQUI / "ferramenta/zepec_cedentes_oficial.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for r in rows:
            sql = (r.get("sql_mestre") or "").strip()
            i = iptu.get(sql)
            cobertura, pend = [], []
            if i:
                r["area_terreno_m2"] = i["area_terreno"]
                r["area_construida_m2"] = i["area_construida"]
                r["v_venal_m2_iptu"] = i["v_venal_m2"]
                r["uso_iptu"] = i["uso"]
                cobertura.append("IPTU2026")
                n_area += 1
                v = q14.get((sql[:6], norm_codlog(i.get("codlog"))))
                if v:
                    r["v_outorga_m2_q14"] = v
                    cobertura.append("Q14-2025")
                    n_v += 1
                else:
                    pend.append("V outorga: face (SQ,Codlog) fora do recorte Q14")
            else:
                pend.append("Atc: SQL sem match no IPTU 2026 (sem cadastro/condominio/SQL invalido)")
            pend.append("CAbas: zona por lote pendente (zoneamento nao carregado)")
            r["cobertura_oficial"] = "+".join(cobertura)
            r["pendencia_calculo"] = " | ".join(pend)
            w.writerow(r)

    print(f"enriquecer_oficial: {len(rows)} cedentes -> {out.name}")
    print(f"  com Atc/area oficial (IPTU 2026): {n_area} ({n_area/len(rows):.0%})")
    print(f"  com V de outorga (Q14 2025):      {n_v} ({n_v/len(rows):.0%})")
    print("  PCpt/preco: NAO calculados (falta CAbas/zona — declarado por linha em pendencia_calculo)")

if __name__ == "__main__":
    main()
