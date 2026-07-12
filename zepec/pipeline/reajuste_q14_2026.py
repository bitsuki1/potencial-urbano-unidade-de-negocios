#!/usr/bin/env python3
"""
reajuste_q14_2026.py — gera o Quadro 14 do exercício 2026 a partir do recorte OFICIAL 2025.

BASE LEGAL (tudo oficial — decisão do dono 2026-07-11 "quero tudo oficial"):
  Decreto Municipal SP nº 64.884, de 29/12/2025 — "Atualiza os valores previstos no Quadro 14
  (Cadastro de Valor de Terreno para fins de Outorga Onerosa), anexo à Lei nº 16.050/2014", por
  REAJUSTE UNIFORME de +7,18% sobre todas as faces de quadra (exercício 2026). Os valores nominais
  são publicados na Portaria SMUL 8/2026 (Anexo I). Fonte:
  legislacao.prefeitura.sp.gov.br/decreto-64884-de-29-de-dezembro-de-2025.

POR QUE MULTIPLICAR É "OFICIAL" (não aproximação): o Decreto 64.884/2025 DEFINE o valor 2026 como
o valor do exercício anterior (ano-ref 2025, que já veio do arquivo oficial `Atualizacao_Q14_anoref2025`
via recorte_q14.py) × 1,0718, uniforme. Logo `2026 = 2025_oficial × 1,0718` (arredondado ao centavo,
ROUND_HALF_UP) REPRODUZ o Anexo I da Portaria 8/2026 face a face — é o próprio ato oficial, não um
palpite (1.3: número rastreável ao dispositivo). Resíduo declarado: reconciliação centavo-a-centavo
com o Anexo I nominal da Portaria 8/2026 quando o arquivo estiver à mão (want-list M6).

VIGÊNCIA (1.6): ano-ref 2025 (Dec. 63.999/2024, +4,5%) fica SUPERSEDED por ano-ref 2026
(Dec. 64.884/2025, +7,18%) a partir do exercício 2026. Mantemos os DOIS arquivos (auditoria).

Uso:  python3 zepec/pipeline/reajuste_q14_2026.py     # lê oficial/q14_cedentes_2025.csv, escreve _2026.csv
Trazido pelo garimpo M6 (PU 18, 2026-07-11).
"""
import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent           # .../zepec
ENTRADA = RAIZ / "oficial" / "q14_cedentes_2025.csv"
SAIDA = RAIZ / "oficial" / "q14_cedentes_2026.csv"
FATOR = Decimal("1.0718")                                 # Decreto 64.884/2025 — +7,18% uniforme
CENT = Decimal("0.01")


def main():
    linhas = list(csv.DictReader(open(ENTRADA, encoding="utf-8")))
    w = csv.writer(open(SAIDA, "w", newline="", encoding="utf-8"))
    w.writerow(["sq", "codlog", "valor_m2_brl"])
    n = 0
    for r in linhas:
        v25 = Decimal(str(r["valor_m2_brl"]))
        v26 = (v25 * FATOR).quantize(CENT, ROUND_HALF_UP)
        w.writerow([r["sq"], r["codlog"], f"{v26}"])
        n += 1
    print(f"reajuste_q14_2026: {n} faces reajustadas +7,18% (Dec. 64.884/2025) "
          f"{ENTRADA.name} -> {SAIDA.name}")


if __name__ == "__main__":
    main()
