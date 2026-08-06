#!/usr/bin/env python3
"""
gate-arrumacao.py — GATE MECÂNICO da arrumação do Drive + separação TDC×IPTU.
Espelha `scripts/fechar-instancia.py` ("declarei feito" ≠ "provei feito") para a frente de arrumação.

7 checagens (docs/PLANO-ARRUMACAO-DRIVE-2026-07-04.md §6). Divididas em:
  LOCAL (provável AGORA, sem tocar o Drive) — bloqueiam:
    C6. dominio ∈ {tdc,iptu,compartilhado} em toda norma/acórdão (carimbar_dominio --check).
    C7. dominio_primario não-vazio em toda lei/jurisprudência.
    C8. tema[] não contém mais 'IPTU'/'TDC' (anti-padrão eliminado) + roteamento provado (eval-dominio).
  DRIVE (execução — dependem do índice, alimentado pelos logs do GAS) — PENDENTE até a arrumação rodar:
    C1. '01 — _entrada' com 0 arquivos soltos.
    C3. índice tem drive_id + destino_path em toda linha.
    C4. nenhum OFICIAL em quarentena/98/99.
    C5. todo item 'moved' tem hash_md5 REAL (vazio/PENDENTE conta como ausente — A-07).

LIMITE HONESTO (A-08, auditoria 2026-07-05): a prova DRIVE repousa nos LOGS que o dono cola de volta
(`gas-log-*.txt`) — NENHUM check confronta o índice com o Drive AO VIVO (não há credencial aqui). O que
o plano §6 chama de "C2 contagem por pasta" e "C3 bate com o Drive" NÃO existe como confronto real:
C3 aqui só valida campos do índice. Portanto "arrumação provada" = "os logs do GAS são consistentes",
não "o Drive foi auditado". Um confronto real com o Drive (via MCP, sob o gate do dono) é BACKLOG.

Enquanto o índice não existir, C1–C5 saem [PENDENTE] (não bloqueiam — a onda Drive ainda não correu).

Uso:  python3 scripts/gate-arrumacao.py
"""
import csv
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PY = sys.executable
CONFRONTACAO = RAIZ / "inventario" / "confrontacao-drive.json"
MESTRE = RAIZ / "inventario" / "INDICE-MESTRE-DRIVE.csv"   # estado REAL (reconciliador)
SEED = RAIZ / "inventario" / "INDICE-SEED.csv"             # o PLANO (seeder)
INDICE = MESTRE if MESTRE.exists() else SEED               # lê o real; cai no plano se ainda não reconciliou
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


# ---------- DRIVE (pendentes até o índice existir) ----------
MOVIDO = ("moved", "espelhado", "quarentena")           # saiu da _entrada de verdade
# R11 — estados TERMINAIS deliberados: não "movidos", mas também NÃO pendentes (senão falso-vermelho
# eterno). 'triagem' = multi-pai/ambíguo p/ decisão humana (99); 'nativo_ignorado' = Google-nativo
# que o dedup pula de propósito. Contam como RESOLVIDOS no C1, fora do denominador de "ainda na _entrada".
TERMINAL = ("triagem", "nativo_ignorado", "excluido")   # 'excluido' = exclusão física D-DONO-2026-07-18 (R11)
RESOLVIDO = MOVIDO + TERMINAL


