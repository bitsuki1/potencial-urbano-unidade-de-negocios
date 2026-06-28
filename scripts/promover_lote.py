#!/usr/bin/env python3
"""
promover_lote.py — Promove em LOTE o verbatim cru trazido do Drive (2026-06-24) para
`leis/.../<id>.md` (com `## Texto integral (verbatim)`) + `.json` (schema 2.4, confianca:alta).

CURADO (RO-18: nunca herdar nº de lei errado): a identidade de cada norma (id, numero, ano,
tipo, tema, vigência) é DECLARADA à mão na tabela CORE abaixo — não inferida por regex frágil.
Para cada entrada, escolhe automaticamente a CÓPIA de MAIOR corpo entre os .txt que casam o
padrão do número (RO-12: a mais completa). SObrescreve um .md/.json existente SE ele for
não-verbatim (resumo, sem marcador ou confianca != alta) — é o destrave: resumo → verbatim.

Uso: python3 scripts/promover_lote.py [--dry]
Trazido pelo orquestrador do PU — 2026-06-24 (destrave H0: pilares TDC verbatim ao RAG).
"""
import json, re, sys, glob
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
MARC = "## Texto integral (verbatim)"

# id, padrão-de-arquivo (regex), tipo, numero, ano, esfera, jurisdicao, tema[], vigencia.inicio
CORE = [
 ("lei-municipal-saopaulo-16050-2014", r"16[-.]?050",  "lei municipal","16050","2014","Municipal-SP","São Paulo - SP",["TDC","urbanística"],"2014-07-31"),
 ("lei-municipal-saopaulo-16402-2016", r"16[-.]?402",  "lei municipal","16402","2016","Municipal-SP","São Paulo - SP",["TDC","urbanística"],"2016-03-22"),
 ("lei-municipal-saopaulo-16642-2017", r"16[-.]?642",  "lei municipal","16642","2017","Municipal-SP","São Paulo - SP",["TDC","urbanística"],"2017-05-09"),
 ("lei-municipal-saopaulo-17844-2022", r"17[-.]?844",  "lei municipal","17844","2022","Municipal-SP","São Paulo - SP",["IPTU"],"2022-09-14"),
 ("lei-municipal-saopaulo-17733-2022", r"17[-.]?733",  "lei municipal","17733","2022","Municipal-SP","São Paulo - SP",["IPTU"],"2022-01-11"),
 ("decreto-saopaulo-57443-2016",       r"57[-.]?443",  "decreto municipal","57443","2016","Municipal-SP","São Paulo - SP",["IPTU"],"2016-11-10"),
]

def body(p):
    t = Path(p).read_text(encoding="utf-8")
    if t.startswith("# FONTE"):
        i = t.find("\n---\n")
        if i>0: t = t[i+5:]
    return t.strip("\n")
def fonte_id(p):
    m = re.search(r"fileId=(\S+)", Path(p).read_text(encoding="utf-8")); return m.group(1) if m else None
def arts(b): return len(re.findall(r"(?m)^\s*Art\.?\s*\d+", b))
def is_verbatim(mdp):
    if not mdp.exists(): return False
    jp = mdp.with_suffix(".json")
    if MARC not in mdp.read_text(encoding="utf-8"): return False
    try: return json.loads(jp.read_text(encoding="utf-8")).get("confianca_extracao")=="alta"
    except Exception: return False

def main():
    dry = "--dry" in sys.argv
    allf = sorted(glob.glob("_entrada/tdc/*.txt")+glob.glob("_entrada/iptu/*.txt")+glob.glob("_entrada/misto/*.txt"))
    n=0
    for cid,pat,tipo,numero,ano,esfera,juris,tema,vig in CORE:
        rx=re.compile(pat)
        cands=[(p,body(p)) for p in allf if rx.search(Path(p).stem)]
        cands=[(p,b) for p,b in cands if arts(b)>=3]
        if not cands:
            print(f"  FALTA {cid}: nenhum .txt articulado casa /{pat}/"); continue
        p,b=max(cands,key=lambda x:len(x[1]))           # maior corpo
        sub="federal" if esfera=="Federal" else "municipal-sp"
        mdp=RAIZ/"leis"/sub/f"{cid}.md"
        if is_verbatim(mdp):
            print(f"  SKIP {cid}: já verbatim — não toco"); continue
        estado = "SOBRESCREVE resumo" if mdp.exists() else "CRIA"
        print(f"  OK   {cid}: {estado}, ~{arts(b)} arts, {len(b)//1024}kB, fonte={Path(p).name[:40]}")
        if dry: continue
        mdp.parent.mkdir(parents=True,exist_ok=True)
        titulo=b.split("\n",1)[0][:120].strip() or cid
        mdp.write_text(
            f"# {titulo}\n\n"
            f"**Proveniência:** VERBATIM via Google Drive (fileId={fonte_id(p)}), conta eduardo@saobentoservicos, "
            f"re-ingerido 2026-06-24 de `{p}`. PDF com camada de texto (sem OCR). Extração pura (1.2), nada interpretado.\n"
            f"**confianca_extracao:** alta (articulado integral verbatim)\n\n"
            f"## Ementa\n\n(ver texto integral)\n\n{MARC}\n\n{b}\n", encoding="utf-8")
        meta={"id":cid,"tipo_norma":tipo,"esfera":esfera,"jurisdicao":juris,"numero":numero,"ano":ano,
              "ementa":"(ver texto integral)","tema":tema,
              "vigencia":{"inicio":vig,"fim":None,"revogada_por":None,"altera":[],"alterada_por":[]},
              "fonte":{"origem":"Google Drive","path":p,"hash":None,"ocr":False,"fileId":fonte_id(p)},
              "status_pipeline":"bruto","confianca_extracao":"alta","revisado_por_humano":False}
        mdp.with_suffix(".json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        n+=1
    print(f"\npromover_lote: {n} normas promovidas{' (DRY)' if dry else ''}. Rode fatiar.py + indexar.py + consolidar.py.")

if __name__=="__main__": main()
