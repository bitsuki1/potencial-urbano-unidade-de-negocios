#!/usr/bin/env python3
"""lista_prospeccao.py — o DELIVERABLE comercial: a partir da ferramenta, separa o que está
PRONTO PARA PROSPECTAR do que vai para CONFERÊNCIA, em buckets FACTUAIS (sem juízo de valor).
- lista_prospeccao.csv  = negociavel=sim, segmentado por estado de venda × tem dono.
- fila_verificar.csv     = negociavel=verificar (não excluído — conferir antes).
Os negociavel=nao (esgotado/vedado, prova escrita) ficam de fora (com motivo).
Ordem = estágio do funil (INTACTO→TEM_SALDO→SO_ELEGIVEL), depois distrito — NÃO é ranking de qualidade.
PU 14 · 2026-06-28.
"""
import csv
from pathlib import Path
from collections import Counter
Z=Path(__file__).resolve().parent
H=list(csv.DictReader(open(Z/"ferramenta/zepec_cedentes.csv",encoding='utf-8')))

COLS=["segmento","estado_venda","nome_bem","endereco_mestre","distrito","proprietario",
      "tipo_zepec","esfera","m2_ja_transferido","status_fundurb","intercorrencia_fundurb","data_ref","sql_mestre"]
ORD={"INTACTO":0,"TEM_SALDO":1,"SO_ELEGIVEL":2,"INCERTO":3}

def linha(r):
    seg=f"{r['estado_venda']}·{'com dono' if r['proprietario'] else 'sem dono'}"
    return {c:(seg if c=="segmento" else r.get(c,"")) for c in COLS}

def chave(r):
    return (ORD.get(r['estado_venda'],9), 0 if r['proprietario'] else 1, r['distrito'], r['nome_bem'])

# prospeccao = negociavel=sim E identificavel (estado != INCERTO). INCERTO (sem SQL/dono) -> verificar/identificar (achado da lente)
prospec=sorted([r for r in H if r['negociavel']=='sim' and r['estado_venda']!='INCERTO'], key=chave)
verif  =sorted([r for r in H if r['negociavel']=='verificar' or (r['negociavel']=='sim' and r['estado_venda']=='INCERTO')], key=chave)

def grava(nome, rows):
    with (Z/"ferramenta"/nome).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(linha(r) for r in rows)

grava("lista_prospeccao.csv", prospec)
grava("fila_verificar.csv", verif)

def _seg(r): return f"{r['estado_venda']}·{'com dono' if r['proprietario'] else 'sem dono'}"
print(f"lista_prospeccao.csv: {len(prospec)} imoveis (negociavel=sim)")
print("  por segmento:", dict(Counter(_seg(r) for r in prospec)))
print(f"fila_verificar.csv: {len(verif)} imoveis (negociavel=verificar)")
print(f"fora (negociavel=nao, prova): {sum(1 for r in H if r['negociavel']=='nao')}")
