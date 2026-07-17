#!/usr/bin/env python3
"""
recorta_receita_oficial.py — recorta a base NACIONAL OFICIAL do CNPJ da Receita Federal (arquivos
`*.EMPRECSV` e `*.SOCIOCSV`, sem cabeçalho, delimitador `;`, latin1) para só os CNPJs dos nossos
contribuintes, em STREAMING (processa 1 arquivo por vez; a Action baixa+descompacta+apaga cada .zip),
e normaliza para o contrato que `zepec/resolver_dono.py` consome.

Por que esta base (e não a parcial anterior): a oficial cobre 100% das PJs do país. O gargalo era
(a) base parcial e (b) CNPJ malformado no nosso lado. Aqui resolvemos os dois:
  - casa por CNPJ BÁSICO (8 díg.) — sócio liga-se ao básico, não ao CNPJ de 14 (que exigiria Estabelecimentos);
  - RECUPERA o básico dos nossos CNPJs malformados casando a RAZÃO SOCIAL exata (Empresas.razao_social).

Layout oficial (metadados Receita):
  SOCIOS  (11 col): cnpj_basico; identificador_socio(1=PJ,2=PF,3=Estr); nome_socio; cnpj_cpf_socio(CPF MASCARADO);
                    qualificacao; data; pais; cpf_repr; nome_repr; qual_repr; faixa_etaria
  EMPRESAS (7 col): cnpj_basico; razao_social; natureza; qual_resp; capital; porte; ente

Chave de saída = CNPJ sintético de 14 = basico(8) + '000000' (consistente dos dois lados: nosso contrib e
os sócios-PJ viram synth14 do seu básico). Assim o resolver (que trata 14-díg como CNPJ e o resto como PF
pelo nome) roda sem mudança. CPF completo do sócio NÃO existe na base aberta (vem mascarado) — isso é a Assertiva.

Fases (a Action chama uma por vez; estado persiste em --estado):
  --fase alvos    --contrib <iptu_contribuinte.csv> --estado <dir>
  --fase empresas --entrada <arq.EMPRECSV>          --estado <dir>   (repete por arquivo)
  --fase socios   --entrada <arq.SOCIOCSV>           --estado <dir>   (repete por arquivo)
  --fase finalize --estado <dir> --saida <recorte>                    (gera empresas/socios/iptu_contribuinte)
  --autoteste
"""
import csv
import re
import sys
import argparse
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FIX = RAIZ / "evals" / "ground-truth" / "receita-oficial-fixture"
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def _dig(s):
    return re.sub(r"\D", "", s or "")


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().upper()


def _basic8(doc):
    d = _dig(doc)
    return d[:8] if len(d) >= 8 else ""


def _synth14(basic8):
    return (basic8 + "000000") if len(basic8) == 8 else ""


def _stream_oficial(path):
    """Gera listas de campos de um arquivo oficial (sem header, `;`, latin1). Streaming."""
    with open(path, encoding="latin-1", errors="replace") as f:
        for row in csv.reader(f, delimiter=";"):
            yield row


def _le_set(p):
    return set(l.strip() for l in open(p, encoding="utf-8") if l.strip()) if Path(p).exists() else set()


def fase_alvos(contrib_path, estado):
    estado = Path(estado); estado.mkdir(parents=True, exist_ok=True)
    basics, nomes = set(), set()
    import shutil
    shutil.copyfile(contrib_path, estado / "contrib.csv")
    for r in csv.DictReader(open(contrib_path, encoding="utf-8", errors="replace")):
        doc = _dig(r.get("documento"))
        nome = _norm(r.get("contribuinte"))
        if len(doc) >= 12:                      # candidato a CNPJ → básico dos 8 primeiros
            b = _basic8(doc)
            if b:
                basics.add(b)
        if nome:
            nomes.add(nome)                     # p/ recuperar básico via razão social exata
    (estado / "alvos_basic.txt").write_text("\n".join(sorted(basics)), encoding="utf-8")
    (estado / "alvos_nome.txt").write_text("\n".join(sorted(nomes)), encoding="utf-8")
    (estado / "needed_basic.txt").write_text("", encoding="utf-8")
    return len(basics), len(nomes)


