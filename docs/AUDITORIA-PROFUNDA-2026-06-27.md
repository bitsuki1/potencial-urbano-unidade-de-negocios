# AUDITORIA PROFUNDA — Potencial Urbano (2026-06-27)

> **Quem:** instância orquestradora do PU (branch `claude/office-standards-consolidation-5gyg00`), sessão "consolidar padrões do escritório".
> **Método (D82/D-12):** 3 lentes adversariais paralelas + leitura própria de governança, sobre o estado vivo do git (não a conversa). Postura: procurar FALSO-VERDE e contradição. Zero-síntese.
> **Gatilho:** o MOU pediu "verificar sua caixa, rodar auditoria profunda, depositar os achados nas caixas".
> **Estado canônico de número:** `MANIFESTO.json` + `python3 scripts/fechar-instancia.py`. Em divergência, vale o git.

---

## 0. VEREDITO (uma linha, honesto)
O **processo/governança** que o escritório depositou (pacote de padronização: caixas v2, REGISTRO/ATA, Tipo D128, políticas D119/D120, resolução de handoff) está **correto e seguro — consolidado nesta sessão**. Mas a auditoria revelou o **buraco real do portfólio**: **trabalho de PRODUTO já feito (≥742 arquivos) está preso fora do `main`** numa branch órfã (`project-audit-roadmap-2thi1g`) — corpus TDC verbatim, tabelas reais e engine rodando sobre imóvel real — enquanto o **SSOT do `main` declara "produto a ~0%, `tabelas/` vazio"**. O escritório padroniza a *forma* enquanto o *valor* apodrece num galho. **ARMADO ≠ DESTRAVADO** continua valendo — agora por causa de consolidação de branch, não de falta de trabalho.

---

## 1. CAIXA — o que o escritório depositou (verificado)
O escritório depositou um **PACOTE DE PADRONIZAÇÃO DE PROJETOS** na branch `origin/claude/maestro-project-audit-h71gqn` (commits `bb7a8df` + `7743a0d`, 2026-06-27), **additive puro sobre o `main`** (12 arquivos; só docs/processo + arquivos novos; nenhuma lei/engine/script de produto tocado). Conteúdo: `caixa-de-entrada/` + `caixa-de-saida/` (caixas v2), `REGISTRO-DE-INSTANCIAS.md`, `ATA-VIVA-SESSAO.md`, Tipo (D128) no `CLAUDE.md`, políticas transversais D119/D120, `HANDOFF-SURFACES.txt` realinhado, `gate-fechamento.sh` com pickup de caixa, `surface-backlog.sh` com auto-estampa.

**Verificação das 7 diretrizes auto-marcadas ✅ APLICADO (DO_ESCRITORIO):** todas **CONFEREM** com o arquivo que as sustenta.

| Diretriz | Claim | Verificação |
|---|---|---|
| D-PU-D128 | `> Tipo (D128): UNIDADE` no cabeçalho do CLAUDE.md | ✅ CONFERE (`CLAUDE.md` cabeçalho) |
| D-PU-MR4 (D120) | §Políticas transversais com D120 | ✅ CONFERE |
| D-PU-MR5 (D119) | política D119 + trava no settings | ✅ CONFERE (deny `keepee-facilities*` presente) |
| D-PU-REGISTRO | REGISTRO+ATA + hook auto-estampa + gate trata ABERTA como fail | ✅ CONFERE (com 2 furos no hook — ver §4 H-1/H-2) |
| D-PU-HANDOFF | gate [5/5] reconhece PROXIMA-INSTANCIA.md | ✅ CONFERE (só vale após consolidar o pacote) |
| D-PU-DENY | deny blanket cobre escritório; caixa-de-saida do PU é escrevível | ✅ CONFERE — **sem contradição** (caixa-de-saida na raiz, fora do glob `escritorio-do-mou/**`) |
| D-PU-CAIXAS-v2 | lado-projeto bootstrapado, não os 7 | ✅ CONFERE |

**Decisão desta sessão:** pacote **consolidado na branch de trabalho por fast-forward** (`dc001bd → 7743a0d`), sem tocar `main`. É a execução do padrão depositado e cria as caixas usadas para depositar os achados abaixo.

