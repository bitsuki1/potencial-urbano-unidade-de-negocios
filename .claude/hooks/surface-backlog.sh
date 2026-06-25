#!/usr/bin/env bash
# SessionStart hook — o "ladrão" (mecanismo anti-perda D83 do escritório) aplicado ao Potencial Urbano.
# Surfaça o BACKLOG no boot para que NENHUMA determinação adiada fique invisível na troca de instância.
# Prevenção por MECANISMO, não por disciplina (a memória é o elo que arrebenta na saturação/troca).
set -euo pipefail
DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
echo "═══════════ POTENCIAL URBANO — retome por aqui (não recomece o que já está FEITO) ═══════════"
echo "• Doutrina: zero-compressão · dialético · agnosticismo · nada se descarta · número nasce no engine (1.3) · citação obrigatória (1.7)."
echo "• Estado vive no GIT, não na conversa. Leia: PROXIMA-INSTANCIA.md → HANDOFF-E-PENDENCIAS.md → MANIFESTO.json."
echo "• CERCA: NÃO toque o Google Drive nem drive-arrumacao/; trabalhe na sua branch; crie arquivos NOVOS."
echo "─────────────────────────────────────────────────────────────────────────────────────────"
if [ -f "$DIR/BACKLOG.md" ]; then
  echo "═══════════ BACKLOG — determinações em aberto (D83 — o que falta; não deixe cair) ═══════════"
  cat "$DIR/BACKLOG.md"
  echo "─────────────────────────────────────────────────────────────────────────────────────────"
  echo "AO FECHAR: rode 'python3 scripts/fechar-instancia.py' — o GATE mecânico. 'Declarei feito' ≠ 'gate verde'."
else
  echo "(BACKLOG.md não encontrado em $DIR — o mecanismo anti-perda depende dele; recrie a partir do PROXIMA-INSTANCIA.md)"
fi
echo "─────────────────────────────────────────────────────────────────────────────────────────"

# D141 (MOU 2026-06-25): boot consolida sozinho o que a sessão anterior deixou preso (árvore limpa).
if git -C "$DIR" rev-parse --git-dir >/dev/null 2>&1; then
  git -C "$DIR" fetch origin main --quiet 2>/dev/null || true
  _behind=$(git -C "$DIR" rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
  if [ "${_behind:-0}" != "0" ] && [ -z "$(git -C "$DIR" status --porcelain 2>/dev/null)" ]; then
    _cs="$DIR/consolidar.sh"; [ -f "$DIR/processos/consolidar.sh" ] && _cs="$DIR/processos/consolidar.sh"
    if [ -f "$_cs" ]; then
      echo "↪ $_behind commit(s) preso(s) da sessão anterior — consolidando sozinho ao main (D141)…"
      bash "$_cs" 2>&1 | sed "s/^/   /" || echo "   (não fechou: main protegido → abra PR, ou conflito p/ a instância resolver)"
    fi
  fi
fi
