# Estratégia da VISTORIA de proveniência do Drive PU — POR CONTEÚDO, SEM ATALHO
> Pedido do MOU: classificar CADA arquivo em **OFICIAL / NÃO-OFICIAL-EXTERNO / CRIADO** (criado = só ideia,
> não usar) e separar tudo que serve para **achar o proprietário** em **`06 — Comercial`**.
> **Override do MOU (2026-07-13):** _"o certo não é usar nada do que está pelo que parece; tem de entrar no
> documento e olhar um por um; não aceito meia boca; não quero atalhos."_ ⇒ **classificação por CONTEÚDO real,
> não por nome/pasta/tag.** Desenho validado por 2 rodadas de lentes independentes (8 lentes, travadas, sem spawn).

## Por que o atalho foi REPROVADO (a 2ª rodada demoliu a 1ª)
- A regra por-sinal classificou só **15%**; deixou **85% (28.038) como "DESCONHECIDO"** — não cobriu "95%", ficou no escuro.
- Erros caros e reais no catálogo: **Lei 16.050 como `.csv` de 171 bytes** tagueado OFICIAL (não cabe 300 artigos = stub);
  **`LEI 16.050 … « Catálogo … (1).pdf`** = redownload da PÁGINA do portal, não Diário Oficial; **DECRETO/PORTARIA `.md`
  oficiais presos na camada SILVER** seriam jogados fora como "criados"; **12.957 PNGs (39% do acervo)** são páginas-imagem
  que a regex de nome não enxerga; a coluna `oficialidade` está **corrompida** (desalinhamento de CSV). Sinal = "meia boca".
- No jurídico, proveniência é **cadeia de custódia** (quem produziu, de que fonte certificada, íntegro até o dispositivo) —
  "parece oficial" não é prova. Um falso-oficial no corpus vira fonte de citação (viola 1.3/1.7). **O ônus da prova é da oficialidade.**

## A REGRA DE OURO (anti-meia-boca)
**Nenhum arquivo recebe classe sem o CONTEÚDO efetivamente inspecionado e a EVIDÊNCIA registrada.**
- "Não consegui ler" é um ESTADO EXPLÍCITO (`ILEGÍVEL`), nunca um palpite silencioso. `PENDENTE` = ainda não olhado.
- **"olhado e inconclusivo" ≠ "não olhado".** Herdar classe pela pasta/extensão/amostra = atalho PROIBIDO.
- Automação escala o ESFORÇO de abrir cada um; ela **nunca** substitui o ato de olhar. O que não pode escalar é a presunção.

## O que prova cada classe (marcas DENTRO do documento — protocolo forense)
- **OFICIAL:** masthead reproduzido no corpo — "Diário Oficial da Cidade de São Paulo" / "Imprensa Oficial", brasão/órgão
  emissor, "publicado em DD/MM/AAAA", nº+data, fecho/assinatura da autoridade, boilerplate do portal
  ("Este texto não substitui o publicado"); em PDF nativo, metadados `/Producer`/`/Author` de órgão gov. A marca é do EMISSOR.
- **CRIADO-POR-NÓS:** cabeçalhos do nosso pipeline (`## Texto integral (verbatim)`, `**Proveniência:**`, blocos de
  chunk/auditoria, JSON nosso, `ORACULO_/CONHECIMENTO_MESTRE/log_extracao`) OU **prosa sintetizada** no lugar do articulado literal.
- **NÃO-OFICIAL-EXTERNO:** o mesmo texto legal, mas SEM masthead oficial E SEM nossos cabeçalhos (PDF de escritório,
  apostila, print, base comprada com colunas proprietárias). Texto certo, custódia ausente. **Só esta classe (externa) serve
  de alicerce operacional (comercial); a CRIADA é só ideia; a OFICIAL é o corpus.**
- **Envelope nosso sobre miolo de terceiro:** registrar as DUAS camadas; a classe segue a FONTE do texto, não a embalagem.

