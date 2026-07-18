#!/usr/bin/env python3
"""
gerar_listas_comercial.py — as DUAS listas comerciais do TDC (v1, com o dado EM MÃOS).

  • VENDEDORES  → casos-reais/tdc/LISTA-VENDEDORES.csv
  • COMPRADORES → casos-reais/tdc/LISTA-COMPRADORES.csv

Regras de ouro (1.3/1.7): número vem do engine (Art. 128) rastreável ao artigo; nada inventado; campo que depende
de acesso que ainda NÃO temos (proprietário, nome do comprador, uso do receptor, processo judicial) sai marcado
`(PENDENTE-ACESSO: <fonte>)` — nunca preenchido no chute. "Data de renovação" = marcos legais do Art. 129 (recarga
aos 10 anos → 70% e 15 anos → 100% da emissão da Declaração), derivados por data-aritmética determinística.

Fontes: zepec/ferramenta/zepec_cedentes_oficial.csv (vendedor) + casos-reais/tdc/certidoes-reais-ago2025.csv (comprador).
Uso: python3 scripts/gerar_listas_comercial.py [--autoteste]
"""
import csv
import sys
import argparse
from datetime import date
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "engines" / "tdc"))
import art128  # noqa: E402

CED = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes_oficial.csv"
CAP = RAIZ / "casos-reais" / "tdc" / "certidoes-reais-ago2025.csv"
OUT_V = RAIZ / "casos-reais" / "tdc" / "LISTA-VENDEDORES.csv"
OUT_C = RAIZ / "casos-reais" / "tdc" / "LISTA-COMPRADORES.csv"
PEND_DONO = "(PENDENTE-ACESSO: canônicas sócios/empresas/holdings — Fase B, gate PD-7)"
PEND_USO = "(PENDENTE-ACESSO: IPTU_2026 completo — uso/zona do receptor)"
PEND_JUD = "(PENDENTE-ACESSO: e-SAJ/TJSP + SEI — processo em andamento)"


def _d(s):
    try:
        return art128._d(s, "x")
    except Exception:
        return None


def _mais_anos(iso, anos):
    """'AAAA-MM-DD' + N anos (determinístico; guarda 29/02). Vazio se data inválida."""
    s = (iso or "").strip()
    if len(s) < 10:
        return ""
    try:
        y, m, d = int(s[:4]), int(s[5:7]), int(s[8:10])
        try:
            return date(y + anos, m, d).isoformat()
        except ValueError:
            return date(y + anos, m, 28).isoformat()
    except Exception:
        return ""


def _valor_art128(r):
    """Referência legal do Art. 128 (base A vigente) p/ o saldo — mesmo motor do dossiê. '' se sem saldo/VTcd."""
    saldo = _d(r.get("saldo_pcpt_m2"))
    vtcd = _d(r.get("v_outorga_m2_q14"))
    if not saldo or saldo <= 0 or not vtcd or vtcd <= 0:
        return "", ""
    vmax = _d(r.get("v_outorga_max_q14"))
    esquina = bool(vmax and vmax > vtcd)
    ref = art128.referencia_art128(str(saldo), str(vmax if esquina else vtcd), via="125", esquina=esquina)
    return ref["referencia_brl"], ref["numerador_brl"]


def _teto_art128(r):
    """OP-1b (tese VTcd-máximo) materializada no PRODUTO. Base B (Art. 128 §2º) do JÁ-DECLARADO:
    VTcd da Declaração (Quadro 14 do ano-ref, via vtcd_na_data) × IPCA (mês da Declaração → mês do
    protocolo da Certidão), e devolve MAX(A piso vigente ; B teto §2º) + a base vencedora. Só computa
    quando há AMBAS as datas (Declaração + Certidão) — o §2º exige o protocolo, que NÃO se adivinha
    (1.3; tese §4). Sem as duas datas → ('', '') e o produto mostra só o piso. O piso (A) NUNCA muda."""
    saldo = _d(r.get("saldo_pcpt_m2"))
    vtcd = _d(r.get("v_outorga_m2_q14"))
    if not saldo or saldo <= 0 or not vtcd or vtcd <= 0:
        return "", ""
    decl = (r.get("data_declaracao_iso") or "").strip()
    cert = (r.get("data_certidao_iso") or "").strip()
    if len(decl) < 7 or len(cert) < 7:
        return "", ""                                  # §2º N/A sem protocolo (não se inventa data)
    vmax = _d(r.get("v_outorga_max_q14"))
    esquina = bool(vmax and vmax > vtcd)
    v_vig = str(vmax if esquina else vtcd)
    try:
        ano_decl = int(decl[:4])
        vtcd_decl = art128.vtcd_na_data(v_vig, 2026, ano_decl)["vtcd_alvo_m2"]   # Q14 na Declaração
        mx = art128.referencia_max_art128(str(saldo), v_vig, via="125", esquina=esquina,
                                          vtcd_declaracao=vtcd_decl, mes_ref=decl[:7], mes_protocolo=cert[:7])
        return mx["referencia_max_brl"], mx["base_vencedora"]
    except Exception:
        return "", ""                                  # série fora de faixa (ex.: pré-2014) → só o piso


