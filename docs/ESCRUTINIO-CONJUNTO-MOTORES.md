# ESCRUTÍNIO CONJUNTO — Motores 1 / 2 / 3 + Google Drive

> 2026-07-03. Painel de 6 lentes (3 de costura entre motores, Opus; 3 de reconciliação do Drive, Sonnet) → **48 achados** → síntese Opus → **crítica adversarial Opus**.

## Veredito reconciliado (o que vale, depois da crítica)

A crítica adversarial confirmou o relatório como **~80% sólido na camada factual** (schema vivo do Supabase, inventário do Drive e diagnóstico de CI conferem), mas apontou que a **cadeia de vedação Art.124§2 (S3 / C1 / C2 / C3 / C7 / S5) repousa num ANCHOR DE ARQUIVO ERRADO e inverte uma posição já resolvida do Motor 1**. Portanto:

**VALE (seguir):** as reconciliações de INFRA —
- **S1 · Crise de canonicidade do schema** (migrations vivas `oficiais.*` sem `.sql` no git; migrations do git `dados.*/geo.*/tabelas.*` nunca aplicadas). Confirmado ao vivo.
- **S2 · "Declarei ≠ provei" no CI** (`consolidar.yml` não cobre `zepec/**`,`engines/**`,`tabelas/**`,`supabase/**`; sem pip, sem PostGIS, sem Supabase no runner).
- **S4 · SSOT de proveniência/vigência fragmentado** (`governanca.de_para` vivo, RLS ON, **0 linhas**, desenhado para 1.6/D-DONO-4 e ignorado; 414 arquivos geo baixados sem `PROVENIENCIA`).
- **Reconciliação do Drive (direção):** os shapefiles oficiais e listas ZEPEC-BIR existem e devem ser ingeridos com proveniência; `SIRGAS_SHP_LOTES` oficiais substituem os `LOTES_*_IA.csv` nossos.

**CORRIGIR antes de implementar (4 reparos da crítica — a cadeia de vedação):**
1. **Anchor errado:** a coluna `cessao_vedada_art124p2` é produzida em `montar_base.py:104` e consumida em `montar_ferramenta.py:119` — **nunca** em `enriquecer_oficial.py:78-98` (esse é o bloco do engine de preço). C1/C2/C3 herdam o anchor errado.
2. **NÃO aposentar o substring** em `bp_categor` como fonte: ele fica como *propagação* (consistência provada); a geometria AUE/APPa é gate ADITIVO de *completude* fail-closed (posição já endurecida do M1; aposentá-lo seria regressão de 1.5/1.7 e remoção do fail-closed).
3. **Não materializar o carimbo em Postgres** (`oficiais.vedacao_aue_appa` é tabela inventada): manter o discriminante path+hash em `zepec/raw/` que o pipeline CSV-first de M1 e M3 consegue ler.
4. **Preservar a separação** CONFLITO (4 SQLs, `negociavel='verificar'`) ≠ puro-vedado (32, `negociavel='nao'`) — são dois ramos legítimos do mesmo flag, não "um erro".

**Também corrigir:** S5 superdimensiona a prontidão — enumerar `ZEPEC_AUE`/`APP-BIR` no `ZMAP` de `overlay_zona.py` **não** é um consumidor de vedação (o overlay resolve 1 zona/lote e des-prioriza selos sem CA); o overlay N:N do G2 ainda precisa ser construído. E a fronteira de fase do passo de CI (D6) deve ser: posse do `consolidar.yml` (F0) → E1/G0 entregam scripts+specs (F1) → integrar e esverdear o CI (fim da F1), nunca F0.

---

## Relatório consolidado (as 6 lentes)

# RELATÓRIO CONSOLIDADO — Escrutínio Conjunto dos Motores 1/2/3 + Google Drive
Potencial Urbano · lado cedente · só-tombado (ZEPEC-BIR já declarada) · 2026-07-03

---

## 1. VISÃO DO TODO — os problemas sistêmicos

Os 48 achados das 6 lentes colapsam em **cinco doenças** que atravessam os três motores. Nenhuma é de um motor só; todas nascem de fronteiras mal costuradas.

**S1 — Crise de canonicidade do schema Postgres (três fontes-de-verdade disjuntas, e o NÚMERO vem da não-governada).**
Verificado ao vivo (projeto `csnalylpvysjvejgsymr`): existem apenas `oficiais.iptu2026_cedentes` (3.905), `oficiais.q14_valor_terreno_2025` (3.676), `governanca.*` e `public.spatial_ref_sys`. As 3 migrations do git (`20260624_010/020/030`, que criam `dados.*`, `geo.lote`, `tabelas.v_feed_alvos`) **nunca foram aplicadas**; as 5 vivas **não têm `.sql` no git**. Pior: o número in-scope não vem de nenhum dos dois — `enriquecer_oficial.py` lê CSVs planos (`oficial/iptu2026_cedentes.csv`, `oficial/q14_cedentes_2025.csv`, `zona_por_cedente.csv`, `ferramenta/zepec_cedentes.csv`) e **não toca Postgres**. Os três motores pisam nesse schema quebrado com destinos incompatíveis: M2/E6 canoniza `oficiais.*` e quer DROPar `geo.*`; M3/G5 quer materializar `geo.lote_zona`; M1/T7 faz probe anon contra `dados.*`/`tabelas.v_feed_alvos` (fantasmas). (Achados 4, 9, 10, 13, 18, 34.)

