#!/usr/bin/env python3
"""extrair_quadro7.py — extrai o Quadro 7 do PDE (parques existentes/propostos) do TXT de PDF
mastigado para tabelas/quadro7-parques.csv. Substrato da VIA DE EXPANSÃO 'parques' (Art.126 IV,
doação). Âncoras confiáveis: código PQ_XX_NN, situação, categoria. `local_bruto` (subpref+distrito+
nome) e endereço saem do PDF e ficam como BRUTO (a refinar). Extração pura, sem inventar.
PU 14 · 2026-06-28.
"""
import re, csv
from pathlib import Path
Z=Path(__file__).resolve().parent
raw=open(Z.parent/"_entrada/tdc/pde2013-subst2-quadro-7-parques-municipais-existentes-propostos.txt",encoding='utf-8').read()
# corta cabeçalho até a linha de colunas
raw=raw.split("CODIGO SUBPREFEITURA DISTRITO NOME SITUAÇÃO CATEGORIA ENDEREÇO",1)[-1]
txt=re.sub(r'\s+',' ', raw).strip()

COD=re.compile(r'PQ_[A-Z]{2}_\d{2,3}')
SIT=re.compile(r'EM PLANEJAMENTO|EM IMPLANTACAO|EM IMPLANTAÇÃO|EXISTENTE')
CAT=re.compile(r'\b(LINEAR|URBANO|NATURAL|LINEAR/URBANO)\b')
# fatia por código
pos=[(m.start(),m.group()) for m in COD.finditer(txt)]
recs=[]
for i,(p,cod) in enumerate(pos):
    fim=pos[i+1][0] if i+1<len(pos) else len(txt)
    bloco=txt[p+len(cod):fim].strip()
    ms=SIT.search(bloco)
    if ms:
        local=bloco[:ms.start()].strip()
        resto=bloco[ms.end():].strip()
        mc=CAT.match(resto) or CAT.search(resto[:20])
        cat=mc.group() if mc else ''
        end=resto[mc.end():].strip() if mc else resto
        sit=ms.group().replace('IMPLANTACAO','IMPLANTAÇÃO')
    else:
        local, sit, cat, end = bloco, '', '', ''
    recs.append({"codigo":cod,"situacao":sit,"categoria":cat,
                 "proposto":"sim" if sit and sit!="EXISTENTE" else ("nao" if sit=="EXISTENTE" else ""),
                 "local_bruto":local[:120],"endereco_bruto":end[:120]})
with (Z.parent/"tabelas/quadro7-parques.csv").open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=["codigo","situacao","categoria","proposto","local_bruto","endereco_bruto"])
    w.writeheader(); w.writerows(recs)
from collections import Counter
print(f"quadro7-parques.csv: {len(recs)} parques")
print("situacao:", dict(Counter(r['situacao'] or '(vazio)' for r in recs)))
print("PROPOSTOS (alvo da doacao):", sum(1 for r in recs if r['proposto']=='sim'))
