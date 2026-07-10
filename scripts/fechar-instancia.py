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


def check_pii_arvore():
    """L-T7-1: nenhum .csv/.json com coluna PII deve estar na árvore git (zepec/ exceto ferramenta/).
    zepec/ferramenta/ excluído: é a saída do produto (cedentes) — proprietario é esperado (D-DONO-17)."""
    tokens_pii = {"proprietario", "contribuinte", "documento", "cpf", "cnpj"}
    r = subprocess.run(
        ["git", "ls-files", "zepec/limpo", "zepec/oficial", "zepec/raw"],
        cwd=RAIZ, capture_output=True, text=True,
    )
    sujos = []
    for rel in r.stdout.splitlines():
        rel = rel.strip()
        if not rel:
            continue
        if not (rel.endswith(".csv") or rel.endswith(".json")):
            continue
        fp = RAIZ / rel
        try:
            with open(fp, encoding="utf-8") as fh:
                header = fh.readline().lower()
        except (OSError, UnicodeDecodeError):
            continue
        if any(tok in header for tok in tokens_pii):
            sujos.append(rel)
    if sujos:
        return False, f"PII rastreada no git: {sujos[:5]}"
    return True, "nenhum arquivo com coluna PII na árvore git (zepec/)"


def check_pii_historico():
    """L-T7-2: verifica se arquivos com PII conhecidos ainda existem no histórico git.
    Mesmo removidos do HEAD, continuam acessíveis via git log. Rewrite do histórico
    (git filter-branch / git filter-repo) requer autorização do dono — por isso é WARNING, não FAIL."""
    # Arquivos PII conhecidos (removidos do HEAD mas possivelmente no histórico)
    pii_conhecidos = {"zepec/limpo/donos_encontrados.csv"}
    # Busca arquivos deletados no histórico dentro das pastas zepec de dados
    r = subprocess.run(
        ["git", "log", "--all", "--diff-filter=D", "--name-only", "--pretty=format:",
         "--", "zepec/limpo/*.csv", "zepec/oficial/*.csv", "zepec/raw/*.csv"],
        cwd=RAIZ, capture_output=True, text=True,
    )
    if r.returncode != 0:
        # Se o git log falhar, não bloqueia — reporta e segue
        return True, "git log falhou ao varrer histórico (não-fatal)"
    # Filtra linhas vazias e deduplica
    deletados = {l.strip() for l in r.stdout.splitlines() if l.strip()}
    encontrados = sorted(deletados & pii_conhecidos)
    if encontrados:
        # WARNING: retorna True (não reprova o gate) mas avisa
        return True, f"AVISO — PII em histórico git (requer rewrite c/ autorização do dono): {encontrados}"
    return True, "nenhum arquivo PII conhecido no histórico git"


def check_oraculos_ausente():
    """L-T6-1: engines/tdc/oraculos/ NÃO deveria existir (Fi vem do CSV, não de oráculo)."""
    p = RAIZ / "engines" / "tdc" / "oraculos"
    if p.exists() and any(p.iterdir()):
        return False, f"engines/tdc/oraculos/ NÃO deveria existir (T6 — Fi vem do CSV, não de oráculo)"
    return True, "engines/tdc/oraculos/ ausente (T6 OK — sem oráculo)"


def check_evals():
    rc, _ = _run(["evals/rodar-evals.py"])
    return rc == 0, "evals/rodar-evals.py saiu 0" if rc == 0 else f"evals quebrou (exit {rc}) — rode e veja FALHA"


def check_engine():
    rc, _ = _run(["engines/tdc/oodc.py"])
    return rc == 0, "engine OODC/TDC auto-teste OK" if rc == 0 else f"engine quebrou (exit {rc})"


def check_engine_fp():
    rc, _ = _run(["engines/tdc/fp.py"])
    return rc == 0, "engine Fp (Quadro 6) auto-teste OK" if rc == 0 else f"Fp quebrou (exit {rc})"


