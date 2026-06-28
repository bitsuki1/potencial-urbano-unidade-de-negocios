# DO ESCRITÓRIO → Potencial Urbano / RAG Jurídico IPTU/TDC (canal de diretrizes, D44)
> SSOT das diretrizes do **Escritório do MOU (PMO)** para esta unidade. O escritório ESCREVE aqui (datado/atribuído);
> o **orquestrador do Potencial Urbano** APLICA respeitando o gate do projeto (D21). Diretriz = proposta fundamentada, não ordem cega.
> Via de volta (do projeto ao escritório): pelo MOU (canal vivo) ou `caixa-de-entrada/` do escritório.
> **Trazido pelo Escritório do MOU — 2026-06-18.**
>
> **PRINCÍPIO-DOCUMENTO-VIVO (2026-06-18):** conteúdo ESTÁVEL (identidade, doutrina, diretrizes, vacinas) fica inline;
> estado VOLÁTIL (contagens, status do pipeline, lotes carregados) vira **PONTEIRO ao SSOT real** — nunca cópia.
> Cópia de dado volátil apodrece a cada trabalho e cria duas verdades (fere D1 + zero-compressão).


## 🔒 REGRA DE OURO + CAIXAS v2 (modelo carregar-depois · slug `potencial-urbano`)
> SSOT: `escritorio-do-mou/processos/COMO-FUNCIONAM-AS-CAIXAS.md`. Naming: `caixa-de-entrada/`+`caixa-de-saida/`.
- NUNCA escreva no canônico do Escritório (a caneta é do maestro, D56/D104). Você só toca a sua `caixa`.
- MANDAR: escreva `caixa-de-saida/para-<destino>/AAAA-MM-DD_potencial-urbano_assunto.md` (para-escritorio/ ou para-<outro>/). Commit. FIM.
- RECEBER: no boot, leia `caixa-de-entrada/` PRIMEIRO; aplique; mova p/ `caixa-de-entrada/processados/`.
- O escritório CARREGA as cartas quando co-montado (você não escreve em outro repo). Resposta a "posso escrever no escritório?": NÃO.

---

> **Arquivo GERENCIAL do escritório (canal D44) — NÃO é instrução de sistema do Claude Code.** Não substitui a constituição deste repo (`CLAUDE.md`). Diretriz aplicada sob o gate do projeto (D21).

## Identidade do escritório (estável)
O escritório NÃO comanda o Potencial Urbano; ele LÊ os documentos, mantém o registro do portfólio e **destrava a esteira** (D26)
— a esteira é **ideia → plano → design → desenvolvimento → deploy → operação**.
Mede-se por bloqueio de PROJETO removido, não por documento produzido. **ARMADO ≠ DESTRAVADO.**
Doutrina: zero-compressão · dialético · agnosticismo · nada se joga fora. (SSOT da doutrina = `escritorio-do-mou`.)

**Quando o orquestrador do Potencial Urbano DISCORDA de uma diretriz (gate D21):** não aplica às cegas — registra a contraproposta
(motivo + alternativa) e devolve ao escritório pelo MOU (canal vivo) ou pela `caixa-de-entrada/` do escritório. Diretriz é proposta.

---

## Onde ver o estado vivo (ponteiros — não copiar aqui)

> **Estado VOLÁTIL não vive aqui (PRINCÍPIO-DOCUMENTO-VIVO).** Contagens e status de pipeline
> vivem em `MANIFESTO.json` (agora GERADO e populado) e no `CODEX-DO-PROJETO.md §ESTADO` + `HANDOFF-E-PENDENCIAS.md`.
> Baseline desta tabela reescrita em **2026-06-19** pela Auditoria triplo-limpo do Escritório (correção do congelamento "tudo vazio" de 2026-06-18, que apodreceu quando o corpus foi carregado).

