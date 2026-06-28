#!/usr/bin/env python3
"""liquidez.py — SENSOR DE LIQUIDEZ do FUNDURB (sinal COMERCIAL de timing, não de preço).
Pergunta comercial (Codex Comercial 5.3): "há janela de mercado agora para transferir TDC?"
Mecânica: o teto de 5% (Art.24 §5º LPUOS) limita o total transferido por período de 12 meses.
folga = teto − somatória já transferida. Quanto mais folga, mais aberta a janela.
NÃO é preço (o R$ aqui é regulatório); é um ESTADO de mercado (aberta/apertada/saturada).
Saida: zepec/limpo/fundurb_janela.md. PU 14 · 2026-06-28.
"""
import csv, re
from pathlib import Path
from datetime import date
Z = Path(__file__).resolve().parent
def f(v):
    v=(v or '').strip()
    return float(v.replace('.','').replace(',','.')) if re.search(r'\d',v) else None

rows = list(csv.DictReader(open(Z/"limpo/fundurb_processos.csv", encoding='utf-8')))
# ordena os periodos por mes final (ex.: 'Dez-24 a Nov-25' -> fim Nov-25)
MES = {m:i for i,m in enumerate(['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],1)}
def fim(periodo):
    m = re.findall(r'([A-Z][a-z]{2})\s*-?(\d{2})', periodo or '')
    if len(m) >= 2:
        mes, ano = m[-1]; return (int('20'+ano), MES.get(mes,0))
    return (0,0)

# pega a linha do periodo mais recente que tenha teto e somatoria
cands = [(fim(r['periodo']), r) for r in rows if f(r.get('teto_5pct_rs')) and f(r.get('somatoria_tdc_rs'))]
cands.sort(key=lambda x: x[0])
(ano,mes), r = cands[-1]
teto = f(r['teto_5pct_rs']); soma = f(r['somatoria_tdc_rs']); folga = teto - soma
uso = soma/teto if teto else 1.0
if   uso < 0.70: janela, nota = "ABERTA", "há folga ampla na fila — janela favorável"
elif uso < 0.95: janela, nota = "APERTADA", "fila se enchendo — janela estreitando"
else:            janela, nota = "SATURADA", "teto quase no limite — sem janela no período"

txt = f"""# Sensor de liquidez FUNDURB — janela de mercado (sinal comercial, não preço)
> Gerado por `zepec/liquidez.py` a partir de `fundurb_processos.csv`. Atualizar quando a fila mudar.

**Período mais recente:** {r['periodo']}
**Janela de mercado: {janela}** — {nota}
- Teto 5% do período: R$ {r['teto_5pct_rs']}
- Já transferido (somatória): R$ {r['somatoria_tdc_rs']}
- Folga: ~R$ {folga:,.2f} ({100*(1-uso):.0f}% do teto livre)

**Leitura comercial (5.3):** checar este sinal **antes de sugerir venda**. Hoje = **{janela}**.
*(O R$ aqui é o teto regulatório, Art.24 §5º LPUOS — não é preço de crédito. Ver Codex Precificação.)*
"""
(Z/"limpo/fundurb_janela.md").write_text(txt, encoding='utf-8')
print(f"janela_mercado={janela} | periodo={r['periodo']} | uso={100*uso:.0f}% do teto | folga=R$ {folga:,.2f}")
print("-> zepec/limpo/fundurb_janela.md")
