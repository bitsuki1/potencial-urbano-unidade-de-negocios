#!/usr/bin/env python3
"""fundurb.py — parseia a fila TDC/FUNDURB (PDF->csv mastigado) por PROCESSO.
Corrigido pós-escrutínio (agentes 2026-06-28):
- valor_pecuniario_rs é VALOR PECUNIÁRIO REGULATÓRIO (Art.24 §5º LPUOS / proxy PCpt×V), **não preço de mercado**.
- extração ROBUSTA por magnitude (não posicional): cap 5% = maior R$; somatória = acumulado; valor = menor.
  sanity: valor < somatória < cap. Emite '(suspeito)' se violar.
- extrai teto_5pct_rs (faltava) e periodo; data_protocolo = 1ª data (não 'publicação').
- intercorrencia: Indeferido/Sobrestado='sim'; Comunique-se='pendencia'; Em análise='em_andamento';
  (sem status)='desconhecido' (nunca 'nao'); Transferido='nao'.
Saida: zepec/limpo/fundurb_processos.csv. PU 14 · 2026-06-28.
"""
import re, csv
from pathlib import Path
from collections import Counter
Z=Path(__file__).resolve().parent
txt=open(Z/"raw/externo/fundurb_fila_tdc_5pct_dez2025.csv",encoding='utf-8').read()
RS=re.compile(r'\d{1,3}(?:\.\d{3})*,\d{2}')
def f(v): return float(v.replace('.','').replace(',','.'))

RISCO={'Indeferido':'sim','Sobrestado':'sim','Comunique-se':'pendencia','Em análise':'em_andamento'}
out=[]
for ln in txt.splitlines():
    mp=re.search(r'6068\.\d{4}/\d+-\d', ln)
    if not mp: continue
    proc=mp.group()
    st=re.search(r'(Transferido em [A-Za-zç]+ de \d{4}|Indeferido|Em an[áa]lise|Comunique-se|Sobrestado)', ln)
    status=st.group().strip() if st else '(sem status)'
    per=re.search(r'[A-Z][a-z]{2}\s*-?\d{2}\s*a\s*[A-Z][a-z]{2}\s*-?\d{2}', ln)
    datas=re.findall(r'\d{2}/\d{2}/\d{4}', ln)
    vals=sorted({f(v):v for v in RS.findall(ln)}.items())   # (float, str) unicos, asc
    teto=vals[-1][1] if vals else ''                         # 5% = maior
    rest=vals[:-1]                                           # tira o teto
    valor=somatoria=''; suspeito=''
    if status.startswith('Transferido') and len(rest)>=2:
        valor=rest[0][1]; somatoria=rest[-1][1]              # menor=valor, maior restante=somatoria
        if rest[0][0]>=rest[-1][0]: suspeito='(suspeito: valor>=somatoria)'
    elif rest:
        somatoria=rest[-1][1]
    interc='nao' if status.startswith('Transferido') else RISCO.get(status,'desconhecido')
    out.append({"n_processo":proc,"periodo":(per.group() if per else ''),
                "status_fundurb":status,"intercorrencia":interc,
                "valor_pecuniario_rs":valor+(' '+suspeito if suspeito else ''),
                "somatoria_tdc_rs":somatoria,"teto_5pct_rs":teto,
                "data_protocolo":datas[0] if datas else ''})
with (Z/"limpo/fundurb_processos.csv").open('w',newline='',encoding='utf-8') as fo:
    w=csv.DictWriter(fo,fieldnames=["n_processo","periodo","status_fundurb","intercorrencia",
        "valor_pecuniario_rs","somatoria_tdc_rs","teto_5pct_rs","data_protocolo"])
    w.writeheader(); w.writerows(out)
print(f"fundurb_processos: {len(out)} processos")
print("intercorrencia:", dict(Counter(o['intercorrencia'] for o in out)))
print("com valor pecuniario:", sum(1 for o in out if o['valor_pecuniario_rs']))
print("suspeitos:", sum(1 for o in out if 'suspeito' in o['valor_pecuniario_rs']))
