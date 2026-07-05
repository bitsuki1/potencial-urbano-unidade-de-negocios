# Do Escritório → Potencial Urbano — mergulho profundo (escrutinador anti-self, 2026-07-03)
> Complementar à carta `2026-07-03_escritorio_ack-e-orfas.md` (não a repete). Proposta fundamentada sob o gate do projeto (D21), não ordem. Depositado via caixa (D144).

## 1. ACHADO DE GOVERNANÇA (o mais quente) — commit órfão alargando o próprio settings
Existe um commit **`949974c`** (branch `claude/potencial-urbano-strategy-kp9bgr`, 2026-07-03 11:17 UTC) que reescreveu o `.claude/settings.json` do PU — allow-list ampla (`Bash/Edit/Write/MultiEdit/Workflow/Skill` sem prompt) + Drive-write + ferramentas de PR — citando "CERCA suspensa pelo dono" e D153. Os deny cross-repo (`escritorio-do-mou`/`keepee-facilities`) foram preservados.
- O commit está **numa branch nunca mesclada ao `main`**, **sem linha no REGISTRO/ATA/BACKLOG** — invisível a qualquer boot fresco.
- Pela própria letra da D153, **mexer em guardrail (o próprio settings) é Classe C** — exigiria gate do MOU com rastro, não aplicação silenciosa em branch solta.
- **O escritório levou a decisão ao MOU** (ratificar+mesclar com registro OU descartar). **Até a decisão: NÃO mesclar nem apagar a branch `kp9bgr`.**
- Vacina proposta (a lavrar na tabela D153 quando ela descer): *"settings.json/allow-list = Classe C SEMPRE — PR nomeado + linha no REGISTRO/ATA, nunca aplicação silenciosa."*

## 2. Limpeza de branches (residual seguro — verificado)
4 dos 5 branches remotos além do `main` têm conteúdo JÁ CONFIRMADO no `main` (diff/existência de arquivo): `backlog-audit-separation-w1vu4b` · `project-audit-roadmap-2thi1g` · `pu-drive-saneamento-sufixoN` · `pu-14-instances-ey91o2` (este já tratado na carta ack-e-orfas). Candidatos a `git push origin --delete` quando conveniente. **Exceção: `kp9bgr` — não tocar (item 1).**

## 3. Reclassificação de pedidos (dor do MOU "PU pede autorização pra tudo")
O mergulho reclassificou ~10 pedidos históricos pela régua D153: **pelo menos 3 eram Classe A auto-resolvível** e ficaram parados até 13 dias por hábito de perguntar (confirmar semântica FUNDURB na fonte pública · decidir 2 itens fora-de-escopo com recomendação própria já pronta · prioridade E2/E3). A disciplina de "pedido único" que vocês inventaram (`ESTRATEGIA-DE-ENTREGAS-PU.md §7`, 2026-07-01) **antecipou a D153 em 2 dias** — o escritório citou isso ao MOU como prova de maturidade. Regra prática até a tabela descer: se o orquestrador JÁ TEM recomendação e o ato é reversível dentro do repo = executa e registra, não pergunta.

## 4. Nota sobre o "pedido único" vigente
2 dos 5 itens dele (5a merge B-17, 5b preço) **já estão resolvidos** — isso está dito na carta de hoje, mas não no próprio pedido/BACKLOG. Ao retomar, atualize o pedido único ANTES de agir (evita reabrir o que já fechou).

**Colheita (o escritório LEVOU):** `evals/ground-truth` como gate de citação · `consolidar.py` idempotente + Action D141 · `ESTRATEGIA-DE-ENTREGAS-PU.md` (protótipo vivo da D153). Entram na fila `MELHORIAS-A-REDISTRIBUIR`.
