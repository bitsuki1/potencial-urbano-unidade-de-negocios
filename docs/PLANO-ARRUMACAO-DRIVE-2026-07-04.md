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

**Lago legado congelado:** o `TODOS TDC` (março/2026, ~1.000+ arquivos, 3 cemitérios de duplicata) **não é reorganizado arquivo-a-arquivo** — vai inteiro para `98 — _LEGADO` como read-only. Saneá-lo é onda separada, só se/quando precisar.

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
**Um** arquivo versionado no git: `inventario/INDICE-MESTRE-DRIVE.csv` (o Drive é espelho; o CSV é a autoridade). Colunas exatas (20):

```
drive_id, nome_origem, nome_canonico, tipo_artefato, dominio, dominio_primario,
proveniencia, oficialidade, confianca, vigencia_inicio, vigencia_fim,
substitui, substituido_por, destino_classe, destino_path,
hash_sha256, bytes, mime, id_pipeline, status_arrumacao, observacao
```
`status_arrumacao ∈ {bruto, carimbado, moved, quarentena, espelhado}`. Herdado pelo pipeline (`promover_entrada.py` lê `nome_canonico`/`dominio`/`proveniencia` do índice — zero re-trabalho).

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
3. **Dedup por hash** — mesmo `hash_sha256` = 1 canônica; irmãs viram `substituido_por`.
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
5. Todo item `moved` tem `hash_sha256` preenchido.
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

## 7. Decisões que são do DONO (gate humano — não decido sozinho)
1. **Lista compartilhado (§4):** confirma as 7 reclassificações? (EC 132, PDE 16.050, LPUOS 16.402, Estatuto da Cidade, CF 182-183, CTN geral, Quadro 14). Alguma sai/entra?
2. **PDE per-dispositivo agora ou depois?** Recomendo `dominio_primario: compartilhado` **já** e quebra por-dispositivo **numa onda futura** (não bloqueia nada).
3. **Lago `TODOS TDC` → congelar em `98`** (recomendado) **ou** sanear arquivo-a-arquivo agora (caro, adia o resto)?
4. **Ordem de entrega:** posso começar **já** pela parte 100% local e reversível (schema `dominio[]` + código `fatiar/indexar/consultar` + `gate-arrumacao.py` + eval de domínio) — tudo na branch, sem tocar o Drive — enquanto você decide 1–3. O Drive (ondas 3–5) só roda com seu "vai".

---

## 8. O que já está pronto para acoplar (não recomeçar)
- `drive-arrumacao/de-para-COMPLETO-2026-07-04.csv` (1.360 arquivos da `_entrada` classificados) → vira as ondas 0–2 do índice-mestre.
- `drive-arrumacao/Organizar-Entrada-2026-07-04.gs` (move os 1.360) → é a **onda 3** para a `_entrada` (falta só o dono rodar).
- `inventario/PESADOS-PARA-SUPABASE.csv` + `inventario/classificacao-*.csv` → alimentam o mapa do §5.
- Enumerações do Drive já coletadas (TABELAS, MOTOR_1, subárvores) → semente do índice-mestre para além da `_entrada`.

---
> **Próximo passo proposto:** com o **de acordo do dono no §7.4**, executo a parte LOCAL (schema + código + gate + eval) nesta branch e trago os diffs para revisão; o Drive fica pausado até o "vai" das ondas 3–5.
