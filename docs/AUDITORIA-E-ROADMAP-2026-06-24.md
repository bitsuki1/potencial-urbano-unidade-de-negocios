# Auditoria Profunda + de Decisões + Roadmap de Alto Nível — Potencial Urbano
> **Chapéu:** orquestrador do Potencial Urbano (D104) · **Data:** 2026-06-24 · **Branch:** `claude/project-audit-roadmap-2thi1g`
> **Método:** confronto do discurso (docs) contra o estado REAL (código rodado, contagens medidas) — RO-24 (triplo-limpo), D12/D82 (lente diferente da que construiu). Não reafirma de memória: prova.
> **Lente honesta:** dá crédito ao que está sólido E declara o que está armado-mas-não-destravado. Auditoria não é teatro (D108).

---

## 0. Veredito em uma linha
**O TUBO está provado; o PRODUTO não começou.** A esteira RAG determinística existe e foi provada fim-a-fim — mas sobre a Lei **7.228/1968 (IPTU-adjacente), NÃO sobre TDC**, que é a base inicial decidida pelo MOU (D-PU-3). O alvo declarado do projeto (TDC) tem **corpus vazio (0 indexado)** e o engine TDC roda **sem combustível** (`tabelas/` vazia). O projeto está **ARMADO, não DESTRAVADO** para o seu próprio objetivo.

---

## 1. O que foi VERIFICADO (rodado, não lido)

| Alegação no repo | Verificação | Resultado |
|---|---|---|
| Esteira RAG provada fim-a-fim, 8/8 evals ativos verdes | `python3 evals/rodar-evals.py` | ✅ **8/8 PASS** (4 positivos + 4 negativos de gate 1.7) sobre a 7.228/1968 |
| 3 evals TDC ficam como spec aguardando verbatim | idem | ✅ **3 FALHA honestas** — `NÃO-FUNDAMENTADA` (corpus TDC vazio); não inflam o build |
| Engine OODC é código determinístico auto-testado | `scripts/fechar-instancia.py` | ✅ auto-teste **OK**; engine exige `V`/`CA_max`, **não inventa** (demo rotulada ILUSTRATIVA) |
| 13 leis indexadas (12 federais + 7.228) | `ls rag/chunks/` | ✅ **13 dirs**; `leis/federal/` = 12 pares `.md`+`.json` |
| 15 municipais ainda não-verbatim | `ls leis/municipal-sp/` | ✅ **15 `.md`** `bruto`/resumo — a guarda do `fatiar.py` corretamente as recusa |
| Jurisprudência 32 ingerida | `ls jurisprudencia/*.md` | ✅ **32** |
| MANIFESTO idempotente, sem stray tags | gate | ✅ **VERDE** (regenerado == commitado) |
| `tabelas/` vazia (engine sem combustível) | `ls tabelas/` | ✅ **VAZIA** — confirma B-1; engine roda só sobre valor de teste |
| `tese/` gerada | `ls tese/` | ✅ **VAZIA** (esperado — gerada pela Action quando houver corpus) |

**Único vermelho do gate:** `BACKLOG.md` com header datado 2026-06-21 (frescor D83) — o mecanismo de frescor **pegou staleness de 3 dias**, exatamente o que deve fazer. Não é defeito de produto. (Corrigido nesta sessão após revisar as ABERTAS.)

---

## 2. Auditoria de DECISÕES

### 2.1 Saúde do registro decisório — SÓLIDA
Três registros, coerentes e dialéticos:
- **`CLAUDE.md` (constituição, Partes 1–4):** princípios invioláveis 1.1–1.7. Estáveis, citados pelo código.
- **`CODEX-DO-PROJETO.md`:** RO-01..RO-24 (regras de ouro) + **D-01..D-12** (decisões de arquitetura em TESE/ANTÍTESE/VACINA). Bem vacinado.
- **`DO_ESCRITORIO.md`:** D-PU-1..D-PU-5 (diretrizes do PMO) — todas resolvidas ou em vigor.

