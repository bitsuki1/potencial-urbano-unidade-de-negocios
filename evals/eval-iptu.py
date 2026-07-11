#!/usr/bin/env python3
"""
eval-iptu.py — Golden do MOTOR IPTU (engines/iptu/iptu.py), independente do --demo.

O que morde (asserts):
  1. Âncoras derivadas À MÃO da lei (recomputadas AQUI, não copiadas do engine):
     alíquota-base (Arts. 7º/8º/27, redação 13.250/2001) + ajuste por porção
     (Arts. 7º-A/8º-A/28; faixas Arts. 3º/4º/5º da Lei 15.889/2013).
  2. Concordância dupla-via: o CSV lido AQUI (parser próprio) reproduz o resultado
     do engine em VVs de varredura — pega desalinhamento engine×tabela.
  3. Continuidade nas 4 fronteiras de faixa (desenho por porção é contínuo).
  4. Obsolescência: monotonicidade decrescente + extremos 1,00/0,30 (Tabela IV).
  5. Fail-closed: recusas obrigatórias continuam recusando.
  6. MUTAÇÃO: sabotar a alíquota-base em memória muda o resultado (o número NASCE
     da tabela, não de constante escondida — anti-oráculo, 1.3).

O que NÃO morde (declarado): confronto VV engine × lançamento real (agora em eval-iptu-oficial.py; gabarito
gabarito-iptu-vv.json) AGUARDA a PGV (Listagem por codlog) + ano de construção por
cedente → status aguardando_pgv. Os 7 cedentes rodam como [INFO] (enquadramento de
uso + faixa do lançamento), sem assert de valor.

PU 18 · 2026-07-10 — IPTU aberto pelo dono ("finalizarmos as duas frentes").
"""
import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "engines" / "iptu"))
import iptu  # noqa: E402

Q2 = Decimal("0.01")
CEM = Decimal("100")
FALHAS = []
PASSOS = []


def chk(nome, cond, detalhe=""):
    if cond:
        PASSOS.append(f"  [PASS ] {nome}" + (f" — {detalhe}" if detalhe else ""))
    else:
        FALHAS.append(f"  [FALHA] {nome}" + (f" — {detalhe}" if detalhe else ""))


# --- 1. âncoras recomputadas à mão (independentes do engine) -----------------
# residencial: base 1,0% (Art. 7º red. 13.250/2001); faixas Art. 3º 15.889:
#   [0–150k]−0,3 · (150k–300k]−0,1 · (300k–600k]+0,1 · (600k–1,2M]+0,3 · acima +0,5
ANCORAS = [
    ("residencial", "100000", Decimal("100000") * Decimal("1.0") / CEM
     + Decimal("100000") * Decimal("-0.3") / CEM),                       # 700,00
    ("residencial", "400000", Decimal("400000") * Decimal("1.0") / CEM
     + Decimal("150000") * Decimal("-0.3") / CEM
     + Decimal("150000.00") * Decimal("-0.1") / CEM
     + Decimal("100000.00") * Decimal("0.1") / CEM),                     # 3.500,00
    ("nao_residencial", "100000", Decimal("100000") * Decimal("1.5") / CEM
     + Decimal("100000") * Decimal("-0.4") / CEM),                       # 1.100,00
    ("territorial", "1000000", Decimal("1000000") * Decimal("1.5") / CEM
     + Decimal("150000") * Decimal("-0.4") / CEM
     + Decimal("150000.00") * Decimal("-0.2") / CEM
     + Decimal("300000.00") * Decimal("0.0") / CEM
     + Decimal("400000.00") * Decimal("0.2") / CEM),                     # 14.900,00
]
for uso, vv, esperado in ANCORAS:
    got = iptu.iptu_devido(vv, uso)["imposto_brl"]
    esp = esperado.quantize(Q2)
    chk(f"âncora {uso} VV={vv}", got == esp, f"{got} (esperado {esp})")

