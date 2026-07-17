#!/usr/bin/env python3
"""
gerar_dossie.py — DOSSIÊ de 1 página por imóvel cedente (Marco M1, produto ao cliente).

Junta, num documento acionável e rastreável, tudo o que a base enriquecida já sabe de um cedente:
identificação, situação de negócio, potencial construtivo (memória citada), PREÇO LEGAL (Art. 128 via
engines/tdc/art128.py), datas/vigência, checklist de due-diligence e pendências — cada número com o
dispositivo de origem (1.7). NÃO define preço de venda: entrega o piso regulatório; a margem é do dono
(D-DONO-7/15). NÃO inventa número: tudo vem da base (enriquecer_oficial.py) e dos engines (1.3).

Uso:
    python3 zepec/gerar_dossie.py --sql 0200670033          # imprime o dossiê de um imóvel
    python3 zepec/gerar_dossie.py --pilotos [N]             # gera os N dossiês com dono → ferramenta/dossies/
    python3 zepec/gerar_dossie.py --autoteste               # gate: invariantes do dossiê
PU 18 · 2026-07-10.
"""
import csv
import sys
import argparse
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "engines" / "tdc"))
import art128  # noqa: E402

SRC = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes_oficial.csv"
OUT_DIR = RAIZ / "zepec" / "ferramenta" / "dossies"

DEC = "Decreto Municipal SP nº 57.536/2016"
LEI = "Lei Municipal SP nº 16.050/2014 (PDE)"

GLOSSA_ESTAGIO = {
    "INTACTO": "declarou potencial e nunca vendeu — potencial cheio",
    "TEM_SALDO": "vendeu parte; ainda resta potencial a transferir",
    "SO_ELEGIVEL": "tombado que ainda não declarou (pode entrar; precisa declarar antes)",
    "INCERTO": "situação a confirmar",
}
GLOSSA_CONSERV = {
    "ELEGIVEL": "tem Atestado de Preservação e Conservação vigente (Art. 129 atendido)",
    "PENDENTE": "conservação a comprovar — falta o Atestado (Art. 129)",
    "SEM_ATESTADO": "sem Atestado de Preservação e Conservação na base (Art. 129 a verificar)",
}
GLOSSA_REGIME = {
    "JA_DECLARADO": "já possui Declaração — o PCpt vale o que a Declaração fixou (Art. 125 §1º)",
    "PROSPECCAO_NOVA": "prospecção nova — PCpt é estimativa pelo escalonado (LPUOS Art. 24)",
}


def _dec(s):
    try:
        return art128._d(s, "x")
    except Exception:
        return None


def _brl(d):
    """Decimal → 'R$ 1.234.567,89' (formato brasileiro)."""
    if d is None:
        return "—"
    q = Decimal(d).quantize(Decimal("0.01"))
    inteiro, _, cent = f"{q:.2f}".partition(".")
    neg = inteiro.startswith("-")
    inteiro = inteiro.lstrip("-")
    grupos = []
    while len(inteiro) > 3:
        grupos.insert(0, inteiro[-3:]); inteiro = inteiro[:-3]
    grupos.insert(0, inteiro)
    return ("-" if neg else "") + "R$ " + ".".join(grupos) + "," + cent


def _m2(s):
    d = _dec(s)
    return f"{d} m²".replace(".", ",") if d is not None else "—"


def _tenta_base_b(saldo, vtcd_vig, esquina, r):
    """§2º CRISTALIZADO (base B do MAX) — só quando a LEI o determina: Declaração E Certidão protocoladas.
    Reconstrói o VTcd histórico da data de referência (Declaração) a partir do VTcd vigente 2026, pela razão
    de reajuste UNIFORME do Quadro 14 (art128.vtcd_na_data), e aplica o §2º IPCA até o protocolo da Certidão.
    Datas: data_declaracao_iso = data de referência (Art. 125 §2º / mês-ref do §2º); data_certidao_iso =
    protocolo da Certidão (mês-fim do §2º). Devolve (mx, conv) ou None (fail-closed 1.3: dado faltante,
    Declaração pré-2014 fora da série IPCA, etc. → cai na base A vigente, sem inventar 'hoje')."""
    d_decl = (r.get("data_declaracao_iso") or "").strip()
    d_cert = (r.get("data_certidao_iso") or "").strip()
    if len(d_decl) < 7 or len(d_cert) < 7:
        return None                       # sem Declaração+Certidão datadas → §2º não cristalizou
    try:
        ano_decl = int(d_decl[:4])
        conv = art128.vtcd_na_data(str(vtcd_vig), 2026, ano_decl)      # VTcd histórico (2026 → ano-ref)
        mx = art128.referencia_max_art128(str(saldo), str(vtcd_vig), via="125", esquina=esquina,
                                          vtcd_declaracao=conv["vtcd_alvo_m2"],
                                          mes_ref=d_decl[:7], mes_protocolo=d_cert[:7])
        return mx, conv
    except Exception:
        return None                       # mês-ref fora da série IPCA (pré-2014) etc. → base A


