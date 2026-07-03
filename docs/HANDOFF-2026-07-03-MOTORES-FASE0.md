# HANDOFF 2026-07-03 — Motores 1/2/3 + Escrutínio conjunto + Fase 0 executada

> **Dossiê de continuação, zero-compressão** (doutrina "nada se descarta"). Para uma próxima
> instância retomar SEM recomeçar o que já está feito. Estado vive no GIT e no BANCO (Supabase),
> não na conversa. Leia isto inteiro antes de tocar qualquer motor.

---

## 0. TL;DR OPERACIONAL (onde estou / o que fazer a seguir)

- **Branch de trabalho:** `claude/potencial-urbano-strategy-kp9bgr`. Convenção: após cada merge, **reinicio do `main`** (`git fetch origin main && git checkout -B claude/potencial-urbano-strategy-kp9bgr origin/main`). Há uma Action de "Consolidação por união → main (automática, D141)" que leva a branch ao main.
- **Supabase project id:** `csnalylpvysjvejgsymr` (org "Gestão Integrada", Pro).
- **Permissões:** allowlist amplo já vigente (D156/M-82 ratificado pelo escritório; `.claude/settings.json`). Deny de segurança preservado (escritorio-do-mou, keepee-facilities). Google Drive: leitura E escrita liberadas pelo dono em 2026-07-03 (CERCA suspensa por ele).
- **FASE 0 (Fundação) = COMPLETA e provada ao vivo.** Ver §5.
- **PRÓXIMO PASSO (fila local, minha):** na ordem — **C-28 (T1)** → **gate de CI (T2/S2)** → **cadeia de vedação Art.124§2 (T8)** → **conservação 3-estados (T4)** → **overlay por área (G1)**. Detalhe e "gotchas" obrigatórios em §8.
- **PENDÊNCIA DO DONO (bloqueia G2/G4):** 2 documentos verbatim — **Decreto 57.536/16** (Regra da Esquina) e **Quadro 2A do PDE** (macroárea/ZOE) — prompt de extensão já entregue; salvar no Drive `01 — _entrada` (fileId `1grhqYgttj7KnJmiu9U73z-lXFHnFthov`) como `decreto-sp-57536-2016.md` e `pde-16050-quadro-2A-macroarea.md`. Confirmado que NÃO estão no Drive nem no repo.

---

## 1. O QUE ESTA SESSÃO PRODUZIU (cronologia, com PR/commit)

1. **`ROADMAP-PU.md`** — documento-mãe (6 marcos de valor M0–M5, 3 forks do dono, painel de 7 lentes + crítica adversarial). **PR #12 (merged).**
2. **`MOTOR-1-ESTRATEGIA.md`, `MOTOR-2-ESTRATEGIA.md`, `MOTOR-3-ESTRATEGIA.md`** — estratégia de cada motor, endurecida por loop de lentes adversariais. **`docs/ESCRUTINIO-CONJUNTO-MOTORES.md`** (visão do todo + reconciliação Drive + crítica). **`docs/INVENTARIO-DRIVE.md`** (fontes oficiais por proveniência). **PR #13 (merged).**
3. **Fase 0 — canonicidade + proveniência** (`supabase/migrations/*`). **PR #16 (merged).**
4. **T7 gate de segurança** (`supabase/migrations/20260703172052_seg_t7_gate_seguranca_fase_a.sql`) — commit `b3c6978` na branch (segue p/ main pela consolidação automática).

---

## 2. COMO CADA MOTOR FOI PRODUZIDO + O RESÍDUO (não recomeçar)

**Método (o mesmo para os 3):** rascunho base → loop de lentes adversariais (Sonnet nas lentes de fan-out, Opus na síntese/crítica) → limites anti-loop (máx 5 rodadas; para em triplo limpo OU 2 rodadas sem achado ALTA). **NENHUM motor atingiu triplo limpo** — e isso É o resultado honesto: os loops recusaram declarar limpo enquanto havia furo real verificado em arquivo. O resíduo de cada um está no header do respectivo `MOTOR-*-ESTRATEGIA.md`.