# --- 2. dupla-via: CSV lido aqui reproduz o engine em varredura --------------
def _faixas_csv():
    porc = {}
    with open(RAIZ / "tabelas" / "iptu-aliquotas-faixa.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            de = Decimal(r["faixa_de_brl"])
            ate = Decimal(r["faixa_ate_brl"]) if (r["faixa_ate_brl"] or "").strip() else None
            porc.setdefault(r["uso"], []).append((de, ate, Decimal(r["aliquota_pct"].replace("+", ""))))
    for fx in porc.values():
        fx.sort(key=lambda t: t[0])
    return porc


def _base_csv():
    out = {}
    with open(RAIZ / "tabelas" / "iptu-aliquota-base.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["uso"]] = Decimal(r["aliquota_pct"])
    return out


FA, BA = _faixas_csv(), _base_csv()


def _imposto_aqui(vv, uso):
    """SEGUNDA VIA de verdade (lente 2026-07-10: a versão anterior reimplementava o loop
    de porção do engine byte-a-byte — tautologia). Aqui a formulação é CUMULATIVA POR
    FRONTEIRA: ajuste(VV em faixa k) = Σ_{j<k} largura_j × pct_j + (VV − fronteira_{k-1}) × pct_k,
    usando SÓ os tetos (`ate`) do CSV como fronteiras — sem o deslocamento +0,01 do engine.
    Uma regressão na aritmética de porção do engine agora DIVERGE desta via."""
    V = Decimal(vv)
    tot = V * BA[uso] / CEM
    fronteiras = [ate for _, ate, _ in FA[uso] if ate is not None]  # [150k, 300k, 600k, 1.2M]
    pcts = [pct for _, _, pct in FA[uso]]
    anterior = Decimal("0")
    for k, pct in enumerate(pcts):
        teto = fronteiras[k] if k < len(fronteiras) else None
        if teto is None or V <= teto:
            tot += (V - anterior) * pct / CEM     # última faixa alcançada (parcial)
            break
        tot += (teto - anterior) * pct / CEM      # faixa inteira
        anterior = teto
    # ROUND_HALF_UP = convenção do projeto (pcpt.py); a lei só permite "desprezar frações"
    # (Art. 19 §2º, Lei 6.989/1966) sem fixar o modo — confronto com lançamento real
    # poderá revelar o arredondamento do fisco (pendência fina, junto com a PGV).
    return tot.quantize(Q2, ROUND_HALF_UP)


VARREDURA = ["50000", "150000", "150000.01", "299999.99", "300000.01", "599999",
             "600000.01", "1199999", "1200000.01", "5000000"]
div = [vv for vv in VARREDURA for uso in FA
       if iptu.iptu_devido(vv, uso)["imposto_brl"] != _imposto_aqui(vv, uso)]
chk("dupla-via engine×CSV (30 pontos)", not div, f"divergentes: {div[:3]}" if div else "0 divergência")

# --- 3. continuidade nas 4 fronteiras ----------------------------------------
for uso in FA:
    for _, ate, _ in FA[uso][:-1]:
        a = iptu.iptu_devido(str(ate), uso)["imposto_brl"]
        b = iptu.iptu_devido(str(ate + Q2), uso)["imposto_brl"]
        if abs(a - b) > Q2:
            chk(f"continuidade {uso}@{ate}", False, f"{a} → {b}")
            break
    else:
        chk(f"continuidade {uso} (4 fronteiras)", True)

# --- 4. obsolescência: monotônica decrescente, extremos legais ---------------
# Tabela IV ano-a-ano (2 colunas). Sem tipo/padrão → coluna "demais" (piso 0,20 aos 60). idade 99 → cap 60.
fat = [iptu.fator_obsolescencia(i) for i in (0, 5, 6, 10, 11, 20, 21, 35, 50, 51, 99)]
chk("obsolescência extremos (1,00 → 0,20)", fat[0] == Decimal("1.00") and fat[-1] == Decimal("0.20"),
    f"{fat[0]}..{fat[-1]}")
chk("obsolescência monotônica", all(a >= b for a, b in zip(fat, fat[1:])), str(fat))
# coluna 'ab' (Tipos 1-2 Padrões A/B) deprecia mais rápido: piso 0,20 já aos 40 anos
chk("obsolescência coluna A/B (Tipo1 idade 40 = 0,20)", iptu.fator_obsolescencia(40, 1, "A") == Decimal("0.20"),
    str(iptu.fator_obsolescencia(40, 1, "A")))

# --- 5. fail-closed ------------------------------------------------------------
for nome, fn in [
    ("uso inválido", lambda: iptu.iptu_devido("1000", "rural")),
    ("vv=0", lambda: iptu.iptu_devido("0", "residencial")),
    ("construção sem obsolescência", lambda: iptu.vv_construcao("100", 1, "A", "1a")),
    ("PGV ausente (sem valor_m2)", lambda: iptu.vv_terreno("100", "0")),
]:
    try:
        fn()
        chk(f"fail-closed: {nome}", False, "não recusou")
    except ValueError:
        chk(f"fail-closed: {nome}", True)

# --- 6. mutação: número nasce da TABELA (anti-oráculo) -------------------------
_orig = iptu.BASE["residencial"]
iptu.BASE["residencial"] = (Decimal("9.9"), _orig[1], _orig[2])
mut = iptu.iptu_devido("100000", "residencial")["imposto_brl"]
iptu.BASE["residencial"] = _orig
chk("mutação da alíquota-base muda o resultado", mut != Decimal("700.00"), f"sabotado → {mut}")

# --- INFO: os 7 cedentes reais (gabarito aguardando_pgv) -----------------------
gab = json.loads((RAIZ / "evals/ground-truth/gabarito-iptu-vv.json").read_text(encoding="utf-8"))
print("gabarito-iptu-vv (7 cedentes reais — confronto de VV AGUARDA PGV/idade; sem assert):")
for c in gab["cedentes"]:
    try:
        uso = iptu.uso_canonico(c["uso"])
        print(f"  [INFO ] {c['sql_mestre']}: uso '{c['uso']}' → {uso}")
    except ValueError as e:
        chk(f"uso_canonico({c['sql_mestre']})", False, str(e))
print()

print("\n".join(PASSOS))
if FALHAS:
    print("\n".join(FALHAS))
    print(f"\nRESUMO: {len(PASSOS)}/{len(PASSOS) + len(FALHAS)} PASS, {len(FALHAS)} falha(s).")
    sys.exit(1)
print(f"\nRESUMO: {len(PASSOS)}/{len(PASSOS)} PASS, 0 falha(s).")
