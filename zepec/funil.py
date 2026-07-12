#!/usr/bin/env python3
"""
funil.py — o FUNIL do produto (M1): da base inteira até os imóveis acionáveis, em estágios CONTÁVEIS.
Cada estágio é um número rastreável (conta linhas da base enriquecida `zepec_cedentes_oficial.csv`),
não um palpite. Grava `zepec/ferramenta/funil.csv` e serve o RESUMO da planilha (gerar_xlsx.py).

Dois blocos:
  • Completude do dado (funil que só decresce): base → IPTU → zona → PCpt → saldo → preço legal.
  • Cortes de ação (não aninhados): negociáveis, acionáveis agora, com dono.
PU 18 · 2026-07-10.
"""
import csv
import sys
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes_oficial.csv"
OUT = RAIZ / "zepec" / "ferramenta" / "funil.csv"


def _num(s):
    try:
        return Decimal(str(s).replace(",", ".")) if str(s).strip() not in ("", "—") else None
    except Exception:
        return None


def _pos(r, k):
    v = _num(r.get(k))
    return v is not None and v > 0


def _tem(r, k):
    return bool((r.get(k) or "").strip() and (r.get(k) or "").strip() != "—")


def calcular(rows):
    total = len(rows)
    tem_preco = lambda r: _pos(r, "saldo_pcpt_m2") and _pos(r, "v_outorga_m2_q14")
    completude = [
        ("Base de cedentes (tombados ZEPEC carregados)", total,
         "todo o universo de imóveis tombados na base"),
        ("Com cadastro no IPTU (SQL → área de terreno)", sum(_tem(r, "area_terreno_m2") for r in rows),
         "casou o SQL no lançamento oficial IPTU 2026 (área, valor de terreno)"),
        ("Com zona e CA básico (GeoSampa + Quadro 3)", sum(_pos(r, "ca_basico") for r in rows),
         "zona-base resolvida → coeficiente de aproveitamento básico"),
        ("Com potencial calculado (PCpt, Art. 125)", sum(_pos(r, "pcpt_m2") for r in rows),
         "PCpt = Atc × CAbás × Fi (× FSCE) pelo engine"),
        ("Com saldo vendável (> 0)", sum(_pos(r, "saldo_pcpt_m2") for r in rows),
         "potencial que ainda resta transferir (descontado o já vendido)"),
        ("Com preço legal de referência (Art. 128)", sum(tem_preco(r) for r in rows),
         "saldo + valor de terreno (Quadro 14) → referência legal pelo engine art128"),
    ]
    negociaveis = sum((r.get("negociavel") or "").strip() == "sim" for r in rows)
    acionaveis = sum(((r.get("negociavel") or "").strip() == "sim" and tem_preco(r)) for r in rows)
    com_dono = sum(_tem(r, "proprietario") for r in rows)
    cortes = [
        ("Negociáveis (prova escrita de negociabilidade)", negociaveis,
         "declarou e/ou já vendeu — pode ser abordado"),
        ("Acionáveis agora (negociável + preço legal)", acionaveis,
         "tem preço de referência E é negociável — a fila de abordagem"),
        ("Com proprietário identificado", com_dono,
         "dono na base hoje (sobe em escala com a Fase B — sócios/empresas)"),
    ]
    return total, completude, cortes


def gravar(total, completude, cortes):
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bloco", "estagio", "quantidade", "do_total_pct", "nota"])
        for nome, q, nota in completude:
            pct = f"{(q * 100 / total):.0f}%" if total else "—"
            w.writerow(["completude", nome, q, pct, nota])
        for nome, q, nota in cortes:
            pct = f"{(q * 100 / total):.0f}%" if total else "—"
            w.writerow(["corte_acao", nome, q, pct, nota])


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
    total, completude, cortes = calcular(rows)
    gravar(total, completude, cortes)
    print(f"funil.csv gravado ({OUT.name}) — base {total} imóveis")
    print("\nCOMPLETUDE DO DADO (só decresce):")
    for nome, q, _ in completude:
        print(f"  {q:>5}  {nome}")
    print("\nCORTES DE AÇÃO:")
    for nome, q, _ in cortes:
        print(f"  {q:>5}  {nome}")
    # sanidade: a completude é monotônica não-crescente
    seq = [q for _, q, _ in completude]
    assert seq == sorted(seq, reverse=True), f"funil de completude não é decrescente: {seq}"
    return 0


if __name__ == "__main__":
    sys.exit(main())
