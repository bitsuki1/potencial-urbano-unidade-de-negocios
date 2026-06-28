#!/usr/bin/env python3
"""montar_base.py — ETAPA 1-3 das ZEPEC: junta as 4 fontes oficiais COM TAG,
canoniza SQL -> SQL_MESTRE (10 dig, decomposto, DV a parte), estrutura o ENDERECO
(CODEX §3) com CASING padrao, normaliza DATA -> ISO (padrao estabelecido abaixo) e
marca a CATEGORIA (BIR/APPa/AUE) como fato. Agnostico: so fato, sem juizo.
Multi-lote por celula é EXPLODIDO (1 linha = 1 imovel/SQL_MESTRE). Campos relacionais
(vinculo/saldo/potencial) ficam A OBSERVAR (carregados crus, nao resolvidos).

PADRAO DE DATA (item 5): saida ISO AAAA-MM-DD. Heuristica US/BR — se um campo >12 ele
é o dia (BR D/M) ou o mes (US M/D) e desambigua; se AMBOS <=12 assume BR (D/M) e marca
`data_amb=ambiguo`. Sem data reconhecida -> `data_iso=''` e `data_amb=sem_data`.

Entrada: zepec/raw/*.csv   Saida: zepec/limpo/zepec_unificada.csv + relatorio no stdout.
PU 14 · 2026-06-28.
"""
import csv, re
from pathlib import Path
from collections import Counter
from datetime import date, timedelta
RAW = Path(__file__).resolve().parent / "raw"
OUT = Path(__file__).resolve().parent / "limpo"; OUT.mkdir(exist_ok=True)

TIPOS = {
    'r':'Rua','rua':'Rua','av':'Avenida','avenida':'Avenida','pç':'Praça','pc':'Praça',
    'praça':'Praça','praca':'Praça','pça':'Praça','al':'Alameda','alameda':'Alameda',
    'largo':'Largo','lgo':'Largo','lg':'Largo','estr':'Estrada','estrada':'Estrada',
    'vd':'Viaduto','viaduto':'Viaduto','tv':'Travessa','travessa':'Travessa',
    'pateo':'Pátio','páteo':'Pátio','patio':'Pátio','pátio':'Pátio','pq':'Parque',
    'rod':'Rodovia','rodovia':'Rodovia','pte':'Ponte','vl':'Vila','via':'Via',
    'est':'Estrada','pr':'Praça','pca':'Praça','lgo.':'Largo','jd':'Jardim',
}
CONECTORES = {'de','da','do','das','dos','e','di','du','del','dos','à','a','o','as','os'}

def titlecase_pt(s, lead_lower=False):
    """Title case PT: conectores em minuscula; resto capitalizado; preserva acentos.
    lead_lower=True deixa conector minusculo MESMO no inicio (uso em logradouro, ja prefixado pelo tipo)."""
    if not s: return s
    out=[]
    for i,w in enumerate(re.split(r'(\s+)', s.strip())):
        if not w.strip(): out.append(w); continue
        lw=w.lower()
        is_con = lw in CONECTORES and (i>0 or lead_lower)
        out.append(lw if is_con else (lw[:1].upper()+lw[1:]))
    return ''.join(out)

