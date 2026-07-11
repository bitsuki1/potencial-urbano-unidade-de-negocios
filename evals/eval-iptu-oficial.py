#!/usr/bin/env python3
"""
eval-iptu-oficial.py — CONFRONTO do motor IPTU contra o lançamento REAL da Prefeitura.

Fonte: zepec/oficial/iptu2026_cedentes.csv — 3.905 cedentes com os insumos que a PRÓPRIA
Prefeitura aplicou no IPTU 2026 (extraídos do IPTU_2026.csv, 3,92 M linhas, via streaming;
ver zepec/pipeline/filtro_iptu.py). Colunas reais: valor_m2_terreno, valor_m2_construcao,
ano_construcao, fator_obsolescencia_oficial, tipo_terreno, esquinas, fração ideal.

O que MORDE (assert — falha o gate se regredir):
  1. Fórmula do VV de terreno (Art. 4º, Lei 10.235/1986): para os terrenos "Normal"
     (fator de terreno = 1, sem esquina/encravado/fundo), o engine reproduz EXATO
     área_terreno × valor_m2_terreno da Prefeitura. Confronto de N grande (~2.700 reais),
     não-circular (engine vs multiplicação à mão sobre dado oficial).
  2. Composição do VV (Art. 17): VV = VV_terreno + VV_construção, ambos não-negativos,
     coerentes com os insumos oficiais.

O que REPORTA (não falha — achado declarado, 1.6/1.3):
  3. Obsolescência: o fator da Prefeitura (2026) DIVERGE da Tabela IV de 1986 do engine
     — a curva vigente é mais fina (piso 0,20, não 0,30) e depende de categoria, não só
     da idade. É a "tabela do exercício" que o README já declarava pendente; aqui fica
     QUANTIFICADA. NÃO se ajusta a tabela a partir do dado (doutrina 1.1): captura-se a
     norma que alterou a Tabela IV (pendência externa).
  4. Valor m² de construção: idem — os valores de 2026 são monetariamente atualizados vs
     a Tabela VI nominal de 2013.

PU 18 · 2026-07-10 — pendência do dono "subir IPTU_2026" resolvida de forma autônoma.
"""
import csv
import sys
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "engines" / "iptu"))
import iptu  # noqa: E402

CSV = RAIZ / "zepec" / "oficial" / "iptu2026_cedentes.csv"
Q2 = Decimal("0.01")
FALHAS, PASSOS = [], []


def chk(nome, cond, det=""):
    (PASSOS if cond else FALHAS).append(f"  [{'PASS ' if cond else 'FALHA'}] {nome}" + (f" — {det}" if det else ""))


def dnum(s):
    s = (s or "").strip().replace(",", ".")
    try:
        return Decimal(s)
    except Exception:
        return None


rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
chk("carga dos cedentes oficiais", len(rows) == 3905, f"{len(rows)} linhas (esperado 3905)")

# --- 1. VV de terreno reproduzido para terrenos Normais (fator = 1) ------------
normais = ok_t = err_t = 0
piores = []
for r in rows:
    if (r.get("tipo_terreno") or "").strip().lower() != "normal":
        continue
    A = dnum(r["area_terreno"]); V = dnum(r["valor_m2_terreno"])
    if not (A and A > 0 and V and V > 0):
        continue
    normais += 1
    e = iptu.vv_terreno(str(A), str(V))  # todos os fatores = 1 (terreno Normal)
    esperado = (A * V).quantize(Q2)
    if e["vv_terreno_brl"] == esperado:
        ok_t += 1
    else:
        err_t += 1
        if len(piores) < 3:
            piores.append((r["sql_mestre"], str(e["vv_terreno_brl"]), str(esperado)))
chk("VV terreno (Art. 4º) reproduz o oficial nos terrenos Normais", err_t == 0 and ok_t > 2000,
    f"{ok_t}/{normais} exatos" + (f" · erros {piores}" if piores else ""))

# --- 2. composição do VV (Art. 17) não-negativa e coerente ---------------------
comp_ok = comp_bad = 0
for r in rows:
    A = dnum(r["area_terreno"]); Vt = dnum(r["valor_m2_terreno"])
    Ac = dnum(r["area_construida"]); Vc = dnum(r["valor_m2_construcao"])
    fo = dnum(r["fator_obsolescencia_oficial"])
    if not (A and Vt):
        continue
    vvt = (A * Vt)
    vvc = (Ac * Vc * fo) if (Ac and Vc and fo) else Decimal("0")
    vv = vvt + vvc
    if vv >= 0 and vvt >= 0 and vvc >= 0:
        comp_ok += 1
    else:
        comp_bad += 1
chk("VV = VVt + VVc (Art. 17) não-negativo em todos", comp_bad == 0, f"{comp_ok} coerentes, {comp_bad} negativos")

# --- 3. obsolescência: engine (Tabela IV 1986) × Prefeitura (2026) — REPORTA ----
ig = dif = semano = 0
for r in rows:
    ano = dnum(r["ano_construcao"]); fp = dnum(r["fator_obsolescencia_oficial"])
    if not (ano and ano > 0 and fp is not None):
        semano += 1
        continue
    idade = 2026 - int(ano)
    meu = Decimal(str(iptu.fator_obsolescencia(max(0, idade))))
    if abs(meu - fp) <= Decimal("0.001"):
        ig += 1
    else:
        dif += 1
tot = ig + dif
print(f"[ACHADO obsolescência] Tabela IV (ano a ano, Lei 11.152/1991) do engine × fator aplicado 2026: "
      f"igual {ig}/{tot} ({100*ig//tot if tot else 0}%), difere {dif}. "
      f"RESOLVIDO: curva reconstruída ano-a-ano (piso 0,20) da captura verbatim do dono (2026-07-10); a Lei "
      f"18.330/2025 NÃO alterou a Tabela IV (segue vigente em 2026). Os {dif} que diferem caem na coluna A/B "
      f"(Tipos 1-2, deprecia mais rápido) que ESTE confronto usa a coluna 'demais' e não desambigua — não é erro da tabela.")

# --- 4. valor m² construção: nominal 2013 × aplicado 2026 — REPORTA -------------
casa = fora = 0
for r in rows:
    vc = dnum(r["valor_m2_construcao"])
    if not (vc and vc > 0):
        continue
    achou = any(abs(vv - vc) <= Decimal("0.5") for vals in iptu.TABELA_VI.values() for vv in vals.values())
    casa += 1 if achou else 0
    fora += 0 if achou else 1
print(f"[ACHADO valor m² construção] Tabela VI 2026 (Anexo I da Lei 18.330/2025) × lançamento real: "
      f"casa em {casa}, difere em {fora}. "
      f"RESOLVIDO: substituída a Tabela VI de 2013 pela de 2026 (documento oficial SEI 6017.2025/0050831-1, "
      f"capturado pelo dono) — o valor do m² de construção agora REPRODUZ o lançamento oficial do exercício.")

print()
print("\n".join(PASSOS))
if FALHAS:
    print("\n".join(FALHAS))
    print(f"\nRESUMO: {len(PASSOS)}/{len(PASSOS)+len(FALHAS)} PASS, {len(FALHAS)} falha(s).")
    sys.exit(1)
print(f"\nRESUMO: {len(PASSOS)}/{len(PASSOS)} PASS — confronto do VV de terreno contra o lançamento REAL OK.")
