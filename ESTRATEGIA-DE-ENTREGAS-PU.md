# ESTRATÉGIA DE ENTREGAS — Potencial Urbano

> **Lente: especialista em loop de IA.** PU 15 · 2026-07-01 · branch `claude/potencial-urbano-strategy-kp9bgr`.
> **O que este documento é:** o mapa do processo inteiro da PU + a leitura do roadmap + a estratégia
> para chegar à **ferramenta comercial completa, auditável e com dados ricos** — dizendo **quais lentes
> (Gens) acionar, em que ordem, e o que cada uma destrava**.
> **Doutrina aplicada:** zero-compressão · dialético · agnosticismo · nada se descarta · número nasce no
> engine (1.3) · citação obrigatória (1.7). Estado medido, não declarado (SSOT = `MANIFESTO.json` + gate).
> **Não altera a constituição** (`CLAUDE.md`) nem decisão de negócio — é plano de execução (D21, gate do projeto).

---

## 0. VEREDITO (uma linha, honesto)

A **ferramenta comercial já EXISTE e está no `main`** — a lista de cedentes ZEPEC (6.131 imóveis, 2.740
prontos para abordar), com engine determinístico e citação. O que falta para ela ser **completa · auditável ·
rica** **não é mais construir o trilho — é ENCHER de dado e FECHAR 3 lacunas de prova**. E o gargalo central,
lido pela lente de loop de IA, é este: **~70% do que falta o loop de IA destrava sozinho (trabalho LOCAL);
~30% exige UM passo de infra/decisão do MOU (dado pesado + confirmação de fonte).** A estratégia abaixo
maximiza o throughput local e concentra o externo num **pedido único**.

---

## 1. O MAPA DO PROCESSO — a máquina PU vista como loop de IA

A PU não é um programa; é um **loop de instâncias de IA** que se passam o bastão pelo Git. Entender o loop é
pré-requisito para entregar por ele.

### 1.1 — O ciclo de uma instância (o "loop externo")
```
  boot (hook surface-backlog.sh)  →  lê estado do GIT (não da conversa)
        │                              PROXIMA-INSTANCIA → HANDOFF → MANIFESTO → BACKLOG
        ▼
  instância CRIA arquivos novos (1 por lei / 1 por tabela / 1 script)   ← criação paralela (1.5)
        │
        ▼
  push  →  GitHub Action consolidar.yml  →  REGENERA MANIFESTO + índice RAG + mestres (determinístico)
        │                                   consolidação serial, Git nunca dá conflito (1.5)
        ▼
  GATE mecânico  fechar-instancia.py  ("declarei feito" ≠ "provei feito", D83)
        │                              evals(1.7) · engine(1.3) · sem stray tags · MANIFESTO idempotente
        ▼
  handoff sem perdas  →  BACKLOG (o "ladrão" D83 captura o que cairia) + PROXIMA-INSTANCIA + REGISTRO
```
**Leitura de loop de IA:** o mecanismo anti-perda (BACKLOG surfaçado no boot + gate no fechamento) é o que
impede a falha nº1 do loop — *"uma determinação é adiada para 'a próxima janela' e CAI"*. **Toda entrega desta
estratégia tem de nascer com DoD mecânica no BACKLOG, ou o loop a perde.**

### 1.2 — O pipeline de produto (o "loop interno" — funil de 5 etapas + 3 camadas)
Da constituição (Parte 3) e do handoff (`HANDOFF-E-PENDENCIAS.md §1`), o produto é um RAG consultável **por
imóvel (SQL)** que responde três perguntas, em três camadas:

| Camada | Pergunta | Onde vive | Estado |
|---|---|---|---|
| **Jurídico — "o PODE"** | dá para mexer no IPTU / vender TDC? | RAG (`leis/`+`rag/`), engine `pcpt.py`/`oodc.py` | ✅ montado e provado (1.7/1.3) |
| **Precificação — "o QUANTO"** | quanto vale? | `CODEX-PRECIFICACAO-TDC.md` (engine `art128.py`) | ⏸️ **PARADO** (decisão MOU 2026-06-28) |
| **Proprietário — "o QUEM"** | quem é o dono? | ITBI/IPTU/socios → Supabase | 🔒 parcial (79 donos; falta escala) |

Esteira: **E1 corpus → E2 preço → E3 proprietários → E4 cruzamento (motor) → E5 produto (lista por imóvel).**

### 1.3 — Os DOIS produtos (não confundir — é a maior fonte de confusão do repo)
| Produto | Lado | O que é | Onde está |
|---|---|---|---|
| **A — Cedentes ZEPEC** (via 1) | CEDENTE (vende TDC) | lista de 6.131 tombados que podem vender potencial | ✅ **no `main`** (`zepec/ferramenta/`) — a "ferramenta comercial" **é este** |
| **B — Alvos por imóvel** (OODC) | RECEPTOR (compra/paga outorga) | lista ranqueada IPTU×valor×dono via engine OODC | 🔒 **preso** na branch `project-audit-roadmap-2thi1g` (B-17, cross-repo/MOU) |
> A frente comercial VIGENTE (contrato OPIT-SP / Bairro Vivo, `CODEX-COMERCIAL-TDC.md §5.2`) é o **Produto A**.
> O Produto B é receptor e depende de merge a `main` protegido → **decisão do MOU**, não do loop.

---

## 2. ESTADO MEDIDO (âncora — números do `MANIFESTO.json` + gate, 2026-07-01)

- **Gate mecânico:** evals(1.7) VERDE · engine(1.3) VERDE · sem stray tags VERDE · MANIFESTO idempotente VERDE.
- **Corpus:** 63 itens (31 leis + 32 juris); **61 no escopo**; **17 leis indexadas** (TDC ligado no `main`: eval
  `tdc-potencial-construtivo-lpuos` verde, LPUOS 16.402 Art. 24); 14 municipais ainda não-verbatim.
- **Engines (determinísticos, auto-teste verde):** `engines/tdc/pcpt.py` (cedente, 2 vias Art.125 / 126-127),
  `engines/tdc/oodc.py` (receptor).
- **Tabelas (combustível):** `q14-valor-terreno.csv` (6.715 V por SQL) · `quadro3-ca-por-zona.csv` (39 zonas) ·
  `quadro5-fator-social-fs.csv` · `quadro7-parques.csv` (272 parques, 147 propostos) · `fi-incentivo-doacao.csv`.
- **Ferramenta comercial (Produto A):** `zepec/ferramenta/zepec_cedentes.csv` — **6.131 imóveis**, 1 linha cada
  (6 estados de venda · certeza · negociável só-com-prova · dono parcial · m² transferido · FUNDURB); listas
  derivadas `lista_prospeccao.csv` (2.740 prontos) + `fila_verificar.csv` (3.350).

---

## 3. A DEFINIÇÃO DE "PRONTO" — a ferramenta comercial em 3 eixos mensuráveis

O norte é *"ferramenta comercial **completa · auditável · com dados ricos**"*. Traduzido em prova mecânica:

| Eixo | O que significa | Como se PROVA (DoD) | Hoje |
|---|---|---|---|
| **COMPLETA** | cobre o funil ponta a ponta e as vias de negócio ativas | 1 fluxo `dado → engine → lista acionável` rodando por imóvel real; vias 1 + expansão mapeadas | 🟡 via 1 pronta; B (receptor) preso; vias 2-6 sem geo |
| **AUDITÁVEL** | toda linha rastreável ao dispositivo + número do engine | cada número com citação (1.7) e nascido no engine (1.3); mérito jurídico revisado (B-10); vigência-por-chunk (B-11c) | 🟡 1.3/1.7 OK; B-10 e B-11c abertos |
| **DADOS RICOS** | dono em escala + Atc + preço + liquidez | dono ≥ maioria dos 599 prontos; Atc do IPTU liga preço; FUNDURB com semântica confirmada | 🔴 dono 79; Atc/preço parados; FUNDURB INDETERMINADO |