def check_engine_cedente():
    # T2/S2: o engine de CEDENTE (pcpt.py, Fi Art. 24 LPUOS) também é gate — antes só o oodc rodava.
    rc, _ = _run(["engines/tdc/pcpt.py", "--demo"])
    return rc == 0, "engine cedente PCpt (Fi escalonado) auto-teste OK" if rc == 0 else f"pcpt quebrou (exit {rc})"


def check_engine_art128():
    # Preço LEGAL (Art. 128 PDE): numerador PCpt×VTcd + referência ÷CAmaxcd(=4 §1º) + §2º IPCA.
    # O --demo roda o auto-teste; o eval-art128 confronta a equação verbatim + 3.334 cedentes reais.
    rc, _ = _run(["engines/tdc/art128.py", "--demo"])
    if rc != 0:
        return False, f"art128 (preço legal) quebrou (exit {rc})"
    rc2, _ = _run(["evals/eval-art128.py"])
    return rc2 == 0, "engine preço legal Art. 128 (numerador + ÷CAmaxcd + IPCA) + prova OK" if rc2 == 0 else f"eval-art128 falhou (exit {rc2})"


def check_produto_dossie():
    # M1 produto: o dossiê 1-página bate o preço no art128 + tem conservação/checklist citados,
    # e o funil de completude é monotônico (número por estágio). Falha se o dossiê inventar ou o funil furar.
    rc, _ = _run(["zepec/gerar_dossie.py", "--autoteste"])
    if rc != 0:
        return False, f"dossiê quebrou (exit {rc})"
    rc2, _ = _run(["zepec/funil.py"])
    return rc2 == 0, "produto M1 (dossiê citado + funil) OK" if rc2 == 0 else f"funil quebrou (exit {rc2})"


def check_fatores_tdc():
    # M4: inventário de fatores TDC (tabelas/fatores-tdc.csv) — nenhum 'verificado' sem chunk+eval gated.
    rc, _ = _run(["scripts/gate_fatores_tdc.py"])
    return rc == 0, "inventário de fatores TDC (chunk real + eval gated) OK" if rc == 0 else f"fatores-tdc falhou (exit {rc})"


def check_engine_iptu():
    # IPTU aberto pelo dono em 2026-07-10 ("finalizarmos as duas frentes"): motor VV×alíquota
    # progressiva por porção (Lei 6.989/1966 arts. 7/8/27 + 7-A/8-A/28; Lei 10.235/1986; faixas
    # Lei 15.889/2013). Demo ancorado em valores derivados à mão da lei.
    rc, _ = _run(["engines/iptu/iptu.py", "--demo"])
    return rc == 0, "engine IPTU (VV × alíquota por porção) auto-teste OK" if rc == 0 else f"iptu quebrou (exit {rc})"


def check_eval_iptu():
    # Golden independente do motor IPTU: âncoras recomputadas + dupla-via CSV×engine + mutação.
    rc, _ = _run(["evals/eval-iptu.py"])
    return rc == 0, "eval-iptu: âncoras da lei + dupla-via + mutação OK" if rc == 0 else f"eval-iptu falhou (exit {rc})"


def check_eval_iptu_oficial():
    # Confronto do VV de terreno (Art. 4º) contra o lançamento REAL da Prefeitura (3.905 cedentes,
    # insumos oficiais do IPTU_2026). Terrenos Normais: engine reproduz EXATO área×valor_m2_terreno.
    rc, _ = _run(["evals/eval-iptu-oficial.py"])
    return rc == 0, "eval-iptu-oficial: VV terreno confrontado com o lançamento real OK" if rc == 0 else f"eval-iptu-oficial falhou (exit {rc})"


def check_eval_semantico():
    # B-5 (2.6): camada de significado (embeddings Gemini). Eval OFFLINE (vetores commitados):
    # o híbrido não regride a palavra-chave (⊇) e agrega ganhos. Pula se os vetores não existirem.
    rc, _ = _run(["evals/eval-semantico.py"])
    return rc == 0, "eval-semantico: híbrido não regride keyword (+ ganhos de significado)" if rc == 0 else f"eval-semantico falhou (exit {rc})"


