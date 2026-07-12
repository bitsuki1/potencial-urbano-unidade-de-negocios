# ROADMAP — Arrumação perfeita do Drive PU (pasta POTENCIAL URBANO)
> Pedido do MOU (2026-07-12): _"deixar ele perfeitamente arrumado... tudo no seu devido lugar, nada órfão
> e nada duplicado. Esta é a minha pasta principal, tudo dentro dela deve estar arrumado em pastas, sem
> exceção, catalogado e tagueado. Os duplicados enviados a UMA única pasta que depois eu limpo."_
> Pasta raiz: `POTENCIAL URBANO` = id `1BrM6q36meTtn5guJoiGbqvCtZF11Uau3` (dentro do Drive do portfólio do MOU).
> Este roadmap é o **contrato da arrumação** — para que nada se perca. Cada fase tem DoD (como PROVAR que fechou).

---
## 0. Estado atual (medido, não achismo) — catálogo `CATALOGO-DRIVE-PU-2026-07-12.csv`
- **33.138 arquivos** catalogados e tagueados (tema · tipo · oficialidade · já-indexado · uso · duplicata).
- Topo da pasta HOJE (bagunça confirmada no print do MOU):
  `00 — Governança & Índice` · `01 — _entrada` · `02 — Leis & Jurisprudência` · `03 — Tabelas & Engines` ·
  `04 — Tese` · **`05 — Geo / Mapas`** · **`05 — Geo`** (← DOIS "05", colisão) · **`TODOS TDC`** (DataLake de
  ~27 mil fragmentos despejado na raiz) + **337 arquivos soltos** fora de qualquer subpasta.
- Classificação por **auditabilidade** (regra do MOU: só se constrói no que se pode auditar):

| Classe (`uso`) | Qtd | O que é | Destino na arrumação |
|---|---:|---|---|
| **USAR** | 396 | Documento oficial que PODEMOS auditar (lei/decreto/portaria/jurisprudência/tabela-fonte) | Canônico (02/03/04/05) |
| **COMERCIAL** | 64 | Listas para achar proprietário (a exceção que o MOU liberou) | Canônico (`06 — Comercial`) |
| **SO_IDEIA** | 23.700 | Chunk/imagem/fragmento/SILVER **não feito por nós** — serve de ideia, NÃO de alicerce | Zona bruta `90` (fora do canônico) |
| **DESCARTE** | 8.978 | Duplicata forte (8.309) + lixo (logs, temporários) | **`99 — APAGAR` (pasta ÚNICA)** |

> O grosso (23.700 SO_IDEIA) é a "matéria-prima" do DataLake `TODOS TDC`: útil como referência, mas **não
> é canônica** (não podemos auditar a origem). Não se apaga (é ideia), mas sai da frente do que é oficial.

---
## 1. Taxonomia canônica ALVO (o "devido lugar" de tudo)
Todo arquivo cai em EXATAMENTE uma destas pastas de 1º nível (sem exceção, nada na raiz solto):

```
POTENCIAL URBANO/
├── 00 — Governança & Índice     → índice, catálogo, este roadmap, decisões, MANIFESTO
├── 01 — _entrada (despejo)      → zona de despejo do bruto novo (IPTU+TDC) antes de triar
├── 02 — Leis & Jurisprudência   → texto normativo OFICIAL auditável (lei/decreto/portaria/acórdão) [fonte do RAG]
├── 03 — Tabelas & Engines       → tabelas extraídas (CSV) + referência dos motores
├── 04 — Tese (Antítese/Vacina)  → camada argumentativa
├── 05 — Geo / Mapas             → geo/mapas (as DUAS pastas "05" FUNDIDAS em uma)
├── 06 — Comercial               → listas de proprietário / prospecção (exceção liberada) [NOVA]
├── 90 — Material bruto (só ideias, NÃO auditável)  → DataLake TODOS TDC + chunks/imagens/fragmentos [NÃO canônico]
└── 99 — APAGAR (duplicados e descarte)  → pasta ÚNICA; o MOU limpa depois
```
**Regras de ouro da taxonomia:**
1. **Nada órfão:** nenhum arquivo direto na raiz nem solto — todo item mora numa das 10 pastas acima.
2. **Nada duplicado no canônico:** duplicata forte → `99`, mantendo **1 cópia canônica** por grupo (keep-canonical).
3. **Não-auditável isolado:** o que não foi feito por nós (chunk/imagem/fragmento/SILVER) fica em `90`, nunca em 02–06.
4. **Uma pasta APAGAR só** (`99`) — reversível; o MOU exclui quando quiser.
5. **Catálogo é o razão:** cada arquivo tem uma linha (id·nome·pasta-destino·tema·tipo·uso). Fonte da verdade da arrumação.

---
## 2. As fases (com DoD — prova mecânica de fechamento)

### Fase 1 — Congelar o mapa e resolver as colisões de topo  *(barato, sem mover arquivo)*
- Consolidar o de-para **arquivo → pasta-destino** para os 33.138 (já existe a base: `CATALOGO-DRIVE-PU`,
  `APAGAR-DE-PARA.csv`, `CORPUS-UTIL-DRIVE.csv`). Preencher `pasta_destino` para 100% das linhas.
