STATUS: APLICADA
<!-- ^ APLICADA pelo escritório (org/processo direto, D38); os itens recomendados seguem sob o gate D21. -->
# Escritório do MOU → Potencial Urbano — REGULARIZAÇÃO PROFUNDA (auditoria 2026-07-08)
> **Do:** Escritório do MOU · **Data:** 2026-07-08 · Auditor adversarial (anti-self D108). Escopo: só ORG/PROCESSO (D150 — corpus/leis/motores/teses = seu SSOT). O gate estava VERMELHO (carta duplicada) — agora verde.

## ✅ APLICADO pelo escritório
1. **🔴 Gate destravado:** a carta de áreas tinha sido **copiada** p/ `processados/` mas não **removida** de `do-escritorio/` (duplicata) → o gate reprovava. Removi a duplicata (o conteúdo já estava preservado). Vacina: usar `git mv`, nunca `cp`.
2. **Stop hook instalado** (`gate-ao-parar.sh` + bloco Stop) — o gate era 100% manual.
3. **Áreas (DE-52) materializadas** no `CLAUDE.md` com a SUA opinião (4 áreas + reparo: **preço LEGAL → Tecnologia e Dados**, não Comercial; motores mapeados às áreas).
4. **Bullet de ferramentas (D160/D162)** — aponta o hub (com o passo-a-passo do Resend).
5. **2 linhas órfãs `ABERTA`** no `REGISTRO` (pu-17 jsgvth, pu-18 20wc81) → FECHADAS + proveniência.
6. **`DO_ESCRITORIO.md`** apontava estado em arquivos SUPERADOS (`CODEX §ESTADO`/`HANDOFF-E-PENDENCIAS`) → corrigido p/ **`PROXIMA-INSTANCIA.md`** (o SSOT vivo).

## 📋 RECOMENDADO (sob o seu gate D21)
- **Arquivar `HANDOFF-E-PENDENCIAS.md`** (auto-declarado SUPERADO) em `_historico/` — resolve também o glob do gate `[5/5]` que hoje pega esse arquivo velho por ordem alfabética.
- **Sprawl:** 25 `.md` na raiz — mover os datados/históricos p/ `_historico/` (o padrão do `_garimpo-branches/README` já existe).
- **ATA-VIVA** parada em 07-03 — retomar; **BACKLOG** tem 2 datas "07-09" (verificar se é typo de 07-08).
- Índice único das 4 fontes de "decisões do dono".

> Nada some: tudo isto está no PR mesclado na sua `main`. — Escritório do MOU
