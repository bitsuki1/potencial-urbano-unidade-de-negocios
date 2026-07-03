# MOTOR 2 — DADOS / INFRA (M-DADOS) · Estratégia

> **Como foi produzida.** Loop de 7 lentes Sonnet + síntese/crítica Opus, limite de 5 rodadas. **NÃO atingiu triplo limpo — bateu no teto** com ALTA persistente (trajetória 7→8→6→7→3 ALTA). É o motor onde o **construído diverge mais de qualquer plano limpo**.
> **Achado grave e REAL (verificado ao vivo no Supabase, projeto `csnalylpvysjvejgsymr`):** crise de canonicidade — as migrations que RODAM no banco (`oficiais.*`, com os 3.905/3.676 dados reais) **não têm `.sql` no git**; as migrations do git (`dados.*/geo.*/tabelas.*`) **nunca foram aplicadas** e não têm dado. "`db reset + migrations`" reproduziria o schema VAZIO, não o que o produto usa. Pior ainda: o número in-scope não vem de nenhum dos dois — `enriquecer_oficial.py` lê CSVs planos e não toca Postgres.
> **Outros ALTA:** o runner do E1 não regenera de checkout limpo (falta o gerador do recorte Q14 e do `cedentes_sqls.txt`, que já diverge da fonte); vintage do E2 conflaciona fato/ingestão/vigência (Q14 precisa de intervalo); E4 esquecia de carregar os 817 shapefiles.
> **Ver `docs/ESCRUTINIO-CONJUNTO-MOTORES.md`** (a reconciliação de schema/CI/proveniência é o caminho crítico que destrava os 3 motores).

---

Confirmed against the repo. Three notes on the findings before I write:

- **F1** holds exactly: `README.md:9` is `curl -sS <url_iptu> | python3 filtro_iptu.py` — no input verification before transform.
- **F2** holds exactly: `filtro_iptu.py:2` is `open('cedentes_sqls.txt')` and `:4` writes `oficiais/cedentes_area_iptu.csv` — bare CWD-relative paths.
- **F3 is half-right and I correct the diagnosis:** the committed `filtro_iptu.py` header (`sql_mestre,area_terreno,area_construida,v_venal_m2,codlog,uso,padrao,endereco`) is **byte-identical** to the committed `zepec/oficial/iptu2026_cedentes.csv` header — so F3's "different column contract" claim is FALSE. The real divergence is **path/name only**: the script writes `oficiais/cedentes_area_iptu.csv` while the artifact README/PROVENIENCIA claim it produces is `zepec/oficial/iptu2026_cedentes.csv`. F3's remedy (byte-for-byte assert, not count) is still correct and I adopt it; I fix the diagnosis.
- **F4** holds (compute tier confirmed in prior rounds).

Definitive version below.

---

# ESTRATÉGIA DO MOTOR 2 — DADOS / INFRA (M-DADOS) — v7 (definitiva)

## 1. Objetivo do motor

O pipeline de dados deixa de ser uma FOTO irreproduzível e vira SISTEMA: cada dado sabe DE ONDE vem (fonte + sha256) e DE QUANDO (vintage — exercício, intervalo de vigência ou data de ato jurídico); a cadeia inteira se regenera de um checkout limpo de forma determinística e byte-idêntica, ancorada não só no transform mas também no INPUT (todo byte de fonte-raiz é pinado por hash antes de ser transformado); e o banco é reconstruível do git (migrations + loaders idempotentes). M-DADOS é o substrato sobre o qual os demais motores assentam: ele TORNA a cadeia reproduzível — o GATE que CHECA a reprodutibilidade (byte-diff no CI) é do Motor 1 (T2), e pinar o input é obrigação de M-DADOS ("tornar reproduzível"), não do gate. Princípio de prova transversal: "declarei feito != provei feito" — todo DoD abaixo é assert mecânico (conta, `cmp`, byte-diff, `SELECT`, grep-de-código-fonte, hash-equality), nunca prosa, e só vale se já foi rodado contra o estado REAL do repo.

---

## 2. Entregas

### E1 — Runner reprodutível único, com INPUT PINADO (cadeia completa, fonte-raiz → deliverable)

**O que faz:** `refazer_oficial.sh` (`make base`) regenera a cadeia inteira de um checkout limpo, SEM `/tmp` e SEM path absoluto de máquina, resolvendo colunas por NOME de header (abort se faltar/renomear) e **verificando o sha256 de cada objeto Bronze baixado contra o manifesto de E2 ANTES de transformar** (aborta se divergir). Todo path deriva de `Path(__file__).resolve().parent`/`REPO_ROOT`, nunca de literal. Ordem real verificada nos scripts:

- **Passo 0 (universo, bootstrap de 2 passadas):** `_pull_externo.py` (decodifica base64 do Drive → `raw/externo/*`, `OUT` corrigido para path relativo) → `montar_base.py` → `montar_ferramenta.py` (1ª passada) → `donos.py` + `fundurb.py` → `montar_ferramenta.py` (2ª passada) → `higienizar.py` (relatório, não-bloqueante). Regenera `zepec/ferramenta/zepec_cedentes.csv` (6.131) das 4 fontes ZEPEC-BIR + 4 externas de titularidade. Nota: `montar_ferramenta.py:130/149` colapsa três datas em `data_ref=max()`; o runner mantém isso SÓ no CSV comercial (Gold), e o Silver de E4 NÃO herda o colapso (ver E2 família 2c).
- **Passo 0b (derivar SQLs, preventivo):** gerar `cedentes_sqls.txt` de `zepec_cedentes.csv` (SQLs únicos, não-vazios, ordenados). Nasce verde; existe só contra drift futuro.
- **Passo 1 (recorte IPTU):** `filtro_iptu.py` REESCRITO — `csv.DictReader` mapeando `area_terreno/area_construida/v_venal_m2/codlog/uso/padrao/endereço` por NOME de header (hoje é `csv.reader` + índices posicionais `r[14],r[15],r[17],r[22],r[23]` com `if len(r)<24: continue` — descarte silencioso), abort explícito (não `continue`) em header ausente ou linha malformada. **Escreve no path canônico `zepec/oficial/iptu2026_cedentes.csv`** (hoje o script committed escreve `oficiais/cedentes_area_iptu.csv` — path/nome divergente do artefato que README/PROVENIENCIA declaram; o header já é idêntico). Sobre IPTU do Silver em E1b.
- **Passo 2 (recorte Q14):** `recorte_q14.py` (script novo/commitado; hoje só existiu em sessão efêmera), filtra por SQL e por NOME de coluna, com abort.
- **Passo 3 (overlay):** `overlay_zona.py` com `DL` (hoje `/tmp/…`, `:8`) e `REPO` (hoje absoluto, `:9`) parametrizados para dentro do repo/workspace. Sobre geometrias do Silver em E1b.
- **Passo 4 (engine + Gold):** `enriquecer_oficial.py` → CSV Gold versionado (`pcpt_m2`, `saldo_pcpt_m2`, `preco_proxy_brl`).
- **Passo 4b (fila comercial):** `lista_prospeccao.py` → `lista_prospeccao.csv` + `fila_verificar.csv`. **Decisão a declarar em 1 linha:** hoje parte de `zepec_cedentes.csv` CRU e ignora o enriquecimento do Passo 4 — decidir se é intencional ou elo quebrado (não reescrever especulativamente).
- **Passo 5 (apresentação):** `gerar_xlsx.py` com `OUT` parametrizado (hoje `/tmp/claude-0/…ZEPEC.xlsx`, `:8`) + pós-processamento de reprodutibilidade (DoD-3).

**Por que:** sem input pinado, "reprodutível de um checkout limpo" é FALSO — a byte-identidade run↔run só prova que o transform é função pura dos bytes REMOTOS DAQUELE DIA; um drift value-only na fonte (mesmo header, `valor_venal`/`Atc` restaurado) mantém `count=3.905`, passa nos asserts de contagem e de coluna-por-nome, e muda silenciosamente `pcpt_m2`/`preco_proxy_brl` a jusante. Só a igualdade de hash de input pega isso. Sem coluna-por-nome, um reordenamento do export municipal troca área com valor venal e passa no assert de contagem. Path absoluto/CWD-relativo faz o runner falhar (ou escrever na árvore errada) em qualquer checkout — o oposto de reprodutível.

**DoD mecânica:**
1. **Higiene de path — dois asserts, um insuficiente sozinho.** (a) grep no LOG por `/tmp`/path de sessão = vazio; (b) grep no CÓDIGO-FONTE de TODOS os scripts do runner por literal absoluto (`="?/home/`, `="?/tmp/`, `Path("/…`, `/tmp/claude`) fora de `Path(__file__)`/`REPO_ROOT` = vazio (hoje pega `overlay_zona.py:8/:9`, `_pull_externo.py:8`, `gerar_xlsx.py:8`); **(c) contrato de CWD (grep de path é necessário mas NÃO suficiente): rodar o runner inteiro a partir de um CWD de scratch ≠ raiz do repo e assertar sucesso** — pega os bare-relative `open('cedentes_sqls.txt')` e a escrita relativa que o grep de `/home` não vê.
2. **Input pinado (integridade de fonte — obrigação de M-DADOS, não do CI):** antes de cada transform, o runner computa sha256 de cada objeto Bronze baixado (IPTU, Q14, shapefiles) e **ABORTA se ≠ hash do manifesto de E2**. A igualdade de hash de input é parte do CONTRATO de byte-identidade, não uma preocupação só do loader de E2.
3. **Byte-identidade run↔run:** 2ª execução produz byte-idênticos (`cmp`) para os 3 CSVs de `zepec/oficial/*`, o Gold `zepec_cedentes_oficial.csv`, e `lista_prospeccao.csv` + `fila_verificar.csv`.
4. **Fidelidade gerador↔artefato (fecha o gap C-01, não só run↔run):** o `filtro_iptu.py` reescrito, sobre o input PINADO (DoD-2), reproduz o committed `zepec/oficial/iptu2026_cedentes.csv` **BYTE-por-BYTE** (`cmp`), não apenas `count=3.905`. Um rewrite afinado para bater a contagem passaria em DoD-3/DoD-7 enquanto a divergência script-do-git vs artefato-do-git (a doença que E1 existe para curar) sobreviveria.
5. **`.xlsx` reprodutível (mecanismo verificado, openpyxl 3.1.5):** normalizar `ZipInfo.date_time` não basta — `docProps/core.xml` carrega o timestamp como CONTEÚDO e `save` faz `properties.modified = datetime.now()`. `gerar_xlsx.py` reabre com `zipfile`, reescreve cada `date_time` para `(1980,1,1,0,0,0)` E fixa `<dcterms:created>/<dcterms:modified>` constantes. Assert triplo: (a) `cmp` do `.xlsx` entre 2 execuções; (b) nenhuma entrada com `date_time` variável; (c) grep em `core.xml` = constante fixa.
6. **Universo:** `zepec_cedentes.csv` = **6.131**; `proprietario` não-vazio = **79**; `status_fundurb` não-vazio = **7**.
7. **Fidelidade SQL (preventivo) — premissa RE-CORRIGIDA:** comparar `set(cedentes_sqls.txt)` vs `set(sql_mestre de zepec_cedentes.csv)` **excluindo simetricamente dos dois lados** (a) `sql_mestre` vazio (os **1.839** sem SQL, exceção conhecida — sem a exclusão a diferença simétrica real é `{''}`, NÃO vazia) e (b) o sentinela `0000000000` (Parque Estadual do Jaraguá). Esperado: **0/0 por token** após excluir `{'', '0000000000'}` — nunca por `wc -l` (arquivo tem 4291 linhas / 4292 tokens por falta de `\n` final).
8. **Coluna-por-nome (dedicado):** o header do IPTU contém literalmente os nomes esperados antes do parse; renomear/embaralhar uma coluna de um IPTU de teste faz `filtro_iptu.py` **abortar**, nunca produzir CSV.
9. **Regressão:** iptu_cedentes **3.905**, q14_cedentes **3.676**, zona_por_cedente **3.693**, PCpt **3.014**, com preço **2.937** (nomes de tabela conforme E4).
10. **Pin de ambiente completo:** `requirements.txt` com versões EXATAS (shapely, pyshp, openpyxl, numpy), idealmente `--require-hashes`; Python fixado (`.python-version`/`python-version: "3.11.9"`; hoje `consolidar.yml:32` = `"3.x"`) e imagem do runner fixada (`ubuntu-24.04`; hoje `:27` = `ubuntu-latest`). Byte-identidade é propriedade durável; bump de patch muda bytes de zlib/GEOS. Eixo não-pinável = risco residual DOCUMENTADO.

