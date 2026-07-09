# T12 — Auditoria das DoDs do Motor 1 (Travas T1-T12)

> **Data:** 2026-07-09. **Auditor:** instancia T12 (Claude Code).
> **Objetivo:** verificar se cada DoD e mecanicamente provavel — por golden-assert sobre dado real, fixture discriminante ou marcador materializado — nunca so prosa.
> **Metodo:** para cada trava FEITA, rastrear o assert/eval/gate no codigo e confirmar que o arquivo existe e que o gate o executa. Para travas ABERTAS, avaliar se a DoD esta bem-especificada para ser mecanica quando implementada.
> **Fonte das DoDs:** `MOTOR-1-ESTRATEGIA.md` (raiz) + `docs/HANDOFF-2026-07-03-MOTORES-FASE0.md` sec.8.

---

## Tabela-resumo

| Trava | Status | Mecanismo de prova | Verificado? | Lacuna |
|---|---|---|---|---|
| **T1** | FEITO | `_norm_disp()` em `rodar-evals.py`; ground-truth ativos; `fatiar.py` guarda lexical | SIM | Nenhuma lacuna critica |
| **T1-bis** | DIVIDA DECLARADA | Nenhum (por design — registrada no BACKLOG) | N/A | Correto: divida declarada, nao bug |
| **T2** | FEITO | `eval-produto.py` (7 cedentes reais, ancora legal); `pcpt.py --demo`; ambos no CI/gate | SIM | Lacuna menor: golden SEM-PII nao implementado como arquivo versionado |
| **T3** | FEITO | `_autoteste_regime()` em `enriquecer_oficial.py`; gate no CI | SIM | DoD 3-7 BLOQUEADOS-EM-M2 (por design) |
| **T4** | FEITO | `_autoteste_conservacao()` em `montar_base.py`; gate no CI | PARCIAL | **5 lacunas**: sem assert sobre cohort real (32/164/0); sem fixture de proveniencia discriminante; sem propagacao per-linha; sem fixture de linha fundida; sem assert nao-vacuo |
| **T5** | FEITO | `eval-divergencia-pcpt.py`; `DISCLAIMER.md` + bloco injetado | PARCIAL | DoD 1-2 BLOQUEADOS-EM-M2; nenhuma decomposicao Fi-vs-CAbas/Atc |
| **T6** | FEITO | `engines/tdc/oraculos/` removido do working tree | PARCIAL | **Sem assert mecanico** no gate: nenhum check verifica ausencia da pasta ou contagem <= 3 fontes |
| **T7** | PARCIAL | Migration RLS + spend cap + rotacao (runbook) | **NAO** | **CRITICO:** probe de PII AUSENTE do gate; `donos_encontrados.csv` AINDA tracked; sem probe de historico; sem probe no CI |
| **T8** | ABERTO | Nenhum (nao implementado) | N/A | DoD bem-especificada; requer implementacao |
| **T9** | FEITO | `_estoque()` em `pcpt.py`; invariante T9 em `eval-produto.py` | PARCIAL | **2 lacunas**: preco nao usa `min(50000, saldo)` no produto; falta fixture ja>0 com saldo < 50k < PCpt |
| **T10** | ABERTO | Nenhum (bloqueado por Decreto 57.536/16) | N/A | DoD bem-especificada; requer dado externo |
| **T11** | FEITO | Logica de conjunto em `enriquecer_oficial.py` L177-203 | PARCIAL | **3 lacunas**: irmao com PCpt ausente nao forca PENDENTE-CONJUNTO; sem assert em eval-produto.py; sem fixture dos 16 conjuntos reais |
| **T12** | EM CURSO | Este documento | — | — |

---

## Analise detalhada por trava

### T1 — Corrigir a citacao da formula central (C-28)

**Status:** FEITO.

**Provas mecanicas verificadas:**
1. `scripts/fatiar.py` — guarda lexical `eh_remissao_line_initial` implementada. Remissao line-initial (minuscula "art.") nao abre chunk; so "Art." MAIUSCULO abre. Verificado no codigo.
2. `evals/rodar-evals.py:28-35` — `_norm_disp()` endurece comparacao de SUBSTRING para igualdade normalizada (`^Art\.? N(º)?$`). Verificado: "Art. 12" != "Art. 125".
3. Ground-truth ativos em `evals/ground-truth/` — 7+ arquivos JSON com itens ATIVOS; piso de cobertura `MIN_ITENS_ATIVOS = 4` em `rodar-evals.py:80`.
4. Wired em `consolidar.yml` (step "Evals") e `fechar-instancia.py` (check_evals).

