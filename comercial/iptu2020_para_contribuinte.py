#!/usr/bin/env python3
"""
iptu2020_para_contribuinte.py — extrai do CADASTRO IPTU (safra 2016/2020, GeoSampa) os campos de
titularidade por imóvel, produzindo os recortes que a Fase B (`zepec/resolver_dono.py`) consome.

Por que a safra 2016/2020 e não a de 2026: a PMSP ANONIMIZOU o download depois (LGPD). A safra antiga
(35 colunas) traz `NOME DO CONTRIBUINTE 1/2` em claro + `CPF/CNPJ DO CONTRIBUINTE` (na 2016, CPF COMPLETO;
na 2020, mascarado). Ver `docs/AUDITORIA-DRIVE-INSUMOS-2026-07-16.md` e `docs/MAPA-FONTES-PROPRIETARIOS.md`.

DISCIPLINA DE PII (decisão do MOU 2026-07-17 — rodar ESCOPADO, guardando CPF):
  - `--filtro-sqls`: só emite as linhas cujo SQL está na NOSSA lista (os 4.292 tombados). O resto da
    cidade é lido e DESCARTADO — nunca vai para o git. Streaming (aguenta arquivo de ~1 GB sem estourar RAM).
  - **CPF/CNPJ são GUARDADOS** (autorizado pelo MOU: "pode guardar CPF"; repo privado, uso interno) — apenas
    dentro do escopo dos nossos SQLs; a cidade inteira nunca é gravada.

Extração PURA (1.2/1.3): só lê o que está no cadastro; não inventa. Limpeza público×privado pelo CONTRIBUINTE.

Saídas (em `zepec/oficial/`): iptu_contribuinte.csv (sql_mestre,documento,contribuinte) + iptu_flags.csv.

Uso:
  python3 comercial/iptu2020_para_contribuinte.py --entrada <iptu.csv> [--filtro-sqls <lista.csv|txt>]
  python3 comercial/iptu2020_para_contribuinte.py --autoteste
"""
import csv
import re
import sys
import argparse
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA_DIR = RAIZ / "zepec" / "oficial"
FIXTURE = RAIZ / "evals" / "ground-truth" / "comercial-fixture" / "iptu2020_amostra.csv"
LISTA_PADRAO = RAIZ / "casos-reais" / "tdc" / "LISTA-VENDEDORES.csv"

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

_PUB = re.compile(
    r"\b(PREFEITURA|MUNICIPIO|MUNICIPAL|UNIAO|UNIÃO|ESTADO DE|FAZENDA (PUBLICA|NACIONAL|DO ESTADO|MUNICIPAL)"
    r"|AUTARQUIA|GOVERNO|SECRETARIA|COMPANHIA DO METRO|METRO DE SAO PAULO|SPTRANS|DAEE|CDHU|COHAB)\b"
)


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().upper()


def _digitos(s):
    return re.sub(r"\D", "", s or "")


def _doc_saida(doc):
    """Guarda o documento completo (CPF 11 ou CNPJ 14) — autorizado pelo MOU 2026-07-17, dentro do escopo."""
    return _digitos(doc)


def _sql10(numero_contribuinte):
    d = _digitos(numero_contribuinte)
    return d[:10] if len(d) >= 10 else ""


def _acha_col(cabecalho_norm, *alvos):
    alvos = [_norm(a) for a in alvos]
    for i, c in enumerate(cabecalho_norm):
        for a in alvos:
            if a in c:
                return i
    return -1


def _detecta_encoding(path):
    with open(path, "rb") as fb:
        chunk = fb.read(8192)
    try:
        chunk.decode("utf-8"); return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"      # cadastro PMSP costuma ser cp1252/latin1


def _ler_csv(path):
    """Gera as linhas (streaming — não materializa o arquivo; aguenta ~1 GB). Delimitador: pipe > ; > ,."""
    enc = _detecta_encoding(path)
    with open(path, encoding=enc, errors="replace") as f:
        amostra = f.readline()
        delim = max(["|", ";", ","], key=lambda d: amostra.count(d))
        f.seek(0)
        for row in csv.reader(f, delimiter=delim):
            yield row


