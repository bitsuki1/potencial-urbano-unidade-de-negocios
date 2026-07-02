#!/usr/bin/env python3
"""
enriquecer_oficial.py — Enriquece a FERRAMENTA (todos os cedentes) com a camada OFICIAL (Fase A / H1).

Junta, por SQL, a base `zepec/ferramenta/zepec_cedentes.csv` (6.131) com as fontes oficiais:
  - `zepec/oficial/iptu2026_cedentes.csv`  -> Atc (área do terreno), área construída, valor venal, uso (IPTU 2026)
  - `zepec/oficial/q14_cedentes_2025.csv`  -> V de outorga do m² (Quadro 14 jan/2025), por (SQ, Codlog do IPTU)
  - `zepec/oficial/zona_por_cedente.csv`   -> ZONA do lote (overlay lote×Lei 16.402) + CAbás (Quadro 3)

Calcula (H1.4), SÓ quando há Atc E CAbás, via o ENGINE (número nasce no engine, 1.3; cita Art. 125):
  - PCpt (m²) = Atc × CAbás × Fi(=1, ZEPEC-BIR, sem doação)  [engine `pcpt.pcpt_sem_doacao`]
  - preço-proxy (R$) = PCpt × V   [PROXY regulatório — Codex Precificação R16; NÃO é preço de mercado]

Saída: `zepec/ferramenta/zepec_cedentes_oficial.csv`. Onde falta insumo, `pendencia_calculo` declara o quê
POR LINHA — nada inventado. Vacina dos dois "V": venal (IPTU) ≠ outorga (Quadro 14).
"""
import csv, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "engines" / "tdc"))
import pcpt as ENGINE  # noqa: E402


def norm_codlog(c): return (c or "").replace("-", "").strip()
def _num(x):
    x = (x or "").strip()
    return x if x and x not in ("0", "—") else ""


def main():
    iptu = {r["sql_mestre"]: r for r in csv.DictReader(open(AQUI / "oficial/iptu2026_cedentes.csv", encoding="utf-8"))}
    q14 = {(r["sq"], norm_codlog(r["codlog"])): r["valor_m2_brl"]
           for r in csv.DictReader(open(AQUI / "oficial/q14_cedentes_2025.csv", encoding="utf-8"))}
    zona = {r["sql_mestre"]: r for r in csv.DictReader(open(AQUI / "oficial/zona_por_cedente.csv", encoding="utf-8"))}

    rows = list(csv.DictReader(open(AQUI / "ferramenta/zepec_cedentes.csv", encoding="utf-8")))
    extras = ["area_terreno_m2", "area_construida_m2", "v_venal_m2_iptu", "v_outorga_m2_q14",
              "zona", "ca_basico", "fi_aplicado", "pcpt_m2", "saldo_pcpt_m2", "parcelas_anuais",
              "preco_proxy_brl", "uso_iptu", "cobertura_oficial", "memoria_calculo", "pendencia_calculo"]
    campos = list(rows[0].keys()) + extras

    n = {"atc": 0, "v": 0, "zona": 0, "cabas": 0, "pcpt": 0, "saldo": 0, "preco": 0}
    out = AQUI / "ferramenta/zepec_cedentes_oficial.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader()
        for r in rows:
            sql = (r.get("sql_mestre") or "").strip()
            for k in extras: r.setdefault(k, "")
            cob, pend = [], []
            i, z = iptu.get(sql), zona.get(sql)

            atc = _num(i["area_terreno"]) if i else ""
            if i:
                r["area_terreno_m2"] = i["area_terreno"]; r["area_construida_m2"] = i["area_construida"]
                r["v_venal_m2_iptu"] = i["v_venal_m2"]; r["uso_iptu"] = i["uso"]; cob.append("IPTU2026"); n["atc"] += 1
                v = q14.get((sql[:6], norm_codlog(i.get("codlog"))))
                if v: r["v_outorga_m2_q14"] = v; cob.append("Q14"); n["v"] += 1
            else:
                pend.append("Atc: SQL sem cadastro no IPTU")

            cabas = ""
            if z:
                r["zona"] = z["zona"]; cob.append("Zona"); n["zona"] += 1
                cabas = _num(z.get("ca_basico"))
                if cabas: r["ca_basico"] = cabas; n["cabas"] += 1
                else: pend.append(f"CAbás: zona {z['zona']} sem CA no Quadro 3 (overlay — resolver zona-base)")
            else:
                pend.append("Zona: lote sem sobreposição (sem SQL / lote / fora de zona)")

            # H1.4 — PCpt e preço só quando há Atc E CAbás; número do ENGINE (1.3).
            # ★ Correções do loop de melhoria (2026-07-02):
            #   (a) Fi ESCALONADO pela área do lote (LPUOS Art. 24 I–VII) — resolvido no engine;
            #   (b) SALDO líquido: abate o m² JÁ TRANSFERIDO (certidões) do PCpt — preço sai do SALDO;
            #   (c) ESGOTADO/VEDADO não é precificado (não se vende o invendável);
            #   (d) parcelamento Art. 124 §3º (>50.000 m² → 10 parcelas) EXPOSTO na saída.
            from decimal import Decimal
            vendido_bloqueado = (r.get("esgotado") or "").strip() == "sim" or (r.get("negociavel") or "").strip() == "nao"
            if atc and cabas:
                try:
                    e = ENGINE.pcpt_sem_doacao(atc, cabas)
                    r["pcpt_m2"] = str(e["valor_m2"]); r["fi_aplicado"] = e.get("fi", "")
                    r["memoria_calculo"] = e["memoria_calculo"]; n["pcpt"] += 1
                    if int(e.get("parcelas_anuais") or 0) > 0:
                        r["parcelas_anuais"] = str(e["parcelas_anuais"])
                        pend.append(f"Art.124 §3º: excedente de 50.000 m² sai em {e['parcelas_anuais']} parcelas anuais")
                    ja = (r.get("m2_ja_transferido") or "").strip()
                    saldo = Decimal(str(e["valor_m2"])) - (Decimal(ja) if ja else Decimal("0"))
                    if saldo < 0:
                        saldo = Decimal("0"); pend.append("saldo: já transferido > PCpt calculado — REVISAR (certidão vs cálculo)")
                    r["saldo_pcpt_m2"] = str(saldo.quantize(Decimal("0.01"))); n["saldo"] += 1
                    if vendido_bloqueado:
                        pend.append("ESGOTADO/VEDADO — não precificar (prova escrita na base)")
                    else:
                        vq = r["v_outorga_m2_q14"]
                        if vq and saldo > 0:
                            preco = (saldo * Decimal(str(vq))).quantize(Decimal("0.01"))
                            r["preco_proxy_brl"] = str(preco); n["preco"] += 1
                except Exception as ex:
                    pend.append(f"PCpt: engine recusou ({ex})")

            r["cobertura_oficial"] = "+".join(cob)
            r["pendencia_calculo"] = " | ".join(pend) if pend else "OK (Atc+CAbás+V) — cálculo completo"
            w.writerow(r)

    tot = len(rows)
    print(f"enriquecer_oficial (H1.4): {tot} cedentes -> {out.name}")
    for k, lbl in [("atc", "Atc (área)"), ("v", "V outorga (Q14)"), ("zona", "Zona"),
                   ("cabas", "CAbás"), ("pcpt", "PCpt calculado (engine)"), ("saldo", "Saldo líquido (– transferido)"), ("preco", "Preço-proxy R$ (do saldo)")]:
        print(f"  {lbl:26}: {n[k]:5} ({n[k]/tot:.0%})")


if __name__ == "__main__":
    main()