def _preco_bloco(r):
    """Bloco 4 — Preço legal (Art. 128) via engine. Devolve (markdown, ref) ou (nota, None).
    Já-declarado com Declaração E Certidão protocoladas ⇒ §2º cristalizado: MAX(A piso vigente ;
    B VTcd da Declaração×IPCA), com o VTcd histórico reconstruído por art128.vtcd_na_data. Senão ⇒
    base A (Quadro 14 vigente 2026), fail-closed (1.3). O `ref` devolvido sempre carrega
    referencia_brl/numerador_brl/base (contrato estável p/ o autoteste e chamadores)."""
    saldo = _dec(r.get("saldo_pcpt_m2"))
    vtcd = _dec(r.get("v_outorga_m2_q14"))
    if not saldo or saldo <= 0 or not vtcd or vtcd <= 0:
        return ("- _Preço legal ainda não calculável_ — falta saldo vendável e/ou valor de terreno "
                "(Quadro 14) para este imóvel. Ver pendências.\n", None)
    vmax = _dec(r.get("v_outorga_max_q14"))
    esquina = bool(vmax and vmax > vtcd)
    vtcd_vig = vmax if esquina else vtcd   # Dec. 57.536/2016 Art. 3º IV — esquina usa o MAIOR do Quadro 14
    ja_declarado = (r.get("regime_pcpt") == "JA_DECLARADO")
    base_b = _tenta_base_b(saldo, vtcd_vig, esquina, r) if ja_declarado else None
    md = []

    if base_b is not None:
        mx, conv = base_b
        venc = mx["base_vencedora"]
        ref = {"referencia_brl": mx["referencia_max_brl"], "numerador_brl": mx["numerador_max_brl"], "base": venc}
        md.append(f"- **Referência legal (independe do comprador):** **{_brl(ref['referencia_brl'])}**  "
                  f"*(MAX das duas bases que a lei assegura — vence a base {venc})*")
        md.append(f"  - fórmula: (PCpt × VTcd) ÷ CAmaxcd — Art. 128 §1º (o Cr do comprador cancela na conta)")
        md.append(f"- **Valor bruto (potencial × terreno):** {_brl(ref['numerador_brl'])}")
        for c in mx["cenarios"]:
            marca = "  ◄ vence" if c["base"] == venc else ""
            md.append(f"  - **Base {c['base']}** — {c['rotulo']}: VTcd R$ {c['vtcd_aplicado_m2']}/m² → "
                      f"**{_brl(c['referencia_brl'])}**{marca}")
        md.append(f"  - _§2º cristalizado:_ VTcd da Declaração reconstruído pela razão de reajuste do "
                  f"Quadro 14 ({conv['memoria_calculo']}), corrigido por IPCA até o protocolo da Certidão.")
        md.append(f"- Componentes: saldo **{_m2(saldo)}** × VTcd (por base, acima)"
                  + (" *(esquina: maior valor da quadra, Dec. 57.536/2016 Art. 3º IV)*" if esquina else "")
                  + " ÷ CAmaxcd **4**")
        md.append(f"- _Citação:_ {mx['citacao']['dispositivo']}. **A margem é sua** — isto é o piso "
                  f"regulatório, não o preço de venda (D-DONO-7).")
        return ("\n".join(md) + "\n", ref)

    # base A — Quadro 14 vigente (prospecção nova, ou já-declarado sem Certidão protocolada)
    ref_a = art128.referencia_art128(str(saldo), str(vtcd_vig), via="125", esquina=esquina)
    ref = {"referencia_brl": ref_a["referencia_brl"], "numerador_brl": ref_a["numerador_brl"], "base": "A"}
    md.append(f"- **Referência legal (independe do comprador):** **{_brl(ref['referencia_brl'])}**")
    md.append(f"  - fórmula: (PCpt × VTcd) ÷ CAmaxcd — Art. 128 §1º (o Cr do comprador cancela na conta)")
    md.append(f"- **Valor bruto (potencial × terreno):** {_brl(ref['numerador_brl'])}")
    md.append(f"- Componentes: saldo **{_m2(saldo)}** × VTcd **{_brl(vtcd_vig)}/m²**"
              + (" *(esquina: maior valor da quadra, Dec. 57.536/2016 Art. 3º IV)*" if esquina else "")
              + " ÷ CAmaxcd **4**")
    if ja_declarado:
        md.append("- ⚠️ *Já-declarado, §2º ainda não cristalizado:* o valor exato do Art. 128 §2º usa o VTcd "
                  "**da data da Declaração + IPCA até o protocolo da Certidão**. O VTcd histórico já é "
                  "reconstruível (motor `vtcd_na_data`); falta a **data do protocolo da Certidão** nesta base "
                  "— enquanto não houver Certidão protocolada, vale o Quadro 14 vigente (2026) acima.")
    md.append(f"- _Citação:_ Art. 128 (PDE), caput e §1º. **A margem é sua** — isto é o piso regulatório, "
              f"não o preço de venda (D-DONO-7).")
    return ("\n".join(md) + "\n", ref)


