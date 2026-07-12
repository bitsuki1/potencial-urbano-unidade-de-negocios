# ROADMAP — Arrumação perfeita do Drive PU (pasta POTENCIAL URBANO)
> Pedido do MOU (2026-07-12): _"deixar ele perfeitamente arrumado... tudo no seu devido lugar, nada órfão
> e nada duplicado. Esta é a minha pasta principal, tudo dentro dela deve estar arrumado em pastas, sem
> exceção, catalogado e tagueado. Os duplicados enviados a UMA única pasta que depois eu limpo."_
> Pasta raiz: `POTENCIAL URBANO` = id `1BrM6q36meTtn5guJoiGbqvCtZF11Uau3` (dentro do Drive do portfólio do MOU).
> Este roadmap é o **contrato da arrumação** — para que nada se perca. Cada fase tem DoD (como PROVAR que fechou).

---
## ✅✅ ARRUMAÇÃO CONCLUÍDA E SELADA (2026-07-12) — ver `inventario/SELO-ARRUMACAO-DRIVE-PU.md`
Run real `29208161824` (erros=0): movidos=2.417 · fica_no_90=22.057 · 2ª lixeira fundida. Selo SA
(run `29211180386`): **0 órfão na raiz · lixo numa pasta só · nada oficial no lixo · tudo em pasta.**
Pendência cosmética: 2 pastas vazias (`05 — Geo`, `99 — DUPLICATAS-A-EXCLUIR`) o MOU exclui.

## ★ ESTADO DA EXECUÇÃO (2026-07-12) — ENSAIO VERDE, aguardando "pode mover" do MOU
- **De-para pronto:** `inventario/drive-pu/ARRUMAR-DE-PARA.csv` (33.138 arquivos → destino). Distribuição:
  **90** (bruto) 22.268 · **99** (APAGAR) 8.603 · **02** 1.422 · **05** 641 · **03** 140 · **00** 64.
- **Motor pronto:** `scripts/mover_por_destino_sa.py` + Action `arrumar-drive.yml` (robô SA, MOVE não apaga).
- **Ensaio (DRY_RUN) rodado 2× — VERDE.** Validado contra o Drive real: renomeia **TODOS TDC → `90`**
  (22.057 SO_IDEIA ficam no lugar, 0 movimento), reaproveita a APAGAR legada como **`99`** e **funde**
  a 2ª lixeira `99 — DUPLICATAS-A-EXCLUIR`, protege norma oficial do lixo. **~11.081 movimentos no teto**
  (~8.600 do APAGAR já lá desde a sessão anterior → idempotente `ja_la`; reais ≈ 2.500 keepers + 211 órfãos).
- **FALTA só o gate humano:** disparar a Action com `dry_run=false` (o "pode mover" do MOU). Reversível.

## 0. Estado atual (medido, não achismo) — catálogo `CATALOGO-DRIVE-PU-2026-07-12.csv`
- **33.138 arquivos** catalogados e tagueados (tema · tipo · oficialidade · já-indexado · uso · duplicata).
- Topo da pasta HOJE (bagunça confirmada no print do MOU):
  `00 — Governança & Índice` · `01 — _entrada` · `02 — Leis & Jurisprudência` · `03 — Tabelas & Engines` ·
  `04 — Tese` · **`05 — Geo / Mapas`** · **`05 — Geo`** (← DOIS "05", colisão) · **`TODOS TDC`** (DataLake de
  ~27 mil fragmentos despejado na raiz) + **337 arquivos soltos** fora de qualquer subpasta.
- Classificação por **auditabilidade** (regra do MOU: só se constrói no que se pode auditar). **O sinal certo de
  "auditável" é `oficialidade=OFICIAL` E não-duplicado** — mais largo que o `uso=USAR` (que era estreito demais):

| Classe (refinada) | Qtd | O que é | Destino na arrumação |
|---|---:|---|---|
| **KEEPERS canônicos** (OFICIAL não-dup + USAR + COMERCIAL) | **~2.126** | Doc oficial auditável: **982 jurídico** (596 leis · 337 decretos · 66 portarias · 31 jurisprudência) + **854 geo** + 77 TDC + 8 IPTU + comercial | Canônico (02/03/04/05/06) |
| **RESGATE** (doc oficial MAL-TAGUEADO, nome único) | **~396** | PDFs/DOCs com assinatura de norma (Lei/Decreto/Portaria/Resolução/Quadro/PDE) que o tagueador marcou "DESCONHECIDO" — **173 presos na LIXEIRA** | Segunda-olhada → canônico (Fase 3.5) |
| **SO_IDEIA** (só ideia) | ~22.341 | Chunk/imagem/fragmento/SILVER **derivado, não feito por nós** — serve de ideia, NÃO de alicerce | Zona bruta `90` (após o resgate) |
| **APAGAR** (duplicata + lixo) | ~8.300 | Duplicata forte (mantém 1 canônica) + lixo (logs, sidecars, temporários) | **`99 — APAGAR` (pasta ÚNICA)** |

