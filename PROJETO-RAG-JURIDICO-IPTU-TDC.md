# PROJETO RAG JURÍDICO — IPTU / TDC
### Potencial Urbano · Documento de Instanciação · v1.0

> **O que é este documento.** É a fundação do projeto que você vai instanciar no Claude Code. Ele tem duas funções:
> 1. **Partes 1 a 4** → cole no repositório como `CLAUDE.md` (a constituição do projeto). É o que orienta toda instância do Code que tocar nesse repo.
> 2. **Parte 5** → é o **prompt extrator universal**. Cole em cada Gen espalhado pelas suas IAs (Claude, ChatGPT, Gemini, Manus...). Cada Gen devolve um arquivo estruturado que você consolida no projeto.
> 3. **Parte 6** → a ordem concreta de instanciação.

---

## PARTE 1 — Princípios invioláveis

Estes são os invariantes. Tudo no projeto se subordina a eles. Se uma decisão futura conflitar com um destes pontos, o princípio ganha.

**1.1 — Quatro artefatos separados, nunca um só.**
O material se divide em quatro coisas com naturezas e velocidades de mudança diferentes. Misturá-las quebra a auditabilidade.

| Artefato | O que é | Velocidade de mudança | Vira |
|---|---|---|---|
| **Lei / Norma** | Texto normativo (constituição, leis, decretos, súmulas, acórdãos) | Lenta | RAG |
| **Tabela / Valor** | Dados numéricos extraídos das leis (alíquotas, índices, faixas) | Lenta, mas é *dado*, não norma | Input de engine |
| **Fórmula / Engine** | Cálculo determinístico (alíquota progressiva de IPTU, valuation de TDC) | Média | Engine determinístico |
| **Tese / Antítese / Vacina** | Camada argumentativa, construída a partir das leis | Alta (evolui com estratégia e cada decisão nova) | Documento(s) de tese |

A regra que veio do seu alerta — *separar fórmula de lei* — é exatamente isto, levado até o fim. Tabela de lei é dado e sai do texto. Fórmula é engine e nunca mora dentro do corpus de leis.

**1.2 — Extrair puro → enriquecer → argumentar. Nunca na mesma passada.**
Três etapas distintas, jamais fundidas:
- **Extração pura:** só o que está literalmente no documento. Sem interpretar, sem calcular, sem opinar.
- **Enriquecimento:** cruzamento, lookups, ligação com jurisprudência. Etapa separada.
- **Tese:** síntese argumentativa, construída *depois*, a partir do corpus já limpo.
Fundir extração com tese contamina a rastreabilidade e faz a tese ficar refém da ordem em que os PDFs foram subindo.

**1.3 — Número nasce no engine, nunca no LLM.**
Auditabilidade é o eixo do projeto (é jurídico-fiscal: número errado é passivo). O LLM **roteia e redige prosa**. Todo fato e todo valor vêm de fonte determinística (engine ou tabela extraída e validada). Todo número tem que ser rastreável até o dispositivo legal de origem.

**1.4 — Funil de custo: o LLM toca o mínimo possível.**
Com volume gigantesco, a meta é o modelo caro tocar só a fração que importa. O determinístico descarta o grosso de graça; o modelo barato faz extração em lote; o modelo forte só entra no raciocínio jurídico fino. (Cascata + batch + caching, detalhado na Parte 3.)

**1.5 — Criação paralela, consolidação serial.**
Várias instâncias do Code podem rodar em paralelo, mas **cada uma só cria arquivos novos** (um por lei). Nenhuma instância edita um documento mestre compartilhado. A consolidação (montar índice e gerar os mestres) é um passo serial e determinístico — uma GitHub Action que *regenera* os mestres a cada push. Assim o Git nunca dá conflito e o mestre nunca tem merge manual.

**1.6 — Toda norma tem vigência.**
Lei muda no tempo. Cada norma carrega seu intervalo de validade (início, fim, o que alterou, o que a alterou). Sem isso, a consulta confunde a redação de hoje com a que valia na data do fato gerador — erro fatal em matéria tributária.

