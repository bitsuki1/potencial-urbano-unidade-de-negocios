#!/usr/bin/env python3
"""Eval: fórmula LEGAL do PCpt para ZEPEC-BIR na AIU-SCE (Setor Central), terreno <= 1.000 m².
ÂNCORA: Art. 57 da Lei 17.844/2022 (verbatim no corpus, leis/.../lei-...-17844-2022.md):
    PCpt = ATC × CAbás × Fi × FSCE,  FSCE (fator setor central) = 2,0.
Reproduz 4 Declarações oficiais (Diário Oficial, 2026-07-08). FALHA (exit 1) se divergir. Fi vem do
engine (tabela Art.24 (incisos I–VII; cf. §§1º e 5º) LPUOS 16.402). Doutrina 1.3/1.7: número da fonte, com citação do dispositivo."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "engines", "tdc"))
import pcpt
FSCE = 2.0  # Art. 57, Lei 17.844/2022 (AIU-SCE, ZEPEC-BIR, terreno <= 1.000 m²)
CASOS = [  # sql, zona, ATC(area terreno), CAbas, declarado (m²) — todos ZEPEC-BIR no Setor Central, <=1000 m²
    ("0010800016", "ZC", 299, 1, 717.60),   # Líbero Badaró 306/310 (gabarito 006/2026)
    ("0020600004", "ZC", 734, 1, 1468.00),  # Anchieta 35 (decl. 0606/25)
    ("0020680006", "ZC", 490, 1, 1176.00),
    ("0330490001", "ZM", 320, 1, 768.00),
]
falhas = []
for sql, zona, atc, cabas, decl in CASOS:
    fi = float(pcpt.fi_zepec_por_area(pcpt.Decimal(str(atc)))[0])
    calc = round(atc * cabas * fi * FSCE, 2)
    ok = abs(calc - decl) < 0.01
    print(f"{sql} {zona} ATC={atc} CAbas={cabas} Fi={fi} FSCE={FSCE} -> {calc} (decl {decl}) {'OK' if ok else 'FALHOU'}")
    if not ok: falhas.append(sql)
if falhas:
    print("FALHAS:", falhas); sys.exit(1)
print("EVAL Art.57/17.844 (PCpt=ATC×CAbás×Fi×FSCE): 4/4 OK")
