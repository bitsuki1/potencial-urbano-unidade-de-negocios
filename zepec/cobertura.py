#!/usr/bin/env python3
"""cobertura.py — fecha A1/A2 (vinculo declaracao<->certidao por imovel) e mede a COBERTURA
em % por dimensao. Tudo local, sobre zepec/ferramenta/zepec_cedentes.csv. PU 14 · 2026-06-28.
"""
import csv
from pathlib import Path
Z=Path(__file__).resolve().parent
rows=list(csv.reader(open(Z/"ferramenta/zepec_cedentes.csv",encoding='utf-8')))
i={c:k for k,c in enumerate(rows[0])}; H=rows[1:]; N=len(H)
g=lambda r,c: r[i[c]]

# --- A1/A2: vinculo (imovel com declaracao E certidao) ---
vinc=[r for r in H if g(r,'tem_declaracao')=='sim' and g(r,'tem_certidao')=='sim']
with (Z/"limpo/vinculo_por_imovel.csv").open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['sql_mestre','nome_bem','endereco_mestre','distrito',
        'estado_venda','m2_ja_transferido','n_transferencias','esgotado','data_ref'])
    for r in sorted(vinc,key=lambda r: float(g(r,'m2_ja_transferido') or 0),reverse=True):
        w.writerow([g(r,'sql_mestre'),g(r,'nome_bem'),g(r,'endereco_mestre'),g(r,'distrito'),
            g(r,'estado_venda'),g(r,'m2_ja_transferido'),g(r,'n_transferencias'),g(r,'esgotado'),g(r,'data_ref')])
print(f"A1/A2 — vinculo declaracao<->certidao: {len(vinc)} imoveis ligados -> zepec/limpo/vinculo_por_imovel.csv\n")

def pct(n): return f"{n:5d}  {100*n/N:5.1f}%"
print(f"COBERTURA (base = {N} imoveis da ferramenta)\n" + "-"*52)
dims=[
 ("Identificado com SQL_MESTRE", sum(1 for r in H if g(r,'sql_mestre'))),
 ("Endereco estruturado (com tipo)", sum(1 for r in H if g(r,'endereco_mestre') and g(r,'tipo_zepec'))),
 ("Distrito preenchido", sum(1 for r in H if g(r,'distrito'))),
 ("Data de referencia", sum(1 for r in H if g(r,'data_ref'))),
 ("Tipo ZEPEC (BIR/APC/tombado)", sum(1 for r in H if g(r,'tipo_zepec'))),
 ("Estado de venda definido (nao INCERTO)", sum(1 for r in H if g(r,'estado_venda')!='INCERTO')),
 ("Negociabilidade classificada (sim/nao/verif.)", N),
 ("Negociavel = sim (com base p/ agir)", sum(1 for r in H if g(r,'negociavel')=='sim')),
 ("Historico de venda (m2 transferido)", sum(1 for r in H if g(r,'m2_ja_transferido'))),
 ("Vinculo declaracao<->certidao", len(vinc)),
 ("Proprietario (dono)", 0),
 ("Atc / preco (engine)", 0),
]
for nome,n in dims: print(f"  {nome:46} {pct(n)}")

print("\nQUALIDADE por estado de venda:")
from collections import Counter
for k,v in Counter(g(r,'estado_venda') for r in H).most_common():
    print(f"  {k:14} {v:5}  {100*v/N:5.1f}%")
print("\nNEGOCIAVEL:")
for k,v in Counter(g(r,'negociavel') for r in H).most_common():
    print(f"  {k:10} {v:5}  {100*v/N:5.1f}%")
