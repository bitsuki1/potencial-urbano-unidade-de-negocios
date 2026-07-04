# MOTOR ZERO (M0) — FECHAMENTO: piso de credibilidade
> PU 17 · 2026-07-04. **Entregável final do M0** do `ROADMAP-PU.md`. Cada item com PROVA MECÂNICA (um gate decide, não prosa). Gate: `python3 scripts/fechar-instancia.py` = VERDE.

## O que o M0 entrega (definição do roadmap)
> "A ferramenta pode ser mostrada a um comprador sofisticado **sem detonar credibilidade na primeira auditoria**. Todo R$ exibido carrega dispositivo citado, banda/estimativa enquadrada e disclaimer. O erro material mais caro (citar a fórmula central com dispositivo errado) some."

O M0 **NÃO** torna os números "certos em escala" (isso é M1+M3, cobertura/geo). Ele torna o produto **auditável e honesto**: cada número sabe o que é, cita a lei, e declara onde é estimativa/pendência.

## Itens do M0 — estado e PROVA

| Item (roadmap M0) | Motor | Prova mecânica (gate) | Estado |
|---|---|---|---|
| Corrigir chunker C-28 (fórmula PCpt citada como Art. 124) | **T1** | `133__art-124` sumiu; fórmula sob **Art. 125**; eval `tdc-formula-pcpt` (dispositivo+conteúdo) verde; 15/15 evals | ✅ |
| Gate de CI cobre o produto (não só o corpus) | **T2** | `consolidar.yml` dispara em `engines/zepec/tabelas/supabase` (push+PR); `eval-produto.py` 7 cedentes reais; **sabotar 1 Fi FALHA** | ✅ |
| Gate de conservação (Art. 129) como elegibilidade binária | **T4** | coluna `elegibilidade_conservacao` 3-estados; **31 ELEGÍVEL / 111 PENDENTE / 7033 SEM_ATESTADO**; Termo/RES nunca ELEGÍVEL (fixture) | ✅ |
| Regime do já-declarado (não aplicar escalonado por default) | **T3** | `regime_pcpt`+`qualidade_estimativa`; **615 JÁ_DECLARADO** flagados `PENDENTE_FI_DECLARADO`; escalonado nunca vira "declarado" (fixture) | ✅ |
| Surfaçar a divergência de 27% (PCpt × certidões) | **—** | `eval-divergencia-pcpt.py`: **55 pares**, mediana transferido/PCpt **1,66**, 100% flagados; gate cai se deixar de surfaçar/flagar | ✅ |
| DISCLAIMER.md + bloco injetado na saída ao cliente | **—** | `DISCLAIMER.md` na raiz; bloco `DISCLAIMER-BLOCO-*` em `COMO-USAR.md`; `check_disclaimer` no gate | ✅ |
| Indexar Art. 128/117 verbatim; constante 4 (CAmaxcd) / fórmula C | **L1** | Art. 128 e 117 **indexados** (destrave do T1); constante 4 **DECLARADA PENDENTE** (abaixo) | ✅ |
| Arquivar oráculos + colapsar fontes-de-verdade em ≤3 papéis | **T6** | `ls engines/tdc/oraculos/` = vazio (git rm, recuperável por `git log`); 3 papéis declarados (abaixo) | ✅ |
| Gate de segurança antes da Fase B (spend cap/RLS/PII) | **T7** | Fase 0 — D-SEG-01 (spend cap ON, RLS deny-all, S3 revogadas); `docs/HANDOFF-2026-07-03-MOTORES-FASE0.md` §5 | ✅ (Fase 0) |

**Gate mecânico:** `scripts/fechar-instancia.py` roda 8 checks de conteúdo (evals · engine OODC · engine cedente T2 · produto T2 · conservação T4 · regime PCpt T3 · divergência M0 · disclaimer M0) + idempotência do MANIFESTO + frescor do BACKLOG. **VERDE.** Os mesmos gates rodam no CI (`consolidar.yml`, push + pull_request nos paths do produto).

## Declaração — constante 4 (CAmaxcd) e fórmula C (L1)
O Art. 128 do PDE (agora verbatim/indexado) traz **`PCr = (PCpt × VTcd) / (Cr × CAmaxcd)`** — `CAmaxcd` é o **coeficiente de aproveitamento máximo do terreno cedente (VARIÁVEL)**, não uma "constante 4". A "constante 4 / ÷4" que os oráculos canonizaram **NÃO tem amparo no verbatim** → é asserção não-verificada. **DECISÃO M0:** nenhum R$ é emitido ancorado no ÷4 (`PENDENTE` até confirmação da fórmula C do Art. 128 §1º verbatim). Moot no escopo vigente: **receptor está FORA de escopo (D-ESCOPO-01)** — o produto de cedente usa o proxy `PCpt × V` (não a fórmula receptora do Art. 128).

## Declaração — 3 papéis de fonte-de-verdade (C-R4)
Para conter a proliferação de "oráculos"/docs write-once, o estado do projeto vive em **3 papéis canônicos**:
1. **git** = o ESTADO real (código, corpus, dados versionados).
2. **`MANIFESTO.json`** = o STATUS do pipeline de cada item (gerado, não editado à mão).
3. **`BACKLOG.md`** = o TRABALHO em aberto (com DoD mecânica).
Os **oráculos** (`engines/tdc/oraculos/*` — "CONHECIMENTO_MESTRE_IA…INABALAVEL" etc.) que canonizaram o **Fi=1 errado** e a **constante-4 sem amparo** foram **arquivados** (git rm; recuperáveis por `git log -- engines/tdc/oraculos/`). "Nada se descarta" = nada se apaga do **histórico git**, não "tudo fica no working tree".

## O que o M0 explicitamente NÃO resolve (honestidade)
- **Cobertura** (só ~49% dos cedentes têm PCpt) — é M1/M3.
- **Geometria** (overlay por área, vedação AUE/APPa, Regra da Esquina) — M3, depende de Drive/2 verbatims do dono.
- **Preço de mercado** (banda 3-stack) — M1, e a régua de preço é fork (c) do dono.
- **Propagar `PRÉ-CONDIÇÃO`/conservação e regime à ferramenta ao cliente** — M1 (a ferramenta religada).

## Ponteiros
- Roadmap-mãe: `ROADMAP-PU.md` (M0–M5). Sequenciamento das ABERTAS: `BACKLOG.md`.
- Provas: `evals/eval-produto.py`, `evals/eval-divergencia-pcpt.py`, `zepec/montar_base.py --autoteste`, `zepec/enriquecer_oficial.py --autoteste`, `engines/tdc/pcpt.py --demo`.
- Gate: `scripts/fechar-instancia.py` · CI: `.github/workflows/consolidar.yml`.
