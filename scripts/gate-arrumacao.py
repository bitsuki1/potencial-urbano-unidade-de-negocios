#!/usr/bin/env python3
"""
gate-arrumacao.py — GATE MECÂNICO da arrumação do Drive + separação TDC×IPTU.
Espelha `scripts/fechar-instancia.py` ("declarei feito" ≠ "provei feito") para a frente de arrumação.

8 checagens do plano (docs/PLANO-ARRUMACAO-DRIVE-2026-07-04.md §6). Divididas em:
  LOCAL (provável AGORA, sem tocar o Drive) — bloqueiam:
    C6. dominio ∈ {tdc,iptu,compartilhado} em toda norma/acórdão (carimbar_dominio --check).
    C7. dominio_primario não-vazio em toda lei/jurisprudência.
    C8. tema[] não contém mais 'IPTU'/'TDC' (anti-padrão eliminado) + roteamento provado (eval-dominio).
  DRIVE (execução — dependem do índice-mestre `inventario/INDICE-MESTRE-DRIVE.csv`) — PENDENTE até
  a arrumação rodar; reportadas honestamente, não fingidas:
    C1. '01 — _entrada' com 0 arquivos soltos.
    C2. toda pasta-alvo com a contagem esperada (bate com o índice).
    C3. índice-mestre bate com o Drive (todo drive_id existe; todo arquivo está no índice).
    C4. nenhum OFICIAL em 98/99/quarentena.
    C5. todo item 'moved' tem hash_sha256.

Enquanto o índice-mestre não existir, C1–C5 saem [PENDENTE] (não bloqueiam — a onda Drive ainda não
correu); quando existir, passam a bloquear. Assim o gate cresce com a execução, sem falso-verde.

Uso:  python3 scripts/gate-arrumacao.py
"""
import csv
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PY = sys.executable
INDICE = RAIZ / "inventario" / "INDICE-MESTRE-DRIVE.csv"
VOCAB = {"tdc", "iptu", "compartilhado"}


def _run(args):
    p = subprocess.run([PY, *args], cwd=RAIZ, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


# ---------- LOCAL (bloqueiam) ----------
def c6_c7_carimbo():
    rc, out = _run(["scripts/carimbar_dominio.py", "--check"])
    return rc == 0, (out.strip().splitlines()[-1] if out.strip() else "carimbo verificado")


def c8_roteamento():
    rc, out = _run(["evals/eval-dominio.py"])
    linha = next((l for l in out.splitlines() if "eval-dominio" in l), "eval-dominio")
    return rc == 0, linha.strip()


# ---------- DRIVE (pendentes até o índice-mestre existir) ----------
ARRUMADO = ("moved", "espelhado", "quarentena")  # status que significam "saiu da _entrada de verdade"


def _indice_rows():
    with open(INDICE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _fase():
    """Fase da arrumação: 'sem-indice' | 'plano' (nada movido ainda) | 'execucao' (algo movido)."""
    if not INDICE.exists():
        return "sem-indice"
    rows = _indice_rows()
    movidos = [r for r in rows if (r.get("status_arrumacao") or "").strip() in ARRUMADO]
    return "execucao" if movidos else "plano"


def c1_entrada_vazia():
    if not INDICE.exists():
        return None, "índice-mestre ausente — onda Drive ainda não correu"
    rows = _indice_rows()
    # "arrumado" = status ∈ ARRUMADO. Enquanto 'planejado', o arquivo AINDA está na _entrada física
    # (o Apps Script não rodou) — NÃO é falso-verde: reporta o pendente honestamente.
    pendentes = [r for r in rows if (r.get("status_arrumacao") or "").strip() not in ARRUMADO]
    if _fase() == "plano":
        return None, f"PLANO pronto: {len(rows)} itens planejados, 0 movidos — execução no Drive PENDENTE"
    return (not pendentes), (f"0 arquivos pendentes na _entrada"
                             if not pendentes else f"{len(pendentes)}/{len(rows)} ainda não movidos")


def c3_indice_bate():
    if not INDICE.exists():
        return None, "índice-mestre ausente"
    rows = _indice_rows()
    sem_id = [r for r in rows if not (r.get("drive_id") or "").strip()]
    sem_destino = [r for r in rows if not (r.get("destino_path") or "").strip()]
    ok = not sem_id and not sem_destino
    return ok, (f"{len(rows)} linhas: todo drive_id e destino_path preenchidos" if ok
                else f"{len(sem_id)} sem drive_id, {len(sem_destino)} sem destino_path")


def c4_oficial_fora_quarentena():
    if not INDICE.exists():
        return None, "índice-mestre ausente"
    rows = _indice_rows()
    viol = [r for r in rows if (r.get("proveniencia") or "").strip().upper().startswith("OFI")
            and (r.get("status_arrumacao") or "").strip() == "quarentena"]
    return (not viol), ("nenhum OFICIAL em quarentena" if not viol else f"{len(viol)} OFICIAL em quarentena — REVISAR")


def c5_moved_tem_hash():
    if not INDICE.exists():
        return None, "índice-mestre ausente"
    rows = _indice_rows()
    viol = [r for r in rows if (r.get("status_arrumacao") or "").strip() in ("moved", "espelhado")
            and not (r.get("hash_sha256") or "").strip()]
    return (not viol), ("todo item movido tem hash" if not viol else f"{len(viol)} movidos sem hash_sha256")


def main():
    print("═══ GATE DA ARRUMAÇÃO — Drive + TDC×IPTU (D83: 'declarei' ≠ 'provei') ═══")
    bloqueiam = [
        ("C6/C7 CARIMBO domínio (vocab fechado + dominio_primario)", c6_c7_carimbo),
        ("C8 ANTI-PADRÃO + ROTEAMENTO (eval-dominio)", c8_roteamento),
    ]
    drive = [
        ("C1 _entrada com 0 soltos", c1_entrada_vazia),
        ("C3 índice-mestre bate com o Drive", c3_indice_bate),
        ("C4 nenhum OFICIAL em quarentena", c4_oficial_fora_quarentena),
        ("C5 todo movido tem hash", c5_moved_tem_hash),
    ]
    falhou = False
    for nome, fn in bloqueiam:
        ok, msg = fn()
        print(f"  [{'VERDE ' if ok else 'VERMELHO'}] {nome}: {msg}")
        falhou = falhou or not ok
    for nome, fn in drive:
        ok, msg = fn()
        tag = "PENDENTE" if ok is None else ("VERDE " if ok else "VERMELHO")
        print(f"  [{tag}] {nome}: {msg}")
        if ok is False:
            falhou = True
    print("──────────────────────────────────────────────────────────────────────")
    if falhou:
        print("VERMELHO — pendência MECÂNICA na arrumação. Não declare 'arrumado'.")
        sys.exit(1)
    fase = _fase()
    if fase == "sem-indice":
        print("VERDE (parte LOCAL) — domínio carimbado e roteamento provado. "
              "Parte DRIVE (C1–C5) PENDENTE: aguarda a onda de execução no Drive gerar o índice-mestre.")
    elif fase == "plano":
        print("VERDE (LOCAL) + PLANO DRIVE pronto — índice-mestre semeado, mas NADA foi movido no Drive "
              "ainda (status=planejado). NÃO declare 'Drive arrumado': falta rodar o Apps Script e "
              "reconciliar. 'declarei' ≠ 'provei'.")
    else:
        print("VERDE — arrumação provada (local + Drive executado).")
    sys.exit(0)


if __name__ == "__main__":
    main()
