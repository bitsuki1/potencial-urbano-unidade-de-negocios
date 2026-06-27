# CODEX DO PROJETO — Potencial Urbano (IPTU / TDC)
## Constituição e Regras de Ouro · v0.5

> **Natureza deste documento.** É a constituição viva do projeto: as regras
> invioláveis e o *porquê* de cada uma. É a fonte da verdade para toda
> instância/agente que tocar o projeto.
>
> **Este documento NÃO é para leitura humana corrida.** O operador trabalha na
> tela, falando com a instância, e não lê documentação (ver RO-11). Os agentes
> mantêm e consultam este Codex; tudo que exigir decisão humana é levado à
> conversa — nunca deixado num arquivo à espera de leitura.

> **Dois Codex, não confundir:**
> - **CODEX DO PROJETO** (este) = governança, estratégia, regras de ouro.
> - **CODEX MESTRE** (a forjar na Etapa 1) = matriz de domínio IPTU/TDC,
>   consolidada de todas as versões e escrutinada em Tese/Antítese/Vacina.
>   Nenhuma matriz atual (TDC v89/v90/v91, IPTU, etc.) é canônica — todas são
>   **insumo** para forjar a nova.

---

## 1. REGRAS DE OURO (invioláveis)

**RO-01 — Inteligência fora do LLM.** A precisão mora no dado e no engine
determinístico, nunca no modelo. O LLM roteia e redige prosa; todo número e todo
fato vêm de fonte determinística e são rastreáveis até a origem.

**RO-02 — Agnosticismo radical.** Nenhum componente depende de um LLM ou
plataforma específicos. O modelo é peça plugável e descartável. Consequência
natural da RO-01.

**RO-03 — Quatro artefatos separados, sempre.** Lei (texto/RAG) · Tabela (dado) ·
Fórmula (engine) · Tese (argumento). Nunca misturados.

**RO-04 — Número nasce no engine.** Cálculo é determinístico e validado contra
casos reais. O LLM nunca calcula.

**RO-05 — Entrada por endereço. Nunca perder negócio por falta de SQL.** A porta
de entrada aceita endereço sozinho. Resolve-se o SQL por trás quando possível; se
não, o negócio segue com endereço + geo, e o SQL entra depois.

**RO-06 — SQL_MESTRE é regra, não entregável nem pedágio.** É a espinha interna
de cruzamento. Padrão em §3.

**RO-07 — Endereço no padrão Correios/DNE.** Padrão em §3. Endereço é chave
secundária (serve para achar o SQL); o SQL é a chave verdadeira do cruzamento.

**RO-08 — Só fonte OFICIAL vira lei.** Nada não-oficial é usado como norma.

**RO-09 — Nada se descarta.** Fonte não-oficial mas com texto importante não é
jogada fora: ela **dispara um alerta para buscar a fonte oficial**, e esse
alerta é trazido ao operador (RO-11). O não-oficial serve de pista, não de base.

**RO-10 — Não-oficial só é aceito tacitamente na MATRIZ COMERCIAL** — e mesmo
assim só nos itens em que a LGPD impede obter o dado oficial. A preferência é
**sempre** oficial. Cada item carrega um **selo de % de oficialidade** (a tag de
confiança).

**RO-11 — O operador não lê documentação.** Trabalha na tela, falando com a
instância. **Nunca espere que ele leia nada.** Tudo que exige atenção dele é
trazido na conversa. Arquivo ilegível **não é só marcado — é trazido
efetivamente** ao operador para resolução. Quando for um **bloco grande de
ilegíveis**, traz-se na conversa a **quantidade** e a **estratégia proposta**
(ex.: rodar conversão de formato / OCR), em bloco. **Nunca se dispensa e nunca se
deixa parado em documentação sem o operador saber.**

**RO-12 — Trazer tudo → identificar tudo → deduplicar com cuidado.** Não se
filtra na entrada (risco de perder). Traz-se tudo, mesmo repetido. **A pasta
identifica o arquivo, não o nome** (muitos nomes mentem; a localização
qualifica). Sobre dedup: o Drive **não expõe hash (md5)** via API, então
deduplica-se por **nome + tamanho**, confirmando suspeitos por leitura do
conteúdo. **Versão NÃO é duplicata** — versões são linhagem (RO-14) e são
preservadas e aproveitadas, nunca descartadas.

**RO-13 — Agentes entram DENTRO dos documentos.** Classificação é por conteúdo,
nunca por título. Se o formato impede a leitura (PDF só-imagem, mapa rasterizado,
corrompido, criptografado), reporta-se e traz-se ao operador — nunca se descarta
em silêncio. Nunca se perde nada por limitação da máquina.

**RO-14 — Vigência e linhagem.** Documentos vencem; partes são substituídas. O
**De/Para** é o livro-razão vivo: cada arquivo guarda vigência, linhagem
(substitui / é substituído por) e o que dele foi aproveitado. Toda tese registra
de qual documento veio (proveniência).