def _checklist(r):
    """Bloco 6 — due-diligence do cedente. Itens LEGAIS citados + operacionais a confirmar."""
    cons = r.get("elegibilidade_conservacao", "")
    linhas = [
        f"- [ ] **Conservação (Art. 129, PDE):** {GLOSSA_CONSERV.get(cons, cons or 'verificar')} "
        f"— exigir o Atestado de Preservação e Conservação vigente.",
        f"- [ ] **Matrícula atualizada** do imóvel (Art. 5º VI, {DEC}).",
        f"- [ ] **IPTU do exercício** — notificação/recibo (Art. 5º V, {DEC}).",
        f"- [ ] **Documentos do proprietário** — RG/CPF (pessoa física) ou CNPJ + contrato/estatuto "
        f"(pessoa jurídica); procuração se houver (Art. 5º I–IV, {DEC}).",
    ]
    if (r.get("tipo_zepec") or "").upper().find("APC") >= 0:
        linhas.append(f"- [ ] **ZEPEC-APC:** transferência só sob o uso que o tombamento confere "
                      f"(Art. 23, {DEC}).")
    linhas += [
        "- [ ] **CADIN municipal** — ausência de débitos que travem a emissão (verificação operacional).",
        "- [ ] **Situação no DPH/CONPRESP** — sem intercorrência de tombamento (verificação operacional).",
    ]
    inter = (r.get("intercorrencia_fundurb") or "").strip()
    if inter and inter not in ("nao", "—", ""):
        linhas.append(f"- [ ] **FUNDURB:** intercorrência registrada ({inter}) — checar antes de avançar.")
    return "\n".join(linhas) + "\n"