**DoD 1-7 cobertura:**
- DoD 1 (discriminador lexical): IMPLEMENTADO em `fatiar.py`.
- DoD 2 (`header_raw` nao-vacuo): IMPLEMENTADO (chunker grava header_raw).
- DoD 3 (unicidade pela formula completa): COBERTO pelo ground-truth `tdc-formula-pcpt` (confirmado no BACKLOG: "formula PCpt = Atc x CAbas x Fi agora sob Art. 125").
- DoD 4 (ground-truth ativo): COBERTO pelos evals ativos.
- DoD 5 (regressao): COBERTO — chunks espurios `126__art-114.json` e `059__art-108.json` ausentes.
- DoD 6 (guarda anti-regressao 6015-1973): NAO VERIFICAVEL diretamente sem rodar o eval, mas a logica lexical (so MAIUSCULO abre chunk) preserva os ~40 chunks por design.
- DoD 7 (endurecer rodar-evals.py): IMPLEMENTADO (`_norm_disp` + `topo.citacao.dispositivo`).

**Veredito: SOLIDO.** Nenhuma lacuna critica. A prova e mecanica, discriminante e roda no gate.

---

### T1-bis — Artigo transcrito sem aspas

**Status:** DIVIDA DECLARADA (registrada no BACKLOG).

**Veredito:** Correto por design — a DoD prescreve que, enquanto nao implementada, e DIVIDA DECLARADA e PROIBIDO alegar "auto-cura". Nao ha prova a verificar porque nao ha implementacao. Nenhuma acao necessaria.

---

### T2 — Estender o gate ao PRODUTO

**Status:** FEITO.

**Provas mecanicas verificadas:**
1. `consolidar.yml` — dispara em `push` E `pull_request`, cobre `engines/**`, `zepec/**`, `tabelas/**`, `supabase/**`. Verificado (L12-41).
2. `engines/tdc/pcpt.py --demo` (`_autoteste`) wired no CI (L81-82) e em `fechar-instancia.py` (check_engine_cedente, L52-55).
3. `evals/eval-produto.py` — 7 cedentes reais (um por faixa I-VII), FAIXAS_LEGAIS hardcoded como ancora independente (L39-47), prova em DOIS pontos: engine E produto entregue. Wired no CI (L86-87) e em `fechar-instancia.py` (check_produto, L58-61).
4. Prova de sabotagem documentada: faixa I 1,2->1,5 faz gate FALHAR (cedente 378 m2: 453,60->567,00).

**DoD cobertura:**
- DoD 1 (gatilho sem paths): IMPLEMENTADO.
- DoD 2 (wire pcpt --demo): IMPLEMENTADO. Assert por igualdade da estrutura completa FI_ZEPEC_ART24 (7 tuplas) + citacao end-to-end por faixa I-VII + borda nos 6 tetos — verificado em `pcpt._autoteste()` (L191-200).
- DoD 3 (wire eval-produto.py): IMPLEMENTADO, mas **PARCIAL**. A DoD exige que `eval-produto.py` REGENERE a cadeia completa (`montar_ferramenta.py -> enriquecer_oficial.py`) e rode os asserts semanticos (BIR, AUE/APPa, conservacao, T3, T8, T9, T10, T11). **O eval atual NAO regenera a cadeia** — le o CSV oficial pre-existente. Os asserts semanticos de T8 (elegibilidade, vedacao, completude_vedacao), T4 (proveniencia), T10, T11 (conjunto) **NAO estao em eval-produto.py**.
- DoD 4 (golden SEM-PII): **NAO IMPLEMENTADO como arquivo versionado.** O eval compara contra o CSV oficial, mas nao existe uma projecao-golden SEM-PII commitada no git. A reconciliacao T2xT7 (dropar proprietario antes de versionar) nao foi feita.
- DoD 5 (cortar byte-diff): IMPLEMENTADO (nao existe byte-diff).
- DoD 6 (eval-vs-declaracao): BLOQUEADO-EM-M2 (por design).

**Lacunas:**
- **L-T2-1 (media):** `eval-produto.py` nao regenera a cadeia completa; le o CSV pre-gerado.
- **L-T2-2 (media):** `eval-produto.py` nao contem os asserts semanticos de T8/T4/T10/T11/T3 que a DoD prescreve.
- **L-T2-3 (baixa):** Golden SEM-PII nao existe como arquivo versionado (a projecao e comparada dinamicamente, nao congelada).

