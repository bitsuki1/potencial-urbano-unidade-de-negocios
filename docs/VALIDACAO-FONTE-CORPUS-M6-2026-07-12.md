# M6 — Validação FONTE (Drive) × CORPUS (engine) · PU 19 · 2026-07-12

> **Missão do M6 (dono, 2026-07-11):** "monta a história inteira do produto... cruzar o que existe no Drive com o
> que as instâncias construíram — achar lacunas, contradições e confirmações." Este é o **relatório fonte×corpus**
> do primeiro passe: usa os documentos oficiais e a doutrina do Drive como camada de VALIDAÇÃO do engine.
> **Regra (OPORTUNIDADES-M6 §método):** documento NOSSO/de auditoria é **pista**, não fonte citável; vira verdade
> só depois de bater na **norma oficial**. Aqui o engine (gated contra 4 Declarações oficiais) é o árbitro empírico.

## O que o Drive tem (achado estrutural)
O dono subiu um corpus **estruturado** (não só bruto): documentos oficiais com cabeçalho medallion (`layer: SILVER`,
`source_origin`, `dominio_negocio`, `status_vigencia`, `confiabilidade`) + um **doc-mestre parametrizado**:
**"INSTRUÇÃO MESTRE DE AUDITORIA FORENSE: TDC — V.4.1 FINAL AUDITADA E PARAMETRIZADA"**
(Drive id `1Y0FmDX4XUcyNRrnjApS-gKL5q-miqCZVQMfI1Ox-WrY`, dono eduardo@saobentoservicos.com.br). É a **tabela de
coeficientes e travas** do TDC na visão do dono — o comparável ideal para validar o engine.

## ✅ CONFIRMAÇÕES — a V.4.1 (independente) valida o nosso engine
Cada linha abaixo: o doc-mestre do dono chega ao MESMO que o nosso código, por caminho independente.

| Item | V.4.1 (Drive) | Nosso engine | Bate? |
|---|---|---|---|
| Fórmula recepção Art. 128 | `PCr = (PCpt×VTcd)/(Cr×CAmaxcd)` | `art128.py` idem | ✅ |
| Contrapartida Cr | `Cr = (At/Ac)×V×Fp×Fs` | `oodc.py`/`art117` idem | ✅ |
| **Parque Fi (Art. 127)** | ≤ **R$ 2.352,06**→1,4 ; >→1,0 (Dec. 64.884/25) | **OP-1c** (limiar-parque-art127.csv) idem | ✅ **confirma o valor da OP-1c** |
| Quadro 14 2026 | +7,18% (Dec. 64.884/25, Portaria SMUL 8/2026) | **OP-1a** (reajuste_q14_2026) idem | ✅ **confirma a OP-1a** |
| Fi doação HIS / Viário | 1,9 / 2,0 | `fi-incentivo-doacao.csv` idem | ✅ |
| Base de preço = Quadro 14, **NÃO** valor venal (veda Art. 130) | sim | doutrina 1.3 do projeto idem | ✅ |
| Vedação recepção (ZER/ZCOR/ZPDS/ZEPAM/OUC, Art. 131) | rol taxativo | lado receptor (fora do escopo cedente) | ✅ (coerente) |
| Renovação estoque ZEPAM 70%/100% **NÃO** vale p/ ZEPEC-BIR | sim (Art. 124 §5º restrito a ZEPAM+TCA) | escopo do projeto idem | ✅ |
| Sem ITBI (cessão incorpórea) · sem caducidade quinquenal do DPC | sim | coerente | ✅ |

**Leitura:** um documento externo, feito por outra mão, **converge** com o engine nos pontos de preço/fórmula —
inclusive confirmando, por conta própria, o **R$ 2.352,06** que capturei do Decreto para a OP-1c hoje. Forte sinal
de que a espinha do motor está certa.

## ⚠️ UMA CONTRADIÇÃO CENTRAL — e a fonte oficial nos dá razão
**V.4.1 afirma:** para ZEPEC-BIR, `PCpt = Atc × CAbas × Fi` com **Fi = 1,0 FIXO** (fonte: PDE Art. 125), e chama a
**"tabela regressiva de Fator de Incentivo" de alucinação REJEITADA**.
**Nosso engine afirma:** `PCpt = Atc × CAbás × Fi × FSCE`, com **Fi ESCALONADO pela área do lote (LPUOS Art. 24 I–VII:
1,2 / 1,0 / 0,9 / 0,7 / 0,5 / 0,2 / 0,1)** + FSCE (Art. 57, Lei 17.844/2022, Setor Central).