**Decisões resolvidas e firmes (não reabrir):**
- **D-PU-3 — base inicial = TDC** (MOU 2026-06-20). Encerra a divergência IPTU×TDC.
- **D-05 — RAG determinístico** (BM25 + metadados, sem LLM/embeddings no tier base). Semântico é extensão futura plugável.
- **D-06 — guarda de verbatim** (só texto integral entra no RAG; resumo mente sobre a fonte).
- **D-07 — re-ingestão verbatim é INTERNA quando o cru já está local** (vacina AUD-01: ".md diz 403" ≠ "verbatim não existe"). Saltou o corpus de 1→13 leis.
- **D-08 — número nasce no engine como CÓDIGO**; fórmula em `.md` = número nascendo no LLM (proibido).
- **D-09 — mecanismo anti-perda ("ladrão"/BACKLOG + gate)**; sobrevive à saturação de contexto (modo de falha nº1).
- **D-10/D-12 — auditar com lente DIFERENTE** (D82): a 2ª auditoria pegou o falso-verde do gate e o valor inventado que a 1ª não viu. **Mecanismo que provou valor.**
- **Supabase adotado** — projeto SEPARADO `potencial-urbano-iptu-tdc`, limpo por decisão (RO-23).

**Postura AMORAL (D106/D-PU-AMORAL):** LGPD/PII e senhas = risco PERMANENTEMENTE ACEITO. Não levantar ao MOU. Mecanismo permanece (RLS deny-all). Esta auditoria **não** abre nada disso.

### 2.2 A CONTRADIÇÃO central (o achado da auditoria de decisões)
> **Decisão estratégica (D-PU-3): "a base inicial é TDC".**
> **Realidade do pipeline: 100% do que foi provado é IPTU-adjacente (7.228/1968); 0% TDC.**

Não é incoerência de má-fé — é o limite físico em que a instância anterior parou e **declarou honestamente** (PROXIMA-INSTANCIA §DESTRAVE-MESTRE). A causa é uma só: **não há verbatim TDC no repo**, e obtê-lo esbarra em dois muros: (a) egress `.gov.br` = HTTP 403; (b) Drive = lane exclusiva (cerca anti-conflito). **Este é o bloqueio nº1 do projeto** — tudo de PRODUTO depende dele.

### 2.3 Decisões PENDENTES do MOU (cobrança com recomendação — RO-22)
1. **Canal para obter verbatim TDC do Drive (B-9) — o destrave nº1.**
   → *Recomendo:* abrir o **PEDIDO-AO-DRIVE** consolidando B-1 (tabelas Q14/Quadro 3) + B-4 (14 municipais) + alerta B-8/AUD-02, **OU** autorizar rodar a re-ingestão de um ambiente com egress liberado. Sem isso, o produto não anda.
2. **Drive: executar o DELETE das duplicatas (D79 já decidido) — quando?**
   → *Recomendo:* só após conferir AUD-02 (IDs canônicos trocados — risco de apagar ~3 GB errado): cada ID "manter" validado por `get_file_metadata` ANTES de `DRY_RUN=false`.
3. **2 jurisprudências fora de escopo (P3):** `stf-tema-1020` (ISS) e `stj-resp-1658054` (previdenciário, nº não verificado).
   → *Recomendo:* realocar a 1ª p/ anexo "correlatos" e arquivar a 2ª como ponto cego declarado.

---

## 3. Pontos cegos DECLARADOS (o que esta e as auditorias anteriores NÃO cobriram)
Honestidade D24 — declarar o que ficou de fora vale mais que fingir cobertura:
- **A DIMENSÃO DADO/PRODUTO — a maior lacuna.** Todas as auditorias miraram o artefato **Lei/RAG**. **Tabela, Fórmula-com-dado e a base de imóveis (IPTU 2026 ~1M linhas, `socios.csv` 3,4 GB, série ITBI) nunca foram auditadas/ingeridas/validadas.** 3 dos 4 artefatos seguem sem varredura. O produto real (Fase 2/3 do Codex) é o **cruzamento** desses — e ele ainda não existe.
- **OCR/legibilidade dos PDFs do Drive não verificada** (D-PU-OCR): re-ingerir scan sem OCR traz alucinação que "parece citação". Validar texto×imagem ANTES de re-ingerir.
- **Mérito JURÍDICO das teses (B-10) não auditado** — só proveniência/fidelidade. O conteúdo jurídico-tributário em si segue sem revisão tema-a-tema.

---

## 4. ROADMAP DE ALTO NÍVEL
> Ordem honesta (D26): **produto puxa; higiene roda em paralelo e nunca lidera a fila.** "Armado ≠ destravado."

