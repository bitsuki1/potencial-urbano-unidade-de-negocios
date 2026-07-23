#!/usr/bin/env python3
"""
enriquecer_compradores.py — monta a LISTA DE COMPRADORES ENRIQUECIDA (o lado da DEMANDA do TDC) a partir
de fontes PRIMÁRIAS (1.2/1.8). Espelha `enriquecer_lista.py` (vendedores), mas chaveado pelo `sql_receptor`.

Quem são os compradores: os RECEPTORES que JÁ compraram potencial construtivo (certidões de TDC emitidas
pelo DEUSO/SMUL — demanda COMPROVADA, não hipótese). O `nome_comprador` estava PENDENTE porque falta casar o
`sql_receptor` no cadastro IPTU — a MESMA máquina dos vendedores resolve (IPTU→nome, Receita→controlador PF).

Cruza `casos-reais/tdc/LISTA-COMPRADORES.csv` com:
  - iptu_flags.csv        (do parser IPTU) → NOME do comprador + PF/PJ/PUBLICO, pelo sql_receptor
  - donos_encontrados.csv (resolver_dono, Fase B) → controlador PF por trás do CNPJ comprador
Calcula ainda (o valor comercial da lista de demanda):
  - compras_qtd:  quantas certidões o MESMO comprador tem (comprador recorrente = incorporadora que
                  PRECISA de potencial toda hora = lead QUENTE). Agrupa por doc (CNPJ) ou nome.
  - total_m2_comprado: soma de m² que aquele comprador já adquiriu (tamanho do apetite).
Doutrina: nome nasce da fonte primária (1.3), proveniência por campo; PENDENTE quando falta (nunca chuta, 1.8).
Contato (telefone/e-mail) = ferramenta externa (Assertiva) — marcado, nunca inventado.

Uso:
  python3 comercial/enriquecer_compradores.py            # usa recortes reais em zepec/oficial + casos-reais
  python3 comercial/enriquecer_compradores.py --autoteste # fixture sintético (sem PII real)
"""
import csv
import re
import sys
import argparse
import unicodedata
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE_LISTA = RAIZ / "casos-reais" / "tdc" / "LISTA-COMPRADORES.csv"
OFICIAL = RAIZ / "zepec" / "oficial"
LIMPO = RAIZ / "zepec" / "limpo"
SAIDA = RAIZ / "casos-reais" / "tdc" / "LISTA-COMPRADORES-ENRIQUECIDA.csv"
FIX = RAIZ / "evals" / "ground-truth" / "comercial-fixture"

PEND_CONTATO = "(ENRIQUECER-EXTERNO: CPF completo + telefone/e-mail — BigDataCorp/Assertiva/Serpro)"
PEND_DONO = "(PENDENTE: sem contribuinte no IPTU p/ este sql_receptor)"

NOVAS_COLS = ["comprador", "comprador_doc", "tipo_comprador", "publico_privado", "controlador_pf",
              "compras_qtd", "total_m2_comprado", "contato", "fonte_dono"]


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().upper()


def _digitos(s):
    return re.sub(r"\D", "", s or "")


def _rows(path):
    return list(csv.DictReader(open(path, encoding="utf-8"))) if Path(path).exists() else []


def _num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".") if "," in (s or "") else (s or "").strip()
    try:
        return Decimal(s) if s else Decimal(0)
    except (InvalidOperation, ValueError):
        return Decimal(0)


def enriquecer(base, flags, donos):
    """Puro e testável. base=linhas de LISTA-COMPRADORES; flags/donos=dicts por sql. Devolve linhas enriquecidas."""
    fl = {f["sql_mestre"]: f for f in flags}
    dn = {d["sql_mestre"]: d for d in donos}

    # 1ª passada: resolve o comprador de cada sql_receptor + a chave de agrupamento (doc CNPJ senão nome)
    resolvido, chave_por_sql = {}, {}
    for r in base:
        sql = (r.get("sql_receptor") or "").strip()
        f = fl.get(sql)
        if not f:
            resolvido[sql] = None
            continue
        nome1 = (f.get("nome1") or "").strip()
        nome2 = (f.get("nome2") or "").strip()
        nome = nome1 + (f" ; {nome2}" if nome2 else "")
        doc1 = _digitos(f.get("doc1"))
        resolvido[sql] = {"nome": nome, "doc": f.get("doc1", ""), "tipo": f.get("tipo_dono", ""),
                          "publico": f.get("publico", "nao"), "fonte": f.get("fonte", "")}
        chave_por_sql[sql] = (doc1 if len(doc1) == 14 else _norm(nome1)) or sql

    # carteira de COMPRAS por comprador: nº de certidões + m² total (linha = uma compra)
    compras = Counter()
    m2_por_chave = defaultdict(Decimal)
    for r in base:
        sql = (r.get("sql_receptor") or "").strip()
        k = chave_por_sql.get(sql)
        if k:
            compras[k] += 1
            m2_por_chave[k] += _num(r.get("metragem_compra_m2"))

    saida = []
    for r in base:
        sql = (r.get("sql_receptor") or "").strip()
        novo = dict(r)  # preserva todas as colunas originais
        res = resolvido.get(sql)
        if not res:
            novo.update({"comprador": PEND_DONO, "comprador_doc": "", "tipo_comprador": "",
                         "publico_privado": "", "controlador_pf": "", "compras_qtd": "",
                         "total_m2_comprado": "", "contato": PEND_CONTATO, "fonte_dono": ""})
        else:
            d = dn.get(sql)
            controlador = ""
            if res["tipo"] == "PJ" and d:
                m = re.search(r"controlador\(es\):\s*(.+)$", d.get("proprietario", ""))
                controlador = m.group(1).strip() if m else ""
            publico = res["publico"] == "sim"
            k = chave_por_sql.get(sql)
            m2 = m2_por_chave.get(k, Decimal(0))
            novo.update({
                "comprador": res["nome"] if not publico else f"[PÚBLICO] {res['nome']}",
                "comprador_doc": res["doc"],
                "tipo_comprador": res["tipo"],
                "publico_privado": "PUBLICO" if publico else "PRIVADO",
                "controlador_pf": controlador,
                "compras_qtd": compras.get(k, 1),
                "total_m2_comprado": (str(m2.quantize(Decimal("0.01"))) if m2 else ""),
                "contato": PEND_CONTATO,
                "fonte_dono": res["fonte"] + (" + Fase B socios/holdings" if controlador else ""),
            })
        saida.append(novo)
    return saida