def check_produto():
    # T2/S2: golden-assert do Fi legal sobre 7 cedentes reais; sabotar 1 Fi (engine ou CSV) FALHA aqui.
    rc, _ = _run(["evals/eval-produto.py"])
    return rc == 0, "produto: 7 cedentes reais c/ Fi legal (Art.24) OK" if rc == 0 else f"produto divergiu do Fi legal (exit {rc})"


def check_zona_mutacao():
    rc, _ = _run(["evals/eval-zona-mutacao.py"])
    return rc == 0, "zona-mutação: 6/6 PASS" if rc == 0 else f"zona-mutação regrediu (exit {rc})"


def check_fsce():
    # FSCE (Art. 57, Lei 17.844/2022): o engine reproduz EXATO 4 Declarações oficiais do Diário Oficial
    # (PCpt = ATC×CAbás×Fi×FSCE, FSCE=2,0). Explica o Fi≈2,4 (=Fi 1,2 × FSCE 2,0). Sabotar o fator FALHA aqui.
    rc, _ = _run(["evals/ground-truth/gabaritos/eval-formula-zepec.py"])
    return rc == 0, "FSCE Art.57: 4/4 reproduz Diário Oficial" if rc == 0 else f"FSCE regrediu (exit {rc})"


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
    if rc2 != 0:
        return False, f"INDICE-MESTRE desatualizado (exit {rc2}) — rode reconciliar_arrumacao.py"
    # Teste de integração end-to-end da toolchain (R8/R9/idempotência/R4/gate) — sintético, restaura sozinho.
    rc3, _ = _run(["evals/eval-arrumacao.py"])
    return rc3 == 0, ("índice consistente + loop de arrumação provado (eval-arrumacao)" if rc3 == 0
                      else f"eval-arrumacao FALHOU (exit {rc3}) — rode evals/eval-arrumacao.py")


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


def check_indice_rag():
    # B-02 (auditoria 2026-07-05): o fechamento LOCAL nunca regenerava rag/chunks+rag/index — um índice
    # adulterado à mão (ou drifted do verbatim das leis/ ou do domínio do JSON) passava localmente; só o
    # CI regenerava. Aqui regenera (fatiar+indexar) e compara contra HEAD — espelha o CI.
    rc1, _ = _run(["scripts/fatiar.py"])
    rc2, _ = _run(["scripts/indexar.py"])
    rc3, _ = _run(["scripts/grafo_remissoes.py"])   # B-6: o grafo mora em rag/ e regenera junto
    if rc1 != 0 or rc2 != 0 or rc3 != 0:
        return False, f"fatiar/indexar/grafo quebrou (fatiar {rc1}, indexar {rc2}, grafo {rc3})"
    d = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", "rag/"], cwd=RAIZ)
    if d.returncode == 0:
        return True, "rag/ commitado == regenerado (índice não-adulterado, bate com leis/+domínio)"
    return False, "rag/ regenerado difere do commitado — rode fatiar+indexar e re-commite"


