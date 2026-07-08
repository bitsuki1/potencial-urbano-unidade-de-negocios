#!/usr/bin/env bash
# Stop hook — roda o GATE DE FECHAMENTO ao tentar encerrar a sessão. Fecha o buraco F1 (mergulho 2026-07-04):
# o gate era 100% VOLUNTÁRIO (sem hook Stop) → instâncias ficaram órfãs (linha ABERTA, trabalho não-consolidado)
# até reconciliação manual. Trazido pelo Escritório do MOU — regularização 2026-07-08 (D38, MOU "organizar a fundo").
#
# DESENHO SEGURO (anti-loop, D156 = mecanismo que NÃO prende a instância):
#   • bloqueia UMA vez (exit 2 → alimenta os bloqueios ao modelo p/ ele resolver antes de fechar);
#   • na 2ª tentativa de parada (stop_hook_active=true) SOLTA (exit 0) — nunca laço infinito;
#   • falha de infra (timeout de rede no fetch) NÃO bloqueia (exit 0) — só bloqueia bloqueio REAL do gate.
# ⚠️ Em sessão REMOTA (web) hooks podem não disparar (A-291/V-HOOK-REMOTO) — vale sobretudo p/ sessão LOCAL.
set -uo pipefail
input=$(cat 2>/dev/null || true)
# anti-loop: se já estamos numa continuação disparada por Stop hook, solta (não re-bloqueia).
case "$input" in
  *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) exit 0 ;;
esac
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "${CLAUDE_PROJECT_DIR:-$(pwd)}")
GATE="$ROOT/gate-fechamento.sh"; [ -f "$ROOT/processos/gate-fechamento.sh" ] && GATE="$ROOT/processos/gate-fechamento.sh"
[ -f "$GATE" ] || exit 0   # repo sem gate: nada a checar
out=$(cd "$ROOT" && timeout 25 bash "$GATE" 2>&1); code=$?
[ "$code" = "124" ] && exit 0   # timeout (rede/infra) — não prende a instância por flakiness
if [ "$code" != "0" ]; then
  { echo "⛔ GATE DE FECHAMENTO não está verde — NÃO feche sem resolver (ou justifique explicitamente ao MOU):"
    printf '%s\n' "$out" | grep -E '❌|⚠️|GATE|NÃO FECHE|preso|ABERTA|não empurrad' | head -25
    echo "   (rode 'bash gate-fechamento.sh' p/ o laudo completo. Este aviso aparece 1× — na próxima parada solta.)"
  } >&2
  exit 2   # bloqueia UMA vez; stderr vai ao modelo
fi
exit 0
