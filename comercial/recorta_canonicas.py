#!/usr/bin/env python3
"""
recorta_canonicas.py — filtra as canônicas societárias (empresas/socios/holdings, ATÉ 3,4 GB cada) para só
os CNPJs que interessam, em STREAMING (nunca carrega a base inteira na RAM), e normaliza as colunas para o
contrato que `zepec/resolver_dono.py` espera. Assim o resolver roda sobre um recorte pequeno, sem OOM.

Fecho recursivo (holding): parte dos CNPJs dos nossos contribuintes-PJ; se um sócio/controladora é outro
CNPJ, entra no conjunto e o próximo passo o percorre (até MAXDEPTH). Passos re-leem os arquivos (streaming),
então a memória fica limitada ao CONJUNTO de CNPJs (pequeno), não às linhas.

Entradas: iptu_contribuinte.csv (nossos CNPJs) + empresas/socios/holdings.csv (brutos, colunas variam).
Saídas (dir --saida): empresas.csv(cnpj,razao_social) · socios.csv(cnpj,doc_socio,nome_socio) ·
                      holdings.csv(cnpj_controlada,cnpj_controladora,nome_controladora)  ← contrato do resolver.

Uso:
  python3 comercial/recorta_canonicas.py --base <dir_brutos> --contrib <iptu_contribuinte.csv> --saida <dir>
  python3 comercial/recorta_canonicas.py --autoteste
"""
import csv
import re
import sys
import argparse
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FIX = RAIZ / "evars" if False else RAIZ / "evals" / "ground-truth" / "canonicas-fixture"
MAXDEPTH = 4
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def _dig(s):
    return re.sub(r"\D", "", s or "")


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().upper()


def _idx(header, *alvos):
    hN = [_norm(h) for h in header]
    for i, c in enumerate(hN):
        for a in alvos:
            if _norm(a) == c or _norm(a) in c:
                return i
    return -1


def _stream(path):
    if not Path(path).exists():
        return
    with open(path, encoding="utf-8", errors="replace") as f:
        amostra = f.readline()
        delim = max([",", ";", "|"], key=lambda d: amostra.count(d))
        f.seek(0)
        rd = csv.reader(f, delimiter=delim)
        try:
            header = next(rd)
        except StopIteration:
            return
        yield header
        for row in rd:
            yield row


def _cols_socios(header):
    return (_idx(header, "cnpj"), _idx(header, "cpf_cnpj_socio", "doc_socio", "cpf/cnpj do socio", "documento socio"),
            _idx(header, "nome_socio", "nome do socio"))


def _cols_holdings(header):
    return (_idx(header, "cnpj_controlada", "cnpj"), _idx(header, "cnpj_controladora", "cnpj_socia", "cnpj socia"),
            _idx(header, "nome_controladora", "razao_social_soc", "razao social socia"))


def fecho_cnpjs(base, alvos):
    """Conjunto de CNPJs no fecho recursivo (nossos + sócios-PJ + controladoras-holding). Streaming."""
    needed = set(alvos)
    for _ in range(MAXDEPTH):
        novos = set()
        it = _stream(Path(base) / "socios.csv"); header = next(it, None)
        if header:
            ic, isoc, _ = _cols_socios(header)
            for row in it:
                if ic < 0 or ic >= len(row):
                    continue
                if _dig(row[ic]) in needed and 0 <= isoc < len(row):
                    d = _dig(row[isoc])
                    if len(d) == 14 and d not in needed:
                        novos.add(d)
        it = _stream(Path(base) / "holdings.csv"); header = next(it, None)
        if header:
            ida, idb, _ = _cols_holdings(header)
            for row in it:
                if 0 <= ida < len(row) and _dig(row[ida]) in needed and 0 <= idb < len(row):
                    d = _dig(row[idb])
                    if len(d) == 14 and d not in needed:
                        novos.add(d)
        if not novos:
            break
        needed |= novos
    return needed