**Desdobramento (resolve a circularidade E1↔E4):**
- **E1a (prioridade 1, provável ANTES de E4):** cadeia completa com Passos 1/3 lendo de download determinístico e PINADO para diretório do repo/workspace (nunca `/tmp`, nunca absoluto) — fixa os 4 hardcodes, o contrato de CWD, coluna-por-nome, input-hash, byte-identidade run↔run e gerador↔artefato, e o `.xlsx`.
- **E1b (gated por E4):** troca Passos 1/3 para consultas Postgres/PostGIS; só aqui vale o assert "zero egress de IPTU/geo no run". A eliminação de egress (894 MB + 457 MB) depende de `oficiais.iptu_bruto` de E4; sem ela, E1b re-baixa 894 MB e a promessa de zero-egress é falsa.

---

### E2 — Vintage obrigatório em TODO dado (1.6 estendida): 2 eixos, 3 famílias de vigência

**O que faz:** todo dado carrega vintage no path Bronze E em coluna Silver. Dois eixos:
- **(1) `capturado_em`** — timestamp de INGESTÃO (proveniência/manifesto).
- **(2) vigência do FATO — três famílias não-colapsáveis:**
  - **(2a) Exercício fiscal (IPTU):** `ano_exercicio` (jan–dez implícito).
  - **(2b) Valor-vigente-até-substituir — INTERVALO `vigencia_inicio` (obrigatório) + `vigencia_fim` (nullable = vigente):** Quadro 14 (`oficiais.q14_valor_terreno`), CA por zona (`oficiais.quadro3_ca_zona`), geometria de zona (`oficiais.zona_geom`). A Lei 16.050 (Art. 125 §1º-III; Art. 127 §2º-III/IV) trata CA/enquadramento como "vigente na data de referência/doação" — rótulo pontual é insuficiente.
  - **(2c) Data do ato jurídico por origem (ZEPEC-BIR):** `montar_base.py` extrai, POR ORIGEM, três datas juridicamente distintas — `data_pub_iso` de DECLARACAO_BIR, de CERTIDAO_BIR_CEDENTE e de TOMBADO_CADASTRO — mas `montar_ferramenta.py:130/149` colapsa em `data_ref=max()` e `gerar_xlsx.py:25` expõe como coluna única. No Silver essas datas sobrevivem SEPARADAS: `data_declaracao_iso`, `data_certidao_iso`, `data_tombamento_iso` (nullable, em `oficiais.zepec_bir`), NUNCA um único `data_ref=max()`. Campo único de exibição, se necessário, é calculado na apresentação citando a origem (1.7) — jamais substitui o bruto no Silver.

**Desambiguação de tabelas (declaração única para E2/E3/E4/E6):** `oficiais.quadro3_ca_zona` = valores de CA (zona, CA básico/máximo) + vigência, sem geometria; `oficiais.zona_geom` = polígonos de zona (via `ST_Contains`) + vigência, tabela NOVA que o overlay exige e hoje não existe.

**Path Bronze:** `oficiais/<fonte>/ano=<AAAA>/…`, manifesto sha256. Vintage obrigatório em: 4 fontes ZEPEC-BIR (`ano=<AAAA-MM>`), 4 externas de titularidade (`ANUAL-2022`, `sissel_2024`, `OODC_2024-2025`, `fila_tdc_5pct_fundurb_dez2025`), **IPTU_2026, Quadro 14 e os 817 shapefiles** (hoje fora de qualquer path com `ano=`).