def montar_dossie(r):
    """Devolve o dossiê (Markdown) de 1 imóvel a partir de uma linha da base enriquecida."""
    nome = (r.get("nome_bem") or "Imóvel tombado").strip()
    sql = (r.get("sql_mestre") or "").strip()
    end = (r.get("endereco_mestre") or "").strip()
    dist = (r.get("distrito") or "").strip()
    est = (r.get("estado_venda") or "").strip()
    regime = (r.get("regime_pcpt") or "").strip()
    prop = (r.get("proprietario") or "").strip() or "_a identificar_"
    preco_md, ref = _preco_bloco(r)

    o = []
    o.append(f"# Dossiê do imóvel — {nome}")
    o.append(f"**Potencial Urbano · TDC (Transferência do Direito de Construir)**  ·  "
             f"documento determinístico, cada número rastreável ao dispositivo legal\n")

    o.append("## 1. Identificação")
    o.append(f"- **Imóvel (SQL):** `{sql}`  ·  **Endereço:** {end}{(' — ' + dist) if dist else ''}")
    o.append(f"- **Tombamento:** {r.get('tipo_zepec','—')}  ·  **Esfera:** {r.get('esfera','—')}")
    o.append(f"- **Zona:** {r.get('zona','—')} (CA básico {r.get('ca_basico','—')})  ·  "
             f"**Uso (IPTU):** {r.get('uso_iptu','—')}")
    o.append(f"- **Proprietário:** {prop}\n")

    o.append("## 2. Situação para negócio")
    o.append(f"- **Estágio:** {est} — {GLOSSA_ESTAGIO.get(est, '')}")
    o.append(f"- **Negociável:** {r.get('negociavel','—')} ({r.get('motivo_negociavel','—')})")
    o.append(f"- **Regime do potencial:** {GLOSSA_REGIME.get(regime, regime)}")
    jt = _dec(r.get("m2_ja_transferido"))
    if jt and jt > 0:
        o.append(f"- **Já transferido:** {_m2(jt)} em {r.get('n_transferencias','?')} operação(ões)")
    o.append("")

    o.append("## 3. Potencial construtivo (memória de cálculo)")
    o.append(f"- {r.get('memoria_calculo','—')}")
    saldo = _dec(r.get("saldo_pcpt_m2"))
    parc = (r.get("parcelas_anuais") or "").strip()
    if saldo is not None:
        entrega = (f"à vista" if not parc or parc in ("0", "") else
                   f"acima de 50.000 m² → 10 parcelas anuais (Art. 124 §3º, PDE)")
        o.append(f"- **Saldo vendável:** {_m2(saldo)}  ·  **Entrega:** {entrega}")
    o.append(f"- _Citação:_ Art. 125 (PDE) c/c LPUOS Art. 24"
             + ("; Art. 57 (Lei 17.844/2022) se Setor Central" if r.get("fsce_aplicado") not in ("", None) else "") + "\n")

    o.append("## 4. Preço legal de referência (Art. 128, PDE)")
    o.append(preco_md)

    o.append("## 5. Datas e vigência (Princípio 1.6)")
    o.append(f"- **Declaração:** {r.get('data_declaracao_iso') or '—'}  ·  "
             f"**Certidão:** {r.get('data_certidao_iso') or '—'}  ·  "
             f"**Tombamento:** {r.get('data_tombamento_iso') or '—'}")
    o.append(f"- **Data de referência (protocolo da Declaração — Art. 125 §2º; base do §2º do Art. 128):** "
             f"{r.get('data_declaracao_iso') or '—'}\n")

    o.append("## 6. Checklist de due-diligence (antes de fechar)")
    o.append(_checklist(r))

    pend = (r.get("pendencia_calculo") or "").strip()
    qual = (r.get("qualidade_estimativa") or "").strip()
    if pend or qual:
        o.append("## 7. Pendências e qualidade")
        if qual:
            o.append(f"- **Qualidade da estimativa:** {qual}")
        if pend:
            o.append(f"- **Pendências:** {pend}")
        o.append("")

    o.append("---")
    o.append(f"**Fontes:** {r.get('cobertura_oficial','—')}  ·  IPTU 2026 (Prefeitura de SP), "
             f"Quadro 14 (Cadastro de Valor de Terreno), GeoSampa (zona/CA), Diário Oficial (Declarações).")
    o.append("_Potencial Urbano — preço é dado de engine, rastreável ao artigo; a margem é do usuário. "
             "Nenhum número foi inventado (Princípios 1.3/1.7)._")
    return "\n".join(o), ref


def _linhas():
    return list(csv.DictReader(open(SRC, encoding="utf-8")))


