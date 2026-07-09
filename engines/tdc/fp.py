#!/usr/bin/env python3
"""
fp.py — Lookup determinístico do FATOR DE PLANEJAMENTO (Fp) para OODC.

Lê o Quadro 6 (PDE Lei 16.050/2014, Anexo) de `tabelas/quadro6-fator-planejamento-fp.csv`.
O Fp entra na fórmula da Outorga Onerosa: OO = (Área_Adicional / CA_max) × Fp × Fs × V
(oodc.outorga_onerosa recebe Fp como ENTRADA; este módulo resolve Fp a partir da localização).

Regras de resolução:
  • O Fp depende da MACROÁREA (e do USO: residencial × não-residencial).
  • Dentro da macroárea "Estruturação Metropolitana", o Fp varia por SUBÁREA — obrigatória.
  • Nas demais macroáreas, subárea não se aplica (a coluna é vazia no Quadro 6).

Fail-closed (1.3): macroárea/subárea desconhecida LEVANTA, não adivinha.
Decimal exato, como pcpt.py.

Uso:
    python3 engines/tdc/fp.py          # auto-teste (gate)
    python3 engines/tdc/fp.py --demo   # exemplos + auto-teste
PU · 2026-07-09.
"""
import sys, csv, argparse
from pathlib import Path
from decimal import Decimal

LEI = "PDE Lei Municipal SP nº 16.050/2014"
TABELAS = Path(__file__).resolve().parents[2] / "tabelas"
_CSV = "quadro6-fator-planejamento-fp.csv"


def _carrega_quadro6():
    """Lê o Quadro 6 e devolve dois dicts:
      por_macroarea: {macroarea_norm -> (fp_r, fp_nr, macrozona)} — macroáreas SEM subárea
      por_subarea:   {(macroarea_norm, subarea_norm) -> (fp_r, fp_nr, macrozona)} — macroáreas COM subárea
    """
    p = TABELAS / _CSV
    if not p.exists():
        raise FileNotFoundError(
            f"tabela obrigatória ausente: {p} (1.1 — Fp nasce da tabela, não do engine)")
    with open(p, encoding="utf-8") as f:
        rows = [r for r in csv.reader(f) if r and not r[0].lstrip().startswith("#")]
    if len(rows) < 2:
        raise ValueError(f"tabela vazia/corrompida: {p}")
    hdr = rows[0]
    linhas = [dict(zip(hdr, r)) for r in rows[1:]]

    por_macroarea = {}
    por_subarea = {}
    _norm = lambda s: " ".join(s.strip().lower().split())

    for ln in linhas:
        mz = ln["macrozona"].strip()
        ma = ln["macroarea"].strip()
        sa = ln.get("subarea", "").strip()
        fp_r = Decimal(ln["fp_r"].strip())
        fp_nr = Decimal(ln["fp_nr"].strip())
        ma_n = _norm(ma)

        if sa:
            por_subarea[(_norm(ma), _norm(sa))] = (fp_r, fp_nr, mz)
        else:
            if ma_n in por_macroarea:
                raise ValueError(
                    f"macroárea duplicada sem subárea no Quadro 6: {ma!r} (corrija o CSV)")
            por_macroarea[ma_n] = (fp_r, fp_nr, mz)

    # Detecta quais macroáreas TÊM subárea (para exigir subárea na consulta)
    com_subarea = {k for (k, _) in por_subarea}

    if not (por_macroarea or por_subarea):
        raise ValueError(f"nenhuma linha útil em {p}")

    return por_macroarea, por_subarea, com_subarea


# Carrega no import (fail-closed: CSV ausente/corrompido = o módulo não carrega)
_POR_MACROAREA, _POR_SUBAREA, _COM_SUBAREA = _carrega_quadro6()


def _norm(s):
    return " ".join(str(s).strip().lower().split())