def _indice_rows():
    with open(INDICE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _fase():
    """Fase da arrumação: 'sem-indice' | 'plano' (nada movido ainda) | 'execucao' (algo movido)."""
    if not INDICE.exists():
        return "sem-indice"
    rows = _indice_rows()
    movidos = [r for r in rows if (r.get("status_arrumacao") or "").strip() in MOVIDO]
    return "execucao" if movidos else "plano"


def c1_entrada_vazia():
    if not INDICE.exists():
        return None, "índice ausente — onda Drive ainda não correu"
    rows = _indice_rows()
    if _fase() == "plano":
        return None, f"PLANO pronto: {len(rows)} itens carimbados, 0 movidos — execução no Drive PENDENTE"
    # Em execução: 'resolvido' = movido OU terminal-deliberado (R11). Só o que ainda não saiu conta.
    pendentes = [r for r in rows if (r.get("status_arrumacao") or "").strip() not in RESOLVIDO]
    return (not pendentes), (f"0 pendentes (todos movidos/quarentenados/triados)"
                             if not pendentes else f"{len(pendentes)}/{len(rows)} ainda não resolvidos")


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
    # B-07 (auditoria): OFICIAL não pode estar em quarentena NEM em 98/99 (zona morta/triagem) — antes
    # só 'quarentena' era checado, então um OFICIAL roteado a triagem/99 escapava.
    def _zona_morta(r):
        st = (r.get("status_arrumacao") or "").strip()
        dst = (r.get("destino_path") or "").strip()
        return st in ("quarentena", "triagem") or dst.startswith("98") or dst.startswith("99")
    viol = [r for r in rows if (r.get("proveniencia") or "").strip().upper().startswith("OFI") and _zona_morta(r)]
    return (not viol), ("nenhum OFICIAL em quarentena/98/99" if not viol
                        else f"{len(viol)} OFICIAL em quarentena/98/99 — REVISAR")


def c5_moved_tem_hash():
    if not INDICE.exists():
        return None, "índice-mestre ausente"
    rows = _indice_rows()
    # A-07 (auditoria): 'PENDENTE' (placeholder do SEED) e '' contam como AUSENTE — senão mover 1.360
    # itens com a Drive API desligada (md5 vazio) deixava hash_md5='PENDENTE' e o C5 passava VERDE.
    def _sem_hash(r):
        h = (r.get("hash_md5") or "").strip()
        return h == "" or h == "PENDENTE"
    viol = [r for r in rows if (r.get("status_arrumacao") or "").strip() in ("moved", "espelhado") and _sem_hash(r)]
    return (not viol), ("todo item movido tem hash_md5 real" if not viol
                        else f"{len(viol)} movidos sem hash_md5 (vazio ou PENDENTE)")


def c2_confrontacao_drive():
    """AUD-A08: lê o resultado da última confrontação índice×Drive (MCP ou script)."""
    if not CONFRONTACAO.exists():
        return None, "confrontacao-drive.json ausente — rodar confrontação via MCP Drive"
    try:
        c = json.loads(CONFRONTACAO.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return False, "confrontacao-drive.json malformado"
    dt = c.get("data_confrontacao", "")
    try:
        dias = (date.today() - date.fromisoformat(dt)).days
    except ValueError:
        return False, f"data_confrontacao inválida: {dt!r}"
    res = c.get("resultado", {})
    status = res.get("status", "?")
    total = res.get("total_indice", "?")
    movidos = res.get("movidos_real", "?")
    msg = f"confrontação {dt} ({dias}d atrás): {movidos}/{total} movidos, status={status}"
    if dias > 30:
        return False, msg + " — STALE (>30 dias, reconferir)"
    return True, msg


def main():
    print("═══ GATE DA ARRUMAÇÃO — Drive + TDC×IPTU (D83: 'declarei' ≠ 'provei') ═══")
    bloqueiam = [
        ("C6/C7 CARIMBO domínio (vocab fechado + dominio_primario)", c6_c7_carimbo),
        ("C8 ANTI-PADRÃO + ROTEAMENTO (eval-dominio)", c8_roteamento),
    ]
    drive = [
        ("C1 _entrada com 0 soltos", c1_entrada_vazia),
        ("C2 confrontação índice×Drive (AUD-A08)", c2_confrontacao_drive),
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
    # R12 — contrato de exit-code: por padrão o gate sai 0 em 'plano' (a parte LOCAL está provada e o
    # PLANO pronto). Um consumidor automático que exige o DRIVE executado passa --require-executed:
    # aí 'sem-indice'/'plano' saem !=0 (o Drive ainda não foi arrumado — não pode ser lido como verde).
    require_exec = "--require-executed" in sys.argv
    if fase == "sem-indice":
        print("VERDE (parte LOCAL) — domínio carimbado e roteamento provado. "
              "Parte DRIVE (C1–C5) PENDENTE: aguarda o seeder/execução gerar o índice.")
    elif fase == "plano":
        print("VERDE (LOCAL) + PLANO DRIVE pronto — índice semeado, mas NADA foi movido no Drive ainda "
              "(status=carimbado). NÃO declare 'Drive arrumado': falta rodar o Apps Script e reconciliar. "
              "'declarei' ≠ 'provei'.")
    else:
        print("VERDE — arrumação provada (local + Drive executado + reconciliado).")
    if require_exec and fase != "execucao":
        print(f"  (--require-executed: fase '{fase}' ≠ 'execucao' → exit 4 p/ o consumidor automático)")
        sys.exit(4)
    sys.exit(0)


if __name__ == "__main__":
    main()