| O que | SSOT (ponteiro — leia lá o número de hoje) |
|---|---|
| **Constituição do projeto** (princípios, arquitetura, pipeline, Gens) | `CLAUDE.md` (raiz) — Partes 1–4, invioláveis |
| **Documento de fundação completo** (Partes 5–6: prompt extrator + instanciação) | `PROJETO-RAG-JURIDICO-IPTU-TDC.md` (raiz) |
| **Estado/contagem/status de CADA item do corpus** | `MANIFESTO.json` (raiz) — GERADO por `scripts/consolidar.py`; **populado** (não mais skeleton) |
| **Estado oficial geral + decisões + pendências** | `CODEX-DO-PROJETO.md §ESTADO` e `HANDOFF-E-PENDENCIAS.md` |
| **Prompt extrator universal** (extração pura — Gen Técnico-RAG) | `extracao/PROMPT-EXTRATOR-UNIVERSAL.md` |
| **Zona de despejo / ingestão** (brutos que o MOU sobe) | `_entrada/` (`iptu/`, `tdc/`, `misto/`) — ver `_entrada/README.md` |
| **Leis** (texto normativo limpo + metadados) | `leis/federal/`, `leis/municipal-sp/` — contagem viva no MANIFESTO |
| **Jurisprudência** (acórdãos, temas STJ/STF) + brutos | `jurisprudencia/` (+ `jurisprudencia/_capturas/`) — contagem viva no MANIFESTO |
| **Tabelas extraídas** (input de engine) | `tabelas/` |
| **Engines determinísticos** (fórmulas IPTU/TDC — NUNCA dentro das leis) | `engines/iptu/`, `engines/tdc/` (+ `FORMULAS-CONSOLIDADAS.md`) |
| **Teses geradas** (GERADO — não editar à mão) | `tese/iptu/`, `tese/tdc/` |
| **Extrações brutas** (saídas do prompt extrator) | `extracao/` |
| **RAG** (chunks e índice vetorial) | `rag/chunks/`, `rag/index/` |
| **Ground-truth de validação** | `evals/ground-truth/` |
| **GitHub Actions** (consolidação serial) | `.github/workflows/consolidar.yml` — **LIGADA** (regenera `MANIFESTO.json` a cada push) |
| **Banco de dados** (a "casa do dado" — RAG/PostGIS/engine) | Supabase `potencial-urbano-iptu-tdc` (ref `csnalylpvysjvejgsymr`, `sa-east-1`) — hoje só `governanca` + `public/PostGIS`; schemas dos artefatos a criar (ver `BETA-CONTINUO.md §4`) |

---

## Diretrizes vigentes (D-PU) — estáveis

| # | Diretriz | Porquê | Estado |
|---|---|---|---|
| **D-PU-1** | **Supabase Storage para brutos pesados** (PDFs volumosos fora do git) + git para texto limpo + metadados + resultados | padrão de dados do portfólio (já decidido pelo MOU, 2026-06-17); desafoga o git e evita corrupção de PDF | em vigor; corpus textual no git; **nenhum bruto pesado subido ao Storage ainda** |
| **D-PU-2** | **Documentos vêm MISTURADOS (IPTU + TDC juntos)** → receber tudo em `_entrada/misto/`; a triagem/tagueamento determinístico (Etapa 2 do pipeline) é a tarefa central | decisão MOU 2026-06-17; não se separa na mão antes da triagem | em vigor; **1º lote recebido** (24 crus em `_entrada/misto/`, processados) |
| **D-PU-3** | **✅ RESOLVIDA (MOU 2026-06-20): base inicial = TDC.** O pipeline começa por TDC; ground-truth/validação concentram em TDC primeiro; IPTU vem depois (replica) | urgência/volume define foco; pipeline replica para a segunda base depois | **DECIDIDO — TDC.** Encerra a divergência M-24/M-49 |
| **D-PU-4** | **GitHub Action `consolidar.yml` — LIGADA (2026-06-20)** — `scripts/consolidar.py` regenera o `MANIFESTO.json` a cada push; índice RAG + mestres de tese a estender quando houver chunks/teses | automação do pipeline (Princípio 1.5/2.3) | **FEITO (base)** — manifesto agora vivo (59 itens); estender p/ índice RAG quando o fatiamento existir |
| **D-PU-5** | **1º lote CHEGOU (2026-06-19)** — corpus de 59 itens (27 leis + 32 juris) já no repo; `_entrada/misto/` recebeu 24 crus | o funil já tem insumo para rodar | **SUPERADO** — bloqueio agora é INTERNO (fatiamento→indexação + re-ingestão verbatim das 15 municipais), não mais entrada |

---

## Pendências que dependem do MOU (cobrança)

