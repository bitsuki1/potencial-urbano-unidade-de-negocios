#!/usr/bin/env python3
"""Agrega todos os catalogo-*.csv num mestre com cabeçalho, marca duplicatas, e emite:
- CATALOGO-DRIVE-PU-2026-07-12.csv (mestre único, dedup por drive_id, com colunas dup_grupo/descarte)
- APAGAR-DE-PARA.csv (drive_ids candidatos à pasta APAGAR: descarte + duplicatas exatas)
- RELATORIO-CATALOGO.md (números)
"""
import csv, glob, os, collections, hashlib
BASE=os.path.dirname(os.path.abspath(__file__))
HDR=["drive_id","path","nome","mime","ext","bytes","created","modified","tema","tipo_artefato","oficialidade","ja_indexado","observacao","fonte_csv"]
rows={}
for f in sorted(glob.glob(os.path.join(BASE,"catalogo-*.csv"))):
    fonte=os.path.basename(f)
    with open(f, encoding="utf-8") as fh:
        r=csv.reader(fh)
        for row in r:
            if not row or row[0]=="drive_id": continue
            row=row[:13]+[""]*(13-len(row))
            did=row[0]
            if did and did not in rows:
                rows[did]=row[:13]+[fonte]
# marca descarte (path/fonte de pasta 99/lixeira/quarentena/deletar)
def is_descarte(row):
    s=(row[1]+" "+row[13]).lower()
    return any(k in s for k in ["99_lixeira","99_quarentena","99_para_deletar","99paradeletar","99quarentena","99lixeira","descarte","duplicad"])
# grupos de duplicata por (nome_base_normalizado, bytes)
import re
def base(n):
    n=n.lower()
    n=re.sub(r"\s*\(\d+\)","",n)  # remove (1),(2)
    n=re.sub(r"[ _]+"," ",n).strip()
    return n
grp=collections.defaultdict(list)
for did,row in rows.items():
    grp[(base(row[2]), row[5])].append(did)
dupset=set()
for k,ids in grp.items():
    if len(ids)>1 and k[1] and k[1].isdigit():  # mesmo nome-base E mesmo tamanho = duplicata forte
        for did in ids[1:]: dupset.add(did)  # mantém a 1ª, marca resto
# escreve mestre
with open(os.path.join(BASE,"..","CATALOGO-DRIVE-PU-2026-07-12.csv"),"w",encoding="utf-8",newline="") as out:
    w=csv.writer(out); w.writerow(HDR+["descarte","dup_forte"])
    for did,row in sorted(rows.items(), key=lambda x:x[1][1]):
        w.writerow(row+["SIM" if is_descarte(row) else "","SIM" if did in dupset else ""])
# de-para APAGAR = descarte OU dup_forte
apagar=[(did,rows[did][2],rows[did][1]) for did in rows if is_descarte(rows[did]) or did in dupset]
with open(os.path.join(BASE,"APAGAR-DE-PARA.csv"),"w",encoding="utf-8",newline="") as out:
    w=csv.writer(out); w.writerow(["drive_id","nome","path_origem","motivo"])
    for did,nome,path in apagar:
        motivo="descarte" if is_descarte(rows[did]) else "duplicata_forte"
        w.writerow([did,nome,path,motivo])
# relatório
tot=len(rows); desc=sum(1 for d in rows if is_descarte(rows[d])); dup=len(dupset)
tipo=collections.Counter(rows[d][9] for d in rows); tema=collections.Counter(rows[d][8] for d in rows)
idx=collections.Counter(rows[d][11] for d in rows)
print(f"TOTAL_UNICO={tot}")
print(f"DESCARTE={desc}  DUP_FORTE={dup}  APAGAR_TOTAL={len(apagar)}")
print(f"ja_indexado: {dict(idx)}")
print("tipo:", dict(tipo.most_common()))
print("tema:", dict(tema.most_common()))
