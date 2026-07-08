# CLAUDE.md — Projeto RAG Jurídico IPTU/TDC (Potencial Urbano)
> Constituição do projeto (Partes 1–4 do documento de fundação `PROJETO-RAG-JURIDICO-IPTU-TDC.md`).
> Lida automaticamente por toda instância do Claude Code que tocar neste repo. Trazido pelo Escritório do MOU — 2026-06-17.
> Marca da unidade: ver o Escritório (decisão de marca em vigor: **SBA Negócios** é a marca do grupo; aqui a unidade é **Potencial Urbano**).
> **Tipo (D128):** UNIDADE — unidade de negócio do portfólio do MOU (não é ESCRITÓRIO, nem USO, nem HUB).

## PARTE 1 — Princípios invioláveis
Invariantes. Tudo se subordina a eles. Se uma decisão futura conflitar com um destes, o princípio ganha.

**1.1 — Quatro artefatos separados, nunca um só.**
| Artefato | O que é | Velocidade | Vira |
|---|---|---|---|
| **Lei / Norma** | Texto normativo (constituição, leis, decretos, súmulas, acórdãos) | Lenta | RAG |
| **Tabela / Valor** | Dados numéricos extraídos das leis (alíquotas, índices, faixas) | Lenta, mas é *dado* | Input de engine |
| **Fórmula / Engine** | Cálculo determinístico (alíquota progressiva IPTU, valuation TDC) | Média | Engine determinístico |
| **Tese / Antítese / Vacina** | Camada argumentativa, construída a partir das leis | Alta | Documento(s) de tese |

Tabela de lei é dado e sai do texto. Fórmula é engine e nunca mora dentro do corpus de leis.

**1.2 — Extrair puro → enriquecer → argumentar. Nunca na mesma passada.**
- **Extração pura:** só o que está literalmente no documento. Sem interpretar/calcular/opinar.
- **Enriquecimento:** cruzamento, lookups, ligação com jurisprudência. Etapa separada.
- **Tese:** síntese argumentativa, construída *depois*, sobre o corpus já limpo.

**1.3 — Número nasce no engine, nunca no LLM.** O LLM roteia e redige prosa; todo fato/valor vem de fonte determinística e é rastreável até o dispositivo legal de origem.

**1.4 — Funil de custo:** o modelo caro toca só a fração que importa (cascata + batch + caching — Parte 3).

**1.5 — Criação paralela, consolidação serial.** Cada instância só CRIA arquivos novos (um por lei); ninguém edita o mestre. A consolidação é uma GitHub Action que REGENERA os mestres a cada push (Git nunca dá conflito).

**1.6 — Toda norma tem vigência.** Cada norma carrega seu intervalo de validade (início, fim, o que alterou, o que a alterou). Sem isso, a consulta confunde a redação de hoje com a vigente na data do fato gerador.

**1.7 — Citação obrigatória.** Nenhuma afirmação entra sem citar dispositivo e fonte. Resposta sem citação = não-fundamentada.