- **[DECISÃO ✅ RESOLVIDA 2026-06-20] IPTU × TDC: base inicial = TDC** (decidido pelo MOU). O pipeline começa por TDC; IPTU replica depois.
- **[AÇÃO ✅ FEITA 2026-06-19] 1º lote recebido** (24 crus → corpus de 59 itens). Bloqueio agora é INTERNO (fatiamento/indexação + re-ingestão verbatim das 15 municipais), não mais entrada.
- **[TÉCNICO — FEITO 2026-06-20]** `consolidar.yml` criada (regenera `MANIFESTO.json` via `scripts/consolidar.py` a cada push). Estender para índice RAG + mestres de tese quando houver fatiamento/teses.

---

## Registro dialético

- TESE: o canal D44 instala a identidade do PMO no projeto de forma rastreável (datada/atribuída); o PRINCÍPIO-DOCUMENTO-VIVO mantém o documento vivo sem apodrecer — dado volátil no SSOT real, diretriz estável inline.
- ANTÍTESE: o escritório não comanda (D2); diretriz aqui não pode virar ordem que atropele o gate do projeto (D21); ponteiros só funcionam se os SSOTs forem mantidos vivos (responsabilidade do orquestrador do Potencial Urbano). O `MANIFESTO.json` agora é gerado por `scripts/consolidar.py` (Action `consolidar.yml` ligada em 2026-06-20) e está populado — mas a Action por ora só regenera o MANIFESTO; índice RAG e mestres de tese ainda não (a estender quando houver chunks/teses).
- CONCILIAÇÃO (provisória): estrutura do projeto está sólida (estrutura criada, constituição clara, Gens mapeados, corpus de 59 itens carregado); bloqueio primário agora é INTERNO (fatiamento→indexação + re-ingestão verbatim das 15 municipais), não mais falta de dado de entrada. A próxima ação concreta envolve decisões do MOU (ver pendências) + avanço da esteira.
- VACINA (1 — não criar 2º CLAUDE.md): este repo já tem `CLAUDE.md` como constituição do RAG (Partes 1–4); NÃO criar um segundo `CLAUDE.md`. Identidade do escritório vai neste arquivo (`DO_ESCRITORIO.md`) + seção curta adicionada ao `CLAUDE.md` existente.
- VACINA (2 — IPTU/TDC ≠ Tema 1130 IRRF): Potencial Urbano trata IPTU (imposto predial municipal) e TDC (tributo/contribuição imobiliária). **Nenhuma relação com o Tema 1130 do STF (IRRF sobre PLR/lucros)** — matérias completamente distintas. Se algum documento em `_entrada/` vier com referência a "stf-tema-1130", marcar `[A VERIFICAR]` e isolar; nunca criar ponte automática com o corpus IPTU/TDC.

## Diretrizes — 2026-06-20 (trazido pelo Escritório do MOU)

### D-PU-AMORAL — Postura AMORAL do MOU (D106) sobre senhas + LGPD
O MOU declarou em 2026-06-20: *"não temos problemas com LGPD nem com senhas expostas e somos amoral"*. Risco PERMANENTEMENTE ACEITO em senhas E LGPD/PII de terceiro. **O gen do PU NÃO levanta** rotação de credencial nem "exposição LGPD" ao MOU — nem em auditoria. 1 linha factual + segue. **Implicação concreta:** o item M-30 (LGPD em produto) está FECHADO; PII em documento ingerido não é mais bloqueio nem pendência. Mecanismo permanece (RLS deny-all no schema `governanca`). SSOT: `escritorio-do-mou/CLAUDE.md` topo + D106.

### D-PU-MANUAIS — Manuais GIT e SUPABASE oficializados (PISO D75)
- `escritorio-do-mou/processos/PROCESSO-USO-GIT.md` — caneta D56, branch por instância, lavrar main D19.
- `escritorio-do-mou/processos/PROCESSO-USO-SUPABASE.md` — mapa dos 3 projetos. O do PU está mapeado (`potencial-urbano-iptu-tdc`, ref `csnalylpvysjvejgsymr`, schema `governanca`). M-41 (toggle `public` no Exposed schemas) ainda no MOU.

