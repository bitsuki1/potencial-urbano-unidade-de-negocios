# PLANO DE ARRUMAÇÃO DO DRIVE + SEPARAÇÃO TDC×IPTU — 2026-07-04 (PU 17)
> Síntese de **4 lentes** que o dono pediu ("lance lentes para estudar essas separações, tagueamentos, regras e técnicas RAG, técnicas gerais").
> Lentes: **(A) Taxonomia de pastas** · **(B) RAG/metadados** · **(C) Domínio jurídico** · **(D) Pipeline/governança**.
> **Status: DESENHO — aguarda aprovação do dono antes de executar** (nenhum arquivo do Drive é movido, nenhum `.json` é reetiquetado sem o "vai").
> Doutrina respeitada: 4 artefatos separados (1.1) · extrair→enriquecer→argumentar (1.2) · número no engine (1.3) · vigência (1.6) · citação (1.7) · nada se descarta.

---

## 0. O problema, em uma frase
O acervo mistura **dois domínios jurídicos** — **TDC** (transferência do direito de construir) e **IPTU** (imposto predial e territorial urbano) — e hoje essa distinção está **enterrada no lugar errado**: no campo `tema[]` de cada lei (ex.: `leis/federal/lei-federal-9514-1997.json` tem `tema:["IPTU", …]`). Isso quebra o retrieval híbrido (2.6), impede filtro por domínio e não sobrevive quando uma norma serve aos **dois** (PDE, Estatuto da Cidade). Uma separação ingênua — "pasta TDC" e "pasta IPTU" — **duplica** as normas compartilhadas ou **perde** uma das cópias. As 4 lentes convergiram numa saída única: **domínio é ETIQUETA (metadado), não PASTA.**

---

## 1. Princípio-mestre das 4 lentes (o que todas concordaram)
| Eixo | Decisão convergente | Por quê |
|---|---|---|
| **Organização primária** | por **TIPO de artefato** (lei / tabela / engine / jurisprudência / geo / tese) | é a doutrina 1.1 (4 artefatos separados); é estável; é o que o pipeline já usa (`leis/`, `tabelas/`, `engines/`, `jurisprudencia/`) |
| **Domínio TDC×IPTU** | é **metadado `dominio[]`**, NÃO pasta | uma norma pode ser dos dois; pasta força escolha binária e duplica |
| **Compartilhado** | vocabulário fechado: `tdc` · `iptu` · `compartilhado`; **lar único**, incluído nas consultas dos DOIS | não duplica o PDE/Estatuto; a consulta de qualquer domínio sempre puxa `compartilhado` |
| **Proveniência** | `OFICIAL` / `ADQUIRIDO` / `NOSSO` (D-DONO-4) explícita no nome e no índice | OFICIAL é citável; NOSSO nunca vira fonte de número |
| **Drive × git** | Drive = **bruto/espelho**; git = **limpo/verbatim/indexado**; cola = **hash** | Drive é zona de despejo; git é o corpus servível |

---

## 2. Árvore do Drive (Lente A — Opção B: TIPO no topo, domínio como subpasta+prefixo)
Raiz `Potencial Urbano` (`1BrM6q36…`). **TIPO** define a pasta; **DOMÍNIO** é subpasta `.1/.2/.3` + prefixo no nome; **PROVENIÊNCIA** é prefixo no nome.

> **DECISÃO DE TAXONOMIA (R6, 2026-07-04): a EXECUÇÃO usa a taxonomia de JUNHO** (a concreta, já fiada: `00 Governança · 02 Leis&Jurisprudência/2.1..2.7 · 03 Tabelas&Engines · 05 Geo · 99 Inbox` — 1.360 arquivos já mapeados, pastas criadas, seeder+Organizer coerentes). A **Opção B abaixo** (TIPO no topo, domínio em `.1/.2/.3`) é o **alvo de REORGANIZAÇÃO FUTURA**, registrado no backlog — **não roda agora** (migrar às vésperas re-mapearia os 1.360 destinos e colidiria na numeração: junho `03`=Tabelas/`05`=Geo vs Opção B `03`=Jurisprudência/`05`=Engines). **Nunca os dois ao mesmo tempo.** O `98 — _LEGADO` (quarentena do saneamento) é criado como zona-morta adjunta à taxonomia de junho.