**1.7 — Citação obrigatória.**
Nenhuma afirmação entra na tese ou na resposta sem citar o dispositivo e a fonte (lei, artigo, parágrafo / acórdão, página). Resposta sem citação é tratada como não-fundamentada.

---

## PARTE 2 — Arquitetura do repositório

**2.1 — Estrutura de pastas**

```
projeto-rag-juridico/
├── CLAUDE.md                      # Partes 1–4 deste documento
├── MANIFESTO.json                 # fonte da verdade do estado de cada item
├── leis/
│   ├── lei-15889-2013.md          # texto normativo limpo, fatiado por hierarquia
│   └── lei-15889-2013.json        # metadados / tags (schema em 2.4)
├── jurisprudencia/
│   ├── stf-tema-1130.md
│   └── stf-tema-1130.json
├── tabelas/
│   └── lei-15889-2013-aliquotas.csv   # tabelas extraídas → input de engine
├── engines/                       # fórmulas determinísticas (SEPARADAS das leis)
│   ├── iptu/
│   └── tdc/
├── tese/                          # GERADO pela Action, não editado à mão
│   ├── iptu/tese-antitese-vacina.md
│   └── tdc/tese-antitese-vacina.md
├── extracao/                      # saídas do prompt extrator, um arquivo por Gen
│   ├── gen-rag.md
│   ├── gen-advogado.md
│   └── ...
├── rag/
│   ├── chunks/                    # corpus chunked pronto p/ indexar
│   └── index/
├── evals/
│   └── ground-truth/              # docs de referência p/ validação
└── .github/workflows/
    └── consolidar.yml             # regenera MANIFESTO, mestres e índices a cada push
```

**2.2 — Formato por artefato** (não é "JSON ou outro" — é cada um no seu papel)
- **Markdown (.md)** → texto normativo. Legível, versionável, é o que entra no RAG.
- **JSON (.json)** → metadados, tags, vigência, remissões. Estruturado e queryável: é o que a máquina filtra antes da busca semântica.
- **CSV (.csv)** → tabelas extraídas. Saem do texto e viram input de engine. Uma informação por coluna, tipos estáveis (data como data, número como número).

**2.3 — Manifesto central (`MANIFESTO.json`)**
A fonte da verdade do estado de cada item — mesmo papel dos seus 5 status fixos no SBA. Cada item tem um `status_pipeline`: `bruto → fatiado → tagueado → validado → indexado`. O manifesto é **gerado** pela Action a partir dos `.json` individuais; ninguém edita à mão.

**2.4 — Schema de metadados de cada lei** (`leis/<id>.json`)

```json
{
  "id": "lei-municipal-saopaulo-15889-2013",
  "tipo_norma": "lei_ordinaria",
  "esfera": "municipal",
  "jurisdicao": "São Paulo/SP",
  "numero": "15.889",
  "ano": 2013,
  "ementa": "Dispõe sobre ...",
  "tema": ["IPTU"],
  "dispositivos_chave": ["art. 7º", "art. 12, §2º"],
  "vigencia": {
    "inicio": "2013-11-05",
    "fim": null,
    "revogada_por": null,
    "altera": [],
    "alterada_por": []
  },
  "remissoes": ["lei-complementar-xxx", "ec-yyy"],
  "jurisprudencia_relacionada": ["stf-tema-1130"],
  "tem_tabela": true,
  "tabelas_extraidas": ["tabelas/lei-15889-2013-aliquotas.csv"],
  "tem_formula": true,
  "formulas_referenciadas": ["engines/iptu/aliquota_progressiva"],
  "fonte": {
    "origem": "drive",
    "path": "Compartilhado/sergio.finger/...",
    "hash": "sha256:...",
    "ocr": false
  },
  "status_pipeline": "tagueado",
  "confianca_extracao": "alta",
  "revisado_por_humano": false
}
```

**2.5 — Chunking estrutural (hierarquia normativa brasileira)**
Não cortar por tamanho fixo. A unidade atômica é o dispositivo: **Título → Capítulo → Seção → Artigo → Parágrafo → Inciso → Alínea**. A própria estrutura da lei já dá os limites de corte certos. Cortar no meio de um artigo destrói a coerência e contamina a recuperação. Quando um dispositivo for grande demais, sub-dividir respeitando a hierarquia, sem nunca quebrar a unidade lógica. Cada chunk carrega no metadado o caminho hierárquico completo e o `id` da lei (para citação e para reconstruir o contexto).

