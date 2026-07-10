# HANDOFF MESTRE — Sessão 2026-07-10 (PU 18) — ZERO-COMPRESSÃO, HONESTÍSSIMO

> **Para quem vai produzir a seguir.** Este doc é a rede de segurança total desta sessão (doutrina D83 —
> "nada cai"; zero-compressão — "nada se comprime"). Registra TUDO: o que foi feito e provado, o que ficou
> pela metade, o que EU (a instância anterior) errei e corrigi, e as RECEITAS EXATAS para a próxima instância
> executar. Na dúvida, documentei. Se algo aqui contradiz um banner curto de `PROXIMA-INSTANCIA.md`, **este doc
> é o detalhe canônico**; o banner é o resumo.
>
> **Estado da produção ao fechar:** `main` @ `a870df3`. Gate local `scripts/fechar-instancia.py` = **23/23 VERDE**.
> CI 2/2 verde (o apagão de infra do GitHub Actions se resolveu ~14:00 UTC). 5 PRs mesclados nesta sessão: #29,
> #30, #31, #32, #33. Working tree limpo. Branch de trabalho `claude/pu-project-organization-l67ond` == main.

---

## ÍNDICE
- PARTE A — O que foi FEITO e PROVADO (com a prova de cada)
- PARTE B — O que a próxima instância deve PRODUZIR (receitas exatas, acionáveis)
- PARTE C — Ações que dependem do DONO / Escritório
- PARTE D — HONESTIDADE: onde eu errei, o que NÃO validei, riscos cegos
- PARTE E — Mapa de arquivos + comandos exatos
- PARTE F — Decisões e por quês (para não re-litigar)

---

## PARTE A — O QUE FOI FEITO E PROVADO NESTA SESSÃO

### A.1 — Auditoria profunda (7 lentes): 10 achados corrigidos (PR #29)
Corrigidos e provados (cada um com fix no código + gate verde):
- **RAG-01 (alta):** `scripts/indexar.py` só promovia itens `fatiado` → 4 leis ficavam presas em `tagueado`
  (11152/15044/17202/17577). Fix: aceitar `tagueado`/`validado`. MANIFESTO 24→**28 indexado**.
- **RAG-02 (alta):** `scripts/consolidar.py` só tinha o check de falso-verde (indexado sem chunk). Fix: check
  REVERSO adicionado (chunks sem status indexado).
- **RAG-03 (média):** `scripts/grafo_remissoes.py` emitia 1108 duplicatas (31,5%). Fix: dedup por
  `(lei_id, chunk_id, tipo, alvo)`. 3518→**2410 arestas**.
- **RAG-04:** MANIFESTO inconsistente — auto-corrigido ao rodar o fix RAG-01.
- **ENG-01 (alta):** `engines/tdc/oodc.py` lia o Fi de doação de `motor00/travas_operacionais_v6.1.json` (viola
  anti-oráculo 1.3). Fix: delega ao `pcpt.py`, que lê de `tabelas/*.csv`.
- **ENG-02 (alta):** faltava `regularizacao_fundiaria` (Art.127 §1º III, Fi=0.8) — adicionado via delegação.
- **ENG-03 (média):** o grep-gate anti-oráculo no `consolidar.yml` não cobria `motor00/` (só `CODEX-*.md`). Fix:
  guard `["']motor00/` (exceto `travas_operacionais`, que é config de engine legítima — precisão/tolerância).
- **PIPE-01 (média):** pipeline ZEPEC dessincronizado — regenerada a cadeia `montar_base → montar_ferramenta →
  enriquecer_oficial → lista_prospeccao`.
- **GOV-01 (média):** o eval `eval-zona-mutacao.py` (G6) estava no CI mas fora do gate local. Fix:
  `fechar-instancia.py` → **22 checks** (era 21).
- **COD-01 (média):** `zepec/montar_ferramenta.py` `_num()` não tratava ponto-milhar BR sem vírgula
  ("1.500" virava 1.5 em vez de 1500). Fix: `elif re.fullmatch(r'\d{1,3}(\.\d{3})+', x)`. Removido dead code
  `norm_sql()`.
- **EVAL-04 (defensivo):** `evals/rodar-evals.py` agora pula `status == "aguardando_engine"` além de
  `aguardando_verbatim`. Protege o `gabarito-iptu-vv.json` de quebrar o gate quando ativado.

