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


def _preco_bloco(r):
    """Bloco 4 — Preço legal (Art. 128) via engine. Devolve (markdown, dados) ou (nota, None)."""
    saldo = _dec(r.get("saldo_pcpt_m2"))
    vtcd = _dec(r.get("v_outorga_m2_q14"))
    if not saldo or saldo <= 0 or not vtcd or vtcd <= 0:
        return ("- _Preço legal ainda não calculável_ — falta saldo vendável e/ou valor de terreno "
                "(Quadro 14) para este imóvel. Ver pendências.\n", None)
    vmax = _dec(r.get("v_outorga_max_q14"))
    esquina = bool(vmax and vmax > vtcd)
    if esquina:
        vtcd = vmax   # Decreto 57.536/2016 Art. 3º IV — lote de esquina usa o MAIOR do Quadro 14 da quadra
    ref = art128.referencia_art128(str(saldo), str(vtcd), via="125", esquina=esquina)
    ja_declarado = (r.get("regime_pcpt") == "JA_DECLARADO")
    md = []
    md.append(f"- **Referência legal (independe do comprador):** **{_brl(ref['referencia_brl'])}**")
    md.append(f"  - fórmula: (PCpt × VTcd) ÷ CAmaxcd — Art. 128 §1º (o Cr do comprador cancela na conta)")
    md.append(f"- **Valor bruto (potencial × terreno):** {_brl(ref['numerador_brl'])}")
    md.append(f"- Componentes: saldo **{_m2(saldo)}** × VTcd **{_brl(vtcd)}/m²**"
              + (" *(esquina: maior valor da quadra, Dec. 57.536/2016 Art. 3º IV)*" if esquina else "")
              + " ÷ CAmaxcd **4**")
    if ja_declarado:
        md.append("- ⚠️ *Já-declarado:* o valor exato do §2º usa o VTcd **da data da Declaração + IPCA** "
                  "(a série do IPCA já está no motor; falta o VTcd histórico da Declaração). O número acima "
                  "usa o Quadro 14 vigente (2025).")
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
    o.append(f"- **Data de referência:** {r.get('data_ref') or '—'}\n")

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
            v = vmax if (vmax and vmax > vtcd) else vtcd
            esp = art128.referencia_art128(str(saldo), str(v), via="125",
                                           esquina=bool(vmax and vmax > vtcd))
            assert esp["referencia_brl"] == ref["referencia_brl"], r.get("sql_mestre")
            assert _brl(ref["referencia_brl"]).startswith("R$"), r.get("sql_mestre")
    assert com_preco > 100, f"esperava muitos dossiês com preço (veio {com_preco})"
    # 2) imóvel sem saldo → bloco de preço vira nota, não quebra
    vazio = {"sql_mestre": "X", "nome_bem": "Teste", "saldo_pcpt_m2": "", "v_outorga_m2_q14": ""}
    md0, ref0 = montar_dossie(vazio)
    assert ref0 is None and "ainda não calculável" in md0
    return com_preco


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sql")
    ap.add_argument("--pilotos", nargs="?", const=20, type=int)
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()

    if a.autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE dossiê: OK — {n} dossiês com preço legal batem o art128; citações e checklist presentes.")
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