**2.6 — Retrieval híbrido (não é opcional no jurídico)**
Busca puramente semântica erra em jurídico porque números de lei, artigos e nomes de caso são *identificadores* — beneficiam-se de busca por palavra-chave exata, não de similaridade vetorial (que "borra" leis parecidas mas juridicamente distintas). A arquitetura combina:
- **Filtro por metadado** primeiro (tema, jurisdição, vigência na data do fato) — corta o universo.
- **Keyword** para identificadores (nº da lei, art., Tema/REsp).
- **Semântico** para a pergunta em linguagem natural.
Sempre com **filtro temporal**: a consulta tem que respeitar qual redação estava vigente na data relevante.

---

## PARTE 3 — O pipeline (o funil, em 5 etapas)

| # | Etapa | Quem faz | Onde roda | Gate de qualidade |
|---|---|---|---|---|
| 1 | **Ingestão** | determinístico | Code + Drive connector | hash confere; sem corrupção |
| 2 | **Triagem** | determinístico (regras/regex) | Code / script | classificado e deduplicado |
| 3 | **Extração pura** | modelo barato (Haiku) | Batch API, em lote | JSON valida contra schema |
| 4 | **Análise / tese** | modelo forte (Opus) | Code, só na fração final | toda afirmação citada |
| 5 | **Consulta** | RAG híbrido | rag/ + Action | resposta carrega citação |

**Regras de operação do funil**
- **Etapa 1 — Ingestão.** Puxa do Drive respeitando o que você já mapeou: `sharedWithMe=true` para o material compartilhado (ex.: pastas do sergio.finger), `title contains` (que funciona) em vez de `fullText`/`mimeType` (que falham). OCR só onde necessário. Grava hash de cada arquivo no manifesto.
- **Etapa 2 — Triagem (zero LLM).** Aqui você elimina o grosso de graça: separa IPTU de TDC, identifica esfera/jurisdição/ano, deduplica. É o que torna o volume gigantesco viável. Tudo que dá pra decidir por regra, decide por regra.
- **Etapa 3 — Extração pura em lote.** O que sobrou vai pro Haiku via **Batch API** (50% mais barato, até 10.000 requisições por lote, resultado em até 24h). Cada requisição leva `custom_id = id do documento`, para reconciliar direto no manifesto. Saída só com o que está no documento, em JSON validado contra o schema. As tabelas detectadas são extraídas para `.csv` e marcadas — não ficam no texto.
- **Etapa 4 — Análise/tese (cascata).** Só os casos que passaram o funil e exigem interpretação sobem pro Opus: cruzamento com jurisprudência (STF Tema 1130, STJ), construção de tese/antítese/vacina. O modelo redige; **os números vêm do engine**. Toda afirmação cita o dispositivo de origem.
- **Etapa 5 — Consulta.** RAG híbrido (2.6) sobre o corpus indexado. Caps apertados no retrieval (2–3 chunks bem escolhidos, não 8 documentos longos) para cortar tokens sem perder precisão.

**Economia (a matemática que torna o projeto viável)**
Empilhar três alavancas: cascata de modelo (manda ~85% do volume pro barato, mantendo ~95% da qualidade) + Batch API (–50%) + prompt caching (–90% no input repetido, que aqui é o schema e as instruções jurídicas estáveis). Combinadas, derrubam o gasto efetivo a uma fração do custo de rodar o modelo forte em tudo.

**Consolidação (a Action `consolidar.yml`)**
Dispara a cada push. Regenera, de forma determinística: o `MANIFESTO.json`, o índice do RAG, e os documentos mestres de tese (que são *saída* da estrutura de dados, nunca arquivos editados à mão). Mudou uma lei? A Action re-deriva só a parte afetada. É a sua preferência por Actions sobre hooks, aplicada como motor de consolidação.

