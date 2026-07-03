# AUDITORIA BETA — 2026-07-03

> **Beta contínuo:** audita "provei feito", não "declarei feito" (mecanismo D83). Método:
> verificação MECÂNICA contra a realidade — gate `scripts/fechar-instancia.py`, git, e o banco
> vivo do Supabase (`csnalylpvysjvejgsymr`) via MCP. Cada afirmação carrega a evidência e o veredito.
> Dialético: os caveats (o que NÃO está provado) estão declarados no fim, sem suavizar.

## 1. Escopo da auditoria
O que a sessão 2026-07-03 declarou como feito: a **Fase 0 — Fundação** (canonicidade do schema,
proveniência `de_para`, segurança T7) e os artefatos de estratégia (roadmap, 3 motores, escrutínio,
inventário do Drive, handoff). A auditoria NÃO cobre a Fase 1 (código dos motores), que **não começou**.

## 2. Resultados — todos PROVADOS ao vivo

| # | Afirmação | Verificação | Evidência (2026-07-03) | Veredito |
|---|---|---|---|---|
| A1 | git == banco (canonicidade, S1/E6) | migrations vivas × `.sql` no git, versão a versão | vivas = `20260619020603, ...020658, ...020951, 20260624100319, 20260702142208, 20260703145720, 20260703172052` = exatamente os 7 arquivos em `supabase/migrations/` | ✅ |
| A2 | Fantasmas receptor NÃO aplicados | `information_schema` | schema `dados` = **não existe**; tabela `geo.lote` = **não existe**; os 3 arquivos em `_nao-aplicadas-receptor/` | ✅ |
| A3 | Proveniência populada (S4) | `count(governanca.de_para)` | 20 linhas — 14 `OFICIAL`, 3 `CRIADO-POR-NOS` (marcadas "não usar") | ✅ |
| A4 | Decisões registradas | `governanca.registro_decisoes` | D-CANON-01, D-CANON-02, D-SEG-01 (+ D-ESCOPO-01, D-DRIVE-01, D-FORK-00, D-MOTOR-01, D-AUDIT-01 nesta auditoria) — todas `vigente`/`pendente` | ✅ |
| A5 | Dados oficiais carregados | `count(oficiais.*)` | `iptu2026_cedentes` = 3.905; `q14_valor_terreno_2025` = 3.676 (batem com `zepec/oficial/PROVENIENCIA.md`) | ✅ |
| A6 | Segurança T7 | `storage.buckets.public` + `pg_policies` | buckets `dados-produto/geo-tabelas/geo-shapefiles` = **todos privados**; `oficiais.*` RLS enabled, **zero policies** (deny-all p/ anon) | ✅ |
| A7 | Gate mecânico + durabilidade | `fechar-instancia.py` | EVALS/ENGINE/CORPUS/MANIFESTO/BACKLOG = VERDE; working tree **limpo**; HEAD **pushado** | ✅ |
| A8 | Escopo receptor removido | A2 + migrations arquivadas | `dados.*`/`geo.lote`/`v_feed_alvos` ausentes do banco e do set ativo de migrations | ✅ |

**Resumo:** a Fase 0 está **sólida e reproduzível a partir do git**. Nenhuma afirmação da Fase 0 ficou "declarada sem prova".

## 3. Caveats (o que NÃO está provado — dialético)

- **C1 — `db reset` clean-room não executado.** A prova de "banco reconstruível do git" é indireta: (a) as 7 versões batem 1:1; (b) as 5 migrations de DDL foram copiadas **verbatim** do banco vivo; (c) as 2 de seed (`de_para`, decisões) são **idempotentes** (`ON CONFLICT`) e reproduzem exatamente as contagens atuais. **Selar na Fase 1:** rodar `supabase db reset` num branch efêmero e conferir contagens.
- **C2 — O gate atual NÃO cobre o produto.** `fechar-instancia.py`/`consolidar.yml` cobrem corpus/engine/manifesto, **não** `zepec/**`, `engines/**`, `tabelas/**`, `supabase/**`. Logo o "verde" **não prova o pipeline de dados nem o banco** — é a lacuna S2/T2, ainda aberta. Uma regressão no produto passaria verde hoje.
- **C3 — `service_role` legada não rotacionada** (resíduo T7, baixo risco — o vetor real, chaves S3, foi revogado; nada ativo usa a service_role). Plano: `sb_secret` nova + desabilitar legadas na Fase 1.
- **C4 — Os 3 motores não atingiram triplo limpo.** O resíduo de cada um (T-*/E-*/G-* pendentes) é **dívida de Fase 1 declarada** (headers dos `MOTOR-*-ESTRATEGIA.md` + §8 do handoff), não regressão. A Fase 1 (código) **não começou**.
- **C5 — Bloqueio externo:** G2 (ZOE/Quadro 2A) e G4 (Regra da Esquina/Decreto 57.536) dependem de 2 verbatim que **não estão no Drive nem no repo** (item do dono).

## 4. Decisões (consolidadas — ver `docs/DECISOES-2026-07-03.md` e `governanca.registro_decisoes`)
D-CANON-01 (canonicidade) · D-CANON-02 (de_para) · D-SEG-01 (T7) · D-ESCOPO-01 (só vendedor/só-tombado) · D-DRIVE-01 (CERCA suspensa) · D-FORK-00 (3 forks abertos) · D-MOTOR-01 (resíduo aceito) · D-AUDIT-01 (esta auditoria).

## 5. Veredito da auditoria beta
**Fase 0 (Fundação): APROVADA — verde, provada ao vivo, reproduzível do git.** Segue para a Fase 1
(código dos motores) com o caminho crítico já apontado (C-28 → gate de CI que fecha C2 → vedação →
conservação → overlay), e 2 bloqueios externos (C5) na mão do dono.