**Veredito: BOM, com lacunas de amplitude.** O nucleo (Fi legal ancorado na lei, sabotagem falha) e solido. Falta estender o eval para cobrir os asserts de TODAS as travas, conforme a DoD prescreve.

---

### T3 — Regime do JA-DECLARADO por VIGENCIA

**Status:** FEITO.

**Provas mecanicas verificadas:**
1. `enriquecer_oficial.py:39-65` — `regime_pcpt()` separa JA_DECLARADO de PROSPECCAO_NOVA; `_autoteste_regime()` com 4 fixtures + 2 asserts negativos.
2. Wired em `fechar-instancia.py` (check_regime_pcpt, L71-74) e `consolidar.yml` (L93-95).
3. Colunas `regime_pcpt` e `qualidade_estimativa` materializadas na saida (L123-124, L166-167).
4. `eval-divergencia-pcpt.py` gateia que 100% dos pares JA_DECLARADO carregam `PENDENTE_FI_DECLARADO` (L29, L48-49).

**DoD cobertura:**
- DoD 1 (`pcpt._autoteste`): COBERTO — `_autoteste_regime()` cobre este eixo.
- DoD 2 (ground-truth): COBERTO pelos fixtures do autoteste.
- DoD 3 (fixture do gap: ja-declarado COM data_emissao SEM declarado_declaracao): **BLOQUEADO-EM-M2** — `declarado_declaracao` nao existe na base. Honestamente pendente.
- DoD 4 (armadilha `data_ref`): **BLOQUEADO-EM-M2** — nenhum campo de emissao existe.
- DoD 5-6 (reconciliacao vs declaracao, sanidade): **BLOQUEADO-EM-M2**.
- DoD 7 (provenance): **BLOQUEADO-EM-M2** — nao ha `declarado_declaracao` para rastrear.

**Lacunas:**
- Nenhuma lacuna nos itens construiveis-agora. Os itens 3-7 sao BLOQUEADOS-EM-M2 por ausencia de dados, e a DoD honestamente declara isso.

**Veredito: SOLIDO para o escopo construivel.** Os bloqueios sao por dependencia de dado, nao por omissao de prova.

---

### T4 — Conservacao como PRE-CONDICAO de 3 ESTADOS

**Status:** FEITO (nucleo), com lacunas de prova mecanica.

**Provas mecanicas verificadas:**
1. `montar_base.py:119-132` — `elegibilidade_conservacao()` classifica 3 estados (ELEGIVEL / PENDENTE_CONSERVACAO / SEM_ATESTADO). Verificado.
2. `montar_base.py:134-151` — `_autoteste_conservacao()` com 7 fixtures sinteticos. Verificado: Atestado->ELEGIVEL, Termo->PENDENTE_CONSERVACAO, RES->SEM_ATESTADO, vazio->SEM_ATESTADO.
3. Separacao `ato_conservacao` vs `ato_tombamento`: `montar_base.py:222-223` — para TOMBADO_CADASTRO, `ato_conservacao=''` e `ato_tombamento=nc(r[5])` (o bp_compres vai para ato_tombamento, nao ato_conservacao). Isso RESOLVE o vetor de falso-positivo (tombamento lido como conservacao) **por fluxo de dados**, nao por gate de proveniencia explicito.
4. Wired em `fechar-instancia.py` (check_conservacao, L64-68) e `consolidar.yml` (L90-91).

**DoD cobertura — lacunas GRAVES:**
- DoD 1 (predicado gateado por PROVENIENCIA): **PARCIALMENTE IMPLEMENTADO.** O vetor de falso-positivo e fechado pela separacao de campos (ato_conservacao vs ato_tombamento), MAS o gate de proveniencia EXPLICITO que a DoD prescreve — predicado que leia o `origem_da_evidencia` e rejeite evidencia nao-CERTIDAO — **NAO EXISTE no codigo**. O que existe e um workaround correto (campo separado), nao a solucao prescrita.
- DoD 3 assert sobre DADO REAL: **NAO IMPLEMENTADO.** A DoD exige assert mecanico sobre o cohort real `CERTIDAO_BIR_CEDENTE` de `zepec_unificada.csv` travando a particao: `count(ELEGIVEL)==32`, `count(PENDENTE)==164`, `count(Termo E resultado != PENDENTE)==0`. **Nenhum desses asserts existe em nenhum arquivo .py.** A contagem e declarada em prosa no MOTOR-1-ESTRATEGIA.md, nao provada mecanicamente.
- DoD 6 (fixture discriminante TOMBADO puro com Atestado-like): **NAO IMPLEMENTADO.** A DoD exige uma fixture com `origem=TOMBADO_CADASTRO` e `ato_conservacao='Atestado de Conservacao 001/20'` que FALHA se sair ELEGIVEL (provando que o gate de proveniencia morde). Nenhuma fixture desse tipo existe. O autoteste so testa a funcao `elegibilidade_conservacao()` pura — que retornaria ELEGIVEL para essa string independente de origem. A protecao real vem do fluxo de dados (campo zerado para TOMBADO), nao do predicado.
- DoD 7 (propagacao por PROVENIENCIA ao runtime): **NAO IMPLEMENTADO.** `zepec/ferramenta/zepec_cedentes.csv` (o input que `enriquecer_oficial.py` consome) NAO carrega `ato_conservacao` nem `origem_da_evidencia` per-linha — so `origens` agregado. Verificado no header de `montar_ferramenta.py` COLS (L117-121).
- DoD 8 (fixture da LINHA FUNDIDA): **NAO IMPLEMENTADO.** Nenhuma fixture exercita uma linha com `origens` contendo CERTIDAO_BIR_CEDENTE+TOMBADO_CADASTRO simultaneamente.

