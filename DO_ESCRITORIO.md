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

Estado verificado em 2026-06-18. Todos os ponteiros abaixo são arquivos reais no repo.

| O que | SSOT | O que tem lá |
|---|---|---|
| **Constituição do projeto** (princípios, arquitetura, pipeline, Gens) | `CLAUDE.md` (raiz) | Partes 1–4; invioláveis |
| **Documento de fundação completo** (Partes 5–6: prompt extrator + instanciação) | `PROJETO-RAG-JURIDICO-IPTU-TDC.md` (raiz) | fonte completa |
| **Estado do manifesto** (itens carregados, status pipeline de cada lei) | `MANIFESTO.json` (raiz) | GERADO pela Action; skeleton vazio em 2026-06-18 |
| **Prompt extrator universal** (instrução de extração pura — usada pelo Gen Técnico-RAG) | `extracao/PROMPT-EXTRATOR-UNIVERSAL.md` | prompt para Etapa 3 |
| **Zona de despejo / ingestão** (documentos brutos que o MOU sobe) | `_entrada/` (`iptu/`, `tdc/`, `misto/`) | vazia em 2026-06-18; ver `_entrada/README.md` |
| **Leis processadas** (texto normativo limpo + metadados) | `leis/` | vazia (skeleton) em 2026-06-18 |
| **Jurisprudência** (acórdãos, temas STJ/STF) | `jurisprudencia/` | vazia (skeleton) em 2026-06-18 |
| **Tabelas extraídas** (alíquotas, índices, faixas — input de engine) | `tabelas/` | vazia (skeleton) em 2026-06-18 |
| **Engines determinísticos** (fórmulas IPTU e TDC — NUNCA dentro das leis) | `engines/iptu/` e `engines/tdc/` | vazias (skeleton) em 2026-06-18 |
| **Teses geradas** (GERADO pela Action — não editar à mão) | `tese/iptu/` e `tese/tdc/` | vazias (skeleton) em 2026-06-18 |
| **Extrações brutas** (saídas do prompt extrator, um arquivo por Gen) | `extracao/` | só o prompt extrator; sem saídas ainda |
| **RAG** (chunks e índice vetorial) | `rag/chunks/` e `rag/index/` | vazias (skeleton) em 2026-06-18 |
| **Ground-truth de validação** | `evals/ground-truth/` | vazia (skeleton) em 2026-06-18 |
| **GitHub Actions** (consolidar.yml — a ligar) | `.github/workflows/` | ainda não existe (pendência técnica) |

---

## Diretrizes vigentes (D-PU) — estáveis

| # | Diretriz | Porquê | Estado |
|---|---|---|---|
| **D-PU-1** | **Supabase Storage para brutos pesados** (PDFs volumosos fora do git) + git para texto limpo + metadados + resultados | padrão de dados do portfólio (já decidido pelo MOU, 2026-06-17); desafoga o git e evita corrupção de PDF | em vigor; nenhum documento subido ainda |
| **D-PU-2** | **Documentos vêm MISTURADOS (IPTU + TDC juntos)** → receber tudo em `_entrada/misto/`; a triagem/tagueamento determinístico (Etapa 2 do pipeline) é a tarefa central | decisão MOU 2026-06-17; não se separa na mão antes da triagem | em vigor; aguarda 1º lote |
| **D-PU-3** | **[ABERTA — depende do MOU] Decisão: por qual base começar — IPTU ou TDC?** A resposta determina a ordem do pipeline e onde concentrar a validação de ground-truth primeiro | urgência/volume define foco; pipeline replica para a segunda base depois | **PENDÊNCIA AO MOU** — não destravar o pipeline sem esta decisão |
| **D-PU-4** | **GitHub Action `consolidar.yml` ainda não existe** — ela regenera o `MANIFESTO.json` + índice RAG + mestres de tese a cada push; sem ela o manifesto fica estático | pendência técnica que bloqueia automação do pipeline (Princípio 1.5/2.3) | **PENDÊNCIA TÉCNICA** — criar antes de subir o 1º lote real |
| **D-PU-5** | **Bloqueio real: falta o 1º lote de documentos** (ação do MOU) — sem documentos em `_entrada/` não há pipeline para rodar | nenhuma etapa do funil pode ser testada em vazio | **BLOQUEIO PRIMÁRIO** — o MOU sobe o lote; escritório roteia ao Gen Técnico-RAG |

---

## Pendências que dependem do MOU (cobrança)

- **[DECISÃO] IPTU × TDC: por qual base começar?** (maior volume/urgência — ver `_entrada/README.md`). Esta decisão destrava a ordem do pipeline.
- **[AÇÃO] Subir o 1º lote de documentos** em `_entrada/` (bruto pesado via Supabase Storage; texto/imagem direto no git). Sem o lote, o projeto está ARMADO mas não DESTRAVADO.
- **[TÉCNICO] Criar `consolidar.yml`** (GitHub Action que regenera `MANIFESTO.json` + índice RAG). Pode ser delegado a um Gen Técnico-RAG; precisa de aprovação de estrutura antes de ligar.

---

## Registro dialético

- TESE: o canal D44 instala a identidade do PMO no projeto de forma rastreável (datada/atribuída); o PRINCÍPIO-DOCUMENTO-VIVO mantém o documento vivo sem apodrecer — dado volátil no SSOT real, diretriz estável inline.
- ANTÍTESE: o escritório não comanda (D2); diretriz aqui não pode virar ordem que atropele o gate do projeto (D21); ponteiros só funcionam se os SSOTs forem mantidos vivos (responsabilidade do orquestrador do Potencial Urbano). O `MANIFESTO.json` é gerado pela Action que ainda não existe — ponteiro honesto mas de SSOT ainda inativo.
- CONCILIAÇÃO (provisória): estrutura do projeto está sólida (skeleton criado, constituição clara, Gens mapeados); bloqueio primário é operacional (falta o dado de entrada), não arquitetural. A próxima ação concreta é do MOU.
- VACINA (1 — não criar 2º CLAUDE.md): este repo já tem `CLAUDE.md` como constituição do RAG (Partes 1–4); NÃO criar um segundo `CLAUDE.md`. Identidade do escritório vai neste arquivo (`DO_ESCRITORIO.md`) + seção curta adicionada ao `CLAUDE.md` existente.
- VACINA (2 — IPTU/TDC ≠ Tema 1130 IRRF): Potencial Urbano trata IPTU (imposto predial municipal) e TDC (tributo/contribuição imobiliária). **Nenhuma relação com o Tema 1130 do STF (IRRF sobre PLR/lucros)** — matérias completamente distintas. Se algum documento em `_entrada/` vier com referência a "stf-tema-1130", marcar `[A VERIFICAR]` e isolar; nunca criar ponte automática com o corpus IPTU/TDC.
