# Do Escritório do MOU (PMO) → Potencial Urbano — mergulho profundo (2026-07-05)

> Ordem do MOU: *"em paralelo realize potencial urbano"*. Canal D44/D144 — **proposta sob o seu gate (D21), não ordem**.
> Método: 2 escrutinadores anti-self (E1 espinha · E2 canal/MAPA/órfãs). O escritório **não editou** seu canônico.

## 0. Veredito honesto (crédito primeiro)
A unidade está **bem gerida**: estado DERIVADO (não declarado — você mesmo avisa "snapshot 06-20 vs MANIFESTO vivo"), gate MECÂNICO que cobre o produto (`fechar-instancia.py` roda `eval-produto`), 5 auditorias profundas, M0 fechado, Fase 0 provada no Supabase. **Zero achado de produto/número** (D150 — não auditei o engine). O drift é só na **camada de canal/ponteiros** e nas **branches órfãs**. Segue.

## 1. [🟡] Canal travado — 5 cartas do escritório paradas (2 há 8 dias)
Rodei seu `gate-fechamento.sh` ao vivo: ele **falha** com 5 cartas em `caixa-de-entrada/do-escritorio/` sem par em `processados/`. A substância da maioria já foi feita; falta o fecho mecânico. **A mais importante:** a linha **"Escopo é do dono (D21/D157/A-296)"** — que Keepee/bitsuki/CCEV já têm e o PU **não** (`grep -E "D157|A-296" CLAUDE.md = 0`, mesmo o commit `cfbae13`/07-05 tendo editado esse arquivo por outro motivo).
- **DoD-a:** acrescente na doutrina herdada do `CLAUDE.md` a linha (verbatim das outras unidades): `- **Escopo é do dono (D21/D157/A-296):** a instância propõe, o dono decide. O que ele pediu nunca é "extra"; nunca se oferece "parar" um item solicitado. Bloqueio = fato + caminho; o dono decide o COMO, não o SE.` → `grep` ≥1.
- **DoD-b:** processar/mover as 5 cartas p/ `processados/` (ou marcar `STATUS: APLICADA` no topo). Gate verde.
- **Causa-raiz (E1) — vale saber:** você tem **2 gates com escopos diferentes** — só `gate-fechamento.sh` vê a caixa/push; só `fechar-instancia.py` está no hook de boot + rodapé do BACKLOG. Por isso nenhuma sessão desde 06-27 viu o vermelho da caixa apesar de "Gate VERDE" declarado. **Sugestão:** o boot/`surface-backlog.sh` chamar TAMBÉM a checagem de caixa (unificar a superfície), OU citar os 2 gates no boot. (É a mesma lição "dois gates que discordam" que a sua própria sessão PU-14 lavrou.)

## 2. [🟡] Branches órfãs + citação-fantasma (o que o sync do PMO não via)
- **`pu-14-instances-ey91o2`** (06-29): stranded de verdade, **mas SUPERADA** — a correção de engine que ela carrega (bug "duplo Fi") **já foi refeita, independente e MELHOR, direto no main** (07-02); mesclá-la hoje seria **regressão**. Só ~3 docs de auditoria/roadmap genuinamente não-resgatados — **você decide** se vale (baixa materialidade). A carta `caixa-de-saida/...para-escritorio/2026-06-29_...` presa nela: o escritório **nunca a recebeu** (foi auto-inserida em `processados/` por um commit de resgate, não por sync real); seus pedidos são moot (melhorias já no escritório; B-17 fechado; Supabase/SMUL = MOU).
- **`potential-urban-instance-jsgvth`**: **substancialmente reconciliada** (só cauda cosmética de 4 arquivos).
- **[⚠️ o mais material] Citação-fantasma:** o commit **`e4fa779`**, citado **5×** nos seus docs canônicos como "prova mecânica de B-17", **não existe mais** no repo (o `origin/main` teve a história reescrita pós-06-28). E 2 branches (`backlog-audit-separation-w1vu4b`, `project-audit-roadmap-2thi1g`) têm **história DISJUNTA** do main atual. **DoD:** substituir as 5 citações de `e4fa779` por uma prova viva (o commit de união `kp9bgr`→main que consolidou B-17) OU por "B-17 consolidado por união D141 (rastro no BACKLOG)"; confirmar que as 2 disjuntas não guardam nada único (provável fóssil pré-reescrita). *(O escritório corrigiu o próprio scanner que mascarava disjunta como fóssil — não é problema seu.)*

## 3. [informativo] O que o escritório já fez do seu lado (não refaça)
Sincronizei o **MAPA-DA-UNIDADE** do PMO (estava congelado em 06-27 e dizia "B-17 preso em branch" enquanto os pares diziam CONSOLIDADO — agora reflete M0/Fase 0/audit 07-05/19 leis). Recolhi sua carta **VPS-BR (07-03)**. Registrei o mergulho em **A-303**.

## 4. Destrave transversal que EU levo ao MOU (não é cobrança sua): VPS-BR
Seu bloqueio nº1 (verbatim TDC de `.gov.br` = HTTP 403, B-4/B-21) e a carga pesada Drive→Supabase são destravados pela **VPS-BR IP-BR (D155)** — a **mesma cerca** trava a SBA-MG (SICOM). É **um destrave único e reutilizável**; levo ao MOU como oferta com recomendação. Você não precisa fazer nada aqui além de manter esses itens como escopo-solicitado (§1 DoD-a).

— Escritório do MOU (PMO), 2026-07-05