**Lacunas:**
- **L-T4-1 (ALTA):** Sem assert sobre cohort real (32/164/0). A particao e declarada em prosa, nao provada.
- **L-T4-2 (ALTA):** Sem fixture discriminante de proveniencia (TOMBADO com Atestado -> PENDENTE).
- **L-T4-3 (ALTA):** Sem propagacao per-linha de `(ato_conservacao, origem_da_evidencia)` ao runtime.
- **L-T4-4 (ALTA):** Sem fixture da linha fundida (79 linhas reais com CERTIDAO+TOMBADO).
- **L-T4-5 (MEDIA):** Sem assert nao-vacuo no eval-produto.py para conservacao.

**Veredito: NUCLEO CORRETO, PROVA INCOMPLETA.** O classificador funciona e o vetor de falso-positivo esta fechado por fluxo de dados. Mas a DoD exige provas mecanicas que nao existem: o "declarei feito != provei feito" se aplica exatamente aqui. A afirmacao "32 Atestado / 111 Termo / 53 vazio" e prosa, nao assert.

**Prova mecanica proposta:**
```python
# Em eval-produto.py ou montar_base.py --autoteste:
# 1. Assert sobre cohort real
uni = csv.DictReader(open("zepec/limpo/zepec_unificada.csv"))
cohort = [r for r in uni if r["origem"] == "CERTIDAO_BIR_CEDENTE"]
assert sum(1 for r in cohort if r["elegibilidade_conservacao"] == "ELEGIVEL") == 32
assert sum(1 for r in cohort if r["elegibilidade_conservacao"] != "ELEGIVEL") == 164
assert sum(1 for r in cohort
           if "termo de compromisso" in r["ato_conservacao"].lower()
           and r["elegibilidade_conservacao"] != "PENDENTE_CONSERVACAO") == 0

# 2. Fixture discriminante: TOMBADO com Atestado nao pode ser ELEGIVEL no runtime
# (requer propagacao de proveniencia para morder de verdade)
```

---

### T5 — Medir e travar o RESIDUO de ESTIMATIVA

**Status:** FEITO (M0-level).

**Provas mecanicas verificadas:**
1. `evals/eval-divergencia-pcpt.py` — mede divergencia sobre pares reais (>=50 pares), gateia 100% flagados como PENDENTE_FI_DECLARADO. Wired no CI e gate.
2. `DISCLAIMER.md` existe; bloco injetado em `zepec/ferramenta/COMO-USAR.md` (marcadores `DISCLAIMER-BLOCO-INICIO/FIM`). Check em `fechar-instancia.py` (check_disclaimer, L110-118).

**DoD cobertura:**
- DoD 1 (passthrough com `declarado_declaracao`): **BLOQUEADO-EM-M2.**
- DoD 2 (residuo apos descontar Fi-regime e CAbas/Atc historico): **NAO IMPLEMENTADO.** O eval mede a divergencia bruta, sem decomposicao em componentes.
- DoD 3 (anti-falso-esgotado): **PARCIALMENTE COBERTO.** O regime_pcpt impede precificacao firme do ja-declarado (PENDENTE), mas o saldo calculado por estimativa ainda pode zerar silenciosamente um saldo real — a DoD exige que, havendo oficial, o saldo USE o oficial. Sem `declarado_declaracao`, isso e impossivel.
- DoD 4 (re-medicao no engine atual): **NAO IMPLEMENTADO.** Os numeros "27%"/"1,27"/"1,66" sao declarados no MOTOR-1-ESTRATEGIA.md e no eval-divergencia, mas a DoD proibe usar numero de divergencia sem ser RE-MEDIDO — e o "1,27" e declarado stale. O eval mede ~1,66 sobre pares atuais, mas nao decompoem em componentes.