### D-PU-D2 — PMO ATIVO (D2 reescrita 2026-06-20)
O escritório NÃO é mais "camada de leitura". É **PMO ATIVO que SERVE; arruma, destrava, executa**. Para o PU isso significa: o escritório pode rodar inventário, propor estrutura, escrever ponteiros — mas a **estratégia jurídico-fiscal e o destravamento do pipeline (1 lei verbatim→fatiar→indexar→consulta)** são do gen PU. A auditoria 2026-06-20 gritou *"PU está ARMADO, não DESTRAVADO"* (BLOQUEIOS-REMOVIDOS): meta-auditoria > produto. Régua D26: andar 1 lei ponta-a-ponta, não fazer mais auditoria.

### D-PU-OCR — Pré-condição da re-ingestão verbatim (destrava M-24 sem cair em armadilha)
Antes de re-rodar os prompts em `docs/PROMPTS-EXTRACAO-EXTENSAO.md` para capturar as 15 leis municipais ainda não-verbatim, **validar arquivo a arquivo** se cada item em `_entrada/misto/` (e demais zonas de despejo) é **TEXTO** (`.md`/`.txt`/PDF com camada de texto) ou **IMAGEM** (`.pdf` scan/`.jpg`/`.png`):
- **Texto** → vai direto ao extrator.
- **Imagem** → passar OCR ANTES (Tesseract / Vision / Google Document AI / a extensão Claude lendo a imagem) e gravar a transcrição em `_entrada/misto/<arquivo>.ocr.md` ao lado do original (D24 — nunca apagar).
- Sem essa validação, o LLM "lê" PDF de scan e devolve citação que parece boa mas é alucinação (Codex C-005). Vacina já registrada no MAESTRO §6 e no PERFIL_MOU "regra de FORMATO". Aplica-se também aos artefatos do Drive que descerem ao repo.

### D-PU-MANIFESTO — Manter o MANIFESTO.json conforme estado real (não inflar contagem)
A auditoria 2026-06-20 contestou a contagem "27 leis verbatim integrais". O manifesto regenerado pela Action `consolidar.yml` deve mostrar **status real por item** (`bruto` × `fatiado` × `tagueado` × `validado` × `indexado`) — verbatim integral confirmado SOMENTE com prova (citação direta validada). Não rotular `validado` por suposição (P1.7). Atualizar contagem no `MANIFESTO.json` se estiver com label desatualizado.

### D-PU-STRANDED (2026-06-25) — branch de orquestrador não-consolidada (forense do escritório)
> Trazido pelo Escritório do MOU (PMO). Forense de fechamento. O escritório recuperou o additive seguro; o resto é reconciliação SUA (D104).
- **4 leis municipais SP IPTU/zoneamento RECUPERADAS ao main** por mim (additive): Lei 16.402/2016 (zoneamento), Decreto 57.443/2016, Leis 16.642/2017, 17.733/2022. Decisão "começa por TDC" mantida — guardadas para a fase IPTU.
- **`claude/project-audit-roadmap-2thi1g`** (24/jun, +14 commit, ~91 arquivos únicos): além das 4 leis (já recuperadas), contém material de auditoria/mapeamento IPTU-TDC. ⚠️ tem arquivos que CONFLITAM com o main (ex.: outras leis com versão diferente — `lei-16050`, `lei-17844` divergem; NÃO sobrescrever às cegas, foi pego no resgate). Reconciliar: o que é corpus novo (additive) entra; versão de lei já existente, você decide a canônica. DoD: branch reconciliada OU declarada superseded. Gatilho: onda PU / orquestrador montado.
- **🟥 DECISÃO DO MOU (2026-06-28) — REGRA "VERBATIM SEMPRE" + dono da execução.** Em conflito de lei entre a branch e o main, a versão **VERBATIM INTEGRAL** (a da branch — texto da lei na íntegra, `confianca_extracao:alta`) **SEMPRE** ganha sobre o stub/resumo do main (stub não se cita — fere P1.7). Aplica-se a `lei-16050/2014` (PDE, 7.172 linhas verbatim vs 14 no main) e `lei-17844/2022` (3.748 vs 14). **Quem EXECUTA = o Escritório/instância do PU sob o gate (D38/D21); NÃO o MOU** (balcão único, D56 — ele não roda prompt). **Timing:** executar DEPOIS de "arrumar a casa" (regularização), ordem do MOU 2026-06-28. **Refino factual (regularização 2026-06-28, auditado anti-self):** a branch tem **389 arquivos únicos** (não ~91) — ouro real: Q14 6.715 valores, PDE/17.844 verbatim, E5 provado. NÃO apagar a branch antes do PR mergeado e provado verde.

