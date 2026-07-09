#!/usr/bin/env python3
"""lista_prospeccao.py — o DELIVERABLE comercial: a partir da ferramenta ENRIQUECIDA,
separa o que está PRONTO PARA PROSPECTAR do que vai para CONFERÊNCIA, em buckets FACTUAIS.
- lista_prospeccao.csv  = negociavel=sim, segmentado por estado de venda × tem dono.
- fila_verificar.csv     = negociavel=verificar (não excluído — conferir antes).
Os negociavel=nao (esgotado/vedado, prova escrita) ficam de fora (com motivo).
Ordem = estágio do funil (INTACTO→TEM_SALDO→SO_ELEGIVEL), depois distrito — NÃO é ranking de qualidade.
PU 14 · 2026-06-28 · costura B-20 (PU 18, 2026-07-09): lê da base OFICIAL (pós-enriquecimento).
"""
import csv, sys
from pathlib import Path
from collections import Counter
Z=Path(__file__).resolve().parent
_OFICIAL=Z/"ferramenta/zepec_cedentes_oficial.csv"
_BASE=Z/"ferramenta/zepec_cedentes.csv"
if _OFICIAL.exists():
    H=list(csv.DictReader(open(_OFICIAL,encoding='utf-8')))
else:
    print(f"AVISO: {_OFICIAL.name} não encontrado — usando base sem enriquecimento.", file=sys.stderr)
    H=list(csv.DictReader(open(_BASE,encoding='utf-8')))

COLS=["segmento","estado_venda","nome_bem","endereco_mestre","distrito","proprietario",
      "tipo_zepec","esfera","m2_ja_transferido","pcpt_m2","saldo_pcpt_m2","preco_proxy_brl",
      "zona","ca_basico","fi_aplicado","regime_pcpt","qualidade_estimativa",
      "area_terreno_m2","v_outorga_m2_q14","pendencia_calculo",
      "status_fundurb","intercorrencia_fundurb","data_ref","sql_mestre"]
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
