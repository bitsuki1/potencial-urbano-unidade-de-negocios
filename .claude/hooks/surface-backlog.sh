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