## PARTE 2 — Arquitetura do repositório
**2.1 — Estrutura de pastas** (já criada neste repo):
```
CLAUDE.md            # este arquivo (Partes 1–4)
MANIFESTO.json       # fonte da verdade do estado de cada item (GERADO pela Action)
_entrada/            # ⬅️ ZONA DE DESPEJO: o MOU joga o bruto aqui (iptu/ e tdc/) — ver README
leis/                # texto normativo limpo (.md) + metadados (.json)
jurisprudencia/      # acórdãos/temas (.md + .json)
tabelas/             # tabelas extraídas (.csv) → input de engine
engines/iptu, engines/tdc   # fórmulas determinísticas (SEPARADAS das leis)
tese/iptu, tese/tdc  # GERADO pela Action, não editar à mão
extracao/            # saídas do prompt extrator, um arquivo por Gen
rag/chunks, rag/index
evals/ground-truth/  # docs de referência p/ validação
.github/workflows/   # consolidar.yml (a ligar)
```
**2.2 — Formato por artefato:** Markdown → texto normativo (entra no RAG); JSON → metadados/tags/vigência/remissões (filtro pré-busca); CSV → tabelas extraídas (input de engine).
**2.3 — Manifesto central** (`MANIFESTO.json`): `status_pipeline` de cada item (`bruto → fatiado → tagueado → validado → indexado`). GERADO pela Action; ninguém edita à mão.
**2.4 — Schema de metadados de cada lei** (`leis/<id>.json`): id, tipo_norma, esfera, jurisdicao, numero, ano, ementa, tema[], dispositivos_chave[], vigencia{inicio,fim,revogada_por,altera[],alterada_por[]}, remissoes[], jurisprudencia_relacionada[], tem_tabela, tabelas_extraidas[], tem_formula, formulas_referenciadas[], fonte{origem,path,hash,ocr}, status_pipeline, confianca_extracao, revisado_por_humano. *(schema completo no doc de fundação Parte 2.4.)*
**2.5 — Chunking estrutural:** unidade atômica = o dispositivo (Título→Capítulo→Seção→Artigo→Parágrafo→Inciso→Alínea). Nunca cortar por tamanho fixo. Cada chunk carrega o caminho hierárquico e o id da lei.
**2.6 — Retrieval híbrido (obrigatório no jurídico):** filtro por metadado (tema/jurisdição/vigência) → keyword (nº de lei/art./Tema) → semântico (pergunta NL). Sempre com filtro temporal.

## PARTE 3 — O pipeline (funil de 5 etapas)
| # | Etapa | Quem faz | Gate |
|---|---|---|---|
| 1 | Ingestão | determinístico (Drive/Supabase connector) | hash confere |
| 2 | Triagem | determinístico (regras/regex) — separa IPTU/TDC, esfera, ano, dedup | classificado |
| 3 | Extração pura | modelo barato (Haiku) via Batch API | JSON valida contra schema |
| 4 | Análise/tese | modelo forte (Opus), só na fração final | toda afirmação citada |
| 5 | Consulta | RAG híbrido | resposta carrega citação |

**Economia:** cascata de modelo (~85% no barato) + Batch API (−50%) + prompt caching (−90% no input repetido).
**Consolidação:** Action `consolidar.yml` a cada push regenera MANIFESTO + índice RAG + mestres de tese (determinístico).
**Validação:** `evals/ground-truth/` — roda campo-a-campo a cada mudança de schema/prompt (gate = citação correta).

## PARTE 4 — Mapa dos Gens (papéis e handoffs)
| Gen | Papel | Recebe de | Entrega para |
|---|---|---|---|
| **Gen Técnico-RAG** | ingestão, triagem, chunking, indexação (1–2 e 5) | Drive/manifesto | Gen RAG, Gen Estudo |
| **Gen RAG** | consulta com citação (5) | corpus indexado | Advogado, Estudo, você |
| **Gen Estudo** | síntese temática, lacunas | Gen RAG | Gen Advogado |
| **Gen Matemática** | engines/fórmulas, validação de cálculo | tabelas extraídas | Advogado, tese |
| **Gen Advogado** | tese/antítese/vacina, parecer (4) | RAG+Estudo+Matemática | mestre de tese |
| **Orquestrador** | roteia, aplica gate humano | todos | você |

Regra de ouro: **Gen Matemática é a única fonte de número**; **Gen Advogado nunca inventa valor**; **Gen RAG nunca responde sem citação**.

---
> **Fonte completa (Partes 5 e 6 — prompt extrator universal + ordem de instanciação):** `PROJETO-RAG-JURIDICO-IPTU-TDC.md` (raiz) e `extracao/PROMPT-EXTRATOR-UNIVERSAL.md`.
> **Decisão do MOU (2026-06-20):** base inicial = **TDC** (o pipeline começa por TDC; IPTU vem depois). _(antes: pendente IPTU×TDC.)_

---

## Escritório do MOU (PMO)
> Seção adicionada pelo Escritório do MOU — 2026-06-18. Não altera a constituição acima (D38).