def check_handoff_nao_stale():
    # C-08 (auditoria): o handoff PRIMÁRIO (PROXIMA-INSTANCIA.md) é o 1º que a próxima instância lê. Ele
    # afirmava "Fase 1 não começou / ZERO fix de produto / T2-T3 vivos" quando T1–T4 estavam FEITOS. Este
    # check reprova se as frases-stale conhecidas reaparecerem (anti-regressão mecânica do overclaim A-12).
    hp = RAIZ / "PROXIMA-INSTANCIA.md"
    if not hp.exists():
        return False, "PROXIMA-INSTANCIA.md ausente (handoff primário)"
    txt = hp.read_text(encoding="utf-8")
    stale = [s for s in ("Fase 1 (código) não começou", "ZERO fix de produto",
                         "gate verde cobre a FUNDAÇÃO, não o produto") if s in txt]
    return (not stale), ("handoff sem frases-stale conhecidas" if not stale
                         else f"handoff com afirmação stale (A-12): {stale[0]!r} — atualize o banner")


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
        ("PII (sem dados pessoais na árvore git, T7)", check_pii_arvore),
        ("PII HISTÓRICO (dados pessoais no git log, L-T7-2)", check_pii_historico),
        ("ORÁCULO AUSENTE (engines/tdc/oraculos/, T6)", check_oraculos_ausente),
        ("EVALS (citação correta, 1.7)", check_evals),
        ("ENGINE (número no engine, 1.3)", check_engine),
        ("ENGINE Fp (Quadro 6, Fator de Planejamento)", check_engine_fp),
        ("ENGINE CEDENTE (Fi Art.24, T2)", check_engine_cedente),
        ("ENGINE PREÇO LEGAL (Art. 128 — numerador + ÷CAmaxcd + IPCA)", check_engine_art128),
        ("ENGINE IPTU (VV × alíquota por porção)", check_engine_iptu),
        ("EVAL IPTU (âncoras da lei + mutação)", check_eval_iptu),
        ("EVAL IPTU OFICIAL (VV terreno × lançamento real)", check_eval_iptu_oficial),
        ("EVAL SEMÂNTICO (B-5, híbrido ⊇ keyword)", check_eval_semantico),
        ("PRODUTO (golden Fi cedentes reais, T2)", check_produto),
        ("PRODUTO M1 (dossiê citado + funil de estágios)", check_produto_dossie),
        ("FATORES TDC (inventário verificado: chunk+eval, M4)", check_fatores_tdc),
        ("ZONA-MUTAÇÃO (CAbás por zona, G6)", check_zona_mutacao),
        ("FSCE (Art.57 Lei 17.844 — Setor Central)", check_fsce),
        ("CONSERVAÇÃO (Art.129 3-estados, T4)", check_conservacao),
        ("REGIME PCpt (já-declarado×novo, T3)", check_regime_pcpt),
        ("DIVERGÊNCIA PCpt×certidões (M0)", check_divergencia),
        ("DOMÍNIO TDC×IPTU (metadado, roteamento)", check_dominio),
        ("ÍNDICE ARRUMAÇÃO (SEED×de-para, MESTRE×reconc.)", check_indice_arrumacao),
        ("DISCLAIMER injetado (M0)", check_disclaimer),
        ("CORPUS (sem stray tags)", check_stray_tags),
        ("ÍNDICE RAG (rag/ regenerado == commitado, B-02)", check_indice_rag),
        ("HANDOFF (sem frase-stale, C-08)", check_handoff_nao_stale),
        ("MANIFESTO (idempotente, SSOT)", check_manifesto_idempotente),
        ("BACKLOG (fresco, D83)", check_backlog_fresh),
        # C-03 (auditoria): durabilidade é HARD — "perda de dados" é o modo de falha nº1; commit não
        # pushado/working-tree sujo somem no reset do container. Rode este gate SÓ ao fechar (já commitado).
        ("GIT limpo (durabilidade, C-03)", check_git_clean),
        ("GIT pushado (durabilidade, C-03)", check_pushed),
    ]
    print("═══ GATE DE FECHAMENTO — Potencial Urbano (D83: 'declarei feito' ≠ 'provei feito') ═══")
    falhou = False
    for nome, fn in hard:
        ok, msg = fn()
        print(f"  [{'VERDE ' if ok else 'VERMELHO'}] {nome}: {msg}")
        falhou = falhou or not ok

    print("─────────────────────────────────────────────────────────────────────────────")
    if falhou:
        print("VERMELHO — há pendência MECÂNICA. NÃO declare 'fechado' até ficar verde.")
        sys.exit(1)
    print("VERDE — os checks mecânicos passaram. (Ainda assim: atualize o BACKLOG e o handoff com o julgamento.)")
    sys.exit(0)


if __name__ == "__main__":
    main()
