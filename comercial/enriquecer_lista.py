#!/usr/bin/env python3
"""
enriquecer_lista.py — monta a LISTA DE VENDEDORES ENRIQUECIDA a partir de fontes PRIMÁRIAS (1.2/1.8).

Cruza a base dos imóveis-cedentes (`casos-reais/tdc/LISTA-VENDEDORES.csv`) com:
  - iptu_flags.csv          (do parser IPTU 2020/2016) → NOME do dono + PF/PJ/PUBLICO + limpeza público×privado
  - donos_encontrados.csv   (do resolver_dono, Fase B) → controlador PF por trás do CNPJ (só PJ)
  - itbi_por_sql.csv        (das guias de ITBI) → preço real da última transação + FRESCOR (dono mudou pós-2020?)
Calcula ainda:
  - dono_carteira_qtd: quantos imóveis o MESMO dono aparece (o "peixe grande") — agrupa por doc (CNPJ) ou nome.
  - cpf_contato_status: marca o que só a FERRAMENTA EXTERNA resolve (CPF completo + telefone/e-mail) — nunca inventado.
Doutrina: nome/valor nascem da fonte primária (1.3), com proveniência por campo (`fonte_dono`); PENDENTE quando falta
(nunca chuta, 1.8). Limpeza público×privado é pelo CONTRIBUINTE (autoritativo), não por nome de logradouro.

Uso:
  python3 comercial/enriquecer_lista.py            # usa os recortes reais em zepec/oficial + casos-reais
  python3 comercial/enriquecer_lista.py --autoteste # roda sobre fixtures sintéticos (sem PII real)
"""
import csv
import re
import sys
import argparse
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE_LISTA = RAIZ / "casos-reais" / "tdc" / "LISTA-VENDEDORES.csv"
OFICIAL = RAIZ / "zepec" / "oficial"
LIMPO = RAIZ / "zepec" / "limpo"
SAIDA = RAIZ / "casos-reais" / "tdc" / "LISTA-VENDEDORES-ENRIQUECIDA.csv"
FIX = RAIZ / "evals" / "ground-truth" / "comercial-fixture"

PEND_CONTATO = "(ENRIQUECER-EXTERNO: CPF completo + telefone/e-mail — BigDataCorp/Assertiva/Serpro)"
PEND_DONO = "(PENDENTE: sem contribuinte no IPTU p/ este SQL)"

NOVAS_COLS = ["proprietario", "proprietario_doc", "tipo_dono", "publico_privado",
              "controlador_pf", "dono_carteira_qtd", "preco_real_itbi", "data_itbi",
              "frescor_dono", "vtcd_m2_iptu", "contato", "fonte_dono"]


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().upper()


def _digitos(s):
    return re.sub(r"\D", "", s or "")


def _rows(path):
    return list(csv.DictReader(open(path, encoding="utf-8"))) if Path(path).exists() else []


def _ano(iso):
    m = re.match(r"\s*(\d{4})", iso or "")
    return int(m.group(1)) if m else 0