def parse_date(s):
    """Extrai data -> (iso, flag). Trata serie do Excel (inteiro) e DD/MM/YYYY (ou US M/D)."""
    s=(s or '').strip()
    if not s: return '', 'sem_data'
    if re.fullmatch(r'\d{4,6}', s) and 15000<=int(s)<=60000:   # serie Excel (dias desde 1899-12-30)
        try: return (date(1899,12,30)+timedelta(days=int(s))).isoformat(), ''
        except Exception: pass
    m=re.search(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', s)
    if not m:
        y=re.search(r'\b(19|20)\d{2}\b', s)
        return (f"{y.group(0)}", 'so_ano') if y else ('', 'sem_data')
    a,b,y=int(m.group(1)),int(m.group(2)),m.group(3)
    if len(y)==2: y='20'+y if int(y)<50 else '19'+y
    amb=''
    if a>12 and b<=12: d,mo=a,b                 # BR D/M
    elif b>12 and a<=12: mo,d=a,b               # US M/D
    elif a<=12 and b<=12: d,mo,amb=a,b,'ambiguo'   # padrao BR, marca
    else: return '', 'invalido'
    if not(1<=d<=31 and 1<=mo<=12): return '', 'invalido'
    return f"{y}-{mo:02d}-{d:02d}", amb

def norm_sql(sq, lote):
    sqd=re.sub(r'\D','',sq or ''); lz=(lote or '').strip()
    m=re.match(r'(\d{4})\s*-?\s*(\d)?', lz)
    if len(sqd)==6 and m:
        return sqd[:3]+sqd[3:6]+m.group(1), sqd[:3], sqd[3:6], m.group(1), (m.group(2) or ''), 'ok'
    return '','','','','', ('ausente' if not sqd else 'invalido')

def norm_sql_decomp(setor,quadra,lote):
    s=re.sub(r'\D','',setor or ''); q=re.sub(r'\D','',quadra or '')
    m=re.match(r'(\d{4})\s*-?\s*(\d)?',(lote or '').strip())
    if len(s)==3 and len(q)==3 and m:
        return s+q+m.group(1), s, q, m.group(1), (m.group(2) or ''), 'ok'
    if not s and not q and not (lote or '').strip():
        return '','','','','', 'ausente'
    return '','','','','', 'invalido'

def split_lotes(lote):
    # separa multi-lote por , ; ' e ' e '/' SOMENTE antes de lote 4-dig (protege DV '0021/4')
    if not lote: return ['']
    parts=[p.strip() for p in re.split(r'[;,]| e |/(?=\s*\d{4})', lote) if re.search(r'\d', p)]
    return parts or [lote.strip()]

def norm_endereco(raw):
    raw=(raw or '').strip()
    if not raw: return '','','','',0
    antes=raw.split(',')[0].strip()
    toks=antes.split(); tipo,logr='',antes
    if toks and toks[0].lower().strip('.') in TIPOS:
        tipo=TIPOS[toks[0].lower().strip('.')]; logr=' '.join(toks[1:]).strip()
    logr=titlecase_pt(logr, lead_lower=True)
    nums=re.findall(r'\b\d+[A-Za-z]?\b', raw.split(',',1)[1]) if ',' in raw else []
    raw2=re.sub(r's\s*/\s*n[ºo°]?','',raw,flags=re.I)   # remove "s/nº" antes de detectar multi
    multi=1 if ('/' in raw2 or re.search(r'\b(R|Av|Al|Pç|Pc|Rua|Avenida|Alameda)\b', raw2[3:])) else 0
    mestre=f"{tipo} {logr}".strip()
    if nums: mestre+=", "+", ".join(nums)
    return mestre, tipo, logr, "; ".join(nums), multi

def cessao_vedada(cat):
    c=(cat or '').lower()
    return 'sim' if ('urbanização especial' in c or 'proteção paisagística' in c) else ''

COLS=['origem','tipo_zepec','esfera','categoria','cessao_vedada_art124p2',
      'sql_mestre','setor','quadra','lote','dv','sql_status',
      'endereco_mestre','end_tipo','end_logradouro','end_numeros','end_multi','end_raw',
      'distrito','nome_bem','n_declaracao','n_processo','ato_conservacao','zepec_cod',
      'data_pub_raw','data_pub_iso','data_amb','ano','situacao','status_declaracao',
      'obs_a_observar','fonte_arquivo']

def main():
    out=[]; rel=Counter()
    L=lambda p: list(csv.reader(open(RAW/p,encoding='utf-8')))
    nc=lambda v: '' if (v or '').strip() in ('não consta','nao consta','-') else (v or '').strip()

    dec=L("lista_declaracoes_ZEPEC-BIR_agosto-2025.csv")
    for r in dec[4:]:
        if not any(c.strip() for c in r): continue
        r=(r+['']*11)[:11]; lts=split_lotes(r[3])
        rel['declaracao_FONTE']+=1            # 1 por declaracao da planilha (grao: declaracao)
        for lt in lts:
            sm,se,qu,lo,dv,st=norm_sql(r[2],lt); em,et,el,en,mu=norm_endereco(r[4])
            di,da=parse_date(r[7])
            out.append(dict(origem='DECLARACAO_BIR',tipo_zepec='BIR',esfera='municipal',categoria='',cessao_vedada_art124p2='',
                sql_mestre=sm,setor=se,quadra=qu,lote=lo,dv=dv,sql_status=st,
                endereco_mestre=em,end_tipo=et,end_logradouro=el,end_numeros=en,end_multi=mu,end_raw=r[4],
                distrito=titlecase_pt(r[5]),nome_bem='',n_declaracao=r[6],n_processo=r[1],ato_conservacao='',zepec_cod='',
                data_pub_raw=r[7],data_pub_iso=di,data_amb=da,ano=r[8],situacao=r[9],status_declaracao=r[10],
                obs_a_observar='', fonte_arquivo='lista_declaracoes_ZEPEC-BIR'))
            rel['declaracao_linhas']+=1
            if st!='ok': rel['decl_sql_'+st]+=1
            if len(lts)>1: rel['decl_multilote_explodido']+=1
            if da in ('ambiguo','invalido'): rel['decl_data_'+da]+=1

    cer=L("lista_certidao_ZEPEC-BIR_agosto-2025.csv")
    for r in cer[5:]:
        if not any(c.strip() for c in r): continue
        r=(r+['']*19)[:19]
        if not r[2].strip() and not r[4].strip(): continue
        rel['certidao_FONTE']+=1             # 1 por certidao da planilha (grao: certidao)
        for lt in split_lotes(r[3]):
            sm,se,qu,lo,dv,st=norm_sql(r[2],lt); em,et,el,en,mu=norm_endereco(r[4])
            di,da=parse_date(r[17])
            out.append(dict(origem='CERTIDAO_BIR_CEDENTE',tipo_zepec='BIR',esfera='municipal',categoria='',cessao_vedada_art124p2='',
                sql_mestre=sm,setor=se,quadra=qu,lote=lo,dv=dv,sql_status=st,
                endereco_mestre=em,end_tipo=et,end_logradouro=el,end_numeros=en,end_multi=mu,end_raw=r[4],
                distrito=titlecase_pt(r[5]),nome_bem='',n_declaracao=r[6],n_processo=r[1],ato_conservacao=r[7],zepec_cod='',
                data_pub_raw=r[17],data_pub_iso=di,data_amb=da,ano='',situacao=r[18],status_declaracao='',
                obs_a_observar=f"saldo/area cedida e vinculo declaracao->certidao A OBSERVAR (certidao {r[12]})",
                fonte_arquivo='lista_certidao_ZEPEC-BIR'))
            rel['certidao_cedente_linhas']+=1
            if st!='ok': rel['cert_sql_'+st]+=1
            if da in ('ambiguo','invalido'): rel['cert_data_'+da]+=1

    bt=L("SIRGAS_SHP_benstombados1.csv")
    for r in bt[1:]:
        if not any(c.strip() for c in r): continue
        r=(r+['']*30)[:30]
        esf=['municipal'] if nc(r[5]) else []
        if nc(r[6]): esf.append('estadual')
        if nc(r[7]): esf.append('federal')
        sm,se,qu,lo,dv,stt=norm_sql_decomp(r[1],r[2],r[3]); em,et,el,en,mu=norm_endereco(r[8])
        di,da=parse_date(r[14]); cat=nc(r[22])
        out.append(dict(origem='TOMBADO_CADASTRO',tipo_zepec='tombado',esfera='+'.join(esf) or '',
            categoria=cat,cessao_vedada_art124p2=cessao_vedada(cat),
            sql_mestre=sm,setor=se,quadra=qu,lote=lo,dv=dv,sql_status=stt,
            endereco_mestre=em,end_tipo=et,end_logradouro=el,end_numeros=en,end_multi=mu,end_raw=r[8],
            distrito=titlecase_pt(nc(r[24])),nome_bem=titlecase_pt(r[0]),n_declaracao='',n_processo=nc(r[26]),
            ato_conservacao=nc(r[5]),zepec_cod=nc(r[12]),data_pub_raw=nc(r[14]),data_pub_iso=di,data_amb=da,
            ano=nc(r[15]),situacao=cat,status_declaracao=nc(r[23]),
            obs_a_observar='', fonte_arquivo='SIRGAS_SHP_benstombados1'))
        rel['tombado_linhas']+=1
        if stt!='ok': rel['tomb_sql_'+stt]+=1

    ap=L("SIRGAS_SHP_ZEPEC1_apc.csv")
    for r in ap[1:]:
        if not any(c.strip() for c in r): continue
        r=(r+['']*9)[:9]; em,et,el,en,mu=norm_endereco(r[2]); di,da=parse_date(r[7])
        out.append(dict(origem='ZEPEC_APC',tipo_zepec='APC',esfera='municipal',categoria='',cessao_vedada_art124p2='',
            sql_mestre='',setor='',quadra='',lote='',dv='',sql_status='ausente',
            endereco_mestre=em,end_tipo=et,end_logradouro=el,end_numeros=en,end_multi=mu,end_raw=r[2],
            distrito='',nome_bem=titlecase_pt(r[3]),n_declaracao='',n_processo=r[1],ato_conservacao='',zepec_cod='',
            data_pub_raw=r[7],data_pub_iso=di,data_amb=da,ano=r[0],situacao=r[8],status_declaracao='',
            obs_a_observar='APC sem SQL na fonte — resolver SQL por endereco (externo)',
            fonte_arquivo='SIRGAS_SHP_ZEPEC1_apc'))
        rel['apc_linhas']+=1

    with (OUT/"zepec_unificada.csv").open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(out)

    print(f"SAIDA: zepec/limpo/zepec_unificada.csv — {len(out)} linhas")
    print("Por origem:", dict(Counter(o['origem'] for o in out)))
    print("SQL:", dict(Counter(o['sql_status'] for o in out)))
    print("Data:", dict(Counter(o['data_amb'] or 'ok' for o in out)))
    print("Cessao vedada (AUE/APPa) marcada:", sum(1 for o in out if o['cessao_vedada_art124p2']))
    print(f"GRAO: declaracoes-FONTE={rel['declaracao_FONTE']} -> imoveis(explodido)={rel['declaracao_linhas']} | "
          f"certidoes-FONTE={rel['certidao_FONTE']} -> imoveis={rel['certidao_cedente_linhas']}")
    for k,v in sorted(rel.items()):
        if 'data' in k or 'sql_inval' in k: print(f"  {k}: {v}")

if __name__=="__main__": main()
