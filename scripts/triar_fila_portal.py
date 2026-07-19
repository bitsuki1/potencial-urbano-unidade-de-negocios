#!/usr/bin/env python3
"""
triar_fila_portal.py — TRIAGEM (Parte 3, etapa 2) da fila de ingestão, SEM escrever no corpus.
Para cada norma faltante com data parseável, deriva o slug do portal, baixa o texto oficial e
extrai ementa + sinais determinísticos (TDC × IPTU × ambiental/outro). Gera uma tabela de triagem
para o orquestrador decidir O QUE ingerir primeiro (TDC = base inicial, decisão do MOU).

NÃO promove nada (não escreve .json/.md em leis/). Só lê e classifica. Saída:
  inventario/drive-pu/TRIAGEM-FILA-PORTAL.csv
"""
import csv, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_norma_portal import baixar, extrair_texto  # reusa o extrator auditável

RAIZ = Path(__file__).resolve().parent.parent
FILA = RAIZ / "inventario" / "drive-pu" / "FILA-INGESTAO-OFICIAL.csv"
SAIDA = RAIZ / "inventario" / "drive-pu" / "TRIAGEM-FILA-PORTAL.csv"

MESES = {"janeiro","fevereiro","março","marco","abril","maio","junho","julho",
         "agosto","setembro","outubro","novembro","dezembro"}
RX_DATA = re.compile(r'(LEI|DECRETO)\s+N[ºo°]\s*[\d.]+\s+DE\s+(\d{1,2})\s+DE\s+(\w+)\s+DE\s+(\d{4})', re.I)

# sinais determinísticos (contagem de ocorrências no texto real)
SIN_TDC = re.compile(r'transfer[êe]ncia do direito de construir|potencial construtivo|outorga onerosa|'
                     r'coeficiente de aproveitamento|CEPAC|solo criado|plano de interven[çc][ãa]o urbana|'
                     r'opera[çc][ãa]o urbana|FUNDURB|ZEPEC|CONPRESP', re.I)
SIN_IPTU = re.compile(r'\bIPTU\b|imposto predial|planta gen[ée]rica de valores|valor venal|'
                      r'lan[çc]amento tribut[áa]rio|base de c[áa]lculo do imposto', re.I)
SIN_AMB = re.compile(r'mata atl[âa]ntica|quota ambiental|[áa]rea de preserva[çc][ãa]o|licenciamento ambiental', re.I)


def slug_de(exemplo):
    m = RX_DATA.search(exemplo)
    if not m:
        return None
    tipo = m.group(1).lower()
    dia = int(m.group(2))
    mes = m.group(3).lower().replace("ç", "c")
    ano = m.group(4)
    if mes not in {x.replace("ç","c") for x in MESES}:
        return None
    return tipo, dia, mes, ano


COLS = ["tipo","numero","ocorrencias","status","slug","n_chars","sin_tdc","sin_iptu","sin_amb","sinal","ementa"]


def main():
    linhas = list(csv.DictReader(open(FILA, encoding="utf-8")))
    # incremental: já feitas (por numero) sobrevivem a corte
    feitas = set()
    if SAIDA.exists():
        for x in csv.DictReader(open(SAIDA, encoding="utf-8")):
            if x.get("status") == "ok":
                feitas.add((x["tipo"], x["numero"]))
    novo = not SAIDA.exists()
    f = open(SAIDA, "a", encoding="utf-8", newline="")
    w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
    if novo:
        w.writeheader(); f.flush()
    ok = tdc = 0
    for r in linhas:
        if (r["tipo"], r["numero"]) in feitas:
            ok += 1; continue
        info = slug_de(r["exemplo_nome"])
        if not info:
            w.writerow({**base_row(r), "status": "sem_data", "slug": ""}); f.flush(); continue
        tipo, dia, mes, ano = info
        # o portal EXIGE o dia com 2 dígitos no slug: `de-07-de-julho` funciona, `de-7-de-julho`
        # devolve só o shell do catálogo (bug que causou os 6 slug-fails da Etapa D — PU 22, 2026-07-19).
        slug = f"{tipo}-{r['numero']}-de-{dia:02d}-de-{mes}-de-{ano}"
        row = {**base_row(r), "slug": slug}
        try:
            raw, final = baixar(slug)
            texto, err = extrair_texto(raw)
        except Exception as e:
            w.writerow({**row, "status": f"erro:{type(e).__name__}"}); f.flush(); continue
        if err or not texto:
            w.writerow({**row, "status": "sem_texto"}); f.flush(); continue
        ementa = extrair_ementa(texto)
        ntdc, niptu, namb = len(SIN_TDC.findall(texto)), len(SIN_IPTU.findall(texto)), len(SIN_AMB.findall(texto))
        sinal = "tdc" if ntdc > niptu and ntdc > 0 else ("iptu" if niptu > 0 else ("ambiental" if namb > 0 else "outro"))
        w.writerow({**row, "status": "ok", "n_chars": len(texto), "sin_tdc": ntdc,
                    "sin_iptu": niptu, "sin_amb": namb, "sinal": sinal, "ementa": ementa[:280]})
        f.flush()
        ok += 1; tdc += (sinal == "tdc")
        print(f"  {r['tipo']:8s}{r['numero']:6s} [{sinal:9s} tdc={ntdc} iptu={niptu}] {ementa[:70]}", flush=True)
    f.close()
    print(f"\ntriagem: {ok} ok | sinal TDC={tdc} | saída: {SAIDA}")


def base_row(r):
    return {"tipo": r["tipo"], "numero": r["numero"], "ocorrencias": r["ocorrencias"]}


def extrair_ementa(texto):
    # a ementa é o 1º parágrafo longo antes de "RICARDO NUNES"/"Prefeito"/"Art. 1"
    corte = re.split(r'RICARDO NUNES|,\s*Prefeit|Art\.?\s*1[ºo]', texto)[0]
    paras = [p.strip() for p in corte.split("\n") if len(p.strip()) > 60]
    return paras[-1] if paras else (texto[:200].replace("\n", " "))


if __name__ == "__main__":
    sys.exit(main())