def parse(rows, filtro=None):
    """rows = iterável de listas (linhas do cadastro, incl. cabeçalho). filtro = set de SQLs a manter (ou None).
    Streaming + fail-closed em PII: CPF pessoal nunca sai (só CNPJ). Devolve (contrib, flags)."""
    it = iter(rows)
    try:
        cab = next(it)
    except StopIteration:
        return [], []
    cabN = [_norm(c) for c in cab]
    i_num = _acha_col(cabN, "NUMERO DO CONTRIBUINTE")
    i_t1 = _acha_col(cabN, "TIPO DE CONTRIBUINTE 1", "TIPO DE CONTRIBUINTE")
    i_d1 = _acha_col(cabN, "CPF/CNPJ DO CONTRIBUINTE 1", "CPF/CNPJ DO CONTRIBUINTE", "DOC CONTRIB")
    i_n1 = _acha_col(cabN, "NOME DO CONTRIBUINTE 1", "NOME DO CONTRIBUINTE")
    i_t2 = _acha_col(cabN, "TIPO DE CONTRIBUINTE 2")
    i_d2 = _acha_col(cabN, "CPF/CNPJ DO CONTRIBUINTE 2")
    i_n2 = _acha_col(cabN, "NOME DO CONTRIBUINTE 2")
    if i_num < 0 or i_n1 < 0:
        raise SystemExit(f"ERRO: cabeçalho sem NUMERO/NOME DO CONTRIBUINTE. Vistas: {cabN[:8]}")

    def cel(row, idx):
        return (row[idx].strip() if 0 <= idx < len(row) else "")

    contrib, flags, vistos = [], [], set()
    for row in it:
        if not row:
            continue
        sql = _sql10(cel(row, i_num))
        nome1 = cel(row, i_n1)
        if not sql or not nome1 or sql in vistos:
            continue
        if filtro is not None and sql not in filtro:
            continue           # ESCOPO: só os nossos SQLs; o resto da cidade é descartado (não vai ao git)
        vistos.add(sql)
        doc1_raw = _digitos(cel(row, i_d1))
        nome2, doc2_raw = cel(row, i_n2), _digitos(cel(row, i_d2))
        tipo1, tipo2 = cel(row, i_t1), cel(row, i_t2)
        publico = bool(_PUB.search(_norm(nome1)) or _PUB.search(_norm(nome2))
                       or _PUB.search(_norm(tipo1)) or _PUB.search(_norm(tipo2)))
        tipo_dono = "PUBLICO" if publico else ("PJ" if len(doc1_raw) == 14 else "PF")
        doc1, doc2 = _doc_saida(doc1_raw), _doc_saida(doc2_raw)   # CPF/CNPJ guardados (MOU 2026-07-17)
        contrib.append({"sql_mestre": sql, "documento": doc1, "contribuinte": nome1})
        flags.append({"sql_mestre": sql, "tipo_dono": tipo_dono, "publico": "sim" if publico else "nao",
                      "nome1": nome1, "doc1": doc1, "nome2": nome2, "doc2": doc2,
                      "fonte": "IPTU cadastral 2016/2020 (GeoSampa) — extração pura"})
    return contrib, flags


def _carrega_filtro(path):
    """Lê os SQLs (10 díg.) de um CSV (coluna 'sql' ou 'sql_mestre') ou txt (um por linha)."""
    p = Path(path)
    sqls = set()
    if not p.exists():
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        primeira = f.readline()
        f.seek(0)
        if "," in primeira or ";" in primeira and ("sql" in primeira.lower()):
            for r in csv.DictReader(f):
                v = r.get("sql") or r.get("sql_mestre") or ""
                d = _digitos(v)[:10]
                if len(d) == 10:
                    sqls.add(d)
        else:
            for ln in f:
                d = _digitos(ln)[:10]
                if len(d) == 10:
                    sqls.add(d)
    return sqls or None


def _autoteste():
    contrib, flags = parse(_ler_csv(FIXTURE))
    porsql = {c["sql_mestre"]: c for c in contrib}
    fl = {f["sql_mestre"]: f for f in flags}
    assert "0200670033" in porsql and "MARCIO" in porsql["0200670033"]["contribuinte"].upper()
    assert fl["0200670033"]["tipo_dono"] == "PF"
    # CPF completo GUARDADO na saída (autorizado pelo MOU 2026-07-17)
    assert porsql["0200670033"]["documento"] == "12345678909", porsql["0200670033"]["documento"]
    # PJ: CNPJ (14) MANTIDO
    assert len(_digitos(porsql["0100010001"]["documento"])) == 14
    assert fl["0100010001"]["tipo_dono"] == "PJ"
    # Público marcado
    assert fl["0000010001"]["publico"] == "sim" and fl["0000010001"]["tipo_dono"] == "PUBLICO"
    # FILTRO por SQL: só mantém o que está no set
    c2, _ = parse(_ler_csv(FIXTURE), filtro={"0100010001"})
    assert {x["sql_mestre"] for x in c2} == {"0100010001"}, {x["sql_mestre"] for x in c2}
    return len(contrib)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", nargs="*", default=[])
    ap.add_argument("--filtro-sqls", default="", help="CSV/txt com os SQLs a manter (escopo). Vazio = todos.")
    ap.add_argument("--autoteste", action="store_true")
    args = ap.parse_args()
    if args.autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE iptu2020_para_contribuinte: OK — {n} do fixture; CPF guardado/CNPJ/filtro/PUBLICO conferidos.")
        return 0
    if not args.entrada:
        print("uso: --entrada <iptu.csv> [--filtro-sqls <lista>]  ou  --autoteste", file=sys.stderr); return 2
    filtro = _carrega_filtro(args.filtro_sqls) if args.filtro_sqls else None
    if args.filtro_sqls and filtro:
        print(f"escopo: {len(filtro)} SQLs — o resto da cidade será descartado.")
    # Múltiplas safras (ex.: 2016 primeiro, 2020 como fallback): PRIMEIRA safra que traz o SQL VENCE,
    # tanto no contrib quanto nos flags (dedup consistente — senão a safra 2 sobrescreveria a 1 no join).
    contrib, flags, vistos = [], [], set()
    for p in args.entrada:
        c, f = parse(_ler_csv(p), filtro=filtro)
        fpor = {x["sql_mestre"]: x for x in f}
        for row in c:
            if row["sql_mestre"] not in vistos:
                vistos.add(row["sql_mestre"]); contrib.append(row)
                if row["sql_mestre"] in fpor:
                    flags.append(fpor[row["sql_mestre"]])
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAIDA_DIR / "iptu_contribuinte.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sql_mestre", "documento", "contribuinte"]); w.writeheader(); w.writerows(contrib)
    with open(SAIDA_DIR / "iptu_flags.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sql_mestre", "tipo_dono", "publico", "nome1", "doc1", "nome2", "doc2", "fonte"])
        w.writeheader(); w.writerows({k: r.get(k, "") for k in w.fieldnames} for r in flags)
    print(f"OK: {len(contrib)} contribuintes → zepec/oficial/iptu_contribuinte.csv (+ iptu_flags.csv) | CPF pessoal omitido")
    return 0


if __name__ == "__main__":
    sys.exit(main())
