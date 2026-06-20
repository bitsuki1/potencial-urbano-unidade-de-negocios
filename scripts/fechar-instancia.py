#!/usr/bin/env python3
"""
fechar-instancia.py — o GATE de fechamento do Potencial Urbano (mecanismo D83 do escritório).

Modo de falha nº1 (MOU): "as instâncias perdem dados / declaram feito sem provar feito". Causa-raiz:
"declarei feito" ≠ "PROVEI feito" — fecha-se por memória, não por verificação. Este script é a
Definition of Done MECÂNICA do encerramento: princípio reincidentemente violado vira MECANISMO.

Checagens (todas determinísticas, sem rede):
  1. EVALS    — evals/rodar-evals.py sai 0 (nenhum ground-truth ATIVO quebrado; citação correta).
  2. ENGINE   — engines/tdc/oodc.py sai 0 (as fórmulas conferem; número nasce no engine, 1.3).
  3. CORPUS   — nenhum stray tag de tool-call (</invoke> etc.) contaminando o verbatim/índice.
  4. MANIFESTO— regenerar é idempotente: rodar consolidar.py NÃO muda MANIFESTO.json (estava atualizado).
  5. BACKLOG  — BACKLOG.md carrega "Atualizado: <hoje>" (senão a próxima sessão vê backlog velho como novo).
  6. GIT      — working tree limpo (SOFT: só avisa; trabalho não-commitado não é durável).

Sai 0 = VERDE (pode fechar). Sai 1 = pendência mecânica → resolva ANTES de declarar "fechado".
Uso:  python3 scripts/fechar-instancia.py
Trazido pela instância orquestradora do PU — aplicação do "ladrão" do escritório (2026-06-20).
"""
import datetime
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PY = sys.executable or "python3"


def _run(args):
    p = subprocess.run([PY, *args], cwd=RAIZ, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def check_evals():
    rc, _ = _run(["evals/rodar-evals.py"])
    return rc == 0, "evals/rodar-evals.py saiu 0" if rc == 0 else f"evals quebrou (exit {rc}) — rode e veja FALHA"


def check_engine():
    rc, _ = _run(["engines/tdc/oodc.py"])
    return rc == 0, "engine OODC/TDC auto-teste OK" if rc == 0 else f"engine quebrou (exit {rc})"


def check_stray_tags():
    # Só a CORPUS-DATA importa: num .md/.json de lei/jurisprudência/índice, uma tag de tool-call é
    # SEMPRE corrupção (já aconteceu: </invoke> vazou para a 7228 e o índice). Código .py é excluído
    # de propósito — pode conter o token legitimamente (este próprio gate define a regex como string).
    alvo = ["leis", "rag", "jurisprudencia"]
    rx = re.compile(r"</?(invoke|content|parameter|function)>")
    sujos = []
    for base in alvo:
        for p in (RAIZ / base).rglob("*"):
            if not p.is_file() or p.suffix not in (".json", ".md", ".txt"):
                continue
            try:
                if rx.search(p.read_text(encoding="utf-8")):
                    sujos.append(str(p.relative_to(RAIZ)))
            except (UnicodeDecodeError, OSError):
                pass
    return (not sujos), "sem stray tags no corpus/índice" if not sujos else f"stray tags em: {sujos[:5]}"


def check_manifesto_idempotente():
    rc, _ = _run(["scripts/consolidar.py"])
    if rc != 0:
        return False, f"consolidar.py quebrou (exit {rc})"
    d = subprocess.run(["git", "diff", "--quiet", "MANIFESTO.json"], cwd=RAIZ)
    if d.returncode == 0:
        return True, "MANIFESTO.json já estava atualizado (idempotente)"
    return False, "MANIFESTO.json mudou ao regenerar — você commitou um MANIFESTO velho? rode consolidar e re-commite"


def check_backlog_fresh():
    hoje = datetime.date.today().isoformat()
    bp = RAIZ / "BACKLOG.md"
    if not bp.exists():
        return False, "BACKLOG.md ausente — o mecanismo anti-perda depende dele"
    txt = bp.read_text(encoding="utf-8")
    if f"Atualizado: {hoje}" in txt or f"Atualizado:** {hoje}" in txt:
        return True, f"BACKLOG.md atualizado hoje ({hoje})"
    return False, f"BACKLOG.md sem 'Atualizado: {hoje}' — atualize a data e revise as ABERTAS antes de fechar"


def check_git_clean():
    p = subprocess.run(["git", "status", "--porcelain"], cwd=RAIZ, capture_output=True, text=True)
    sujo = [l for l in p.stdout.splitlines() if l.strip()]
    return (not sujo), "working tree limpo" if not sujo else f"{len(sujo)} arquivo(s) não-commitado(s) — commite+push antes de fechar (trabalho não-durável)"


def main():
    hard = [
        ("EVALS (citação correta, 1.7)", check_evals),
        ("ENGINE (número no engine, 1.3)", check_engine),
        ("CORPUS (sem stray tags)", check_stray_tags),
        ("MANIFESTO (idempotente, SSOT)", check_manifesto_idempotente),
        ("BACKLOG (fresco, D83)", check_backlog_fresh),
    ]
    print("═══ GATE DE FECHAMENTO — Potencial Urbano (D83: 'declarei feito' ≠ 'provei feito') ═══")
    falhou = False
    for nome, fn in hard:
        ok, msg = fn()
        print(f"  [{'VERDE ' if ok else 'VERMELHO'}] {nome}: {msg}")
        falhou = falhou or not ok
    # SOFT (não derruba o gate, mas avisa)
    ok, msg = check_git_clean()
    print(f"  [{'verde ' if ok else 'AVISO '}] GIT (durabilidade): {msg}")

    print("─────────────────────────────────────────────────────────────────────────────")
    if falhou:
        print("VERMELHO — há pendência MECÂNICA. NÃO declare 'fechado' até ficar verde.")
        sys.exit(1)
    print("VERDE — os checks mecânicos passaram. (Ainda assim: atualize o BACKLOG e o handoff com o julgamento.)")
    sys.exit(0)


if __name__ == "__main__":
    main()
