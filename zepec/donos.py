#!/usr/bin/env python3
"""donos.py — camada de TITULARIDADE: cruza fontes externas (por SQL) com nosso universo e
produz zepec/limpo/donos_encontrados.csv (sql_mestre -> proprietario, area_terreno, fonte).
Extensivel: adicione fontes em SOURCES. So fato; sem juizo. PU 14 · 2026-06-28.
"""
import csv, re
from pathlib import Path
Z=Path(__file__).resolve().parent
def split_lotes(s):
    """Separa multi-lote: , ; ' e ' e '/' SOMENTE quando seguido de lote de 4 dig
    (protege DV tipo '0021/4'). Achado dos agentes: OODC usa '/' p/ multi-lote."""
    s=(s or '').strip()
    if not s: return []
    parts=re.split(r'[;,]| e |/(?=\s*\d{4})', s)
    return [p.strip() for p in parts if re.search(r'\d', p)]

def keys_single(sqstr):
    """SQ num campo unico tipo '172.393.0010-1' -> chave 10 dig (setor3+quadra3+lote4).
    Guarda: rejeita se <10 digitos (evita chave deslocada por zero perdido)."""
    d=re.sub(r'\D','',sqstr or '')
    return [d[:10]] if len(d) in (10,11) else []

def keys_parts(se,qu,lo):
    """setor/quadra/lote separados (OODC). Explode multi-lote -> 1 chave por lote."""
    s=re.sub(r'\D','',se or ''); q=re.sub(r'\D','',qu or '')
    if len(s)!=3 or len(q)!=3: return []
    out=[]
    for part in split_lotes(lo):
        m=re.match(r'(\d{4})', part.strip())
        if m: out.append(s+q+m.group(1))
    return out

# (arquivo, linha_cabecalho, col_sql (int OU tupla setor,quadra,lote), col_dono, col_atc, col_end|None, fonte)
SOURCES=[
    ("raw/externo/ANUAL-2022.csv",       0, 7,        13, 14, 15,   "ANUAL-2022 (alvaras)"),
    ("raw/externo/sissel_ANO_2024.csv", 10, 22,       32, 33, 34,   "SISSEL-2024 (processos)"),
    ("raw/externo/OODC_2024-2025.csv",   0, (6,7,8),  19, 58, None,  "OODC-2024-2025 (outorga)"),
]
donos={}; conflitos=0   # sql -> dict
for arq,hr,cs,cd,ca,ce,fonte in SOURCES:
    p=Z/arq
    if not p.exists(): continue
    for r in list(csv.reader(open(p,encoding='utf-8')))[hr+1:]:
        need=max([cd,ca]+([cs] if isinstance(cs,int) else list(cs))+([ce] if ce is not None else []))
        if len(r)<=need: continue
        ks=keys_parts(r[cs[0]],r[cs[1]],r[cs[2]]) if isinstance(cs,tuple) else keys_single(r[cs])
        dono=r[cd].strip()
        if not ks or not dono: continue
        for k in ks:
            if k in donos and donos[k]['proprietario']!=dono: conflitos+=1
            donos.setdefault(k, {"proprietario":dono,"area_terreno":r[ca].strip(),
                                 "endereco_fonte":(r[ce].strip() if ce is not None else ''),"fonte_dono":fonte})

with (Z/"limpo/donos_encontrados.csv").open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['sql_mestre','proprietario','area_terreno','endereco_fonte','fonte_dono'])
    for k,v in donos.items():
        w.writerow([k,v['proprietario'],v['area_terreno'],v['endereco_fonte'],v['fonte_dono']])

# cobertura sobre cedentes
ced=list(csv.reader(open(Z/"ferramenta/zepec_cedentes.csv",encoding='utf-8')))
ci={c:i for i,c in enumerate(ced[0])}
cedsq=set(r[ci['sql_mestre']] for r in ced[1:] if r[ci['sql_mestre']])
match=cedsq & set(donos)
print(f"donos_encontrados: {len(donos)} SQL com dono (fontes: {len(SOURCES)}); conflitos de dono ignorados: {conflitos}")
print(f"cobertura sobre cedentes com SQL ({len(cedsq)}): {len(match)} = {100*len(match)/max(len(cedsq),1):.1f}%")