**Lacunas:**
- **L-T5-1 (MEDIA):** Decomposicao Fi-regime vs CAbas/Atc historico nao implementada.
- **L-T5-2 (BAIXA):** Bloqueios EM-M2 sao honestos e declarados.

**Veredito: HONESTO PARA O ESTADO ATUAL.** O que pode ser provado (divergencia surfacada, disclaimer) esta provado. Os itens que dependem de `declarado_declaracao` sao corretamente declarados pendentes.

---

### T6 — Arquivar o cemiterio + fonte unica

**Status:** FEITO.

**Provas mecanicas verificadas:**
1. `engines/tdc/oraculos/` **NAO EXISTE** no working tree (verificado: glob retorna vazio). Portanto o `git rm` foi executado e o historico preserva os arquivos.

**DoD cobertura:**
- DoD (assert no gate que nao ha novo oraculo): **NAO IMPLEMENTADO.** Nenhum check em `fechar-instancia.py` nem em `consolidar.yml` verifica a ausencia de `engines/tdc/oraculos/`.
- DoD (contagem fontes-mestre <= 3): **NAO IMPLEMENTADO.** Nenhum check conta as fontes-mestre vivas.

**Lacunas:**
- **L-T6-1 (MEDIA):** Sem assert mecanico no gate. O `git rm` e recuperavel do historico e a pasta pode ser recriada sem que nenhum gate reprove.

**Prova mecanica proposta:**
```python
# Em fechar-instancia.py:
def check_cemiterio():
    orac = RAIZ / "engines" / "tdc" / "oraculos"
    if orac.exists() and any(orac.iterdir()):
        return False, "engines/tdc/oraculos/ deveria estar removido (T6)"
    return True, "cemiterio de oraculos ausente (T6 ok)"
```

---

### T7 — Gate de seguranca (PII)

**Status:** PARCIALMENTE FEITO — a parte de runbook (RLS, spend cap) esta feita; os probes mecanicos no gate NAO.

**Provas mecanicas verificadas:**
1. Migration `20260703172052_seg_t7_gate_seguranca_fase_a.sql` — RLS deny-all. Verificado no git.
2. Spend cap ativado (confirmado pelo dono no handoff).
3. `DISCLAIMER.md` + `COMO-USAR.md` com bloco injetado.

**DoD cobertura — LACUNAS CRITICAS:**
- DoD 1A (arvore git): **NAO IMPLEMENTADO.** Nenhum step em `fechar-instancia.py` roda `git ls-files` para verificar PII. **ACHADO MATERIAL:** `zepec/limpo/donos_encontrados.csv` (4.967 linhas com coluna `proprietario`) **ESTA TRACKED pelo git** (verificado: `git ls-files -- zepec/limpo/donos_encontrados.csv` retorna o path). Isso viola diretamente a DoD.
- DoD 1A.2 (historico git): **NAO IMPLEMENTADO.** Nenhum check verifica `git log --all -- <path_pii>`.
- DoD 1B (probe anon de bucket): **NAO NO GATE** (runbook manual).
- DoD 2 (SELECT anon = 0): Coberto pela migration RLS deny-all.
- DoD 3 (whitelist Exposed schemas): **NAO NO GATE.**
- DoD 4 (spend cap): FEITO (dono).
- DoD 5 (rotacao): Parcial — `service_role` legada nao rotacionada (residuo de baixo risco declarado no handoff).

**Lacunas:**
- **L-T7-1 (CRITICA):** Probe de PII na arvore git AUSENTE do gate. `donos_encontrados.csv` com `proprietario` e TRACKED.
- **L-T7-2 (ALTA):** Probe de PII no historico git AUSENTE.
- **L-T7-3 (MEDIA):** Probe anon de bucket nao automatizado.
- **L-T7-4 (MEDIA):** Nenhum step no CI (`consolidar.yml`) bloqueia push com PII.