## Diretrizes — 2026-06-27 · PACOTE DE PADRONIZAÇÃO DE PROJETOS (trazido pelo Escritório do MOU)

> **Origem:** auditoria profunda da frente "padronização de projetos" (sessão maestro+PU co-montado, anti-self D108; 2 escrutínios — chão do PU vs `processos/PADRAO-DE-REPO.md` + consolidação de decisões/beta do escritório). **Regra desta sessão (MOU):** o escritório NÃO escreve no canônico do PU; deposita aqui e a instância do PU EXECUTA sob o gate do projeto (D21). Tudo abaixo é **reversível** (git) e fecha DEs já abertas no escritório (DE-28/31/32/24/27/34/38) — não são decisões novas, é a DESCIDA de políticas já lavradas (D119/D120/D128/D143). **Vacina "PROPAGAR ≠ EMPACOTAR" (DE-34):** estas diretrizes só "chegam" quando aplicadas no canônico do PU pela instância do projeto — ESCRITAS aqui = empacotadas; APLICADAS no repo = entregues.

### D-PU-D128 — Declarar o Tipo (D128) no cérebro `[fecha DE-28/A-054 p/ o PU]`
**O quê:** o `CLAUDE.md` do PU não declara o tipo do repo. Adicionar, no cabeçalho (junto às linhas `>` do topo): `> **Tipo (D128):** UNIDADE` (Potencial Urbano = unidade de negócio do portfólio). **Porquê:** sem a tag, qualquer inventário do portfólio por tipo não classifica o PU (padrão `PADRAO-DE-REPO.md §1`). **DoD:** `grep "Tipo (D128)" CLAUDE.md` retorna a linha. **Estado:** ✅ APLICADO 2026-06-27 (`> **Tipo (D128):** UNIDADE` no cabeçalho do CLAUDE.md).

### D-PU-MR4 — POLÍTICA D120: área de trabalho × repo de produto `[fecha DE-31/MR-4 p/ o PU]`
**O quê:** a **área de trabalho** do escritório é o repo do PMO (`escritorio-do-mou`); os repos de **produto/unidade** (como este) são **consulta + execução do projeto** — o escritório toca via git, atribuído e sob o gate, nunca como comando (D2). **Porquê:** política "desce JÁ" desde 2026-06-21; PU estava ⬜ há 6 dias (DE-31). **DoD:** seção no `CLAUDE.md §Escritório do MOU` (ou neste arquivo, marcada aplicada) com a regra D120; `grep "D120" CLAUDE.md`. **Estado:** ✅ APLICADO 2026-06-27 (`CLAUDE.md §Políticas transversais`).

### D-PU-MR5 — POLÍTICA D119: "TODOS LEEM, só a KEEPEE TOCA" o DEV `[fecha DE-32/MR-5 p/ o PU]`
**O quê:** o repositório de DESENVOLVIMENTO do Profinders (org `keepee-facilities`) tem **LEITURA liberada** a qualquer unidade/instância (inventário/as-built) mas **ESCRITA EXCLUSIVA da unidade Keepee**. O PU **NUNCA escreve** no DEV. A trava já está no seu `.claude/settings.json` (deny `keepee-facilities*`); esta diretriz só registra a POLÍTICA por escrito no canônico. **Porquê:** D119 revisa D29; "desce JÁ" desde 2026-06-21; PU ⬜ (DE-32). **DoD:** menção da política D119 no `CLAUDE.md`/este arquivo marcada aplicada; `grep "D119" `. **Estado:** ✅ APLICADO 2026-06-27 (`CLAUDE.md §Políticas transversais`; a trava no settings já existia).

