#!/usr/bin/env python3
"""montar_ferramenta.py — a SAIDA assertiva: 1 linha por IMOVEL (SQL_MESTRE), com o
ESTADO DE VENDA e a CERTEZA. Agrega a base unificada por imovel e cruza o ESGOTADO das
certidoes. Regra de ouro: so marca 'pular' quando ESGOTADO esta ESCRITO; falta de dado =
INCERTO (verificar), nunca 'morto'.
Entrada: zepec/limpo/zepec_unificada.csv + zepec/raw/lista_certidao (p/ ESGOTADO).
Saida: zepec/ferramenta/zepec_cedentes.csv (so as colunas que o usuario precisa).
PU 14 · 2026-06-28.
"""
import csv, re
from pathlib import Path
from collections import defaultdict, Counter
Z = Path(__file__).resolve().parent
OUT = Z / "ferramenta"; OUT.mkdir(exist_ok=True)

def norm_sql(sq, lote):
    sqd=re.sub(r'\D','',sq or ''); m=re.match(r'(\d{4})',(lote or '').strip())
    return (sqd[:3]+sqd[3:6]+m.group(1)) if (len(sqd)==6 and m) else ''

# 1) das certidoes: ESGOTADOS, marca de OPERACAO URBANA e m2 JA TRANSFERIDO por cedente
from collections import defaultdict as _dd
esgotado=set(); operacao_urbana=set(); transferido=_dd(float); n_transf=_dd(int)
def _num(x):
    x=(x or '').strip().replace(' ','')
    if re.search(r',\d{2}$',x): x=x.replace('.','').replace(',','.')
    else: x=x.replace(',','')
    try: return float(re.sub(r'[^\d.]','',x))
    except Exception: return None
def _split_lotes(s):
    s=(s or '').strip()
    return [p.strip() for p in re.split(r'[;,]| e |/(?=\s*\d{4})', s) if re.search(r'\d',p)] or ([s] if s else [])
def _sm(sq,lt):
    d=re.sub(r'\D','',sq or ''); m=re.match(r'(\d{4})',(lt or '').strip())
    return d[:3]+d[3:6]+m.group(1) if (len(d)==6 and m) else ''
cer=list(csv.reader(open(Z/"raw/lista_certidao_ZEPEC-BIR_agosto-2025.csv",encoding='utf-8')))
# T11 (2026-07-05): certidao que cobre LOTES IRMAOS forma um CONJUNTO — o m2 transferido e do conjunto,
# nao de um lote. Registramos o conjunto (id + membros) e propagamos a marca a TODOS os irmaos; o saldo
# desses lotes so existe NO NIVEL DO CONJUNTO (calculado em enriquecer_oficial.py; individual = indeterminado).
conjunto_de={}; membros_conj=defaultdict(set)
for r in cer[5:]:
    r=(r+['']*19)[:19]
    lotes=_split_lotes(r[3]); sms=[s for s in (_sm(r[2],lt) for lt in lotes) if s]
    if not sms: continue
    esg='ESGOTAD' in r[14].upper()
    ouc=bool(re.search(r'\bOU\b|SEMPLA|EMURB|OUC', (r[12]+' '+r[7]).upper()))
    a=_num(r[15])
    for j,s in enumerate(sms):                 # flags p/ TODOS os lotes irmaos (achado dos agentes)
        if esg: esgotado.add(s)
        if ouc: operacao_urbana.add(s)
    if len(sms)>1:                             # T11: lotes irmaos na MESMA certidao -> conjunto (com merge)
        cids=sorted({conjunto_de[s] for s in sms if s in conjunto_de})
        cid=cids[0] if cids else 'CONJ-'+sms[0]
        for outro in cids[1:]:
            for s in membros_conj.pop(outro): conjunto_de[s]=cid; membros_conj[cid].add(s)
        for s in sms: conjunto_de[s]=cid; membros_conj[cid].add(s)
    if a: transferido[sms[0]]+=a; n_transf[sms[0]]+=1   # m2 registrado no 1o lote; saldo sai POR CONJUNTO (T11)

# padroes de SINAL (suspeita, nao prova) — usados so p/ mandar a VERIFICAR, nunca p/ excluir
RE_AREA   = re.compile(r'\bBAIRRO\b|PER[IÍ]METRO|N[UÚ]CLEO\s+URBANO|CONJUNTO\s+(URBANO|ARQUITET)', re.I)
RE_PUBLICO= re.compile(r'\b(PRA[ÇC]A|PARQUE|VIADUTO|ESTA[ÇC][AÃ]O|CEMIT[EÉ]RIO|MERCADO MUNICIPAL|TEATRO MUNICIPAL|BIBLIOTECA MUNICIPAL|C[AÂ]MARA MUNICIPAL|PREFEITURA|F[OÓ]RUM)\b', re.I)

