#!/usr/bin/env python3
"""
fechar-instancia.py — o GATE de fechamento do Potencial Urbano (mecanismo D83 do escritório).

Modo de falha nº1 (MOU): "as instâncias perdem dados / declaram feito sem provar feito". Causa-raiz:
"declarei feito" ≠ "PROVEI feito" — fecha-se por memória, não por verificação. Este script é a
Definition of Done MECÂNICA do encerramento: princípio reincidentemente violado vira MECANISMO.

Checagens (todas determinísticas, sem rede):
  1. EVALS    — evals/rodar-evals.py sai 0 (nenhum ground-truth ATIVO quebrado; citação correta).
  2. ENGINE   — engines/tdc/oodc.py sai 0 (as fórmulas conferem; número nasce no engine, 1.3).
  2b.ENGINE CEDENTE — engines/tdc/pcpt.py --demo sai 0 (Fi escalonado Art.24 LPUOS; T2).
  2c.PRODUTO  — evals/eval-produto.py sai 0 (golden Fi legal sobre 7 cedentes reais; sabotar 1 Fi FALHA; T2).
  3. CORPUS   — nenhum stray tag de tool-call (</invoke> etc.) contaminando o verbatim/índice.
  4. MANIFESTO— regenerar é idempotente: rodar consolidar.py NÃO muda MANIFESTO.json (estava atualizado).
  5. BACKLOG  — BACKLOG.md (HEADER) carrega "Atualizado: <hoje>" (senão a próxima sessão vê backlog velho como novo).
  6. GIT      — working tree limpo E HEAD pushado (SOFT: só avisam; não-commitado/não-pushado = não-durável).

ESCOPO HONESTO (F-4): isto prova 5 INVARIANTES MECÂNICAS de CONTEÚDO + 2 avisos de durabilidade.
NÃO substitui o julgamento e NÃO cobre: regressão dos 14 municipais, links dos docs, handoff atualizado,
mérito jurídico. "Gate verde" = esses 5 eixos passaram, não "tudo certo".

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


def check_engine_cedente():
    # T2/S2: o engine de CEDENTE (pcpt.py, Fi Art. 24 LPUOS) também é gate — antes só o oodc rodava.
    rc, _ = _run(["engines/tdc/pcpt.py", "--demo"])
    return rc == 0, "engine cedente PCpt (Fi escalonado) auto-teste OK" if rc == 0 else f"pcpt quebrou (exit {rc})"


def check_produto():
    # T2/S2: golden-assert do Fi legal sobre 7 cedentes reais; sabotar 1 Fi (engine ou CSV) FALHA aqui.
    rc, _ = _run(["evals/eval-produto.py"])
    return rc == 0, "produto: 7 cedentes reais c/ Fi legal (Art.24) OK" if rc == 0 else f"produto divergiu do Fi legal (exit {rc})"


def check_conservacao():
    # T4: gate de conservação (Art. 129) 3-estados; Termo→PENDENTE e RES.(tombamento)→SEM_ATESTADO,
    # nunca ELEGIVEL. Fixtures FALHAM se a regra regredir.
    rc, _ = _run(["zepec/montar_base.py", "--autoteste"])
    return rc == 0, "conservação: Atestado=ELEGIVEL·Termo=PENDENTE·RES=SEM_ATESTADO OK" if rc == 0 else f"conservação regrediu (exit {rc})"


def check_regime_pcpt():
    # T3: já-declarado (Art.125 §1º I) não recebe o escalonado como valor firme; prospecção-nova sim (Art.24).
    rc, _ = _run(["zepec/enriquecer_oficial.py", "--autoteste"])
    return rc == 0, "regime PCpt: já-declarado=PENDENTE·prospecção=estimativa OK" if rc == 0 else f"regime PCpt regrediu (exit {rc})"


def check_divergencia():
    # M0: a divergência PCpt×certidões é SURFAÇADA e 100% flagada (nunca escondida/firme).
    rc, _ = _run(["evals/eval-divergencia-pcpt.py"])
    return rc == 0, "divergência PCpt×certidões surfaçada e flagada OK" if rc == 0 else f"divergência não surfaçada/flagada (exit {rc})"


def check_dominio():
    # Separação TDC×IPTU (plano 2026-07-04): (1) toda norma/acórdão carimbada com dominio válido;
    # (2) as invariantes de roteamento (não-poluição, não-perda, PDE alcançável do TDC, anti-padrão
    # eliminado) provadas. Sabotar o carimbo ou vazar iptu-puro numa consulta tdc FALHA aqui.
    rc1, _ = _run(["scripts/carimbar_dominio.py", "--check"])
    if rc1 != 0:
        return False, f"carimbo de domínio incompleto (exit {rc1}) — rode scripts/carimbar_dominio.py"
    rc2, _ = _run(["evals/eval-dominio.py"])
    return rc2 == 0, ("domínio TDC×IPTU: carimbo válido + roteamento provado OK" if rc2 == 0
                      else f"invariantes de domínio regrediram (exit {rc2}) — rode evals/eval-dominio.py")


def check_indice_arrumacao():
    # Arrumação Drive: o SEED bate com o de-para e o MESTRE bate com o reconciliado (SEED+logs).
    # Protege contra drift (alguém edita o índice à mão ou o de-para muda sem re-semear).
    rc1, _ = _run(["scripts/semear_indice_mestre.py", "--check"])
    if rc1 != 0:
        return False, f"INDICE-SEED desatualizado vs de-para (exit {rc1}) — rode semear_indice_mestre.py"
    rc2, _ = _run(["scripts/reconciliar_arrumacao.py", "--check"])
    return rc2 == 0, ("índice de arrumação consistente (SEED×de-para, MESTRE×reconciliado)" if rc2 == 0
                      else f"INDICE-MESTRE desatualizado (exit {rc2}) — rode reconciliar_arrumacao.py")


def check_disclaimer():
    # M0: DISCLAIMER.md existe E o bloco está injetado na saída ao cliente (COMO-USAR.md).
    disc = RAIZ / "DISCLAIMER.md"
    como = RAIZ / "zepec" / "ferramenta" / "COMO-USAR.md"
    if not disc.exists():
        return False, "DISCLAIMER.md ausente na raiz"
    if not como.exists() or "DISCLAIMER-BLOCO-INICIO" not in como.read_text(encoding="utf-8"):
        return False, "bloco DISCLAIMER não injetado em zepec/ferramenta/COMO-USAR.md"
    return True, "DISCLAIMER.md + bloco na saída ao cliente OK"


def check_stray_tags():
    # Só a CORPUS-DATA importa: num .md/.json de lei/jurisprudência/índice, uma tag de tool-call é
    # SEMPRE corrupção (já aconteceu: </invoke> vazou para a 7228 e o índice). Código .py é excluído
    # de propósito — pode conter o token legitimamente (este próprio gate define a regex como string).
    # B-13/F-3: além do corpus, varre os dados que alimentam evals/engine/produto (ground-truth,
    # tabelas, tese, extração) + .csv — uma tag vazada ali contamina silenciosamente. .py fica de fora
    # (pode conter o token legitimamente, como este próprio gate).
    alvo = ["leis", "rag", "jurisprudencia", "evals/ground-truth", "tabelas", "tese", "extracao"]
    rx = re.compile(r"</?(invoke|content|parameter|function)>")
    sujos = []
    for base in alvo:
        for p in (RAIZ / base).rglob("*"):
            if not p.is_file() or p.suffix not in (".json", ".md", ".txt", ".csv"):
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
    # F-7: compara contra HEAD (o commitado), não contra o índice de staging.
    d = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", "MANIFESTO.json"], cwd=RAIZ)
    if d.returncode == 0:
        return True, "MANIFESTO.json commitado == regenerado (idempotente)"
    return False, "MANIFESTO.json regenerado difere do commitado — rode consolidar e re-commite"


def check_backlog_fresh():
    hoje = datetime.date.today().isoformat()
    bp = RAIZ / "BACKLOG.md"
    if not bp.exists():
        return False, "BACKLOG.md ausente — o mecanismo anti-perda depende dele"
    txt = bp.read_text(encoding="utf-8")
    # F-5: ancora à LINHA do header (`**Atualizado: <hoje>.**`), não a qualquer ocorrência da data
    # (senão uma data no rastro/exemplo passa o check com o header velho).
    if re.search(rf"(?m)^\s*>?\s*\*\*Atualizado:\s*{re.escape(hoje)}", txt):
        return True, f"BACKLOG.md (header) atualizado hoje ({hoje})"
    return False, f"BACKLOG.md sem header 'Atualizado: {hoje}' — atualize a data do header e revise as ABERTAS"


def check_git_clean():
    p = subprocess.run(["git", "status", "--porcelain"], cwd=RAIZ, capture_output=True, text=True)
    sujo = [l for l in p.stdout.splitlines() if l.strip()]
    return (not sujo), "working tree limpo" if not sujo else f"{len(sujo)} arquivo(s) não-commitado(s) — commite+push antes de fechar (trabalho não-durável)"


def check_pushed():
    """F-4: 'commitei' ≠ 'pushei'. Conta commits locais à frente do upstream."""
    r = subprocess.run(["git", "rev-list", "--count", "@{u}..HEAD"], cwd=RAIZ,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return True, "sem upstream configurado (não dá p/ checar push)"
    n = (r.stdout or "0").strip()
    return (n == "0"), "HEAD pushado (== upstream)" if n == "0" else f"{n} commit(s) NÃO pushado(s) — trabalho não-durável"


def main():
    hard = [
        ("EVALS (citação correta, 1.7)", check_evals),
        ("ENGINE (número no engine, 1.3)", check_engine),
        ("ENGINE CEDENTE (Fi Art.24, T2)", check_engine_cedente),
        ("PRODUTO (golden Fi cedentes reais, T2)", check_produto),
        ("CONSERVAÇÃO (Art.129 3-estados, T4)", check_conservacao),
        ("REGIME PCpt (já-declarado×novo, T3)", check_regime_pcpt),
        ("DIVERGÊNCIA PCpt×certidões (M0)", check_divergencia),
        ("DOMÍNIO TDC×IPTU (metadado, roteamento)", check_dominio),
        ("ÍNDICE ARRUMAÇÃO (SEED×de-para, MESTRE×reconc.)", check_indice_arrumacao),
        ("DISCLAIMER injetado (M0)", check_disclaimer),
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
    # SOFT (não derrubam o gate, mas avisam — durabilidade não é invariante mecânica do conteúdo)
    for nome, fn in (("GIT limpo", check_git_clean), ("GIT pushado", check_pushed)):
        ok, msg = fn()
        print(f"  [{'verde ' if ok else 'AVISO '}] {nome} (durabilidade): {msg}")

    print("─────────────────────────────────────────────────────────────────────────────")
    if falhou:
        print("VERMELHO — há pendência MECÂNICA. NÃO declare 'fechado' até ficar verde.")
        sys.exit(1)
    print("VERDE — os checks mecânicos passaram. (Ainda assim: atualize o BACKLOG e o handoff com o julgamento.)")
    sys.exit(0)


if __name__ == "__main__":
    main()
