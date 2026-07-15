#!/usr/bin/env python3
"""
capturar_casos_reais_tdc.py — CAPTURA de CASOS REAIS de TDC a partir das fontes OFICIAIS já em mãos
(extração PURA, 1.2: transcreve o que a fonte diz; não calcula, não inventa; célula ausente fica VAZIA).

Fonte primária: `zepec/raw/lista_certidao_ZEPEC-BIR_agosto-2025.csv` — a lista DEUSO/SMUL (Dec. 57.536/2016
Art. 12º) das Certidões de Transferência de Potencial Construtivo EMITIDAS (consolidação ago/2025). Cada linha
é uma TRANSFERÊNCIA REAL e traz, além do cedente, o **imóvel RECEPTOR** e as **áreas cedida-equivalente ×
recebida-real** — dados que o produto (cedente-side) ainda não tinha propagado.

Enriquecimento (etapa separada, 1.2): join por `N. processo` com `zepec/limpo/fundurb_processos.csv` (informe
FUNDURB do teto de 5%, Art. 24 §5º LPUOS) → anexa o `valor_pecuniario_rs` REAL aos ~7 processos grandes que casam.

Saída: `casos-reais/tdc/certidoes-reais-ago2025.csv` (arquivo NOVO — 1.5, não edita mestre), com proveniência
(fonte + sha256 + data de consolidação da fonte) em cada linha. Alimenta o diagnóstico (recalibra o Art. 128 com
n maior) e a validação da equivalência (área cedida equiv × recebida real = PCr do Art. 128).

Uso:
    python3 scripts/capturar_casos_reais_tdc.py            # captura + relatório
    python3 scripts/capturar_casos_reais_tdc.py --autoteste
"""
import csv
import re
import sys
import hashlib
import argparse
from pathlib import Path
from decimal import Decimal, InvalidOperation

RAIZ = Path(__file__).resolve().parent.parent
FONTE_CERT = RAIZ / "zepec" / "raw" / "lista_certidao_ZEPEC-BIR_agosto-2025.csv"
FONTE_FUND = RAIZ / "zepec" / "limpo" / "fundurb_processos.csv"
OUT_DIR = RAIZ / "casos-reais" / "tdc"
OUT = OUT_DIR / "certidoes-reais-ago2025.csv"
FONTE_TAG = ("DEUSO/SMUL — lista de Certidões de Transferência de Potencial Construtivo emitidas "
            "(Dec. 57.536/2016 Art. 12º), consolidação Agosto/2025")

CAMPOS = [
    "sql_cedente", "sq_cedente", "lote_cedente", "endereco_cedente", "distrito_cedente",
    "n_processo", "n_declaracao", "conservacao_art129",
    "sql_receptor", "sq_receptor", "lote_receptor", "endereco_receptor", "distrito_receptor",
    "n_certidao", "ano_certidao",
    "area_cedida_equivalente_m2", "area_recebida_real_m2", "data_publicacao", "situacao",
    "valor_pecuniario_rs", "status_fundurb", "base_periodo_fundurb_rs",  # enriquecimento (join FUNDURB)
    "fonte", "sha256_fonte",
]


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sql(sq, lote):
    """sql_mestre 10 díg = SQ(6: setor3+quadra3) + lote(4). Lote pode vir '0177-1' ou multi '0090-2, 0496-7'
    (receptor) → pega o PRIMEIRO token; só dígitos, zero-pad 4. Vazio se não der (fail-closed, não inventa)."""
    sqd = re.sub(r"\D", "", sq or "")
    tok = re.split(r"[,\s]", (lote or "").strip())[0] if lote else ""
    lod = re.sub(r"\D", "", tok)[:4]
    if len(sqd) < 6 or not lod:
        return ""
    return sqd[:6] + lod.zfill(4)


def _excel_data(serial):
    """Serial Excel (dias desde 1899-12-30) → 'AAAA-MM-DD'. Determinístico (não usa 'hoje'). Vazio se não-numérico."""
    s = (serial or "").strip()
    if not re.fullmatch(r"\d{4,6}", s):
        return s  # já pode ser texto/data; devolve como veio (extração pura)
    from datetime import date, timedelta
    return (date(1899, 12, 30) + timedelta(days=int(s))).isoformat()


def _norm_proc(p):
    return (p or "").strip()