---

## 2. LENTE A — DIVERGÊNCIA DE BRANCHES (o achado central)
13 branches `origin/claude/*` divergem do `main`. Mapa forense:

| Branch | commits únicos | arquivos | tipo | vs main | classificação |
|---|---|---|---|---|---|
| **`project-audit-roadmap-2thi1g`** | 14 | ~742 | **destrave de PRODUTO** (tabelas+engine+TDC verbatim+E5) | additive + 2 conflitos aditivos | **🟥 ÓRFÃ-ADDITIVE — DEVE CONSOLIDAR** |
| `backlog-audit-separation-w1vu4b` | 7 | — | rastreamento BACKLOG + ESTADO.md | additive | ÓRFÃ-ADDITIVE (governança) |
| `maestro-project-audit-h71gqn` | 2 | 12 | pacote padronização | additive | ✅ CONSOLIDADO nesta sessão |
| `nice-gates-5s8g73` / `office-audit-ozack5` / `tender-dijkstra-c4vs25` | 1–2 cada | — | estrutura/governança | additive | ÓRFÃ-ADDITIVE (menor) |
| `dreamy-cannon` / `maestro-office-audit-tlrer2` / `potencial-urbano-setup-t8irkf` / `wizardly-ritchie` | 0 | 0 | — | — | JÁ-NO-MAIN (delete-safe) |
| `exciting-tesla-rwyzks` | 39 | — | auditoria paralela R1/R2 (remove MANIFESTO/BACKLOG) | história não-relacionada | ⚠️ INVESTIGAR antes de descartar |
| `iptu-tdc-document-mapping-mjm1sn` | 10 | — | ingestão jurisprudência STF/STJ | história não-relacionada (poss. duplicada) | ⚠️ INVESTIGAR |
| `modest-mendel-xpj1ml` | 5 | — | desconhecido | história não-relacionada | ⚠️ INVESTIGAR |

### TRABALHO DE PRODUTO/CORPUS PRESO FORA DO MAIN (`project-audit-roadmap-2thi1g`)
- ✅ **B-1 FECHADO** — `tabelas/` com Q14 (**6.715 valores V por SQL**), Quadro 3 (**39 zonas, CA_max**), Q5 (Fs). É o "combustível do engine" que o BACKLOG do main lista como ABERTO/bloqueado-pelo-Drive.
- ✅ **Engine OODC sobre dados REAIS** — auto-teste com imóvel real: `SQ 001003 / Codlog 038121 × ZEU = R$ 931.800` (não mais valor ilustrativo). Fecha parte de B-12.
- ✅ **H0 — corpus TDC verbatim no RAG** — **19 leis indexadas** (vs `main`=13): PDE 16.050/2014, LPUOS 16.402/2016, COE 16.642/2017. É o destrave que o `PROXIMA-INSTANCIA.md` chama de "fatia de PRODUTO".
- ✅ **H3 — estágio E5 (produto) PROVADO** em amostra real (6 imóveis, topo R$ 1,68M) + schema Supabase DDL completo.

### CONFLITOS a resolver antes da consolidação (não-destrutivos)
- `lei-municipal-saopaulo-16050-2014` e `lei-municipal-saopaulo-17844-2022`: `main` = ~14 linhas (resumo WebSearch, `confianca:baixa`); branch = 7.172 e 3.748 linhas (**verbatim integral de PDF, `confianca:alta`**). **Resolução recomendada: aceitar a versão da branch** (é melhoria pura, casa com B-4).

**Recomendação:** consolidar `project-audit-roadmap-2thi1g` ao `main` (com a resolução acima) é a **ação de maior valor do portfólio** — sozinha tira o produto de "0%" para "E5 provado" e fecha B-1. Requer PR (main protegido). **É decisão cross-repo → depositada na caixa-de-saida para o escritório.**

---