```
00 — Governança & Índice        ← INDICE-MESTRE, manifestos, logs, relatórios NOSSOS, disclaimers
01 — _entrada                    ← zona de despejo (deve ficar VAZIA após arrumar — é o gate)
02 — Leis & Normas
      02.1 [TDC] · 02.2 [IPTU] · 02.3 [COMUM]
03 — Jurisprudência
      03.1 [TDC] · 03.2 [IPTU] · 03.3 [COMUM]
04 — Tabelas & Valores           (input de engine — CSV)
      04.1 [TDC] · 04.2 [IPTU] · 04.3 [COMUM]
05 — Engines & Fórmulas
06 — Geo / Mapas                 (shapefiles SIRGAS, zoneamento, ZEPEC — PESADO → Supabase)
07 — Tese / Antítese / Vacina
      07.1 [TDC] · 07.2 [IPTU]
08 — Doutrina & Referência
09 — NOSSO (não-confiável p/ número: LOTES_IA, rascunhos, saídas de modelo)
98 — _LEGADO (congelado, read-only: lago "TODOS TDC", MOTOR_2, cemitérios de duplicata)
99 — Inbox / Triagem            (ambíguos — nunca perdidos, decisão manual)
```

**Convenção de nome canônico** (carimba domínio + proveniência + vigência no próprio arquivo):
```
[DOM][PROV] <identificador> — <descrição> {vig=AAAA→AAAA}.<ext>
   ex.: [COMUM][OFI] PDE Lei 16.050-2014 — Plano Diretor Estratégico {vig=2014→}.pdf
        [TDC][OFI]   Decreto 57.536-2016 — regulamento TDC {vig=2016→}.pdf
        [IPTU][OFI]  Lei 6.989-1966 — IPTU município SP {vig=1966→}.pdf
        [TDC][NOS]   LOTE_IA cedentes-rascunho {vig=2026}.csv   → vai p/ 09
```
`DOM ∈ {TDC, IPTU, COMUM}` · `PROV ∈ {OFI, ADQ, NOS}`. O **INDICE-MESTRE** (§5) é a camada de tag verdadeira; o nome é o espelho legível.

**Lago legado — SANEAR (decisão do dono 2026-07-04):** o `TODOS TDC` (março/2026, ~1.000+ arquivos, 3 cemitérios de duplicata) é **saneado**, não só congelado: **dedup por hash → a canônica vai para a pasta-tipo correta; as irmãs vão para quarentena datada** (`98/_quarentena-AAAA-MM-DD/`, nunca lixeira — "nada se descarta"). É a **onda 1** da execução Drive.

---

## 3. Domínio `dominio[]` no git (Lente B — o metadado, não a pasta)
**Regra:** `leis/` continua organizado por **esfera** (`federal/`, `municipal-sp/`) — **NÃO** criar `leis/tdc/` e `leis/iptu/`. O domínio entra como **campo no `.json`**.

### 3.1 Mudança de schema (aditiva — não quebra o existente)
Adicionar a cada `leis/<id>.json` e `jurisprudencia/<id>.json`:
```json
"dominio_primario": "compartilhado",        // 1 valor: o efeito jurídico dominante do DOCUMENTO
"dominio": ["tdc", "iptu"]                    // array por-chunk (vocab fechado); compartilhado ⇒ ["tdc","iptu"] ou ["compartilhado"]
```
E **remover** `"IPTU"`/`"TDC"` de dentro de `tema[]` (o anti-padrão vivo — 28× IPTU, 3× TDC hoje). `tema[]` volta a ser só assunto material (`alienacao_fiduciaria`, `progressividade`, `outorga_onerosa`…).