**Conclusão da lente:** *completa* está a poucos passos LOCAIS; *auditável* é quase toda LOCAL; *rica* é onde
mora a dependência EXTERNA (dado pesado + fonte SMUL). É exatamente esse recorte que a estratégia ataca.

---

## 4. ANÁLISE DE GARGALOS PELA LENTE DE LOOP DE IA

O achado central: **cada item aberto pertence a uma de duas classes**, e tratá-las igual é o que trava o loop.

### 4.1 — Classe LOCAL (o loop de IA destrava sozinho — sem esperar ninguém)
Trabalho de criar arquivo/rodar engine/auditar, 100% dentro da cerca. **Deve rodar JÁ, em paralelo.**
- **B-5** camada semântica + filtro por `tema` (mata a armadilha lexical) · **B-6** grafo de remissões/vigência.
- **B-11(c)** vigência POR CHUNK (280 rótulos de redação compilada) · **B-7** vigência municipal datada (1.6).
- **B-12** guarda de DECIMAL(10,3) total no engine (resíduo — FATAL e citação-por-dispositivo já pagos).
- **B-3** completar tabelas Fs/Fp no `oodc.py` (faixas HIS/HMP/R) — os quadros já estão em `tabelas/`.
- **B-10** auditar o MÉRITO JURÍDICO das 32 juris + leis-chave (ponto cego declarado — só proveniência foi vista).
- **Via 5 (parques):** cruzar `quadro7-parques.csv` (147 propostos) × substrato já extraído.
- **Consolidar a semântica dos 6 estados de venda + `verificar`** em uma camada de prospecção mais rica (local).

### 4.2 — Classe EXTERNA (exige UM passo do MOU/infra — o loop NÃO resolve sozinho)
- **Dado pesado (Drive→Supabase):** `IPTU_2026.csv` (937 MB), `socios.csv`, série ITBI → **dono em escala + Atc**
  (destrava eixo "rico" e o engine de preço). Passos em `PLANO-H3-PRODUTO.md` + `scripts/transferir-pesados-*.md`.
- **Cru verbatim das 14 municipais** (B-4) e **tabelas Q14/Quadro 3 na fonte** — Drive é lane exclusiva (B-9).
- **Perímetros geo** (ZEPAM/ZEIS/corredores) → destrava vias 2/3/4/6 (`zepec/VIAS-EXPANSAO.md`).
- **Semântica FUNDURB** (teto 5% vs arrecadação; janela rolante vs all-time) → confirmar na fonte **SMUL**
  → destrava o sensor de liquidez (hoje honestamente `INDETERMINADO`, `CODEX-PRECIFICACAO-TDC.md §5`).
- **Produto B ao `main`** (B-17): PR a `main` protegido + conflito leis 16.050/17.844 → **decisão do MOU**.
- **Despausar o preço** (`CODEX-PRECIFICACAO-TDC.md`): decisão de negócio do MOU (hoje PARADO de propósito).

**Regra de ouro do loop:** a Classe LOCAL **nunca espera** a Classe EXTERNA. E toda a Classe EXTERNA vira **um
pedido único e datado** ao MOU (§7) — em vez de N adiamentos que caem no vão entre instâncias.

---

## 5. AS LENTES A ACIONAR (Gens) — e o que cada uma destrava

Mapa dos Gens (`CLAUDE.md` Parte 4) traduzido em **lentes acionáveis** por esta estratégia. Cada lente é um
subagente com fronteira e handoff próprios. "Acionar" = despachar um agente com escopo fechado + DoD.

