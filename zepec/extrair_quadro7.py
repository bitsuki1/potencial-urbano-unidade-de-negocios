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

# achados do escrutinio: GUAIANASES usa PQ_G_NN (1 letra) e 5 codigos usam hifen -> aceitar [_-] e 1-3 letras
COD=re.compile(r'PQ[_-][A-Z]{1,3}[_-]\d{1,3}')
# situacao: PDF quebra o token "EM PLANEJAMENTO" no salto de pagina -> casar sem exigir "EM"
SIT=re.compile(r'PLANEJAMENTO|IMPLANTA[CÇ][AÃ]O|EXISTENTE')
CAT=re.compile(r'\b(LINEAR|URBANO|NATURAL|LINEAR/URBANO)\b')
# fatia por código
pos=[(m.start(),m.group()) for m in COD.finditer(txt)]
recs=[]
for i,(p,cod) in enumerate(pos):
    fim=pos[i+1][0] if i+1<len(pos) else len(txt)
    bloco=txt[p+len(cod):fim].strip()
    ms=SIT.search(bloco)
    if ms:
        local=bloco[:ms.start()].strip().rstrip('/ ').removesuffix(' EM').strip()
        resto=bloco[ms.end():].strip().lstrip('/ ').strip()
        mc=CAT.match(resto) or CAT.search(resto[:20])
        cat=mc.group() if mc else ''
        end=resto[mc.end():].strip() if mc else resto
        key=ms.group().upper()
        sit='EM PLANEJAMENTO' if key.startswith('PLAN') else ('EM IMPLANTAÇÃO' if key.startswith('IMPLANT') else 'EXISTENTE')
    else:
        local, sit, cat, end = bloco, '', '', ''
    recs.append({"codigo":cod,"situacao":sit,"categoria":cat,
                 "proposto":"sim" if sit and sit!="EXISTENTE" else ("nao" if sit=="EXISTENTE" else ""),
                 "revisar":"" if sit else "sem situacao na fonte (PDF) — conferir manual",
                 "local_bruto":local[:300],"endereco_bruto":end[:300]})
with (Z.parent/"tabelas/quadro7-parques.csv").open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=["codigo","situacao","categoria","proposto","revisar","local_bruto","endereco_bruto"])
    w.writeheader(); w.writerows(recs)
from collections import Counter
print(f"quadro7-parques.csv: {len(recs)} parques")
print("situacao:", dict(Counter(r['situacao'] or '(vazio)' for r in recs)))
print("PROPOSTOS (alvo da doacao):", sum(1 for r in recs if r['proposto']=='sim'))