def fp_por_localizacao(macroarea, uso, subarea=None):
    """Resolve Fp a partir da macroárea, uso (R/NR) e subárea (quando aplicável).

    Parâmetros:
      macroarea: nome da macroárea (case-insensitive, ex.: "Urbanização Consolidada")
      uso:       "R" (residencial) ou "NR" (não-residencial)
      subarea:   obrigatória p/ Estruturação Metropolitana; None p/ as demais

    Devolve dict com: fp (Decimal), macroarea, subarea, macrozona, uso, citacao.
    LEVANTA ValueError se macroárea/subárea/uso desconhecidos (1.3 fail-closed).
    """
    uso_up = str(uso).strip().upper()
    if uso_up not in ("R", "NR"):
        raise ValueError(
            f"uso deve ser 'R' (residencial) ou 'NR' (não-residencial); recebido: {uso!r}")

    ma_n = _norm(macroarea)

    if ma_n in _COM_SUBAREA:
        # Macroárea com subáreas — subárea obrigatória
        if not subarea:
            subs_disp = sorted({sa for (_, sa) in _POR_SUBAREA if _ == ma_n})
            raise ValueError(
                f"macroárea {macroarea!r} exige subárea (Quadro 6 tem valores distintos por subárea). "
                f"Subáreas disponíveis: {subs_disp}")
        sa_n = _norm(subarea)
        chave = (ma_n, sa_n)
        if chave not in _POR_SUBAREA:
            subs_disp = sorted({sa for (m, sa) in _POR_SUBAREA if m == ma_n})
            raise ValueError(
                f"subárea {subarea!r} não encontrada na macroárea {macroarea!r}. "
                f"Subáreas disponíveis no Quadro 6: {subs_disp}")
        fp_r, fp_nr, mz = _POR_SUBAREA[chave]
        sa_out = subarea.strip()
    elif ma_n in _POR_MACROAREA:
        # Macroárea sem subárea
        if subarea:
            raise ValueError(
                f"macroárea {macroarea!r} NÃO tem subárea no Quadro 6 (subárea informada: {subarea!r})")
        fp_r, fp_nr, mz = _POR_MACROAREA[ma_n]
        sa_out = None
    else:
        todas = sorted(set(list(_POR_MACROAREA.keys()) + [m for (m, _) in _POR_SUBAREA]))
        raise ValueError(
            f"macroárea {macroarea!r} não encontrada no Quadro 6. "
            f"Macroáreas disponíveis: {todas}")

    fp = fp_r if uso_up == "R" else fp_nr

    return {
        "fp": fp,
        "uso": uso_up,
        "macroarea": macroarea.strip(),
        "subarea": sa_out,
        "macrozona": mz,
        "citacao": {
            "dispositivo": "Quadro 6 do PDE (Fator de Planejamento Fp por macroárea/uso)",
            "norma": LEI,
            "confianca": "alta",
            "fonte_tabela": f"tabelas/{_CSV}",
        },
    }


def listar_fp():
    """Devolve TODOS os Fp do Quadro 6 (p/ inspeção/debug). Lista de dicts."""
    resultado = []
    for ma_n, (fp_r, fp_nr, mz) in sorted(_POR_MACROAREA.items()):
        resultado.append({"macrozona": mz, "macroarea": ma_n, "subarea": None,
                          "fp_r": fp_r, "fp_nr": fp_nr})
    for (ma_n, sa_n), (fp_r, fp_nr, mz) in sorted(_POR_SUBAREA.items()):
        resultado.append({"macrozona": mz, "macroarea": ma_n, "subarea": sa_n,
                          "fp_r": fp_r, "fp_nr": fp_nr})
    return resultado