- **E2-0 (pré-requisito):** as duas tabelas VIVAS (`oficiais.iptu2026_cedentes`, `oficiais.q14_valor_terreno_2025`) não têm coluna de vintage e trazem o ano no NOME — migrar em E4-0.
- **E2b (o canal físico precisa emitir `ano=`):** `subir-oficiais-para-supabase.gs:22-31` (10 `dest:` FLAT) e `subir-grandes-colab.py:28` (`"dest": "oficiais/IPTU_2026.csv"`, 894 MB) não têm segmento `ano=`. Sem E2b, a próxima carga (IPTU_2027) reusa o `dest` flat e SOBRESCREVE `IPTU_2026.csv`. O que faz: reescrever os `dest` para `<fonte>/ano=<AAAA>/<arquivo>`.
- **E2c (`tabelas/*.csv` entra no escopo):** `tabelas/q14-valor-terreno.csv` (git-tracked, sem vintage/hash) é lido DIRETO por `engines/tdc/oodc.py:286`. Toda `tabelas/*.csv` ganha `data_base` + hash no manifesto (e canonicidade em E6).

**Por que:** sem separar captura × exercício × intervalo × ato-por-origem, reproduzimos em dado o erro que 1.6 corrige para leis. Sem E2b, vintage é ficção que o próximo upload apaga. M-DADOS só EXPÕE o intervalo/as datas; correção IPCA e seleção de qual data exibir ficam em M-CALC/apresentação.

**DoD mecânica:**
1. `SELECT` em `oficiais.q14_valor_terreno` retorna `vigencia_inicio/vigencia_fim`; "V vigente na data X" retorna 1 linha por SQ+codlog.
2. Toda Silver tem `capturado_em` não-nulo e `ano_exercicio` OU intervalo conforme família; `quadro3_ca_zona` e `zona_geom` têm `vigencia_inicio/fim`.
3. Manifesto `sha256` por objeto Bronze; loader recusa carga SEM vintage (abort).
4. **8 fontes de titularidade** (4 ZEPEC-BIR + 4 externas) MAIS IPTU_2026, Quadro 14 e o pacote de shapefiles, todas com path `ano=…` e hash (assert: nenhuma fonte crítica em path flat).
5. **(E2b)** grep nos dois scripts de upload: zero `dest` sem `ano=`.
6. **(E2c)** toda `tabelas/*.csv` git-tracked tem entrada vintage+hash no manifesto.
7. **(família 2c)** dois asserts: (a) `oficiais.zepec_bir` tem as três colunas de data por origem (nullable), não um campo agregado; (b) grep em `montar_ferramenta.py` e no loader do Silver confirmando que NENHUMA agregação `max`/`min` de datas de origens distintas ocorre antes da gravação em Silver — se `data_ref=max()` for mantido, é SÓ no Gold de apresentação, documentado como decisão.

---

### E3 — Medallion enxuto (1 página, SÓ convenção de path)

**O que faz:** Bronze = Storage imutável (`oficiais/<fonte>/ano=…`); Silver = Postgres tipado, UMA árvore canônica = `oficiais.*` (E6-fase-0); Gold = CSV versionado no git (inclui `tabelas/*.csv` sob E2c). Sem codex/oráculo por camada.

**Por que:** o cemitério de migrations paralelas já mostrou o risco de cerimônia que ninguém aplica.

**DoD mecânica:** o doc de 1 página existe e nomeia `oficiais.*` como árvore Silver (assert: schemas citados = schemas que `list_tables` retorna vivos com dado). Rejeito "governança por camada" — a convenção de path basta.

---

### E6 (fase 0 — RECONCILIAÇÃO, precede E4) — Uma única árvore de schema canônica

> Antes de E4: quem executa E4 precisa saber em qual árvore trabalhar.

**Estado real (reverificado):** **5** migrations aplicadas SEM `.sql` no git (`enable_core_extensions`, `scaffold_canonico_governanca`, `harden_function_search_path`, `storage_buckets_pesados_e_schema_rag`, `oficiais_camada_produto_tdc`); o git só tem os **3 órfãos** `20260624_010/020/030` (nunca aplicados). Schema `dados` NUNCA existiu. `oficiais.*` e `governanca.*` têm dado; `engine/geo/leis/rag/tese/tabelas` existem vazios. Sem os 5 `.sql`, um `db reset` não recria extensões/buckets/schemas.

**O que faz:**
- (a) `supabase db pull`/`db diff` das 5 vivas → gerar e commitar os 5 `.sql`.
- (b) Fixar Silver canônico = `oficiais.*`; para cada schema vazio: DROP ou população deliberada em `oficiais.*` (nunca dois destinos vivos); aposentar os 3 `.sql` órfãos.
- (c) Criar a migration de `oficiais.zona_geom` (polígonos + `vigencia_inicio/fim`) — o overlay depende dela para zero-egress em E1b. Distinta de `quadro3_ca_zona`.
- (d) **Reconciliar a 2ª fonte de Quadro 14 como as DUAS VIGÊNCIAS reais do mesmo dispositivo (NÃO aposentar a histórica).** Verificado: das 1.753 chaves `(sq,codlog)` em comum entre `tabelas/q14-valor-terreno.csv` (`PDE2013_SUBST2_Quadro_14_cadastro`, lida por `oodc.py:286`) e `oficiais.q14_valor_terreno_2025` (`Atualizacacao_Q14_anoref2025`), **1.753/1.753 têm `valor_m2_brl` diferente**, a oficial ~1,17515× maior (razão constante → correção monetária sobre uma vintage). O próprio repo já classifica o par como as duas vigências (`CATALOGO-MESTRE-DADOS-2026-07-01.md:19`). Ação: carregar AMBAS na MESMA `oficiais.q14_valor_terreno` via SCD-2 (histórica `vigencia_inicio=<data documentada>`, `vigencia_fim='2025-01-01'`; vigente `vigencia_inicio='2025-01-01'`, `vigencia_fim=NULL`); migrar `oodc.py` para consultar "V vigente na data do fato gerador"; a base guarda o V BRUTO de cada fonte (1.2/1.3), a correção 1,17515× é função citável de M-CALC. Só aposentar uma fonte após checagem PRÉVIA de identidade legal (texto/data do Anexo vs Lei 16.050 e sua atualização) — passo explícito do DoD. Aposentar a histórica sem isso descarta a única cópia do V pré-2025 (cedentes que já venderam parcialmente — cenário central), violando 1.6 e "nada se joga fora".

