# HANDOFF — FSCE, pendências e achados não-corrigidos (2026-07-10, PU 18)

> Doc de rede (D83 — "não deixar cair"): o que esta sessão FEZ, o que RESTA e a **receita exata** de
> como terminar, para que nada viva só na memória da conversa. Complementa os banners de `PROXIMA-INSTANCIA.md`
> e o `BACKLOG.md`. Estado da produção ao escrever: `main` @ `af57815`, gate **23/23 VERDE**, CI 2/2 verde.

## 0. O que foi à produção nesta sessão (3 PRs mesclados)
- **#29** — auditoria 10 achados (7 lentes) + G2 fechado (zona-base 377/377).
- **#30** — ★ resgate do **motor FSCE** (resolve o mistério Fi≈2,4) + 25 gabaritos TDC reais + consolidação de órfãos.
- **#31** — correção de registro (órfãos consolidados; deleção de refs pendente por 403).

---

## 1. ★ FSCE — como ATIVAR no pipeline (a peça que falta)

**O que já está na produção (feito):**
- `engines/tdc/pcpt.py`: `pcpt_sem_doacao(atc, cabas, fi=None, setor_central=False)`. Quando `setor_central=True`
  E terreno ≤ 1.000 m², aplica **FSCE=2,0** (Art. 57, Lei 17.844/2022): `PCpt = Atc × CAbás × Fi × FSCE`.
  Default `False` → retrocompatível (não muda nada existente).
- Gates provando: `evals/ground-truth/gabaritos/eval-formula-zepec.py` (4/4 reproduz o Diário Oficial) +
  `pcpt.py --demo` (autoteste FSCE) — ambos no CI e no `fechar-instancia.py`.
- `scripts/preencher_cabas_do_wfs.py`: **gera a coluna `na_aiu_sce`** ('1' = dentro do perímetro AIU-SCE)
  a partir de `zepec/oficial/zonas_377_geosampa.csv` (dado GeoSampa WFS) → escreve em `zona_base_cedente.csv`
  e pode acrescentá-la a `zona_por_cedente.csv`.

**O que FALTA (o hook está DORMENTE — o engine sabe calcular, mas o pipeline nunca passa `setor_central=True`):**

1. **Popular `na_aiu_sce` no `zona_por_cedente.csv` de produção (377/377).**
   - O `zona_por_cedente.csv` atual (main) tem 377/377 CAbás, mas **NÃO tem a coluna `na_aiu_sce`**.
   - `preencher_cabas_do_wfs.py` gera essa coluna, mas foi escrito sobre a cobertura ANTERIOR (366) — precisa
     **reconciliar**: reaplicar o `na_aiu_sce` (de `zonas_377_geosampa.csv`) por SQL sobre o CSV 377/377 atual,
     SEM reverter a cobertura de CAbás nova. (Foi por isso que NÃO trouxemos o `zona_por_cedente.csv` da branch
     órfã — ela tinha `na_aiu_sce` mas cobertura antiga.)

2. **Ligar o gancho em `zepec/enriquecer_oficial.py`** (hoje NÃO tem FSCE). Receita EXATA (da branch órfã
   `project-analysis-pending-20wc81`, auditada e correta — o **filtro ZEPEC-BIR é obrigatório**):
   ```python
   # FSCE — Setor Central (Art. 57, Lei 17.844/2022): pertinência à AIU-SCE vem do overlay GeoSampa
   # (coluna na_aiu_sce em zona_por_cedente; '1' = dentro). O engine aplica FSCE=2,0 só se terreno ≤ 1.000 m².
   # ★ FILTRO ZEPEC-BIR (Art. 57 restringe a BIR): a classificação vem do CADASTRO (tipo_zepec), NÃO do
   #   selo do polígono GeoSampa (que pode dizer ZEPEC_APC a um imóvel BIR pela Declaração). Sem o filtro,
   #   um 'tombado'/'APC' ≤1.000 m² dentro da AIU-SCE receberia FSCE indevido (dobraria o PCpt).
   eh_bir = "BIR" in (r.get("tipo_zepec") or "").upper()
   na_sce = bool(z and str(z.get("na_aiu_sce", "")).strip() == "1") and eh_bir
   if atc and cabas:
       e = ENGINE.pcpt_sem_doacao(atc, cabas, setor_central=na_sce)   # ← passar setor_central=na_sce
       ...
   ```
   (`z` = a linha de `zona_por_cedente` casada por SQL; `r` = a linha do cedente.)

3. **Regenerar o pipeline** (`enriquecer_oficial.py` → `lista_prospeccao.py`) e **provar**: `eval-produto`
   (15/15) + `eval-formula-zepec` (4/4) + `eval-zona-cabas` seguem verdes; os cedentes ZEPEC-BIR dentro da
   AIU-SCE ≤1.000 m² passam a mostrar PCpt dobrado (com citação Art. 57 na memória de cálculo).

**DoD:** um cedente ZEPEC-BIR conhecido dentro da AIU-SCE (ex.: SQL 0010800016, gabarito Termo 006/2026 = 717,60 m²)
sai da lista com `pcpt_m2 = 717,60` e memória citando `× FSCE(2.0) (Art. 57, Lei 17.844/2022)`.