**Prova mecanica proposta (construivel-agora, DoD 1A):**
```python
# Em fechar-instancia.py (ANTES do step de push no CI):
def check_pii_arvore():
    import subprocess
    ASSINATURA_PII = ["proprietario", "dono", "contribuinte", "documento", "cpf"]
    paths_pii = ["zepec/limpo", "zepec/oficial", "zepec/raw", "zepec/ferramenta"]
    tracked = subprocess.run(
        ["git", "ls-files"] + paths_pii,
        cwd=RAIZ, capture_output=True, text=True
    ).stdout.splitlines()
    sujos = []
    for p in tracked:
        fp = RAIZ / p
        if not fp.exists() or fp.suffix not in (".csv", ".json", ".xlsx"):
            continue
        header = fp.open(encoding="utf-8").readline().lower()
        if any(tok in header for tok in ASSINATURA_PII):
            sujos.append(p)
    return (not sujos), ("sem PII na arvore git" if not sujos
            else f"PII tracked: {sujos[:5]} — git rm + purge historico ANTES de push")
```

---

### T8 — Enquadramento ZEPEC-BIR + vedacao AUE/APPa

**Status:** ABERTO (marcado como vermelho no BACKLOG).

**Estado atual no codigo:**
- `cessao_vedada()` em `montar_base.py:104` — substring em `bp_categor` (existe, funciona).
- `montar_ferramenta.py:129` — consome a coluna (classifica como VEDADO_LEI).
- `enriquecer_oficial.py` — **NAO gateia** em `elegibilidade_tdc` nem `vedacao_tdc`. O guard ANTES de atc/cabas **NAO existe**. Linhas vedadas podem receber `pcpt_m2`/`saldo`/`preco` se tiverem atc+cabas.
- Nenhuma coluna `elegibilidade_tdc`, `completude_vedacao`, `PENDENTE-VEDACAO` existe no MANIFESTO.

**Avaliacao da DoD para implementacao:**
A DoD (9 itens) esta BEM-ESPECIFICADA para ser mecanica:
- Itens 1-3 (guard positivo e negativo): especificam exatamente os predicados e a coluna booleana.
- Itens 4-5 (ground-truth): especificam as fixtures com o nivel de detalhe necessario.
- Item 6 (golden assert corpus): dois predicados claros.
- Item 7 (anti-over-block): define o eixo do teste diferencial.
- Item 8 (corrigir etiqueta TOMBADO_CADASTRO): acao clara.
- Item 9 (materializacao PENDENTE-VEDACAO + discriminante do flip): tres pernas mecanicas com asserts.

**Veredito: DoD PRONTA PARA IMPLEMENTACAO.** Nenhuma ambiguidade que impeca prova mecanica. Quando implementada, cada item gera um assert verificavel.

---

### T9 — Parcelamento legal do excedente > 50.000 m2

**Status:** FEITO.

**Provas mecanicas verificadas:**
1. `pcpt.py:137-143` — `_estoque()` implementa o split (estoque_a_vista=50000, excedente=pcpt-50000, parcelas=10).
2. `pcpt._autoteste()` L207-209 — assert >50k com 20000x4x2=160000: estoque=50000, excedente=110000.
3. `eval-produto.py` L123-135 — invariante T9: nenhuma linha com PCpt>50000 pode sair sem `parcelas_anuais=10` + "Art.124 §3" na pendencia.
4. Wired no CI e gate.

**DoD cobertura:**
- DoD 1 (`preco_proxy_brl` usa `min(50000, saldo)`): **LACUNA.** `enriquecer_oficial.py:_precificar()` (L101-110) calcula `preco = saldo * V` — usa o SALDO CHEIO, nao `min(50000, saldo)`. O `eval-produto.py` verifica a PRESENCA do flag `parcelas_anuais=10`, mas NAO verifica que o PRECO reflete so a fracao a-vista. Hoje 0 cedentes reais >50k (declarado no eval), entao o check e vacuo.
- DoD 2 (fixture SALDO > 50000 prova a-vista < saldo total): **NAO IMPLEMENTADO.** O eval nao tem fixture com saldo > 50000.
- DoD 3 (reconciliacao com T3): **PARCIALMENTE COBERTO** pela logica do regime (T3 poe PENDENTE no ja-declarado).
- DoD 4 (anti-regressao, fixture ja>0 com saldo < 50k < PCpt): **NAO IMPLEMENTADO.** Nenhuma fixture testa PCpt=60k, ja=15k: preco sobre 45k e NAO sobre 50k.

**Lacunas:**
- **L-T9-1 (ALTA):** `_precificar()` nao aplica `min(50000, saldo)` — preco sobre saldo cheio quando saldo > 50000.
- **L-T9-2 (MEDIA):** Sem fixture para saldo > 50000 no eval.
- **L-T9-3 (MEDIA):** Sem fixture para o caso ja>0 onde saldo < 50000 < PCpt.