**A fonte OFICIAL (Diário Oficial) falsifica o Fi=1,0 fixo.** Os 4 gabaritos reais que o engine reproduz ao centavo
(gate FSCE) EXIGEM que o Fi varie com a área:

| SQL (Atc) | PCpt oficial (DOC) | PCpt ÷ Atc | Decomposição que reproduz | Fi implícito |
|---|---|---|---|---|
| 299 m² | 717,60 | 2,40 | CAbás 1 × **Fi 1,2** × FSCE 2,0 | 1,2 (lote ≤500 → Art. 24 I) |
| 734 m² | 1.468,00 | 2,00 | CAbás 1 × **Fi 1,0** × FSCE 2,0 | 1,0 (lote >500 → Art. 24 II) |
| 490 m² | 1.176,00 | 2,40 | CAbás 1 × **Fi 1,2** × FSCE 2,0 | 1,2 |
| 320 m² | 768,00 | 2,40 | CAbás 1 × **Fi 1,2** × FSCE 2,0 | 1,2 |

Se o Fi fosse **fixo em 1,0**, o cedente de 299 m² daria `299×1×1,0×2,0 = 598,00` — **mas a Declaração oficial diz
717,60**. Só o **Fi escalonado (1,2 para ≤500 m²)** fecha. Ou seja: o Fi **precisa** variar; a "tabela regressiva"
que a V.4.1 chama de alucinação é, na verdade, **o Art. 24 da LPUOS aplicado — e o Diário Oficial confirma**.

**Recomendação (fechada):** MANTER o engine como está (Fi escalonado Art. 24 + FSCE) — é a versão **provada contra 4
atos oficiais**. A **V.4.1 do Drive precisa de correção** neste ponto (o `Fi=1,0 fixo` e o "tabela regressiva rejeitada").
Provável causa do erro na V.4.1: ela **não conhece o FSCE** (Art. 57 / AIU-SCE — descoberta desta unidade que resolveu
o "mistério Fi≈2,4"); sem o FSCE, quem olha o número ~2,4 e crava Fi=1,0 erra a decomposição. _(Nada mudou no código:
o engine já estava certo; este relatório só registra a divergência e de que lado está a prova.)_

## 🔎 GAPS e LEADS (want-list do próximo passe)
1. **Lei 18.298/2025 — AUSENTE do corpus.** A V.4.1 a lista no arcabouço vigente; nosso corpus vai só até 18.222/2024.
   É a lei municipal mais nova citada — **candidata nº1 a ingerir** (pode alterar PDE/LPUOS). _(Capturar do portal
   oficial/Drive → `_entrada` → promover/fatiar/indexar, como as demais.)_
2. **Citação do Fi: Art. 24 × Art. 25 da LPUOS.** A V.4.1 cita "LPUOS Art. 25" para o PCpt de ZEPEC-BIR; nosso engine
   escalona por "LPUOS Art. 24 I–VII". Conferir no verbatim da LPUOS 16.402/2016 qual artigo traz a escala de Fi por
   área (o engine já bate os gabaritos; é conferência de rótulo de dispositivo, 1.7).
3. **Corpus estruturado do Drive (medallion SILVER).** Há muitos oficiais já OCR/parametrizados no Drive (ex.: Portaria
   SMUL 8/2026 em `.md` SILVER). Vale um passe de reconciliação com o nosso `leis/` para achar o que falta ingerir.

## Método e honestidade (1.2/1.3/1.7)
Este passe **leu a fonte e cruzou** — não precificou nem argumentou nada novo. A única "decisão" é de **veracidade**:
onde o engine e o doc do dono divergem, o **ato oficial (Diário Oficial)** decide — e decidiu a favor do engine no Fi.
As confirmações não são auto-elogio: vêm de um documento de **outra autoria** convergindo com o nosso motor.

---
> Fontes: Drive (id `1Y0FmDX4XUcyNRrnjApS-gKL5q-miqCZVQMfI1Ox-WrY`, V.4.1; Portaria SMUL 8/2026 SILVER); gabaritos
> oficiais em `evals/ground-truth/gabaritos/` (gate FSCE `pcpt.py`); Decreto 64.884/2025 (OP-1a/OP-1c). PU 19.