- Decidir a fusão dos **dois "05"** (Geo / Mapas + Geo) → uma pasta `05 — Geo / Mapas`.
- Classificar os **337 órfãos da raiz** (cada um recebe pasta-destino).
- **DoD:** `arrumar-de-para.csv` com `pasta_destino` preenchida em **33.138/33.138** linhas (0 vazias); relatório
  de colisões/órfãos zerado no papel.

### Fase 2 — Duplicatas → `99 — APAGAR` (pasta única)  *(em grande parte JÁ FEITO)*
- A sessão anterior já moveu **8.976** arquivos (`APAGAR-DE-PARA.csv`) via Action `mover-para-apagar.yml`
  (conta de serviço / robô) para a pasta "APAGAR — duplicados e descarte (PU 19)". **2 falharam** (SA sem
  alcance) — reprocessar. Confirmar que é a pasta ÚNICA e renomeá-la para `99 — APAGAR`.
- **DoD:** `dup_forte=SIM` e `descarte=SIM` = **0 fora de `99`**; log da run bate a contagem (8.978 movidos).

### Fase 3 — Material bruto / não-auditável → `90`  *(o grosso do volume)*
- Renomear/reposicionar o `TODOS TDC` como `90 — Material bruto (só ideias)` OU mover os 23.700 SO_IDEIA
  para `90`. **Antes**, PUXAR de dentro dele os oficiais auditáveis (`01A_BRONZE_OFICIAL`, ~PDFs de lei
  reais que viram USAR) para a Fase 4.
- **DoD:** `uso=SO_IDEIA` = **0 fora de `90`**; nenhum PDF oficial (USAR) preso dentro de `90`.

### Fase 4 — Canônico no devido lugar (as 460 que importam)
- Mover os **396 USAR** para `02` (lei/decreto/portaria/jurisprudência), `03` (tabela), `04` (tese) e `05`
  (geo), por `tema`+`tipo_artefato`. Os **64 COMERCIAL** para `06`.
- Cruzar com o corpus `leis/` do repo: o que é USAR e ainda não está ingerido entra na fila (`GAP-INGESTAO`).
- **DoD:** 100% das linhas USAR/COMERCIAL com pasta-destino canônica atingida; catálogo re-lido bate o Drive real.

### Fase 5 — Órfãos zerados
- Varrer a raiz: nenhum arquivo direto; os 337 (Fase 1) todos realocados.
- **DoD:** listagem da raiz = só pastas (0 arquivos soltos); `path` vazio no catálogo = 0.

### Fase 6 — Catalogar & taguear (selo final) + verificação
- Recatalogar a pasta inteira já arrumada → catálogo final com `pasta_destino` = pasta real.
- **DoD (o selo "perfeitamente arrumado"):**
  (a) todo arquivo em uma das 10 pastas (0 órfão);
  (b) 0 duplicata forte fora de `99`;
  (c) 0 SO_IDEIA fora de `90`;
  (d) 100% catalogado e tagueado;
  (e) relatório final `fonte × destino` publicado em `00 — Governança & Índice`.

---
## 3. Como executa (mecânica) — e a trava anti-runaway
- **Motor de movimento:** conta de serviço (o "robô"), via Action, **MOVE (não apaga)** — reversível.
  Já existe `scripts/mover_para_apagar_sa.py` + `.github/workflows/mover-para-apagar.yml` (ENSAIO primeiro,
  depois real). Generalizar para `mover_por_destino_sa.py` (lê `arrumar-de-para.csv`: `drive_id → pasta_destino`).
- **Ensaio SEMPRE antes do real** (`DRY_RUN=true`) — confere contagem por pasta-destino antes de mexer.
- **Catalogação:** trabalhadores **TRAVADOS** (proibido spawnar sub-agentes; recursão sequencial própria) —
  lição do runaway da sessão de catálogo. Dedup por `drive_id` (o conector Drive tem bug de paginação).
- **Idempotente:** rodar 2× não duplica movimento (já-na-pasta-destino é no-op).

## 4. O que depende do MOU (decisões de dono, D21)
1. **Confirmar a taxonomia** (00–06 + 90 + 99) — em especial a pasta `90` para o não-auditável (manter como
   referência) e a `06 — Comercial`.
2. **`90` fica ou some?** Alternativa: mandar TODO o `TODOS TDC` (SO_IDEIA) para `99 — APAGAR` também
   (se o MOU não quiser guardar nem como ideia). Default proposto: **guardar em `90`** (é ideia, não lixo).
3. **Autorizar o real** (o ensaio roda sozinho; o `DRY_RUN=false` que move de verdade é o gate humano).

## 5. Ativos já prontos (não se refaz)
- `CATALOGO-DRIVE-PU-2026-07-12.csv` (33.138 tagueados) · `APAGAR-DE-PARA.csv` (8.978) ·
  `CORPUS-UTIL-DRIVE.csv` (460 úteis) · `GAP-INGESTAO-OFICIAIS.csv` (48 normas oficiais faltando no corpus) ·
  `scripts/mover_para_apagar_sa.py` + Action · `MAPA-TODOS-TDC-DATALAKE.md`.
