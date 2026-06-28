#!/usr/bin/env bash
# gate-fechamento.sh — GATE DE FECHAMENTO UNIVERSAL (qualquer repo do portfólio).
# Prova mecânica de "fechado" antes de declarar (D83/D141): árvore limpa · trabalho CONSOLIDADO no main
# (auto-consolida) · branch empurrada · linha de instância FECHADA · handoff existe. Não depende dos
# arquivos PMO do escritório (AGENDA/DETERMINAÇÕES/ACHADOS) — esses só o escritório tem (use fechar-instancia.py lá).
# "Declarei feito" ≠ "gate verde". Uso: bash processos/gate-fechamento.sh   (ou ./gate-fechamento.sh na raiz)
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1
BR=$(git branch --show-current)
fails=0; warns=0
say(){ printf '%s\n' "$1"; }
fail(){ say "  ❌ $1"; fails=$((fails+1)); }
warn(){ say "  ⚠️  $1"; warns=$((warns+1)); }
ok(){ say "  ✅ $1"; }

say "═══ GATE DE FECHAMENTO — $(basename "$(pwd)") @ $BR ═══"

# [1] árvore limpa
say "[1/5] árvore de trabalho…"
if [ -z "$(git status --porcelain)" ]; then ok "limpa (nada não-commitado)"; else fail "há mudanças não-commitadas — commit ANTES de fechar:"; git status --short | sed 's/^/      /'; fi

# [2] consolidado no main (D135/D141) — tenta consolidar sozinho
say "[2/5] consolidado no origin/main (D141 — auto)…"
if git fetch origin main --quiet 2>/dev/null; then
  presos=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
  if [ "$presos" = "0" ]; then ok "0 commit preso — tudo no main"
  else
    if [ -f processos/consolidar.sh ] || [ -f consolidar.sh ]; then
      say "      $presos preso(s) — consolidando sozinho (D141)…"
      bash "$( [ -f processos/consolidar.sh ] && echo processos/consolidar.sh || echo consolidar.sh )" >/dev/null 2>&1
      presos2=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
      [ "$presos2" = "0" ] && ok "consolidado agora ($presos commit(s))" || fail "$presos2 preso(s) — consolidação não fechou (conflito textual real: a INSTÂNCIA resolve por união, não o MOU)"
    else fail "$presos commit(s) preso(s) e sem consolidar.sh — consolide ao main antes de fechar"; fi
  fi
  naoint=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
  [ "$naoint" != "0" ] && warn "origin/main tem $naoint commit(s) de OUTRA instância — integre por união antes (D135)"
else warn "sem rede p/ fetch — confirme à mão que seu trabalho está no main"; fi

# [3] branch empurrada
say "[3/5] branch no origin…"
if git rev-parse --verify "origin/$BR" >/dev/null 2>&1; then
  ahead=$(git rev-list --count "origin/$BR..HEAD" 2>/dev/null || echo 0)
  [ "$ahead" = "0" ] && ok "origin/$BR em dia" || { warn "$ahead commit(s) não empurrado(s) — git push origin $BR"; }
else warn "origin/$BR não existe ainda — git push -u origin $BR"; fi

# [4] registro de instância fechado (se o repo tiver)
say "[4/5] registro de instância…"
REG=$(ls processos/REGISTRO-DE-INSTANCIAS.md REGISTRO-DE-INSTANCIAS.md 2>/dev/null | head -1)
if [ -n "${REG:-}" ]; then
  if grep -E "\| ABERTA \|" "$REG" 2>/dev/null | grep -qF "\`$BR\`"; then fail "sua linha em $REG ainda está ABERTA — marque FECHADA + escreva o handoff dela"; else ok "nenhuma linha ABERTA da sua branch"; fi
else warn "sem REGISTRO-DE-INSTANCIAS.md (ok se o repo não usa contagem)"; fi

# [5] handoff existe e foi tocado
say "[5/5] handoff de retomada…"
HO=$(ls HANDOFF-ULTIMO.md HANDOFF*.md ESTADO*.md START-HERE*.md PROXIMA-INSTANCIA.md 2>/dev/null | head -1)
[ -n "${HO:-}" ] && ok "handoff presente: $HO (confirme que reflete ESTA sessão)" || warn "nenhum handoff óbvio — deixe um para a próxima instância"

# [CAIXA] pickup das caixas v2 (PROTOCOLO-DE-CAIXAS §4): FALHA se há recado não-aplicado na caixa-de-entrada/.
say "[CAIXA] recados não-aplicados (caixas v2 §4)…"
if [ -d caixa-de-entrada ]; then
  pend=$(find caixa-de-entrada -type f -name '*.md' ! -path '*/processados/*' ! -name 'README.md' 2>/dev/null | sort || true)
  n=$(printf '%s\n' "$pend" | grep -c . || true)
  if [ "${n:-0}" = "0" ]; then ok "nenhum recado pendente (ou caixa vazia)"; else
    fail "$n recado(s) NÃO-APLICADO(S) na caixa-de-entrada/ — aplique e MOVA p/ processados/ antes de fechar:"
    printf '%s\n' "$pend" | sed 's/^/      /'
  fi
else ok "sem caixa-de-entrada/ (v2 não bootstrapado neste repo)"; fi

# [MANIFESTO] idempotência do SSOT (B-18, 2026-06-27): alinha este gate ao fechar-instancia.py — antes
# ele dava VERDE com o MANIFESTO defasado/inflado (falso-verde F-1). Regenera, compara, restaura.
say "[MANIFESTO] idempotência do SSOT (B-18)…"
if [ -f scripts/consolidar.py ] && command -v python3 >/dev/null 2>&1; then
  python3 scripts/consolidar.py >/dev/null 2>&1 || true
  _drift=$(git status --porcelain -- MANIFESTO.json 2>/dev/null)
  _falso=$(python3 -c "import json;a=json.load(open('MANIFESTO.json'))['alertas'].get('indexado_sem_chunks_no_indice',[]);print(len(a))" 2>/dev/null || echo 0)
  git checkout -- MANIFESTO.json 2>/dev/null || true
  if [ -n "$_drift" ]; then fail "MANIFESTO.json regenerado difere do commitado — rode 'python3 scripts/consolidar.py' e re-commite (idempotência 2.3)";
  elif [ "${_falso:-0}" != "0" ]; then fail "$_falso lei(s) com status 'indexado' SEM chunk no índice (NV-1) — indexe de verdade ou rebaixe o rótulo";
  else ok "MANIFESTO idempotente e sem rótulo 'indexado' falso"; fi
else warn "sem scripts/consolidar.py ou python3 — não verifiquei idempotência do MANIFESTO"; fi

say "─────────────────────────────────────────────"
if [ "$fails" = "0" ]; then say "✅ GATE VERDE — pode fechar ($warns aviso(s))."; exit 0
else say "❌ NÃO FECHE — $fails bloqueio(s), $warns aviso(s). Resolva e rode de novo."; exit 1; fi
