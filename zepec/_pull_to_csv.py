#!/usr/bin/env python3
"""Converte os despejos do Drive MCP (base64/JSON) das 4 planilhas ZEPEC em CSV limpo
em zepec/raw/. Stdlib only (sem openpyxl/pandas). Parser xlsx minimo via zipfile+xml.
Proveniencia: cada fonte traz fileId do Drive (ver zepec/raw/PROVENIENCIA.md).
Uso: python3 zepec/_pull_to_csv.py
"""
import json, base64, zipfile, io, csv, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
RAW = Path(__file__).resolve().parent / "raw"
RAW.mkdir(parents=True, exist_ok=True)

def col_to_idx(col):
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n - 1

def xlsx_to_rows(b):
    z = zipfile.ZipFile(io.BytesIO(b))
    shared = []
    if 'xl/sharedStrings.xml' in z.namelist():
        t = ET.fromstring(z.read('xl/sharedStrings.xml'))
        for si in t.findall(NS + 'si'):
            shared.append(''.join(n.text or '' for n in si.iter(NS + 't')))
    names = [n for n in z.namelist() if re.match(r'xl/worksheets/sheet\d+\.xml$', n)]
    names.sort()
    t = ET.fromstring(z.read(names[0]))
    rows = []
    for row in t.iter(NS + 'row'):
        cells, maxc = {}, -1
        for c in row.findall(NS + 'c'):
            ci = col_to_idx(re.match(r'[A-Z]+', c.get('r')).group())
            typ = c.get('t'); v = c.find(NS + 'v'); val = ''
            if typ == 'inlineStr':
                isv = c.find(NS + 'is')
                if isv is not None:
                    val = ''.join(n.text or '' for n in isv.iter(NS + 't'))
            elif v is not None:
                val = shared[int(v.text)] if typ == 's' else (v.text or '')
            cells[ci] = val; maxc = max(maxc, ci)
        rows.append([cells.get(i, '') for i in range(maxc + 1)])
    return rows

def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write_csv(name, rows):
    out = RAW / name
    with out.open('w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(rows)
    print(f"{name}: {len(rows)} linhas, {max((len(r) for r in rows), default=0)} colunas -> {out}")

def from_download_xlsx(path, name):
    b = base64.b64decode(load_json(path)['content'])
    write_csv(name, xlsx_to_rows(b))

def from_download_csv(path, name):
    txt = base64.b64decode(load_json(path)['content']).decode('utf-8', 'replace')
    rows = list(csv.reader(io.StringIO(txt)))
    write_csv(name, rows)

def from_inline_b64_csv(b64, name):
    txt = base64.b64decode(b64).decode('utf-8', 'replace')
    rows = list(csv.reader(io.StringIO(txt)))
    write_csv(name, rows)

if __name__ == "__main__":
    # caminhos dos despejos do Drive MCP (sessao atual) — base64/JSON
    TR = "/root/.claude/projects/-home-user-potencial-urbano-unidade-de-negocios/56fa297c-0d21-52e7-a71e-0d438841e590/tool-results"
    from_download_xlsx(f"{TR}/mcp-Google_Drive-download_file_content-1782657791838.txt", "lista_declaracoes_ZEPEC-BIR_agosto-2025.csv")
    from_download_xlsx(f"{TR}/mcp-Google_Drive-download_file_content-1782657726049.txt", "lista_certidao_ZEPEC-BIR_agosto-2025.csv")
    from_download_csv(f"{TR}/mcp-Google_Drive-download_file_content-1782657731918.txt", "SIRGAS_SHP_benstombados1.csv")
    b64 = (RAW / "_zepec_apc.b64").read_text().strip()
    from_inline_b64_csv(b64, "SIRGAS_SHP_ZEPEC1_apc.csv")