**DoD mecânica:**
1. Git contém os `.sql` das 5 vivas (assert: `list_migrations` = migrations do git, nome a nome — 5, não 1).
2. `list_tables` não retorna tabela em schema aposentado; `dados` continua inexistente (não alegar DROP do que nunca existiu).
3. **Anti-ano-no-nome — regex CORRIGIDO:** `table_name ~ '_(19|20)[0-9]{2}(_|$)'` contra `information_schema.tables` na árvore canônica — pega `_2025` no fim E `2026_` no meio (o regex de sufixo da v5 não pegava `iptu2026_cedentes`/`iptu2026_bruto`).
4. **Consistência entre entregas:** grep em E2/E4 por `dados.`/`geo.`/`tabelas.` como schema-alvo = vazio.
5. Árvore canônica `oficiais.*` nomeada no doc de E3.
6. **Anti-fonte-dupla + reconciliação Q14:** (a) grep em `engines/**` por leitura direta de `tabelas/*.csv` sem passar pela camada de vintage/reconciliação = vazio (hoje pega `oodc.py:286`); (b) `oficiais.q14_valor_terreno` contém AS DUAS linhas de vigência para as chaves em comum (histórica `vigencia_fim='2025-01-01'` + vigente `vigencia_fim=NULL`), OU — só se a checagem de identidade legal de (d) rejeitou uma — a rejeição está registrada com proveniência. Duas fontes vivas sem vigência declarada reprova.

---

### E4 — Silver completo em Postgres/PostGIS com vintage e modelo temporal (MIGRAÇÃO, não green-field)

**Estado real:** `oficiais.iptu2026_cedentes` (3.905, PK `sql_mestre`) e `oficiais.q14_valor_terreno_2025` (3.676, PK `(sq,codlog)`) já existem (migration `oficiais_camada_produto_tdc`, 2026-07-02), sem vintage e com o ano no NOME. Tarefa = MIGRAR tabela viva E tirar o ano do nome (o ano passa a viver na coluna/PK).

**E4-0 (migração das 2 vivas — bloqueia o resto):**
- (a) `ALTER TABLE`: `ano_exercicio`+`capturado_em`+`sha256` (IPTU); `vigencia_inicio`+`vigencia_fim`+`capturado_em`+`sha256` (Q14).
- (b) **Backfill determinístico da proveniência DOCUMENTADA, não da data do ALTER:** `PROVENIENCIA.md` linha 3 = "Extraídos em 2026-07-02". IPTU `ano_exercicio=2026`, `capturado_em='2026-07-02'`; Q14 `vigencia_inicio='2025-01-01'`, `vigencia_fim=NULL`, `capturado_em='2026-07-02'`. (Hoje já é 2026-07-03 — a data da migration gravaria o eixo errado.)
- (c) **Renomear removendo o ano dos DOIS lados:** `q14_valor_terreno_2025 → q14_valor_terreno` E `iptu2026_cedentes → iptu_cedentes`. Sem isso, IPTU_2027 exigiria criar `iptu2027_cedentes` (reescrita de tabela+código) em vez de `INSERT … ano_exercicio=2027`.
- (d) **PK do Q14 → `(sq,codlog,vigencia_inicio)`; do IPTU → `(sql_mestre, ano_exercicio)`**, via migration versionada.

**Cargas NOVAS (green-field — aqui o gate de capacidade se aplica):**
- **IPTU_2026 BRUTO → `oficiais.iptu_bruto`** (SEM ano no nome; ~3,92M linhas, `ano_exercicio=2026` na PK, `capturado_em`, `sha256`), com `pg_trgm` (GIN) no endereço rodando sobre ELA (não sobre o subconjunto de 3.905). Sem a bruta, E1b re-baixa 894 MB a cada run e o objetivo de casar `endereco_mestre` contra o IPTU completo (fechar os 1.839 sem SQL) fica inviável. IPTU_2027 = `INSERT … ano_exercicio=2027` na MESMA tabela.
- **817 shapefiles → `oficiais.lote_geom`** (geometria+vintage) e **`oficiais.zona_geom`** (polígonos + vigência), carga única (mata ~457 MB/run). Base pronta para o Motor 3.
- **`oficiais.zepec_bir`** (universo 6.131) com as datas por origem SEPARADAS (`data_declaracao_iso/data_certidao_iso/data_tombamento_iso`, nullable — E2 família 2c), nunca `data_ref=max()`.
- **`oficiais.quadro3_ca_zona`** (CA por zona com vigência).

