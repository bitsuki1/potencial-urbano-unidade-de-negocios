#!/usr/bin/env bash
# consolidar.sh — consolida a branch de trabalho ao origin/main numa tacada (friction #2, 2026-06-25).
# Resolve a dança manual repetitiva (checkout main && merge --ff-only && push && checkout branch) que já
# causou divergência silenciosa (achados A-027/A-032). Aborta com instrução se o FF não for limpo
# (cai no merge-por-UNIÃO do D135 — nunca --force). Uso: bash processos/consolidar.sh [branch].
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
BR="${1:-$(git branch --show-current)}"
[ "$BR" = "main" ] && { echo "❌ você está em main; passe a branch de trabalho."; exit 1; }
echo "▶ consolidando '$BR' → origin/main…"
git fetch origin main --quiet
git checkout main --quiet
git merge --ff-only origin/main --quiet 2>/dev/null || true   # atualiza main local (evita split A-027)
if git merge --ff-only "$BR" --quiet 2>/dev/null; then
  git push origin main 2>&1 | tail -1
  echo "✅ origin/main = $(git rev-parse --short main) (consolidado e empurrado por FF)"
  git checkout "$BR" --quiet
  echo "▶ de volta em '$BR'."
else
  # AUTOMÁTICO (D141, MOU 2026-06-25 "nada da esteira depende de eu lembrar/autorizar"): divergiu →
  # faz a UNIÃO sozinho (merge, NUNCA --force; preserva os dois lados). Não para pedir humano.
  echo "↪ divergência detectada — fazendo UNIÃO automática (D135/D141, preserva os dois lados)…"
  if git merge --no-ff "$BR" -m "Consolidação por união: $BR → main (automática, D141)" --quiet 2>/dev/null; then
    git push origin main 2>&1 | tail -1
    echo "✅ origin/main = $(git rev-parse --short main) (consolidado por UNIÃO)"
    git checkout "$BR" --quiet
    echo "▶ de volta em '$BR'."
  else
    # sobra só o conflito textual real — aí a INSTÂNCIA resolve (tem o contexto), NUNCA o MOU.
    git merge --abort 2>/dev/null || true
    git checkout "$BR" --quiet
    echo "⚠️  CONFLITO TEXTUAL real '$BR' × main — a INSTÂNCIA resolve por união (D135), NÃO o MOU:"
    echo "      git checkout main && git merge $BR  (resolva os <<<< a favor do conteúdo certo) && git push origin main && git checkout $BR"
    exit 2
  fi
fi