## 3. LENTE B — GATES / PROCESSO
| Gate | Exit | Veredito |
|---|---|---|
| `bash gate-fechamento.sh` | **0 (VERDE)** | **FALSO-VERDE** (ver F-1) |
| `python3 scripts/fechar-instancia.py` | **1 (VERMELHO)** | **CORRETO** — pega o que o outro não pega |
| `python3 evals/rodar-evals.py` | 0 | OK — 8/11 PASS (3 falhas todas em `aguardando_verbatim`; 8 ativos ≥ piso 4) |
| `python3 engines/tdc/oodc.py` | 0 | OK — `_autoteste()` (12 checagens); sai 1 em falha real (gate genuíno) |

- **F-1 (ALTO) — os dois gates DISCORDAM no mesmo estado.** `gate-fechamento.sh` só checa "árvore limpa" + "0 commit preso"; **não** regenera o MANIFESTO nem compara com o corpus → declara VERDE com o SSOT dessincronizado. Só `fechar-instancia.py` (check de idempotência) pega. **Quem rodar só o `gate-fechamento.sh` fecha em falso-verde.**
- **Piso de evals SÓLIDO** (`MIN_ITENS_ATIVOS=4`): rebaixar evals a `aguardando_verbatim` não fura o gate. Bem feito (fecha F-1/F-2 da 2ª auditoria).
- **Gate 1.7 do `consultar.py` SÓLIDO:** três travas combinadas (cobertura ≥0,34 **E** BM25 ≥1,5 **E** ≥2 termos casados) → `NÃO-FUNDAMENTADA` quando falha; o script nunca redige prosa, só devolve dispositivos verbatim com `citacao{}`. Nenhum caminho emite afirmação sem citar.

---

## 4. LENTE C — CORPUS/RAG + ENGINE + furos do HOOK v2

### Achados NOVOS (não-rastreados)
- **N-1 [CRÍTICO] Rótulo `status_pipeline:"indexado"` FALSO nas 4 leis IPTU resgatadas** (`16402-2016`, `16642-2017`, `17733-2022`, `decreto-57443-2016`). Os `.json` declaram `indexado` + `confianca:alta`, mas: **0 chunks** em `rag/chunks/<id>/`, **ausentes do `rag/index/metadados.json`** (índice só tem os 13 originais), **ausentes do `MANIFESTO.json`** (`grep -c` = 0). Não são consultáveis — `consultar.py` nunca as devolve. É o anti-padrão "declarei feito ≠ provei feito" gravado no próprio corpus (fere registro honesto + 1.3 + 2.3). → **B-15**.
- **N-2 [SÉRIO] `MANIFESTO.json` defasado vs disco (−4 leis).** Disco = 31 leis `.json` + 32 juris = 63; MANIFESTO = 59 itens / 27 leis. `consolidar.py` não foi rodado/commitado após o resgate (commits 2026-06-25). Regenerar muda total 59→63, leis 27→31, indexado 13→17 — **mas 17 seria inflado** enquanto N-1 não for resolvido (as 4 não têm chunk). Ordem correta: resolver N-1 (indexar de verdade OU rebaixar o rótulo) **e então** regenerar. → **B-16**.
- **N-5 [MÉDIO] Furos do hook v2 (`surface-backlog.sh`):**
  - **H-1** — o dedup do auto-estampa só checa linha **ABERTA** (`! grep "| ABERTA |" | grep -qF "\`$BR\`"`). Num boot na mesma branch já registrada **FECHADA**, o dedup falha → anexa nova linha ABERTA (acumula duplicata). Corrigir: deduplicar por branch independente do estado.
  - **H-2** — o `>> REGISTRO` em SessionStart **suja a árvore** (REGISTRO não está no `.gitignore`) → o boot seguinte deixa ` M REGISTRO-DE-INSTANCIAS.md`, e tanto `gate-fechamento.sh [1/5]` quanto `fechar-instancia.py check_git_clean` passam a acusar não-commitado. Mecanismo anti-perda que cria pendência mecânica fantasma a cada boot. Corrigir: `.gitignore` o REGISTRO, ou o hook auto-commitar a linha, ou aceitar que a 1ª ação commita.
  - **H-3 [BAIXO]** sem furo de credencial — o hook só grava `date`/branch/hash. OK. O pickup `[CAIXA]` (find … ! processados ! README) está consistente entre hook e gate, sem furo.
