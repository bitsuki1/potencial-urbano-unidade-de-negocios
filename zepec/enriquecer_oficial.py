#!/usr/bin/env python3
"""
enriquecer_oficial.py — Enriquece a FERRAMENTA (todos os cedentes) com a camada OFICIAL (Fase A / H1).

Junta, por SQL, a base `zepec/ferramenta/zepec_cedentes.csv` (6.131) com as fontes oficiais:
  - `zepec/oficial/iptu2026_cedentes.csv`  -> Atc (área do terreno), área construída, valor venal, uso (IPTU 2026)
  - `zepec/oficial/q14_cedentes_2025.csv`  -> V de outorga do m² (Quadro 14 jan/2025), por (SQ, Codlog do IPTU)
  - `zepec/oficial/zona_por_cedente.csv`   -> ZONA do lote (overlay lote×Lei 16.402) + CAbás (Quadro 3)

Calcula (H1.4), SÓ quando há Atc E CAbás, via o ENGINE (número nasce no engine, 1.3; cita Art. 125):
  - PCpt (m²) = Atc × CAbás × Fi(ESCALONADO pela área, Art. 24 I–VII LPUOS, sem doação)  [engine `pcpt.pcpt_sem_doacao`]
  - preço-proxy (R$) = PCpt × V   [PROXY regulatório — Codex Precificação R16; NÃO é preço de mercado]

Saída: `zepec/ferramenta/zepec_cedentes_oficial.csv`. Onde falta insumo, `pendencia_calculo` declara o quê
POR LINHA — nada inventado. Vacina dos dois "V": venal (IPTU) ≠ outorga (Quadro 14).
"""
import csv, sys
from pathlib import Path
from decimal import Decimal
from collections import defaultdict

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "engines" / "tdc"))
import pcpt as ENGINE  # noqa: E402


def norm_codlog(c): return (c or "").replace("-", "").strip()
def _num(x):
    x = (x or "").strip()
    return x if x and x not in ("0", "—") else ""


# T3 — REGIME DO PCpt (Art. 24 caput LPUOS × Art. 125 §1º I PDE). O Fi ESCALONADO do Art. 24 aplica-se
# "na emissão de NOVAS declarações" (caput) — logo é o estimador correto para PROSPECÇÃO NOVA (tombado
# ainda SEM declaração). Para o JÁ-DECLARADO, o PCpt total é o que CONSTA NA DECLARAÇÃO (Art. 125 §1º I):
# não renasce no engine com CAbás/Atc/Fi de HOJE. Defeito vivo (enriquecer_oficial.py:81): o engine aplicava
# o escalonado a TODA a base — inclusive ao já-declarado — fabricando um PCpt que NÃO é o declarado. Como o
# Fi/PCpt da Declaração NÃO está na base, o já-declarado fica ESTIMATIVA/PENDENTE, nunca "o valor declarado".
def regime_pcpt(r):
    """Devolve (regime, qualidade_estimativa) para a linha do cedente.
      JA_DECLARADO   + PENDENTE_FI_DECLARADO      — tem declaração/certidão; o escalonado NÃO é o PCpt
                                                    declarado (Art. 125 §1º I); Fi da Declaração ausente na base.
      PROSPECCAO_NOVA + ESTIMATIVA_PROSPECCAO_ART24 — sem declaração; escalonado do Art. 24 caput é o estimador
                                                    lícito de uma futura declaração."""
    v = lambda k: (r.get(k) or "").strip().lower() in ("sim", "true", "1")
    if v("tem_declaracao") or v("tem_certidao"):
        return "JA_DECLARADO", "PENDENTE_FI_DECLARADO"
    return "PROSPECCAO_NOVA", "ESTIMATIVA_PROSPECCAO_ART24"

def _autoteste_regime():
    """Fixtures OBRIGATÓRIAS (T3): já-declarado NUNCA sai como estimativa-de-prospecção firme; prospecção
    nova é a única em que o escalonado é o estimador legítimo. FALHA se a separação de cohort regredir."""
    casos = [
        ({"tem_declaracao": "sim", "tem_certidao": "nao"}, "JA_DECLARADO",   "PENDENTE_FI_DECLARADO"),
        ({"tem_declaracao": "nao", "tem_certidao": "sim"}, "JA_DECLARADO",   "PENDENTE_FI_DECLARADO"),
        ({"tem_declaracao": "nao", "tem_certidao": "nao"}, "PROSPECCAO_NOVA","ESTIMATIVA_PROSPECCAO_ART24"),
        ({"tem_declaracao": "",    "tem_certidao": ""},    "PROSPECCAO_NOVA","ESTIMATIVA_PROSPECCAO_ART24"),
    ]
    for r, reg, qual in casos:
        g_reg, g_qual = regime_pcpt(r)
        assert (g_reg, g_qual) == (reg, qual), f"regime: {r} -> {(g_reg,g_qual)} (esperado {(reg,qual)})"
    # a garantia central do T3: quem TEM declaração/certidão nunca recebe a marca de estimativa-de-prospecção
    for r in ({"tem_declaracao": "sim"}, {"tem_certidao": "sim"}):
        assert regime_pcpt(r)[1] != "ESTIMATIVA_PROSPECCAO_ART24", f"regime: {r} já-declarado != estimativa-prospecção"
    return True