**RO-15 — Citação obrigatória.** Nenhuma afirmação entra em tese ou resposta sem
citar dispositivo e fonte. Resposta sem citação é não-fundamentada.

---

## 2. TAXONOMIA DE TAGS (facetada — cada arquivo recebe várias)

- **Tema:** IPTU · TDC · AMBOS · CORRELATO · GERAL
- **Artefato:** LEI · TABELA · FÓRMULA · TESE · MAPA/GEO · DADO-CADASTRAL ·
  META/PROCESSO · IDEAÇÃO (plantas do operador e relatórios de Gens)
- **Tipo de arquivo:** CSV · XLSX · PDF-texto · PDF-imagem · DOCX · MD · JSON ·
  SHP/GeoJSON · IMG · outro
- **Oficialidade:** OFICIAL · NÃO-OFICIAL · CRIADO-POR-NÓS · CRIADO-POR-TERCEIROS
- **Esfera:** Municipal-SP · Estadual · Federal
- **Vigência:** VIGENTE · REVOGADO/SUBSTITUÍDO · DATADO(ano) — com início/fim
- **Leitura:** LIDO-OK · PARCIAL · ILEGÍVEL(motivo)
- **Uso no Codex:** USADO(→ qual tese) · NÃO-USADO
- **Confiança / selo de oficialidade:** alta · média · baixa (% de oficialidade
  na matriz comercial)
- **Hash:** fingerprint (dedup)

---

## 3. PADRÕES CANÔNICOS

**SQL_MESTRE** — chave de cruzamento.
- 10 dígitos, só número, com zero à esquerda (`SSSQQQLLLL`).
- Guardado também decomposto: `setor`(3) · `quadra`(3) · `lote`(4).
- `SQL_DV` (dígito verificador) em campo à parte, validado, **nunca usado como
  chave**.
- Exibição humana (`SSS.QQQ.LLLL-D`) é derivada, não armazenada.
- **Qualquer formato de entrada é convertido para o SQL_MESTRE antes de cruzar.**

**ENDERECO_MESTRE** — chave secundária.
- Estrutura Correios/DNE: tipo+logradouro · número · complemento · bairro ·
  município · UF · CEP(8 dígitos numérico) + versão normalizada concatenada.
- Usado para geocodificar e resolver o SQL quando ele falta.

---

## 4. FASES

**Fase 0 — Trazer tudo (completude primeiro).**
Varredura do Drive inteiro pelo critério de pasta; reconciliação contra o que
instâncias anteriores mapearam (o que não veio, tem que vir); produção do
**De/Para localizador** (manifesto-mestre, uma linha por arquivo). Consolidação
física na estrutura do projeto e dedup por hash. Ilegíveis trazidos ao operador.

**Etapa 1 — Fundação Canônica** *(validada)*.
1. Cravar as regras transversais (§1, §3).
2. Identificar e taguear tudo (§2), agentes entrando nos documentos (RO-13).
3. Separar nos quatro artefatos (RO-03).
4. Forjar o **Codex Mestre**: consolidar as versões das matrizes (insumo) →
   escrutinar **documento por documento**, em Tese/Antítese/Vacina,
   exaustivamente → registrar proveniência e linhagem (RO-14).

**Fase 2 — Identificação de imóveis.**
Base = planilha de IPTU 2026 da cidade de SP (~1 milhão de linhas).
**Enriquecimento parte a parte, nunca de uma vez.** Cruzamento em camadas: SQL ↔
endereço ↔ matrícula ↔ IPTU ↔ ITBI ↔ CPF/CNPJ ↔ nome do proprietário, **com o
ano em que cada informação aparece** (proveniência temporal por campo; em
conflito, a mais recente vence, guardando histórico). Antes de cruzar:
inventariar o que cada arquivo entrega e pesquisar como obter — ou se conseguimos
— outras fontes.

**Fase 3 — Validação por casos reais.**
Baixar o máximo de casos reais de IPTU e TDC para formar o ground-truth e testar
o engine campo a campo. Fórmula que não bate com caso real não passa.

---

## 5. DECISÕES DE ARQUITETURA (Tese / Antítese / Vacina)

**D-01 — A inteligência mora no banco/engine, não no LLM.**
- *Tese:* dado exato em banco relacional/espacial + engine determinístico; LLM só
  traduz. Precisão e auditabilidade máximas; custo do modelo caro cai.
- *Antítese:* "é mais simples colocar tudo no prompt do LLM."
- *Vacina:* LLM erra matemática e tabela longa; número errado é passivo
  jurídico-fiscal. A precisão tributária mora no dado. (Convergência independente
  de múltiplos Gens.)

**D-02 — Porta de entrada por endereço.**
- *Tese:* aceitar endereço sozinho; resolver SQL por trás.
- *Antítese:* "sem SQL o cruzamento é fraco."
- *Vacina:* exigir SQL na entrada faz perder negócio (RO-05). SQL é espinha
  interna, não barreira de entrada.

**D-03 — Oficialidade como lei; não-oficial como alerta.**
- *Tese:* só oficial vira norma; não-oficial importante dispara busca da fonte
  oficial; nada se descarta.