### 3.2 Pontos de código a tocar (~10 linhas, cirúrgico)
| Arquivo | O quê |
|---|---|
| `scripts/fatiar.py` | propagar `dominio` da lei p/ cada chunk (o chunk herda; PDE pode ter chunk `tdc` e chunk `iptu`) |
| `scripts/indexar.py` | indexar `dominio` como faceta filtrável (não como texto) |
| `scripts/consultar.py` | filtro por domínio ANTES do BM25/semântico; **regra de ouro:** `dominio == alvo OR "compartilhado" ∈ dominio` (compartilhado sempre entra) |
| `evals/` | 1 eval que prova: consulta TDC puxa PDE (compartilhado) e NÃO puxa súmula de IPTU-puro |

### 3.3 Granularidade (Lente C)
- **Por-DOCUMENTO agora** (`dominio_primario`): rápido, cobre 90% dos casos, destrava já.
- **Por-DISPOSITIVO depois** (`dominio` no chunk): só onde importa juridicamente — hoje **só o PDE (Lei 16.050)**, que tem artigos TDC (122–133) e artigos que afetam base de cálculo. Decisão do dono (§7).

### 3.4 Técnicas RAG habilitadas (ordem de custo)
- **P1 — filtro facetado por `dominio`** (grátis, já no híbrido 2.6) — **fazer já**.
- **P2 — roteamento de query** (classifica a pergunta em tdc/iptu/ambos antes de buscar).
- **P3 — grafo de remissões** (`remissoes[]` já existe; ligar norma→norma cruzando domínio).
- **P4 — pré-filtro semântico** (embeddings) — última milha, só quando o corpus crescer.

---

## 4. Regra de fronteira TDC×IPTU (Lente C — o teste do "efeito jurídico")
Para taguear qualquer documento/dispositivo, pergunte **qual efeito jurídico ele produz**:

```
P1. Cria/transfere/regula POTENCIAL CONSTRUTIVO (solo criado, outorga, TDC, ZEPEC)?  → tdc
P2. Institui/calcula/isenta o TRIBUTO IPTU (base, alíquota, progressividade, imunidade)? → iptu
P3. Produz os DOIS efeitos (ou é regra-quadro que ambos invocam)?                        → compartilhado
P4. É matriz constitucional/geral (função social, reforma tributária, CTN geral)?        → compartilhado
```
**Casos-limite resolvidos:**
- Acórdão que *cita* IPTU mas *decide* sobre tombamento → **tdc** (decide o efeito, não a citação).
- Tabela de valor de terreno (Quadro 14) que serve outorga (TDC) **e** é venal-adjacente (IPTU) → **compartilhado**.
- PDE: artigo 122–133 → `tdc`; artigo de parâmetro urbanístico que afeta base → `iptu`; documento inteiro → `dominio_primario: compartilhado`.

**Lista COMPARTILHADO (reclassificações propostas — dono confirma em §7):**
| Norma | Hoje | Proposto | Razão |
|---|---|---|---|
| CF arts. 182-183 | — | compartilhado | matriz da política urbana (P4) |
| Estatuto da Cidade (Lei 10.257) | — | compartilhado | função social serve aos dois (P4) |
| **EC 132/2023** (`leis/federal/ec-132-2023`) | tema tributário | compartilhado | reforma tributária toca IPTU e o financiamento urbano |
| **PDE Lei 16.050/2014** (`leis/municipal-sp/…16050…`) | — | compartilhado (per-disp. depois) | TDC E base de cálculo (P3) |
| **LPUOS Lei 16.402/2016** (`…16402…`) | — | compartilhado | zoneamento alimenta CAbás (TDC) e parâmetros (IPTU) |
| CTN — regras gerais | — | compartilhado | regra-quadro tributária |
| **Quadro 14** (`tabelas/q14-valor-terreno.csv`) | — | compartilhado | outorga (V) E venal-adjacente |

---