**Modelo temporal por família:**
- **IPTU (exercício):** PK `(sql_mestre, ano_exercicio)` / `(<chave>, ano_exercicio)`; `ON CONFLICT DO UPDATE` aceitável.
- **Q14 e valores-vigentes-até-substituir (SCD-2):** PK `(sq,codlog,vigencia_inicio)`. **Idempotente com GUARDA:** antes de UPDATE+INSERT, `SELECT vigencia_inicio WHERE (sq,codlog)=… AND vigencia_fim IS NULL`; se o vigente for IGUAL ao vintage ingerido → NO-OP total; só quando o novo `vigencia_inicio` for estritamente POSTERIOR → `UPDATE … SET vigencia_fim=<novo> WHERE vigencia_fim IS NULL` + `INSERT … vigencia_fim=NULL`, NUNCA UPDATE do valor. Preserva o histórico que a Lei 16.050 Art. 128 §2º exige e que a carga inicial das duas vigências de Q14 (E6-fase-0 d) povoa.
- **ZEPEC-BIR:** as três datas são colunas nullable, não geram versão SCD-2.
- **`q14_max_face` REMOVIDO:** "pegar o máximo" é decisão de cálculo (15% dos V têm face até 6× mais cara na mesma quadra), viola 1.3 — é função citável do Motor 5.

**DoD mecânica:**
1. Após E4-0: `count(*)` bate 3.905 (`iptu_cedentes`) e 3.676 (`q14_valor_terreno`) agrupado por `ano_exercicio`/`vigencia_inicio` (só passa após backfill).
2. `capturado_em` das migradas = constante documentada `2026-07-02`, NÃO a data de aplicação da migration.
3. **IPTU bruto:** `count(*) ≈ 3,92M` com `ano_exercicio=2026`/`capturado_em`/`sha256`; GIN `pg_trgm` VÁLIDO sobre o endereço DELA (assert: consulta trgm retorna candidato para um SQL-alvo conhecido dos 1.839 sem SQL); nome sem ano (regex E6-DoD-3).
4. **Geometrias:** `count(*) FROM lote_geom / zona_geom > 0` com vintage+`sha256`, GIST válido. (zero-egress do overlay é DoD de E1b, não de E4.)
5. `zepec_bir` reflete o universo (coerente com 6.131) E tem as três colunas de data por origem, nenhuma agregação de datas de origens distintas gravada.
6. Q14 expõe todas as faces (assert: existe SQ com >1 codlog; nenhuma view pré-seleciona máximo) E contém as DUAS vigências para as chaves em comum.
7. **Idempotência SCD-2 com guarda:** ingerir o MESMO vintage 2x não duplica NEM move `vigencia_fim`; vintage NOVO fecha o anterior e insere 1 vigente. Assert por **comparação linha-a-linha de `vigencia_fim` antes/depois** (count idêntico mascara corrupção sob `ON CONFLICT DO NOTHING`).
8. **Gate de capacidade — disco E COMPUTE tier.** Verificado ao vivo (Pro, tier Micro ~1GB RAM): `maintenance_work_mem=32MB`, `shared_buffers=224MB`, `effective_cache_size=384MB`. Quatro condições:
   - (i) `pg_database_size` atual + estimativa pós-carga (3,92M do bruto + GIN trgm + GIST das geometrias) contra o disco do plano;
   - (ii) spend cap OU alerta de orçamento ligado antes de autorizar;
   - (iii) assert pós-carga dentro do incluído, OU custo de armazenamento (US$0,125/GB/mês) registrado como decisão;
   - (iv) **(CORRIGIDO — furo F4)** o custo de build de GIN/GIST NÃO extrapola linearmente: é DESCONTÍNUO no limiar de spill de `maintenance_work_mem`. Uma amostra de 5–10% pode construir inteiramente em memória (projeção linear otimista) enquanto o build completo cruza o regime de sort externo (horas/OOM). Portanto o gate NÃO usa extrapolação linear temporal de amostra in-memory: usa UM de dois critérios — **(a)** estimar o tamanho do conjunto de build de cada índice (GIN sobre ~3,92M endereços; GIST sobre `lote_geom`, 720 MB de `.shp` brutos → plausivelmente centenas de milhares a >1M polígonos) e disparar a decisão de upsize quando **estimativa > `maintenance_work_mem` do tier atual**; OU **(b)** construir numa amostra dimensionada para CRUZAR o `maintenance_work_mem` atual (observando de fato o regime de spill), nunca numa amostra que cabe em memória. Se qualquer critério indicar estouro, declarar EXPLICITAMENTE o upsize de compute tier ANTES da carga (não durante), com o custo mensal incremental registrado ao lado do spend cap de (ii). O gate prova "cabe em disco E o índice constrói nesse hardware". Sem os 4, E4 não fecha.

---

### E7 — Loaders idempotentes (folded no gate de E6-fase-1)

**O que faz:** todo loader roda 2x sem alterar contagens NEM histórico SCD-2.

**Por que:** E6 embute "loaders idempotentes"; a PROVA é E7 — funde-se ao DoD de E6-fase-1 (imediatamente antes, nunca depois), senão E6 se declara "feita" com um reset+load único que bate contagens sem provar 2x-idêntico.

**DoD mecânica:** cada loader 2x → `count(*)` idêntico por tabela; para SCD-2, 2x do mesmo vintage não cria linha nem move `vigencia_fim` (guarda SELECT-antes-de-UPDATE de E4), verificado por comparação linha-a-linha de `vigencia_fim` (count sozinho não pega destruição de histórico nem PK-collision mascarada).

---

