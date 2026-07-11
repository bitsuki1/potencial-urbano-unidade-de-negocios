# OP-2 — Revisão de tombamento: Mancha "Benedito Calixto (I)" × CONPRESP Res. 01/2025

> **Achado do garimpo M6 (2026-07-11), confirmado contra a fonte OFICIAL** (decisão do dono "tudo oficial").
> **Vacina dialética:** a pista NOSSO (Auditoria TDC V9.0) dizia "26 falso-positivos — quadra arquivada".
> A **resolução oficial CONTRADIZ o "blanco"**: o arquivamento foi **PARCIAL**. Confirmar na fonte evitou
> descartarmos cedentes que continuam **válidos**. Isto é exatamente "melhores condições": nem vender o
> inválido, nem jogar fora o válido.

## A norma oficial
**Resolução SMC/CONPRESP nº 1, de 27 de janeiro de 2025** (814ª Reunião Ordinária; processos SEI
6025.2023/0000155-1 e 6025.2024/0005678-1). Fonte:
<https://legislacao.prefeitura.sp.gov.br/leis/resolucao-secretaria-municipal-de-cultura-smc-conpresp-1-de-27-de-janeiro-de-2025>

- **Art. 1º — ARQUIVOU** a abertura de processo de tombamento (APT) de **PARTE** dos elementos das
  Manchas Heterogêneas **Benedito Calixto (I)** e Vila Cândida (J) do **Anexo II da Res. 11/CONPRESP/2023**,
  e dos bens individuais **ID 50 a ID 52** do Anexo I da Res. 11/2023.
- **MANTEVE** o processo de tombamento dos elementos **1I, 2I, 4I (com recomendação), 10I, 11I, 1J e 3J**;
  excluiu a área envoltória.

## Por que toca a nossa lista
Nossos **26 cedentes da quadra 013.036** (setor 013, quadra 036) estão todos rotulados
**"Vila Cerqueira César / Manchas Urbanas Heterogênea"** — ou seja, a Mancha **Benedito Calixto (I)**.
Como o arquivamento foi **parcial**:
- os elementos cuja **APT foi arquivada** → **falso-positivo** (APT arquivada NÃO gera TDC por tombamento);
- os elementos **1I, 2I, 4I, 10I, 11I** (mantidos) → **seguem válidos**.

**Não dá para dizer QUAIS dos 26 sem o mapa `elemento-ID → endereço/SQL`** (Anexo II da Res. 11/2023 +
a lista de arquivamento da Res. 01/2025). Por isso **não removemos nenhum** — **sinalizamos os 26 para
revisão**, com a citação oficial, no próprio entregável (`pendencia_calculo`).

## Os 26 SQLs sinalizados (revisão de tombamento)
```
0130360001 0130360011 0130360012 0130360013 0130360014 0130360015 0130360016 0130360017
0130360018 0130360019 0130360020 0130360021 0130360022 0130360023 0130360024 0130360025
0130360026 0130360027 0130360028 0130360029 0130360030 0130360031 0130360032 0130360033
0130360048 0130360049
```
Sinal aplicado em `zepec/enriquecer_oficial.py` (prefixo 013036) → aparece na coluna `pendencia_calculo`
de cada um dos 26 no `zepec_cedentes_oficial.csv` e nos dossiês. Texto: *"REVISAR TOMBAMENTO — CONPRESP
Res. 01/2025 … arquivou PARTE da Mancha Benedito Calixto (I); manteve 1I/2I/4I/10I/11I …"*.

## Want-list para FECHAR (quais dos 26 saem)
1. **Anexo II da Res. 11/CONPRESP/2023** (a lista dos elementos I/J com endereço) — id do elemento → endereço.
2. **A lista de arquivamento da Res. 01/2025** (quais elementos "I" foram arquivados vs mantidos).
3. Cruzar com o **codlog/SQL** dos nossos 26 → marcar cada um como **arquivado (remover)** ou **mantido (fica)**.
   Aí sim vira remoção — **com sua palavra** (o dono autorizou "conferir e sinalizar"; a remoção fica para
   depois do mapa).

> M6 · OP-2 · PU 18 · 2026-07-11. Registrado também em `docs/OPORTUNIDADES-M6-TDC-IPTU.md` e no want-list.