```
HORIZONTE      OBJETIVO                                    BLOQUEIO        ESTADO
────────────────────────────────────────────────────────────────────────────────
H0 (crítico)   Destravar o caminho de PRODUTO = verbatim   Drive/egress    🔴 bloqueado
               TDC indexado (≥1 norma: PDE 16.050/2014)    (decisão MOU)      externamente
H1             Encher o engine com combustível REAL         Drive (Q14/Q3)  🔴 depende H0-canal
               (Tabelas V + CA_max → tabelas/)
H2             Completar o corpus jurídico                  Drive + local   🟡 parcial
H3 (o produto) Dimensão DADO: IPTU 2026 × proprietários ×   dados pesados   ⬜ não começou
               ITBI × SQL → 1ª lista de alvos por imóvel    (Drive→Supabase)
H4             Produto/operação: dossiê por imóvel +         após H1–H3      ⬜ futuro
               Supabase carregado (RO-23) + Codex Mestre
```

### H0 — Destravar o PRODUTO (TDC) · **a única coisa que importa agora**
- Obter **≥1 norma TDC verbatim** (PDE 16.050/2014 e correlatas) → `_entrada/` → `scripts/promover_entrada.py` → `fatiar`+`indexar`. **Zero código novo.**
- Aceite mecânico já pronto: os 3 evals `tdc-produto-pendente.json` viram VERDE = produto destravado.
- **Ação do MOU:** resolver o canal do Drive (decisão pendente nº1).

### H1 — Combustível real no engine (B-1, B-3)
- Ingerir **Q14 (`V` por SQL)** + **Quadro 3 (`CA_max` por ZONA)** → `tabelas/*.csv` com proveniência.
- Completar tabelas **Fs/Fp** no `oodc.py` (hoje parciais: só F-A/V3.1), cada faixa citando o quadro-fonte.
- DoD: engine roda sobre `V`/`CA_max` REAIS de ≥1 imóvel — fim do "valor ilustrativo".

### H2 — Completar o corpus jurídico (B-4, B-5, B-6, B-7, B-11)
- Re-ingerir **14/15 municipais verbatim** (precisa do Drive; mesmo `promover_entrada.py`).
- **Camada semântica** (embeddings) + filtro por `tema` → resolve a vacina "match lexical ≠ relevância semântica".
- **Grafo de remissões + vigência DATADA** por chunk (1.6) → consulta "a partir de quando vale o art. X?".

### H3 — A dimensão DADO/PRODUTO (B-2) · **a maior lacuna vira o entregável**
- Auditar/ingerir **IPTU_2026 (~1M linhas)**, `socios.csv`, série ITBI (bruto pesado → Supabase, não git — RO-23).
- **1º JOIN do produto:** `IPTU_2026` (1 distrito) ⋈ LOTES (SQL/geo) ⋈ Q14 (valor) ⋈ zoneamento (CA) → engine → **1ª lista de alvos por imóvel** {SQL, valor, oportunidade TDC/IPTU, dono}.

### H4 — Produto e operação
- Dossiê/lista de prospecção por imóvel (oportunidade + valor + dono) — o entregável final.
- Criar schemas dos 4 artefatos + geo + rag no Supabase (após organização aprovada, RO-23).
- Forjar o **Codex Mestre** (Etapa 1) — matriz de domínio escrutinada T/A/V.

### Trilha de HIGIENE (paralela, NÃO bloqueia, NÃO lidera)
- **Drive DELETE** das duplicatas (D79) — após conferir AUD-02. Causa-raiz (V-3): upload de máquinas distintas → precisa ponto único de upload + dedup no upload, senão repete.
- **Supabase API** — remover `public` dos Exposed schemas (M-41, ação física do MOU).
- **2 juris fora de escopo** (P3) · **B-10** mérito jurídico das teses · **B-12** endurecer engine (decimal-total/FATAL/citação-por-dispositivo).

---

## 5. Caminho crítico (a régua do orquestrador)
**Uma decisão do MOU destrava 80% do roadmap:** o **canal para tirar verbatim TDC + tabelas do Drive** (H0+H1). Com ele resolvido, o tubo já pronto roda sem código novo e o produto começa a existir. Sem ele, o projeto fica preso em "armado, não destravado" — auditando o que já foi auditado em vez de andar 1 lei TDC ponta-a-ponta (D26/D-PU-D2).

> **Próxima ação concreta recomendada:** abrir o PEDIDO-AO-DRIVE consolidado (B-9) e levar ao MOU as 3 decisões pendentes do §2.3 com a recomendação em cada uma.