## 5. Índice-mestre do Drive (Lente D — a fonte da verdade da arrumação)
**DOIS arquivos, um dono cada** (correção da lente de reconciliação R2 — o seeder não pode sobrescrever a execução):
- `inventario/INDICE-SEED.csv` — o **PLANO** imutável, escrito só por `scripts/semear_indice_mestre.py` (do de-para).
- `inventario/INDICE-MESTRE-DRIVE.csv` — o **estado REAL**, escrito só por `scripts/reconciliar_arrumacao.py` (SEED + logs do GAS).

Colunas exatas (20):
```
drive_id, nome_origem, nome_canonico, tipo_artefato, dominio, dominio_primario,
proveniencia, oficialidade, confianca, vigencia_inicio, vigencia_fim,
substitui, substituido_por, destino_classe, destino_path,
hash_md5, bytes, mime, id_pipeline, status_arrumacao, observacao
```
> **`hash_md5`, não `hash_sha256`** (R5): a única hash que o Drive/GAS entrega é o `md5Checksum`. Nomear a coluna pela hash real evita a trilha "dizer sha256 e carregar md5".

`status_arrumacao ∈ {bruto, carimbado, moved, quarentena, espelhado, triagem}`. `triagem` (R11) = estado TERMINAL deliberado (multi-pai/ambíguo → decisão humana em `99`) — conta como resolvido, não como pendência. Herdado pelo pipeline (`promover_entrada.py` lê `nome_canonico`/`dominio`/`proveniencia` — zero re-trabalho).

### O loop que fecha (reconciliação — sem ele a arrumação nunca se PROVA, R1)
```
semear_indice_mestre.py → INDICE-SEED.csv (status=carimbado, PLANO)
        ↓  (dono roda o Apps Script no Drive; cola o Log em inventario/gas-log-<data>.txt)
Organizar-Entrada.gs emite  MOVE_LINHA drive_id,folderId,md5,bytes,status   (R3)
Sanear-Lago.gs       emite  CSV_LINHA  drive_id,md5,acao,canonico_id
        ↓
reconciliar_arrumacao.py → INDICE-MESTRE-DRIVE.csv (status=moved/quarentena, hash preenchido)
                         + inventario/arrumacao-log.csv (trilha durável append-only, a prova mora no git — R13)
        ↓
gate-arrumacao.py vê fase 'execucao' → C1–C5 passam a BLOQUEAR → arrumação PROVADA
```
`reconciliar` faz **UPSERT** (R4): arquivo do lago fora do SEED é inserido; e **bloqueia** se uma irmã OFICIAL for quarentenada sob canônica NOSSA (a canônica tem de ser a de maior oficialidade — "OFICIAL é citável").

### Mapa Drive → git → Supabase (por tipo)
| tipo_artefato | Drive | git | Supabase | domínio marcado onde |
|---|---|---|---|---|
| Lei/Norma verbatim | 02.x | `leis/<esfera>/` | — | campo `.json` `dominio` |
| Jurisprudência | 03.x | `jurisprudencia/` | — | campo `.json` `dominio` |
| Tabela leve (CSV) | 04.x | `tabelas/` | — | subpasta Drive + linha do índice |
| Engine/fórmula | 05 | `engines/tdc\|iptu/` | — | subpasta (tdc/iptu já existem) |
| Tese | 07.x | `tese/<dom>/` | — | subpasta |
| Geo / pesado (>50MB, shapefile, IPTU_2026.csv 937MB) | 06 | **NÃO** (git-ignore) | **Storage/tabela** | linha do índice + `PESADOS-PARA-SUPABASE.csv` |
| NOSSO / rascunho | 09 | — (fora do corpus) | — | prefixo `[NOS]` |

### 6 invariantes de governança
1. **Move, não copia** (`file.moveTo`) — nunca duplica (modo de falha V-3).
2. **Nada se descarta** — ambíguo → `99`; suspeito de lixo → `98`/quarentena datada, nunca lixeira.
3. **Dedup por hash** — mesmo `hash_md5` = 1 canônica; irmãs viram `substituido_por`.
4. **Canônica única** — cada conteúdo tem um `destino_path` só.
5. **Idempotência** — rodar 2× = mesmo estado (skip-if-already-there).
6. **Auditabilidade** — todo move é uma linha no índice + log do Apps Script.