**S2 — "Declarei ≠ provei" institucionalizado no CI: o gate não enxerga nem o número nem o banco.**
`.github/workflows/consolidar.yml` roda só scripts stdlib (`fatiar`/`indexar`/`consolidar`/`rodar-evals`/`oodc`), com `on.push.paths` cobrindo `leis/jurisprudencia/scripts/evals/rag` — **não** `zepec/**`, `engines/**`, `tabelas/**`, `supabase/**`; sem `pip install`, sem service PostGIS, sem conexão Supabase. Consequência transversal: TODA DoD dos três motores que promete "assert em `eval-produto.py`", "`rodar-eval-geo.py`", "probe anon do T7" ou "diff no CSV oficial" asserta contra um harness e uma conexão **que hoje não existem no runner**. Cada motor diagnostica sua fatia (M1/T2, M2/E1, M3/G0-G6) mas nenhum é dono único do passo que conecta o gate ao produto e ao banco. (Achados 6, 7, 8, 15, 20.)

**S3 — `enriquecer_oficial.py` é o mestre compartilhado que três motores editam em paralelo (viola 1.5).**
É o único gate de preço, e M1 + M3 querem escrever a MESMA vedação Art.124§2 no MESMO bloco (linhas 78-98) com **colunas, fontes e escopos diferentes**: M1/T8 → `cessao_vedada_art124p2` (substring em `bp_categor`, escopo "4 SQLs"); M3/G2b → `flag_tdc_vedado_art124_par2` (overlay N:N + `motivo_negociavel`, escopo "32 linhas"). Os dois conjuntos-alvo são **disjuntos e ambos mal-diagnosticados** contra o dado (as 32 já têm `negociavel='nao'`; os 4 têm `motivo` VAZIO). Além disso o fail-closed de M1 é só-PREÇO: nas 32 linhas AUE/APPa, `pcpt_m2`/`saldo`/`ca_basico` continuam fabricados (linhas 82/91 calculam antes do gate). Guard duplo, colunas redundantes, falso-verde na costura M1↔M5. (Achados 1, 2, 3, 11, 17.)

**S4 — Fragmentação do SSOT de proveniência/vigência (a mesma doença de canonicidade, na camada de metadado).**
Existe `governanca.de_para` VIVO (RLS ON, 0 linhas) com exatamente as colunas de 1.6 + D-DONO-4 (`drive_id, vigencia_inicio/fim, substitui/substituido_por, proveniencia, oficialidade, confianca`) — desenhado para isto e **ignorado**. Cada motor inventa o seu: M1 usa `MANIFESTO.json`, M2 propõe manifesto sha256 novo, M3 usa `funil.csv`. E o pull de **414 arquivos geo** já baixados (`.../scratchpad/geo/dl`: 96 distritos SIRGAS_LOTES + 43 zonas + 7 ZEPEC) **não tem nenhum PROVENIENCIA.md** — viola 1.5/1.6 e some quando o scratchpad reciclar. (Achados 14, 28, 30, 40, 46, 48.)

**S5 — A premissa D1 ("vedação AUE/APPa inconstruível do dado presente") caiu: o dado sempre esteve no Drive e o consumidor já foi escrito.**
`ZEPEC_AUE.shp` (fileId `1gYeb5cYlFgVlYt87VZhCSFgdja4njttK`, 1.683.820 B) e `ZEPEC_APP-BIR.shp` (`1nSJNIe4lhxSGAuVgdY2bMbr0pkLyoQbN`) são oficiais (GeoSampa/CONPRESP), `overlay_zona.py` já os enumera no `ZMAP` (L22-24) e já estão baixados. D1 é verdadeiro só para o **repo de hoje** — é lacuna de ingestão Drive→repo que cai ENTRE M2 e M3. Mas o flip `PENDENTE-VEDACAO→RESOLVIDO` de M1/T8-DoD9c espera um artefato em `zepec/raw/` que **nenhum motor entrega** (M3 escreve em `DL`/`zona_por_cedente.csv`, nunca em `zepec/raw/`, nem emite carimbo M-GEO). Sem costura, o caveat `completude_vedacao=PENDENTE_M-GEO` é permanente. (Achados 5, 12, 16, 24, 32, 39.)

**Transversal de escopo (dono, 2026-07-03):** sobrevivem planos RECEPTOR que re-envenenam schema e dado — PD-3 citywide (`ROADMAP-PU.md` L154/266/347 → `geo.lote_zona` da cidade inteira), `v_feed_alvos`/`gerar_alvos.py`/`oodc.py`, e `LOTES_*_IA.csv` (NOSSO, proibido por D-DONO-4). O código vivo já se autocorrigiu (overlay lê SIRGAS oficial; `subir-grandes-colab.py:31` comenta o `_IA`), mas os docs e a migration órfã ainda os consagram. (Achados 22, 33, 34, 41.)

---

## 2. COSTURAS ENTRE MOTORES — contradições, sobreposições, lacunas