### D-PU-REGISTRO — Registro de instâncias + ata (PADRAO-DE-REPO §4) `[gap PU-PAD-02/03]`
**O quê:** o PU não tem `REGISTRO-DE-INSTANCIAS.md` nem `ATA-VIVA-SESSAO.md`. Criar ambos (raiz ou `processos/`) e ligar o `.claude/hooks/surface-backlog.sh` para AUTO-ESTAMPAR a linha de instância (data+branch+HEAD+chapéu) no boot e capturar a fala do MOU na ata. Modelo: `escritorio-do-mou/processos/REGISTRO-DE-INSTANCIAS.md`. **Porquê:** sem registro, instância perdida não deixa rastro (dor que gerou o mecanismo, MOU 2026-06-25); hoje `gate-fechamento.sh` só avisa, não falha. **DoD:** nova sessão deixa linha ABERTA automática + ata populada na 1ª resposta; elevar o `warn` do gate a `fail` quando o REGISTRO existir. **Estado:** ✅ APLICADO 2026-06-27 (`REGISTRO-DE-INSTANCIAS.md` + `ATA-VIVA-SESSAO.md` criados; `surface-backlog.sh` auto-estampa a instância no boot; o `gate-fechamento.sh` já trata REGISTRO ABERTA como fail).

### D-PU-HANDOFF — Resolver as superfícies de retomada divergentes `[gap PU-PAD-06 / refina A-009]`
**O quê:** o PU tem ≥5 superfícies de handoff que se contradizem — `HANDOFF-SURFACES.txt` lista `CLAUDE.md`+`DO_ESCRITORIO.md`; o hook instrui `PROXIMA-INSTANCIA.md → HANDOFF-E-PENDENCIAS.md → MANIFESTO.json`; `PU.md` se diz "ponto de entrada único"; `CODEX §ESTADO` é 5º candidato. Eleger **1 surface primária** (rec.: `PROXIMA-INSTANCIA.md`, que o hook já surfaça) e alinhar o `HANDOFF-SURFACES.txt` a ela; marcar os demais como secundários. **Porquê:** A-009 (re-homed ao PU) — instância nova garimpa estado em 4-5 lugares divergentes. **DoD:** `HANDOFF-SURFACES.txt` e o hook apontam a MESMA surface primária; um único doc declara "estado vivo aqui". **Estado:** ✅ APLICADO 2026-06-27 (`HANDOFF-SURFACES.txt` reescrito: `PROXIMA-INSTANCIA.md` primária, alinhado ao hook; `CODEX §ESTADO`/`PU.md` rebaixados a secundários).

### D-PU-DENY — Reconciliar a deny do `settings.json` ao spec v2 `[gap PU-PAD-08 / A-147 / DE-34]`
**O quê:** confirmar/expandir o bloco `deny` do `.claude/settings.json` do PU ao spec corrente (A-147, 2026-06-26): além de `escritorio-do-mou/**` e `keepee-facilities*/**`, garantir cobertura de `Edit/Write/MultiEdit` (os 3 verbos) e, quando o modelo de caixas v2 entrar, **liberar `caixa-de-entrada/**`/`caixa/**`** para não bloquear o próprio depósito do projeto (a deny v1 A-113 é larga demais). **Porquê:** deny inconsistente = trava parcial (mecanismo > memória). ⚠️ deny é defense-in-depth (shell/`python3` furam — a trava REAL é o hook da DE-36, lado escritório). **DoD:** tentativa de Edit em `escritorio-do-mou/cadastro/PROJETOS.md` numa sessão de PU = bloqueada; registrar o output literal. **Estado:** ✅ CONFORME-v2 (sem mudança) 2026-06-27 — o deny atual `Edit/Write/MultiEdit(**/escritorio-do-mou/**)` é BLANKET e já cobre `cadastro/`, `caixa-de-saida/`, `.claude/` etc. (superset do A-147). No modelo v2 o projeto NÃO escreve no escritório → o blanket é o correto; o C1 (depositar p/ o escritório) não existe mais (o sync recolhe da `caixa-de-saida/` do projeto). Nada a expandir.

### D-PU-FRENTES — PAUTA de DELIBERAÇÃO (MR-14, modo deliberação — NÃO é imposição) `[abre a discussão]`
**O quê:** o MOU decidiu (2026-06-26, MR-14) que **um tema denso preso dentro do documento-mãe vira FRENTE própria** (documento à parte + desenho sob ciclo "edita → MOU valida → desenha"). Isso **NÃO desce por imposição**: o escritório **abre a pauta**, e o **orquestrador do PU delibera as frentes DIRETO com o MOU**, que consolida. (Origem: Profinders → "Trilhas das Personas".) **Status do PU: 🗣️ discussão a abrir.**

