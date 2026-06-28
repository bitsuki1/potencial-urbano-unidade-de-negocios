#!/usr/bin/env python3
"""montar_base.py — ETAPA 1-3 das ZEPEC: junta as 4 fontes oficiais COM TAG,
canoniza SQL -> SQL_MESTRE (10 dig, decomposto, DV a parte) e estrutura o ENDERECO
no padrao (CODEX §3). Agnostico: so fato, sem juizo. Multi-lote por celula é EXPLODIDO
(1 linha = 1 imovel/SQL_MESTRE). Campos relacionais (vinculo/saldo/potencial) ficam
A OBSERVAR (carregados crus num campo, nao resolvidos).
Entrada: zepec/raw/*.csv   Saida: zepec/limpo/zepec_unificada.csv + relatorio no stdout.
PU 14 · 2026-06-28.
"""
import csv, re, sys
from pathlib import Path
from collections import Counter
RAW = Path(__file__).resolve().parent / "raw"
OUT = Path(__file__).resolve().parent / "limpo"; OUT.mkdir(exist_ok=True)

TIPOS = {  # abreviacao do logradouro -> canonico (DNE)
    'r':'Rua','rua':'Rua','av':'Avenida','avenida':'Avenida','pç':'Praça','pc':'Praça',
    'praça':'Praça','praca':'Praça','pça':'Praça','al':'Alameda','alameda':'Alameda',
    'largo':'Largo','lgo':'Largo','lg':'Largo','estr':'Estrada','estrada':'Estrada',
    'vd':'Viaduto','viaduto':'Viaduto','tv':'Travessa','travessa':'Travessa',
    'pateo':'Pátio','páteo':'Pátio','patio':'Pátio','pátio':'Pátio','pq':'Parque',
    'rod':'Rodovia','rodovia':'Rodovia','pte':'Ponte','vl':'Vila','via':'Via',
}
def norm_sql(sq, lote):
    """sq=6dig setor+quadra ; lote pode ter DV (0054-2). Retorna (sql_mestre,setor,quadra,lote,dv,status)."""
    sqd = re.sub(r'\D','',sq or '')
    lz = (lote or '').strip()
    m = re.match(r'(\d{4})\s*-?\s*(\d)?', lz)
    if len(sqd) == 6 and m:
        setor,quadra = sqd[:3],sqd[3:6]
        lt = m.group(1); dv = m.group(2) or ''
        return setor+quadra+lt, setor, quadra, lt, dv, 'ok'
    return '', '', '', '', '', ('ausente' if not sqd else 'invalido')

def norm_sql_decomp(setor,quadra,lote):
    s=re.sub(r'\D','',setor or ''); q=re.sub(r'\D','',quadra or '')
    m=re.match(r'(\d{4})\s*-?\s*(\d)?',(lote or '').strip())
    if len(s)==3 and len(q)==3 and m:
        return s+q+m.group(1), s, q, m.group(1), (m.group(2) or ''), 'ok'
    # nada de setor/quadra/lote = tombado sem SQL cadastral na fonte (bairro/monumento)
    if not s and not q and not (lote or '').strip():
        return '','','','','', 'ausente'
    return '','','','','', 'invalido'

def split_lotes(lote):
    """Multi-lote numa celula -> lista. Reconhece '0090-2, 0496-7' etc."""
    if not lote: return ['']
    parts = re.split(r'[;,]| e ', lote)
    parts = [p.strip() for p in parts if re.search(r'\d', p)]
    return parts or [lote.strip()]

def norm_endereco(raw):
    raw = (raw or '').strip()
    if not raw: return '', '', '', '', 0
    antes = raw.split(',')[0].strip()
    toks = antes.split()
    tipo, logr = '', antes
    if toks:
        cand = toks[0].lower().strip('.')
        if cand in TIPOS:
            tipo = TIPOS[cand]; logr = ' '.join(toks[1:]).strip()
    nums = re.findall(r'\b\d+[A-Za-z]?\b', raw.split(',',1)[1]) if ',' in raw else []
    multi = 1 if ('/' in raw or re.search(r'\bR\b|\bAv\b|\bAl\b', raw[3:])) else 0
    mestre = f"{tipo} {logr}".strip()
    if nums: mestre += ", " + ", ".join(nums)
    return mestre, tipo, logr, "; ".join(nums), multi

COLS = ['origem','tipo_zepec','esfera','sql_mestre','setor','quadra','lote','dv','sql_status',
        'endereco_mestre','end_tipo','end_logradouro','end_numeros','end_multi','end_raw',
        'distrito','nome_bem','n_declaracao','n_processo','ato_conservacao','zepec_cod',
        'ano','situacao','status_declaracao','obs_a_observar','fonte_arquivo']