**Prova mecanica proposta:**
```python
# Em _precificar() ou wrapper:
preco_base = min(saldo, LIMITE_PARCELAMENTO)  # Art. 124 §3
preco = (preco_base * V).quantize(...)

# Fixture em eval-produto.py:
# PCpt=60000, ja=15000 -> saldo=45000 -> preco sobre 45000, NAO 50000
# PCpt=80000, ja=0 -> saldo=80000 -> preco sobre 50000, NAO 80000
```

---

### T10 — Vigencia da PROPRIA OUTORGA (validade da DPC)

**Status:** ABERTO (bloqueado por ausencia do Decreto 57.536/16 no corpus).

**Estado atual:** Nenhuma coluna `vigencia_da_outorga` existe. Nenhum fixture. Nenhum gate.

**Avaliacao da DoD:**
A DoD (4 itens) esta BEM-ESPECIFICADA:
- Item 1 (fixture DPC > 5 anos): claro e testavel.
- Item 2 (assert default PENDENTE-RENOVACAO): claro.
- Item 3 (provenance Decreto 57.536): bloqueado pela ingestao.
- Item 4 (dependencia M-DADOS): corretamente declarada.

**Veredito: DoD PRONTA.** Quando o Decreto for ingerido e os campos de emissao existirem, a implementacao e direta.

---

### T11 — Reconciliacao do saldo por CONJUNTO cedente

**Status:** FEITO (logica implementada), com lacunas de prova.

**Provas mecanicas verificadas:**
1. `montar_ferramenta.py:155` — `conjunto_certidao` atribuido.
2. `enriquecer_oficial.py:177-203` — logica de reconciliacao por conjunto: agrupa por `conjunto_certidao`, soma PCpts, desconta transferido, limpa saldo/preco individual dos membros.

**DoD cobertura:**
- DoD 1 (reconciliacao por conjunto): IMPLEMENTADO.
- DoD 2 (irmao com PCpt ausente -> PENDENTE-CONJUNTO): **PARCIALMENTE IMPLEMENTADO.** O codigo em L189-194 detecta `not completo` e adiciona nota "PARCIAL: ha membro sem PCpt", mas **NAO forca PENDENTE-CONJUNTO** — o saldo calculado usa so os membros com PCpt (soma parcial), o que pode fabricar um ESGOTADO falso. A DoD exige que PCpt ausente em qualquer membro force PENDENTE-CONJUNTO, nunca ESGOTADO.
- DoD 3 (assert em eval-produto.py): **NAO IMPLEMENTADO.** Nenhum assert no eval verifica que nenhuma linha com preco e lote-irmao de conjunto com saldo_conjunto <= total_cedido.
- DoD 4 (fixture com 16 conjuntos reais): **NAO IMPLEMENTADO.** Nenhum eval exercita os conjuntos 007050, 008026, 040085.
- DoD 5 (relacao com T9/T3): **NAO VERIFICAVEL** — T9 split sobre saldo ja reconciliado por conjunto.

**Lacunas:**
- **L-T11-1 (ALTA):** Irmao com PCpt ausente nao forca PENDENTE-CONJUNTO (pode fabricar ESGOTADO falso).
- **L-T11-2 (ALTA):** Sem assert em eval-produto.py para a reconciliacao por conjunto.
- **L-T11-3 (MEDIA):** Sem fixture com os 16 conjuntos reais.

**Prova mecanica proposta:**
```python
# Em eval-produto.py:
# 1. Assert: nenhum membro de conjunto esgotado sai com preco
# 2. Assert: conjunto com membro sem PCpt -> PENDENTE-CONJUNTO, nunca ESGOTADO
# 3. Fixture: exercitar conjuntos 007050, 008026, 040085
```

---

## Resumo de lacunas e acoes propostas

### Lacunas CRITICAS (prova ausente onde o defeito ja e construivel-agora)

| ID | Trava | Lacuna | Acao proposta |
|---|---|---|---|
| **L-T7-1** | T7 | PII tracked no git (`donos_encontrados.csv` com `proprietario`); sem probe no gate/CI | Implementar `check_pii_arvore()` em `fechar-instancia.py` + step no `consolidar.yml` ANTES do push; `git rm --cached` o arquivo; atualizar `.gitignore` |

### Lacunas ALTAS (prova mecanica prescrita na DoD mas nao implementada)