- **Motor 1 (Travas):** 7 lentes (8 rodadas) + verificação focada D1/D2/D3 (3 rodadas). 12 travas **T1..T12**. Resíduo = classe única: *DoDs que declaram sem provar contra dado real* (encapsulada na **T12** — provar por golden-assert sobre o cohort real, fixture discriminante ou marcador materializado, nunca prosa).
- **Motor 2 (Dados/Infra):** 5 rodadas (teto), trajetória 7→8→6→7→3 ALTA. Achado grave: **crise de canonicidade** (schema git ≠ banco vivo) — **JÁ RESOLVIDA na Fase 0** (§5).
- **Motor 3 (Espacial):** 5 rodadas (teto), 10→5→2→4→1 ALTA. Achados-chave em §8.

---

## 3. ESCRUTÍNIO CONJUNTO — 5 doenças sistêmicas + a correção adversarial

6 lentes (3 costura entre motores Opus + 3 reconciliação Drive Sonnet), 48 achados → 5 doenças que atravessam os motores (`docs/ESCRUTINIO-CONJUNTO-MOTORES.md`):

- **S1 — Canonicidade do schema** (migrations vivas `oficiais.*` sem `.sql` no git; git `dados.*/geo.*/tabelas.*` nunca aplicadas). **RESOLVIDA (§5).**
- **S2 — "Declarei ≠ provei" no CI** (`consolidar.yml` não cobre `zepec/**`,`engines/**`,`tabelas/**`,`supabase/**`; sem pip, sem PostGIS, sem Supabase no runner). **PENDENTE (T2, §8).**
- **S3 — cadeia de vedação Art.124§2** — a síntese errou a âncora; a **crítica adversarial corrigiu** (ver abaixo).
- **S4 — SSOT de proveniência fragmentado** (`governanca.de_para` vivo e vazio). **RESOLVIDA (§5).**
- **S5 — premissa D1 cai** (a camada AUE/APPa existe no Drive). Ver §6/§8.

**A correção adversarial da cadeia de vedação (OBRIGATÓRIA ao codar T8):**
1. **Âncora correta:** `cessao_vedada_art124p2` é produzida em `montar_base.py:104` (`cessao_vedada(cat)` — substring em `bp_categor` de `benstombados1.csv`) e consumida em `montar_ferramenta.py:119`. **NUNCA em `enriquecer_oficial.py`** (esse é o bloco do engine de preço, linhas 78-98, que só lê `negociavel`/`esgotado`).
2. **NÃO aposentar o substring** como fonte: ele fica como *propagação* (consistência provada); a geometria AUE/APPa é gate **ADITIVO de completude fail-closed** (aposentá-lo = regressão de 1.5/1.7 e perda do fail-closed).
3. **Não materializar o carimbo em Postgres** (`oficiais.vedacao_aue_appa` era tabela inventada): manter o discriminante path+hash em `zepec/raw/` que o pipeline CSV-first lê.
4. **Preservar a separação** CONFLITO (4 SQLs: `0180270001, 0020590054, 0090190000, 2000580001`, `negociavel='verificar'`) ≠ puro-vedado (32 linhas, `negociavel='nao'`).

---

## 4. RECONCILIAÇÃO DO DRIVE (o que preenche lacuna / substitui / conflita)

Fontes OFICIAIS do Drive já mapeadas no `de_para` (§5) e em `docs/INVENTARIO-DRIVE.md`. As de maior impacto para os motores:

| Ativo (fileId) | Papel | Motor |
|---|---|---|
| `ZEPEC_AUE.shp` `1gYeb5cYlFgVlYt87VZhCSFgdja4njttK` + `ZEPEC_APP-BIR.shp` `1nSJNIe4lhxSGAuVgdY2bMbr0pkLyoQbN` | **camada espacial da vedação Art.124§2 — derruba a premissa D1 do Motor 1** | M1 (T8) / M3 (G2) |
| `ZEPEC_BIR.shp` `1SMJ5NlYfloTSOKt_PwwI618OToAKZQUk` | geometria dos lotes tombados p/ overlay | M3 (G1) |
| `SIRGAS_SHP_LOTES` (96 distritos, pasta-mãe `1ds4u4ZpoLl_ySSIDywPbh_iicRCt6zNI`; ex. Santana `1vjYfo976BeZOAO893iMIv3dWafjbNXcE`) | malha cadastral **OFICIAL que substitui os `LOTES_*_IA.csv` NOSSOS** (proibidos, D-DONO-4) | M3 (G1) |
| `SIRGAS_SHP_setorfiscal` `1Cu7SIG_gxzk9ItsmT0dv2qYDDIrh5Ps1` / `quadraMDSF` `1VdbAkuqv3p_yKX_rO_ZUzGw5MOfVsxOo` | chave de join geo↔IPTU | M2/M3 |
| `SIRGAS_SHP_logradouronbl` `118bVYfXP9mpu8VIbm_4qBazI4fQfcFWG` | geocodificação dos 63 sem SQL | M3 (G3) |
| `lista_declaracoes_ZEPEC-BIR_ago-2025.xlsx` `17j94xkgVk4eberaRpRLK2j_ekz480Lny` / `lista_certidao_…` `1en2WC2A-Wd21NNDhZ8ThheAyHmODIOl-` | fonte de verdade das certidões p/ os gates | M1 |
| `IPTU_2026.csv` `1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM` (937 MB) | bronze; **o recorte de cedentes já está em `oficiais.iptu2026_cedentes`**; o COMPLETO (3,9M linhas) é o alvo do fuzzy do G3 | M2/M3 |

**NÃO USAR (marcado no `de_para`):** `LOTES_*_IA.csv` (`1EyzQ9O6HTbiUSBgotHYBun_haesZHGC_` …), docs de análise nossos, Modelo Reduzido. Tabelas Quadro 3/5/OODC são extração NOSSA de fonte oficial → usar só após revisão humana.

**FALTAM no Drive (item do dono):** Decreto 57.536/16 e Quadro 2A (§0).

---

## 5. FASE 0 — EXECUTADA (feito e provado ao vivo no Supabase)

**Migrations no git == banco vivo** (`supabase/migrations/`, `db reset` reproduz a produção):
- `20260619020603_enable_core_extensions.sql`
- `20260619020658_scaffold_canonico_governanca.sql` (cria schemas leis/tabelas/engine/tese/geo/governanca + `de_para` + `registro_decisoes` + `is_sql_mestre()`)
- `20260619020951_harden_function_search_path.sql`
- `20260624100319_storage_buckets_pesados_e_schema_rag.sql` (schema rag + 3 buckets privados)
- `20260702142208_oficiais_camada_produto_tdc.sql` (**oficiais.iptu2026_cedentes**, **oficiais.q14_valor_terreno_2025**; RLS deny-all)
- `20260703145720_seed_de_para_proveniencia_drive.sql` (**S4** — 20 fontes no `de_para`, 14 OFICIAL; D-CANON-01/02)
- `20260703172052_seg_t7_gate_seguranca_fase_a.sql` (**T7** — D-SEG-01)
- **Arquivadas** (nunca aplicadas, schema RECEPTOR, fora de escopo): `supabase/migrations/_nao-aplicadas-receptor/20260624_010/020/030` + README.