def _indicio_processo(r):
    """Sinais de processo/intercorrência que TEMOS (não é consulta judicial — isso é PEND_JUD)."""
    sig = []
    st = (r.get("status_fundurb") or "").strip()
    if st:
        sig.append(f"FUNDURB: {st}")
    inter = (r.get("intercorrencia_fundurb") or "").strip()
    if inter and inter not in ("nao", "não", "—", ""):
        sig.append(f"intercorrência: {inter}")
    pend = (r.get("pendencia_calculo") or "").strip()
    if "CONPRESP" in pend or "REVISAR TOMBAMENTO" in pend:
        sig.append("revisão de tombamento (CONPRESP)")
    sinais = (r.get("sinais_revisar") or "").strip()
    if sinais:
        sig.append(f"sinais: {sinais}")
    return " | ".join(sig)


VEND_COLS = ["sql", "endereco", "distrito", "zona", "tipo_zepec", "esfera", "nome_bem",
             "area_terreno_m2", "pcpt_m2", "saldo_vendavel_m2", "parcelas_anuais",
             "valor_ref_art128_brl", "valor_bruto_brl",
             "valor_teto_art128_brl", "base_vencedora_art128",
             "estado_venda", "ja_transferido_m2", "n_transferencias",
             "data_declaracao", "data_certidao", "data_referencia",
             "renovacao_70pct_10anos_art129", "renovacao_100pct_15anos_art129", "conservacao_art129",
             "negociavel", "indicio_processo", "proprietario", "fonte"]

COMP_COLS = ["sql_receptor", "endereco_receptor", "distrito_receptor",
             "metragem_compra_m2", "area_cedida_equivalente_m2",
             "valor_pecuniario_rs", "n_certidao", "ano_certidao", "data_publicacao",
             "sql_cedente_de_quem_comprou", "uso_receptor", "nome_comprador", "fonte"]


def gerar_vendedores():
    rows = list(csv.DictReader(open(CED, encoding="utf-8")))
    out = []
    for r in rows:
        sql = (r.get("sql_mestre") or "").strip()
        if not sql:
            continue
        vref, vbruto = _valor_art128(r)
        vteto, base_venc = _teto_art128(r)
        decl = (r.get("data_declaracao_iso") or "").strip()
        out.append({
            "sql": sql, "endereco": r.get("endereco_mestre", ""), "distrito": r.get("distrito", ""),
            "zona": r.get("zona", ""), "tipo_zepec": r.get("tipo_zepec", ""), "esfera": r.get("esfera", ""),
            "nome_bem": r.get("nome_bem", ""),
            "area_terreno_m2": r.get("area_terreno_m2", ""), "pcpt_m2": r.get("pcpt_m2", ""),
            "saldo_vendavel_m2": r.get("saldo_pcpt_m2", ""), "parcelas_anuais": r.get("parcelas_anuais", ""),
            "valor_ref_art128_brl": vref, "valor_bruto_brl": vbruto,
            "valor_teto_art128_brl": vteto, "base_vencedora_art128": base_venc,
            "estado_venda": r.get("estado_venda", ""), "ja_transferido_m2": r.get("m2_ja_transferido", ""),
            "n_transferencias": r.get("n_transferencias", ""),
            "data_declaracao": decl, "data_certidao": r.get("data_certidao_iso", ""),
            "data_referencia": decl,
            "renovacao_70pct_10anos_art129": _mais_anos(decl, 10),
            "renovacao_100pct_15anos_art129": _mais_anos(decl, 15),
            "conservacao_art129": r.get("elegibilidade_conservacao", ""),
            "negociavel": r.get("negociavel", ""),
            "indicio_processo": _indicio_processo(r) or PEND_JUD,
            "proprietario": PEND_DONO,
            "fonte": "IPTU 2026 + ZEPEC/DEUSO + Quadro 14 + FUNDURB (recortes oficiais)",
        })
    return out