def main():
    iptu = {r["sql_mestre"]: r for r in csv.DictReader(open(AQUI / "oficial/iptu2026_cedentes.csv", encoding="utf-8"))}
    q14 = {(r["sq"], norm_codlog(r["codlog"])): r["valor_m2_brl"]
           for r in csv.DictReader(open(AQUI / "oficial/q14_cedentes_2025.csv", encoding="utf-8"))}
    zona = {r["sql_mestre"]: r for r in csv.DictReader(open(AQUI / "oficial/zona_por_cedente.csv", encoding="utf-8"))}

    rows = list(csv.DictReader(open(AQUI / "ferramenta/zepec_cedentes.csv", encoding="utf-8")))
    extras = ["area_terreno_m2", "area_construida_m2", "v_venal_m2_iptu", "v_outorga_m2_q14",
              "zona", "ca_basico", "fi_aplicado", "pcpt_m2", "saldo_pcpt_m2", "parcelas_anuais",
              "preco_proxy_brl", "uso_iptu", "cobertura_oficial", "memoria_calculo", "pendencia_calculo",
              # T3 — regime do PCpt: separa já-declarado (Art.125 §1º I) de prospecção nova (Art.24 caput).
              "regime_pcpt", "qualidade_estimativa"]
    campos = list(rows[0].keys()) + extras

    n = {"atc": 0, "v": 0, "zona": 0, "cabas": 0, "pcpt": 0, "saldo": 0, "preco": 0}
    out = AQUI / "ferramenta/zepec_cedentes_oficial.csv"
    enr = []
    if True:  # (indentação preservada; a escrita acontece após a passada de CONJUNTO — T11)
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

            # T3 — carimba o REGIME do PCpt. Para o já-declarado, o escalonado calculado acima é ESTIMATIVA,
            # não o PCpt da Declaração (Art. 125 §1º I) — flaga e declara a pendência (Fi declarado ausente).
            reg, qual = regime_pcpt(r)
            r["regime_pcpt"] = reg; r["qualidade_estimativa"] = qual
            if reg == "JA_DECLARADO" and r.get("pcpt_m2"):
                pend.append("PCpt do JÁ-DECLARADO governado pela Declaração (Art.125 §1º I); o escalonado é "
                            "ESTIMATIVA (Art.24 caput = NOVAS declarações), NÃO o valor declarado — Fi/PCpt da "
                            "Declaração ausente na base (PENDENTE). Confiável só p/ prospecção nova.")

            r["cobertura_oficial"] = "+".join(cob)
            r["pendencia_calculo"] = " | ".join(pend) if pend else "OK (Atc+CAbás+V) — cálculo completo"
            enr.append(r)

    # T11 — SALDO POR CONJUNTO (lotes IRMÃOS na mesma certidão). O m² transferido é do CONJUNTO
    # (registrado no 1º lote em montar_ferramenta.py); afirmar saldo POR LOTE ali é inventar alocação.
    # Regra: membros de conjunto têm saldo/preço INDIVIDUAL em branco + pendência declarando o saldo
    # DO CONJUNTO = max(0, Σ PCpt(membros) − transferido_total). Nada é inventado (1.3).
    conj = defaultdict(list)
    for r in enr:
        if (r.get("conjunto_certidao") or "").strip():
            conj[r["conjunto_certidao"]].append(r)
    for cid, membros in sorted(conj.items()):
        pcpts = [Decimal(m["pcpt_m2"]) for m in membros if (m.get("pcpt_m2") or "").strip()]
        transf = sum((Decimal(m["m2_ja_transferido"]) for m in membros
                      if (m.get("m2_ja_transferido") or "").strip()), Decimal("0"))
        completo = len(pcpts) == len(membros)
        saldo_conj = max(Decimal("0"), sum(pcpts, Decimal("0")) - transf).quantize(Decimal("0.01")) if pcpts else None
        if saldo_conj is None:
            txt_saldo = "PENDENTE (nenhum membro com PCpt calculado)"
        else:
            txt_saldo = f"{saldo_conj} m² (Σ PCpt − transferido{'' if completo else '; PARCIAL: há membro sem PCpt'})"
        nota = (f"T11: conjunto {cid} ({len(membros)} lotes irmãos na mesma certidão) — m² transferido é do "
                f"CONJUNTO; saldo individual INDETERMINADO; saldo do conjunto = {txt_saldo}")
        for m in membros:
            if m.get("saldo_pcpt_m2"): n["saldo"] -= 1
            if m.get("preco_proxy_brl"): n["preco"] -= 1
            m["saldo_pcpt_m2"] = ""; m["preco_proxy_brl"] = ""
            m["pendencia_calculo"] = (m["pendencia_calculo"].replace("OK (Atc+CAbás+V) — cálculo completo", "").strip(" |")
                                      + " | " + nota).strip(" |")

    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader()
        for r in enr:
            w.writerow(r)

    tot = len(rows)
    print(f"enriquecer_oficial (H1.4): {tot} cedentes -> {out.name}")
    for k, lbl in [("atc", "Atc (área)"), ("v", "V outorga (Q14)"), ("zona", "Zona"),
                   ("cabas", "CAbás"), ("pcpt", "PCpt calculado (engine)"), ("saldo", "Saldo líquido (– transferido)"), ("preco", "Preço-proxy R$ (do saldo)")]:
        print(f"  {lbl:26}: {n[k]:5} ({n[k]/tot:.0%})")


if __name__ == "__main__":
    if "--autoteste" in sys.argv:
        _autoteste_regime()
        print("AUTO-TESTE regime PCpt (T3): OK — já-declarado=PENDENTE_FI_DECLARADO · "
              "prospecção-nova=ESTIMATIVA_PROSPECCAO_ART24 (escalonado nunca vira 'declarado').")
    else:
        main()