### E6 (fase 1 — RECONSTRUTIBILIDADE, depois de E4/E7) — Banco reconstruível do git

**O que faz:** `db reset` + migrations reconciliadas (5 `.sql` + `zona_geom` nova + PK-SCD-2 do Q14 + renomeação/PK do IPTU) + loaders idempotentes reproduz as contagens; espelho `oficiais.*` não diverge do git — UMA política de canonicidade.

**DoD mecânica:** de banco zerado, `supabase db reset` + loaders → as 5 contagens de regressão + universo 6.131. Loaders 2x mantêm contagens + vigência SCD-2 (E7 aqui). `db diff` contra o vivo = vazio (espelho = git). Inclui a reconciliação de E6-fase-0 DoD-6: as duas vigências de Q14 numa única `oficiais.q14_valor_terreno`; `oodc.py` lê por vigência-na-data-do-fato-gerador; nenhuma `tabelas/*.csv` divergente alimenta cálculo.

---

### E5 — Canal único de upload + dedup por sha256 de CONTEÚDO + abort de multipart RECORRENTE

**O que faz:** unifica o upload num único canal `rclone` com manifesto versionado (`sha256`); remove duplicatas byte-idênticas com regra de sobrevivência determinística; guarda anti-duplicata; e aborta multipart uploads pendentes de forma CONTÍNUA.

**Correção de método:** os **40,6% / 330 MB** vieram de `metadata->>'eTag'` (158 grupos, 551 objetos / 813 MB do bucket geo). ETag de multipart tem sufixo `-N` e não é md5 de conteúdo → dois arquivos byte-idênticos por canais de chunk distinto têm ETags DIFERENTES (falso-negativo no cenário multi-canal que E5 existe para resolver). Logo: `hash` no DoD = **sha256 de CONTEÚDO, não ETag**.

**Correção de sobrevivência:** os grupos de duplicata incluem o nome canônico (`ZC.shp`) junto de variantes (`ZC (1).shp`, `ZC_84b9b6.shp`). `overlay_zona.py` resolve por NOME EXATO (`:38` `os.path.exists(DL/b+'.shp')`; `:68` `glob(SIRGAS_SHP_LOTES_*.shp)`) e PULA a zona/lote SILENCIOSAMENTE se o `.shp` esperado não existir. Se o dedup mantiver `ZC_84b9b6.shp` no lugar de `ZC.shp`, o assert "sem par de hash igual" passa VERDE mas a cobertura cai sem nenhum assert de contagem apontar a causa.

**Por que:** o runbook `rclone` de 1 comando nunca rodou; com 3 canais o bucket re-suja; e abort de multipart pontual re-suja com partes órfãs cobradas na próxima reconexão.

**DoD mecânica:**
1. Manifesto `sha256`-de-conteúdo versionado, populado por: (a) hash no cliente antes do upload dos NOVOS via o canal rclone único; (b) uma passada única de re-hash retroativo dos ~1,7 GB já no bucket (egress orçado uma vez) antes de ligar o guard. Documentar que 40,6%/330 MB é PISO por-ETag.
2. Guarda anti-duplicata rejeita hash já presente (2º upload do mesmo blob = no-op).
3. Pós-dedup: `GROUP BY sha256 HAVING count>1` = vazio.
4. **Regra de sobrevivência determinística e AUDITÁVEL:** por grupo de sha256, o sobrevivente é o nome que bate o padrão que o código committed já espera (chaves do `ZMAP` de `overlay_zona.py` + `SIRGAS_SHP_LOTES_*.shp` SEM sufixo `(N)`/hex). **Assert PÓS-dedup:** rodar `overlay_zona.py` (ou ao menos a lista de basenames esperados por `ZMAP` + o glob) contra o resultado, **falhando se qualquer arquivo que o overlay enxergava antes sumiu**.
5. **Abort de multipart como INVARIANTE CONTÍNUO:** os 2 multiparts órfãos de `oficiais/IPTU_2026.csv` (de `subir-grandes-colab.py`, boto3 multipart automático) só aparecem em `storage.s3_multipart_uploads`. DoD: `ListMultipartUploads` → `AbortMultipartUpload` para pendentes >24h rodando RECORRENTEMENTE (job em `consolidar.yml` ou cron dedicado), não faxina única (assert: a cada execução, nenhum pendente >24h sobrevive).

---

## 3. Prioridade interna

**E1a → E2 (incl. E2b canal `ano=`, E2c `tabelas/*.csv`, família 2c ZEPEC-BIR) → E3 → E6(fase 0: 5 migrations + criar `zona_geom` + fixar `oficiais.*` + carregar as DUAS vigências de Q14 no SCD-2) → E4(E4-0 migração+renomeação das 2 vivas → `iptu_bruto` + geometrias + demais cargas, gate de compute tier) → E1b → E7 → E6(fase 1: reconstrutibilidade) → E5.**

Racional da ordem: E1a entrega o runner determinístico e o input pinado (a tese do motor) sem depender do banco; E2/E3 fixam a semântica de vintage e a árvore antes de qualquer carga; E6-fase-0 reconcilia o schema para que E4 saiba onde escrever; E4 migra e carrega; E1b só então elimina egress; E7 prova idempotência dentro de E6-fase-1; E5 (limpeza de bucket) por último por ser o de menor risco à cadeia de produto.