# --------------------------------------------------------------------------- auto-teste
def _autoteste():
    falhas = []

    def checa(nome, got, esperado):
        if got != esperado:
            falhas.append(f"{nome}: obtido {got!r}, esperado {esperado!r}")

    # --- Macroáreas SEM subárea (valores verbatim do Quadro 6) ---
    r = fp_por_localizacao("Urbanização Consolidada", "R")
    checa("UC R", r["fp"], Decimal("0.7"))
    checa("UC NR", fp_por_localizacao("Urbanização Consolidada", "NR")["fp"], Decimal("1.3"))

    checa("Qualif R", fp_por_localizacao("Qualificação Urbana", "R")["fp"], Decimal("0.6"))
    checa("Qualif NR", fp_por_localizacao("Qualificação Urbana", "NR")["fp"], Decimal("0.5"))

    # Redução da Vulnerabilidade (macrozona Estruturação)
    checa("RedVuln EQU R", fp_por_localizacao("Redução da Vulnerabilidade", "R")["fp"], Decimal("0.3"))
    checa("RedVuln EQU NR", fp_por_localizacao("Redução da Vulnerabilidade", "NR")["fp"], Decimal("0"))

    # Proteção e Recuperação Ambiental — macroáreas sem subárea
    checa("RedVuln PRA R",
          fp_por_localizacao("Redução da Vulnerabilidade Urbana e Recuperação Ambiental", "R")["fp"],
          Decimal("1.0"))
    checa("RedVuln PRA NR",
          fp_por_localizacao("Redução da Vulnerabilidade Urbana e Recuperação Ambiental", "NR")["fp"],
          Decimal("0"))
    checa("Controle PRA R",
          fp_por_localizacao("Controle e Qualificação Urbana e Ambiental", "R")["fp"],
          Decimal("1.0"))

    # --- Macroárea COM subárea: Estruturação Metropolitana ---
    # Grupo periferia (Fp_r=0.3, Fp_nr=0)
    checa("EM Noroeste R",
          fp_por_localizacao("Estruturação Metropolitana", "R", subarea="Noroeste")["fp"],
          Decimal("0.3"))
    checa("EM Noroeste NR",
          fp_por_localizacao("Estruturação Metropolitana", "NR", subarea="Noroeste")["fp"],
          Decimal("0"))
    checa("EM Arco Jacu-Péssego R",
          fp_por_localizacao("Estruturação Metropolitana", "R", subarea="Arco Jacu-Péssego")["fp"],
          Decimal("0.3"))

    # Grupo centro (Fp_r=1.2, Fp_nr=1.3)
    checa("EM Arco Tietê R",
          fp_por_localizacao("Estruturação Metropolitana", "R", subarea="Arco Tietê")["fp"],
          Decimal("1.2"))
    checa("EM Centro NR",
          fp_por_localizacao("Estruturação Metropolitana", "NR", subarea="Centro")["fp"],
          Decimal("1.3"))
    checa("EM Arco Pinheiros R",
          fp_por_localizacao("Estruturação Metropolitana", "R", subarea="Arco Pinheiros")["fp"],
          Decimal("1.2"))

    # --- Citação presente e correta ---
    r2 = fp_por_localizacao("Qualificação Urbana", "R")
    checa("citacao dispositivo", "Quadro 6" in r2["citacao"]["dispositivo"], True)
    checa("citacao norma", "16.050" in r2["citacao"]["norma"], True)
    checa("citacao fonte_tabela", r2["citacao"]["fonte_tabela"], f"tabelas/{_CSV}")

    # --- Macrozona correta ---
    checa("macrozona UC", r["macrozona"], "Estruturação e Qualificação Urbana")
    checa("macrozona PRA",
          fp_por_localizacao("Controle e Qualificação Urbana e Ambiental", "R")["macrozona"],
          "Proteção e Recuperação Ambiental")

    # --- Case-insensitive ---
    checa("case insensitive",
          fp_por_localizacao("urbanização consolidada", "r")["fp"], Decimal("0.7"))

    # --- listar_fp retorna algo ---
    lst = listar_fp()
    checa("listar_fp não vazio", len(lst) > 0, True)
    checa("listar_fp total", len(lst), 15)  # 10 subáreas EM + 5 macroáreas sem subárea

    # --- Rejeições (fail-closed) ---
    # Macroárea inexistente
    try:
        fp_por_localizacao("Zona Inexistente XYZ", "R")
        falhas.append("macroárea inexistente não levantou ValueError")
    except ValueError:
        pass

    # Uso inválido
    try:
        fp_por_localizacao("Urbanização Consolidada", "X")
        falhas.append("uso inválido não levantou ValueError")
    except ValueError:
        pass

    # Estruturação Metropolitana SEM subárea (obrigatória)
    try:
        fp_por_localizacao("Estruturação Metropolitana", "R")
        falhas.append("EM sem subárea não levantou ValueError")
    except ValueError:
        pass

    # Estruturação Metropolitana com subárea inexistente
    try:
        fp_por_localizacao("Estruturação Metropolitana", "R", subarea="Zona Leste Inexistente")
        falhas.append("EM subárea inexistente não levantou ValueError")
    except ValueError:
        pass

    # Macroárea sem subárea + subárea informada = erro
    try:
        fp_por_localizacao("Urbanização Consolidada", "R", subarea="Centro")
        falhas.append("subárea em macroárea sem subárea não levantou ValueError")
    except ValueError:
        pass

    return falhas


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    falhas = _autoteste()
    if falhas:
        print("AUTO-TESTE FALHOU:", *falhas, sep="\n  ", file=sys.stderr)
        sys.exit(1)
    print("AUTO-TESTE Fp (Quadro 6): OK (gate verde — inclui subáreas EM, case-insensitive, rejeições)\n")

    if args.demo:
        print("Quadro 6 — Fator de Planejamento (Fp) completo:\n")
        print(f"{'Macroárea':<55} {'Sub':<22} {'Fp(R)':>6}  {'Fp(NR)':>6}")
        print("-" * 95)
        for e in listar_fp():
            sa = e["subarea"] or ""
            print(f"{e['macroarea']:<55} {sa:<22} {e['fp_r']:>6}  {e['fp_nr']:>6}")
        print()

        # Exemplos de uso
        exemplos = [
            ("Urbanização Consolidada", "R", None),
            ("Urbanização Consolidada", "NR", None),
            ("Estruturação Metropolitana", "R", "Centro"),
            ("Estruturação Metropolitana", "NR", "Noroeste"),
            ("Qualificação Urbana", "R", None),
        ]
        print("Exemplos de lookup:")
        for ma, uso, sa in exemplos:
            r = fp_por_localizacao(ma, uso, subarea=sa)
            loc = f"{ma}" + (f" / {sa}" if sa else "")
            print(f"  {loc:<60} uso={uso:<3} -> Fp={r['fp']}")