def main():
    out=[]; rel=Counter()
    L=lambda p: list(csv.reader(open(RAW/p,encoding='utf-8')))

    # 1) DECLARACOES (cabecalho linha 3; col-lider vazia)
    dec=L("lista_declaracoes_ZEPEC-BIR_agosto-2025.csv")
    for r in dec[4:]:
        if not any(c.strip() for c in r): continue
        r=(r+['']*11)[:11]
        for lt in split_lotes(r[3]):
            sm,se,qu,lo,dv,st=norm_sql(r[2],lt)
            em,et,el,en,mu=norm_endereco(r[4])
            out.append(dict(origem='DECLARACAO_BIR',tipo_zepec='BIR',esfera='municipal',
                sql_mestre=sm,setor=se,quadra=qu,lote=lo,dv=dv,sql_status=st,
                endereco_mestre=em,end_tipo=et,end_logradouro=el,end_numeros=en,end_multi=mu,end_raw=r[4],
                distrito=r[5],nome_bem='',n_declaracao=r[6],n_processo=r[1],ato_conservacao='',zepec_cod='',
                ano=r[8],situacao=r[9],status_declaracao=r[10],
                obs_a_observar='', fonte_arquivo='lista_declaracoes_ZEPEC-BIR'))
            rel['declaracao_linhas']+=1
            if st!='ok': rel['decl_sql_'+st]+=1
            if len(split_lotes(r[3]))>1: rel['decl_multilote_explodido']+=1

    # 2) CERTIDOES — lado CEDENTE (cabecalho linha 4; col-lider vazia)
    cer=L("lista_certidao_ZEPEC-BIR_agosto-2025.csv")
    for r in cer[5:]:
        if not any(c.strip() for c in r): continue
        r=(r+['']*19)[:19]
        if not r[2].strip() and not r[4].strip(): continue
        for lt in split_lotes(r[3]):
            sm,se,qu,lo,dv,st=norm_sql(r[2],lt)
            em,et,el,en,mu=norm_endereco(r[4])
            out.append(dict(origem='CERTIDAO_BIR_CEDENTE',tipo_zepec='BIR',esfera='municipal',
                sql_mestre=sm,setor=se,quadra=qu,lote=lo,dv=dv,sql_status=st,
                endereco_mestre=em,end_tipo=et,end_logradouro=el,end_numeros=en,end_multi=mu,end_raw=r[4],
                distrito=r[5],nome_bem='',n_declaracao=r[6],n_processo=r[1],ato_conservacao=r[7],zepec_cod='',
                ano='',situacao=r[18],status_declaracao='',
                obs_a_observar=f"saldo/area cedida e vinculo declaracao->certidao A OBSERVAR (certidao {r[12]})",
                fonte_arquivo='lista_certidao_ZEPEC-BIR'))
            rel['certidao_cedente_linhas']+=1
            if st!='ok': rel['cert_sql_'+st]+=1

    # 3) BENSTOMBADOS (setor/quadra/lote separados)
    bt=L("SIRGAS_SHP_benstombados1.csv")
    for r in bt[1:]:
        if not any(c.strip() for c in r): continue
        r=(r+['']*30)[:30]
        nc=lambda v: '' if v.strip() in ('não consta','nao consta','-') else v.strip()
        esf=['municipal'] if nc(r[5]) else []
        if nc(r[6]): esf.append('estadual')
        if nc(r[7]): esf.append('federal')
        sm,se,qu,lo,dv,stt=norm_sql_decomp(r[1],r[2],r[3])
        em,et,el,en,mu=norm_endereco(r[8])
        out.append(dict(origem='TOMBADO_CADASTRO',tipo_zepec='tombado',esfera='+'.join(esf) or '',
            sql_mestre=sm,setor=se,quadra=qu,lote=lo,dv=dv,sql_status=stt,
            endereco_mestre=em,end_tipo=et,end_logradouro=el,end_numeros=en,end_multi=mu,end_raw=r[8],
            distrito=nc(r[24]),nome_bem=r[0],n_declaracao='',n_processo=nc(r[26]),ato_conservacao=nc(r[5]),
            zepec_cod=nc(r[12]),ano=nc(r[15]),situacao=nc(r[22]),status_declaracao=nc(r[23]),
            obs_a_observar='', fonte_arquivo='SIRGAS_SHP_benstombados1'))
        rel['tombado_linhas']+=1
        if stt!='ok': rel['tomb_sql_'+stt]+=1

    # 4) ZEPEC-APC (sem SQL)
    ap=L("SIRGAS_SHP_ZEPEC1_apc.csv")
    for r in ap[1:]:
        if not any(c.strip() for c in r): continue
        r=(r+['']*9)[:9]
        em,et,el,en,mu=norm_endereco(r[2])
        out.append(dict(origem='ZEPEC_APC',tipo_zepec='APC',esfera='municipal',
            sql_mestre='',setor='',quadra='',lote='',dv='',sql_status='ausente',
            endereco_mestre=em,end_tipo=et,end_logradouro=el,end_numeros=en,end_multi=mu,end_raw=r[2],
            distrito='',nome_bem=r[3],n_declaracao='',n_processo=r[1],ato_conservacao='',zepec_cod='',
            ano=r[0],situacao=r[8],status_declaracao='',
            obs_a_observar='APC sem SQL na fonte — resolver SQL por endereco (enriquecimento externo)',
            fonte_arquivo='SIRGAS_SHP_ZEPEC1_apc'))
        rel['apc_linhas']+=1

    with (OUT/"zepec_unificada.csv").open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(out)

    print(f"SAIDA: zepec/limpo/zepec_unificada.csv — {len(out)} linhas")
    print("Por origem:", dict(Counter(o['origem'] for o in out)))
    print("SQL ok:", sum(1 for o in out if o['sql_status']=='ok'),
          "| ausente:", sum(1 for o in out if o['sql_status']=='ausente'),
          "| invalido:", sum(1 for o in out if o['sql_status']=='invalido'))
    print("Endereco com tipo reconhecido:", sum(1 for o in out if o['end_tipo']),
          "| sem tipo:", sum(1 for o in out if not o['end_tipo'] and o['end_raw']))
    print("Endereco multi (varios numeros/ruas):", sum(1 for o in out if o['end_multi']))
    for k,v in sorted(rel.items()): print(f"  {k}: {v}")

if __name__=="__main__": main()
