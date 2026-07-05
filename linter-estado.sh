#!/usr/bin/env bash
# linter-estado.sh — LINTER DE ESTADO portável (kit de processos A9, propagado pelo Escritório do MOU 2026-07-05).
# Mecânico (grep/git); roda no gate, na GitHub Action (remoto-safe) e à mão. Defensivo: pula o check cujo
# artefato não existe no repo. Exit != 0 se 🟥. Doutrina/origem: escritorio-do-mou A-304 ("o estado se auto-verifica").
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"   # o script vive na RAIZ do repo do projeto
FAIL=0; WARN=0
red(){ echo "🟥 $1"; FAIL=1; }
yel(){ echo "🟨 $1"; WARN=$((WARN+1)); }
grn(){ echo "🟩 $1"; }
echo "═══ LINTER DE ESTADO — $(basename "$ROOT") ═══"

# [1] RÉGUA-POR-BYTE: a constituição do repo (CLAUDE.md / AGENTS.md) não pode inchar (régua = byte, não linha).
for c in CLAUDE.md AGENTS.md; do
  [ -f "$ROOT/$c" ] || continue
  b=$(wc -c < "$ROOT/$c" | tr -d ' ')
  if [ "$b" -gt 32768 ]; then red "[1] $c INCHADO: $((b/1024))KB > 32KB — enxugar (ponteiro > payload)"
  else grn "[1] $c ok: $((b/1024))KB (≤ 32KB)"; fi
done

# [2] gate de fechamento presente + executável (o kit exige gate).
if [ -f "$ROOT/gate-fechamento.sh" ]; then grn "[2] gate-fechamento.sh presente"
else yel "[2] sem gate-fechamento.sh (kit incompleto)"; fi

# [3] CARTAS paradas na caixa (do-escritorio + de-*/) sem par em processados/ nem marcador STATUS.
if [ -d "$ROOT/caixa-de-entrada" ]; then
  paradas=0
  while IFS= read -r f; do
    base="$(basename "$f")"; dir="$(dirname "$f")"
    case "$base" in README.md) continue;; esac
    [ -f "$dir/processados/$base" ] && continue
    grep -qE '^STATUS:[[:space:]]*(APLICADA|ROTEADA|RESPONDIDA|RECUSADA|CONTRAPROPOSTA)' "$f" 2>/dev/null && continue
    paradas=$((paradas+1))
  done < <(find "$ROOT/caixa-de-entrada" -type f -name '*.md' ! -path '*/processados/*' 2>/dev/null)
  [ "$paradas" -gt 0 ] && yel "[3] $paradas carta(s) na caixa sem processar (aplicar+mover OU STATUS)" || grn "[3] caixa-de-entrada sem carta pendente"
fi

# [4] REGISTRO-DE-INSTANCIAS: linha ABERTA da branch corrente = instância não-fechada (órfã).
if [ -f "$ROOT/REGISTRO-DE-INSTANCIAS.md" ]; then
  BR=$(git -C "$ROOT" branch --show-current 2>/dev/null || echo "?")
  minha=$(grep -F "$BR" "$ROOT/REGISTRO-DE-INSTANCIAS.md" 2>/dev/null | grep -w ABERTA | grep -vw FECHADA)
  [ -n "$minha" ] && yel "[4] sua linha no REGISTRO ainda ABERTA (feche + handoff)" || grn "[4] REGISTRO sem linha ABERTA da sua branch"
fi

# [5] doutrina "escopo é do dono" gravada (só em repo de UNIDADE).
if [ -f "$ROOT/CLAUDE.md" ] && grep -qiE 'Tipo.*UNIDADE|unidade de negócio' "$ROOT/CLAUDE.md" 2>/dev/null; then
  grep -qE 'D157|A-296|Escopo é do dono' "$ROOT/CLAUDE.md" && grn "[5] doutrina 'escopo é do dono' presente" || yel "[5] falta a linha 'escopo é do dono (D157/A-296)' no CLAUDE.md"
fi

echo "─────────────────────────────────────────────"
[ "$FAIL" -eq 0 ] && echo "RESULTADO: 🟩 sem 🟥 · $WARN aviso(s) 🟨" || echo "RESULTADO: 🟥 há bloqueio — corrija antes de fechar"
exit $FAIL
