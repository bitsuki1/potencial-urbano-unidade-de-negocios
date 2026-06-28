#!/usr/bin/env python3
"""higienizar.py — fecho local da base (itens A3-A6). NAO inventa SQL.
- A4: extrai os SQL nao-normalizaveis das fontes -> fila de revisao (ancorada no endereco).
- A3: confere arredondamento de m2 na ferramenta.
- A6: conta datas ambiguas e fixa a convencao (BR p/ docs PMSP).
- A5: aponta o unico OCR suspeito (APC Borogodo).
Saida: zepec/limpo/_revisar_sql_invalido.csv + relatorio. PU 14 · 2026-06-28.
"""
import csv, re
from pathlib import Path
Z=Path(__file__).resolve().parent
L=lambda p: list(csv.reader(open(Z/"raw"/p,encoding='utf-8')))

def sql_ok(sq, lote):
    sqd=re.sub(r'\D','',sq or ''); return len(sqd)==6 and re.match(r'\d{4}',(lote or '').strip())
def sql_ok_dec(s,q,l):
    return len(re.sub(r'\D','',s or ''))==3 and len(re.sub(r'\D','',q or ''))==3 and re.match(r'\d{4}',(l or '').strip())

rev=[]
for r in L("lista_declaracoes_ZEPEC-BIR_agosto-2025.csv")[4:]:
    r=(r+['']*11)[:11]
    if not any(c.strip() for c in r): continue
    if r[2].strip() and not sql_ok(r[2],r[3]):
        rev.append(['DECLARACAO_BIR', r[2], r[3], r[4], r[5], r[1], ''])
for r in L("lista_certidao_ZEPEC-BIR_agosto-2025.csv")[5:]:
    r=(r+['']*19)[:19]
    if not any(c.strip() for c in r): continue
    if r[2].strip() and not sql_ok(r[2],r[3]):
        rev.append(['CERTIDAO_BIR_CEDENTE', r[2], r[3], r[4], r[5], r[1], ''])
for r in L("SIRGAS_SHP_benstombados1.csv")[1:]:
    r=(r+['']*30)[:30]
    if not any(c.strip() for c in r): continue
    if (r[1].strip() or r[2].strip()) and not sql_ok_dec(r[1],r[2],r[3]):  # tem setor/quadra mas nao fecha
        rev.append(['TOMBADO_CADASTRO', f"{r[1]}/{r[2]}/{r[3]}", r[3], r[8], r[24], r[26], r[0]])

with (Z/"limpo/_revisar_sql_invalido.csv").open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['origem','sq_ou_setor_quadra_lote_bruto','lote_bruto','endereco','distrito','n_processo','nome_bem'])
    w.writerows(rev)
print(f"A4 — fila de revisao SQL: {len(rev)} linhas -> zepec/limpo/_revisar_sql_invalido.csv (ancora = endereco; resolver por geo)")

# A3 — m2 arredondado na ferramenta?
fr=list(csv.reader(open(Z/"ferramenta/zepec_cedentes.csv",encoding='utf-8')))
fi={c:i for i,c in enumerate(fr[0])}
ruido=[r[fi['m2_ja_transferido']] for r in fr[1:] if r[fi['m2_ja_transferido']] and len(r[fi['m2_ja_transferido']].split('.')[-1])>2]
print(f"A3 — m2 com mais de 2 casas (ruido de float): {len(ruido)}  (0 = limpo)")

# A6 — datas
u=list(csv.reader(open(Z/"limpo/zepec_unificada.csv",encoding='utf-8'))); ui={c:i for i,c in enumerate(u[0])}
amb=sum(1 for r in u[1:] if r[ui['data_amb']]=='ambiguo')
print(f"A6 — datas ambiguas (dia e mes <=12): {amb}. CONVENCAO FIXADA: assume BR (dia/mes) — padrao de doc PMSP. Marcadas em data_amb.")
exemplo=[(r[ui['data_pub_raw']][:18], r[ui['data_pub_iso']]) for r in u[1:] if r[ui['data_amb']]=='ambiguo'][:4]
print("   amostra (raw -> iso):", exemplo)
print("A5 — OCR: 1 caso a revisar -> APC 'Bar O do Borogodo' (provavel 'Bar do Borogodo').")