**Validação (auditabilidade contínua)**
Em `evals/ground-truth/` ficam documentos de referência com a extração verificada. Sempre que mudar schema ou prompt, roda-se a validação campo a campo contra esse gabarito — pega regressão silenciosa antes de ir pro corpus. No jurídico, o gate que importa é **citação correta**: um chunk corrompido que vira citação alucinada meses depois é o pior caso, e o eval existe pra impedir isso.

---

## PARTE 4 — Mapa dos Gens (papéis e handoffs)

Cada Gen tem um papel no funil. Os handoffs são explícitos: A propõe, você aprova, B executa (seu ADR-004). Os papéis abaixo são o alvo — o prompt extrator (Parte 5) vai revelar o estado real de cada um.

| Gen | Papel no pipeline | Recebe de | Entrega para |
|---|---|---|---|
| **Gen Técnico-RAG** | Ingestão, triagem, chunking, indexação (etapas 1–2 e 5) | Drive / manifesto | Gen RAG e Gen Estudo |
| **Gen RAG** | Consulta sobre o corpus, recuperação com citação (etapa 5) | corpus indexado | Gen Advogado, Gen Estudo, você |
| **Gen Estudo** | Síntese temática, levantamento de lacunas, mapeamento | Gen RAG | Gen Advogado |
| **Gen Matemática** | Engines/fórmulas determinísticas, validação de cálculo (artefato Fórmula) | tabelas extraídas | Gen Advogado, tese |
| **Gen Advogado** | Tese/antítese/vacina, parecer, cruzamento jurisprudencial (etapa 4) | RAG + Estudo + Matemática | documento mestre de tese |
| **Orquestrador** (se houver) | Roteia tarefas, aplica gates humanos | todos | você |

Regra de ouro que atravessa todos: **Gen Matemática é a única fonte de número**; **Gen Advogado nunca inventa valor** (pede ao Gen Matemática); **Gen RAG nunca responde sem citação**.

---

## PARTE 5 — PROMPT EXTRATOR UNIVERSAL

> **Como usar.** Abra cada Gen (em qualquer IA: Claude, ChatGPT, Gemini, Manus...). Cole o bloco abaixo inteiro. O Gen vai devolver um arquivo estruturado. Salve a saída em `extracao/gen-<id>.md` no repositório. Rode em **todos** os Gens antes de consolidar. O documento é desenhado para ser auto-contido: quem consolidar depois não precisa ter acesso ao histórico daquele Gen.