def fase_empresas(entrada, estado):
    estado = Path(estado)
    alvos_basic = _le_set(estado / "alvos_basic.txt")
    alvos_nome = _le_set(estado / "alvos_nome.txt")
    needed = _le_set(estado / "needed_basic.txt")
    n = 0
    with open(estado / "empresas_recorte.tsv", "a", encoding="utf-8") as fe, \
         open(estado / "nome2basic.tsv", "a", encoding="utf-8") as fn:
        for row in _stream_oficial(entrada):
            if len(row) < 2:
                continue
            basic = _dig(row[0])[:8]
            razao = row[1].strip()
            if not basic:
                continue
            por_basic = basic in alvos_basic
            por_nome = _norm(razao) in alvos_nome
            if por_basic or por_nome:
                fe.write(f"{basic}\t{razao}\n"); n += 1
                needed.add(basic)
                if por_nome:
                    fn.write(f"{_norm(razao)}\t{basic}\n")
    (estado / "needed_basic.txt").write_text("\n".join(sorted(needed)), encoding="utf-8")
    return n


def fase_socios(entrada, estado):
    estado = Path(estado)
    needed = _le_set(estado / "needed_basic.txt")   # conjunto vivo (holdings forward-ref entram aqui)
    n = 0
    with open(estado / "socios_recorte.tsv", "a", encoding="utf-8") as fs:
        for row in _stream_oficial(entrada):
            if len(row) < 4:
                continue
            basic = _dig(row[0])[:8]
            if not basic or basic not in needed:
                continue
            ident = (row[1] or "").strip()
            nome = (row[2] or "").strip()
            doc_socio = _dig(row[3])
            if ident == "1" and len(doc_socio) >= 8:        # sócio PJ → sobe a cadeia (synth14 do básico)
                b2 = doc_socio[:8]
                doc_out = _synth14(b2)
                needed.add(b2)                              # captura holding (forward-ref no mesmo streaming)
            else:                                           # PF/estrangeiro → é a pessoa; doc mascarado descartado
                doc_out = ""
            fs.write(f"{_synth14(basic)}\t{doc_out}\t{nome}\n"); n += 1
    (estado / "needed_basic.txt").write_text("\n".join(sorted(needed)), encoding="utf-8")
    return n


def fase_finalize(estado, saida):
    estado = Path(estado); saida = Path(saida); saida.mkdir(parents=True, exist_ok=True)
    # empresas: básico → razão (primeiro vence)
    basic2razao = {}
    p = estado / "empresas_recorte.tsv"
    if p.exists():
        for ln in open(p, encoding="utf-8"):
            b, _, razao = ln.rstrip("\n").partition("\t")
            if b and b not in basic2razao:
                basic2razao[b] = razao
    nome2basic = {}
    p = estado / "nome2basic.tsv"
    if p.exists():
        for ln in open(p, encoding="utf-8"):
            nm, _, b = ln.rstrip("\n").partition("\t")
            if nm and nm not in nome2basic:
                nome2basic[nm] = b
    with open(saida / "empresas.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cnpj", "razao_social"])
        for b, razao in basic2razao.items():
            w.writerow([_synth14(b), razao])
    # socios: dedup
    vistos = set(); n_soc = 0
    with open(saida / "socios.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cnpj", "doc_socio", "nome_socio"])
        p = estado / "socios_recorte.tsv"
        if p.exists():
            for ln in open(p, encoding="utf-8"):
                parts = ln.rstrip("\n").split("\t")
                if len(parts) != 3:
                    continue
                key = tuple(parts)
                if key in vistos:
                    continue
                vistos.add(key); w.writerow(parts); n_soc += 1
    # contrib corrigido: remapeia o documento p/ synth14 do básico recuperado (CNPJ válido OU razão social)
    n_corr = 0
    with open(saida / "iptu_contribuinte.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sql_mestre", "documento", "contribuinte"]); w.writeheader()
        for r in csv.DictReader(open(estado / "contrib.csv", encoding="utf-8", errors="replace")):
            doc = _dig(r.get("documento")); nome = _norm(r.get("contribuinte"))
            out = r.get("documento") or ""
            if len(doc) == 11:                                  # CPF → PF direta, mantém
                out = doc
            else:
                b = _basic8(doc)
                if b and b in basic2razao:                      # casou por CNPJ básico
                    out = _synth14(b); n_corr += 1
                elif nome in nome2basic:                        # recuperado por razão social
                    out = _synth14(nome2basic[nome]); n_corr += 1
            w.writerow({"sql_mestre": r.get("sql_mestre", ""), "documento": out,
                        "contribuinte": r.get("contribuinte", "")})
    return len(basic2razao), n_soc, n_corr


