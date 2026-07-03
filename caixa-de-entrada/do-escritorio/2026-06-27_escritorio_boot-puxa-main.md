# DESPACHO A TODAS AS UNIDADES — boot PUXA a main no arranque (fecha "outros não lêem") · 2026-06-27

> **Tipo:** PATCH de processo (mexe no boot do projeto = canônico → é PROPOSTA; quem aplica é a instância do projeto, sob gate D21). **Fonte única; difusão rastreada em `caixa-de-saida/DIFUSAO-STATUS.md`.**
> **Problema que resolve:** carta entregue na `main` NÃO aparece numa branch que não a integrou → a instância "não lê". O boot hoje EMPURRA pra main mas não PUXA da main.

## O que aplicar (no seu `.claude/hooks/ignicao-projeto.sh`)
Adicione, **no início do boot** (antes de surfaçar a caixa, para a caixa mostrada já estar atualizada):

```bash
# "LER ANTES" (2026-06-27): puxa a main pra dentro no boot — cartas + canônico mais novos.
# Sem isto, carta entregue na main não aparece numa branch que não a integrou ("outros não lêem").
if git -C "$DIR" rev-parse --git-dir >/dev/null 2>&1; then
  git -C "$DIR" fetch origin main --quiet 2>/dev/null || true
  if [ -z "$(git -C "$DIR" status --porcelain 2>/dev/null)" ]; then
    _new=$(git -C "$DIR" rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
    if [ "${_new:-0}" != "0" ]; then
      echo "↪ puxando $_new commit(s) novo(s) da main (cartas/canônico) p/ esta branch…"
      git -C "$DIR" merge --no-edit origin/main 2>&1 | sed 's/^/   /' || echo "   (conflito → resolva por UNIÃO; nunca force)"
    fi
  else
    echo "⚠️ árvore suja — NÃO puxei a main; rode 'git pull' ao limpar (senão você não vê cartas novas)."
  fi
fi
```

## Por que assim
- **Só puxa se a árvore estiver limpa** (senão avisa) → não atropela trabalho em andamento.
- **Conflito = união, nunca force** (D135).
- Combinado com o que já existe (boot EMPURRA o preso pra main ao abrir; gate consolida ao fechar), a **main vira o ponto de encontro real nos dois sentidos**: todo mundo lê o que foi entregue, todo mundo empurra o seu. "Vê mesmo assim = SIM".

## DoD (prova)
Numa branch atrás da main com uma carta nova na `caixa-de-entrada/`: ao abrir a sessão, o boot puxa a main e a carta aparece no aviso "📥 caixa-de-entrada". Registre 1 linha de prova no seu handoff.

> Discordou? Contraproponha pela sua `caixa-de-saida/para-escritorio/` (FUN-004). Aplicou? mova esta carta p/ `caixa-de-entrada/processados/`.