def _autoteste():
    rows = _linhas()
    assert rows, "base vazia"
    # 1) todo imóvel com saldo+VTcd gera dossiê e o preço bate o art128 (sem inventar)
    com_preco = 0
    com_base_b = 0
    for r in rows:
        md, ref = montar_dossie(r)
        assert md.startswith("# Dossiê do imóvel"), r.get("sql_mestre")
        assert "Art. 128" in md and "Art. 129" in md and "Art. 125" in md, r.get("sql_mestre")
        assert "due-diligence" in md.lower()
        if ref is not None:
            com_preco += 1
            saldo = _dec(r.get("saldo_pcpt_m2"))
            vtcd = _dec(r.get("v_outorga_m2_q14"))
            vmax = _dec(r.get("v_outorga_max_q14"))
            esquina = bool(vmax and vmax > vtcd)
            v = vmax if esquina else vtcd
            # Recompute pelo MESMO ramo que o montar usa (base B §2º cristalizado quando a lei o determina;
            # senão base A vigente) — independente do CSV, ancorado no engine: sabota o q14/IPCA e diverge.
            bb = _tenta_base_b(saldo, v, esquina, r) if (r.get("regime_pcpt") == "JA_DECLARADO") else None
            if bb is not None:
                com_base_b += 1
                esp_ref = bb[0]["referencia_max_brl"]
                assert ref["base"] == bb[0]["base_vencedora"], r.get("sql_mestre")
            else:
                esp_ref = art128.referencia_art128(str(saldo), str(v), via="125", esquina=esquina)["referencia_brl"]
                assert ref["base"] == "A", r.get("sql_mestre")
            assert esp_ref == ref["referencia_brl"], r.get("sql_mestre")
            assert _brl(ref["referencia_brl"]).startswith("R$"), r.get("sql_mestre")
    assert com_preco > 100, f"esperava muitos dossiês com preço (veio {com_preco})"
    # 2) imóvel sem saldo → bloco de preço vira nota, não quebra
    vazio = {"sql_mestre": "X", "nome_bem": "Teste", "saldo_pcpt_m2": "", "v_outorga_m2_q14": ""}
    md0, ref0 = montar_dossie(vazio)
    assert ref0 is None and "ainda não calculável" in md0
    # 3) NÃO-VÁCUO da base B (§2º cristalizado) — fixture DETERMINÍSTICO, independe da base viva:
    #    já-declarado com Declaração (2018) + Certidão (2024) protocoladas ⇒ MAX(A;B) com VTcd histórico
    #    reconstruído por vtcd_na_data (razão de reajuste do Quadro 14). Garante que a fiação nunca fica morta.
    fix = {"sql_mestre": "FIXB", "nome_bem": "Fixture §2º", "regime_pcpt": "JA_DECLARADO",
           "saldo_pcpt_m2": "1000", "v_outorga_m2_q14": "3000", "v_outorga_max_q14": "",
           "data_declaracao_iso": "2018-05-10", "data_certidao_iso": "2024-03-01",
           "elegibilidade_conservacao": "PENDENTE_CONSERVACAO"}
    md_b, ref_b = montar_dossie(fix)
    conv = art128.vtcd_na_data("3000", 2026, 2018)
    mx = art128.referencia_max_art128("1000", "3000", via="125", esquina=False,
                                      vtcd_declaracao=conv["vtcd_alvo_m2"],
                                      mes_ref="2018-05", mes_protocolo="2024-03")
    assert ref_b is not None and ref_b["referencia_brl"] == mx["referencia_max_brl"], ref_b
    assert ref_b["base"] == mx["base_vencedora"] and len(mx["cenarios"]) == 2, ref_b
    assert "MAX das duas bases" in md_b and "§2º cristalizado" in md_b, "bloco base B mal formado"
    return com_preco, com_base_b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sql")
    ap.add_argument("--pilotos", nargs="?", const=20, type=int)
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()

    if a.autoteste:
        n, nb = _autoteste()
        print(f"AUTO-TESTE dossiê: OK — {n} dossiês com preço legal batem o art128 "
              f"({nb} com §2º cristalizado via base B/vtcd_na_data + fixture não-vácuo); "
              f"citações e checklist presentes.")
        return 0

    rows = _linhas()
    if a.sql:
        r = next((x for x in rows if (x.get("sql_mestre") or "").strip() == a.sql.strip()), None)
        if not r:
            print(f"SQL não encontrado: {a.sql}"); return 1
        md, _ = montar_dossie(r)
        print(md)
        return 0

    if a.pilotos is not None:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        # Piloto = imóveis ACIONÁVEIS (negociável + preço legal). O proprietário fica em base PII
        # separada (donos_encontrados.csv, fora do git) — os dossiês-piloto saem SEM nome (seguros).
        alvos = [r for r in rows if (r.get("negociavel") or "").strip() == "sim"
                 and _dec(r.get("saldo_pcpt_m2")) and _dec(r.get("saldo_pcpt_m2")) > 0
                 and _dec(r.get("v_outorga_m2_q14"))][:a.pilotos]
        for r in alvos:
            md, _ = montar_dossie(r)
            (OUT_DIR / f"dossie_{r['sql_mestre']}.md").write_text(md + "\n", encoding="utf-8")
        print(f"gerados {len(alvos)} dossiês-piloto (imóveis acionáveis, sem PII) em {OUT_DIR}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