def negociabilidade(nome, tem_decl, tem_cert, vedado, esg, sem_lote, ouc):
    # esgotado vence tudo (vendeu tudo, nada a negociar agora):
    if esg:    return 'nao','esgotado (escrito na certidao)',''
    # CONFLITO: vedado por lei (AUE/APPa) MAS declarou/vendeu = contradicao -> revisar, nao 'sim' seco:
    if vedado and (tem_decl or tem_cert):
        return 'verificar','','tag AUE/APPa conflita com declaracao/venda — revisar'
    # PROVA de que negocia (declarou/vendeu) vence a suspeita de NOME:
    if tem_decl or tem_cert: return 'sim','declarou/vendeu (prova de negociabilidade)',''
    # vedado por lei, e que nunca declarou/vendeu:
    if vedado: return 'nao','vedado por lei (categoria AUE/APPa)',''
    # senao, junta SINAIS (suspeita) -> VERIFICAR, nunca excluir:
    sinais=[]
    if sem_lote: sinais.append('sem lote individual na fonte')
    if ouc: sinais.append('marca de operacao urbana (regime CEPAC)')
    if nome and RE_AREA.search(nome): sinais.append('nome de area/bairro')
    if nome and RE_PUBLICO.search(nome): sinais.append('nome sugere bem publico')
    if sinais: return 'verificar','', ' | '.join(sinais)
    return 'sim','lote identificavel, sem sinal contrario',''

# 1b) camada de donos (se ja gerada por donos.py)
donos={}
_dp=Z/"limpo/donos_encontrados.csv"
if _dp.exists():
    for r in csv.DictReader(open(_dp,encoding='utf-8')): donos[r['sql_mestre']]=r
# 1c) FUNDURB por n_processo (preco real + intercorrencia)
fundurb={}
_fp=Z/"limpo/fundurb_processos.csv"
if _fp.exists():
    for r in csv.DictReader(open(_fp,encoding='utf-8')): fundurb[r['n_processo'].strip()]=r

# 2) agrega a base unificada por SQL_MESTRE (e guarda os sem-SQL como individuais)
rows=list(csv.reader(open(Z/"limpo/zepec_unificada.csv",encoding='utf-8')))
idx={c:i for i,c in enumerate(rows[0])}; g=lambda r,c: r[idx[c]]
grupos=defaultdict(list); soltos=[]
for r in rows[1:]:
    sm=g(r,'sql_mestre')
    if sm: grupos[sm].append(r)
    else:  soltos.append(r)

def first(rs, col, origens=None):
    for r in rs:
        if origens and g(r,'origem') not in origens: continue
        if g(r,col).strip(): return g(r,col)
    return ''

def classifica(tem_decl, tem_cert, eh_tombado, vedado, esg):
    # evidencia real (vendeu/declarou) pesa MAIS que a inferencia de categoria
    conflito = vedado and (tem_decl or tem_cert)   # tag AUE/APPa contradiz prova -> menos certeza
    if esg:                            return 'ESGOTADO','alta'        # vendeu tudo -> pular
    if tem_cert:                       return 'TEM_SALDO','media'      # vendeu parte, resta (quanto=calcular)
    if tem_decl:                       return 'INTACTO',('media' if conflito else 'alta')  # declarado, nunca vendeu
    if vedado:                         return 'VEDADO_LEI','alta'      # Art.124 §2º — nao pode ceder (e nunca declarou/vendeu)
    if eh_tombado:                     return 'SO_ELEGIVEL','media'    # tombado sem declaracao ainda
    return 'INCERTO','baixa'

COLS=['sql_mestre','setor','quadra','lote','nome_bem','endereco_mestre','distrito',
      'proprietario','fonte_dono',
      'tipo_zepec','esfera','estado_venda','certeza','negociavel','motivo_negociavel','sinais_revisar',
      'm2_ja_transferido','n_transferencias','conjunto_certidao','valor_pecuniario_rs','status_fundurb','intercorrencia_fundurb','base_periodo_fundurb_rs',
      'tem_declaracao','tem_certidao','esgotado','elegibilidade_conservacao','data_ref','origens','obs']
out=[]

_CONSERV_RANK={'ELEGIVEL':0,'PENDENTE_CONSERVACAO':1,'SEM_ATESTADO':2}
def _conservacao_agregada(rs):
    vals=[g(r,'elegibilidade_conservacao') for r in rs if g(r,'elegibilidade_conservacao')]
    if not vals: return 'SEM_ATESTADO'
    return min(vals, key=lambda v: _CONSERV_RANK.get(v, 9))

