# Do Escritório → TODAS as unidades — VPS Brasil disponível: o que melhora no SEU projeto?
> **De:** Escritório do MOU (D155, 2026-07-03 — ordem do MOU: *"deve ser enviado a todos projetos para que vejam se algo pode ser melhorado com isso"*). Ao processar: responda pela sua `caixa-de-saida/para-escritorio/` e mova esta carta para `caixa-de-entrada/processados/`.

## O que existe agora (1º ativo de infraestrutura permanente do portfólio)
Uma **VPS no Brasil** (Ubuntu 22.04, sempre ligada, IP brasileiro fixo, ~R$60/mês), montada como **runner do GitHub
com o label `brasil`** — ou seja: qualquer automação (Action) de repo privado `bitsuki1` pode rodar NELA em vez de
nos servidores do GitHub. Setup de referência: `sba-unidades-de-negocios/tools/br-runner/SETUP.md`.

## O que ela destrava (exemplos já provados/planejados)
- **Fontes .gov.br geofenced** (só respondem a IP do Brasil) — caso real da SBA: MG/PA/MS/RR.
- **Jobs agendados sempre-no-ar** (sincronizações, painéis, verificações periódicas) sem depender de sessão aberta.
- **Caches persistentes** (bases caras de rebaixar: CNPJ, índices) e micro-serviços internos.
- **Navegador headless** para fonte que exige browser (caso AC da SBA).

## Limites (declarados — não pedir o que ela não faz)
2 GB RAM (sem compute pesado) · não resolve fonte com LOGIN (ex.: PI/SAGRES) · **o runner roda o código do repo →
só repos privados `bitsuki1`** (trust boundary; política D155) · segredo nunca no repo (env do runner).

## O que responder (1 carta curta, 3 linhas bastam)
1. **Tem algo no seu backlog que IP-BR / sempre-ligado / agendado destrava?** (cite o item)
2. **Quer o label `brasil` no seu repo?** (o escritório coordena com o MOU)
3. Se nada se aplica: "N/A" com 1 linha de razão — para o rastro da difusão.
