#!/usr/bin/env python3
"""
gerar_fila_ingestao.py — Cruza os OFICIAL-pdf da vistoria de conteúdo (PROVENIENCIA-DE-PARA.csv)
contra o corpus já ingerido (leis/**/*.md) e produz a FILA DE INGESTÃO das normas ainda AUSENTES.

Doutrina: a vistoria só APONTA candidatos; a ingestão RE-VERIFICA cada um contra a fonte
(hash + verbatim + vigência, Partes 1.6/1.7) antes de virar leis/ citável. Este script é o passo
de TRIAGEM (Parte 3, etapa 2) — determinístico, sem LLM. Um número de norma que já existe no
corpus é descartado; o que falta entra na fila com o melhor drive_id (mais ocorrências = fonte
mais "inteira") para a ingestão puxar do Drive.

Saídas:
  inventario/drive-pu/FILA-INGESTAO-OFICIAL.csv  (uma linha por norma faltante)
"""
import csv, re, os, glob, sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DE_PARA = os.path.join(RAIZ, "inventario", "drive-pu", "PROVENIENCIA-DE-PARA.csv")
SAIDA = os.path.join(RAIZ, "inventario", "drive-pu", "FILA-INGESTAO-OFICIAL.csv")

# Número inteiro: n.nnn (com separador) ou 4-6 dígitos seguidos. Evita truncar "16050" em "160".
RX_NORMA = re.compile(r'\b(lei complementar|lei|decreto)\b\D{0,15}?(\d{1,2}[.\s]\d{3}|\d{4,6})', re.I)
RX_ANO = re.compile(r'\b(19\d{2}|20\d{2})\b')


def so_digitos(s):
    return re.sub(r'[.\s]', '', s)


def numeros_do_corpus():
    nums = set()
    for p in glob.glob(os.path.join(RAIZ, "leis", "**", "*.md"), recursive=True):
        b = os.path.basename(p)
        if b == "README.md":
            continue
        m = re.search(r'(\d{3,6})-(\d{4})', b)
        if m:
            nums.add(m.group(1))
    return nums


def main():
    corpus = numeros_do_corpus()
    cand = defaultdict(lambda: {"n": 0, "anos": set(), "melhor_id": "", "melhor_n": -1,
                                 "ex_nome": "", "evid": ""})
    with open(DE_PARA, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["classe"] != "OFICIAL" or r["ext"].lower() != "pdf":
                continue
            texto = r["nome"] + " || " + r["evidencia_conteudo"]
            achou = set()
            for m in RX_NORMA.finditer(texto):
                num = so_digitos(m.group(2))
                if len(num) < 4:
                    continue
                achou.add((m.group(1).split()[0].lower(), num))
            for k in achou:
                info = cand[k]
                info["n"] += 1
                for a in RX_ANO.findall(r["nome"]):
                    info["anos"].add(a)
                # melhor fonte = a com mais caracteres lidos (n_chars), proxy de "documento inteiro"
                try:
                    nch = int(r.get("n_chars") or 0)
                except ValueError:
                    nch = 0
                if nch > info["melhor_n"]:
                    info["melhor_n"] = nch
                    info["melhor_id"] = r["drive_id"]
                    info["ex_nome"] = r["nome"][:80]
                    info["evid"] = r["evidencia_conteudo"][:120]

    faltam = [(t, n, i) for (t, n), i in cand.items() if n not in corpus]
    faltam.sort(key=lambda x: -x[2]["n"])

    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tipo", "numero", "ano_provavel", "ocorrencias", "melhor_drive_id",
                    "n_chars_melhor", "exemplo_nome", "evidencia_conteudo"])
        for t, n, i in faltam:
            ano = sorted(i["anos"])[-1] if i["anos"] else ""
            w.writerow([t, n, ano, i["n"], i["melhor_id"], i["melhor_n"],
                        i["ex_nome"], i["evid"]])

    print(f"corpus (números já ingeridos): {len(corpus)}")
    print(f"normas OFICIAL-pdf detectadas: {len(cand)} | já no corpus: {len(cand)-len(faltam)} | FALTANTES: {len(faltam)}")
    print(f"fila gravada: {SAIDA}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
