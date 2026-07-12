#!/usr/bin/env python3
"""Eval: fórmula LEGAL do PCpt para ZEPEC-BIR — os DOIS ramos, contra Declarações oficiais do DOC.
ÂNCORAS:
  · Art. 57 da Lei 17.844/2022 (verbatim no corpus): PCpt = ATC × CAbás × Fi × FSCE, FSCE = 2,0
    (ZEPEC-BIR dentro da AIU-SCE, terreno ≤ 1.000 m²) — 4 Declarações (DOC, 2026-07-08).
  · Escalonado PURO (Art. 24 I–VII LPUOS 16.402, SEM Setor Central) — +3 Declarações (DOC,
    27/01 e 06/04/2026) reproduzidas EXATO pelo engine (ampliação 2026-07-10, PU 18).
O cálculo passa pelo CAMINHO REAL do engine (pcpt_sem_doacao com a flag setor_central — exercita
teto de 1.000 m², quantize e citação). FALHA (exit 1) se divergir >R$0,01.
Doutrina 1.3/1.7: número da fonte, com citação do dispositivo."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "engines", "tdc"))
import pcpt
CASOS = [  # sql, zona, ATC (m²), CAbas, declarado (m²), setor_central (AIU-SCE ×2 — Art. 57)
    ("0010800016", "ZC", "299", "1", 717.60, True),    # Líbero Badaró 306/310 (gabarito 006/2026)
    ("0020600004", "ZC", "734", "1", 1468.00, True),   # Anchieta 35 (decl. 0606/25)
    ("0020680006", "ZC", "490", "1", 1176.00, True),
    ("0330490001", "ZM", "320", "1", 768.00, True),
    # — SEM Setor Central (escalonado puro; ampliação 2026-07-10 a partir dos 25 gabaritos DOC resgatados):
    ("0370360063", "ZPR", "598.17", "1", 598.17, False),   # decl. 0608/25 · proc. 6068.2025/0008215-0 · DOC 27/01/2026
    ("0880190001", "ZM", "787.22", "1", 787.22, False),    # decl. 0610/25 · proc. 6068.2025/0009061-7 · DOC 06/04/2026
    ("0210740019", "ZEU", "1345.00", "1", 1345.00, False), # decl. 0614/25 · proc. 6068.2025/0010551-7 · DOC 06/04/2026
]
falhas = []
for sql, zona, atc, cabas, decl, sce in CASOS:
    e = pcpt.pcpt_sem_doacao(atc, cabas, setor_central=sce)
    calc = float(e["valor_m2"])
    ok = abs(calc - decl) < 0.01
    print(f"{sql} {zona} ATC={atc} CAbas={cabas} Fi={e['fi']} FSCE={e['fsce']} -> {calc} (decl {decl}) {'OK' if ok else 'FALHOU'}")
    if not ok: falhas.append(sql)
if falhas:
    print("FALHAS:", falhas); sys.exit(1)
print(f"EVAL Art.57/17.844 + Art.24 LPUOS (PCpt com e sem FSCE): {len(CASOS)}/{len(CASOS)} OK")