| Lente (Gen) | Papel no loop | O que destrava aqui | Itens que fecha |
|---|---|---|---|
| **Gen Técnico-RAG** | ingestão · chunking · indexação | semântica + remissões + vigência-por-chunk | B-5, B-6, B-11c, B-7 |
| **Gen Matemática** | engines · validação de cálculo · **única fonte de número** (1.3) | guarda decimal · Fs/Fp completos · via 5 (parques) | B-3, B-12(resíduo), Via 5 |
| **Gen Advogado** | tese/antítese/vacina · mérito jurídico | auditar mérito das 32 juris (ponto cego) | B-10 |
| **Gen Estudo** | síntese temática · lacunas | enriquecer a ferramenta comercial (segmentos/estados) | camada de prospecção rica |
| **Gen RAG** | consulta com citação (1.7) · **nunca responde sem citar** | prova de auditabilidade ponta a ponta | gate de aceite de cada onda |
| **Lente adversarial (triplo-limpo)** | auditoria com **lente DIFERENTE** (D-12) | pega bug silencioso ANTES do gate | verifica cada entrega |
| **Orquestrador (esta instância)** | roteia · aplica o gate humano/mecânico · monta o pedido ao MOU | esta estratégia + o pedido único | §6, §7 |

> **Invariante de segurança (Parte 4):** *Gen Matemática é a única fonte de número; Gen Advogado nunca inventa
> valor; Gen RAG nunca responde sem citação.* Toda lente acionada herda estas travas.

---

## 6. A ESTRATÉGIA DE ENTREGAS — ondas sequenciadas (cada onda tem dono, gate e é durável)

Princípio: **ondas de VALOR LOCAL primeiro** (não dependem de ninguém), com a lente adversarial validando cada
uma antes do gate, enquanto o **pedido único ao MOU** (§7) corre em paralelo destravando a Classe EXTERNA.

### ONDA 1 — Auditabilidade (torna a ferramenta *defensável*) · lentes: Gen Técnico-RAG + Gen Advogado
- **B-11c** vigência-por-chunk: `consultar.py` deixa de devolver redação revogada como vigente (eval de redação
  compilada = gate). **B-7** vigência municipal datada (1.6). **B-10** mérito jurídico das 32 juris (registro
  dialético + vacinas). **B-5/B-6** semântica + remissões (mata a armadilha lexical).
- **DoD:** novos evals (armadilha lexical · redação-compilada · data-por-remissão) verdes no gate; mérito
  jurídico com citação verificada tema-a-tema. **Por que primeiro:** "auditável" é o eixo mais barato e o que
  protege TODA venda — sem ele, cada número é contestável.

### ONDA 2 — Riqueza LOCAL do dado (o que dá para enriquecer sem o Drive) · lentes: Gen Matemática + Gen Estudo
- **B-3** Fs/Fp completos no `oodc.py` (faixas HIS/HMP/R com citação do quadro). **B-12** guarda decimal total.
- **Via 5 (parques):** cruzar `quadro7-parques.csv` (147 propostos) × cadastro → 2ª linha de negócio (doação).
- **Enriquecer a ferramenta comercial:** consolidar estados de venda + `verificar` numa camada de prospecção
  com mais fato por linha (sem inventar; só o que já está no git).
- **DoD:** engine com faixas completas auto-testado; nova lista de via 5; `zepec_cedentes.csv` mais rico com
  proveniência. **Por que segundo:** extrai todo o suco dos dados que JÁ temos antes de pedir os pesados.

### ONDA 3 — Riqueza EXTERNA (só destrava com o §7) · lentes: Gen Técnico-RAG + Gen Matemática
- Carregar IPTU/socios/ITBI no Supabase → **dono em escala** + **Atc** → liga o **engine de preço** (se o MOU
  despausar) → Produto A vira "rico". Perímetros geo → vias 2/3/4/6. FUNDURB confirmado → sensor de liquidez.