| # | Tipo | Motores | O conflito (verificado) | Ação de reconciliação (uma vez) | Dono |
|---|---|---|---|---|---|
| C1 | Sobreposição | M1/T8 · M3/G2b | Vedação Art.124§2 escrita 2× no mesmo bloco de `enriquecer_oficial.py:78-98`, 2 colunas/2 fontes/2 escopos | **UMA coluna booleana** de vedação, alimentada pelo overlay N:N de M3, consumida pelo gate de M1. Aposentar a derivação por substring `bp_categor` como FONTE de vedação. | M3 produz a coluna; M1 consome |
| C2 | Falso-verde | M1/T8 · M3/G2b · M5 | Fail-closed de M1 é só-preço; `pcpt_m2`/`saldo`/`ca_basico` seguem fabricados nas 32 vedadas e fluem p/ M5 | Mover o guard de vedação para **ANTES** do bloco atc/cabas (linha 79), zerando os intermediários; assert de M1 exige `pcpt_m2`/`saldo`/`ca_basico` VAZIOS, não só `preco=0` | M3 escreve o guard; M1 amplia o assert |
| C3 | Diagnóstico errado | M1/T8 · M3/G2b | Conjuntos-alvo disjuntos e ambos falsos: 4 SQLs de M1 têm `motivo` VAZIO; 32 de M3 já são `negociavel='nao'` | Predicado único que cobre AMBOS os sinais (`bp_categor` E `motivo_negociavel` E overlay N:N); assert de cobertura cruzada 32+4 | M3 (define população) |
| C4 | Contradição de DoD | M2/E6 · M3/G5 | M2 asserta "grep por `geo.` = vazio" (DROP `geo.*`); M3 constrói `geo.lote_zona` dentro de `geo.*` | M3/G5 materializa em **`oficiais.zona_geom`/`oficiais.lote_geom`** (alvo que M2/E4 já cria). Uma decisão de schema registrada antes de qualquer migration PostGIS | M2 fixa o schema; M3 mira nele |
| C5 | Três casas p/ geometria | M2/E4 · M3/G5 · migration órfã | `oficiais.lote_geom` (M2) vs `geo.lote_zona` (M3) vs `geo.lote` (git órfão, coluna única `.zona`) | Casa única = `oficiais.*`; a granularidade por feição/`ST_Subdivide` (M3) e a migration `zona_geom` (M2) são a MESMA entrega | M2 dono da migration; M3 spec de SRID/granularidade |
| C6 | Premissa falsa contra produção | M3/G5 | G5 diz "produção lê `geo.lote.zona` via `v_feed_alvos`" — nenhum dos dois existe vivo; caminho cedente é CSV | Corrigir o texto de premissa de G5: produção é CSV plano; `v_feed_alvos` é RECEPTOR fora de escopo | M3 (retificar) |
| C7 | Lacuna-entre-motores | M1/T8-DoD9c · M2/E4 · M3/G2 | Flip espera artefato em `zepec/raw/`; M3 escreve em `DL`, M2 em `oficiais.*` — ninguém alimenta `zepec/raw/` nem carimba | Definir o "carimbo M-GEO" = tabela independente **`oficiais.vedacao_aue_appa`** (sql_mestre+veredicto+hash) produzida por G2 do overlay ZEPEC_AUE/APP-BIR; M1 aponta o flip para ela | M3 produz+carimba; M1 lê |
| C8 | Sub-check ausente | M1/T8-DoD9c · M3 | O discriminante do flip só olha path/hash do arquivo AUE/APPa; se a malha de lotes for `_IA`, o carimbo passa com geocode proibido | Sub-check mecânico: carimbo só válido se a camada de lotes na interseção for **SIRGAS_SHP_LOTES oficial**, nunca `LOTES_*_IA.csv` (registrar hash/nome na proveniência) | M1 (endurecer critério) |
| C9 | Cadeia não regenera | M1/T2 · M2/E1 | T2 checa reprodutibilidade de cadeia que E1 não regenera: `recorte_q14.py` não existe; `filtro_iptu.py` escreve path errado; `overlay_zona.py` DL hardcoded | E1 commita `recorte_q14.py`, corrige path de `filtro_iptu.py`→`zepec/oficial/iptu2026_cedentes.csv`, parametriza `DL`; só então o byte-diff de T2 não é vácuo | M2 (E1) |
| C10 | Mestre editado por 3 | M1/T2 · M2/E1 · M3/G0-G6 | `consolidar.yml`: M1 quer tirar `paths`, M3 quer adicionar `zepec/**`+pip+PostGIS, M2 quer pin `3.11.9`/`ubuntu-24.04` — provisionamento sem dono | **Dono único = M1/T2.** M2 e M3 entregam ESPEC (`requirements-geo.txt`, pins, scripts); M1 integra num patch: paths ⊇ `zepec/**`+`engines/**`+`tabelas/**`+`supabase/**`, pip, service PostGIS, URL+anon-key Supabase p/ probe T7 | M1 |
| C11 | Dupla-cobertura de eval | M1/T2 · M3/G6 · M4 | `eval-produto.py` e `rodar-eval-geo.py` (ambos inexistentes) rodam o mesmo `enriquecer_oficial.py`; geo-json em `evals/ground-truth/` quebra o gate RAG | Fronteira explícita de asserts; ground-truth geo vai p/ `evals/ground-truth-geo/` (fora do glob de `rodar-evals.py`) | M3 (harness geo); M1 (harness produto) |
| C12 | Probe contra fantasma | M1/T7 · M2 | T7 faz `SELECT anon` contra `dados.iptu_2026`/`dados.socios`/`v_feed_alvos` (inexistentes → verde vácuo); a tabela viva com quasi-PII fica fora | Repontar o probe p/ `oficiais.iptu2026_cedentes(endereco)` (RLS ON, policy a confirmar) + storage buckets | M1 (T7) |
| C13 | Dupla parametrização | M2/E1 · M3/G0 | E1 e G0 ambos parametrizam `overlay_zona.py` DL e `gerar_xlsx.py` OUT, ambos criam requirements com shapely/pyshp | Um dono por arquivo: camada geo (`overlay_zona.py`, requirements-geo) é de M3/G0; E1 CONSOME. UM requirements | M3 (geo); M2 consome |
| C14 | Path gerador≠consumido | M2/E1 · M1/M3 | `filtro_iptu.py` escreve `oficiais/cedentes_area_iptu.csv`; a cadeia lê `zepec/oficial/iptu2026_cedentes.csv` (header byte-idêntico) | E1 reescreve o `dest` p/ o path canônico + prova byte-a-byte (E1-DoD-4) | M2 (E1) |
| C15 | SSOT paralelo | M1 · M2 · M3 | 3 mecanismos de proveniência (`MANIFESTO.json`, manifesto sha256 novo, `funil.csv`) ignoram `governanca.de_para` vivo | Decidir: `de_para` é o SSOT (popular do `drive_inventario.md` com sha256/oficialidade; DoDs de vintage leem/escrevem nela) OU declará-la aposentada. Não criar um 4º | M2 (dono de schema) com aval do dono |