---

## 6. Gate mecânico + sequência em ondas (Lente D — "declarei ≠ provei")
### `scripts/gate-arrumacao.py` (espelha `fechar-instancia.py`) — 8 checks
1. `01 — _entrada` tem **0** arquivos soltos.
2. Toda pasta-alvo com **contagem esperada** (bate com o índice).
3. Índice-mestre **bate** com o Drive (todo `drive_id` do índice existe; todo arquivo do Drive está no índice).
4. **Nenhum OFICIAL** em `98`/`99`/quarentena.
5. Todo item `moved` tem `hash_md5` preenchido.
6. Todo `dominio` ∈ vocab fechado `{tdc,iptu,compartilhado}`.
7. Nenhum `dominio_primario` vazio em lei/jurisprudência.
8. `tema[]` **não** contém mais `TDC`/`IPTU` (anti-padrão eliminado).

### Ondas de execução (gate entre cada — minimiza risco de perda)
| Onda | Ação | Gate de saída |
|---|---|---|
| **0** | Snapshot + hash de tudo (índice bruto) | índice tem 100% dos `drive_id` |
| **1** | Dedup + quarentena datada (irmãs → `98`) | 0 duplicatas na zona ativa |
| **2** | Carimbar índice (nome_canonico, dominio, proveniencia, vigencia) | 0 linhas `bruto` |
| **3** | Mover por TIPO (Apps Script `moveTo`) | `_entrada` vazia; contagens batem |
| **4** | Separar DOMÍNIO (subpastas .1/.2/.3 + campo `.json`) | check 6/7/8 verdes |
| **5** | Espelhar no git (leis/juris) + Supabase (pesados) | pipeline reindexado; evals verdes |

**Restrição técnica confirmada:** o conector MCP do Drive **não move** arquivos — só o **Apps Script** (`file.moveTo`) move de verdade sem duplicar. Por isso a onda 3 é entregue como script `.gs` para o dono colar e rodar (`DRY_RUN` primeiro).

---

## 7. Decisões do DONO — REGISTRADAS 2026-07-04 (gate humano)
1. **Lista compartilhado (§4):** dono respondeu *"como achar melhor, não quero correr o risco de perder nada"* → adotada a regra que **não perde por construção**: `compartilhado` INCLUI a norma nas consultas dos DOIS domínios; **na dúvida → compartilhado**; nunca se remove uma norma de um domínio. Aplicadas as 6 reclassificações efetivas no corpus atual (EC 132, PDE 16.050, LPUOS 16.402, COE 16.642, registro-imóveis 6.015, tombados 12.350). CF 182-183/Estatuto/CTN/Quadro 14 entram `compartilhado` quando ingeridos. **Registro auditável em `scripts/carimbar_dominio.py` (razão por item); o dono pode estreitar depois e re-rodar.**
2. **PDE per-dispositivo:** `dominio_primario: compartilhado` **já** (feito); quebra por-dispositivo é **onda futura** (não bloqueia).
3. **Lago `TODOS TDC`:** dono escolheu **SANEAR** (não congelar). Regra: **dedup por hash + quarentena datada** (invariante "nada se descarta" — irmãs vão para quarentena datada, não pra lixeira). Execução é Drive-side (Apps Script na onda de saneamento); **entra na trilha de ondas 1**, não some.
4. **Ordem de entrega:** dono autorizou **começar já** a parte 100% local e reversível → **EXECUTADO** nesta branch (ver §9). O Drive (ondas 3–5 + saneamento do lago) só roda com o "vai".

---