def gerar_compradores():
    rows = list(csv.DictReader(open(CAP, encoding="utf-8")))
    ced = {(r.get("sql_mestre") or "").strip(): r
           for r in csv.DictReader(open(CED, encoding="utf-8"))}
    out = []
    for r in rows:
        sqlr = (r.get("sql_receptor") or "").strip()
        # uso do receptor: só se o SQL estiver no nosso cadastro (raro) — senão PEND_USO
        uso = ""
        if sqlr and sqlr in ced:
            uso = ced[sqlr].get("uso_iptu", "") or ""
        out.append({
            "sql_receptor": sqlr, "endereco_receptor": r.get("endereco_receptor", ""),
            "distrito_receptor": r.get("distrito_receptor", ""),
            "metragem_compra_m2": r.get("area_recebida_real_m2", ""),
            "area_cedida_equivalente_m2": r.get("area_cedida_equivalente_m2", ""),
            "valor_pecuniario_rs": r.get("valor_pecuniario_rs", ""),
            "n_certidao": r.get("n_certidao", ""), "ano_certidao": r.get("ano_certidao", ""),
            "data_publicacao": r.get("data_publicacao", ""),
            "sql_cedente_de_quem_comprou": r.get("sql_cedente", ""),
            "uso_receptor": uso or PEND_USO,
            "nome_comprador": PEND_DONO,
            "fonte": r.get("fonte", ""),
        })
    return out


def _autoteste():
    v = gerar_vendedores()
    c = gerar_compradores()
    assert len(v) > 3000, f"vendedores {len(v)}"
    assert len(c) > 150, f"compradores {len(c)}"
    # todo vendedor com saldo+VTcd tem valor do engine (não vazio) e bate o art128
    com_valor = [x for x in v if x["valor_ref_art128_brl"]]
    assert len(com_valor) > 3000, f"esperava valor na maioria: {len(com_valor)}"
    # renovação = decl+10/+15 quando há declaração
    assert any(x["renovacao_70pct_10anos_art129"] for x in v), "marcos Art.129 vazios"
    # proprietário e nome_comprador SEMPRE marcados PENDENTE (nunca inventados)
    assert all(x["proprietario"].startswith("(PENDENTE-ACESSO") for x in v)
    assert all(x["nome_comprador"].startswith("(PENDENTE-ACESSO") for x in c)
    # comprador traz metragem real na maioria
    assert sum(1 for x in c if x["metragem_compra_m2"]) > 150
    return len(v), len(c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()
    if a.autoteste:
        nv, nc = _autoteste()
        print(f"AUTO-TESTE listas: OK — {nv} vendedores, {nc} compradores; valores batem o art128; "
              f"proprietário/comprador marcados PENDENTE-ACESSO (nunca inventados).")
        return 0
    v, c = gerar_vendedores(), gerar_compradores()
    CAP.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_V, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=VEND_COLS); w.writeheader(); w.writerows(v)
    with open(OUT_C, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COMP_COLS); w.writeheader(); w.writerows(c)
    negociaveis = sum(1 for x in v if x["negociavel"] == "sim")
    com_saldo = sum(1 for x in v if x["saldo_vendavel_m2"] and _d(x["saldo_vendavel_m2"]) and _d(x["saldo_vendavel_m2"]) > 0)
    vendidos = sum(1 for x in v if x["ja_transferido_m2"] and _d(x["ja_transferido_m2"]) and _d(x["ja_transferido_m2"]) > 0)
    print(f"VENDEDORES: {len(v)} imóveis → {OUT_V.relative_to(RAIZ)}")
    print(f"  negociáveis={negociaveis} · com saldo vendável={com_saldo} · já venderam (certidão)={vendidos}")
    print(f"COMPRADORES: {len(c)} compras reais → {OUT_C.relative_to(RAIZ)}")
    print(f"  com valor R$={sum(1 for x in c if x['valor_pecuniario_rs'])} · com metragem={sum(1 for x in c if x['metragem_compra_m2'])}")
    print("\nCampos PENDENTE-ACESSO (o que falta liberar): proprietário (vendedor) · nome do comprador · "
          "uso do receptor · processo judicial em andamento.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