- *Antítese:* "o texto não-oficial já basta."
- *Vacina:* usar não-oficial como lei contamina a base. Exceção tácita única:
  matriz comercial, só onde a LGPD impede o oficial, com selo de % de
  oficialidade. (RO-08, RO-09, RO-10.)

**D-04 — Nenhuma matriz atual é canônica.**
- *Tese:* todas as versões são insumo; forja-se uma nova por consolidação +
  escrutínio documento a documento.
- *Antítese:* "adotar a versão mais recente (v91) e seguir."
- *Vacina:* as versões foram se sintetizando e perdendo rastro; consolidar com
  Tese/Antítese/Vacina recupera a linhagem e blinda o resultado.

**D-05 — A esteira RAG é DETERMINÍSTICA (sem LLM/embeddings no tier base). (2026-06-20)**
- *Tese:* chunking estrutural por dispositivo (2.5) → índice invertido BM25 + metadados (2.6) →
  consulta com gate de cobertura — tudo stdlib, sem rede. `scripts/fatiar|indexar|consultar`.
- *Antítese:* "use embeddings/LLM logo de cara — keyword é fraco."
- *Vacina:* o número e a citação nascem de fonte determinística (1.3/1.7); a camada semântica é
  extensão FUTURA plugável no mesmo índice. **Limite DECLARADO do tier keyword:** match lexical ≠
  relevância semântica — "direito de construir" casa a Lei 4.591/1964 Art. 68 ("construir
  habitações") com 100% de cobertura sem ser TDC. Não inflar o que o tier não faz.

**D-06 — GUARDA DE VERBATIM: só texto integral verbatim entra no RAG. (2026-06-20)**
- *Tese:* `fatiar.py` só fatia `.md` com `## Texto integral (verbatim)` + `.json confianca:alta`.
- *Antítese:* "indexa o resumo também — é melhor que nada."
- *Vacina:* citar uma síntese = resposta não-fundamentada (1.7); resumo no RAG mente sobre a fonte.
  Por isso as 14 municipais não-verbatim ficam de fora até serem re-ingeridas.

**D-07 — Re-ingestão verbatim é INTERNA quando o cru já está local. (2026-06-20)**
- *Tese:* o articulado integral das 12 federais já estava em `_entrada/misto/*.txt`;
  `scripts/promover_entrada.py` promove para `leis/federal/*.md` verbatim sem Drive nem egress.
- *Antítese:* "precisa capturar do planalto (que dá HTTP 403)."
- *Vacina (a grande, AUD-01):* um `.md` dizer "não baixado/403" **≠** o verbatim não existir no repo.
  Conferir `_entrada/` por id ANTES de declarar uma lei não-citável. A "CRÍTICA-1" da auditoria
  anterior ("NENHUMA das 27 é verbatim") era FALSO-NEGATIVO: confundiu "o .md é resumo" com "o
  verbatim não existe". Corpus saltou de 1 → 13 leis indexadas ao corrigir isso.

**D-08 — Número nasce no engine como CÓDIGO, não como prosa. (2026-06-20)**
- *Tese:* `engines/tdc/oodc.py` implementa as fórmulas OODC/TDC determinísticas (DECIMAL(10,3),
  constantes de `travas_operacionais_v6.1.json`, cada resultado com memória de cálculo + citação).
- *Antítese:* "as fórmulas em `FORMULAS-CONSOLIDADAS.md` já bastam."
- *Vacina:* fórmula em `.md` = número nascendo no LLM (proibido por 1.3/RO-04). `V` (Q14) e `CA_max`
  (Quadro 3) são TABELA — entradas obrigatórias, o engine NÃO os inventa. A grafia `(At/Ac)×V×Fs×Fp`
  **não tem fonte**; as 3 fontes-mestre usam `OO = (Aa/CA_max)×Fp×Fs×V` (CONF-2).

**D-09 — Mecanismo anti-perda ("ladrão" D83 do escritório) adotado no PU. (2026-06-20)**
- *Tese:* `BACKLOG.md` (item com DoD = prova mecânica) + hook de boot que o surfaça +
  `scripts/fechar-instancia.py` (GATE: "declarei feito" ≠ "provei feito").
- *Antítese:* "disciplina/handoff já bastam."
- *Vacina:* a disciplina arrebenta exatamente na saturação de contexto e na troca de instância
  (modo de falha nº1). Prevenção por MECANISMO sobrevive a esses dois momentos. O gate provou o
  valor na estreia: pegou uma não-idempotência do MANIFESTO (contava `.pyc` de cache).

**D-10 — O gate de fechamento NÃO pode passar verde com a suíte de evals esvaziada. (2026-06-20, 2ª auditoria)**
- *Tese:* `evals/rodar-evals.py` exige PISO de itens ATIVOS (`MIN_ITENS_ATIVOS=4`); 0 ativos → exit 1.
  O gate declara escopo honesto (5 invariantes mecânicas de conteúdo + 2 avisos de durabilidade; não
  cobre regressão/handoff/mérito).
- *Antítese:* "evals exit 0 = evals provaram algo; gate verde = tudo certo."
- *Vacina:* FALSO-VERDE (achado F-1/F-2). Rebaixar a flag `status:"aguardando_verbatim"` do único
  ground-truth ativo (ou deletá-lo) zerava `falhas_ativas` e o gate passava VERDE **com o RAG destruído**.
  "exit 0" ≠ "houve cobertura ativa". A própria ferramenta anti-perda tinha um furo que a 1ª auditoria
  (mesma lente da construção) não viu.

**D-11 — Robustez determinística: insumo BR no engine; dispositivo distinto no chunker. (2026-06-20)**
- *Tese:* `oodc.py._d` parseia decimal BR (vírgula=decimal, ponto=milhar); guardas Fp>0/Fs≥0 (OODC
  negativa é absurdo). `fatiar.py` captura o sufixo `-A/-B` e NÃO abre chunk para artigo CITADO entre
  aspas dentro de lei alteradora.
- *Antítese:* "`Decimal(str(x))` basta; `^Art\.\d+` é fiel."
- *Vacina:* as tabelas-fonte (Q14) são BR e **quebravam** o engine antes de ligar `tabelas/`; "Art. 156-A"
  rotulado "Art. 156" CITA dispositivo inexistente (viola 1.7). Número BR e sufixo de artigo NÃO são
  detalhe cosmético. (Resta a vigência-por-chunk em texto compilado — B-11(c).)

**D-12 — RO-24 reforçado: auditar com LENTE DIFERENTE da que construiu (D82 do escritório). (2026-06-20)**
- *Tese:* um deliverable só é "sólido" depois de auditado por uma lente DIFERENTE da que o produziu.
- *Antítese:* "rodei os testes/auto-teste, está pronto."
- *Vacina:* a construção não enxerga o próprio ponto cego. A 2ª auditoria (lentes diferentes) achou o
  falso-verde do gate (D-10) e o valor inventado (D-08 corrigido) que a 1ª passada não pegou. Re-rodar a
  MESMA lente = falsa convergência. Candidata a regra de portfólio (depositada ao escritório). Reflete em
  `BETA-CONTINUO.md §3`.

**D-13 — Padrões do escritório consolidados ao main; caixas v2 lado-projeto. (2026-06-27)**
- *Tese:* o pacote de padronização (Tipo D128=UNIDADE · D119/D120 · REGISTRO/ATA · handoff único · caixas v2 · gate de pickup) foi auditado ADDITIVE-seguro e consolidado ao main.
- *Antítese:* "é diretriz do escritório, aplico às cegas." *Vacina:* aplicado sob o gate do projeto (D21), só após verificar que é additive (12 arquivos, nada de corpus/engine tocado). PROPAGAR≠EMPACOTAR (DE-34): vale por estar no canônico, não por escrito na caixa.

**D-14 — O gate D141 AUTO-EMPURRA ao main (comportamento de risco, agora com guarda). (2026-06-27)**
- *Tese:* `gate-fechamento.sh [2/5]` e o hook de boot consolidam sozinhos a branch ao `origin/main` (main não-protegido neste repo) — economiza a dança manual, mas empurra sem revisão humana.
- *Antítese:* "rodar um gate é inócuo." *Vacina:* rodar o gate MOVE o main. A guarda **NV-2** (2026-06-27) ABORTA a auto-consolidação se o MANIFESTO não for idempotente — não propaga falso-verde. Toda instância deve saber que `gate-fechamento.sh`/boot tocam o main.

**D-15 — 'indexado' é o ÍNDICE, não o rótulo do .json (B-15/NV-1). (2026-06-27)**
- *Tese:* `status_pipeline:"indexado"` só é verdade se há chunk em `rag/chunks/<id>/` E entrada em `rag/index/`. 4 leis IPTU diziam "indexado" com 0 chunks (falso-verde gravado no corpus).
- *Antítese:* "o .json diz indexado, então está indexado." *Vacina:* `consolidar.py` agora deriva a verdade do índice e alerta `indexado_sem_chunks_no_indice`; ambos os gates FALHAM se a lista não for vazia. Corrigido indexando de verdade as 4 (destravar, não rebaixar — RO-09).

**D-16 — Indexar a LPUOS 16.402/2016 destravou TDC no main; negativo é relativo ao acervo. (2026-06-27)**
- *Tese:* ao pagar B-15, a LPUOS entrou no índice e a consulta de TDC ("potencial construtivo passível de transferência") passou a ser FUNDAMENTADA com citação real (Art. 24, cobertura 86%) — 1º destrave de produto TDC no main.
- *Antítese:* "o eval negativo quebrou, força ele a passar." *Vacina:* a premissa do `neg-tdc-fora-de-corpus` mudou (TDC entrou no corpus); revalidado para POSITIVO conforme a vacina "negativo é relativo ao acervo". Revalidar negativos a cada expansão do corpus.

**D-17 — Engine: trava FATAL em campo próprio + citação por dispositivo (B-12c/d). (2026-06-27)**
- *Tese:* a trava FATAL de gabarito (COMAER/CONPRESP/LPUOS-Q3) virou campo próprio EXECUTADO (antes caía muda em `blocos_nao_avaliados`); a citação do engine aponta o DISPOSITIVO (PDE art. 125 via remissão na LPUOS; Estatuto da Cidade art. 28-31), não a lei inteira.
- *Antítese:* "cita a lei e está fundamentado." *Vacina:* lei-inteira não é citação (1.7). Onde o artigo do PDE não está no verbatim (PDE ainda bruto, B-4), `confianca:"a_confirmar"` — apontar+sinalizar > blob.

> **Pendência REGISTRADA (não resolvida nesta sessão): B-17 — produto preso na branch órfã `project-audit-roadmap-2thi1g`** (B-1 fechado, TDC verbatim 19×13, engine sobre imóvel real, E5 provado). Consolidar ao main é cross-repo (decisão MOU); depositado em `caixa-de-saida/para-escritorio/`.

---

## 6. DECISÕES PENDENTES
- Nome definitivo do Codex Mestre (domínio).
- Escopo geográfico/temático além de IPTU+TDC em São Paulo capital.
- Onde mora o software quando for a hora (banco relacional + espacial; LLM na
  casca) — confirmar stack.
  - **Achado (2026-06-19):** existe a org Supabase **"Gestão Integrada"** com 1
    projeto ativo `gestao-integrada-dados` (Postgres 17, sa-east-1). Hoje é do
    **KEEPEE** (migration `init_keepee_raw`; schema `public` vazio) — **fora do
    escopo Potencial Urbano**; o IPTU/TDC **não usa Supabase ainda** (0 referências
    no repo). Porém o Supabase **encaixa no requisito** (PostGIS, pgvector,
    pgrouting, address_standardizer, pg_cron — todos disponíveis). **Sugestão p/ o
    operador (RO-22):** se adotar, usar um **projeto SEPARADO** para IPTU/TDC (não
    misturar com o do Keepee — separação de escopo). Decisão dele.
  - **RESOLVIDO (2026-06-19):** operador adotou Supabase. Criado projeto SEPARADO
    `potencial-urbano-iptu-tdc` (ref `csnalylpvysjvejgsymr`, sa-east-1). Stack
    confirmado: Postgres 17 + PostGIS + pgvector + pg_trgm/unaccent/fuzzystrmatch.
    Esqueleto canônico iniciado. **VACINA (2026-06-20, auditoria triplo-limpo):**
    verificado via MCP que HOJE existem apenas `governanca` (`de_para` [livro-razão
    RO-14] + `registro_decisoes`, vazias) e `public`/PostGIS. Os schemas dos 4
    artefatos + `geo` + `rag` **ainda NÃO foram criados** — eram plano, não fato.
    Playbook reutilizável em `BETA-CONTINUO.md`. Chaves só em env (não no git).

---

## 7. REGISTRO DE FASE 0 (achados e decisões)

**Estrutura no Drive** (projeto raiz "POTENCIAL URBANO"):
`00 Governança` · `01 entrada (despejo)` · `02 Leis & Jurisprudência` ·
`03 Tabelas & Engines` · `04 Tese (Antítese/Vacina)` · `05 Geo / Mapas` (criada
nesta fase) · `99 Inbox/Triagem`.

**Inventário da pasta de entrada:** 1.398 arquivos únicos, **100% identificados,
0 ilegíveis**. Esqueleto do De/Para em `inventario/de-para-entrada.csv`.

**Achado estratégico:** 648 arquivos "octet-stream" eram a **base cartográfica
completa de São Paulo** (~160 camadas de shapefile: zoneamento, ZEIS, ZEPEC,
LOTES, SIRGAS + 2 GeoPackage) = o **Motor 3 (geo)** inteiro, já em mãos.

**Insumos de tabela/dado:** ~169 planilhas (CSV/XLSX/XLS/ODS) + 1 `.tgz` com a
Tabela VI (padrões de construção, Lei 16768/2017) + 464 PDFs.

**Verificação do acervo jurídico (2026-06-18) — corpo legal COMPLETO no Drive.**
Varredura direcionada (title + fullText) confirmou que **todo o backbone
normativo já está no Drive**, em PDF oficial (e boa parte também em texto integral
fatiado). **Nada falta baixar; nenhuma captura externa (extensão/anti-bot) é
necessária** — a fonte verbatim das leis é o próprio Drive. Catálogo com os
`drive_id` em `inventario/catalogo-juridico-drive.csv`.
> **CONCILIAÇÃO (2026-06-20, auditoria):** "nenhuma captura EXTERNA" segue verdadeiro
> — a fonte está no Drive. Mas a INGESTÃO no repo está incompleta: 12 federais + 1
> municipal (7228) + 11 STF foram ingeridas verbatim do upload do MOU (2026-06-19);
> **15 leis municipais-SP no repo ainda são RESUMOS não-verbatim** (`confianca: baixa`,
> ver `MANIFESTO.json` campo `alertas`) e precisam ser RE-INGERIDAS dos PDFs do Drive
> — não é captura externa, é fatiamento do que já temos.

Eixos confirmados:
- **Urbanística:** PDE Lei 16.050/2014 · LPUOS/zoneamento Lei 16.402/2016 ·
  Código de Obras e Edificações Lei 16.642/2017 · `codigo_de_obras_ilustrado` ·
  PDE2013 Quadro 1 (CA) · Resol./Portarias SMUL·CTLU·CEUSO.
- **TDC / Potencial Construtivo:** Certidão e Declaração de Potencial
  Construtivo + ~100 docs de **tombamento / ZEPEC-APC / patrimônio** (CONPRESP) —
  a origem da transferência.
- **IPTU / tributário municipal:** Lei 6.989/1966 + cadeia de alterações
  (13.250, 14.256, 15.044, 15.889, 17.719, 18.095, 18.270, 18.330…) + Instruções
  Normativas SF/SUREM + decretos 52.884→64.018.
- **Federal e CF:** Estatuto da Cidade (L10.257), CTN (L5.172), CF art. 156,
  L6.015, L6.830, L8.009, L8.668, L9.514, L10.931, L11.101.
- **Jurisprudência e norma técnica:** ~69 acórdãos/decisões (TJSP, STF Tema
  1062, STJ Súmula 160, REsp) + ABNT NBR 14653-2 (avaliação de imóveis urbanos).

**Executor de movimentação — REVISADO (2026-06-18): NÃO é mais necessário rodar
Apps Script.** A decisão anterior previa **Google Apps Script** para *mover
fisicamente* os arquivos no Drive (sem duplicar), porque a ferramenta MCP só
copia. Verificou-se que **o pipeline não exige mover nada**: o MCP **lê todo
arquivo no lugar, pelo `id`**, e a pasta de origem fica registrada no metadado
(`parentId`) — então a qualificação-por-pasta (RO-12) é feita de forma **virtual**
no De/Para, sem tocar no Drive. Mover fisicamente vira **opcional** (só conforto
de navegação humana) e fica **fora do caminho crítico**. Não copiar também honra
a RO-19 (redundância é inimiga). Se algum dia o operador quiser a arrumação
física, o Apps Script é gerado sob demanda a partir do mapa De/Para.

**Arrumação física do Drive — EXECUTADA a pedido do operador (2026-06-19).** O
operador optou pelo conforto de navegação humana e pediu a arrumação física. Foi
gerado, sob demanda, o pacote em `drive-arrumacao/` (subordinado a este Codex —
RO-17; aqui é o registro canônico, lá são os artefatos operacionais):
- **De/Para localizador do sub-projeto:** `de-para-final.csv` — fonte da verdade,
  **992 itens (984 arquivos + 8 pastas)**, colunas drive_id·titulo·destino·origem·tipo.
- **Executor:** `Arrumar-Drive-PotencialUrbano.gs` (Apps Script). Move sem
  duplicar; idempotente (`JA_OK`). **Motor v5:** roda por orçamento de tempo
  (~4,5 min, abaixo do limite de 6 min), grava a cada 25 itens, trava
  `LockService`, e **auto-reagenda no `finally`** até `=== FIM. 992 itens. ===`.
  Reset: `resetProgresso`. Relatório = planilha "Arrumacao Potencial Urbano FINAL".
  (Motivo do v5: o lote fixo de 200 travava no meio — ensaios pararam em 400/800/620.)
- **Auditor:** `auditar-relatorio.py` cruza o relatório de saída × De/Para e dá
  veredito "COMPLETO" só com 992 itens, 0 ERRO e a linha FIM.
- **Apoio:** `DECISOES.md` (log de decisões do sub-task), `HANDOFF.md` (runbook +
  próximos passos), `ESTRUTURA.md` (árvore final), `triagem-classificar.py`.
- **Origem dos 992:** 868 do despejo `01 — _entrada` · 65 Meu Drive (solto) · 51
  Google AI Studio · 7 Meu Drive (pasta) · 1 MAPAS.
- **8 pastas inteiras (bloco):** →03 Tabelas: DataLake_TDC, TODOS TDC, IPTU 12-05,
  Colab Notebooks (24 nb); →02 Leis: IRRF Tema 1130, **Novos** (64 PDFs juris/
  doutrina IPTU), dados_pericia1 (decisões DOSP); →05 Geo: Imagens_Extraidas (84 PNGs).
- **Escopo (RO-09 honrada + decisão do operador "só A"):** só pauta IPTU/TDC na
  arrumação física. **52 arquivos fora de pauta foram RETIRADOS do plano de
  movimentação** (16 IA-infra/.md, 20 logs/artefatos de download, 13 financeiros,
  3 de outro projeto — Keepee/BNDES, Contrato de Gestão, Guia de Pastas).
  **Nada foi apagado** — ficam onde estão no Drive. Certidoes (41) idem.
  - **ALERTA ao operador (RO-16):** os "mestres de IA" (CONHECIMENTO_MESTRE,
    oráculos, MÓDULO I) são **insumo de escrutínio**, não lixo. Só ficaram fora da
    ARRUMAÇÃO FÍSICA; permanecem no Drive para a Etapa 1. Decisão de não organizá-
    los junto é só de navegação — eles NÃO se perdem.
- **Triagem (99):** sobraram **10 itens ambíguos** (decisão manual posterior):
  `02-23 Anexo I/II`, `MON.pdf`, `mover_pdfs_STJ.ps1`, `Novo Relatorio SITE 2021`,
  `Pedido de Reconhecimento de Complexo de Saúde` (candidato a 2.1), `vilas
  operárias (Migliari)`, `tabela_2025_Retificado`, `tributario 2`, `Tributario Cidades 2`.
- **Auditoria (2 sub-agentes, 2026-06-19):** integridade do plano PASSOU
  (.gs == De/Para; 992; 0 ID duplicado/malformado/em-dois-destinos; 8 pastas ok);
  catalogação sólida (0 enquadramentos claramente errados).
- **Dedup — PENDENTE, sob RO-12/RO-14/RO-19:** sinalizadas ~59 cópias por
  nome+pasta (ex.: stf-sumula-539 6×, SIRGAS_SHP_benstombados1 6×, BASE_TDC_v1_3
  4×). **Antes de eliminar:** confirmar por conteúdo e tratar VERSÃO como linhagem
  (RO-12: versão não é duplicata; nunca descartar). Só remover cópia **idêntica
  confirmada**, **pós-move** e com OK do operador. Não atrapalha a movimentação.
- **Varredura das PASTAS VIVAS (2026-06-19, acesso Drive liberado):** mapeados os
  IDs reais das pastas-destino. **Bug achado e corrigido:** o resolvedor de
  caminho quebrava o destino em "/", e como as pastas canônicas têm a barra no
  nome (`05 — Geo / Mapas`, `99 — Inbox / Triagem`) ele criava pastas aninhadas
  erradas. Corrigido com `CONFIG.FOLDER_IDS` (ancora destino→ID real). Sobraram 2
  pastas órfãs vazias (`05 — Geo`, `99 — Inbox`) a remover com OK do operador.
  Detalhe em `drive-arrumacao/DECISOES.md` (AF-27..30).

---

## 8. LIÇÕES DA INSTÂNCIA ANTERIOR (vacinas — valem para o projeto E para o Escritório do MOU)

**RO-16 — O documento oficial gerado do zero é a fonte da verdade.** Os
mestres/matrizes de IPTU e TDC (v89–v91, oráculos, "Conhecimento Mestre",
MÓDULO I) são **base de início de escrutínio, NÃO fonte da verdade**. Somos
agnósticos: a verdade é o documento oficial que **nós geramos do zero** a partir
de fonte oficial; os mestres apenas **enriquecem e provocam** o escrutínio.

**RO-17 — Uma única fonte da verdade (SSOT).** Erro anterior: 3 branches
paralelas reescrevendo a constituição, nunca reconciliadas → sem SSOT.
Reconciliar antes de bifurcar; não reescrever a constituição em paralelo.

**RO-18 — Toda citação legal conferida na fonte oficial.** Erro anterior: herdou
citações erradas dos mestres (isenção por enchente é Lei 17.202/2019, não
14.493/2007; Tema 1.084 do STF é ARE 1.245.097). Nunca herdar nº de lei/citação
de documento não-oficial sem conferir no oficial.

**RO-19 — Redundância é inimiga.** Erro anterior: acervo com redundância 16–20× e
re-síntese sem linhagem. Dedup ativo + versão sempre como linhagem rastreada
(RO-14); nada de nova síntese sem registrar de onde veio e o que substitui.

**RO-20 — Proveniência honesta, nunca verbatim falso.** Erro anterior: resumo de
busca gravado como se fosse o texto da lei. Sempre marcar proveniência e
confiança; nunca passar resumo por verbatim; nunca classificar documento sem
abrir (RO-13).

**RO-21 — Não cravar ausência sem varredura.** Nunca afirmar que um documento
"não existe" (nem propor captura externa para "suprir" o que faltaria) sem antes
**provar** com busca direcionada no Drive (`title` + `fullText`). Ausência de um
item numa amostra parcial **não** é ausência no Drive (provado: `L10257.pdf`
existia mas não estava na primeira amostra de 1.000). Quando o operador
questionar uma afirmação de ausência, a resposta é **rodar a varredura e mostrar
a prova (com `drive_id`)**, não reafirmar de memória.

**RO-22 — Toda escolha do operador é trazida como SUGESTÃO pronta.** Quando a
decisão é dele, o agente traz a **recomendação na frente** (a opção que ele
mesmo faria) com os trade-offs, para o operador só **vetar/confirmar** — nunca se
devolve a decisão crua nem se pede que ele escolha do zero. Complementa a RO-11
(operador trabalha na tela). *(cravada pelo operador nesta instância, 2026-06-19.)*

**RO-23 — O banco só recebe dado depois da organização completa e aprovada.** O
Supabase mantém-se **limpo** (só estrutura/esqueleto) até o acervo estar
organizado e o operador aprovar a carga. DDL/estrutura é organização e pode
existir; **dado de documento (De/Para, leis, geo, tabelas) NÃO entra antes da
hora**. Lá dentro tudo nasce limpo. *(cravada 2026-06-19.)*

**RO-24 — Após QUALQUER alteração, re-varrer tudo até o TRIPLO-LIMPO oficial.**
Toda mudança ou implantação — em doc, código, Drive ou banco — dispara nova
auditoria cruzada em **todos os locais** (repo/docs · Drive · conversa · Supabase
· beta-contínuo) até **3 rodadas limpas consecutivas em todos**, sem pendências.
Só então a mudança é **oficial**. *(cravada pelo operador nesta instância, 2026-06-19.)*

---

*Versão 0.5 — documento vivo. Toda regra nova decidida em conversa é registrada
aqui pelos agentes (RO-11). v0.2 (2026-06-18): RO-21; verificação do acervo
jurídico (corpo legal completo no Drive, sem captura externa); Apps Script de
movimentação rebaixado a opcional/fora do caminho crítico. v0.3 (2026-06-19):
RO-22 (sugestão pronta); §7 registra a ARRUMAÇÃO FÍSICA executada a pedido do
operador (pacote `drive-arrumacao/`, motor v5, plano de 992 itens, escopo "só A"
IPTU/TDC, Triagem=10, auditoria por sub-agentes). Detalhe operacional subordinado
em `drive-arrumacao/DECISOES.md` (decisões AF-xx) e `HANDOFF.md`.
v0.4 (2026-06-19): RO-23 (banco limpo até organização) e RO-24 (triplo-limpo após
qualquer alteração); Supabase ADOTADO — projeto `potencial-urbano-iptu-tdc`
(scaffold limpo, sem dado); playbook reutilizável `BETA-CONTINUO.md`.*

---

## ESTADO OFICIAL (para a próxima instância) — 2026-06-20; ATUALIZADO 2026-06-27 (3 auditorias + pague-tudo)
> Atualização 2026-06-27: ver `docs/AUDITORIA-PROFUNDA-2026-06-27.md`, `BACKLOG.md`, `PROXIMA-INSTANCIA.md`.
> Decisões novas: **D-13…D-17** (§5). Números canônicos vivem no `MANIFESTO.json` (não cravar à mão — NV-5).
- **Esteira RAG:** EXISTE e provada fim-a-fim (`scripts/fatiar|indexar|consultar` + `evals/`, gate 1.7).
  **17 leis indexadas** (12 federais + 7.228/1968 + 4 IPTU/zoneamento: LPUOS 16.402, COE 16.642, 17.733,
  decreto 57.443), **1.571 dispositivos** (era 13/1.246 — B-15 indexou de verdade as 4 que tinham rótulo
  `indexado` falso). **TDC DESTRAVADO no main:** consulta de potencial construtivo transferível cita a LPUOS
  16.402 Art. 24 (cobertura 86%). 14 municipais ainda só resumo (re-ingerir — B-4). Engine TDC em CÓDIGO
  (`engines/tdc/oodc.py`; trava FATAL + citação por dispositivo — D-17).
- **Mecanismo anti-perda ("ladrão" D83):** `BACKLOG.md` + hook de boot + `scripts/fechar-instancia.py`
  (rodar ao fechar; sai 0 = verde).
- **SSOT:** este Codex (v0.5). Playbook do escritório: `BETA-CONTINUO.md`.
- **Arrumação física:** plano FINAL de 992 itens (984+8) auditado; motor v5 com fix
  do `/` (FOLDER_IDS). Ainda em ENSAIO — falta o operador rodar até `=== FIM ===`
  e então o move real.
- **Supabase:** `potencial-urbano-iptu-tdc` (`csnalylpvysjvejgsymr`) — esqueleto
  canônico LIMPO: hoje **só `governanca`** (`de_para`/`registro_decisoes`, vazias)
  **+ `public`/PostGIS**. (VACINA 2026-06-20: docs antes diziam "6 schemas" — os 4
  artefatos + geo + rag ainda não existem; verificado via MCP.)
  **Sem dado por decisão (RO-23)** até a organização completa e aprovada.
- **PENDÊNCIAS DO MOU/escritório (registradas, não bloqueiam):**
  (a) apagar as 2 pastas órfãs vazias no Drive — `05 — Geo`/`99 — Inbox` (AF-29);
  (b) rodar o ensaio até `=== FIM ===` e o move real, quando quiser.
- **Próximos passos:** (1) operador conclui o ensaio/move e apaga as órfãs;
  (2) planejar e aprovar a organização do acervo antes de carregar o banco;
  (3) Etapa 1 (Codex Mestre) e Fase 2 (identificação de imóveis).