**Estado do banco vivo (exato, 2026-07-03):**
- `oficiais.iptu2026_cedentes` = 3.905 linhas; `oficiais.q14_valor_terreno_2025` = 3.676.
- `governanca.de_para` = 20 linhas (14 OFICIAL); `governanca.registro_decisoes` = 3 (**D-CANON-01** canonicidade, **D-CANON-02** de_para, **D-SEG-01** T7).
- Schemas `leis/tabelas/engine/tese/geo/rag` existem e estão VAZIOS. `dados.*` NÃO existe (era fantasma).
- Buckets `dados-produto`, `geo-tabelas`, `geo-shapefiles` = **privados**. `oficiais.*` = RLS enabled, **zero policies** (deny-all p/ anon).
- **Nada em produção usa a `service_role`** — os scripts do pipeline leem CSV plano (`enriquecer_oficial.py` etc.); o número in-scope NÃO vem do Postgres hoje.

**T7 (segurança) — feito pelo dono via extensão + verificado por mim:** spend cap ATIVADO (org Pro, estava off); 3 S3 access keys da Fase A revogadas; buckets privados + RLS deny-all confirmados. **Resíduo de baixo risco:** `service_role` legada não rotacionada isoladamente (Supabase só oferece "Generate new JWT secret", que derruba anon+service_role). Plano: ao precisar de chave de serviço (Fase 1 loaders), criar `sb_secret` nova e desabilitar as legadas — zero quebra.

---

## 6. PENDÊNCIAS DO DONO (externas — não dá para eu fazer)