**Bloqueio real:** o dado de pertinência `na_aiu_sce` por cedente vem do **overlay do perímetro AIU-SCE** (GeoSampa
WFS) — `zonas_377_geosampa.csv` traz isso para os 377 sob selo ZEPEC. Se algum cedente BIR estiver fora desses 377,
precisa de nova coleta GeoSampa (roda no hub `portfolio-automacoes`, runner `brasil`).

---

## 2. Achados da AUDITORIA PROFUNDA (7 lentes) que NÃO foram corrigidos

> A auditoria desta sessão corrigiu 10 (RAG-01..04, ENG-01/02/03, PIPE-01, GOV-01, COD-01) + EVAL-04. Os abaixo
> foram TRIADOS como design/bloqueado/baixa-prioridade e ficam registrados para não se perderem.

| id | Sev | Achado | Por que não foi feito / caminho |
|---|---|---|---|
| **PIPE-02** | alta | CI (`consolidar.yml`) não regenera/commita os artefatos de `zepec/` (só RAG/MANIFESTO). | Decisão de design: o pipeline completo depende de dados grandes. Caminho: gerar em CI só se os insumos estiverem no repo, ou aceitar que `zepec/*.csv` são commitados à mão pela instância. |
| **EVAL-01** | alta | `saldo_pcpt_m2` e `preco_proxy_brl` não têm teste de valor-ouro (golden). | Precisa de valores esperados de domínio (o dono/uma fonte). Caminho: ancorar ≥3 cedentes com saldo/preço conferidos manualmente e travar no `eval-produto`. |
| **EVAL-02** | média | Auto-testes de `oodc.py`/`fp.py` são circulares (o teste usa a própria fórmula). | Por design o `eval-produto` (ancorado na LEI, não-circular) é a rede. Caminho: se quiser, um golden externo por engine. |
| **COD-02** | média | `montar_ferramenta.py` usa `float` em campos financeiros (contaminação de precisão). | Caminho: migrar os campos monetários/área para `Decimal` (como em `pcpt.py`/`oodc.py`). Baixo risco, mecânico. |
| **COD-03** | baixa | `pcpt.py` quantiza `Q2=0.01`; `oodc.py` usa 3 decimais no UTXO. | Consistência de precisão entre engines. Verificar se o produto final precisa de casas iguais. |
| **GEO-02** | média | `overlay_zona.py` mistura selo ZEPEC com zonas de zoneamento. | Caminho: separar as duas camadas (selo × zona-base) explicitamente. |
| **GEO-03** | alta | Shapefiles referenciados por `overlay_zona.py` (SIRGAS_SHP_LOTES_*) não estão no repo (Drive). | Bloqueio externo: baixar LOTES do Drive p/ teste de integração do overlay (G1). |
| **GEO-04** | média | `vedacao_geo.py` (AUE, 741 polígonos) não está integrado ao pipeline (só substring cobre a vedação). | Bloqueio: precisa de coordenadas de lote (LOTES shapefiles) p/ ponto-em-polígono. É o "resto" do T8. |
| **ENG-04/05/06** | baixa | Achados menores da auditoria de sessão anterior (ver histórico). | Baixa prioridade; revisitar se o engine for reescrito. |

> Nota: **EVAL-03** (arquivo órfão `termo-006-2026.json` na subpasta `gabaritos/`) foi resolvido de fato —
> o arquivo agora tem status **RESOLVIDO** com a explicação FSCE e é lido pelo `eval-zona-cabas.py`.

---

## 3. Decisões e ações que dependem do DONO

1. **Deletar os 7 refs órfãos** (conteúdo 100% no main — nada se perde). O `git push --delete` da sessão dá
   **HTTP 403** (o token pusha commits mas não deleta refs; sem tool MCP de delete-branch). Ação do dono:
   GitHub → aba **Branches** → deletar:
   `claude/d164-caixafix-2026-07-08`, `claude/liberar-ferramentas`, `claude/opiniao-areas-escritorio`,
   `claude/pu-move-laudo-2026-07-08`, `claude/pu-regularizacao-2026-07-08`,
   `claude/project-analysis-pending-20wc81`, `claude/potential-urban-instance-jsgvth`. (Atualiza B-23.)
2. **Ativar FSCE no pipeline** — ver §1 (precisa reconciliar `na_aiu_sce` sobre o `zona_por_cedente.csv` 377/377).
3. **Política de CI (D168)** — a branch `claude/instance-concurrency-94pbeg` (NÃO deletar — tem conteúdo único
   fora do main) propõe **`linter-estado` só no `push`** (tira o gatilho `pull_request`, −50% de runs de Actions,
   mas deixa os PRs sem o linter). Decisão do dono: aplicar ou descartar. É o único conteúdo órfão restante que
   é uma **mudança de política** (não um dado) — por isso ficou de fora do consolidado.

---

## 4. Estado das branches remotas (ao escrever)
- `main` — produção (`af57815`).
- `claude/pu-project-organization-l67ond` — branch de trabalho, == `main` (não órfã).
- 7 refs órfãos (§3.1) — CONTEÚDO no main; refs pendentes de deleção pelo dono (403).
- `claude/instance-concurrency-94pbeg` — proposta de política de CI (§3.3), decisão do dono.