def monta(sm, rs):
    orig=set(g(r,'origem') for r in rs)
    tem_decl='DECLARACAO_BIR' in orig
    tem_cert='CERTIDAO_BIR_CEDENTE' in orig
    eh_tomb='TOMBADO_CADASTRO' in orig
    vedado=any(g(r,'cessao_vedada_art124p2')=='sim' for r in rs)
    esg= sm in esgotado if sm else False
    estado,cert=classifica(tem_decl,tem_cert,eh_tomb,vedado,esg)
    if not sm: estado,cert='INCERTO','baixa'   # sem SQL nao da p/ confiar na identificacao
    nome=first(rs,'nome_bem',['TOMBADO_CADASTRO','ZEPEC_APC'])
    neg,motivo,sinais=negociabilidade(nome,tem_decl,tem_cert,vedado,esg,not sm, sm in operacao_urbana if sm else False)
    # FUNDURB: casa SO por processo de CERTIDAO (a transferencia), nunca declaracao (achado lente B)
    fmatches=[fundurb[g(r,'n_processo').strip()] for r in rs
              if g(r,'origem')=='CERTIDAO_BIR_CEDENTE' and g(r,'n_processo').strip() in fundurb]
    fu=fmatches[0] if fmatches else {}
    tz='/'.join(sorted(set(g(r,'tipo_zepec') for r in rs if g(r,'tipo_zepec'))))
    datas=[g(r,'data_pub_iso') for r in rs if g(r,'data_pub_iso')]
    obs=[]
    if tem_decl and tem_cert: obs.append('declarou e ja vendeu (tem vinculo)')
    if vedado and (tem_decl or tem_cert): obs.append('tem tag AUE/APPa mas declarou/vendeu — revisar')
    if not sm: obs.append('sem SQL na fonte — identificar por endereco')
    return dict(sql_mestre=sm,setor=first(rs,'setor'),quadra=first(rs,'quadra'),lote=first(rs,'lote'),
        nome_bem=first(rs,'nome_bem',['TOMBADO_CADASTRO','ZEPEC_APC']),
        endereco_mestre=first(rs,'endereco_mestre',['DECLARACAO_BIR','CERTIDAO_BIR_CEDENTE','TOMBADO_CADASTRO','ZEPEC_APC']) or first(rs,'endereco_mestre'),
        distrito=first(rs,'distrito'),
        proprietario=(donos.get(sm,{}).get('proprietario','') if sm else ''),
        fonte_dono=(donos.get(sm,{}).get('fonte_dono','') if sm else ''),
        tipo_zepec=tz,esfera=first(rs,'esfera',['TOMBADO_CADASTRO']),
        estado_venda=estado,certeza=cert,negociavel=neg,motivo_negociavel=motivo,sinais_revisar=sinais,
        m2_ja_transferido=(f"{round(transferido[sm],2)}" if sm and sm in transferido else ''),
        n_transferencias=(n_transf[sm] if sm and sm in n_transf else ''),
        conjunto_certidao=(conjunto_de.get(sm,'') if sm else ''),
        valor_pecuniario_rs=fu.get('valor_pecuniario_rs',''),status_fundurb=fu.get('status_fundurb',''),
        intercorrencia_fundurb=fu.get('intercorrencia',''),base_periodo_fundurb_rs=fu.get('base_periodo_rs',''),
        tem_declaracao='sim' if tem_decl else 'nao',
        tem_certidao='sim' if tem_cert else 'nao',esgotado='sim' if esg else 'nao',
        elegibilidade_conservacao=_conservacao_agregada(rs),
        data_ref=max(datas) if datas else '',origens='+'.join(sorted(orig)),obs=' | '.join(obs))

for sm,rs in grupos.items():
    if sm: out.append(monta(sm,rs))

# G3 / D-DONO (2026-07-05): bem COLETIVO/SERIADO sem lote cadastral — a MESMA linha da fonte repetida em
# serie (ex.: 1.772x "Luminarias Ornamentais da Light", tombamento coletivo de postes) NAO e imovel
# comercializavel individualmente. Cravado no motor: vira 1 linha 'COLETIVO' (negociavel=nao), nao N
# 'INCERTO' inflando a fila de verificacao. Os itens seguem integros em zepec/limpo/zepec_unificada.csv
# (nada se joga fora). Limiar factual: nome identico repetido >=20x sem SQL = serie coletiva.
LIMIAR_COLETIVO=20
por_nome=defaultdict(list)
for r in soltos: por_nome[g(r,'nome_bem').strip()].append(r)
for nome,rs in sorted(por_nome.items()):
    if nome and len(rs)>=LIMIAR_COLETIVO:
        o=monta('', rs[:1])
        o.update(estado_venda='COLETIVO', certeza='alta', negociavel='nao',
                 motivo_negociavel='tombamento coletivo/seriado sem lote cadastral individual — nao e imovel comercializavel (G3; D-DONO 2026-07-05)',
                 sinais_revisar='',
                 obs=f'bem coletivo: {len(rs)} itens identicos na fonte modelados como 1 bem; itens preservados em zepec/limpo/zepec_unificada.csv')
        out.append(o)
    else:
        for r in rs: out.append(monta('', [r]))

ordem={'INTACTO':0,'TEM_SALDO':1,'SO_ELEGIVEL':2,'INCERTO':3,'VEDADO_LEI':4,'ESGOTADO':5,'COLETIVO':6}
out.sort(key=lambda o:(ordem.get(o['estado_venda'],9), o['distrito']))
with (OUT/"zepec_cedentes.csv").open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(out)

print(f"SAIDA: zepec/ferramenta/zepec_cedentes.csv — {len(out)} imoveis (1 linha/imovel)")
print("Por estado_venda:")
for k,v in Counter(o['estado_venda'] for o in out).most_common():
    print(f"  {k:14} {v:5}   (certeza {next(o['certeza'] for o in out if o['estado_venda']==k)})")
print("ESGOTADOS provados (cedentes):", len(esgotado))