Este repo é a unidade **Potencial Urbano** (RAG Jurídico IPTU/TDC) do portfólio do MOU. O **Escritório do MOU** (repo `escritorio-do-mou`) é o PMO que coordena o portfólio; esta unidade é um dos projetos dele.
- Se você montou SÓ este repo, você é o **orquestrador do Potencial Urbano** — trabalha aqui sob a governança/gate do próprio projeto (D21).
- Se montou TAMBÉM o `escritorio-do-mou`, o chapéu é o do ESCRITÓRIO (a constituição dele manda); este repo é DADO a ler/servir.
- As **diretrizes do escritório** para este projeto vivem em `DO_ESCRITORIO.md` (raiz) — canal D44; diretriz é proposta fundamentada, não ordem cega.
- **Retomada (estado vivo):** leia **`PROXIMA-INSTANCIA.md`** (topo ★★★) + **`BACKLOG.md`** ANTES de executar. O hook de boot os surfaça, mas **em sessão remota hooks NÃO disparam** (A-291/D132) — este ponteiro é a rede. _(Acrescentado pelo Escritório — triplo-limpo L2, 2026-07-05.)_
- **Doutrina herdada (obrigatória):** zero-compressão · dialético · agnosticismo · nada se joga fora. SSOT da doutrina = `escritorio-do-mou/CLAUDE.md`. Em divergência, vale o escritório.
- **Escopo é do dono (D21/D157/A-296):** a instância propõe, o dono decide. O que ele pediu **nunca** é "extra"; **nunca** se oferece "parar" um item solicitado. Bloqueio = fato + caminho (recomendação fechada); o dono decide o **COMO**, não o **SE**.
- **🔑 IDIOMA — SEMPRE PORTUGUÊS DO BRASIL, EM TUDO (D164, MOU 2026-07-08: "em portugues sempre... nao sei ingles" + "para todos projetos sempre").** O MOU NÃO lê inglês. TODA superfície que ele lê vai em português: chat, selos, entregáveis, título/corpo de PR, commits voltados a ele, perguntas. Nome próprio em inglês sempre glosado. Responder ao MOU em inglês = violação de regra de ouro.
- **🔑 CAIXA DO ESCRITÓRIO (F4/D-CAIXA-FIX):** ANTES de declarar "nada pendente", confira **`caixa-de-entrada/do-escritorio/`** (fora de `processados/`) — em sessão remota o hook de boot NÃO dispara (A-291/D132), este ponteiro é a rede. Diretriz do escritório só "existe" depois de MESCLADA na `main`.

### Políticas transversais do portfólio (aplicam-se a esta unidade)
> Descidas do escritório em 2026-06-27 (canal D44; SSOT no `escritorio-do-mou`). Aplicadas sob o gate do projeto (D21).
- **D120 — área de trabalho × repo de produto:** a área de trabalho do PMO é o repo `escritorio-do-mou`; os repos de **produto/unidade** (como ESTE) são consulta + execução do próprio projeto. O escritório toca este repo via git, atribuído e sob o gate (D21), **nunca como comando** (D2). Esta instância **NÃO escreve** no `escritorio-do-mou`.
- **D119 — "TODOS LEEM, só a KEEPEE TOCA" o DEV:** o repositório de DESENVOLVIMENTO do Profinders (org `keepee-facilities`) tem **leitura liberada** a qualquer unidade (inventário/as-built) mas **escrita EXCLUSIVA da unidade Keepee**. O Potencial Urbano **NUNCA escreve** no DEV. _(D119 revisa o antigo D29 "intocável por todos".)_
> **Alcance real da trava (auditoria C-02, 2026-07-05):** a trava em `.claude/settings.json` bloqueia **Edit/Write/MultiEdit** nesses paths — NÃO cobre `Bash` (um redirecionamento/`git push` via Bash não é interceptado pelo matcher de path). A garantia contra escrita nesses repos é, portanto, **doutrinária** (esta instância não emite comando de escrita neles) somada ao **gate humano** (D21), reforçada pela trava de ferramenta. "NÃO/NUNCA escreve" = doutrina + trava de Edit/Write, não trava absoluta de rede.
