#!/usr/bin/env python3
"""
eval-arrumacao.py — TESTE DE INTEGRAÇÃO da toolchain de arrumação do Drive (end-to-end, sintético).

Simula um Log completo do Apps Script (MOVE_LINHA + INV_LINHA + CSV_LINHA) e prova o LOOP inteiro,
sem tocar o Drive: reconciliação → tipificação do lago (R8) → dedup cross-tree (R9) → idempotência →
bloqueio R4 → o gate vira fase 'execucao'. Restaura o estado 'plano' ao final (try/finally).

Falha (exit≠0) se qualquer invariante da arrumação regredir. Espelha o gate mecânico do projeto.
Uso:  python3 evals/eval-arrumacao.py
"""
import csv
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INV = RAIZ / "inventario"
SEED = INV / "INDICE-SEED.csv"
MESTRE = INV / "INDICE-MESTRE-DRIVE.csv"
CROSS = INV / "cross-tree-dups.csv"
TRILHA = INV / "arrumacao-log.csv"
LOG = INV / "gas-log-9999-99-99-EVAL.txt"     # nome improvável — não colide com log real
PY = sys.executable

falhas = []


def _run(*args):
    return subprocess.run([PY, *args], cwd=RAIZ, capture_output=True, text=True)


def _reconciliar():
    return _run("scripts/reconciliar_arrumacao.py")


def _mestre():
    return {r["drive_id"]: r for r in csv.DictReader(open(MESTRE, encoding="utf-8"))}


def _ck(cond, msg):
    if not cond:
        falhas.append(msg)


def main():
    if not SEED.exists():
        print("eval-arrumacao: SEED ausente — rode semear_indice_mestre.py antes.")
        return 1
    e0 = next(iter(csv.DictReader(open(SEED, encoding="utf-8"))))["drive_id"]  # 1º id real da _entrada

    try:
        # --- Log sintético: move e0 (_entrada) com md5 SHARED; inventário do lago com 1 lei, 1 mapa,
        # e 1 cópia byte-idêntica de e0 (cross-tree); dedup do lago mantém a cópia. ---
        LOG.write_text(
            f"MOVE_LINHA {e0},FOLDERx,SHARED,10,moved\n"
            'INV_INICIO\n'
            'INV_LINHA ZZlei,"LEI Nº 16.402 DE 2016 zoneamento.pdf",h1,100\n'
            'INV_LINHA ZZmapa,"MAPA ZEPEC distrito.shp",h2,200\n'
            'INV_LINHA ZZdup,"copia identica.pdf",SHARED,10\n'
            'INV_FIM\n'
            "CSV_LINHA ZZdup,SHARED,MANTER,ZZdup\n", encoding="utf-8")
        r = _reconciliar()
        _ck(r.returncode == 0, f"reconciliar saiu {r.returncode}: {r.stderr[-200:]}")
        m = _mestre()

        # R8 — canônicas do lago tipificadas (não órfãs)
        _ck("ZZlei" in m and m["ZZlei"]["tipo_artefato"] == "lei" and m["ZZlei"]["dominio"] == "compartilhado",
            "R8: LEI 16.402 do lago não virou lei/compartilhado")
        _ck("ZZmapa" in m and m["ZZmapa"]["tipo_artefato"] == "geo" and m["ZZmapa"]["dominio"] == "tdc",
            "R8: MAPA ZEPEC do lago não virou geo/tdc")
        _ck(m.get("ZZlei", {}).get("destino_path", "").startswith("02"),
            "R8: LEI do lago sem destino de Leis (02)")

        # R9 — dedup cross-tree emitido (e0 × ZZdup, mesmo md5 SHARED, ambos colocados)
        _ck(CROSS.exists(), "R9: cross-tree-dups.csv não foi emitido")
        if CROSS.exists():
            dups = list(csv.DictReader(open(CROSS, encoding="utf-8")))
            ids = {d["dup_id"] for d in dups}
            _ck(len(dups) == 1 and ({e0, "ZZdup"} & ids), "R9: dup cross-tree e0×ZZdup não detectada corretamente")

        # gerar_gas_crosstree produz o .gs a partir do cross
        g = _run("scripts/gerar_gas_crosstree.py")
        gs = RAIZ / "drive-arrumacao" / "Quarentenar-CrossTree.gs"
        _ck(g.returncode == 0 and gs.exists(), "R9: gerar_gas_crosstree não gerou o .gs")

        # idempotência — 2ª run: MESTRE e trilha idênticos (não dobra)
        h1 = MESTRE.read_text(encoding="utf-8")
        t1 = TRILHA.read_text(encoding="utf-8") if TRILHA.exists() else ""
        _reconciliar()
        _ck(MESTRE.read_text(encoding="utf-8") == h1, "idempotência: MESTRE mudou na 2ª run")
        _ck((TRILHA.read_text(encoding="utf-8") if TRILHA.exists() else "") == t1,
            "idempotência: trilha dobrou/mudou na 2ª run")

        # gate saiu da fase 'plano' (algo foi movido). Com só 1 de N movido, o C1 fica corretamente
        # VERMELHO (a maioria ainda não moveu) — o que se prova é que NÃO está mais em 'PLANO pronto'.
        gate = _run("scripts/gate-arrumacao.py")
        _ck("PLANO pronto" not in gate.stdout, "gate ainda em fase 'plano' após um move (deveria ser execução)")

        # R4 — OFICIAL quarentenado sob canônica NOSSA deve BLOQUEAR (exit 2)
        LOG.write_text(
            'INV_INICIO\n'
            'INV_LINHA ZZofi,"LEI Nº 10.257 DE 2001 estatuto da cidade.pdf",hz,1\n'
            'INV_LINHA ZZnos,"rascunho LOTE_IA copia.pdf",hz,1\n'
            'INV_FIM\n'
            "CSV_LINHA ZZnos,hz,MANTER,ZZnos\n"
            "CSV_LINHA ZZofi,hz,QUARENTENA,ZZnos\n", encoding="utf-8")
        rb = _reconciliar()
        _ck(rb.returncode == 2, f"R4: OFICIAL sob canônica NOSSA não bloqueou (exit {rb.returncode})")

    finally:
        # restaura estado 'plano': remove sintéticos e regenera MESTRE==SEED
        for p in (LOG, CROSS, TRILHA, RAIZ / "drive-arrumacao" / "Quarentenar-CrossTree.gs"):
            if p.exists():
                p.unlink()
        _reconciliar()

    if falhas:
        print("eval-arrumacao: FALHA")
        for f in falhas:
            print(f"  ✗ {f}")
        return 1
    print("eval-arrumacao: OK — loop end-to-end provado (R8 tipifica lago · R9 cross-tree · "
          "idempotência · R4 bloqueia OFICIAL sob NOSSA · gate vê execução). Estado 'plano' restaurado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