**O que muda vs. v6:** integradas as 4 correções finais — (F1) E1 ganha input-pinning por sha256 antes do transform como parte do contrato de byte-identidade (o furo que fazia "reprodutível de checkout limpo" ser não-provado); (F2) E1-DoD-1 ganha o contrato de CWD (rodar de scratch-CWD ≠ raiz), pois grep de `/home` não pega bare-relative `open()`; (F3) E1-DoD-4 exige reprodução BYTE-a-byte do committed `iptu2026_cedentes.csv`, não só `count=3.905`, e o `filtro_iptu` reescrito passa a escrever no path canônico `zepec/oficial/` (hoje escreve `oficiais/cedentes_area_iptu.csv` — divergência de PATH/nome; o header já é idêntico, então a diagnose de "column contract diferente" é rejeitada); (F4) E4-DoD-8(iv) troca extrapolação linear de amostra in-memory por gatilho de `estimativa-de-build > maintenance_work_mem` ou amostra dimensionada para cruzar o spill.

---

## 4. Fronteiras (o que NÃO é deste motor)

- **Motor 1 (M-GATE):** o GATE que CHECA reprodutibilidade (byte-diff no CI, incl. estender `on.push.paths` de `consolidar.yml` para `engines/**` e `zepec/**`, hoje ausentes; pinar `ubuntu-24.04`/`.python-version` no workflow) = T2; PII/segurança = T7. M-DADOS torna reproduzível e PINA o input; M-GATE trava no CI. (Pinar o input é de M-DADOS; verificar o byte-diff é de M-GATE.)
- **Motor 3 (M-GEO):** overlay geométrico (`ST_Contains`/`ST_PointOnSurface`) e a resolução robusta de nome de shapefile no overlay; aqui só `oficiais.lote_geom`/`oficiais.zona_geom` base com vintage, loader idempotente e a regra de dedup que preserva os basenames que o overlay espera.
- **Motor 4 (M-JUR):** tabela dos 47 fatores e vigência de normas.
- **Motor 5 (M-CALC):** toda seleção de face do Q14 (max/média/faixa); a correção IPCA sobre o intervalo de vigência que E2/E4 EXPÕEM — incluindo decidir se a divergência ~1,17515× entre as duas vigências de Q14 é correção monetária (a base guarda os dois V brutos com vigência; M-CALC corrige — M-DADOS nunca escolhe o V, 1.3); e a escolha de QUAL das três datas ZEPEC-BIR exibir num campo único de apresentação, citando a origem (1.7).

**Rejeições explícitas (anti-gold-plating):** `q14_max_face` como view (decisão de cálculo disfarçada de infra, viola 1.3); codex/oráculo por camada medallion (cerimônia não-aplicada vira dívida — E3 é só path); governança/RLS além do que já roda (M-GATE/T7); reescrever `enriquecer_oficial.py` para alimentar `lista_prospeccao.py` sem a decisão do Passo 4b declarada (pode ser design intencional — 1 linha resolve); manter `dados.*`/`tabelas.*`/`geo.*` como destino paralelo a `oficiais.*` (o C-27 que o motor mata); escolher em M-DADOS qual V de Q14 é "o certo" ou APOSENTAR a vigência histórica (viola 1.6 e "nada se joga fora"); colapsar as três datas ZEPEC-BIR num único `data_ref` no Silver. Também rejeitada a diagnose F3 de "column contract divergente" — os headers são byte-idênticos; a divergência real é de path/nome, e o remédio byte-a-byte é adotado assim mesmo.

---

## 5. O que fica pronto quando o motor fecha

1. **A cadeia inteira roda de um `git clean -fdx` e é byte-idêntica em re-execução — inclusive o input:** todo objeto Bronze é verificado por sha256 contra o manifesto ANTES de transformar; sem `/tmp`, sem path absoluto, sem dependência de CWD; colunas do IPTU resolvidas por NOME com abort; `filtro_iptu` reescrito reproduz o artefato committed byte-a-byte; ambiente (pip+Python+imagem) pinado.
2. **Todo dado tem vintage:** path Bronze `oficiais/<fonte>/ano=<AAAA>/`; coluna Silver por família (exercício / intervalo SCD-2 / datas-por-origem); manifesto sha256; loader recusa carga sem vintage; o canal físico de upload emite `ano=`; `tabelas/*.csv` dentro do escopo.
3. **UMA árvore canônica (`oficiais.*`) reconstruível do git:** 5 migrations vivas commitadas + as novas (`zona_geom`, PK-SCD-2 do Q14, renomeação/PK do IPTU); `db reset` + loaders idempotentes reproduz as 5 contagens (3.905/3.676/3.693/3.014/2.937) + universo 6.131; `db diff` vazio; nenhum nome de tabela com ano embutido.
4. **IPTU_2026 bruto (~3,92M), Q14 (duas vigências), 817 geometrias e o universo ZEPEC-BIR carregados em Postgres/PostGIS com vintage**, índices GIN/GIST válidos construídos dentro de um compute tier explicitamente dimensionado (ou upsize declarado e orçado ANTES da carga) — matando o re-stream de 894 MB + 457 MB por run em E1b.
5. **Bucket dedup por sha256 de conteúdo**, canal único rclone com guarda anti-duplicata, sobrevivência de arquivo que preserva os basenames que o overlay espera, e abort de multipart órfão como invariante contínuo.
6. **Cada uma das afirmações acima é um assert mecânico que já rodou contra o repo vivo** — nenhuma é prosa: o motor entrega o substrato onde "declarei feito != provei feito" vale de ponta a ponta, e sobre o qual os Motores 3/4/5 assentam. Zero resíduo de comprador/matching.