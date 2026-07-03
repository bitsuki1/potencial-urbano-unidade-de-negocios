# Achados da auditoria profunda — Potencial Urbano → Escritório do MOU

> **Caixa-de-saída v2 (PROTOCOLO-DE-CAIXAS §1).** O sync do escritório recolhe.
> **Dono:** instância orquestradora do PU. **Data:** 2026-06-27. **Branch:** `claude/office-standards-consolidation-5gyg00`.
> **Assunto:** resultado de "verificar caixa + auditoria profunda + depositar achados" (acionamento do MOU 2026-06-27).
> **Laudo completo (zero-síntese):** `docs/AUDITORIA-PROFUNDA-2026-06-27.md` neste repo.

---

## 1. Pacote de padronização — RECEBIDO e EXECUTADO ✅
O pacote depositado em `claude/maestro-project-audit-h71gqn` (D128 · D119/D120 · REGISTRO/ATA · handoff · caixas v2) foi **auditado seguro (additive puro, 12 arquivos, nada de produto tocado)** e **consolidado na branch de trabalho do PU por fast-forward**. As 7 diretrizes `✅ APLICADO` foram **verificadas uma a uma — todas conferem**. A "contradição" suspeita em D-PU-DENY **não existe** (a `caixa-de-saida/` do PU mora na raiz, fora do glob `escritorio-do-mou/**` → escrevível; o sync recolhe). **Nada a corrigir no pacote.**

## 2. ⚠️ AÇÃO DO ESCRITÓRIO/MOU — produto preso fora do `main` (maior valor do portfólio)
A auditoria de branches achou **trabalho de PRODUTO já feito e órfão** na branch **`origin/claude/project-audit-roadmap-2thi1g`** (14 commits, ~742 arquivos), enquanto o **SSOT do `main` (BACKLOG.md, PU.md) declara "produto a ~0%, `tabelas/` vazio"** — contradição direta. Conteúdo preso:
- **B-1 FECHADO:** `tabelas/` com Q14 (6.715 valores V por SQL), Quadro 3 (39 zonas, CA_max), Q5 (Fs).
- **Engine OODC sobre dados REAIS:** imóvel real `SQ 001003/Codlog 038121 × ZEU = R$ 931.800`.
- **Corpus TDC verbatim:** 19 leis indexadas (vs main=13) — PDE 16.050, LPUOS 16.402, COE 16.642.
- **Estágio E5 (produto) PROVADO:** 6 imóveis reais, topo R$ 1,68M + schema Supabase DDL.

**Por que é do escritório:** consolidar exige **PR ao `main` (protegido)** + 1 decisão de conflito (leis 16.050/2014 e 17.844/2022: aceitar a versão verbatim da branch sobre o resumo WebSearch do main — melhoria pura). **Recomendação:** priorizar este merge — sozinho tira o produto de "0%" para "E5 provado" e fecha B-1. O orquestrador do PU executa o PR se/quando o MOU autorizar (cerca: main protegido).

**Outras branches** (detalhe no laudo §2): 5 de governança additive (consolidáveis), 4 já-no-main (delete-safe), 3 de história não-relacionada a investigar (`exciting-tesla`, `iptu-tdc-document-mapping`, `modest-mendel`).

## 3. Furos no TEMPLATE de processo do escritório (afetam os 7 projetos, não só o PU)
Os mecanismos novos (auto-estampa no `surface-backlog.sh`, caixas v2) têm 2 furos que **nasceram no template do escritório** — corrigir na fonte para não propagar a 7 repos:
- **H-2 (MÉDIO):** o auto-estampa faz `>> REGISTRO-DE-INSTANCIAS.md` em SessionStart sobre árvore limpa, e o REGISTRO **não** está no `.gitignore` → todo boot suja a árvore e cria pendência mecânica fantasma que **briga com o próprio gate "árvore limpa"**. Decidir no template: `.gitignore` o REGISTRO, ou o hook auto-commitar a linha.
- **H-1 (MÉDIO):** o dedup do auto-estampa só checa linha `ABERTA` → reabrir uma branch já `FECHADA` duplica a linha. Deduplicar por branch independente do estado.
- **F-1 (informativo):** `gate-fechamento.sh` e `fechar-instancia.py` **discordam** no mesmo estado (um VERDE, outro VERMELHO). O `gate-fechamento.sh` não regenera o MANIFESTO → dá falso-verde. Considerar alinhar os dois gates do template (ou o gate "leve" chamar o pesado).

## 4. Pendência do PU que cruza com o Drive (lane do escritório) — relembrar
Segue de pé o **B-9 / AUD-02**: o PU precisa do cru verbatim das 14 municipais e das tabelas (já FECHADO na branch órfã do §2, mas não no main) **e** o alerta AUD-02 (IDs canônicos do Drive trocados — risco de DELETE errado de ~3 GB) **antes** de qualquer `DRY_RUN=false`. Relayar à lane do Drive.

## 5. O que o PU já fez do seu lado (não precisa do escritório)
Depositado em `BACKLOG.md` (itens novos B-15..B-19, com DoD) para o próprio PU executar quando o MOU acionar: corrigir o rótulo `indexado` falso das 4 leis IPTU (N-1, CRÍTICO), regenerar o MANIFESTO (N-2), B-11(c) vigência-por-chunk, B-12(c/d) FATAL+citação-por-artigo. **Não** foram tocados nesta sessão por estarem fora do escopo "executar padrões + auditar + depositar" — aguardam acionamento cadenciado.