## 8. O que já está pronto para acoplar (não recomeçar)
- `drive-arrumacao/de-para-COMPLETO-2026-07-04.csv` (1.360 arquivos da `_entrada` classificados) → vira as ondas 0–2 do índice-mestre.
- `drive-arrumacao/Organizar-Entrada-2026-07-04.gs` (move os 1.360) → é a **onda 3** para a `_entrada` (falta só o dono rodar).
- `inventario/PESADOS-PARA-SUPABASE.csv` + `inventario/classificacao-*.csv` → alimentam o mapa do §5.
- Enumerações do Drive já coletadas (TABELAS, MOTOR_1, subárvores) → semente do índice-mestre para além da `_entrada`.

---

## 9. Parte LOCAL — EXECUTADA 2026-07-04 (na branch, sem tocar o Drive)
Autorizada pelo dono (§7.4). Tudo reversível, provado por gate mecânico, **suíte de evals 15/15 + eval-dominio verde, sem regressão**.

| Entregue | Arquivo | Prova |
|---|---|---|
| Carimbo de domínio (63 itens: 31 leis + 32 juris) | `scripts/carimbar_dominio.py` | `--check` verde; distribuição compartilhado=6 · iptu=57 · tdc=0 |
| Anti-padrão eliminado (IPTU/TDC fora de `tema[]`) | idem | I5 do eval-dominio |
| Domínio propagado ao chunk | `scripts/fatiar.py` | 1.864 chunks, 0 sem domínio |
| Domínio como faceta no índice | `scripts/indexar.py` | metadados carregam `dominio` |
| Filtro `--dominio` (compartilhado sempre entra) | `scripts/consultar.py` | `--dominio tdc` traz PDE Art.125/128, sem vazar IPTU-puro |
| Eval das invariantes (I1–I5) | `evals/eval-dominio.py` | OK — não-poluição · não-perda · PDE alcançável · vocab fechado · anti-padrão |
| Gate da arrumação (local verde, Drive pendente honesto) | `scripts/gate-arrumacao.py` | C6/C7/C8 verde; C1–C5 PENDENTE (aguardam índice-mestre) |
| Domínio no gate de fechamento | `scripts/fechar-instancia.py` | check DOMÍNIO verde |
| Domínio no CI | `.github/workflows/consolidar.yml` | novo passo gate |

**Distribuição de chunks:** iptu=868 · compartilhado=996 (PDE+LPUOS+COE são grandes → muitos chunks compartilhados). Sob `--dominio tdc`: 989 elegíveis (só compartilhado, IPTU-puro excluído). Sob `--dominio iptu`: 1.843 (iptu + compartilhado).

> **Próximo passo (aguarda "vai" do dono):** ondas Drive 1–5 (incl. saneamento do lago) — o dono roda os Apps Scripts, cola os Logs em `inventario/gas-log-*.txt`, `reconciliar_arrumacao.py` fecha o loop, e aí C1–C5 do gate provam a arrumação. O Drive segue pausado até sua ordem.

---

## 10. Preparação das ondas Drive + REVISÃO POR LENTES (2026-07-04)
O dono pediu para eu **preparar e afinar por lentes** (não revisar à mão). Preparei os artefatos e rodei **3 lentes de revisão adversarial local** (sem tocar o Drive). Achados e resolução:

### Artefatos preparados
| Artefato | Papel |
|---|---|
| `scripts/semear_indice_mestre.py` → `inventario/INDICE-SEED.csv` | PLANO: 1.360 itens classificados (domínio/tipo/proveniência inferidos do de-para) |
| `scripts/reconciliar_arrumacao.py` → `inventario/INDICE-MESTRE-DRIVE.csv` + `arrumacao-log.csv` | fecha o loop: SEED + logs do GAS → estado real + trilha durável |
| `drive-arrumacao/Sanear-Lago-TDC-2026-07-04.gs` | onda 1: dedup por md5 + quarentena datada (move, não lixeira) |
| `drive-arrumacao/Organizar-Entrada-2026-07-04.gs` | onda 3: move a `_entrada` (agora emite `MOVE_LINHA` com hash) |
| `scripts/gate-arrumacao.py` | gate por fase (plano/execução) — não declara feito sem prova |

