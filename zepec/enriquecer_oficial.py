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
        # L3 (2026-07-10): se o Fi da Declaração está na base (fi_declarado), o PCpt é FIRME (o valor
        # declarado, Art. 125 §1º I) — não a estimativa. Sem ele, segue PENDENTE (falta o dado da Declaração).
        if (r.get("fi_declarado") or "").strip():
            return "JA_DECLARADO", "DECLARADO_FIRME"
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
    # L3 (2026-07-10): já-declarado COM o Fi da Declaração na base → PCpt FIRME (usa o declarado, Art.125 §1º I);
    # SEM ele, segue PENDENTE. Prova o mecanismo de redação-datada (pronto p/ quando o fi_declarado subir).
    assert regime_pcpt({"tem_declaracao": "sim", "fi_declarado": "1.4"}) == ("JA_DECLARADO", "DECLARADO_FIRME")
    assert regime_pcpt({"tem_declaracao": "sim"}) == ("JA_DECLARADO", "PENDENTE_FI_DECLARADO")
    return True


# ---------------------------------------------------------------------------
# Motor Fórmulas — cálculo PURO do PCpt (princípio 1.1: fórmula é engine).
# Número nasce no engine (1.3); cita Art. 24 I–VII LPUOS (escalonado) e Art. 125 §1º I PDE.
# ---------------------------------------------------------------------------
def _calcular_pcpt(r, atc, cabas, pend, n, setor_central=False):
    """Calcula PCpt (m²) e saldo líquido via ENGINE. Devolve o saldo (Decimal) ou None se falhar.
    Correções do loop de melhoria (2026-07-02):
      (a) Fi ESCALONADO pela área do lote (LPUOS Art. 24 I–VII) — resolvido no engine;
      (b) SALDO líquido: abate o m² JÁ TRANSFERIDO (certidões) do PCpt;
      (d) parcelamento Art. 124 §3º (>50.000 m² → 10 parcelas) EXPOSTO na saída.
    setor_central (2026-07-10, ativação FSCE): pertinência à AIU-SCE é ENTRADA geográfica
      ('1' da camada perímetro AIU-SCE, GeoSampa) — o teto de terreno ≤1.000 m² do Art. 57
      é resolvido DENTRO do engine (1.3)."""
    try:
        # L3 (2026-07-10): já-declarado COM Fi da Declaração usa o valor DECLARADO (Art. 125 §1º I),
        # não o escalonado (Art. 24 caput = estimador de NOVAS declarações). Redação datada: a Declaração
        # fixa o Fi vigente na sua data de referência. Sem fi_declarado na base, mantém o escalonado (no-op).
        fi_dec = _num(r.get("fi_declarado"))
        ja_declarado = (r.get("tem_declaracao") or "").strip().lower() in ("sim", "true", "1") \
            or (r.get("tem_certidao") or "").strip().lower() in ("sim", "true", "1")
        if fi_dec and ja_declarado:
            e = ENGINE.pcpt_sem_doacao(atc, cabas, fi=fi_dec, setor_central=setor_central)
        else:
            e = ENGINE.pcpt_sem_doacao(atc, cabas, setor_central=setor_central)
        r["pcpt_m2"] = str(e["valor_m2"]); r["fi_aplicado"] = e.get("fi", "")
        if e.get("fsce") not in (None, "", "1"):
            r["fsce_aplicado"] = e["fsce"]; n["fsce"] += 1
        r["memoria_calculo"] = e["memoria_calculo"]; n["pcpt"] += 1
        if int(e.get("parcelas_anuais") or 0) > 0:
            r["parcelas_anuais"] = str(e["parcelas_anuais"])
            pend.append(f"Art.124 §3º: excedente de 50.000 m² sai em {e['parcelas_anuais']} parcelas anuais")
        ja = (r.get("m2_ja_transferido") or "").strip()
        saldo = Decimal(str(e["valor_m2"])) - (Decimal(ja) if ja else Decimal("0"))
        if saldo < 0:
            saldo = Decimal("0"); pend.append("saldo: já transferido > PCpt calculado — REVISAR (certidão vs cálculo)")
        r["saldo_pcpt_m2"] = str(saldo.quantize(Decimal("0.01"))); n["saldo"] += 1
        return saldo
    except Exception as ex:
        pend.append(f"PCpt: engine recusou ({ex})")
        return None


