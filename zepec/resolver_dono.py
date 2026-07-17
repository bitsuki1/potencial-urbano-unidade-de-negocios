#!/usr/bin/env python3
"""
resolver_dono.py — FASE B: resolve o PROPRIETÁRIO (pessoa física controladora) em escala.

Sobe a cadeia de titularidade a partir do imóvel, cruzando as 4 canônicas do Drive:
    SQL (IPTU) → contribuinte/documento → empresas (CNPJ→razão) → sócios (CNPJ→sócio-QSA)
              → holdings (elos CNPJ→CNPJ, recursão) → PESSOA FÍSICA controladora.
As 4 canônicas: iptu_contribuinte.csv · empresas.csv · socios.csv · holdings.csv. A `holdings.csv`
é OPCIONAL e explícita (recorte curado do Drive: `cnpj_controlada,cnpj_controladora[,nome_controladora]`);
seus elos são dobrados no grafo de sócios, então a mesma recursão anti-loop os percorre. Sem ela,
o controle por holding ainda é pego quando a própria holding aparece como SÓCIO PJ (via socios.csv).

Grava `zepec/limpo/donos_encontrados.csv` no MESMO schema de 5 colunas que `donos.py` usa
(`sql_mestre, proprietario, area_terreno, endereco_fonte, fonte_dono`) — `montar_ferramenta.py`
consome SEM mudança. É a Fase B (adquiridas ENRIQUECEM por cima da Fase A oficial — D-DONO-6):
na escrita real, faz MERGE preenchendo LACUNAS (a Fase A do `donos.py` tem precedência; a proveniência
de cada linha fica no `fonte_dono`), NUNCA sobrescreve o que a Fase A já resolveu.

PII & segurança (LGPD/D-DONO-17b/D106): a SAÍDA carrega nome/CPF/CNPJ → fica FORA do git
(.gitignore) e depende do gate de segurança PD-7 (bucket privado + RLS deny-all) ANTES da carga.
Este script é DETERMINÍSTICO e não inventa (1.3): sem documento na base → sem dono (PENDENTE).

Uso:
    python3 zepec/resolver_dono.py            # roda sobre os recortes reais (quando existirem)
    python3 zepec/resolver_dono.py --autoteste  # gate: roda sobre o fixture SINTÉTICO (sem PII real)
PU 18 · 2026-07-10 (Fase B — pronto para rodar quando o dado pesado chegar).
"""
import csv
import re
import sys
import argparse
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
OFICIAL = RAIZ / "zepec" / "oficial"
SAIDA = RAIZ / "zepec" / "limpo" / "donos_encontrados.csv"
FIXTURE = RAIZ / "evals" / "ground-truth" / "fase-b-fixture"
SCHEMA = ["sql_mestre", "proprietario", "area_terreno", "endereco_fonte", "fonte_dono"]
MAXDEPTH = 6   # trava anti-loop na recursão de holdings


def _digitos(s):
    return re.sub(r"\D", "", s or "")


def _tipo_doc(doc):
    d = _digitos(doc)
    return "CPF" if len(d) == 11 else ("CNPJ" if len(d) == 14 else "INVALIDO")


def controladores_pf(doc, nome, socios_por_cnpj, seen=None, depth=0):
    """Devolve o conjunto de PESSOAS FÍSICAS controladoras a partir de um documento.
    CNPJ (14 díg.) → sobe pelos sócios (recursivo, holdings) até achar as PF. Anti-loop.
    QUALQUER outro documento num SÓCIO = pessoa física: o CPF do sócio na base da Receita vem
    MASCARADO (`***NNNNNN**`, <11 díg.), então NÃO se pode exigir 11 dígitos — usa-se o NOME completo
    do sócio (a fonte primária traz o nome inteiro). Sem isso, todo controlador-PF se perdia (bug 2026-07-17)."""
    seen = seen if seen is not None else set()
    cnpj = _digitos(doc)
    if len(cnpj) == 14:  # é CNPJ → sobe a cadeia societária
        if depth > MAXDEPTH or cnpj in seen:
            return set()
        seen.add(cnpj)
        out = set()
        for s in socios_por_cnpj.get(cnpj, []):
            out |= controladores_pf(s.get("doc_socio"), s.get("nome_socio"), socios_por_cnpj, seen, depth + 1)
        return out
    # não é CNPJ: no topo (seed) sem nome não há o que resolver; num sócio, é a PF (pelo nome)
    if depth == 0:
        return {(nome or "").strip()} if (nome or "").strip() else set()
    nm = (nome or "").strip()
    if nm:
        return {nm}
    return {f"CPF {cnpj}"} if cnpj else set()