## Como abrir e ler CADA tipo (o conteúdo, não a borda)
| Tipo | O que extrair / onde olhar |
|---|---|
| PDF nativo | texto das páginas **1ª e ÚLTIMA** (masthead no topo, assinatura no fim) + metadados `/Producer /Author /CreationDate` |
| PDF escaneado / imagem | rasteriza pág.1 + **OCR (tesseract-pt)**; procura brasão/carimbo/Diário Oficial; sem texto ⇒ `SEM_TEXTO` registrado |
| `.md` / `.txt` | primeiros ~8 KB (cabeçalho do nosso pipeline aparece no topo); rolar ao miolo p/ ver se é verbatim ou resumo |
| `.csv` / `.xlsx` | cabeçalho de colunas + primeiras ~20 linhas (streaming); colunas proprietárias/marca de fornecedor = base externa |
| imagem (png/jpg) | OCR / visão; masthead ⇒ oficial, barra de navegador/recorte ⇒ print de terceiro; ilegível ⇒ registrado |
| shapefile (.shp/.dbf/.prj) | schema do `.dbf` + `.prj` (produtor GeoSampa/PMSP, datum SIRGAS) — a identidade do geodado |
| **GIGANTES** (socios 3,44 GB, empresas 2,27 GB, IPTU_2026 937 MB, iptu-2020 152 MB) | **`Range: bytes=0-262143`** (256 KB) = cabeçalho + amostra. **Isto É ler o documento** (a identidade de um CSV está no header+amostra), não atalho. Nunca baixar o corpo inteiro. |
| Google Docs/Sheets/Forms | `files.export` p/ texto (trunca ~10 KB) |
> Em TODOS grava-se `sha256` do que foi lido — **prova de que abriu**.

## Pipeline (viável, sem runaway, sem custo absurdo)
1. **Extração de conteúdo** — Action SA `extrair_conteudo_sa.py`: para cada `drive_id`, `files.get(alt=media)` em stream,
   extrai texto real por tipo (acima) → grava `conteudo_extraido(drive_id, texto_amostra, n_chars, ocr, sha256, extrator)`.
2. **Classificação SOBRE o conteúdo extraído** (nunca sobre o nome):
   - Passada A — **determinística sobre marcas reais no texto** (masthead/nossos-cabeçalhos/colunas) resolve ~70–85%;
   - Passada B — fração AMBÍGUA → **Haiku via Batch API, 1 doc por chamada** (cascata 1.4), devolve `{classe, evidência, trecho}`.
   - Custo (ordem de grandeza): ambíguos ~3–6 mil → **US$ 3–7** (todos os 33k no Haiku daria ~US$ 40, teto trivial).
   - Tempo: gargalo é o OCR das ~12.785 imagens (~1–2 h com shards); a classificação LLM é minutos.
3. **De-para de proveniência** (o razão, versionado + Supabase `governanca.de_para` que JÁ EXISTE — migração
   `20260703145720_seed_de_para_proveniencia_drive.sql`): colunas
   `drive_id · caminho(contexto) · nome · mime · bytes · classe{OFICIAL|NAO_OFICIAL_EXTERNO|CRIADO|ILEGIVEL|PENDENTE} ·
   comercial{sim|nao} · evidencia_conteudo(trecho literal do arquivo) · evidencia_localizacao(pág/linha) ·
   metodo{texto_nativo|ocr|leitura_llm|metadados} · confianca · revisado_humano · motivo_ilegivel · sha256 · timestamp`.
4. **Auditoria (como o MOU confere que não houve atalho):** para QUALQUER `drive_id`, a linha mostra o trecho real que
   decidiu; classe preenchida com `evidencia_conteudo` vazia ⇒ **erro sinalizado**. Amostra cega conferível. Matriz
   **classe × método** (quantos por texto-nativo, OCR, LLM, ILEGÍVEL). 100% dos OFICIAL e COMERCIAL revisados (os caros de errar).
5. **ANTI-RUNAWAY:** ZERO Agent/Task/sub-agente; um job sequencial por shard, **matrix de N shards na Action**
   (`drive_id % 10 == shard`), idempotente/retomável por `sha256` (pula o já-lido). READ-ONLY no Drive nesta fase (só lê).
6. **Depois** (fase separada, com ENSAIO + gate humano "pode mover"): mover por classe/comercial → `06` etc. + selo. Nada se apaga.

## `06 — Comercial` — os 3 itens que o MOU citou (localizados; classe CONFIRMADA por conteúdo na vistoria)
| Citado | Arquivo | Tam. | Hoje | Classe provável (confirmar por conteúdo) |
|---|---|---|---|---|
| "IPTU não-2026" | `iptu-2020-cep01.csv` (+`.gz`) | 152 MB | `03` | OFICIAL (cadastro IPTU 2020) → **`06`** |
| "sócios" | `socios.csv` | 3,44 GB | `03` | NÃO-OFICIAL-EXTERNO (base Receita/QSA) → **`06`** |
| "empresas" | `empresas.csv` | 2,27 GB | `03` | NÃO-OFICIAL-EXTERNO (CNPJ) → **`06`** |
> Bônus p/ `06`: `GUIAS*ITBI*`, `SIRGAS_SHP_LOTES_*`, Cartão CNPJ. **NÃO vai p/ `06`:** `IPTU_2026`/Quadro 14/PGV (dado de
> ENGINE → `03`). Toda classe acima é **hipótese até a vistoria abrir o arquivo e confirmar pelo conteúdo.**
