#!/usr/bin/env python3
"""
iptu2020_para_contribuinte.py — extrai do CADASTRO IPTU (safra 2020/2016, GeoSampa) os campos de
titularidade por imóvel, produzindo os recortes que a Fase B (`zepec/resolver_dono.py`) consome.

Por que a safra 2020/2016 e não a de 2026: a PMSP ANONIMIZOU o download entre 2020 e 2026 (LGPD).
A safra antiga (35 colunas) ainda traz `NOME DO CONTRIBUINTE 1/2` em claro + `CPF/CNPJ DO CONTRIBUINTE`
(CPF vem MASCARADO, ex. `XXXXXX0214XXXX`; CNPJ tende a vir inteiro). Provado por cabeçalho real em
repo público (learning-crawlers/Dados-Publicos GEOSAMPA/IPTU_2020.csv + oficial geoinfo-smdu/cadastro-fiscal).
Ver `docs/AUDITORIA-DRIVE-INSUMOS-2026-07-16.md`.

Extração PURA (1.2/1.3): só lê o que está no cadastro; não inventa, não interpreta. Cada saída rastreia à fonte.

Entradas: um ou mais CSVs do cadastro IPTU (delimitador `;`), casados por NOME de coluna (robusto à ordem).
Saídas (em `zepec/oficial/`, consumidas pelo resolver e pelo enriquecedor):
  - iptu_contribuinte.csv  → sql_mestre, documento, contribuinte   (o contrato do resolver_dono)
  - iptu_flags.csv         → sql_mestre, tipo_dono, publico, nome1, doc1, nome2, doc2, fonte
Regra da limpeza público×privado (autoritativa, do contribuinte — NÃO por nome de logradouro):
  público = TIPO/ NOME do contribuinte casa PREFEITURA/MUNICIPIO/UNIAO/ESTADO/FAZENDA PUBLICA/AUTARQUIA/GOVERNO.

Uso:
  python3 comercial/iptu2020_para_contribuinte.py --entrada <iptu.csv> [<iptu2.csv> ...]
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

# aumenta o teto de campo (linhas de cadastro podem ser largas)
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

_PUB = re.compile(
    r"\b(PREFEITURA|MUNICIPIO|MUNICIPAL|UNIAO|UNIÃO|ESTADO DE|FAZENDA (PUBLICA|NACIONAL|DO ESTADO|MUNICIPAL)"
    r"|AUTARQUIA|GOVERNO|SECRETARIA|COMPANHIA DO METRO|METRO DE SAO PAULO|SPTRANS|DAEE|CDHU|COHAB)\b"
)


def _norm(s):
    """Maiúsculas sem acento, para casar cabeçalho/valor de forma robusta."""
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().upper()


def _digitos(s):
    return re.sub(r"\D", "", s or "")


def _sql10(numero_contribuinte):
    """Normaliza o 'NUMERO DO CONTRIBUINTE' do IPTU para o SQL de 10 dígitos usado nas nossas listas.
    Ex.: '001.003.0001-4' / '0010030001-4' → '0010030001' (setor+quadra+lote, sem dígito verificador)."""
    d = _digitos(numero_contribuinte)
    return d[:10] if len(d) >= 10 else ""


def _acha_col(cabecalho_norm, *alvos):
    """Devolve o índice da 1ª coluna cujo nome normalizado casa um dos alvos (também normalizados)."""
    alvos = [_norm(a) for a in alvos]
    for i, c in enumerate(cabecalho_norm):
        for a in alvos:
            if a in c:
                return i
    return -1


def _doc_utilizavel(doc):
    """CNPJ de 14 dígitos é inteiro (utilizável na cadeia). CPF vem mascarado (não 11 dígitos limpos):
    guardamos como veio (parcial) — o nome é que identifica a PF; o CPF completo é enriquecimento externo."""
    return _digitos(doc)


def parse(rows):
    """rows = iterável de listas (linhas do CSV do cadastro, incl. cabeçalho). Devolve (contrib, flags)."""
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
        raise SystemExit("ERRO: cabeçalho não tem 'NUMERO DO CONTRIBUINTE' e/ou 'NOME DO CONTRIBUINTE 1'. "
                         f"Colunas vistas: {cabN[:8]}...")

    def cel(row, idx):
        return (row[idx].strip() if 0 <= idx < len(row) else "")

    contrib, flags = [], []
    vistos = set()
    for row in it:
        if not row:
            continue
        sql = _sql10(cel(row, i_num))
        nome1 = cel(row, i_n1)
        if not sql or not nome1:
            continue
        if sql in vistos:      # 1ª ocorrência do SQL manda (dedup determinístico)
            continue
        vistos.add(sql)
        doc1 = _doc_utilizavel(cel(row, i_d1))
        nome2 = cel(row, i_n2)
        doc2 = _doc_utilizavel(cel(row, i_d2))
        tipo1 = cel(row, i_t1)
        tipo2 = cel(row, i_t2)
        publico = bool(_PUB.search(_norm(nome1)) or _PUB.search(_norm(nome2))
                       or _PUB.search(_norm(tipo1)) or _PUB.search(_norm(tipo2)))
        # tipo do dono: PJ se o doc do 1º contribuinte tem 14 díg.; senão PF (CPF mascarado)
        tipo_dono = "PUBLICO" if publico else ("PJ" if len(doc1) == 14 else "PF")
        # contrato do resolver_dono: documento CNPJ (14) sobe a cadeia; CPF mascarado não valida (fica PENDENTE lá,
        # mas o nome vem pelo enriquecedor via iptu_flags). Passamos o doc como está.
        contrib.append({"sql_mestre": sql, "documento": doc1, "contribuinte": nome1})
        flags.append({"sql_mestre": sql, "tipo_dono": tipo_dono, "publico": "sim" if publico else "nao",
                      "nome1": nome1, "doc1": doc1, "nome2": nome2, "doc2": doc2,
                      "fonte": "IPTU cadastral 2020/2016 (GeoSampa) — extração pura"})
    return contrib, flags


def _ler_csv(path):
    # cadastro IPTU é ';' — mas aceitamos ',' no fixture; detecta pelo cabeçalho
    with open(path, encoding="utf-8", errors="replace") as f:
        amostra = f.readline()
        delim = ";" if amostra.count(";") >= amostra.count(",") else ","
        f.seek(0)
        return list(csv.reader(f, delimiter=delim))


def _autoteste():
    contrib, flags = parse(_ler_csv(FIXTURE))
    porsql = {c["sql_mestre"]: c for c in contrib}
    fl = {f["sql_mestre"]: f for f in flags}
    # PF com CPF mascarado: nome vem, doc fica parcial, tipo PF
    assert "0200670033" in porsql, porsql.keys()
    assert "MARCIO" in porsql["0200670033"]["contribuinte"].upper()
    assert fl["0200670033"]["tipo_dono"] == "PF"
    # PJ com CNPJ inteiro: documento com 14 dígitos, tipo PJ
    assert len(_digitos(porsql["0100010001"]["documento"])) == 14
    assert fl["0100010001"]["tipo_dono"] == "PJ"
    # Público: Prefeitura marcada
    assert fl["0000010001"]["publico"] == "sim" and fl["0000010001"]["tipo_dono"] == "PUBLICO"
    # SQL normalizado a 10 díg. a partir de '020.067.0033-1'
    return len(contrib)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", nargs="*", default=[], help="CSV(s) do cadastro IPTU 2020/2016")
    ap.add_argument("--autoteste", action="store_true")
    args = ap.parse_args()
    if args.autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE iptu2020_para_contribuinte: OK — {n} contribuintes do fixture; "
              f"PF(mascarado)/PJ(CNPJ)/PUBLICO e SQL-10 conferidos.")
        return 0
    if not args.entrada:
        print("uso: --entrada <iptu.csv> [...]  ou  --autoteste", file=sys.stderr)
        return 2
    contrib, flags = [], []
    vistos = set()
    for p in args.entrada:
        c, f = parse(_ler_csv(p))
        for row in c:
            if row["sql_mestre"] not in vistos:
                vistos.add(row["sql_mestre"]); contrib.append(row)
        flags.extend(f)
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAIDA_DIR / "iptu_contribuinte.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sql_mestre", "documento", "contribuinte"]); w.writeheader(); w.writerows(contrib)
    with open(SAIDA_DIR / "iptu_flags.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sql_mestre", "tipo_dono", "publico", "nome1", "doc1", "nome2", "doc2", "fonte"])
        w.writeheader(); w.writerows({k: r.get(k, "") for k in w.fieldnames} for r in flags)
    print(f"OK: {len(contrib)} contribuintes → zepec/oficial/iptu_contribuinte.csv (+ iptu_flags.csv)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