---

## 3. RECONCILIAÇÃO DO DRIVE — ativo × motor × categoria × ação

Categorias: **PL** = preenche-lacuna · **MV** = melhor-visão · **SF** = substitui-fonte-fraca · **CF** = conflito/derruba-premissa.

| Ativo (fileId) | Proveniência | Motor | Cat. | Ação |
|---|---|---|---|---|
| **ZEPEC_AUE.shp** `1gYeb5cYlFgVlYt87VZhCSFgdja4njttK` | OFICIAL GeoSampa/CONPRESP | M1·M3 | **CF** | **Derruba D1.** Ingerir em local persistente (`zepec/raw/geo/` ou `oficiais.*`) com fileId+hash; overlay N:N de G2 produz `oficiais.vedacao_aue_appa`; carimbo do flip de M1 aponta p/ ela |
| **ZEPEC_APP-BIR.shp** `1nSJNIe4lhxSGAuVgdY2bMbr0pkLyoQbN` | OFICIAL (APP sobre BIR) | M1·M3 | **CF** | Idem — é literalmente a camada de vedação Art.124§2 que D1 dizia faltar |
| **414 arquivos geo já em `scratchpad/geo/dl`** (96 SIRGAS_LOTES + 43 zonas + 7 ZEPEC) | OFICIAL, baixados nesta sessão | M3 | **PL/CF** | **URGENTE:** gerar `zepec/pipeline/PROVENIENCIA-GEO.md` (fileId+checksum cruzado com inventário) e mover p/ local versionado ANTES do scratchpad reciclar; fecha G0 com dado que já existe |
| **SIRGAS_SHP_LOTES_NN_<distrito>** (96 distritos; ex. 70_SANTANA `1vjYfo976BeZOAO893iMIv3dWafjbNXcE`) | OFICIAL GeoSampa | M3 | **SF** | Fonte de lote = SIRGAS oficial; nunca `LOTES_*_IA.csv`. Código vivo já usa; **formalizar** com assert G0 "nenhum script lê `_IA`" |
| **IPTU_2026.csv** `1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM` (~937 MB) | OFICIAL PMSP | M2 | **PL** | Já referenciado em `subir-grandes-colab.py:28`. Carregar `oficiais.iptu_bruto` (E4) **após** gerar os 5 .sql (E6-fase-0), não repetir "aplicado sem .sql no git" |
| **Q14 vigente** `1Q499wCFws3H1d3w0jY1PFYOkCD5PjieF` + **histórica** `1KPeSlCXVtWyuFr52gr0Wg4uzPqymbVaD` | OFICIAL PDE/SMUL | M2 | **PL** | Já em `subir-oficiais-para-supabase.gs:22-23`. Carregar AMBAS vigências em `oficiais.q14_valor_terreno` (SCD-2). **Faltam no `drive_inventario.md`** — corrigir o inventário |
| **SIRGAS_SHP_planomacro** (macrozonas/macroáreas; catalogado em `inventario/camadas-geo.md`) | OFICIAL GeoSampa | M3·M2 | **PL** | **Peça que falta p/ os 77 ZOE.** Ingerir + segundo overlay lote→macroárea → `macroarea_por_lote`; só então `flag_zoe_aguardando_quadro2a` cai (junto com Quadro 2A) |
| **Quadro 2A** já em `_entrada/tdc/pde2013-subst2-quadro-2a-ca-macroareas.txt` (`1D0bge5O8yc60b8pHV4foQSrXF1kuw-Ax`) | OFICIAL, extraído verbatim | M3·M2 | **PL** | Rodar Etapa 3 (extração pura) → `tabelas/quadro2a-ca-macroarea.csv`; combina com planomacro p/ CA de ZOE |
| **SIRGAS_SHP_logradouronbl** `118bVYfXP9mpu8VIbm_4qBazI4fQfcFWG` (30,8 MB) | OFICIAL GeoSampa | M3·M4 | **PL** | Matéria-prima da adjacência lote-face (FURO#1 de G4). Reenquadra o bloqueio de "fonte inexistente" p/ "engenharia de interseção" — não desbloqueia MAX sozinho (falta Decreto verbatim) |
| **SIRGAS_SHP_setorfiscal** `1Cu7SIG_gxzk9ItsmT0dv2qYDDIrh5Ps1` + **quadraMDSF** `1VdbAkuqv3p_yKX_rO_ZUzGw5MOfVsxOo` | OFICIAL GeoSampa | M2·M3 | **PL** | Chave de join geo↔IPTU oficial; ingerir junto de G0; usar em G3a e como âncora da decisão de schema `oficiais.lote_geom` |
| **benstombados.shp** `1WpeKCsz2EcovMBUVOJH79OPE39iWNDeD` (2,54 MB) | OFICIAL GeoSampa | M3·M1 | **MV/CF** | fileId diverge do CSV commitado (`151Rwikuh2bBi4DAvi5v6KSjYE2lEr5eX`, `PROVENIENCIA.md`). **Reconciliar hash/contagem** antes de confiar; a CSV de atributos já serve de cross-check das listas ZEPEC-BIR |
| **ZEPEC_BIR.shp** `1SMJ5NlYfloTSOKt_PwwI618OToAKZQUk` + **ZEPEC_BIR_INDIC.shp** `1X0muNAcafJYXqb52GsI5Jn69gSnQ_Arc` | OFICIAL GeoSampa | M3·M1 | **MV** | Não bloqueiam trava atual (T8-DoD1 resolve o positivo por evidência). Backlog M-GEO p/ cross-check de falso-positivo de enquadramento |
| **lista_declaracoes** `17j94xkgVk4eberaRpRLK2j_ekz480Lny` + **lista_certidao** `1en2WC2A-Wd21NNDhZ8ThheAyHmODIOl-` (ago-2025) | OFICIAL SMUL/DEUSO | M1·M2 | **(já ingerido)** | `PROVENIENCIA.md` bate fileId-a-fileId. Nenhuma ingestão nova; **confirmar vintage** (nenhuma lista mais nova) como parte do gate T3/T4 |
| **LOTES_Parte_1..5_IA.csv** `1EyzQ9O6…`…`1zQeOweW…` | NOSSO (`_IA`) | M3 | **(proibido)** | D-DONO-4: **nunca usar**. Manter comentado em `subir-grandes-colab.py:31`; atualizar docs/inventários que ainda os listam sem ressalva |
| **iptu-2020-cep01.csv** `1AV8v4esuCxGulgxvGskzo595vycDa3U-` | OFICIAL PMSP (2020) | M2 | **MV** | Fora de escopo atual (Fase B/P6); não ingerir agora |
| **Decreto 57.536/2016** | **NÃO está no Drive** | M1/T10·M4 | **lacuna real** | Reconciliação Drive NÃO resolve. Abrir dependência M-JUR p/ buscar em portal de legislação municipal SP; T10 segue PENDENTE-RENOVAÇÃO |
| **governanca.de_para** (vivo, vazio) | Supabase | M1·M2·M3 | **PL** | Popular do `drive_inventario.md` como SSOT de proveniência/vigência, OU aposentar — não criar 4º manifesto |

---

## 4. ORDEM CORRETA CROSS-MOTOR — caminho crítico mínimo

O erro de sequenciamento que os três motores cometem é **começar o retrabalho antes de reconciliar o schema e ingerir as fontes certas**. A ordem abaixo faz cada reconciliação UMA vez, na frente do trabalho que ela destrava.

**Fase 0 — Decisões de fronteira (sem código de produto; destravam tudo):**
1. **Dono confirma escopo RECEPTOR fora** (`gerar_alvos.py`, `v_feed_alvos`, `oodc.py`, PD-3 citywide, `LOTES_*_IA`). Sem dado real em risco (tabelas órfãs vazias). → torna seguro o DROP de `geo.*`/`dados.*`/`tabelas.*` e corta metade dos conflitos de schema.
2. **M2/E6-fase-0 fixa a árvore canônica:** `supabase db pull` gera os 5 `.sql` vivos; fixa `oficiais.*` como Silver; DROP dos 3 órfãos; cria `oficiais.zona_geom`/`oficiais.lote_geom`. → resolve C4/C5/C6; dá a M3 a casa de geometria; dá a M1/T7 o alvo real do probe (C12).
3. **Decisão de SSOT de proveniência:** `governanca.de_para` é o registro (ou aposentada). **Em paralelo e URGENTE:** `PROVENIENCIA-GEO.md` dos 414 arquivos antes do scratchpad reciclar (S4).
4. **Contrato de coluna de vedação único** (C1): um nome, fonte = overlay N:N de M3, consumido pelo gate de M1; o guard mora ANTES do bloco atc/cabas (C2); o "carimbo M-GEO" = `oficiais.vedacao_aue_appa` (C7), com sub-check de lote SIRGAS oficial (C8).
5. **M1/T2 vira dono único do `consolidar.yml`** (C10): paths ⊇ `zepec/**`+`engines/**`+`tabelas/**`+`supabase/**`; pip (requirements unificado); service PostGIS; URL+anon-key Supabase. Sem isso os harnesses de prova dos 3 motores são decorativos (S2).

**Fase 1 — Ingestão determinística das fontes certas do Drive (antes de qualquer overlay/carga):**
6. Ingerir com hash pinado: ZEPEC_AUE + ZEPEC_APP-BIR + SIRGAS_LOTES (96) + planomacro + logradouronbl + setorfiscal/quadraMDSF; reconciliar hash de `benstombados`. Normalizar basenames (strip `_hash`/"Cópia de") p/ casar `ZMAP`/glob (achado 36).
7. **M2/E1 fecha a cadeia reprodutível:** commita `recorte_q14.py`, corrige path de `filtro_iptu.py` (C14), parametriza `DL`/`OUT` (dono = M3/G0, C13); prova byte-a-byte. → só agora o byte-diff de T2 não é vácuo (C9).
8. **M2/E4** carrega `oficiais.iptu_bruto`, as duas vigências de Q14 (SCD-2), geometrias em `oficiais.lote_geom`/`zona_geom` — dentro do gate de compute tier.

**Fase 2 — Retrabalho de produto (agora barato e provável):**
9. M3: G1 (overlay por área confinado a `in_q3`) → G2 (454 sob selo, vedação por varredura universal com o guard no arquivo/coluna certos, exceção dual) → produz `oficiais.vedacao_aue_appa` e as flags.
10. M1: gate positivo/negativo de T8 consome a coluna única; T3/T4/T9/T10/T11 sobre a saída; T2 congela o golden SEM-PII e liga os três nets no CI.
11. M3/G6 + M1/T2: evals (produto + geo, harness separados) mordem no gate já provisionado.

---

## 5. O QUE MUDA EM CADA MOTOR

**Motor 1 (Travas / M-GATE):**
- **Para de ser dono da vedação como FONTE.** A coluna de vedação Art.124§2 passa a ser CONSUMIDA (produzida pelo overlay N:N de M3), não derivada de substring `bp_categor`. O assert de T8 exige `pcpt_m2`/`saldo`/`ca_basico` VAZIOS nas vedadas, não só `preco=0` (fecha o falso-verde M1↔M5).
- **O flip PENDENTE-VEDACAO ganha produtor real:** aponta para `oficiais.vedacao_aue_appa` (carimbo M-GEO), com sub-check de que a interseção usou SIRGAS oficial — não um path em `zepec/raw/` que ninguém alimenta. A premissa D1 é retratada: a vedação é COMPUTÁVEL hoje (geometria no Drive/repo), o que faltava era ingestão + separação selo≠zona-base.
- **T7 repontado para o schema vivo** (`oficiais.iptu2026_cedentes(endereco)` + buckets), não para `dados.*`/`v_feed_alvos` fantasmas; e assume ser **dono único do `consolidar.yml`** (paths + provisionamento + injeção de credencial Supabase).

**Motor 2 (Dados / Infra / M-DADOS):**
- **E6-fase-0 é pré-requisito, não paralelo:** gera os 5 `.sql`, fixa `oficiais.*`, DROP de `geo.*`/`dados.*`/`tabelas.*`, cria `oficiais.zona_geom`/`lote_geom` — a decisão de schema que destrava M3/G5 e M1/T7. Declarar explicitamente que a árvore canônica **não cobre o número in-scope hoje** (que vem de CSV) e escolher: puxar os 3 CSVs p/ `oficiais.*` OU declará-los Gold canônico com gerador versionado + sha256.
- **E1 fecha a cadeia que T2 vai checar:** commita `recorte_q14.py`, corrige o path de `filtro_iptu.py`, cede a camada geo (`overlay_zona.py`/requirements) para M3 e apenas consome. As fontes do Drive (IPTU/Q14/geo) já foram achadas — a lacuna é carga determinística, não descoberta.
- **Reconcilia proveniência:** decidir `governanca.de_para` como SSOT (ou aposentar); corrigir `drive_inventario.md` (Q14/IPTU faltantes); emitir `ano=` no path Bronze antes da próxima carga.

**Motor 3 (Espacial / M-GEO):**
- **Materializa em `oficiais.*`, não em `geo.*`:** abandona `geo.lote_zona`/`geo.lote`; o FK-placeholder de ZOE/ZEP aponta p/ a tabela de CA canônica de `oficiais.*`. G5 opcional (PostGIS) mira o alvo que M2/E4 já cria.
- **É a fonte da coluna única de vedação** (produz `oficiais.vedacao_aue_appa` do overlay ZEPEC_AUE/APP-BIR) e o guard de G2b mora em `enriquecer_oficial.py` numa passada sequenciada com o gate de M1 — nunca duas instâncias no mesmo bloco.
- **Persiste o que já baixou:** `PROVENIENCIA-GEO.md` dos 414 arquivos (URGENTE); ingere planomacro (77 ZOE), logradouronbl (adjacência de G4), setorfiscal/quadraMDSF; ground-truth geo vai p/ `evals/ground-truth-geo/` para não quebrar o gate RAG.

---

## Crítica adversarial (íntegra)

I have verified enough against the live repo, the live Supabase, and the three source strategies. Here is my adversarial verdict.

---

# CRÍTICA ADVERSARIAL — Escrutínio conjunto Motores 1/2/3 + Drive

O relatório está **~80% sólido na camada factual** (o esquema vivo do Supabase, o inventário do Drive e o diagnóstico de CI conferem), mas a sua **espinha dorsal — as costuras S3/C1/C2/C3 sobre a vedação Art.124§2 — repousa num anchor de arquivo ERRADO**, e a reconciliação proposta **inverte uma posição do Motor 1 que já estava resolvida e endurecida**. Esses dois defeitos contaminam a Fase 2 do caminho crítico. Detalho os que ainda importam, ranqueados.

## DEFEITOS QUE AINDA IMPORTAM

**D1 [grave — anchor factual falso]. A vedação NÃO é "escrita 2× no mesmo bloco de `enriquecer_oficial.py:78-98`" (S3, C1).**
Verificado no código: a coluna de M1 `cessao_vedada_art124p2` é PRODUZIDA em `montar_base.py:104` (`cessao_vedada(cat)` — substring em `categoria`/`bp_categor` de `benstombados1.csv`) e CONSUMIDA em `montar_ferramenta.py:119`. Ela **nunca aparece em `enriquecer_oficial.py`**. As linhas 78-98 de `enriquecer_oficial.py` são o **bloco do ENGINE de PCpt/preço**; a única interação com vedação ali é ler `negociavel`/`esgotado` (L81 `vendido_bloqueado`) para gatear PREÇO. Não existe "mesmo bloco, duas colunas escritas 2×". O ponto real de coordenação em `enriquecer_oficial.py` é outro (M1 quer o price-gate chaveado na coluna propagada; M3 quer ADICIONAR um guard+flag acima do engine) — é read-vs-write em estágios diferentes do pipeline, não a colisão que o relatório descreve. Como C1/C2/C3 herdam esse anchor, a "reconciliação de uma coluna única no bloco 78-98" está mal-endereçada.

**D2 [grave — inverte posição já resolvida do Motor 1; regressão de doutrina].** O relatório prescreve (C1, S5, §5): *"M1 para de ser dono da vedação como FONTE… a coluna passa a ser produzida pelo overlay N:N de M3… aposentar a derivação por substring `bp_categor` como FONTE."* Isso **inverte a posição explícita e já endurecida do Motor 1** (motor1 §§ item 4, 9c, e hand-off M-GEO): o substring-em-`bp_categor` **PERMANECE** como fonte de PROPAGAÇÃO (consistência provada), e a geometria é um gate ADITIVO de COMPLETUDE que fica `PENDENTE-VEDACAO`/fail-closed, com M-GEO apenas CARIMBANDO — *"dependência aberta"*, nunca a fonte substituta. Aposentar o substring e confiar numa coluna-overlay única **apaga o guard fail-closed de completude e o desenho de dois sinais independentes** — exatamente o falso-verde que a T8-DoD9 foi construída para impedir (um lote rotulado BIR em `bp_categor` mas geometricamente AUE ficaria refém de o overlay pegá-lo, sem cross-check). É regressão de 1.5/1.7 (fonte única de flag jurídica + remoção de gate fail-closed) vestida de "de-duplicação". A costura não estava "por resolver"; o Motor 1 a resolveu no sentido OPOSTO ao que o relatório propõe, e o relatório não reconhece isso.

**D3 [moderado — artefato inventado que quebra o discriminante mecânico de M1].** C7/C8/S5 definem o "carimbo M-GEO" como a tabela Postgres **`oficiais.vedacao_aue_appa`**, para a qual o flip de M1 apontaria. **Nenhum dos dois motores nomeia essa tabela.** Pior: o discriminante do flip de M1 (DoD 9c) é mecanicamente definido como *"um artefato EM `zepec/raw/` com path E hash distintos de `benstombados1.csv`"*, e `enriquecer_oficial.py` lê **CSV plano, não Postgres**. Uma tabela Postgres não é arquivo em `zepec/raw/` e não satisfaz o discriminante path+hash, nem gateia o pipeline CSV sem encanamento que o relatório não especifica. E o próprio Motor 3 insiste que seu hand-off core é a cadeia CSV, NÃO materialização Postgres (motor3: *"provar contra `v_feed_alvos`/Postgres seria falso-verde estrutural"*). C7 portanto **contradiz o design CSV-first de AMBOS os motores** e é insatisfazível como escrita.

**D4 [moderado — conflação de duas populações legítimas em C3].** C3 trata "4 SQLs de M1" e "32 de M3" como dois alvos disjuntos e *ambos falsos*, e propõe *"predicado único que cobre AMBOS"*. Mas são duas sub-populações legitimamente distintas do MESMO flag `cessao_vedada_art124p2` (verificado: 56 linhas-flag / 33 SQLs na base unificada; 32 com `motivo_negociavel` AUE/APPa em `zepec_cedentes.csv`): os **4** (`0180270001, 0020590054, 0090190000, 2000580001`) são as linhas de CONFLITO (flag=sim **E** declarou/vendeu → `montar_ferramenta.py:56` deliberadamente marca `negociavel='verificar'`, contradição a revisar); os **32** são o puro-vedado (flag=sim, nunca declarou → `negociavel='nao'`). Fundir num "predicado único" **colapsa o ramo CONFLITO/revisão de M1 dentro de vedado**, destruindo a distinção que `montar_ferramenta.py:56` codifica de propósito. Não é "ambos mal-diagnosticados"; é o relatório mal-lendo dois ramos como um erro.

**D5 [moderado — S5 superdimensiona a prontidão; D1-premissa não "cai" só por estar no ZMAP].** "*`overlay_zona.py` já os enumera no ZMAP (L22-24)… o consumidor já foi escrito*" superestima. Enumerar `ZEPEC_AUE`/`APP-BIR` no ZMAP **não é um consumidor de vedação**: `overlay_zona.py` resolve UM label de zona por lote com preferência explícita por zonas do Quadro 3 (`if in_q3[i]: base_hit=i; break`, L88-94), e os selos AUE/APP não têm CA → são **des-priorizados e ficam escondidos atrás da zona-base com CA**. `zona_por_cedente.csv` não tem coluna de vedação/selo (header: `sql_mestre,zona,ca_basico,fonte`). Logo o sinal geométrico de vedação **não é produzido hoje**; o overlay N:N de G2 ainda precisa ser construído. A premissa D1 ("inconstruível do dado presente") segue verdadeira PARA O REPO, e nem o dado do Drive a resolve sem G2. A direção do relatório (o dado existe no Drive) está certa, mas "a premissa cai / consumidor já escrito" é forte demais.

**D6 [moderado — fronteira de fase mal-desenhada, quase-circular no caminho crítico].** Fase 0 passo 5 torna M1/T2 "dono único do `consolidar.yml`" e o **provisiona** (pip/requirements-geo, service PostGIS, credencial Supabase, paths), rotulado como *"decisão de fronteira, sem código de produto"*. Mas os insumos que ele integra (`requirements-geo.txt`, pins, `recorte_q14.py`, `DL` parametrizado) só nascem na Fase 1 (passos 6-7, C9/C13), e o CI só fica verde ("o byte-diff de T2 não é vácuo") **depois** de E1 commitar `recorte_q14.py` e corrigir o path de `filtro_iptu.py` — também Fase 1. O próprio C9 diz "só então… não é vácuo". Então o passo 5 **não pode COMPLETAR na Fase 0**; só a decisão de posse pode. O gate de CI é simultaneamente pré-requisito Fase-0 ("senão os harnesses são decorativos", S2) e dependente Fase-1 de scripts que ainda não existem. Não é ciclo duro, mas a fronteira está errada: sequenciar posse (F0) → E1/G0 entregam scripts+specs (F1) → integrar e esverdear o CI (fim da F1), nunca F0.

**Nit (não-bloqueante):** C2/S3 lista `ca_basico` entre os "intermediários fabricados" nas 32 vedadas. Impreciso: `ca_basico` vem do overlay oficial `zona_por_cedente.csv` (lookup Quadro 3, L66 de `enriquecer_oficial.py`), não é fabricado. `pcpt_m2`/`saldo_pcpt_m2` SIM são computados antes do gate de preço (o núcleo de C2 está correto).

## O QUE CHECA (para não jogar fora o sólido)

- **S1/C12/C15 confirmados ao vivo** (projeto `csnalylpvysjvejgsymr`): existem só `oficiais.iptu2026_cedentes`, `oficiais.q14_valor_terreno_2025`, `governanca.de_para`, `governanca.registro_decisoes`, `public.spatial_ref_sys`. **Não existe schema `geo`, `dados` nem `tabelas`** — as migrations `20260624_010/020/030` (que criam `geo.lote`, `dados.*`, `tabelas.v_feed_alvos`) nunca foram aplicadas. A crise de canonicidade é real.
- **Drive/S5 base factual:** `scratchpad/geo/dl` tem 414 arquivos, 138 `.shp`, **96 distritos SIRGAS_LOTES distintos**, e `ZEPEC_AUE.shp` + `ZEPEC_APP-BIR.shp` presentes. A urgência de `PROVENIENCIA-GEO.md` antes de reciclar o scratchpad é legítima.
- **D-DONO-4/escopo:** `subir-grandes-colab.py:31` de fato comenta o `_IA` com ressalva ("_IA é nosso; use shapefile oficial") e **nenhum `.py` vivo lê `_IA`**. RECEPTOR (`gerar_alvos.py`/`oodc.py`/`v_feed_alvos`) fora de escopo — consistente. O relatório respeita o escopo vendedor/já-tombado; não introduz comprador/matching.
- **C2 (núcleo), C9/C14, S2 (CI sem pip/service, paths não cobrem `zepec/**`):** conferem contra `enriquecer_oficial.py`, `consolidar.yml` e a estratégia do Motor 2.

## VEREDITO
As reconciliações de infraestrutura (schema, CI, proveniência, ingestão do Drive) estão corretas e podem seguir. **A cadeia de vedação Art.124§2 (S3/C1/C2/C3/C7/S5), que é o coração adversarial do relatório, precisa ser reescrita**: (a) corrigir o anchor `montar_base.py`≠`enriquecer_oficial.py`; (b) NÃO aposentar o substring como fonte — mantê-lo como propagação e a geometria como gate de completude fail-closed (posição já resolvida do M1); (c) não materializar o carimbo em Postgres — manter o discriminante path+hash em `zepec/raw/` que o pipeline CSV consegue ler; (d) preservar a separação CONFLITO(4)≠puro-vedado(32). Sem esses quatro reparos, a Fase 2 do caminho crítico implementaria uma regressão de doutrina (fonte única de flag jurídica + remoção de fail-closed) com aparência de limpeza.