def _autoteste():
    import tempfile
    sys.path.insert(0, str(RAIZ / "zepec"))
    import importlib
    resolver = importlib.import_module("resolver_dono")
    with tempfile.TemporaryDirectory() as d:
        fase_alvos(FIX / "contrib.csv", d)
        fase_empresas(FIX / "empresas0.csv", d)
        fase_socios(FIX / "socios0.csv", d)
        with tempfile.TemporaryDirectory() as saida:
            ne, ns, nc = fase_finalize(d, saida)
            contrib, empresas, socios = resolver._carregar(Path(saida))
            linhas = {l["sql_mestre"]: l["proprietario"] for l in resolver.resolver(contrib, empresas, socios)}
    # SQLPJ0001 (CNPJ válido) → RAZAO UM, controladores FULANO + BELTRANO (via holding RAZAO TRES)
    assert "FULANO" in linhas["SQLPJ0001"].upper() and "BELTRANO" in linhas["SQLPJ0001"].upper(), linhas["SQLPJ0001"]
    # SQLPJ0002 (CNPJ malformado, recuperado por RAZÃO SOCIAL) → controlador BELTRANO
    assert "BELTRANO" in linhas["SQLPJ0002"].upper(), linhas["SQLPJ0002"]
    # SQLPF0003 (CPF) → PF direta
    assert "FULANO PESSOA FISICA" in linhas["SQLPF0003"].upper(), linhas["SQLPF0003"]
    return len(linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fase", choices=["alvos", "empresas", "socios", "finalize"])
    ap.add_argument("--contrib", default="")
    ap.add_argument("--entrada", default="")
    ap.add_argument("--estado", default="_rf_estado")
    ap.add_argument("--saida", default="zepec/oficial/recorte")
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()
    if a.autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE recorta_receita_oficial: OK — {n} SQLs; CNPJ básico + recuperação por razão social + "
              f"holding forward-ref + PF direta conferidos (cadeia ponta a ponta com o resolver).")
        return 0
    if a.fase == "alvos":
        nb, nn = fase_alvos(a.contrib, a.estado)
        print(f"alvos: {nb} básicos + {nn} nomes p/ recuperação")
    elif a.fase == "empresas":
        n = fase_empresas(a.entrada, a.estado)
        print(f"empresas: +{n} casadas em {Path(a.entrada).name}")
    elif a.fase == "socios":
        n = fase_socios(a.entrada, a.estado)
        print(f"socios: +{n} sócios em {Path(a.entrada).name}")
    elif a.fase == "finalize":
        ne, ns, nc = fase_finalize(a.estado, a.saida)
        print(f"finalize: empresas={ne} socios={ns} contrib_corrigidos={nc} → {a.saida}")
    else:
        print("informe --fase ou --autoteste", file=sys.stderr); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
