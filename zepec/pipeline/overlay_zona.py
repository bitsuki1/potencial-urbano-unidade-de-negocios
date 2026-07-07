import shapefile, csv, glob, os, sys
from collections import Counter
from shapely.geometry import shape as shp_shape
from shapely.ops import unary_union
from shapely.strtree import STRtree
from shapely.prepared import prep

import os as _os
# Caminhos parametrizados (fim do "/tmp morto" — escrutínio GEO/repro). Defaults reprodutíveis:
#  GEO_DL = pasta dos shapefiles (zonas + SIRGAS_SHP_LOTES_*); default = zepec/raw/geo no repo.
#  PU_REPO = raiz do repo; default = 2 níveis acima deste arquivo.
REPO=_os.environ.get("PU_REPO", _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))))
DL=_os.environ.get("GEO_DL", _os.path.join(REPO,"zepec/raw/geo"))

ZMAP={
 "ZC":"ZC","ZC_a":"ZCa","ZC_ZEIS":"ZC-ZEIS",
 "ZCOR_1":"ZCOR-1","ZCOR_2":"ZCOR-2","ZCOR_3":"ZCOR-3","ZCOR_a":"ZCORa",
 "ZDE_1":"ZDE-1","ZDE_2":"ZDE-2",
 "ZEIS_1":"ZEIS-1","ZEIS_2":"ZEIS-2","ZEIS_3":"ZEIS-3","ZEIS_4":"ZEIS-4","ZEIS_5":"ZEIS-5",
 "ZEM":"ZEM","ZEMP":"ZEMP","ZEP":"ZEP","ZEPAM":"ZEPAM",
 "ZER_1":"ZER-1","ZER_2":"ZER-2","ZER_a":"ZERa",
 "ZEU_a":"ZEUa","ZEU_u":"ZEU","ZEUP_a":"ZEUPa","ZEUP_u":"ZEUP",
 "ZM_a":"ZMa","ZM_u":"ZM","ZMIS_a":"ZMISa","ZMIS_u":"ZMIS",
 "ZOE":"ZOE","ZPDS_r":"ZPDSr","ZPDS_u":"ZPDS",
 "ZPI_1":"ZPI-1","ZPI_2":"ZPI-2","ZPR":"ZPR",
 "ZEPEC_APC":"ZEPEC_APC","ZEPEC_APP-BIR":"ZEPEC_APP-BIR","ZEPEC_APP":"ZEPEC_APP",
 "ZEPEC_AUE_INDIC":"ZEPEC_AUE_INDIC","ZEPEC_AUE":"ZEPEC_AUE",
 "ZEPEC_BIR_INDIC":"ZEPEC_BIR_INDIC","ZEPEC_BIR":"ZEPEC_BIR",
}

# Quadro 3: normalized zona (lower) -> ca_basico
q3={}
with open(os.path.join(REPO,"tabelas/quadro3-ca-por-zona.csv")) as f:
    for line in f:
        if line.startswith("#") or line.startswith("zona,"): continue
        parts=next(csv.reader([line]))
        if len(parts)<3: continue
        q3[parts[0].strip().lower()]=parts[2].strip()
def ca_for(label): return q3.get(label.lower(),"")

# build zone unions + STRtree
zone_bases=sorted([b for b in ZMAP if os.path.exists(os.path.join(DL,b+".shp"))])
labels=[]; geoms=[]; in_q3=[]; fonte=[]
for b in zone_bases:
    r=shapefile.Reader(os.path.join(DL,b+".shp"))
    polys=[]
    for i in range(len(r)):
        try:
            g=shp_shape(r.shape(i).__geo_interface__)
            if not g.is_valid: g=g.buffer(0)
            if not g.is_empty: polys.append(g)
        except Exception: pass
    if not polys: continue
    u=unary_union(polys); lab=ZMAP[b]
    labels.append(lab); geoms.append(u); in_q3.append(ca_for(lab)!=""); fonte.append(b+".shp")
    print("zone",b,"->",lab,"polys",len(polys),"CA=",ca_for(lab),file=sys.stderr)
prepared=[prep(g) for g in geoms]
tree=STRtree(geoms)
print("tree zones:",len(geoms),file=sys.stderr)

# cedentes
ced=[]
with open(os.path.join(REPO,"zepec/ferramenta/zepec_cedentes.csv")) as f:
    for row in csv.DictReader(f):
        s=(row.get("sql_mestre") or "").strip()
        if len(s)==10 and s.isdigit(): ced.append(s)
ced_set=set(ced)
print("cedentes rows valid sql:",len(ced),"unique:",len(ced_set),file=sys.stderr)

# lotes centroids (only for cedente sqls)
cent={}
for shp in sorted(glob.glob(DL+"/SIRGAS_SHP_LOTES_*.shp")):
    r=shapefile.Reader(shp)
    flds=[fld[0] for fld in r.fields[1:]]
    i_s=flds.index("lo_setor"); i_q=flds.index("lo_quadra"); i_l=flds.index("lo_lote")
    recs=r.records()
    for i in range(len(recs)):
        rec=recs[i]
        sql=f"{str(rec[i_s]).zfill(3)}{str(rec[i_q]).zfill(3)}{str(rec[i_l]).zfill(4)}"
        if sql in ced_set and sql not in cent:
            try: cent[sql]=shp_shape(r.shape(i).__geo_interface__).centroid
            except Exception: pass
print("cedentes with lote centroid:",len(cent),file=sys.stderr)

# spatial join
out=[]; no_zone=0; no_lote=0
for sql in ced_set:
    c=cent.get(sql)
    if c is None: no_lote+=1; continue
    base_hit=None; any_hit=None
    for idx in tree.query(c):
        i=int(idx)
        if prepared[i].contains(c):
            if any_hit is None: any_hit=i
            if in_q3[i]: base_hit=i; break
    hit=base_hit if base_hit is not None else any_hit
    if hit is None: no_zone+=1; continue
    out.append((sql,labels[hit],ca_for(labels[hit]),fonte[hit]))

out.sort()
outdir=os.path.join(REPO,"zepec/oficial"); os.makedirs(outdir,exist_ok=True)
outpath=os.path.join(outdir,"zona_por_cedente.csv")
with open(outpath,"w",newline="") as f:
    w=csv.writer(f); w.writerow(["sql_mestre","zona","ca_basico","fonte"])
    for r in out: w.writerow(r)

zc=Counter(r[1] for r in out)
with_ca=sum(1 for r in out if r[2]!="")
print("=== RESULT ===")
print("total_com_zona",len(out))
print("unique_cedentes",len(ced_set))
print("no_lote(sem centroide)",no_lote)
print("no_zone(centroide sem zona)",no_zone)
print("with_CA",with_ca,"without_CA",len(out)-with_ca)
print("TOP", zc.most_common(8))
print("outpath",outpath)