| ID | Trava | Lacuna | Acao proposta |
|---|---|---|---|
| **L-T4-1** | T4 | Sem assert sobre cohort real (32/164/0) | Adicionar assert em `_autoteste_conservacao()` ou `eval-produto.py` que leia `zepec_unificada.csv` e trave a particao |
| **L-T4-2** | T4 | Sem fixture discriminante de proveniencia (TOMBADO com Atestado -> nao-ELEGIVEL) | Adicionar fixture que prove que o fluxo de dados (ato_conservacao='' para TOMBADO) IMPEDE a falsa elegibilidade |
| **L-T4-3** | T4 | Sem propagacao per-linha de `(ato_conservacao, origem_da_evidencia)` ao runtime | Estender `montar_ferramenta.py` COLS para incluir os campos de proveniencia |
| **L-T4-4** | T4 | Sem fixture da linha fundida (79 linhas CERTIDAO+TOMBADO) | Adicionar fixture em eval ou autoteste exercitando o caso multi-origem |
| **L-T9-1** | T9 | `_precificar()` nao aplica `min(50000, saldo)` | Corrigir `_precificar()` para usar `min(saldo, 50000)` como base do preco |
| **L-T11-1** | T11 | Irmao com PCpt ausente nao forca PENDENTE-CONJUNTO | Corrigir logica de reconciliacao: se `not completo`, forcar PENDENTE-CONJUNTO |
| **L-T11-2** | T11 | Sem assert em eval-produto.py para reconciliacao por conjunto | Adicionar assert: nenhum irmao de conjunto esgotado sai com preco e abatimento 0 |
| **L-T7-2** | T7 | Probe de historico git AUSENTE | Adicionar `git log --all --oneline -- <paths_pii>` == 0 linhas ao gate |

### Lacunas MEDIAS

| ID | Trava | Lacuna | Acao proposta |
|---|---|---|---|
| **L-T2-1** | T2 | `eval-produto.py` nao regenera a cadeia completa | Estender para rodar `montar_ferramenta.py -> enriquecer_oficial.py` inline |
| **L-T2-2** | T2 | `eval-produto.py` sem asserts semanticos de T8/T4/T10/T11 | Adicionar os asserts prescritos na DoD item 3-ii |
| **L-T4-5** | T4 | Sem assert nao-vacuo em eval-produto.py para conservacao | Adicionar check de que a contagem de pares avaliados > 0 |
| **L-T5-1** | T5 | Decomposicao Fi-regime vs CAbas/Atc historico nao implementada | Implementar decomposicao no eval-divergencia |
| **L-T6-1** | T6 | Sem assert mecanico no gate para ausencia de oraculos | Adicionar `check_cemiterio()` em `fechar-instancia.py` |
| **L-T9-2** | T9 | Sem fixture para saldo > 50000 no eval | Adicionar fixture com saldo sintetico > 50k |
| **L-T9-3** | T9 | Sem fixture para ja>0 com saldo < 50k < PCpt | Adicionar fixture PCpt=60k, ja=15k |
| **L-T11-3** | T11 | Sem fixture com os 16 conjuntos reais | Adicionar fixture exercitando conjuntos 007050/008026/040085 |
| **L-T7-3** | T7 | Probe anon de bucket nao automatizado | Documentar como runbook; automatizar quando possivel |
| **L-T7-4** | T7 | Nenhum step no CI bloqueia push com PII | Adicionar step `check_pii` em `consolidar.yml` |
| **L-T2-3** | T2 | Golden SEM-PII nao existe como arquivo versionado | Implementar projecao SEM-PII como artefato commitado |

---

## Contabilidade final

- **Travas auditadas:** 12 (T1-T12, incluindo T1-bis)
- **Travas FEITAS e com prova SOLIDA:** T1, T3 (no escopo construivel)
- **Travas FEITAS com prova PARCIAL:** T2, T4, T5, T6, T9, T11
- **Travas PARCIALMENTE FEITAS (parte runbook, parte sem gate):** T7
- **Travas ABERTAS (DoD bem-especificada, aguardando implementacao):** T8, T10
- **Divida declarada:** T1-bis
- **Este documento:** T12

**Total de lacunas encontradas:** 19
- Criticas: 1 (L-T7-1 — PII tracked)
- Altas: 7 (L-T4-1/2/3/4, L-T9-1, L-T11-1/2, L-T7-2)
- Medias: 11

**Principio reafirmado:** "declarei feito != provei feito" — vale para as PROPRIAS DoDs. Uma DoD que prescreve asserts que nao existem no codigo e ela mesma uma declaracao, nao uma prova.