```
Você é um Gen (instância especializada) que faz parte de um ecossistema de IAs
trabalhando num projeto jurídico-fiscal de RAG sobre IPTU e TDC (Potencial Urbano).

Estou consolidando o conhecimento de todos os Gens num projeto único, versionado
em Git e operado no Claude Code. Preciso que você faça um RELATÓRIO DE EXTRAÇÃO
completo de tudo o que você sabe, faz e mantém, para que eu possa migrar e
reorganizar esse conhecimento sem perder nada e sem depender do seu histórico.

REGRAS DE COMPORTAMENTO (siga à risca):
- NÃO invente. Reporte só o que você realmente sabe, faz ou guarda.
- Marque claramente o que é FATO (você tem certeza) vs SUPOSIÇÃO (você infere).
- Seja AUTO-CONTIDO: explique cada termo, sigla ou nome de arquivo que citar.
  Quem ler isto não terá acesso ao nosso histórico de conversas.
- Quebre o conhecimento em itens INDEPENDENTES E VERIFICÁVEIS (um fato por linha).
- Se você mantém um "Codex" (documento canônico de processo/regras), COLE o teor.
  Se for muito longo, cole as partes que descrevem dados, processos e regras, e
  liste os títulos das seções omitidas.
- Onde não souber, escreva "NÃO SEI" — é uma resposta válida e útil.

Devolva EXATAMENTE neste formato (Markdown com cabeçalho YAML):

---
gen_id: <um-slug-curto-ex-gen-advogado>
papel: <rag | estudo | matematica | advogado | tecnico-rag | orquestrador | outro>
ia_hospedeira: <Claude | ChatGPT | Gemini | Manus | outro>
versao_codex: <ex: V5.5 | nenhuma>
data_extracao: <AAAA-MM-DD>
confianca_global: <alta | media | baixa>
---

# 1. IDENTIDADE E ESCOPO
Em 3–5 linhas: qual é a sua função, qual o limite do que você cobre e o que
explicitamente NÃO é sua responsabilidade.

# 2. DADOS QUE EU GOVERNO (inventário)
Tabela com TODOS os dados/insumos importantes sob a sua ótica:

| Nome do dado | Onde encontrar (fonte/path/link) | Tipo | Criticidade | Formato atual | Fato/Suposição |
|---|---|---|---|---|---|

- Tipo: LEI (norma) | TABELA (valor/dado) | FORMULA (cálculo) | TESE (argumento) | META (config/processo)
- Criticidade: alta | media | baixa
- "Onde encontrar" deve ser específico: pasta do Drive, nome de planilha, repo, etc.

# 3. PROCESSO ATUAL (AS-IS)
Passo a passo de como você opera HOJE. Para cada passo: o que entra, o que você
faz, o que sai. Inclua o que é manual e o que é automático.

# 4. PROCESSO IDEAL (TO-BE)
Como você acha que esse processo DEVERIA funcionar. Onde estão os atritos hoje.

# 5. LACUNAS E SUGESTÕES DE MELHORIA
O que falta, o que está frágil, o que você melhoraria. Priorize (alta/média/baixa).

# 6. ARTEFATOS E DOCUMENTAÇÃO QUE MANTENHO
Liste todo documento, planilha, prompt ou código que você produz ou guarda.
Se você tem um CODEX, cole o teor aqui (regras de dados/processo/tratamento).

# 7. REGRAS DE TRATAMENTO (como cada coisa deve ser tratada)
Suas regras para: limpeza, o que descartar, como separar LEI de FORMULA de TABELA
de TESE, deduplicação, fatiamento, citação, vigência temporal. Seja específico.

# 8. INTERFACES E DEPENDÊNCIAS (handoffs)
De quais outros Gens/fontes você DEPENDE (o que recebe e de quem).
Para quem você ENTREGA (o que produz e para quem).

# 9. MINHA VISÃO DO PROJETO
Como você acha que o projeto inteiro deveria ser estruturado. Como VOCÊ faria,
se fosse seu. O que priorizaria primeiro. Discorde de mim se achar que devo
fazer diferente — quero a sua leitura, não concordância.

# 10. RISCOS E ALERTAS
O que pode dar errado, o que já deu errado, armadilhas que você conhece.

# 11. LACUNAS DE CONFIANÇA
Liste o que neste relatório é SUPOSIÇÃO e precisa de revisão humana, e o que
você marcou como "NÃO SEI".
```

---

## PARTE 6 — Ordem de instanciação

1. **Crie o repositório** (ex.: `bitsuki1/projeto-rag-juridico`) e cole as Partes 1–4 deste documento como `CLAUDE.md`. Crie a estrutura de pastas vazia da seção 2.1.
2. **Rode o prompt extrator (Parte 5) em todos os Gens.** Salve cada saída em `extracao/gen-<id>.md`. Esse passo é a fotografia do estado real — sem ele, a consolidação é chute.
3. **Consolide o que veio.** Com as extrações na mão, abra uma instância do Code só para ler `extracao/` e produzir: (a) o mapa real de Gens vs Parte 4, (b) a lista de Codex existentes a unificar, (c) as divergências entre o AS-IS reportado e o TO-BE deste documento.
4. **Defina as regras de triagem (etapa 2)** — é o gargalo de partida. Quanto mais o determinístico resolver aqui, menos o LLM custa depois. Comece pela base de maior volume (IPTU ou TDC).
5. **Suba o primeiro lote de leis** pela estratégia de criação paralela (1.5): cada instância cria `leis/<id>.md` + `.json`, nunca toca em mestre.
6. **Ligue a Action `consolidar.yml`** para regenerar manifesto, índice e mestres a cada push.
7. **Monte o ground-truth** com 10–20 leis já validadas à mão, para travar a qualidade antes de escalar o volume.

> **Decisão do MOU (2026-06-20):** base inicial = **TDC** (o pipeline começa por TDC; IPTU replica depois).