> **⚠️ "TODOS TDC" NÃO é só não-auditável (correção do MOU, 2026-07-12).** Dentro dele o `01A_BRONZE_OFICIAL`
> tem ~1.197 OFICIAIS e a própria `99_LIXEIRA` esconde ~351 docs oficiais de nome único (Quadros do PDE 2013,
> Resoluções SMUL, tombamentos, leis como a L16642). Por isso NADA vai para `90`/`99` **antes** da Fase de
> Resgate (3.5) varrer os não-keepers por assinatura de nome. Lista pronta: `inventario/drive-pu/RESGATE-CANDIDATOS.csv`.
> O grosso (SO_IDEIA) é a matéria-prima do DataLake: referência, não canônico — guardado em `90` (o MOU olha 1-a-1 depois).

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

### Fase 3.5 — RESGATE (o ponto que o MOU mandou olhar direito) — ANTES de mandar nada pro 90/99
- Varrer TODOS os não-keepers por **assinatura de nome** (Lei/Decreto/Portaria/Resolução/Acórdão/Quadro/PDE/
  LPUOS + nº) → lista `RESGATE-CANDIDATOS.csv` (**396**: 39 leis + 39 decretos + 16 portarias + 9 jurisprudências
  + 274 PDFs, dos quais **173 na LIXEIRA**). Segunda-olhada (barata, por nome+hash): confirma oficial → **puxa pro
  canônico** (02/05), não pro 90/99.
- Cruzar com `leis/` do repo: resgatado que ainda não está no corpus entra em `GAP-INGESTAO-OFICIAIS.csv`.
- **DoD:** cada linha do `RESGATE-CANDIDATOS.csv` decidida (canônico | é-dup-real→99 | é-ideia→90); **0** doc com
  assinatura de norma sobrando em `90`/`99` sem decisão registrada.

### Fase 3 — Material bruto / só-ideias → `90`  *(o grosso do volume, só DEPOIS do resgate)*
- Mover o residual `SO_IDEIA` (~22.341: SILVER derivado, chunks, imagens, fragmentos) para `90 — Material bruto`.
  Renomear `TODOS TDC` → `90 — Material bruto (só ideias)` e esvaziar dele o que foi resgatado (3.5) e o que é dup (2).
- **DoD:** `uso=SO_IDEIA` = **0 fora de `90`**; nenhum candidato de resgate não-decidido preso em `90`.

### Fase 4 — Canônico no devido lugar (~2.126 keepers + resgatados)
- Mover os **~2.126 keepers** (+ os resgatados na 3.5) para o canônico por `tema`+`tipo_artefato`:
  **982 jurídico → `02`** · **854 geo → `05`** · tabelas → `03` · tese → `04` · **64 comercial → `06`**.
- Cruzar com o corpus `leis/` do repo: keeper/resgatado ainda não ingerido entra na fila (`GAP-INGESTAO-OFICIAIS.csv`).
- **DoD:** 100% dos keepers/resgatados com pasta-destino canônica atingida; catálogo re-lido bate o Drive real.

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

## 4. Decisões do MOU (D21) — JÁ TOMADAS (2026-07-12)
1. ✅ **Taxonomia aprovada** (00–06 + 90 + 99) — "de acordo".
2. ✅ **`90` GUARDA** o material bruto/só-ideias — "guarda, depois da arrumação iremos olhar um por um".
3. ✅ **"TODOS TDC não é só não-auditável"** — obrigatória a Fase de Resgate (3.5) antes de 90/99. FEITO o
   mapeamento (396 candidatos em `RESGATE-CANDIDATOS.csv`).
- Resta só **autorizar o `DRY_RUN=false`** (o real) — o ensaio roda sozinho; mover de verdade é o gate humano.

## 5. Ativos já prontos (não se refaz)
- `CATALOGO-DRIVE-PU-2026-07-12.csv` (33.138 tagueados) · `APAGAR-DE-PARA.csv` (8.978) ·
  `CORPUS-UTIL-DRIVE.csv` (460 úteis) · `GAP-INGESTAO-OFICIAIS.csv` (48 normas oficiais faltando no corpus) ·
  `scripts/mover_para_apagar_sa.py` + Action · `MAPA-TODOS-TDC-DATALAKE.md`.