def resolver(contrib_rows, empresas, socios_por_cnpj):
    """Núcleo puro: recebe as linhas de contribuinte + dicts de empresas/sócios, devolve as linhas de dono.
    - documento CPF  → PF direta (o próprio contribuinte);
    - documento CNPJ → razão social + PF(s) controladora(s) pela cadeia;
    - sem documento  → NÃO entra (dono PENDENTE, não se inventa)."""
    linhas = []
    for r in contrib_rows:
        sql = (r.get("sql_mestre") or "").strip()
        doc = (r.get("documento") or "").strip()
        contribuinte = (r.get("contribuinte") or "").strip()
        t = _tipo_doc(doc)
        if not sql or t == "INVALIDO":
            continue  # sem SQL ou sem documento → PENDENTE (não se inventa dono)
        if t == "CPF":
            prop = contribuinte or f"CPF {_digitos(doc)}"
            fonte = "FaseB:IPTU-contribuinte(PF)"
        else:  # CNPJ
            razao = (empresas.get(_digitos(doc), {}).get("razao_social") or contribuinte or f"CNPJ {_digitos(doc)}").strip()
            pfs = sorted(controladores_pf(doc, None, socios_por_cnpj))
            if pfs:
                prop = f"{razao} — controlador(es): {', '.join(pfs)}"
                fonte = "FaseB:socios/holdings"
            else:
                prop = razao
                fonte = "FaseB:empresa(sem socio PF resolvido)"
        linhas.append({"sql_mestre": sql, "proprietario": prop, "area_terreno": "",
                       "endereco_fonte": "FaseB", "fonte_dono": fonte})
    return linhas


def _carregar(base):
    """Lê as 4 canônicas de `base/` (ou fixture). Ausência de arquivo = dict/lista vazia (fail-soft na carga,
    fail-closed no resultado: sem dado → sem dono). A holdings.csv é opcional; seus elos CNPJ→CNPJ são
    DOBRADOS no grafo de sócios (como um sócio-PJ sintético), então a recursão de `controladores_pf` os
    percorre sem código novo. Mantém o contrato de 3-tupla que o eval consome."""
    def rows(nome):
        p = base / nome
        return list(csv.DictReader(open(p, encoding="utf-8"))) if p.exists() else []
    contrib = rows("iptu_contribuinte.csv")
    empresas = {_digitos(e["cnpj"]): e for e in rows("empresas.csv") if e.get("cnpj")}
    socios_por_cnpj = {}
    for s in rows("socios.csv"):
        socios_por_cnpj.setdefault(_digitos(s.get("cnpj")), []).append(s)
    # 4ª canônica (opcional): elos explícitos de holding. Cada elo vira um "sócio" PJ da controlada,
    # apontando para o CNPJ da controladora → a mesma recursão anti-loop sobe até a PF no topo.
    for h in rows("holdings.csv"):
        controlada = _digitos(h.get("cnpj_controlada"))
        controladora = _digitos(h.get("cnpj_controladora"))
        if not controlada or not controladora:
            continue
        socios_por_cnpj.setdefault(controlada, []).append(
            {"cnpj": controlada, "doc_socio": controladora,
             "nome_socio": (h.get("nome_controladora") or "").strip()})
    return contrib, empresas, socios_por_cnpj


def _autoteste():
    """Roda sobre o fixture SINTÉTICO (CPF/CNPJ/nomes FALSOS) — prova a cadeia sem tocar PII real."""
    sys.path.insert(0, str(RAIZ / "evals"))
    import importlib
    ev = importlib.import_module("eval-fase-b") if (RAIZ / "evals" / "eval-fase-b.py").exists() else None
    if ev is None:
        # autoteste embutido (caso o eval não exista): valida a cadeia sobre o fixture
        contrib, empresas, socios = _carregar(FIXTURE)
        assert contrib, "fixture ausente — evals/ground-truth/fase-b-fixture/"
        linhas = {l["sql_mestre"]: l for l in resolver(contrib, empresas, socios)}
        assert "SQLPF0001" in linhas and "FULANO" in linhas["SQLPF0001"]["proprietario"].upper()
        return len(linhas)
    return ev.main_asserts()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autoteste", action="store_true")
    ap.add_argument("--base", default=str(OFICIAL), help="pasta com iptu_contribuinte/empresas/socios.csv")
    a = ap.parse_args()
    if a.autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE Fase B: OK — cadeia de titularidade resolvida sobre fixture sintético ({n} casos, sem PII).")
        return 0
    base = Path(a.base)
    contrib, empresas, socios = _carregar(base)
    if not contrib:
        print(f"[AGUARDANDO] {base}/iptu_contribuinte.csv ausente — Fase B sem insumo (dado pesado ainda não "
              f"recortado). Pipeline pronto; rode quando o dado chegar. Ver docs/FASE-B-DONOS-EM-ESCALA.md.")
        return 0
    linhas = resolver(contrib, empresas, socios)
    # MERGE (D-DONO-6): a Fase A (donos.py — alvarás/OODC) tem precedência; a Fase B preenche LACUNAS.
    # NUNCA sobrescreve o que a Fase A já resolveu. A proveniência de cada linha fica no `fonte_dono`.
    existentes = {}
    if SAIDA.exists():
        existentes = {r["sql_mestre"]: r for r in csv.DictReader(open(SAIDA, encoding="utf-8"))}
    fase_a = len(existentes)
    novos = 0
    for l in linhas:
        if l["sql_mestre"] not in existentes:   # só preenche lacuna (Fase A primeiro)
            existentes[l["sql_mestre"]] = l
            novos += 1
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA); w.writeheader(); w.writerows(existentes.values())
    print(f"donos_encontrados.csv: {len(linhas)} donos resolvidos pela Fase B de {len(contrib)} contribuintes; "
          f"merge preencheu {novos} lacunas sobre {fase_a} da Fase A → {len(existentes)} no total. "
          f"PII — fora do git (.gitignore).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
