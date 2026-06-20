# DO ESCRITÓRIO → Potencial Urbano / RAG Jurídico IPTU/TDC (canal de diretrizes, D44)
> SSOT das diretrizes do **Escritório do MOU (PMO)** para esta unidade. O escritório ESCREVE aqui (datado/atribuído);
> o **orquestrador do Potencial Urbano** APLICA respeitando o gate do projeto (D21). Diretriz = proposta fundamentada, não ordem cega.
> Via de volta (do projeto ao escritório): pelo MOU (canal vivo) ou `caixa-de-entrada/` do escritório.
> **Trazido pelo Escritório do MOU — 2026-06-18.**
>
> **PRINCÍPIO-DOCUMENTO-VIVO (2026-06-18):** conteúdo ESTÁVEL (identidade, doutrina, diretrizes, vacinas) fica inline;
> estado VOLÁTIL (contagens, status do pipeline, lotes carregados) vira **PONTEIRO ao SSOT real** — nunca cópia.
> Cópia de dado volátil apodrece a cada trabalho e cria duas verdades (fere D1 + zero-compressão).

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
| **D-PU-1** | **Supabase Storage para brutos pesados** (PDFs volumosos fora do git) + git para texto limpo + metadados + resultados | padrão de dados do portfólio (já decidido pelo MOU, 2026-06-17); desafoga o git e evita corrupção de PDF | em vigor; nenhum documento subido ainda |
| **D-PU-2** | **Documentos vêm MISTURADOS (IPTU + TDC juntos)** → receber tudo em `_entrada/misto/`; a triagem/tagueamento determinístico (Etapa 2 do pipeline) é a tarefa central | decisão MOU 2026-06-17; não se separa na mão antes da triagem | em vigor; aguarda 1º lote |
| **D-PU-3** | **[ABERTA — depende do MOU] Decisão: por qual base começar — IPTU ou TDC?** A resposta determina a ordem do pipeline e onde concentrar a validação de ground-truth primeiro | urgência/volume define foco; pipeline replica para a segunda base depois | **PENDÊNCIA AO MOU** — não destravar o pipeline sem esta decisão |
| **D-PU-4** | **GitHub Action `consolidar.yml` — LIGADA (2026-06-20)** — `scripts/consolidar.py` regenera o `MANIFESTO.json` a cada push; índice RAG + mestres de tese a estender quando houver chunks/teses | automação do pipeline (Princípio 1.5/2.3) | **FEITO (base)** — manifesto agora vivo (59 itens); estender p/ índice RAG quando o fatiamento existir |
| **D-PU-5** | **1º lote CHEGOU (2026-06-19)** — corpus de 59 itens (27 leis + 32 juris) já no repo; `_entrada/misto/` recebeu 24 crus | o funil já tem insumo para rodar | **SUPERADO** — bloqueio agora é INTERNO (fatiamento→indexação + re-ingestão verbatim das 14 municipais), não mais entrada |

---

## Pendências que dependem do MOU (cobrança)

- **[DECISÃO] IPTU × TDC: por qual base começar?** (maior volume/urgência — ver `_entrada/README.md`). Esta decisão destrava a ordem do pipeline.
- **[AÇÃO] Subir o 1º lote de documentos** em `_entrada/` (bruto pesado via Supabase Storage; texto/imagem direto no git). Sem o lote, o projeto está ARMADO mas não DESTRAVADO.
- **[TÉCNICO — FEITO 2026-06-20]** `consolidar.yml` criada (regenera `MANIFESTO.json` via `scripts/consolidar.py` a cada push). Estender para índice RAG + mestres de tese quando houver fatiamento/teses.

---

## Registro dialético

- TESE: o canal D44 instala a identidade do PMO no projeto de forma rastreável (datada/atribuída); o PRINCÍPIO-DOCUMENTO-VIVO mantém o documento vivo sem apodrecer — dado volátil no SSOT real, diretriz estável inline.
- ANTÍTESE: o escritório não comanda (D2); diretriz aqui não pode virar ordem que atropele o gate do projeto (D21); ponteiros só funcionam se os SSOTs forem mantidos vivos (responsabilidade do orquestrador do Potencial Urbano). O `MANIFESTO.json` agora é gerado por `scripts/consolidar.py` (Action `consolidar.yml` ligada em 2026-06-20) e está populado — mas a Action por ora só regenera o MANIFESTO; índice RAG e mestres de tese ainda não (a estender quando houver chunks/teses).
- CONCILIAÇÃO (provisória): estrutura do projeto está sólida (estrutura criada, constituição clara, Gens mapeados, corpus de 59 itens carregado); bloqueio primário agora é INTERNO (fatiamento→indexação + re-ingestão verbatim das 14 municipais), não mais falta de dado de entrada. A próxima ação concreta envolve decisões do MOU (ver pendências) + avanço da esteira.
- VACINA (1 — não criar 2º CLAUDE.md): este repo já tem `CLAUDE.md` como constituição do RAG (Partes 1–4); NÃO criar um segundo `CLAUDE.md`. Identidade do escritório vai neste arquivo (`DO_ESCRITORIO.md`) + seção curta adicionada ao `CLAUDE.md` existente.
- VACINA (2 — IPTU/TDC ≠ Tema 1130 IRRF): Potencial Urbano trata IPTU (imposto predial municipal) e TDC (tributo/contribuição imobiliária). **Nenhuma relação com o Tema 1130 do STF (IRRF sobre PLR/lucros)** — matérias completamente distintas. Se algum documento em `_entrada/` vier com referência a "stf-tema-1130", marcar `[A VERIFICAR]` e isolar; nunca criar ponte automática com o corpus IPTU/TDC.