# ---------------------------------------------------------------------------
# Motor Comercial — decisão de preço-proxy (princípio 1.1: comercial ≠ fórmula).
# preço-proxy (R$) = saldo × V (Codex Precificação R16; NÃO é preço de mercado).
# (c) ESGOTADO/VEDADO não é precificado (não se vende o invendável).
# ---------------------------------------------------------------------------
def _precificar(r, saldo, vendido_bloqueado, pend, n):
    """Calcula preço-proxy regulatório a partir do saldo e do V de outorga (Quadro 14).
    Separado de _calcular_pcpt por princípio 1.1: decisão comercial ≠ fórmula de engine."""
    if vendido_bloqueado:
        pend.append("ESGOTADO/VEDADO — não precificar (prova escrita na base)")
        return
    vq = r["v_outorga_m2_q14"]
    if vq and saldo > 0:
        LIMITE_PARCELAMENTO = Decimal("50000")
        preco_base = min(saldo, LIMITE_PARCELAMENTO)
        preco = (preco_base * Decimal(str(vq))).quantize(Decimal("0.01"))
        r["preco_proxy_brl"] = str(preco); n["preco"] += 1
        if saldo > LIMITE_PARCELAMENTO:
            r["parcelas_anuais"] = "10"


def main():
    iptu = {r["sql_mestre"]: r for r in csv.DictReader(open(AQUI / "oficial/iptu2026_cedentes.csv", encoding="utf-8"))}
    # VTcd vigente = Quadro 14 ano-ref 2026 (Dec. 64.884/2025, +7,18% uniforme sobre o ano-ref 2025
    # oficial — gerado por pipeline/reajuste_q14_2026.py; base legal no docstring desse gerador).
    # Supersede o ano-ref 2025 (Dec. 63.999/2024) a partir do exercício 2026 (1.6 vigência). O arquivo
    # oficial/q14_cedentes_2025.csv fica no repo para auditoria da vigência anterior.
    q14 = {(r["sq"], norm_codlog(r["codlog"])): r["valor_m2_brl"]
           for r in csv.DictReader(open(AQUI / "oficial/q14_cedentes_2026.csv", encoding="utf-8"))}
    # G4 — Decreto 57.536/2016 Art. 3º IV: lotes com frente para distintas faces da mesma quadra
    # usam o MAIOR valor do Q14. Agrupa por SQ para calcular max.
    q14_por_sq = defaultdict(list)
    for (sq, codlog), val in q14.items():
        q14_por_sq[sq].append(Decimal(val))
    q14_max = {sq: max(vals) for sq, vals in q14_por_sq.items()}
    zona = {r["sql_mestre"]: r for r in csv.DictReader(open(AQUI / "oficial/zona_por_cedente.csv", encoding="utf-8"))}

    rows = list(csv.DictReader(open(AQUI / "ferramenta/zepec_cedentes.csv", encoding="utf-8")))
    extras = ["area_terreno_m2", "area_construida_m2", "valor_m2_terreno_iptu", "v_outorga_m2_q14",
              "v_outorga_max_q14",
              "zona", "ca_basico", "fi_aplicado", "fsce_aplicado", "pcpt_m2", "saldo_pcpt_m2", "parcelas_anuais",
              "preco_proxy_brl", "uso_iptu", "cobertura_oficial", "memoria_calculo", "pendencia_calculo",
              # T3 — regime do PCpt: separa já-declarado (Art.125 §1º I) de prospecção nova (Art.24 caput).
              "regime_pcpt", "qualidade_estimativa"]
    campos = list(rows[0].keys()) + extras

    n = {"atc": 0, "v": 0, "zona": 0, "cabas": 0, "pcpt": 0, "saldo": 0, "preco": 0,
         "multi_face": 0, "vedado": 0, "fsce": 0}
    out = AQUI / "ferramenta/zepec_cedentes_oficial.csv"
    enr = []
    for r in rows:
        sql = (r.get("sql_mestre") or "").strip()
        for k in extras: r.setdefault(k, "")
        cob, pend = [], []
        i, z = iptu.get(sql), zona.get(sql)

        # OP-2 (garimpo M6): CONPRESP Res. 01/CONPRESP/2025 (27/01/2025) ARQUIVOU a abertura de processo
        # de tombamento (APT) de PARTE da Mancha Heterogênea "Benedito Calixto (I)" (Anexo II da Res.
        # 11/CONPRESP/2023), mas MANTEVE os elementos 1I, 2I, 4I, 10I e 11I. Logo os 26 cedentes desta
        # quadra (013.036) precisam de REVISÃO: os arquivados viram falso-positivo (APT arquivada não
        # gera TDC por tombamento); os mantidos seguem válidos. Sinal honesto (NÃO remove) — falta o mapa
        # elemento-ID -> SQL para dizer QUAIS (want-list M6). Fonte: legislacao.prefeitura.sp.gov.br.
        if sql.startswith("013036"):
            pend.append("REVISAR TOMBAMENTO — CONPRESP Res. 01/2025 (27/01/2025) arquivou PARTE da Mancha "
                        "Benedito Calixto (I); manteve 1I/2I/4I/10I/11I. Confirmar se este SQL foi arquivado "
                        "(falso-positivo) ou mantido antes de prospectar (precisa do mapa elemento->SQL)")

        atc = _num(i["area_terreno"]) if i else ""
        if i:
            r["area_terreno_m2"] = i["area_terreno"]; r["area_construida_m2"] = i["area_construida"]
            # CORREÇÃO 2026-07-10: a coluna 17 do IPTU_2026 é VALOR DO M2 DO TERRENO, não valor venal
            # (bug de rótulo do extrator antigo, provado 3905/3905 contra o cabeçalho oficial do arquivo).
            r["valor_m2_terreno_iptu"] = i["valor_m2_terreno"]; r["uso_iptu"] = i["uso"]; cob.append("IPTU2026"); n["atc"] += 1
            sq6 = sql[:6]
            v = q14.get((sq6, norm_codlog(i.get("codlog"))))
            if v: r["v_outorga_m2_q14"] = v; cob.append("Q14"); n["v"] += 1
            # G4 — Decreto 57.536/2016 Art. 3º IV: MAX do Q14 por quadra (todas as faces).
            vmax = q14_max.get(sq6)
            if vmax is not None:
                r["v_outorga_max_q14"] = str(vmax)
                if v and Decimal(v) < vmax:
                    n["multi_face"] += 1
                    pend.append(f"Decreto 57.536/2016 Art. 3º IV: se lote tem frente p/ distintas faces, "
                                f"V=MAX(Q14)=R${vmax}/m² (face atual: R${v}/m²)")
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

        # T8 — VEDAÇÃO GEOMÉTRICA Art. 124 §2º (Lei 16.050/2014): categorias AUE/APPa são VEDADAS
        # à cessão de PCpt. Guard ANTES do cálculo: vedado → PCpt/saldo/preço não calculados.
        # Hoje a detecção é por substring na categoria (montar_base.py); a geometria via shapefile
        # ZEPEC_AUE será ligada quando as coordenadas do lote estiverem disponíveis (vedacao_geo.py).
        vedado_lei = (r.get("motivo_negociavel") or "").strip().startswith("vedado por lei")
        vendido_bloqueado = (r.get("esgotado") or "").strip() == "sim" or (r.get("negociavel") or "").strip() == "nao"

        if vedado_lei:
            pend.append("Art. 124 §2º: cessão VEDADA (AUE/APPa) — PCpt/saldo/preço não calculados "
                        "(potencial é intransferível; Lei 16.050/2014)")
            n["vedado"] += 1
        elif atc and cabas:
            # FSCE (Art. 57, Lei 17.844/2022): ZEPEC-BIR dentro da AIU-SCE (Setor Central).
            # Pertinência é ENTRADA geográfica ('1'/'0'/'?' da camada perímetro AIU-SCE via
            # GeoSampa, propagada por preencher_cabas_do_wfs.py ao zona_por_cedente.csv).
            # Fail-closed: só '1' liga o FSCE; '?'/vazio em BIR vira pendência declarada.
            # CAVEAT DE PROVENIÊNCIA (lente 2026-07-10): na_aiu_sce hoje vem das camadas GeoSampa
            # `perimetro_aiu` (núcleo) + `requalifica_centro_perimetro_geral` (proxy), NÃO do Mapa 2
            # oficial dos "perímetros EXPANDIDOS" do Art. 57. Risco: BIR≤1.000 m² num perímetro
            # expandido fora do núcleo pode sair '0' → FSCE omitido (subavaliação de 50%). Pendência
            # declarada: obter os 2 polígonos expandidos do Mapa 2 (Lei 17.844) e uni-los à camada.
            bir = "BIR" in (r.get("tipo_zepec") or "")
            sce = ((z.get("na_aiu_sce") or "").strip() if z else "")
            saldo = _calcular_pcpt(r, atc, cabas, pend, n, setor_central=(bir and sce == "1"))
            if bir and sce not in ("1", "0"):
                pend.append("FSCE (Art.57 Lei 17.844/2022): pertinência à AIU-SCE PENDENTE "
                            "(coleta GeoSampa) — PCpt calculado SEM FSCE")
            elif bir and sce == "1" and Decimal(str(atc)) > Decimal("1000"):
                # rastro do teto (lente 2026-07-10): número certo (engine não aplica o FSCE),
                # mas a linha ficava MUDA sobre o porquê — persiste a razão legal.
                pend.append("Art. 57 Lei 17.844/2022: imóvel NA AIU-SCE porém terreno > 1.000 m² "
                            "— FSCE NÃO aplicável (teto do Art. 57); PCpt sem o fator")
            if saldo is not None:
                _precificar(r, saldo, vendido_bloqueado, pend, n)

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
        elif not completo:
            txt_saldo = f"PENDENTE-CONJUNTO: {saldo_conj} m² parcial (há membro sem PCpt — saldo INDETERMINADO até completar)"
        else:
            txt_saldo = f"{saldo_conj} m² (Σ PCpt − transferido)"
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
    for k, lbl in [("atc", "Atc (área)"), ("v", "V outorga (Q14)"), ("multi_face", "Multi-face (G4 Dec.57536)"),
                   ("zona", "Zona"), ("cabas", "CAbás"), ("vedado", "Vedado Art.124§2 (sem PCpt)"),
                   ("pcpt", "PCpt calculado (engine)"), ("fsce", "FSCE aplicado (Art.57 SCE)"),
                   ("saldo", "Saldo líquido (– transferido)"), ("preco", "Preço-proxy R$ (do saldo)")]:
        print(f"  {lbl:26}: {n[k]:5} ({n[k]/tot:.0%})")


if __name__ == "__main__":
    if "--autoteste" in sys.argv:
        _autoteste_regime()
        print("AUTO-TESTE regime PCpt (T3): OK — já-declarado=PENDENTE_FI_DECLARADO · "
              "prospecção-nova=ESTIMATIVA_PROSPECCAO_ART24 (escalonado nunca vira 'declarado').")
    else:
        main()
