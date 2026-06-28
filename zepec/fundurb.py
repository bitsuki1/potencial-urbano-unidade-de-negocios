#!/usr/bin/env python3
"""fundurb.py — parseia a fila TDC/FUNDURB (PDF->csv mastigado) por PROCESSO.
Disciplina: STATUS é fato limpo (intercorrência); valor transferido só quando inequívoco
(status 'Transferido' e >=3 valores R$ -> penúltimo = valor; último = somatória).
Saida: zepec/limpo/fundurb_processos.csv. PU 14 · 2026-06-28.
"""
import re, csv
from pathlib import Path
Z=Path(__file__).resolve().parent
txt=open(Z/"raw/externo/fundurb_fila_tdc_5pct_dez2025.csv",encoding='utf-8').read()
RS=re.compile(r'\d{1,3}(?:\.\d{3})*,\d{2}')
out=[]
for ln in txt.splitlines():
    mp=re.search(r'6068\.\d{4}/\d+-\d', ln)
    if not mp: continue
    proc=mp.group()
    st=re.search(r'(Transferido em [A-Za-zç]+ de \d{4}|Indeferido|Em an[áa]lise|Comunique-se|Sobrestado)', ln)
    status=st.group().strip() if st else ''
    datas=re.findall(r'\d{2}/\d{2}/\d{4}', ln)
    vals=RS.findall(ln)
    valor_transf=''; somatoria=''
    if status.startswith('Transferido') and len(vals)>=3:
        valor_transf=vals[-2]; somatoria=vals[-1]
    elif vals:
        somatoria=vals[-1]
    # classifica intercorrencia
    risco = 'sim' if status in ('Indeferido','Sobrestado') else ('em_andamento' if status in ('Em análise','Em análise','Comunique-se') else 'nao')
    out.append({"n_processo":proc,"status_fundurb":status or '(sem status)',
                "intercorrencia":risco,"valor_transferido_rs":valor_transf,
                "somatoria_tdc_rs":somatoria,"data_pub":datas[0] if datas else ''})
with (Z/"limpo/fundurb_processos.csv").open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=["n_processo","status_fundurb","intercorrencia","valor_transferido_rs","somatoria_tdc_rs","data_pub"])
    w.writeheader(); w.writerows(out)
from collections import Counter
print(f"fundurb_processos: {len(out)} processos")
print("status:", dict(Counter(o['status_fundurb'][:18] for o in out)))
print("intercorrencia:", dict(Counter(o['intercorrencia'] for o in out)))
print("com valor transferido (R$):", sum(1 for o in out if o['valor_transferido_rs']))