### Achados das lentes e resolução
| # | Lente | Achado | Resolução |
|---|---|---|---|
| F1 | GAS | "Retomável" era ficção (cursor nunca persistido) | cache de md5 em JSON no Drive + trava "só dedup após enum+hash completos" |
| F2 | GAS | sem Drive API, dizia "0 duplicados" (falso-limpo) | **ABORTA** com mensagem clara se o serviço avançado estiver desligado |
| F3 | GAS | `moveTo` arranca arquivo multi-pai de pasta boa | multi-pai → `MULTI_PAI_MANUAL` (não move; decisão humana em 99) |
| F4 | GAS | fallback nome+tamanho prometido e ausente | removida a promessa; md5 é obrigatório (mais seguro que nome+tamanho) |
| F5 | GAS | dedup sobre hashing incompleto | trava: só agrupa quando 100% enumerado+hasheado |
| F7/F10 | GAS | data chumbada; reset apagava tudo | data via `formatDate`; reset só do cache deste script |
| A1 | índice | 2.4 Federal=compartilhado contradizia o SSOT git (iptu) | 2.4 base=iptu + inferência bumpa só EC132/PDE/LPUOS/COE/registro/tombados |
| A2/A3 | índice | jurisprudência oficial virava doutrina; mapas viravam "lei" | override de tipo por título (juris→jurisprudencia, mapa→geo) |
| A4 | índice | capturas e-SAJ marcadas OFICIAL | `RE_NOSSO` estendido (e-saj/portal/captura → NOSSO) |
| B2/B3 | índice | status fora do enum; vigência PENDENTE à toa | status=`carimbado`; `vigencia_inicio` extraída do ano no título |
| R1/R2 | reconc. | loop não fechava; seeder sobrescreveria a execução | `reconciliar_arrumacao.py` novo; SEED (seeder) × MESTRE (reconciliador) separados |
| R3 | reconc. | Organizer só logava contadores (C5 insatisfazível) | Organizer emite `MOVE_LINHA drive_id,folderId,md5,bytes,status` |
| R4 | reconc. | ações do lago sem linha no índice; canônica podia ser NOSSA | UPSERT + bloqueio se OFICIAL quarentenado sob canônica NOSSA |
| R5 | reconc. | `hash_sha256` carregava md5 | coluna renomeada `hash_md5` (schema, seeder, reconc., gate) |
| R6 | taxon. | dois esquemas (junho × Opção B) | adotada JUNHO p/ executar; Opção B = backlog de reorg futura (§2) |
| R11 | gate | estados terminais (triagem/inbox) davam falso-vermelho | `triagem` como estado resolvido, fora do denominador de pendência |
| R12 | gate | exit-code verde em 'plano' enganava CI | flag `--require-executed` (exit 4 se Drive não executado) |

### R8 e R9 — ENDEREÇADOS (2ª rodada autônoma, 2026-07-04)
- **R8 — canônicas do lago tipificadas (não mais órfãs):** o Sanear agora emite `INV_LINHA drive_id,"nome",md5,bytes` de TODO o lago. O reconciliador **classifica cada canônica pelo nome** (reusa `semear_indice_mestre.classificar`) e a INDEXA com tipo/domínio/`destino_path` — deixa de ser órfã no legado. *(O move físico da canônica p/ a pasta-tipo é a onda de reingestão — um GAS análogo ao Organizar, dirigido pelo MESTRE; a classificação/índice já está pronta.)*
- **R9 — dedup GLOBAL cross-tree:** o reconciliador agrupa por `hash_md5` TODOS os itens colocados (`moved`/`espelhado`), de `_entrada` E do lago. Cópia byte-idêntica entre árvores → elege a canônica (maior oficialidade) e emite as extras em `inventario/cross-tree-dups.csv` p/ um GAS de quarentena consumir. A promessa "canônica única" passa a valer ENTRE árvores, não só dentro. Surfaçado no gate (não escondido).
- **A prova só existe após o dono rodar os GAS:** enquanto `gas-log-*.txt` não existir, o gate fica em fase 'plano' — honesto, não falso-verde.
