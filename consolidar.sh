#!/usr/bin/env bash
# consolidar.sh — consolida a branch de trabalho ao origin/main numa tacada (friction #2, 2026-06-25).
# Resolve a dança manual (checkout main && merge --ff-only && push && checkout branch) que já causou
# divergência silenciosa (A-027/A-032). FF; se divergiu, UNIÃO automática (D135/D141, nunca --force).
# main PROTEGIDO (push falha) → NÃO finge sucesso: avisa para ABRIR PR (squash) e sai com código 3.
# Uso: bash consolidar.sh [branch]   (funciona de qualquer repo via show-toplevel).
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1
BR="${1:-$(git branch --show-current)}"
[ "$BR" = "main" ] && { echo "❌ você está em main; passe a branch de trabalho."; exit 1; }
echo "▶ consolidando '$BR' → origin/main…"
git fetch origin main --quiet 2>/dev/null || { echo "⚠️ sem rede p/ fetch origin/main"; exit 4; }
git checkout main --quiet || { echo "❌ não consegui checkout main (árvore suja?)"; exit 1; }
git merge --ff-only origin/main --quiet 2>/dev/null || true   # atualiza main local

push_main(){ # empurra main; se falhar (protegido), avisa PR e sinaliza
  if git push origin main 2>/tmp/_cons_pusherr; then
    echo "✅ origin/main = $(git rev-parse --short main) ($1)"; git checkout "$BR" --quiet; echo "▶ de volta em '$BR'."; return 0
  else
    echo "⚠️  PUSH AO MAIN FALHOU — main PROTEGIDO (ou sem permissão). NÃO finjo sucesso (D141)."
    echo "    $(tail -1 /tmp/_cons_pusherr 2>/dev/null)"
    echo "    AÇÃO (agente com GitHub MCP): abra PR \`$BR\` → main e MERGE squash. O conteúdo já está pronto na branch (perda-zero)."
    git checkout "$BR" --quiet 2>/dev/null || true; return 3
  fi
}

if git merge --ff-only "$BR" --quiet 2>/dev/null; then
  push_main "consolidado por FF"; exit $?
else
  echo "↪ divergência — fazendo UNIÃO automática (D135/D141, preserva os dois lados)…"
  if git merge --no-ff "$BR" -m "Consolidação por união: $BR → main (automática, D141)" --quiet 2>/dev/null; then
    push_main "consolidado por UNIÃO"; exit $?
  else
    git merge --abort 2>/dev/null || true
    git checkout "$BR" --quiet 2>/dev/null || true
    echo "⚠️  CONFLITO TEXTUAL real '$BR' × main — a INSTÂNCIA resolve por união (D135), NÃO o MOU:"
    echo "      git checkout main && git merge $BR  (resolva os <<<< a favor do conteúdo certo) && git push origin main && git checkout $BR"
    exit 2
  fi
fi