- **DoD:** dono cobrindo a maioria dos 599 prontos; `pcpt.py`/`art128.py` rodando sobre Atc real; sensor de
  liquidez saindo de `INDETERMINADO`. **Gatilho:** cada peça do §7 que o MOU entregar dispara sua sub-onda.

### ONDA 4 — Unificação e fechamento comercial · lentes: Orquestrador + lente adversarial
- Unir Produto A (cedente) + Produto B (receptor, se o MOU fizer o merge B-17) numa **visão única por imóvel**.
- Auditoria triplo-limpo final (lente DIFERENTE, D-12) + gate verde + handoff.
- **DoD:** ferramenta comercial única, auditável e rica; gate `fechar-instancia.py` verde; entrega registrada.

**Ordem honesta (régua D26 "armado ≠ destravado"):** Ondas 1-2 são LOCAIS e **começam já**; Onda 3 é gatilhada
pelo §7; Onda 4 fecha. Nenhuma onda local espera a externa.

---

## 7. O PEDIDO ÚNICO AO MOU (concentra toda a Classe EXTERNA — para nada cair no vão)

Em vez de N pendências espalhadas, **um pedido datado** ao escritório (canal `caixa-de-saida/para-escritorio/`,
cerca do Drive = lane B-9). Ordenado por quanto destrava:

1. **[MAIOR ALAVANCA] Dado pesado Drive→Supabase** (IPTU_2026, socios, ITBI): destrava **dono em escala + Atc**
   → eixo "rico" + engine de preço. Trilho pronto: `PLANO-H3-PRODUTO.md` + `scripts/transferir-pesados-*.md`.
2. **Cru verbatim das 14 municipais + Q14/Quadro 3 na fonte** (B-4/B-9): fecha o corpus jurídico.
3. **Perímetros geo** (ZEPAM/ZEIS/corredores): destrava as vias de expansão 2/3/4/6.
4. **Confirmar semântica FUNDURB na fonte SMUL** (B-20d): destrava o sensor de liquidez.
5. **Decisão: merge do Produto B (B-17) a `main`** + **decisão: despausar o preço** (2 decisões de negócio).

> Enquanto o MOU processa este pedido, **Ondas 1-2 já entregam valor** — o loop não fica ocioso esperando.

---

## 8. POR QUE ISTO É AUDITÁVEL (a estratégia se submete à própria doutrina)

- **Número:** todo valor nasce em engine determinístico (`pcpt.py`/`oodc.py`), nunca no LLM (1.3); Gen
  Matemática é a única fonte de número (Parte 4).
- **Citação:** toda afirmação jurídica cita dispositivo (1.7); Gen RAG recusa resposta sem citação.
- **Prova ≠ declaração:** cada onda só "fecha" pelo gate mecânico `fechar-instancia.py` (D83) — não por
  autodeclaração. A lente adversarial (D-12) audita com lente DIFERENTE antes do gate.
- **Nada se perde:** cada item vira linha no `BACKLOG.md` com DoD mecânica (o "ladrão" D83), surfaçada no boot.
- **Agnóstico (R2):** a ferramenta comercial reporta fato (estado de venda, negociável só-com-prova), sem
  "vale/melhor/pior"; onde a semântica é incerta, diz `INDETERMINADO` em vez de chutar.

---

## 9. PRÓXIMO PASSO CONCRETO (para esta instância ou a próxima)

O caminho de maior valor imediato, 100% LOCAL, sem esperar o MOU: **acionar a Onda 1 (Gen Técnico-RAG + Gen
Advogado)** — auditabilidade — porque protege toda a base comercial já existente e é o eixo mais barato.
As entradas para o BACKLOG (B-5, B-6, B-7, B-10, B-11c) já têm DoD; a próxima instância despacha as lentes.

> **Este documento é a bússola; o `BACKLOG.md` é o motor (o que falta, com prova); o gate é o juiz.**
