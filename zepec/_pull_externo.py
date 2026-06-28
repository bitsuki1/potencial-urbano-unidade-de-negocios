#!/usr/bin/env python3
"""Decodifica os despejos base64 do Drive -> .xlsx VERBATIM em zepec/raw/externo/ + CSV de
trabalho, e imprime cabecalho/linhas. Stdlib. PU 14 · 2026-06-28."""
import json, base64, zipfile, io, csv, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
OUT=Path("/home/user/potencial-urbano-unidade-de-negocios/zepec/raw/externo"); OUT.mkdir(parents=True,exist_ok=True)
def ci(col):
    n=0
    for ch in col: n=n*26+(ord(ch)-64)
    return n-1
def xlsx_rows(b):
    z=zipfile.ZipFile(io.BytesIO(b)); sh=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall(NS+'si'):
            sh.append(''.join(n.text or '' for n in si.iter(NS+'t')))
    names=sorted(n for n in z.namelist() if re.match(r'xl/worksheets/sheet\d+\.xml$',n))
    rows=[]
    for row in ET.fromstring(z.read(names[0])).iter(NS+'row'):
        cells={}; mx=-1
        for c in row.findall(NS+'c'):
            k=ci(re.match(r'[A-Z]+',c.get('r')).group()); t=c.get('t'); v=c.find(NS+'v'); val=''
            if t=='inlineStr':
                isv=c.find(NS+'is'); val=''.join(n.text or '' for n in isv.iter(NS+'t')) if isv is not None else ''
            elif v is not None: val=sh[int(v.text)] if t=='s' else (v.text or '')
            cells[k]=val; mx=max(mx,k)
        rows.append([cells.get(j,'') for j in range(mx+1)])
    return rows
for path,xlsx,csvn in json.loads(sys.argv[1]):
    d=json.loads(Path(path).read_text()); b=base64.b64decode(d['content'])
    (OUT/xlsx).write_bytes(b)                      # VERBATIM
    rows=xlsx_rows(b)
    with (OUT/csvn).open('w',newline='',encoding='utf-8') as f: csv.writer(f).writerows(rows)
    print(f"\n=== {xlsx}  ({len(rows)} linhas x {len(rows[0]) if rows else 0} col) [verbatim+csv] ===")
    # acha linha de cabecalho (a com mais textos nao-vazios entre as 3 primeiras)
    hi=max(range(min(3,len(rows))), key=lambda k: sum(1 for c in rows[k] if c.strip()))
    print("cabecalho linha",hi,":", " | ".join(c[:18] for c in rows[hi] if c.strip())[:300])
