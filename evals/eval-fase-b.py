#!/usr/bin/env python3
"""
eval-fase-b.py — PROVA da cadeia de titularidade (Fase B), sobre FIXTURE SINTÉTICO (sem PII real).

Roda `zepec/resolver_dono.py` sobre `evals/ground-truth/fase-b-fixture/` (CPF/CNPJ/nomes FICTÍCIOS) e
confere, por caso, a pessoa física controladora esperada (`esperado.json`):
  • PF direta (CPF no IPTU)               → o próprio contribuinte;
  • PJ → sócio PF                          → o sócio pessoa física;
  • holding em 2 níveis (CNPJ→CNPJ→PF)     → a PF no topo da cadeia;
  • conflito (2 sócios PF)                 → ambos aparecem;
  • documento ausente                      → NÃO aparece (dono PENDENTE, não se inventa).

Ancorado no fixture, não circular (o gabarito é escrito à mão). Roda no gate SEM o dado pesado real e
SEM PII (passa o PII probe do consolidar.yml, que só varre zepec/limpo|oficial|raw).
PU 18 · 2026-07-10.
"""
import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FIX = RAIZ / "evals" / "ground-truth" / "fase-b-fixture"
sys.path.insert(0, str(RAIZ / "zepec"))
import resolver_dono as R  # noqa: E402


def _rodar():
    contrib, empresas, socios = R._carregar(FIX)
    linhas = {l["sql_mestre"]: l for l in R.resolver(contrib, empresas, socios)}
    gab = json.loads((FIX / "esperado.json").read_text(encoding="utf-8"))
    return linhas, gab


def _falhas(linhas, gab):
    falhas = []
    for sql, esperados in gab["esperado"].items():
        if sql not in linhas:
            falhas.append(f"{sql}: sem dono resolvido (esperava {esperados})"); continue
        prop = linhas[sql]["proprietario"].upper()
        for nome in esperados:
            if nome.upper() not in prop:
                falhas.append(f"{sql}: '{nome}' não aparece em «{linhas[sql]['proprietario']}»")
    for sql in gab.get("ausentes", []):
        if sql in linhas:
            falhas.append(f"{sql}: apareceu com dono, mas o documento é ausente (deveria ficar PENDENTE)")
    return falhas


def main_asserts():
    """Chamado por resolver_dono.py --autoteste. Levanta AssertionError se algo falhar."""
    linhas, gab = _rodar()
    falhas = _falhas(linhas, gab)
    assert not falhas, "; ".join(falhas)
    return len(gab["esperado"])


def main():
    linhas, gab = _rodar()
    falhas = _falhas(linhas, gab)
    print("═══ PROVA Fase B (cadeia de titularidade, fixture sintético) ═══")
    for sql, esperados in gab["esperado"].items():
        got = linhas.get(sql, {}).get("proprietario", "(ausente)")
        print(f"  {sql}: {got}")
    if falhas:
        print("[FALHA]")
        for f in falhas:
            print("   -", f)
        print(f"\nRESUMO: FALHA ({len(falhas)}).")
        return 1
    print(f"\nRESUMO: OK — {len(gab['esperado'])} casos da cadeia (PF direta, PJ→sócio, holding 2 níveis, "
          f"conflito) + documento ausente fica PENDENTE. Pronto p/ o dado real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