**Frentes candidatas que o escritório enxergou no doc-mãe do PU** (`CLAUDE.md` Partes 1–4 + `PROJETO-RAG-JURIDICO-IPTU-TDC.md`) — STARTER para a deliberação, não decisão:
- **F-PU-A · Engine de Cálculo (TDC OODC + IPTU progressivo)** — o subsistema determinístico de NÚMERO (CLAUDE 1.1/1.3 + Gen Matemática + `engines/tdc/oodc.py` + tabelas Q14/Quadro3/Quadro5). Doc próprio: fórmulas + derivação + exemplos trabalhados + **desenho do fluxo de cálculo**. Hoje espalhado entre `engines/` e os itens B-1/B-2/B-3/B-12 do BACKLOG.
- **F-PU-B · Produto: Lista de Alvos por Imóvel** — o ENTREGÁVEL de negócio (IPTU 2026 × LOTES × Q14 × zoneamento → oportunidades TDC/IPTU por imóvel + dono). Doc próprio: spec do produto + modelo de dados + **desenho do pipeline de cruzamento**. Hoje preso como B-2 no BACKLOG — é o "valor" do PU.
- **F-PU-C · Corpus Jurídico & RAG** — ingestão verbatim → chunking → retrieval híbrido → citação (CLAUDE Partes 2–3 + `scripts/`). Já tem `scripts/README.md`; candidata a frente formal (a espinha técnica).
- **F-PU-D · Tese/Parecer Jurídico** — camada argumentativa tese/antítese/vacina (Gen Advogado, CLAUDE 1.2/Parte 4). Ainda não construída; candidata FUTURA.

**Como deliberar (MR-14):** o orquestrador do PU leva estas candidatas (e outras que enxergar) ao MOU e **decide COM ele** quais viram frente própria; consolidadas → o orquestrador deposita na `caixa-de-saida/para-escritorio/` e a caneta reflete no `MAPA-DA-UNIDADE` do PU. **Referência de FORMATO** (não clonar conteúdo): `profinders/MAPA-DA-UNIDADE.md` (frente VD-3). **DoD:** coluna PU em MR-14 vira ✅ quando o MOU consolidar as frentes do PU. **Estado:** 🗣️ DELIBERADO PELO ORQUESTRADOR 2026-06-27 — recomendação: A/B/C viram frente, D futura (ordem de valor: B Produto lidera, A Engine + C Corpus = combustível; pré-condição = consolidar B-17). Depositada em `caixa-de-saida/para-escritorio/2026-06-27_potencial-urbano_pague-tudo-e-deliberacao-frentes.md`. **Aguarda o MOU consolidar** (→ MAPA-DA-UNIDADE).

### D-PU-CAIXAS-v2 — Modelo de caixas v2 (D143/DE-39) — AGUARDA o piloto do escritório `[heads-up, NÃO agir ainda]`
**O quê:** o modelo de caixas v2 (`caixa/{entrada,saida,processados}/` no projeto + gate de pickup) ainda **NÃO é operacional** (0/7 projetos; `PROTOCOLO-DE-CAIXAS` = EM-ADOÇÃO). O escritório vai construir o motor de sync + rodar **piloto na SBA, provar 2×** antes de escalar (DE-39). **Não criar a estrutura `caixa/` no PU agora** — esperar o piloto + a ordem (evita lock-in sobre modelo instável). **Porquê:** PRO-08 da auditoria (v1→v2 mudou em 1 dia). **Estado:** 🟡 LADO-PROJETO BOOTSTRAPADO 2026-06-27 — criados `caixa-de-entrada/{,processados/}` + `caixa-de-saida/{para-escritorio/,processados/}` (PROTOCOLO §1, naming idêntico ao escritório); `surface-backlog.sh` surfaça a `caixa-de-entrada/` no boot; `gate-fechamento.sh` FALHA com recado não-aplicado (§4). **Falta (escritório):** o sync (`sync-caixas.py`) rodar o ciclo completo e o PILOTO provar 2× — só na sessão-escritório-sync (DE-39). _(Revisão: criei a estrutura do lado-projeto porque o MOU mandou "executar todas as pendências da frente" no PU; é 1 repo, reversível, não é o lock-in de 7 que a PRO-08 veta.)_
