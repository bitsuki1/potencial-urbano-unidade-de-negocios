# Pague-tudo + deliberação de frentes (MR-14) — Potencial Urbano → Escritório do MOU

> Caixa-de-saída v2. **Dono:** orquestrador do PU. **Data:** 2026-06-27. **Branch:** `claude/office-standards-consolidation-5gyg00`.
> **Assunto:** 2º acionamento do MOU ("verificar caixa, 3 auditorias, pague tudo, deposite") + resposta à pauta MR-14.
> **Laudo:** `docs/AUDITORIA-PROFUNDA-2026-06-27.md`. **Decisões:** CODEX §5 D-13..D-17.

---

## 1. Caixa lida e PAGA (lado-projeto, sem precisar do escritório)
3 auditorias rodadas (profunda·beta·decisões, lentes diferentes D-12). Achados locais **pagos com prova** (gate `fechar-instancia.py` VERDE, exit 0):
- **B-15 (CRÍTICO):** as 4 leis IPTU diziam `indexado` com 0 chunks (falso-verde no corpus). Indexadas DE VERDADE → **17 leis / 1.571 chunks**. **Bônus:** indexar a LPUOS 16.402 **destravou TDC no main** (consulta cita Art. 24, cobertura 86% — 1º TDC consultável no main).
- **NV-1:** `consolidar.py` passou a derivar `indexado` do índice (não do rótulo) + alerta `indexado_sem_chunks`.
- **B-16:** MANIFESTO honesto. **B-18:** os dois gates agora concordam na idempotência do SSOT (fim do falso-verde F-1). **B-19:** o hook não suja/duplica mais o REGISTRO a cada boot. **B-12(c/d):** trava FATAL de gabarito executada + citação por dispositivo.

## 2. ⚠️ Furo que nasce no TEMPLATE do escritório — PORTAR na fonte
Corrigi **localmente** no PU 3 furos que vieram do template (`surface-backlog.sh`/`gate-fechamento.sh`). **Porte ao template do escritório** para não repetir nos 7 projetos:
- **H-2:** auto-estampa do REGISTRO sujava a árvore a cada boot. Fix PU: dedup por branch em QUALQUER estado (só estampa na 1ª vez genuína).
- **H-1:** reabrir branch FECHADA duplicava linha. Mesmo fix.
- **NV-2 (novo, importante):** `gate-fechamento.sh [2/5]` e o boot **AUTO-EMPURRAM ao main** (D141). Rodar o gate MOVE o main. Adicionei guarda que ABORTA a auto-consolidação se o MANIFESTO não for idempotente. **Avaliar no template:** auto-push ao main sem gate de integridade é vetor de propagação de falso-verde.

## 3. ⚠️ B-17 — produto preso fora do main (decisão do MOU, segue de pé)
Continua o maior valor parado: a branch `project-audit-roadmap-2thi1g` (~742 arquivos) tem B-1 fechado (tabelas reais), engine sobre imóvel real, TDC verbatim (19×13) e E5 provado. Consolidar exige **PR ao main + resolver conflito leis 16.050/17.844 (aceitar a versão verbatim)**. É cross-repo (decisão sua). Hoje o PU destravou TDC parcialmente pela LPUOS, mas o produto PLENO está nessa branch.

## 4. RESPOSTA À PAUTA MR-14 (deliberação de frentes) — recomendação do orquestrador
Pauta aberta (modo deliberação). Minha leitura do doc-mãe, para você **consolidar COM**:

| Frente candidata | Recomendação | Porquê |
|---|---|---|
| **F-PU-A · Engine de Cálculo** (TDC OODC + IPTU progressivo) | ✅ **VIRA FRENTE** | Subsistema determinístico de NÚMERO (1.3). Já é código (`engines/tdc/oodc.py`, trava FATAL, citação por dispositivo); merece doc próprio (fórmulas+derivação+desenho do fluxo) e absorve B-3/B-12. |
| **F-PU-B · Produto: Lista de Alvos por Imóvel** | ✅ **VIRA FRENTE — É O VALOR** | O entregável de negócio (IPTU×LOTES×Q14×zoneamento→alvos). É o "porquê" do PU. Hoje preso em B-2/B-17. Doc: spec do produto + modelo de dados + desenho do pipeline. **Lidera a fila.** |
| **F-PU-C · Corpus Jurídico & RAG** | ✅ **VIRA FRENTE** | A espinha técnica (esteira provada fim-a-fim, `scripts/README.md`). Doc formaliza o que já roda. |
| **F-PU-D · Tese/Parecer Jurídico** | 🕐 **FUTURA** | Camada argumentativa (Gen Advogado) ainda não construída. Candidata depois que A/B/C andarem. |

**Ordem de valor (recomendada):** F-PU-B (produto) lidera, **combustível** de F-PU-A (engine) + F-PU-C (corpus). **Pré-condição de A e B no main = consolidar B-17.**
**DoD da MR-14 (sua):** consolidar as frentes do PU → coluna PU vira ✅. Aguardo sua palavra para refletir no `MAPA-DA-UNIDADE` (formato `profinders/MAPA-DA-UNIDADE.md`) e depositar a versão consolidada.