1. **2 documentos verbatim** (§0): Decreto 57.536/16 + Quadro 2A. Bloqueiam G2 (ZOE) e G4 (Regra da Esquina). Prompt de extensão já entregue nesta thread.
2. **(opcional, Fase 1)** rotação da `service_role` legada — só quando formos usar chave de serviço.
3. **Merges** no `main` protegido (a consolidação automática D141 tem feito isso; PRs #12/#13/#16 já mergeados).

---

## 7. INVARIANTES / DOUTRINA / CERCAS (não violar)

- Número nasce no ENGINE (1.3); citação por dispositivo (1.7); fonte única (1.5); todo dado tem vintage/vigência (1.6); "declarei feito ≠ provei feito" (gate `scripts/fechar-instancia.py`).
- **Escopo (dono, 2026-07-03): SÓ lado VENDEDOR (cedente), SÓ o que JÁ ESTÁ TOMBADO** (ZEPEC-BIR já declarada). **Sem comprador/matching/receptor, sem vias 2-6, sem OODC/`v_feed_alvos`/`gerar_alvos`.** Qualquer resíduo receptor nos docs antigos (ROADMAP §, migrations arquivadas) está fora.
- **D-DONO-4:** só fonte OFICIAL/ADQUIRIDA; NUNCA planilha nossa (`_IA`, MEGA_PLANILHA, Modelo Reduzido, PotencialUrbano_*).
- **NUNCA fabricar** dado onde a lei não ampara: sinalizar/FLAG, nunca inventar (vale p/ ZOE/Quadro 2A e Regra da Esquina enquanto a fonte não chega).
- Cercas de escrita: `escritorio-do-mou` e `keepee-facilities` (deny em `.claude/settings.json`).

---

## 8. FILA LOCAL (minha) — ordem de execução + gotchas OBRIGATÓRIOS

> A estratégia completa de cada item está em `MOTOR-1/2/3-ESTRATEGIA.md`. Abaixo, a ordem e os pontos que um coder DEVE honrar (verificados em arquivo pelos loops).

**[T1] C-28 — corrigir a citação da fórmula central (fatiar.py).** A fórmula PCpt vive num chunk ROTULADO "Art. 124" quando é **Art. 125**. Causa: remissão line-initial ("art. 124 desta lei") abre chunk. **NÃO usar monotonicidade de número** (invariante ERRADO: falso-positivo em lei alteradora, ex. EC-132 Art.2º após Art.156-B; falso-negativo em remissão para número maior). Usar **discriminador lexical + `header_raw` obrigatório (comparar contra o rótulo, reprovar divergência) + unicidade pela FÓRMULA COMPLETA** (`PCpt = Atc × CAbas × Fi` ⇒ Art.125; `PCpt = Atc × CAmax × Fi` ⇒ Art.127). O bug atinge **≥6 leis** (6015-1973, 10931-2004, ec-132-2023, 17844, 16050, 16402). Eval **sobre CONTEÚDO** (dispositivo E texto juntos): hoje `rodar-evals.py:41` compara rótulo por SUBSTRING ('Art. 12' é substring de 'Art. 125') → endurecer para regex normalizada. Falso-verde atual: existem DOIS chunks "Art. 124".

**[T2/S2] Gate de CI cobrindo o produto.** `consolidar.yml`: `on.push.paths` adicionar `zepec/** engines/** tabelas/** supabase/**`; adicionar `on: pull_request`; adicionar `pip install`; adicionar step `pcpt.py --demo`/`_autoteste`; escrever `scripts/eval-produto.py` (5-10 cedentes conferidos à mão) que REGENERA a cadeia e compara. **Cético cortou o "byte-diff do enriquecer" como cerimônia** — usar em vez disso um **golden CSV projeção SEM PII** (dropar proprietario/endereco/nome antes de versionar).

**[T8] Cadeia de vedação Art.124§2 — usar a correção adversarial de §3.** Âncora `montar_base.py:104`/`montar_ferramenta.py:119` (não `enriquecer_oficial.py`). Substring = propagação; geometria AUE/APPa (fileIds em §4) = gate aditivo de completude fail-closed. Guard ANTES do bloco atc/cabas de `enriquecer_oficial.py:79` zerando `pcpt_m2`/`saldo` nas vedadas (o fail-closed de M1 hoje é só-preço; `pcpt`/`saldo` seguem fabricados). Separar CONFLITO(4)≠vedado(32).

**[T4] Conservação 3-estados.** Filtro de cohort `origem == CERTIDAO_BIR_CEDENTE` **mecânico** (não em prosa) — para `TOMBADO_CADASTRO`, `montar_base.py:173` põe `ato_conservacao = bp_compres` (string de tombamento "RES. 22/02"), que uma regra global leria como elegível. **Termo de Compromisso (111 linhas) → PENDENTE-CONSERVAÇÃO; Atestado de Conservação (32) → ELEGÍVEL** (Termo é compromisso de REMEDIAR, evidencia conservação inadequada — NÃO elegível). Fixtures obrigatórias que FALHEM: uma linha Termo marcada ELEGÍVEL; uma `RES. 22/02` marcada ELEGÍVEL. Art.129 §2 (Lei 17.975/23) amarra o MONTANTE à idade (70% aos 10 anos c/ Atestado, 100% aos 15).

**[T3] Regime do já-declarado.** Engine recusa aplicar o Fi escalonado por default no escopo (100% já-declarado). **CORREÇÃO verificada:** a restrição do escalonado está no **CAPUT do Art. 24 LPUOS** ("na emissão de NOVAS declarações…"), **NÃO no Art. 25** (que é reforma com acréscimo). Para o já-declarado, exigir Fi da certidão ou marcar PENDENTE. `enriquecer_oficial.py:81` hoje chama `pcpt_sem_doacao(atc, cabas)` sem `fi` → aplica escalonado a TODA a base (errado p/ o cohort inteiro).

**[G1] Overlay por área + unary_union.** `overlay_zona.py:66-78` pega a **1ª feature** do SQL (MAT-2: 250 SQLs multi-feature) e usa `.centroid` (293 caem fora de zona, 14 fora do lote). Usar `unary_union` de TODAS as features do SQL + `representative_point()` + overlay por MAX área. Trocar `LOTES_*_IA` pelo `SIRGAS_SHP_LOTES` oficial (§4).

**[G2] Zona-base N:N (os 454) + ZOE.** Overlay N:N devolvendo todas as camadas; zona-base de maior área; confirmar juridicamente se o CAbás da zona-base se aplica a APC/APP/AUE (senão FLAG). **ZOE (77) tem regime PRÓPRIO: Quadro 2A/macroárea do PDE, NÃO Quadro 3** — FLAG até o Quadro 2A chegar (§6). Nunca fabricar.

**[G3] Geocodificar — só 63, não 1.839.** Dos 1.839 sem SQL, **1.772 são a MESMA linha** ("Luminárias Ornamentais da Light" — tombamento coletivo de postes, sem lote individual → problema de MODELAGEM, não geocode). Só **63 têm endereço**. O alvo do fuzzy (pg_trgm) deve ser o **IPTU_2026.csv COMPLETO** (3,9M linhas no Storage), não o recorte `iptu2026_cedentes` (que só tem cedentes já identificados).

**[G4] Regra da Esquina.** `enriquecer_oficial.py:57` casa V por 1 face (`sql[:6]`+codlog). Expor **RANGE `v_min/v_max` + `flag_v_sensivel`** (posição MAT-5), **NÃO** comprometer com MAX até o **Decreto 57.536/16** ser ingerido verbatim (§6). Nunca citar dispositivo não-lido.

**[G5] Materializar overlay.** Mirar `oficiais.*` (não `geo.lote_zona`). Produção do cedente lê CSV plano hoje; `geo.lote.zona`/`v_feed_alvos` são schema receptor/fantasma (arquivado).

**[G6] Eval geo.** `rodar-evals.py` só tem schema RAG (`pergunta` → `consultar.py`). `geo-overlay.json` precisa de branch por domínio ou runner próprio; 30-50 cedentes conferidos no GeoSampa; deve MORDER ao injetar zona errada (mutation).

**[Motor 2 restante]** E1 (gerador `recorte_q14.py` + `cedentes_sqls.txt` — hoje diverge 4291 vs 4292; `refazer_oficial.sh` byte-idêntico; colunas por header) · E2 (vintage fato/ingestão/vigência-intervalo; Q14 precisa `vigencia_inicio/fim` — C-21/J7: Q14 jan/2025 p/ protocolos 2026+ sem data-base/IPCA) · E3 (medallion 1 pág) · E4 (IPTU/Q14 Postgres + 817 shapefiles + pg_trgm) · E5 (rclone canal único + dedup 40,6%) · E7 (loaders idempotentes). **E6 (canonicidade) JÁ FEITO (§5).**

**[Motor 1 restante]** T5 (divergência 27% + disclaimer) · T6 (arquivar `engines/tdc/oraculos/` + ≤3 fontes) · T9 (parcelamento >50k m²) · T10 (validade DPC 5 anos — depende Decreto 57.536) · T11 (saldo por CONJUNTO: `montar_ferramenta.py:46` atribui o m² do conjunto só a `sms[0]`) · T12 (regra de endurecimento — aplicar nas DoDs).

---

## 9. PONTEIROS (todos os artefatos)

- Estratégias: `ROADMAP-PU.md`, `MOTOR-1-ESTRATEGIA.md`, `MOTOR-2-ESTRATEGIA.md`, `MOTOR-3-ESTRATEGIA.md`.
- Escrutínio + Drive: `docs/ESCRUTINIO-CONJUNTO-MOTORES.md`, `docs/INVENTARIO-DRIVE.md`.
- Loop anterior (14 lentes) + doc-mestre: `docs/LOOP-MELHORIA-H1-2026-07-02.md`, `docs/EXTRACAO-DOC-MESTRE-TDC-2026-07-02.md`.
- Migrations: `supabase/migrations/` (7 canônicas + `_nao-aplicadas-receptor/`).
- Pipeline/produto: `engines/tdc/pcpt.py`, `zepec/enriquecer_oficial.py`, `zepec/montar_base.py`, `zepec/montar_ferramenta.py`, `zepec/pipeline/` (filtro_iptu, overlay_zona, gerar_xlsx).
- Gate: `scripts/fechar-instancia.py`; CI: `.github/workflows/consolidar.yml`.
- Decisões vivas: `governanca.registro_decisoes` (D-CANON-01/02, D-SEG-01) + `BACKLOG.md`.