def _carregar_reais():
    base = _rows(BASE_LISTA)
    flags = _rows(OFICIAL / "iptu_flags.csv")
    donos = _rows(LIMPO / "donos_encontrados.csv")
    for d in donos:
        d.setdefault("sql_mestre", d.get("sql_mestre", ""))
    return base, flags, donos


def _autoteste():
    # fixture sintético (sem PII real): 3 compras, 1 comprador-PJ recorrente (2×) + 1 PF; 1 sem contribuinte.
    base = [
        {"sql_receptor": "0100010001", "metragem_compra_m2": "1000"},
        {"sql_receptor": "0100010001", "metragem_compra_m2": "500"},   # mesma torre, 2ª compra
        {"sql_receptor": "0200670033", "metragem_compra_m2": "300"},
        {"sql_receptor": "0999999999", "metragem_compra_m2": "10"},    # sem contribuinte no IPTU
    ]
    flags = [
        {"sql_mestre": "0100010001", "tipo_dono": "PJ", "publico": "nao", "nome1": "INCORPORADORA X SA",
         "doc1": "11222333000181", "nome2": "", "fonte": "IPTU cadastral"},
        {"sql_mestre": "0200670033", "tipo_dono": "PF", "publico": "nao", "nome1": "MARCIO COMPRADOR",
         "doc1": "12345678909", "nome2": "", "fonte": "IPTU cadastral"},
    ]
    donos = [{"sql_mestre": "0100010001", "proprietario": "INCORPORADORA X SA — controlador(es): FULANO"}]
    out = {i: o for i, o in enumerate(enriquecer(base, flags, donos))}
    # comprador-PJ recorrente: 2 compras, 1.500 m², controlador PF resolvido
    assert out[0]["tipo_comprador"] == "PJ" and "INCORPORADORA" in out[0]["comprador"], out[0]
    assert str(out[0]["compras_qtd"]) == "2", out[0]["compras_qtd"]
    assert out[0]["total_m2_comprado"] == "1500.00", out[0]["total_m2_comprado"]
    assert "FULANO" in out[0]["controlador_pf"].upper(), out[0]
    # comprador PF
    assert out[2]["tipo_comprador"] == "PF" and "MARCIO" in out[2]["comprador"].upper()
    assert str(out[2]["compras_qtd"]) == "1"
    # sem contribuinte → PENDENTE, nunca inventado; contato sempre externo
    assert out[3]["comprador"] == PEND_DONO
    assert all(o["contato"].startswith("(ENRIQUECER-EXTERNO") for o in out.values())
    return len(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autoteste", action="store_true")
    if ap.parse_args().autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE enriquecer_compradores: OK — {n} compras; comprador(PF/PJ)/controlador/recorrência/"
              f"m²-total/contato-externo/PENDENTE conferidos (nada inventado).")
        return 0
    base, flags, donos = _carregar_reais()
    if not base:
        print("ERRO: base LISTA-COMPRADORES.csv ausente.", file=sys.stderr); return 2
    out = enriquecer(base, flags, donos)
    cols = list(base[0].keys())
    for c in NOVAS_COLS:
        if c not in cols:
            cols.append(c)
    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(out)
    com_nome = sum(1 for o in out if o.get("comprador") and not o["comprador"].startswith("(PENDENTE"))
    recorrentes = sum(1 for o in out if str(o.get("compras_qtd") or "1") not in ("", "1"))
    print(f"OK: {len(out)} compras → {SAIDA.name} | com nome de comprador: {com_nome} | "
          f"linhas de comprador recorrente: {recorrentes} | contato p/ ferramenta externa em todos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
