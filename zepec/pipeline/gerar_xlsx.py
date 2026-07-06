# -*- coding: utf-8 -*-
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SRC = "zepec/ferramenta/lista_prospeccao.csv"
OUT = "/tmp/claude-0/-home-user-potencial-urbano-unidade-de-negocios/2359fb9f-e373-5054-bf05-a75b20e69771/scratchpad/Potencial-Urbano_Lista-Prospeccao-ZEPEC.xlsx"

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))

# Colunas -> cabeçalho amigável (na ordem de exibição)
COLS = [
    ("segmento",              "Segmento (estágio·dono)"),
    ("estado_venda",          "Estágio de venda"),
    ("nome_bem",              "Bem tombado"),
    ("endereco_mestre",       "Endereço"),
    ("distrito",              "Distrito"),
    ("proprietario",          "Proprietário"),
    ("tipo_zepec",            "Tipo ZEPEC"),
    ("esfera",                "Esferas (quem tombou)"),
    ("m2_ja_transferido",     "m² já transferido"),
    ("status_fundurb",        "Status FUNDURB do cedente"),
    ("intercorrencia_fundurb","Intercorrência FUNDURB"),
    ("data_ref",              "Data ref."),
    ("sql_mestre",            "SQL (chave do imóvel)"),
]

# ---- paleta ----
AZUL_ESCURO = "1F4E78"; AZUL = "2E75B6"; CINZA = "F2F2F2"
COR_ESTAGIO = {
    "INTACTO":    "C6EFCE",  # verde
    "TEM_SALDO":  "FFEB9C",  # amarelo
    "SO_ELEGIVEL":"BDD7EE",  # azul claro
    "INCERTO":    "F2F2F2",  # cinza
}
F_TITULO = Font(bold=True, size=15, color="FFFFFF")
FILL_TITULO = PatternFill("solid", fgColor=AZUL_ESCURO)
F_HEAD = Font(bold=True, color="FFFFFF", size=10)
FILL_HEAD = PatternFill("solid", fgColor=AZUL)
FILL_ZEBRA = PatternFill("solid", fgColor=CINZA)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
thin = Side(style="thin", color="D9D9D9")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()
ws = wb.active
ws.title = "Lista de Prospecção"

ncol = len(COLS)
# Título
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncol)
c = ws.cell(row=1, column=1, value="POTENCIAL URBANO — Lista de Prospecção ZEPEC (cedentes de TDC)")
c.font = F_TITULO; c.fill = FILL_TITULO; c.alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[1].height = 26
# Subtítulo
ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncol)
sc = ws.cell(row=2, column=2 if False else 1,
             value=f"{len(rows)} imóveis prontos para abordar  ·  só fato, sem juízo de valor (a priorização é sua)  ·  base completa: 6.131 imóveis")
sc.font = Font(italic=True, size=9, color="595959"); sc.alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[2].height = 16

HEAD_ROW = 3
for j, (_, titulo) in enumerate(COLS, start=1):
    cell = ws.cell(row=HEAD_ROW, column=j, value=titulo)
    cell.font = F_HEAD; cell.fill = FILL_HEAD; cell.alignment = CENTER; cell.border = BORDER
ws.row_dimensions[HEAD_ROW].height = 30

for i, r in enumerate(rows):
    rownum = HEAD_ROW + 1 + i
    for j, (key, _) in enumerate(COLS, start=1):
        val = (r.get(key, "") or "").strip()
        if val == "—": val = ""
        if key == "m2_ja_transferido" and val:
            try: val = round(float(val), 2)
            except ValueError: pass
        cell = ws.cell(row=rownum, column=j, value=val)
        cell.alignment = CENTER if key in ("estado_venda","tipo_zepec","esfera","distrito","m2_ja_transferido","data_ref","sql_mestre","status_fundurb") else LEFT
        cell.border = BORDER
        cell.font = Font(size=9)
        if i % 2 == 1:
            cell.fill = FILL_ZEBRA
    # cor do estágio na coluna 2
    est = (r.get("estado_venda","") or "").strip()
    if est in COR_ESTAGIO:
        cc = ws.cell(row=rownum, column=2)
        cc.fill = PatternFill("solid", fgColor=COR_ESTAGIO[est])
        cc.font = Font(size=9, bold=True)

# larguras
larg = {"Segmento (estágio·dono)":20,"Estágio de venda":15,"Bem tombado":34,"Endereço":30,"Distrito":16,
        "Proprietário":34,"Tipo ZEPEC":12,"Esferas (quem tombou)":22,"m² já transferido":14,
        "Status FUNDURB do cedente":22,"Intercorrência FUNDURB":20,"Data ref.":12,"SQL (chave do imóvel)":18}
for j, (_, titulo) in enumerate(COLS, start=1):
    ws.column_dimensions[get_column_letter(j)].width = larg.get(titulo, 16)

ws.freeze_panes = f"A{HEAD_ROW+1}"
ws.auto_filter.ref = f"A{HEAD_ROW}:{get_column_letter(ncol)}{HEAD_ROW+len(rows)}"

# ---- aba LEGENDA ----
wl = wb.create_sheet("Legenda")
wl.column_dimensions["A"].width = 22; wl.column_dimensions["B"].width = 70
tc = wl.cell(row=1, column=1, value="Como ler a planilha"); tc.font = Font(bold=True, size=13, color="FFFFFF"); tc.fill = FILL_TITULO
wl.merge_cells("A1:B1")
legenda = [
    ("Estágio de venda", ""),
    ("INTACTO", "Declarou potencial e NUNCA vendeu — potencial cheio. Abordar."),
    ("TEM_SALDO", "Vendeu parte, ainda resta potencial. Abordar (calcular o que resta)."),
    ("SO_ELEGIVEL", "Tombado que ainda NÃO declarou — pode entrar (precisa declarar antes)."),
    ("", ""),
    ("Esferas", "Quem tombou o bem: municipal (CONPRESP) / estadual (CONDEPHAAT) / federal (IPHAN). Mais esferas = mais órgãos na negociação."),
    ("m² já transferido", "Quanto de potencial o imóvel já vendeu (0 = intacto)."),
    ("SQL", "'CPF do imóvel' (setor-quadra-lote) — a chave que liga tudo."),
    ("Status FUNDURB do cedente", "Status do processo pecuniário FUNDURB do próprio cedente. Hoje INDETERMINADO até confirmar a semântica com a Prefeitura (SMUL)."),
    ("Proprietário", "Cobertura PARCIAL hoje — sobe em escala quando o IPTU/ITBI subir ao Supabase."),
    ("Preço (R$)", "NÃO está aqui (decisão de pausar). Quando despausar + subir o dado pesado, entra o valor estimado por imóvel."),
    ("Princípio", "Só fato, sem 'vale/melhor/pior'. A priorização comercial é do time. Preço nasce do engine, nunca é inventado."),
]
for i, (a, b) in enumerate(legenda, start=2):
    ca = wl.cell(row=i, column=1, value=a); ca.font = Font(bold=bool(a and not b), size=10); ca.alignment = Alignment(vertical="top", wrap_text=True)
    cb = wl.cell(row=i, column=2, value=b); cb.font = Font(size=10); cb.alignment = Alignment(vertical="top", wrap_text=True)
    if a in COR_ESTAGIO:
        ca.fill = PatternFill("solid", fgColor=COR_ESTAGIO[a])

wb.save(OUT)
print("gerado:", OUT, "| imóveis:", len(rows))