def capturar():
    raw = list(csv.reader(open(FONTE_CERT, encoding="utf-8")))
    hdr_i = next(i for i, row in enumerate(raw)
                 if any("N. processo" in (c or "") for c in row) and any((c or "").strip() == "SQ" for c in row))
    data = [r for r in raw[hdr_i + 1:] if any((c or "").strip() for c in r)]
    sha = _sha256(FONTE_CERT)

    fund = {}
    if FONTE_FUND.exists():
        for p in csv.DictReader(open(FONTE_FUND, encoding="utf-8")):
            fund[_norm_proc(p.get("n_processo"))] = p

    def cell(r, i):
        return (r[i].strip() if len(r) > i and r[i] is not None else "")

    linhas = []
    for r in data:
        proc = cell(r, 1)
        fp = fund.get(_norm_proc(proc), {})
        linhas.append({
            "sql_cedente": _sql(cell(r, 2), cell(r, 3)),
            "sq_cedente": cell(r, 2), "lote_cedente": cell(r, 3),
            "endereco_cedente": cell(r, 4), "distrito_cedente": cell(r, 5),
            "n_processo": proc, "n_declaracao": cell(r, 6), "conservacao_art129": cell(r, 7),
            "sql_receptor": _sql(cell(r, 8), cell(r, 9)),
            "sq_receptor": cell(r, 8), "lote_receptor": cell(r, 9),
            "endereco_receptor": cell(r, 10), "distrito_receptor": cell(r, 11),
            "n_certidao": cell(r, 12), "ano_certidao": cell(r, 13),
            "area_cedida_equivalente_m2": cell(r, 15), "area_recebida_real_m2": cell(r, 16),
            "data_publicacao": _excel_data(cell(r, 17)), "situacao": cell(r, 18),
            "valor_pecuniario_rs": (fp.get("valor_pecuniario_rs") or "").strip(),
            "status_fundurb": (fp.get("status_fundurb") or "").strip(),
            "base_periodo_fundurb_rs": (fp.get("base_periodo_rs") or "").strip(),
            "fonte": FONTE_TAG, "sha256_fonte": sha[:16],
        })
    return linhas


def _num(s):
    s = (s or "").strip()
    if not s:
        return None
    s = s.replace(".", "").replace(",", ".") if ("," in s) else s
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def relatorio(linhas):
    n = len(linhas)
    ced = sum(1 for l in linhas if l["sql_cedente"])
    rec = sum(1 for l in linhas if l["sql_receptor"])
    ar_eq = sum(1 for l in linhas if _num(l["area_cedida_equivalente_m2"]))
    ar_re = sum(1 for l in linhas if _num(l["area_recebida_real_m2"]))
    val = sum(1 for l in linhas if l["valor_pecuniario_rs"])
    ced_dist = len({l["sql_cedente"] for l in linhas if l["sql_cedente"]})
    rec_dist = len({l["sql_receptor"] for l in linhas if l["sql_receptor"]})
    print(f"=== CAPTURA de casos reais (certidões DEUSO/SMUL ago/2025) ===")
    print(f"  transferências reais capturadas : {n}")
    print(f"  com SQL cedente resolvido       : {ced}  ({ced_dist} cedentes distintos)")
    print(f"  com SQL RECEPTOR (novo!)        : {rec}  ({rec_dist} receptores distintos)")
    print(f"  com área cedida-equivalente     : {ar_eq}")
    print(f"  com área recebida-real          : {ar_re}")
    print(f"  com valor R$ REAL (join FUNDURB): {val}")
    # want-list: linhas sem SQL cedente resolvido
    faltam = [l["n_processo"] for l in linhas if not l["sql_cedente"]]
    print(f"  WANT-LIST — sem SQL cedente ({len(faltam)}): {faltam[:8]}{'…' if len(faltam) > 8 else ''}")
    return dict(n=n, ced=ced, rec=rec, val=val, ar_eq=ar_eq)


def _autoteste():
    linhas = capturar()
    assert len(linhas) > 150, f"esperava >150 certidões reais, veio {len(linhas)}"
    assert sum(1 for l in linhas if l["sql_receptor"]) > 100, "receptor deve vir na maioria (coluna nova)"
    assert sum(1 for l in linhas if l["valor_pecuniario_rs"]) >= 7, "join FUNDURB deve casar >=7 valores"
    # SQL bem formado (10 díg) quando resolvido
    for l in linhas:
        if l["sql_cedente"]:
            assert re.fullmatch(r"\d{10}", l["sql_cedente"]), l["sql_cedente"]
    # data em ISO quando era serial Excel
    assert any(re.fullmatch(r"\d{4}-\d{2}-\d{2}", l["data_publicacao"]) for l in linhas), "datas Excel→ISO"
    return len(linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()
    if a.autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE captura: OK — {n} casos reais, SQL/receptor/valor/data validados.")
        return 0
    linhas = capturar()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(linhas)
    relatorio(linhas)
    print(f"\nSAÍDA: {OUT.relative_to(RAIZ)} ({len(linhas)} linhas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