def recorta(base, needed, saida):
    saida = Path(saida); saida.mkdir(parents=True, exist_ok=True)
    # empresas
    it = _stream(Path(base) / "empresas.csv"); header = next(it, None); n_emp = 0
    with open(saida / "empresas.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cnpj", "razao_social"])
        if header:
            ic, ir = _idx(header, "cnpj"), _idx(header, "razao_social", "razao social")
            for row in it:
                if 0 <= ic < len(row) and _dig(row[ic]) in needed:
                    w.writerow([_dig(row[ic]), (row[ir] if 0 <= ir < len(row) else "").strip()]); n_emp += 1
    # socios
    it = _stream(Path(base) / "socios.csv"); header = next(it, None); n_soc = 0
    with open(saida / "socios.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cnpj", "doc_socio", "nome_socio"])
        if header:
            ic, isoc, inome = _cols_socios(header)
            for row in it:
                if 0 <= ic < len(row) and _dig(row[ic]) in needed:
                    w.writerow([_dig(row[ic]), _dig(row[isoc]) if 0 <= isoc < len(row) else "",
                                (row[inome] if 0 <= inome < len(row) else "").strip()]); n_soc += 1
    # holdings
    it = _stream(Path(base) / "holdings.csv"); header = next(it, None); n_hold = 0
    with open(saida / "holdings.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cnpj_controlada", "cnpj_controladora", "nome_controladora"])
        if header:
            ida, idb, inome = _cols_holdings(header)
            for row in it:
                if 0 <= ida < len(row) and _dig(row[ida]) in needed:
                    w.writerow([_dig(row[ida]), _dig(row[idb]) if 0 <= idb < len(row) else "",
                                (row[inome] if 0 <= inome < len(row) else "").strip()]); n_hold += 1
    return n_emp, n_soc, n_hold


def _alvos_do_contrib(path):
    alvos = set()
    if Path(path).exists():
        for r in csv.DictReader(open(path, encoding="utf-8", errors="replace")):
            d = _dig(r.get("documento"))
            if len(d) == 14:
                alvos.add(d)
    return alvos


def _autoteste():
    needed = fecho_cnpjs(FIX, {"11111111111111"})
    # 111 é sócia da 222 (holding) e tem sócio-PJ 333 → fecho pega 111, 333, e via holdings a controladora
    assert "11111111111111" in needed and "33333333333333" in needed, needed
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        ne, ns, nh = recorta(FIX, needed, d)
        emp = {r["cnpj"]: r for r in csv.DictReader(open(Path(d) / "empresas.csv"))}
        soc = list(csv.DictReader(open(Path(d) / "socios.csv")))
        assert "11111111111111" in emp and "RAZAO UM" in emp["11111111111111"]["razao_social"].upper()
        # socios normalizado: cnpj, doc_socio, nome_socio
        assert any(s["cnpj"] == "11111111111111" and "FULANO" in s["nome_socio"].upper() for s in soc), soc
    return len(needed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="zepec/oficial")
    ap.add_argument("--contrib", default="zepec/oficial/iptu_contribuinte.csv")
    ap.add_argument("--saida", default="zepec/oficial/recorte")
    ap.add_argument("--autoteste", action="store_true")
    args = ap.parse_args()
    if args.autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE recorta_canonicas: OK — fecho de {n} CNPJs; recorte+normalização conferidos.")
        return 0
    alvos = _alvos_do_contrib(args.contrib)
    print(f"CNPJs alvo (nossos PJ): {len(alvos)}")
    needed = fecho_cnpjs(args.base, alvos)
    print(f"fecho recursivo (com holdings): {len(needed)} CNPJs")
    ne, ns, nh = recorta(args.base, needed, args.saida)
    # o recorte precisa ser AUTO-SUFICIENTE p/ o resolver (`--base <recorte>`): ele lê iptu_contribuinte.csv
    # de DENTRO da base. O recortador só emite empresas/socios/holdings; sem esta cópia o resolver aborta
    # com "[AGUARDANDO] ... iptu_contribuinte.csv ausente" e não resolve nenhum controlador.
    n_contrib = 0
    if Path(args.contrib).exists():
        import shutil
        Path(args.saida).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.contrib, Path(args.saida) / "iptu_contribuinte.csv")
        with open(args.contrib, encoding="utf-8", errors="replace") as f:
            n_contrib = max(0, sum(1 for _ in f) - 1)
    print(f"recorte → empresas={ne} socios={ns} holdings={nh} contrib={n_contrib} em {args.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
