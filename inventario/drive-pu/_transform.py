import sys, json, csv, re, subprocess, os
# uso: _transform.py <json_file> <path_label> <indexed_ids_file> >> saida.csv
jf, path_label, idxf = sys.argv[1], sys.argv[2], sys.argv[3]
data = json.load(open(jf, encoding="utf-8"))
files = data.get("files", data if isinstance(data, list) else [])
idx = set()
if os.path.exists(idxf):
    idx = set(l.strip() for l in open(idxf) if l.strip())
def tema(n):
    n=n.lower()
    if any(k in n for k in ["sirgas","shp","shx","dbf","prj","cpg","geosampa","lote","zona","mapa","distrit"]): return "GEO"
    if "iptu" in n: return "IPTU"
    if any(k in n for k in ["lei","decreto","portaria","acordao","acórdão","súmula","sumula","jurisprud"]): return "JURIDICO"
    if any(k in n for k in ["tdc","tombad","zepec","outorga","potencial","cepac","fundurb"]): return "TDC"
    if any(k in n for k in ["log","relatorio","relatório","manifesto","indice","índice","codex","governanca","governança"]): return "GOVERNANCA"
    return "OUTRO"
def tipo(n,m):
    nl=n.lower()
    if m=="application/vnd.google-apps.folder": return "PASTA"
    if any(e in nl for e in [".shp",".shx",".dbf",".prj",".cpg"]): return "GEO_SHP"
    if "portaria" in nl: return "PORTARIA"
    if "decreto" in nl: return "DECRETO"
    if re.search(r"lei\b|lei ?n|lei-", nl): return "LEI"
    if any(k in nl for k in ["acordao","acórdão","súmula","sumula","jurisprud","resp ","tema "]): return "JURISPRUDENCIA"
    if any(k in nl for k in ["auditoria","memorial","validac","validaç","stress","análise","analise","dossie","dossiê"]): return "AUDITORIA"
    if any(k in nl for k in ["codex","biblia","bíblia","manual","conhecimento","oraculo","oráculo"]): return "CODEX_DOC"
    if nl.endswith(".py") or nl.endswith(".ipynb") or "colab" in nl: return "ENGINE_CODIGO"
    if "sheet" in m or nl.endswith((".xlsx",".xls",".ods",".csv")): return "PLANILHA" if ("sheet" in m or nl.endswith((".xlsx",".xls",".ods"))) else "TABELA_DADO"
    if "document" in m: return "DOC_GOOGLE"
    if "form" in m: return "FORMULARIO"
    if nl.endswith(".pdf") or m=="application/pdf": return "PDF"
    return "OUTRO"
def ofi(n):
    nl=n.lower()
    if any(k in nl for k in ["lei","decreto","portaria","diário","diario","prefeitura","sirgas","geosampa","conpresp","acordao","acórdão","súmula","sumula","diario oficial"]): return "OFICIAL"
    if any(k in nl for k in ["codex","auditoria","inventario","inventário","base","dossie","dossiê","memorial","análise","analise","enriquec","biblia","bíblia","oraculo","oráculo","manifesto"]): return "NOSSO"
    return "DESCONHECIDO"
w=csv.writer(sys.stdout)
n=0
for f in files:
    if f.get("mimeType")=="application/vnd.google-apps.folder":
        continue  # pastas não entram como linha de arquivo (o path já as representa)
    did=f.get("id",""); nome=f.get("title") or f.get("name",""); mime=f.get("mimeType","")
    ext=f.get("fileExtension",""); by=f.get("fileSize",""); cr=f.get("createdTime",""); mo=f.get("modifiedTime","")
    obs=""
    if by and by.isdigit() and int(by)>104857600: obs="GIGANTE>100MB"
    w.writerow([did,path_label,nome,mime,ext,by,cr,mo,tema(nome),tipo(nome,mime),ofi(nome),"SIM" if did in idx else "NAO",obs])
    n+=1
sys.stderr.write(f"linhas={n} subpastas={sum(1 for f in files if f.get('mimeType')=='application/vnd.google-apps.folder')} nextToken={data.get('nextPageToken','')[:20] if data.get('nextPageToken') else ''}\n")