def enriquecer(base, flags, donos, itbi):
    """Puro e testável. base=linhas da lista; flags/donos/itbi=dicts por sql. Devolve linhas enriquecidas."""
    fl = {f["sql_mestre"]: f for f in flags}
    dn = {d["sql_mestre"]: d for d in donos}
    it = {i["sql_mestre"]: i for i in itbi}

    # 1ª passada: resolve o dono de cada SQL e a chave de agrupamento (doc CNPJ senão nome normalizado)
    resolvido = {}
    chave_por_sql = {}
    for r in base:
        sql = (r.get("sql") or "").strip()
        f = fl.get(sql)
        if not f:
            resolvido[sql] = None
            continue
        nome1 = (f.get("nome1") or "").strip()
        nome2 = (f.get("nome2") or "").strip()
        nome = nome1 + (f" ; {nome2}" if nome2 else "")
        doc1 = _digitos(f.get("doc1"))
        resolvido[sql] = {"nome": nome, "doc": f.get("doc1", ""), "tipo": f.get("tipo_dono", ""),
                          "publico": f.get("publico", "nao"), "fonte": f.get("fonte", ""),
                          "vterr": (f.get("valor_m2_terreno") or "").strip()}
        chave_por_sql[sql] = (doc1 if len(doc1) == 14 else _norm(nome1)) or sql

    # carteira: quantos SQLs por chave de dono
    from collections import Counter
    cont = Counter(k for k in chave_por_sql.values())

    saida = []
    for r in base:
        sql = (r.get("sql") or "").strip()
        novo = dict(r)  # preserva todas as colunas originais (metragem, preço legal, agenda, etc.)
        res = resolvido.get(sql)
        if not res:
            novo.update({"proprietario": PEND_DONO, "proprietario_doc": "", "tipo_dono": "",
                         "publico_privado": "", "controlador_pf": "", "dono_carteira_qtd": "",
                         "preco_real_itbi": "", "data_itbi": "", "frescor_dono": "",
                         "vtcd_m2_iptu": "", "contato": PEND_CONTATO, "fonte_dono": ""})
        else:
            d = dn.get(sql)
            controlador = ""
            if res["tipo"] == "PJ" and d:
                # o resolver devolve "razão — controlador(es): X, Y"
                m = re.search(r"controlador\(es\):\s*(.+)$", d.get("proprietario", ""))
                controlador = m.group(1).strip() if m else ""
            i = it.get(sql)
            preco = (i or {}).get("valor_transacao", "")
            data_itbi = (i or {}).get("data_transacao", "")
            frescor = "dono possivelmente mudou (ITBI pós-2020)" if _ano(data_itbi) >= 2021 else ""
            publico = res["publico"] == "sim"
            novo.update({
                "proprietario": res["nome"] if not publico else f"[PÚBLICO] {res['nome']}",
                "proprietario_doc": res["doc"],
                "tipo_dono": res["tipo"],
                "publico_privado": "PUBLICO" if publico else "PRIVADO",
                "controlador_pf": controlador,
                "dono_carteira_qtd": cont.get(chave_por_sql.get(sql), 1),
                "preco_real_itbi": preco,
                "data_itbi": data_itbi,
                "frescor_dono": frescor,
                "vtcd_m2_iptu": res.get("vterr", ""),
                "contato": PEND_CONTATO,
                "fonte_dono": res["fonte"] + (" + Fase B socios/holdings" if controlador else ""),
            })
        saida.append(novo)
    return saida


def _carregar_reais():
    base = _rows(BASE_LISTA)
    flags = _rows(OFICIAL / "iptu_flags.csv")
    donos = _rows(LIMPO / "donos_encontrados.csv")
    # aceita 'sql_mestre' do resolver
    for d in donos:
        d.setdefault("sql_mestre", d.get("sql_mestre", ""))
    itbi = _rows(OFICIAL / "itbi_por_sql.csv")
    return base, flags, donos, itbi


def _autoteste():
    base = _rows(FIX / "lista_vendedores_amostra.csv")
    flags = _rows(FIX / "iptu_flags_amostra.csv")
    donos = _rows(FIX / "donos_amostra.csv")
    itbi = _rows(FIX / "itbi_amostra.csv")
    out = {o["sql"]: o for o in enriquecer(base, flags, donos, itbi)}
    # PF: nome direto do IPTU
    assert "MARCIO" in out["0200670033"]["proprietario"].upper()
    assert out["0200670033"]["publico_privado"] == "PRIVADO"
    # PJ: controlador PF do resolver aparece
    assert out["0100010001"]["tipo_dono"] == "PJ"
    assert "FULANO" in out["0100010001"]["controlador_pf"].upper()
    # Público: marcado e separado
    assert out["0000010001"]["publico_privado"] == "PUBLICO"
    # ITBI: preço + frescor pós-2020
    assert out["0200670033"]["preco_real_itbi"] == "4804259.04"
    assert "mudou" in out["0200670033"]["frescor_dono"]
    # carteira: o mesmo CNPJ em 2 imóveis conta 2
    assert str(out["0100010001"]["dono_carteira_qtd"]) == "2", out["0100010001"]["dono_carteira_qtd"]
    # contato SEMPRE externo, nunca inventado
    assert all(o["contato"].startswith("(ENRIQUECER-EXTERNO") for o in out.values())
    # SQL sem contribuinte no IPTU: dono PENDENTE, não inventado
    assert out["0999999999"]["proprietario"] == PEND_DONO
    return len(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autoteste", action="store_true")
    if ap.parse_args().autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE enriquecer_lista: OK — {n} imóveis; nome(PF)/controlador(PJ)/público/ITBI/carteira/"
              f"contato-externo/PENDENTE conferidos (nada inventado).")
        return 0
    base, flags, donos, itbi = _carregar_reais()
    if not base:
        print("ERRO: base LISTA-VENDEDORES.csv ausente.", file=sys.stderr); return 2
    out = enriquecer(base, flags, donos, itbi)
    cols = list(base[0].keys())
    for c in NOVAS_COLS:
        if c not in cols:
            cols.append(c)
    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(out)
    com_nome = sum(1 for o in out if o["proprietario"] and not o["proprietario"].startswith("(PENDENTE"))
    print(f"OK: {len(out)} imóveis → {SAIDA.name} | com nome de dono: {com_nome} | "
          f"contato marcado p/ ferramenta externa em todos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
