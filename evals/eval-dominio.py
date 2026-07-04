#!/usr/bin/env python3
"""
eval-dominio.py — GATE da separação TDC×IPTU (plano `docs/PLANO-ARRUMACAO-DRIVE-2026-07-04.md`).

Prova, mecanicamente (não "declarei" — PROVEI), as invariantes do domínio como METADADO:

  I1. NÃO-POLUIÇÃO — sob `--dominio tdc` NENHUM chunk iptu-puro é elegível (e vice-versa).
  I2. NÃO-PERDA    — 'compartilhado' (PDE/LPUOS/CF/…) entra nas consultas dos DOIS domínios.
  I3. ALCANCE      — uma pergunta de TDC ('potencial construtivo/outorga') ROTEADA a --dominio tdc
                     traz o PDE (Lei 16.050, arts. 122-133) FUNDAMENTADA — a norma-chave TDC é
                     alcançável mesmo sendo compartilhada.
  I4. VOCAB FECHADO — todo chunk indexado tem dominio ⊆ {tdc, iptu, compartilhado} e não-vazio.
  I5. ANTI-PADRÃO  — nenhum chunk carrega 'IPTU'/'TDC' dentro de tema[] (domínio saiu do tema).

Falha (exit≠0) se qualquer invariante regredir. Espelha o gate mecânico do projeto.
Uso:  python3 evals/eval-dominio.py
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import consultar as C  # noqa: E402

VOCAB = {"tdc", "iptu", "compartilhado"}


def _doms(meta, eleg):
    return {tuple(meta[c].get("dominio") or []) for c in eleg}


def main():
    store, inv, meta = C.carregar_indice()
    falhas = []

    # I1 + I2 — não-poluição e não-perda, nos dois sentidos.
    eleg_tdc = C.filtrar(meta, dominio="tdc")
    eleg_iptu = C.filtrar(meta, dominio="iptu")
    if ("iptu",) in _doms(meta, eleg_tdc):
        falhas.append("I1: chunk iptu-puro vazou sob --dominio tdc")
    if ("tdc",) in _doms(meta, eleg_iptu):
        falhas.append("I1: chunk tdc-puro vazou sob --dominio iptu")
    if ("compartilhado",) not in _doms(meta, eleg_tdc):
        falhas.append("I2: 'compartilhado' não entrou na consulta tdc (não-perda quebrada)")
    if ("compartilhado",) not in _doms(meta, eleg_iptu):
        falhas.append("I2: 'compartilhado' não entrou na consulta iptu (não-perda quebrada)")

    # I3 — a norma-chave TDC (PDE) é alcançável e fundamenta, roteada a tdc.
    r = C.consultar("transferência de potencial construtivo outorga", dominio="tdc", top=3)
    if not r["fundamentada"]:
        falhas.append(f"I3: consulta TDC não fundamentou ({r['veredito']})")
    else:
        leis_topo = {res["chunk_id"].split("::")[0] for res in r["resultados"]}
        if "lei-municipal-saopaulo-16050-2014" not in leis_topo:
            falhas.append(f"I3: PDE (16.050) não apareceu no topo da consulta TDC — veio {leis_topo}")

    # I4 + I5 — vocab fechado e anti-padrão eliminado, em TODO chunk indexado.
    sem_dom = fora_vocab = tema_sujo = 0
    for cid, m in meta.items():
        dom = m.get("dominio") or []
        if not dom:
            sem_dom += 1
        if any(d not in VOCAB for d in dom):
            fora_vocab += 1
        if any(str(t).strip().lower() in ("iptu", "tdc") for t in (m.get("tema") or [])):
            tema_sujo += 1
    if sem_dom:
        falhas.append(f"I4: {sem_dom} chunks SEM dominio")
    if fora_vocab:
        falhas.append(f"I4: {fora_vocab} chunks com dominio fora de {VOCAB}")
    if tema_sujo:
        falhas.append(f"I5: {tema_sujo} chunks ainda com IPTU/TDC em tema[] (anti-padrão)")

    if falhas:
        print("eval-dominio: FALHA")
        for f in falhas:
            print(f"  ✗ {f}")
        return 1
    n_tdc = len(eleg_tdc)
    n_iptu = len(eleg_iptu)
    print("eval-dominio: OK — separação TDC×IPTU provada.")
    print(f"  I1 não-poluição · I2 não-perda · I3 PDE alcançável do TDC (FUNDAMENTADA) · "
          f"I4 vocab fechado · I5 anti-padrão eliminado")
    print(f"  elegíveis: --dominio tdc → {n_tdc} chunks (iptu-puro excluído; compartilhado incluído) · "
          f"--dominio iptu → {n_iptu} chunks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
