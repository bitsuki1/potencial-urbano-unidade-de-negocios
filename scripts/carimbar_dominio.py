#!/usr/bin/env python3
"""
carimbar_dominio.py — Carimba o DOMÍNIO (tdc | iptu | compartilhado) em cada norma e acórdão.

Constituição da separação TDC×IPTU (plano `docs/PLANO-ARRUMACAO-DRIVE-2026-07-04.md`):
- O domínio é METADADO, não pasta (uma norma pode servir aos dois). `leis/` segue por ESFERA.
- Vocabulário FECHADO: tdc · iptu · compartilhado. `compartilhado` = lar único que ENTRA nas
  consultas dos DOIS domínios (consultar.py: `alvo ∈ dominio OR "compartilhado" ∈ dominio`) — por
  construção NÃO perde nada (decisão do dono 2026-07-04: "não quero correr o risco de perder nada").
- Regra de fronteira do EFEITO JURÍDICO (plano §4): potencial construtivo→tdc; tributo IPTU→iptu;
  os dois / matriz-geral→compartilhado. Na dúvida → compartilhado (viés de não-perda).
- Anti-padrão eliminado: `tema[]` NÃO carrega mais 'IPTU'/'TDC' (domínio saiu do lugar errado —
  hoje 28× IPTU e 3× TDC enterrados em tema[]; ver leis/federal/lei-federal-9514-1997.json).

Grava (idempotente) em cada `leis/**/*.json` e `jurisprudencia/*.json`:
  "dominio_primario": "<tdc|iptu|compartilhado>",   # 1 valor: efeito jurídico dominante do DOCUMENTO
  "dominio": ["<...>"]                                 # array (vocab fechado) p/ o filtro pré-busca (2.6)
e remove os tokens 'IPTU'/'TDC' de `tema[]`.

Este arquivo É o registro auditável da classificação (cada compartilhado traz a RAZÃO). O dono pode
estreitar depois: mover um id de COMPARTILHADO para IPTU/TDC aqui e re-rodar (idempotente).

Uso:  python3 scripts/carimbar_dominio.py            # aplica
      python3 scripts/carimbar_dominio.py --check    # só verifica (não escreve; exit≠0 se faltar)
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VOCAB = {"tdc", "iptu", "compartilhado"}

# --- COMPARTILHADO: serve aos DOIS domínios (lar único, incluído nas consultas de ambos). ---
# Chave = stem do arquivo (basename sem .json). Cada um com a RAZÃO (efeito jurídico duplo / matriz).
COMPARTILHADO = {
    "ec-132-2023":
        "Reforma tributária (STN): toca o IPTU E o financiamento urbano/outorga — matriz (P4).",
    "lei-federal-6015-1973":
        "Registros públicos / matrícula / titularidade: base do registro da CERTIDÃO de transferência "
        "de potencial (TDC) E da titularidade para o IPTU (P3).",
    "lei-municipal-saopaulo-12350-1997":
        "Incentivo fiscal a imóveis TOMBADOS (restauro de fachada): universo ZEPEC/tombamento (TDC) E "
        "incentivo de IPTU (P3) — a prospecção TDC de tombados precisa alcançá-la.",
    "lei-municipal-saopaulo-16050-2014":
        "PDE — Plano Diretor Estratégico: arts. 122-133 são TDC/outorga E há parâmetros que afetam a "
        "base de cálculo do IPTU (P3). dominio_primario=compartilhado; quebra por-dispositivo é onda futura.",
    "lei-municipal-saopaulo-16402-2016":
        "LPUOS — zoneamento: alimenta o CAbás do PCpt (TDC) E os parâmetros urbanísticos que refletem no "
        "IPTU (P3).",
    "lei-municipal-saopaulo-16642-2017":
        "COE — Código de Obras e Edificações: define a área construída, que alimenta o potencial (TDC) E "
        "a base de cálculo do IPTU (P3).",
}
# --- TDC puro: efeito exclusivo de potencial construtivo. Hoje VAZIO em leis/ — a massa normativa TDC
# (Decreto 57.536/2016, decretos ZEPEC/CONPRESP) ainda não foi ingerida; entrará marcada 'tdc'. ---
TDC = {
    # A-05 (auditoria 2026-07-05): a Lei 17.844/2022 é a lei-NÚCLEO da Transferência do Direito de
    # Construir (menciona TDC/potencial construtivo 77×). Estava mistagueada `iptu` → `--dominio tdc`
    # a excluía silenciosamente (a lei mais on-point do projeto sumia da consulta TDC).
    "lei-municipal-saopaulo-17844-2022":
        "Lei da Transferência do Direito de Construir (TDC) — potencial construtivo passível de "
        "transferência; efeito jurídico é TDC puro (não tributo IPTU).",
    # (mais massa normativa TDC — Decreto 57.536, decretos ZEPEC — entra quando ingerida; ver A-11)
}
# Todo o resto → iptu (o corpus de leis/ e TODA a jurisprudencia/ foram montados p/ a tese IPTU).

TOKENS_DOMINIO_EM_TEMA = {"iptu", "tdc"}  # a remover de tema[] (domínio saiu do lugar errado)


def classificar(stem: str) -> str:
    if stem in COMPARTILHADO:
        return "compartilhado"
    if stem in TDC:
        return "tdc"
    return "iptu"


def alvos():
    for p in sorted((RAIZ / "leis").rglob("*.json")):
        yield p
    for p in sorted((RAIZ / "jurisprudencia").glob("*.json")):
        yield p


def main(check_only: bool):
    dist = {"tdc": 0, "iptu": 0, "compartilhado": 0}
    faltando, mudados = [], []
    for p in alvos():
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  ERRO {p.name}: JSON inválido ({e}) — pulado", file=sys.stderr)
            faltando.append(p.name)
            continue
        stem = p.stem
        dom = classificar(stem)
        dist[dom] += 1

        # tema[] sem os tokens de domínio (preserva os temas materiais, remove só IPTU/TDC)
        tema_novo = [t for t in (meta.get("tema") or [])
                     if str(t).strip().lower() not in TOKENS_DOMINIO_EM_TEMA]

        precisa = (meta.get("dominio_primario") != dom
                   or meta.get("dominio") != [dom]
                   or tema_novo != (meta.get("tema") or []))
        if check_only:
            if meta.get("dominio_primario") not in VOCAB or meta.get("dominio") != [dom]:
                faltando.append(p.name)
            continue
        if precisa:
            meta["dominio_primario"] = dom
            meta["dominio"] = [dom]
            meta["tema"] = tema_novo
            p.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            mudados.append(p.name)

    if check_only:
        if faltando:
            print(f"carimbar_dominio --check: FALHA — {len(faltando)} sem domínio válido: "
                  f"{', '.join(faltando[:8])}{'…' if len(faltando) > 8 else ''}")
            return 1
        print("carimbar_dominio --check: OK — toda norma/acórdão tem dominio ∈ {tdc,iptu,compartilhado}.")
        return 0

    print(f"carimbar_dominio: distribuição → compartilhado={dist['compartilhado']} "
          f"iptu={dist['iptu']} tdc={dist['tdc']} ({sum(dist.values())} itens).")
    print(f"  carimbados/atualizados: {len(mudados)}")
    print("  COMPARTILHADO (lar único, entra nas consultas dos dois):")
    for k in sorted(COMPARTILHADO):
        print(f"    · {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