- **N-6 [BAIXO] BACKLOG header `2026-06-21`** não registra o resgate das 4 leis IPTU (commits 2026-06-25) — defasagem de doc (o próprio "ladrão" que o BACKLOG mantém). → corrigido nesta sessão (data + itens novos).

### Defeitos reais já RASTREADOS (confirmados, não-novos)
- **B-11(c) [SÉRIO]** — **280 rótulos de dispositivo duplicados** (`6015-1973`=194, `10931-2004`=25, `11101-2005`=25, `9514-1997`=17, `4591-1964`=14, `8668-1993`=4, `dl-57-1966`=1) por redação compilada; **zero vigência por chunk**: nenhum chunk tem campo de redação/revogação; 266 chunks contêm "Redação dada"/"Revogado"/"Vide" no texto mas **nenhum** é marcado revogado → `consultar.py` pode devolver redação revogada como vigente (fura 1.6).
- **B-11(d) [MENOR]** — preâmbulo segue chunk citável com boilerplate (`4591-1964/001__preambulo.json` `tipo:"preambulo"`, retrievável).
- **B-12(c) [SÉRIO]** — trava **FATAL_ERROR (COMAER/CONPRESP)** existe no `travas_operacionais_v6.1.json` mas em `oodc.py` cai em `blocos_nao_avaliados` (string informativa) — **não é executada nem tem campo próprio**. Gabarito aeronáutico/tombamento não dispara.
- **B-12(d) [SÉRIO]** — citação do engine é pela **LEI inteira** (`FONTE_LEGAL` = blob de 6 leis; `dispositivo:"Outorga Onerosa…(PDE/LPUOS)"`), não por artigo (art. 128 PDE). Fura a granularidade de B-12 e o espírito de 1.7.

### Limitações DECLARADAS (não-defeitos, dependem do Drive)
- B-3 Fs/Fp parciais (3 entradas cada, `_REF`; não inventa mediana de faixa — honesto). · B-1 `tabelas/` vazio no main (só `.gitkeep`) **— já FECHADO na branch órfã**. · B-4 14 municipais não-verbatim (`confianca:baixa`, banner "REQUER re-captura"). · B-5/B-6 sem camada semântica / grafo de remissões.

---

## 5. ÍNDICE DE ACHADOS (priorizado)

| ID | Sev | Achado | Onde fica | Estado |
|---|---|---|---|---|
| N-3 | ALTO | Produto preso na branch `project-audit-roadmap` (B-1/TDC verbatim/E5) + SSOT do main mente "0%" | caixa-de-saida (cross-repo, PR a main) + B-17 | depositado |
| N-1 | CRÍTICO | 4 leis IPTU com `indexado` falso (0 chunks/0 index) | B-15 | depositado |
| N-2 | SÉRIO | MANIFESTO defasado vs disco (−4 leis) | B-16 | depositado |
| F-1 | ALTO | `gate-fechamento.sh` falso-verde vs `fechar-instancia.py` | B-18 | depositado |
| N-5 | MÉDIO | Furos hook v2 (H-1 dedup, H-2 suja árvore) | B-19 + caixa-de-saida (afeta o template do escritório) | depositado |
| B-11c | SÉRIO | 280 dups + zero vigência-por-chunk | B-11 (já aberto) | confirmado |
| B-12c/d | SÉRIO | FATAL não-executada + citação por lei-inteira | B-12 (já aberto) | confirmado |

## 6. O QUE FOI FEITO NESTA SESSÃO
1. Caixa verificada; pacote de padronização do escritório **consolidado** (FF na branch de trabalho).
2. Auditoria profunda 3-lentes rodada; este laudo lavrado.
3. Achados depositados: este doc + `caixa-de-saida/para-escritorio/` (cross-repo) + `BACKLOG.md` (B-15..B-19) + REGISTRO/ATA atualizados.
4. **NÃO** feito (fora do escopo "executar padrões + auditar + depositar", aguarda acionamento cadenciado): cirurgia de corpus (indexar as 4 leis / corrigir rótulo), B-11/B-12, e o **PR de `project-audit-roadmap` ao main** (decisão do escritório/MOU).