### A.2 — G2 fechado: zona-base 377/377 (100%) (PR #29)
Os 11 cedentes ZEPEC sem CAbás (10 `sem_lote` no GeoSampa + 1 `Praça/Canteiro`) foram resolvidos por fallback
**PDE Art. 14 §1º** (CAbás=1 em TODO o Município, exceto ZEPAM/ZPDSr/AC-1/AC-2/AVP-1 — nenhum dos 11 é zona de
exceção). Fix em `zepec/pipeline/resolver_zona_geosampa.py`: (a) `sem_lote` → `r["ca_basico"]="1"` +
`fonte="PDE_Art14§1(sem_lote)"`; (b) na função `resolver`, 4ª tentativa: zona ∉ exceções → CAbás=1. Resultado:
`irresolvivel=0`, CAbás total **3.693/3.693**. Fonte rastreável na coluna `fonte` do CSV.

### A.3 — ★ FSCE resgatado: o mistério Fi≈2,4 EXPLICADO no engine (PR #30)
**O achado central da sessão.** Os imóveis JA_DECLARADO divergiam ~2× do PCpt escalonado (ex.: Termo 006/2026 =
717,60 m² oficial vs. 358,80 m² escalonado). O projeto tratava isso como "Fi declarado ≈2,4, pendente do acervo de
Termos". **Nunca foi Fi=2,4.** É **Fi(1,2 Art.24 LPUOS) × FSCE(2,0)** — o **Fator Setor Central** do
**Art. 57, Lei Municipal 17.844/2022** (AIU-SCE / "Requalifica Centro"), aplicável a ZEPEC-BIR com terreno ≤ 1.000 m².

- Motor: `engines/tdc/pcpt.py` `pcpt_sem_doacao(atc, cabas, fi=None, setor_central=False)`. Com `setor_central=True`
  E terreno ≤ 1.000 m²: `PCpt = Atc × CAbás × Fi × 2,0`. Default `False` → **retrocompatível** (gate intacto).
- **Prova:** `evals/ground-truth/gabaritos/eval-formula-zepec.py` reproduz EXATO **4 Declarações oficiais** do
  Diário Oficial: 717,60 (299×1×1,2×2) · 1468,0 (734×1×1,0×2) · 1176,0 (490×1×1,2×2) · 768,0 (320×1×1,2×2). 4/4 OK.
- Ground-truth resgatado (25 gabaritos TDC reais coletados do Diário Oficial pela extensão do navegador do dono):
  `evals/ground-truth/gabaritos/gabaritos-tdc-doc.csv`, `coletados/gabaritos-doc-extraidos.csv/json`,
  `GABARITO-FORMULA-ZEPEC-BIR.md` (âncora legal), `ACHADO-GABARITOS-DOC-2026-07-08.md`.
- Também resgatados: `scripts/preencher_cabas_do_wfs.py`, `zepec/oficial/zona_base_cedente.csv`,
  `zonas_377_geosampa.csv`, `docs/ENCERRAMENTO-E-HANDOFF-2026-07-05.md` (histórico).
- Gates novos (CI + `fechar-instancia.py`, agora **23 checks**): `eval-formula-zepec.py` (FSCE 4/4) +
  `eval-zona-cabas.py` (regressão do overlay GeoSampa).

> **⚠️ MAS NÃO ESTÁ NO PRODUTO — ver PARTE B.1 e PARTE D.** O FSCE está provado NO ENGINE; a lista de cedentes
> (`lista_prospeccao.csv`) ainda mostra o PCpt SEM FSCE (pela metade) no Setor Central, porque a cadeia de DADO
> (`na_aiu_sce`) não está fechada.

### A.4 — Consolidação de órfãos no repo PU: 8 branches (PRs #30/#31)
Havia 8 branches remotas do PU com commits únicos NÃO no main. Auditei cada uma (análise de supersessão) e trouxe
só o conteúdo NOVO que não reverteria o PU 18 mais recente:
- **5 100%-superadas** (conteúdo já no main via PU 18): `d164-caixafix-2026-07-08`, `liberar-ferramentas`,
  `opiniao-areas-escritorio`, `pu-move-laudo-2026-07-08`, `pu-regularizacao-2026-07-08`.
- **2 cherry-pick de arquivos novos:** `project-analysis-pending-20wc81` (pacote FSCE + gabaritos — verificado
  arquivo-a-arquivo que os 11 arquivos novos vieram) e `potential-urban-instance-jsgvth` (só o doc de encerramento).
