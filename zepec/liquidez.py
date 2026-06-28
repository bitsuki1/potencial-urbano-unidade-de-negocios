#!/usr/bin/env python3
"""liquidez.py — sensor de liquidez FUNDURB (sinal COMERCIAL de timing).
⚠️ REBAIXADO pós-escrutínio (2026-06-28): a semântica das colunas do bruto NÃO é confiável o
suficiente para emitir um sinal verde/vermelho honesto:
  - `somatoria_tdc_acum_rs` é ACUMULADO ALL-TIME (cresce sem resetar), NÃO o total da janela de 12m.
  - `base_periodo_rs` (col "5% FUNDURB (período | R$)") parece ser a ARRECADAÇÃO (~50-77M), não os 5%.
Logo `folga = base − somatoria` mistura grandezas (fator ~20 + bases temporais diferentes) e o sinal
sairia INVERTIDO. Doutrina: não inventar — reportar os FATOS crus e marcar INDETERMINADO até confirmar
a semântica na fonte (SMUL/PDF original). NÃO é preço.
Saida: zepec/limpo/fundurb_janela.md. PU 14 · 2026-06-28.
"""
import csv, re
from pathlib import Path
Z = Path(__file__).resolve().parent
def f(v):
    v=(v or '').strip()
    return float(v.replace('.','').replace(',','.')) if re.search(r'\d',v) else None
MES = {m:i for i,m in enumerate(['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],1)}
def fim(periodo):
    m = re.findall(r'([A-Z][a-z]{2})\s*-?(\d{2})', periodo or '')
    return (int('20'+m[-1][1]), MES.get(m[-1][0],0)) if len(m)>=2 else (0,0)

rows = list(csv.DictReader(open(Z/"limpo/fundurb_processos.csv", encoding='utf-8')))
cands = [(fim(r['periodo']), r) for r in rows if f(r.get('base_periodo_rs')) and f(r.get('somatoria_tdc_acum_rs'))]
cands.sort(key=lambda x: x[0])
r = cands[-1][1]
# soma dos valores efetivamente TRANSFERIDOS no período-alvo (janela), a partir do valor por processo
alvo = r['periodo']
transf = [f(x['valor_pecuniario_rs'].split()[0]) for x in rows
          if x['periodo']==alvo and x['status_fundurb'].startswith('Transferido') and f(x['valor_pecuniario_rs'].split()[0] if x['valor_pecuniario_rs'] else '')]
soma_janela = sum(v for v in transf if v) if transf else 0.0

txt = f"""# Sensor de liquidez FUNDURB — janela de mercado (sinal comercial)
> Gerado por `zepec/liquidez.py`. **JANELA: INDETERMINADO** — semântica das colunas do bruto a confirmar (ver abaixo).

**Período mais recente:** {alvo}
**Fatos crus (sem juízo):**
- "base do período" (col 5% FUNDURB do bruto, **ambígua**): R$ {r['base_periodo_rs']}
- Somatória TDC **acumulada all-time** (não é a janela): R$ {r['somatoria_tdc_acum_rs']}
- Soma dos valores efetivamente transferidos NESTE período: R$ {soma_janela:,.2f}

**Por que INDETERMINADO** (achado do escrutínio 2026-06-28):
1. A somatória é acumulada (cresce sem resetar) → não dá o "transferido na janela de 12m".
2. A coluna "5% FUNDURB (período)" traz ~R$50-77M — parece a **arrecadação**, não os 5%; o teto real (~5%) seria ~R$2,5-3,9M.
→ Comparar os dois daria sinal INVERTIDO. **Não emitimos verde/vermelho sobre isso.**

**Para destravar (passo do MOU):** confirmar na fonte SMUL/PDF qual coluna é o **teto de transferência** e se a somatória reseta por período. Aí o sinal vira confiável.
"""
(Z/"limpo/fundurb_janela.md").write_text(txt, encoding='utf-8')
print(f"JANELA=INDETERMINADO (semantica a confirmar) | periodo={alvo} | transferido_no_periodo=R$ {soma_janela:,.2f}")
print("-> zepec/limpo/fundurb_janela.md")
