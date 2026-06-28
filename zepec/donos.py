#!/usr/bin/env python3
"""donos.py — camada de TITULARIDADE: cruza fontes externas (por SQL) com nosso universo e
produz zepec/limpo/donos_encontrados.csv (sql_mestre -> proprietario, area_terreno, fonte).
Extensivel: adicione fontes em SOURCES. So fato; sem juizo. PU 14 · 2026-06-28.
"""
import csv, re
from pathlib import Path
Z=Path(__file__).resolve().parent
def sm(s):
    d=re.sub(r'\D','',s or ''); return d[:10] if len(d)>=10 else ''

# (arquivo, linha_cabecalho, col_sql, col_dono, col_atc, col_end, nome_fonte)
SOURCES=[
    ("raw/externo/ANUAL-2022.csv", 0, 7, 13, 14, 15, "ANUAL-2022 (alvaras)"),
]
donos={}   # sql -> dict
for arq,hr,cs,cd,ca,ce,fonte in SOURCES:
    p=Z/arq
    if not p.exists(): continue
    rows=list(csv.reader(open(p,encoding='utf-8')))[hr+1:]
    for r in rows:
        if len(r)<=max(cs,cd,ca,ce): continue
        k=sm(r[cs]); dono=r[cd].strip()
        if not k or not dono: continue
        donos.setdefault(k, {"proprietario":dono,"area_terreno":r[ca].strip(),
                             "endereco_fonte":r[ce].strip(),"fonte_dono":fonte})

with (Z/"limpo/donos_encontrados.csv").open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['sql_mestre','proprietario','area_terreno','endereco_fonte','fonte_dono'])
    for k,v in donos.items():
        w.writerow([k,v['proprietario'],v['area_terreno'],v['endereco_fonte'],v['fonte_dono']])

# cobertura sobre cedentes
ced=list(csv.reader(open(Z/"ferramenta/zepec_cedentes.csv",encoding='utf-8')))
ci={c:i for i,c in enumerate(ced[0])}
cedsq=set(r[ci['sql_mestre']] for r in ced[1:] if r[ci['sql_mestre']])
match=cedsq & set(donos)
print(f"donos_encontrados: {len(donos)} SQL com dono (fontes: {len(SOURCES)})")
print(f"cobertura sobre cedentes com SQL ({len(cedsq)}): {len(match)} = {100*len(match)/max(len(cedsq),1):.1f}%")