- **NÃO trazido** (reverteria o mais novo): `zona_por_cedente.csv` (377/377 é mais novo que o do branch),
  `zepec/enriquecer_oficial.py` (G4/T8 mais novos), `BACKLOG.md`/`PROXIMA-INSTANCIA.md` do branch.
- **Como pcpt.py foi trazido sem quebrar nada:** o diff `main→branch` de `pcpt.py` é um SUPERSET limpo (+34/−5, as
  −5 são a reformatação do `return`; nenhuma linha do main foi perdida). Verificado antes de sobrescrever.

### A.5 — Registro honesto: refs órfãos NÃO deletados (PR #31)
O dono autorizou deletar os 7 refs redundantes, mas `git push --delete` deu **HTTP 403** (o token da sessão remota
pusha commits mas NÃO deleta refs; não há tool MCP de delete-branch). Corrigi os docs que diziam "deletadas" →
"consolidadas; refs pendentes de deleção pelo dono". B-23 atualizado.

### A.7 — Varredura final "nada órfão" (PRs #35 no PU + #26 no hub)
Sob pressão do dono ("não quero nada fora de produção e órfão"), varri os DOIS repos com teste preciso
(arquivo/conteúdo único fora do main). Achei 3 órfãos de conteúdo REAIS que eu tinha deixado passar, e **resgatei
os 3**:
- **[PU] `docs/pagina-mapa-do-mou.html`** (501 linhas) — a página da unidade no Mapa Vivo do Portfólio (D159/D161),
  criada nesta sessão por outra instância. → main (PR #35).
- **[PU] política CI D168** — `linter-estado.yml` sem `pull_request` (cota de Actions, "propagada a todos os repos").
  → main (PR #35).
- **[HUB] cofre §4.1** — Gmail+Drive por MCP (conta do MOU) no `ACESSOS-FERRAMENTAS.md`, da branch
  `bitsuki-instance-setup-aabhm7`. → main do hub (PR #26).
- **NÃO re-injetei 2 "falsos órfãos":** as cartas `caixa-de-entrada/do-escritorio/2026-07-07_...opiniao-areas.md`
  e `2026-07-08_...REGULARIZACAO-pu.md` aparecem como "novo arquivo" nas branches, mas o conteúdo JÁ está no main em
  `caixa-de-entrada/processados/` (verificado: a versão processada contém 100% das linhas). Trazê-las de volta à
  caixa ATIVA seria re-injetar carta processada como pendente (bug do mecanismo de caixa, D144/D-CAIXA-FIX). Deixadas.
- **Resultado:** ZERO conteúdo órfão nos dois repos. Resta só a DELEÇÃO dos refs redundantes (bloqueada por 403 —
  ação do dono via UI). Ver PARTE C.

### A.6 — Auditoria das 23 branches do HUB `portfolio-automacoes` (PR #33)
Na 1ª passada declarei o hub "limpo" sem olhar — **erro** (ver PARTE D). Auditei as 23 branches com commits únicos:
- **12 `geosampa-*`**: TODAS SUPERADAS (squash-merges via PRs #6–#19 do hub). Incluindo `geosampa-sce` (a lógica
  `na_aiu_sce`, PR #18) → já na main do hub.
- **10 de 11 branches de portfólio** (`cofre-*`, `drive-*`, `hub-*`, `instance-concurrency`): SUPERADAS.
- **★ 1 exceção com conteúdo ÚNICO não-mesclado:** `claude/bitsuki-instance-setup-aabhm7` — seção §4.1 do cofre
  (Gmail + Drive via MCP). Território do Escritório do MOU (D38/D120), não do PU.

---

## PARTE B — O QUE A PRÓXIMA INSTÂNCIA DEVE PRODUZIR (receitas exatas)

### B.1 — ★★★ ATIVAR o FSCE no produto (a maior entrega pendente)
O engine sabe calcular o FSCE, mas o **pipeline nunca passa `setor_central=True`** porque o dado de pertinência
`na_aiu_sce` não existe. Cadeia completa, em ORDEM:

**Passo 0 — [HUB, ação do dono/Escritório] Produzir e VALIDAR `na_aiu_sce`.**
- O coletor JÁ está na main do hub: `portfolio-automacoes:tools/geosampa/siszon_probe.js` (função `dentroSCE()`,
  `INTERSECTS(ge_poligono, POINT(x y))` contra `geoportal:requalifica_centro_perimetro_geral` /
  `geoportal:perimetro_aiu`). Emite `zonas_377.csv` com header `sql_mestre,zona_v3,zona_18177,na_aiu_sce,status`.
- **Re-rodar** `.github/workflows/geosampa-siszon.yml` no runner `brasil` até um bulk limpo (guard exige ≥90% de
  sucesso, ~357/377). Runs throttled pelo IP do GeoSampa (Imperva) não gravam. O `main:zonas_377.csv` de hoje tem
  dado bom (367 ok) mas SEM a coluna; a única rodada que já a populou (`ef69878`) foi revertida por throttling.
- **⚠️ VALIDAR ANTES DE CONFIAR:** naquela amostra, **288/306 lotes deram `na_aiu_sce=1` (~94% "dentro")** —
  implausível (o perímetro requalifica_centro é pequeno). Provável bug: camada SCE errada, SRID/projeção do POINT
  trocado, ou INTERSECTS invertido. **DoD do dado:** um mini-eval com ~5 SQLs sabidamente FORA do Setor Central
  deve dar `na_aiu_sce=0`. Sem isso, o FSCE dobraria o PCpt de imóveis que NÃO são do Setor Central (erro grave).

**Passo 1 — [PU] Descer o dado e popular `na_aiu_sce` no `zona_por_cedente.csv` (377/377).**
- Trazer o `zonas_377.csv` (com `na_aiu_sce` validado) do hub para `zepec/oficial/zonas_377_geosampa.csv`.
- `scripts/preencher_cabas_do_wfs.py` já casa por SQL e faz o patch — reaplicar `na_aiu_sce` sobre o CSV 377/377
  atual, SEM reverter a cobertura de CAbás. Ele LÊ `na_aiu_sce` do WFS (não a produz).

**Passo 2 — [PU] Ligar o gancho em `zepec/enriquecer_oficial.py`** (hoje NÃO tem FSCE). Receita EXATA (auditada,
da branch `project-analysis-pending-20wc81` — o **filtro ZEPEC-BIR é obrigatório**):
```python
# FSCE — Setor Central (Art. 57, Lei 17.844/2022): pertinência à AIU-SCE vem do overlay GeoSampa
# (coluna na_aiu_sce em zona_por_cedente; '1' = dentro). O engine aplica FSCE=2,0 só se terreno ≤ 1.000 m².
# ★ FILTRO ZEPEC-BIR: Art. 57 restringe a BIR. A classificação vem do CADASTRO (tipo_zepec), NÃO do selo do
#   polígono GeoSampa (que pode dizer ZEPEC_APC a um imóvel BIR pela Declaração). Sem o filtro, um 'tombado'/'APC'
#   ≤1.000 m² dentro da AIU-SCE receberia FSCE indevido (dobraria o PCpt).
eh_bir = "BIR" in (r.get("tipo_zepec") or "").upper()
na_sce = bool(z and str(z.get("na_aiu_sce", "")).strip() == "1") and eh_bir
if atc and cabas:
    e = ENGINE.pcpt_sem_doacao(atc, cabas, setor_central=na_sce)   # ← passar setor_central=na_sce
    ...
```
(`z` = linha de `zona_por_cedente` casada por SQL; `r` = linha do cedente.)

**Passo 3 — [PU] Regenerar + provar.** `enriquecer_oficial.py` → `lista_prospeccao.py`. Gates verdes:
`eval-produto` (15/15), `eval-formula-zepec` (4/4), `eval-zona-cabas`. **DoD:** SQL 0010800016 (Termo 006/2026)
sai da lista com `pcpt_m2 = 717,60` e memória citando `× FSCE(2.0) (Art. 57, Lei 17.844/2022)`.

### B.2 — Achados da auditoria profunda NÃO-corrigidos (registrados, não feitos)
| id | Sev | Achado | Caminho / DoD |
|---|---|---|---|
| **PIPE-02** | alta | CI não regenera/commita artefatos de `zepec/` (só RAG/MANIFESTO). | Design: pipeline depende de dados grandes. Ou gerar em CI se insumos no repo, ou aceitar commit à mão. |
| **EVAL-01** | alta | `saldo_pcpt_m2` e `preco_proxy_brl` sem teste golden. | Ancorar ≥3 cedentes com saldo/preço conferidos e travar no `eval-produto`. |
| **EVAL-02** | média | Auto-testes de `oodc.py`/`fp.py` circulares. | Por design `eval-produto` (ancorado na lei) é a rede não-circular. Opcional: golden externo por engine. |
| **COD-02** | média | `montar_ferramenta.py` usa `float` em campos financeiros. | Migrar monetário/área para `Decimal` (como pcpt/oodc). Mecânico, baixo risco. |
| **COD-03** | baixa | `pcpt.py` quantiza Q2=0.01; `oodc.py` 3 decimais no UTXO. | Conferir se o produto final exige casas iguais. |
| **GEO-02** | média | `overlay_zona.py` mistura selo ZEPEC com zonas de zoneamento. | Separar as duas camadas explicitamente. |
| **GEO-03** | alta | Shapefiles de `overlay_zona.py` (SIRGAS_SHP_LOTES_*) não estão no repo. | Bloqueio: baixar LOTES do Drive p/ teste de integração (G1). |
| **GEO-04** | média | `vedacao_geo.py` (AUE, 741 polígonos) não integrado ao pipeline. | Bloqueio: coordenadas de lote (LOTES) p/ ponto-em-polígono. É o "resto" do T8. |
| **ENG-04/05/06** | baixa | Achados menores de sessão anterior. | Revisitar se o engine for reescrito. |

### B.3 — Backlog remanescente relevante (ver `BACKLOG.md` para o texto completo)
- **Fi declarado / acervo de Termos**: era o bloqueio nº1; o FSCE explica a maior parte. Ainda pode restar
  resíduo para JA_DECLARADO específicos — reavaliar DEPOIS do FSCE ativo no produto.
- **B-5 (embeddings):** camada semântica no `consultar.py` — destravado por decisão, falta chave de provedor.
- **B-21 (jurisprudência TDC):** corpus é TDC-cego (0/32 juris tratam de TDC) — captura de acórdãos (egress
  .gov.br = 403 / via Drive).
- **G1/T8 geometria fina:** dependem de LOTES shapefiles (Drive).

---

## PARTE C — AÇÕES QUE DEPENDEM DO DONO / ESCRITÓRIO
1. **Deletar 7 refs órfãos do PU** (conteúdo 100% no main; `git push --delete` deu 403). Via GitHub → Branches:
   `claude/d164-caixafix-2026-07-08`, `claude/liberar-ferramentas`, `claude/opiniao-areas-escritorio`,
   `claude/pu-move-laudo-2026-07-08`, `claude/pu-regularizacao-2026-07-08`, `claude/project-analysis-pending-20wc81`,
   `claude/potential-urban-instance-jsgvth`.
2. **[HUB] Re-rodar + validar a coleta `na_aiu_sce`** (runner `brasil`) — desbloqueia o FSCE (PARTE B.1, passo 0).
3. **Política de CI (D168)** — branch PU `claude/instance-concurrency-94pbeg` propõe `linter-estado` só no `push`
   (−50% de runs, mas PRs sem linter). Aplicar ou descartar.
4. **[HUB] Seção §4.1 do cofre** — branch `claude/bitsuki-instance-setup-aabhm7` (Gmail+Drive MCP) tem conteúdo
   único não-mesclado. Governança do Escritório (D38/D120): consolidar ou descartar.
5. **[HUB] Deletar refs redundantes das 22 branches superadas do hub** (mesmo 403; via UI).

---

## PARTE D — HONESTIDADE: onde EU errei, o que NÃO validei, riscos cegos

1. **Errei sobre o FSCE, duas vezes.** (a) Primeiro documentei como se estivesse pronto/no produto — **não está**.
   (b) Depois escrevi que "o coletor está órfão na branch `geosampa-sce`" — **errado**: ele já está na main do hub
   (PR #18). Corrigido no `HANDOFF-FSCE-E-PENDENCIAS-2026-07-10.md`. Lição p/ a próxima: **o FSCE está provado no
   engine, NÃO no produto**; o gargalo é o dado `na_aiu_sce`.
2. **Declarei o hub "limpo" sem auditar.** Só olhei a branch corrente. Havia 23 branches. Depois auditei — quase
   todas superadas, mas foi um furo de método. Se eu não tivesse sido cobrado, teria ficado por documentar.
3. **NÃO validei os 94% de `na_aiu_sce=1`.** Só sinalizei. Este é o **risco cego mais perigoso**: se o INTERSECTS
   estiver over-inclusivo e ninguém validar, ligar o FSCE vai DOBRAR indevidamente o PCpt de imóveis fora do Setor
   Central — pior que não ter FSCE. **A próxima instância NÃO deve ligar o FSCE no pipeline antes de validar isso.**
4. **A carta `2026-07-08_...mapa-vivo-e-metodo-FSCE.md`** que resgatei ficou na outbox ativa (`para-escritorio/`),
   2 dias velha, sem versão em `processados/`. Não verifiquei o estado de entrega — pode re-injetar como "pendente"
   ou estar stale. A próxima instância deve conferir se essa carta ainda faz sentido enviar ao Escritório.
5. **Não rodei `preencher_cabas_do_wfs.py` de ponta a ponta** contra os dados atuais — só rodei os evals que o
   consomem. Se os inputs mudaram, o script pode precisar de ajuste.
6. **Deleção de branches é bloqueada por 403** na sessão remota — não é o classificador de permissão (que o dono
   autorizou), é o token não ter escopo de deleção de ref. Não tem workaround do meu lado (nem via MCP).
7. **"Mistério Fi≈2,4 RESOLVIDO"** nos banners/`portfolio-fragmento.json` é honesto SÓ no sentido de engine/prova
   matemática. Se a próxima instância ler só o banner, pode achar que o produto já está certo. **Não está.**

---

## PARTE E — MAPA DE ARQUIVOS + COMANDOS

**Arquivos do FSCE (produção):**
- `engines/tdc/pcpt.py` — motor com `setor_central` (FSCE).
- `evals/ground-truth/gabaritos/eval-formula-zepec.py` — prova FSCE vs Diário Oficial (4/4). Importa `pcpt`.
- `evals/ground-truth/gabaritos/eval-zona-cabas.py` — lê `zepec/oficial/zona_base_cedente.csv`.
- `evals/ground-truth/gabaritos/gabaritos-tdc-doc.csv` + `coletados/gabaritos-doc-extraidos.csv/json` — 25 gabaritos.
- `evals/ground-truth/gabaritos/GABARITO-FORMULA-ZEPEC-BIR.md` — âncora legal (Art. 57).
- `evals/ground-truth/gabaritos/termo-006-2026.json` — status RESOLVIDO (717,60 explicado).
- `scripts/preencher_cabas_do_wfs.py` — consome `na_aiu_sce` do WFS; patcheia `zona_por_cedente.csv`.
- `zepec/oficial/zona_por_cedente.csv` — 377/377 CAbás, **SEM** coluna `na_aiu_sce` (falta popular).
- `zepec/enriquecer_oficial.py` — **NÃO tem** o gancho FSCE (ligar — B.1 passo 2).

**Hub (`../portfolio-automacoes/`):**
- `tools/geosampa/siszon_probe.js` — coletor (tem `na_aiu_sce`, na main).
- `tools/geosampa/zonas_377.csv` — 367 ok, SEM `na_aiu_sce` (precisa re-rodar).
- `.github/workflows/geosampa-siszon.yml` — dispara a coleta no runner `brasil`.

**Comandos:**
- Gate local completo: `python3 scripts/fechar-instancia.py` (23 checks).
- Evals RAG: `python3 evals/rodar-evals.py` (29/29). Produto: `python3 evals/eval-produto.py` (15/15).
  Zona: `python3 evals/eval-zona-mutacao.py` (6/6). FSCE: `python3 evals/ground-truth/gabaritos/eval-formula-zepec.py` (4/4).
- Regenerar pipeline: `python3 zepec/enriquecer_oficial.py && python3 zepec/lista_prospeccao.py`.

---

## PARTE F — DECISÕES E POR QUÊS (para não re-litigar)
- **Merge (não squash) dos PRs:** doutrina zero-compressão — preserva os 37 commits, nada se joga fora.
- **Reiniciar `l67ond` da main após cada merge:** regra de branch-mesclada (PR mesclado = finished; follow-up é
  mudança fresca a partir do main).
- **NÃO merjar as branches órfãs inteiras:** reverteria docs/CSVs mais novos do PU 18. Só cherry-pick de arquivos
  NOVOS (verificado arquivo-a-arquivo que nada novo ficou para trás).
- **NÃO tocar as branches do hub além de auditar:** governança do Escritório do MOU (D38/D120); o PU propõe por
  branch/PR atribuído, não escreve por comando.
- **FSCE trazido mesmo com o dado faltando:** o ENGINE + a PROVA (4/4) + os gabaritos são valor real e verificável
  agora; a ativação no pipeline é a etapa seguinte, com dependência de dado explicitada. Preferi resgatar a jóia
  provada a deixá-la morrer numa branch órfã.
