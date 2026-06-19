# Correções de Referência e Vacinas — RAG IPTU

> Registro dialético (CLAUDE.md do Escritório): cada correção carrega a VACINA — "já achamos X; X está
> errado porque Y; não reafirmar X". Origem: gap analysis interna+externa (2026-06-18). Estes erros estavam
> nos docs-mestre do projeto (Mestre IPTU, Estudo Profundo, Documento Base IA, prompts Gen2/OrgNormativa) e
> NÃO devem ser herdados pelo RAG. Onde o texto-fonte continua no Google Drive, ele precisa ser corrigido na
> origem também (o conector atual do Drive é só leitura/criação — a correção no Doc do Drive é manual).

## C-1 — Isenção por ENCHENTE
- **Errado (nos docs):** "Lei 14.493/2007".
- **Correto:** **Lei municipal SP 17.202/2019** (isenção de IPTU para imóvel atingido por enchente, limite ~R$20 mil),
  com procedimento atualizado pela **Lei 17.759/2022**.
- **VACINA:** não citar 14.493/2007 para enchente em SP; a base é a 17.202/2019 (+17.759/2022).

## C-2 — Imóveis TOMBADOS
- **Errado (nos docs):** "Lei 10.598/1988" como isenção genérica de IPTU por tombamento.
- **Correto:** não há isenção **genérica** de IPTU por tombamento no município de SP. O benefício real é a
  **Lei 12.350/1997 ("Lei das Fachadas")** — isenção de até 10 anos para restauro de imóvel no centro/tombado —
  e os incentivos do **Requalifica Centro (Lei 17.577/2021)**.
- **VACINA:** não afirmar "imóvel tombado é isento de IPTU". A tese 6 deve ser reescrita para as hipóteses
  específicas (fachadas/restauro/Requalifica), não isenção automática.

## C-3 — Encadeamento da PGV (Planta Genérica de Valores)
- **Errado (nos docs):** tratar a "Lei 15.889/2013" como **a** lei da PGV.
- **Correto (cadeia):** **Lei 10.235/1986** (lei-mãe das tabelas de valores unitários) → **Lei 15.889/2013**
  (revisão geral) → **Lei 18.330/2025** (revisão vigente a partir do exercício 2026).
- **VACINA:** a 15.889/13 é um elo, não a base. Sempre amarrar a redação vigente na DATA do fato gerador.

## C-4 — Tema 1.084 do STF (avaliação individualizada)
- **Errado/ambíguo (nos docs):** usar **ARE 1.216.078** como leading case do Tema 1.084.
- **Correto:** o Tema 1.084 é o **ARE 1.245.097** (avaliação individualizada de imóvel fora da PGV exige
  critérios EM LEI + contraditório). O **ARE 1.216.078** é o **Tema 1.062** (juros/limite SELIC) — caso diferente.
- **VACINA:** não trocar os dois AREs; manter ambos com o tema correto.

## C-5 — Lei 11.614/1994 (aposentados/pensionistas)
- **Status:** referência correta, mas **conferir se o corpus tem o TEXTO CONSOLIDADO** da 11.614/1994 (atualizada
  pela 15.889/2013), e não apenas a 17.719/2021 que a alterou. Teto de valor venal atualizado por IPCA (~R$1,5 mi),
  renda até 3 SM (total) / 3-5 SM (parcial).

## C-6 — NBR 14653
- **Status:** confirmar que a "14653-2" presente é a **Parte 2 (imóveis urbanos, método Ross-Heidecke)** em edição
  atual, e adquirir a **Parte 1 (procedimentos gerais)**. ABNT é paga — registrar como pendência, não baixar pirata.

---
_Status: todas as correções acima estão REGISTRADAS; a aplicação nos textos-fonte do Drive é pendência manual
(ver limitação de ferramenta). Os arquivos do RAG criados a partir daqui já nascem com a referência correta._
