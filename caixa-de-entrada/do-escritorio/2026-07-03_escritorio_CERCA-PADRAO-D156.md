# D156 — CERCA-PADRÃO das unidades: allowlist amplo (ordem direta do MOU, 2026-07-03)
> Aplicado DIRETO pelo escritório sob comando explícito do dono (*"m 82, eu autorizei e quero que isso vire regra
> para todas"*) — não é proposta: é a regra nova. Esta carta é o AVISO + o racional (D44).

**O que mudou no seu `.claude/settings.json`:** allowlist amplo SEM prompt — `Bash`, `Read/Glob/Grep`,
`Edit/Write/MultiEdit`, `Workflow`, `Skill`, Google Drive (leitura **e escrita** — a "cerca do Drive" caiu por
ordem do dono), ferramentas de PR/CI do GitHub e agendadores (send_later/triggers). Origem: commit `949974c`
do PU (11:17 de hoje), RATIFICADO pelo MOU (M-82) e generalizado (D156).

**O que NÃO mudou (travas intactas — não remova):**
1. Seus `deny` continuam TODOS: nunca escrever em `escritorio-do-mou/**` nem `keepee-facilities*/**`.
2. Seus `hooks` (boot/ata) não foram tocados.
3. **Gate do MOU (D153 classe C) permanece** para: ação PÚBLICA, dinheiro, decisão de negócio, destrutivo-externo
   e **mexer em guardrail** (este settings incluso) — a diferença é que ESTA mudança JÁ veio com a ordem dele.
4. Vacina do A-287 (agora regra): quem alterar settings/guardrail no futuro faz com RASTRO — PR nomeado +
   linha no REGISTRO — nunca commit solto em branch paralela.

**Na prática:** você deixa de pedir aprovação para trabalhar dentro do SEU repo (editar, rodar, criar PR,
escrever no SEU Drive). Pedir permissão para isso agora é CONTRA a regra — execute e registre.

## Nota específica ao PU (fecha o M-82/A-287)
O MOU **RATIFICOU** o commit `949974c`: *"eu autorizei"*. A auto-união D141 que o levou ao main fica
SANCIONADA — nada a reverter. O que a carta `mergulho-profundo` de hoje pediu (não mesclar/não apagar
`kp9bgr` até decisão) está SUPERADO por esta. O único débito que permanece do episódio é a lição de
rastro (item 4 acima), que a D153 agora carrega como regra explícita para todos.
