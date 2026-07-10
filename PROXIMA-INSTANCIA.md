# PRÓXIMA INSTÂNCIA — o que fazer (Potencial Urbano)

> **★★★★★★★★★★★★ PU 18 (2026-07-10) — E2/E3 ENTREGUES: vintage obrigatório + medallion convention.**
> **E3 FEITO:** `docs/CONVENCAO-MEDALLION.md` — convenção medallion de 1 página (Bronze/Silver/Gold). Silver = `oficiais.*`. Sem governança por camada.
> **E2b FEITO:** upload scripts (`subir-oficiais-para-supabase.gs`, `subir-grandes-colab.py`) todos com `ano=AAAA` no path. Zero `dest` sem vintage.
> **E2c FEITO:** `consolidar.py` rastreia vintage+hash de cada `tabelas/*.csv` via `tabelas/METADATA.json` → seção `tabelas_vintage` no MANIFESTO (10 CSVs, 0 sem data_base).
> **E2 família-2c FEITO:** `montar_ferramenta.py` preserva datas por origem (`data_declaracao_iso`, `data_certidao_iso`, `data_tombamento_iso`) — nunca agrega origens distintas antes do dado bruto. `data_ref=max()` mantido como agregado Gold/apresentação.
> **Gate:** 14/14 eval-produto + 6/6 eval-zona-mutacao PASS. Pipeline regenerado.
> **E2 restantes (BLOCKED):** E2-0 (migrar tabelas Postgres sem vintage) depende de E4/Supabase infra.
> **PRÓXIMO na fila:** outros itens do backlog LOCAL.
>
> **★★★★★★★★★★★ PU 18 (2026-07-10) — T12 LACUNAS 16/19 RESOLVIDAS + G6 eval geo + E1 pipeline scripts + conservation bug fix.**
> **T12 auditoria: 17/19 lacunas resolvidas** (era 12/19; +5 esta sessão):
> - L-T4-3 ALTA (propagação `elegibilidade_conservacao` ao runtime — `montar_ferramenta.py` COLS)
> - L-T2-2 MEDIA (asserts semânticos T3 regime + T4 conservação no eval-produto: JA_DECLARADO→PENDENTE_FI_DECLARADO, 18 ELEGIVEL + 68 PENDENTE)
> - L-T11-3 MEDIA (fixture com 12 conjuntos reais no eval-produto)
> - L-T9-3 MEDIA (documentado: sem dados reais que casem ja>0+saldo<50k<PCpt — skip)
> - L-T5-1 MEDIA (decomposição Fi-regime: Fi explica 100% da divergência em 54 cedentes)
> **Sessão anterior (compactada):** L-T4-1/2/4, L-T7-2 (coorte real, discriminante, linhas mescladas, PII histórico).
> **G6 eval geo criado:** `evals/eval-zona-mutacao.py` — mutation test zona→CAbás (6/6 PASS, 5 casos). Gate no CI.
> **E1 pipeline scripts:** `recorte_q14.py` (criado), `filtro_iptu.py` (fix path), `refazer_oficial.sh` (criado).
> **Conservation bug fix:** pattern matching broadened para "Atestado de Preservação e Conservação".
> **Gate:** 20/20 evals + 14/14 eval-produto + 6/6 eval-zona-mutacao PASS.
> **Pipeline:** 2.280 chunks, 28 leis indexadas, 66 MANIFESTO, 3.518 remissões.
> **Restam (2/19):** L-T2-1 (cadeia completa no eval — CI já cobre), L-T2-3/L-T7-3 (baixas/runbook).
> **PRÓXIMO na fila:** (1) outros itens do backlog LOCAL, (2) T8 geometria fina (BLOCKED), (3) G1 overlay por área (BLOCKED).
>
> **★★★★★★★★★ PU 18 (2026-07-09) — T8 GUARD VEDAÇÃO Art.124§2 + B-4 +4 LEIS MUNICIPAIS INGERIDAS.**
> **T8 guard FEITO (parcial):** `enriquecer_oficial.py` BLOQUEIA PCpt/saldo/preço de imóveis vedados por Art.124§2 (AUE/APPa) ANTES do cálculo. 32 vedadas bloqueadas (13 tinham Atc+CAbás e recebiam PCpt indevido). `vedacao_geo.py` criado (carrega AUE shapefile 741 polígonos EPSG:31983; pronto p/ geometria fina quando coordenadas de lote estiverem disponíveis — LOTES shapefiles ou geocoding). **RESTA:** cruzar coordenadas de lote com shapefile AUE para pegar os ~28 vedados que a substring não alcança (precisa LOTES shapefiles).
> **B-4 +4 leis municipais** ingeridas do Drive verbatim: Lei 11.152/1991 (alíquotas IPTU progressivas), Lei 15.044/2009 (nova Tabela VI IPTU), Lei 17.202/2019 (regularização edificações, compartilhado), Lei 17.577/2021 (Requalifica Centro, compartilhado). `carimbar_dominio.py` atualizado. **3 leis inacessíveis** pelo MCP Drive (10.235/86, 13.250/01, 14.865/08 = PDFs scan sem camada de texto).
> **Pipeline:** 2.280 chunks, 28 leis indexadas, 66 MANIFESTO, 3.518 remissões. 20/20 evals + 8/8 eval-produto PASS.
> **PRÓXIMO na fila:** (1) itens do backlog que restam locais (G5/G6/E1/E7 — materializar overlay, eval geo, runner); (2) T8 geometria fina (BLOCKED: LOTES shapefiles); (3) G1 overlay por área (BLOCKED: idem); (4) B-5 camada semântica (BLOCKED: chave API).
>
> **★★★★★★★★ PU 18 (2026-07-09) — +3 LEIS TDC INGERIDAS + MOTOR Fp + T12 AUDITORIA + SHAPEFILES ZEPEC.**
> **Corpus TDC ampliado:** 3 leis baixadas do Drive e ingeridas verbatim: Lei 17.975/2023 (revisão intermediária PDE, 132 chunks, domínio compartilhado), Lei 18.081/2024 (revisão parcial LPUOS, 98 chunks, domínio compartilhado), Lei 18.222/2024 (PIU Arco Pinheiros, 62 chunks, domínio TDC). Pipeline: **2.201 chunks**, **24 leis indexadas**, **66 itens MANIFESTO**. Grafo de remissões regenerado: **3.416 arestas** (era 2.733). Gate VERDE: 20/20 evals + 8/8 eval-produto.
> **B-3 FECHADO:** engine Fp (Fator de Planejamento) `engines/tdc/fp.py` + tabela `tabelas/quadro6-fator-planejamento-fp.csv` (Quadro 6 PDE, 15 linhas, baixado do Drive). Decimal exato, fail-closed, citação obrigatória.
> **T12 FEITO:** auditoria mecânica de todas as 12 travas do Motor 1 → `docs/T12-AUDITORIA-DODS-2026-07-09.md`. 19 lacunas (1 CRÍTICA: PII donos_encontrados.csv tracked; 7 altas; 11 médias). Proposta de prova mecânica para cada.
> **ZEPEC shapefiles:** `.shp/.shx/.dbf/.prj` baixados do Drive (741 polígonos AUE, EPSG:31983, verificados com geopandas) → prepara T8 (vedação geométrica Art.124§2) e G1 (overlay por área).
> **PRÓXIMO na fila:** (1) ingerir as 7 municipais restantes do Drive (B-4: 10.235/86, 11.152/91, 13.250/01, 14.865/08, 15.044/09, 17.202/19, 17.577/21); (2) T8 (vedação geométrica com shapefiles AUE); (3) G1 (overlay por área — ZEPEC pronto, falta LOTES); (4) regenerar grafo de remissões completo com arestas inter-lei.
>
> **★★★★★★★ PU 18 (2026-07-09) — ZONA-BASE ZEPEC RESOLVIDA: 366/377 CAbás preenchidos via GeoSampa SISZON.**
> **Achado:** a coleta GeoSampa (`portfolio-automacoes/tools/geosampa/zonas_377.csv`) JÁ RODOU no runner `brasil` — 366/377 zonas-base sob o selo ZEPEC capturadas. **Ação:** `resolver_zona_geosampa.py` cruza zona_18177 → Quadro 3 LPUOS → CAbás; preenche `zona_por_cedente.csv` (era 3316 → agora **3682**/3693 com CAbás). Makefile atualizado (etapa 3.5). **Impacto na ponta:** prospecção com PCpt = **2.078** (era 1.879, +199); preço-proxy = **2.003** (era 1.809, +194). **Gabarito Termo 006/2026:** zona-base = ZC (CAbás=1); PCpt escalonado = 358,80 m² (Fi=1,2 Art.24); oficial = 717,60 m² (Fi declarado ≈2,4). Divergência 2× EXPLICADA pelo T3 (JA_DECLARADO vs escalonado). Status atualizado: `CABAS_RESOLVIDO_FI_PENDENTE`. 20/20 evals PASS, gate 16/17 (só git). **Irresolvíveis:** 10 sem_lote + 1 Praça/Canteiro sem zona_v3.
>
> **★★★★★★ PU 18 (2026-07-09) — COSTURA B-20 RESTANTE FEITA + IPTU PRIMEIRO TERRENO INGERIDO.**
> **Costura (commit `e5c04cb`):** `enriquecer_oficial.py` refatorado — Motor Fórmulas (`_calcular_pcpt`) separado do Motor Comercial (`_precificar`), cada trava num módulo (fachada `travas.py`), Makefile orquestrador criado. Output idêntico verificado, 20/20 evals PASS.
> **IPTU ingestão (commit `1d8326e`):** triagem de `_entrada/iptu/` (2/7 IPTU); Lei 15.889/2013 ingerida verbatim (md+json+17 chunks); tabelas extraídas: `iptu-aliquotas-faixa.csv` (15 faixas, Arts. 3/4/5) + `iptu-valor-construcao-m2.csv` (Tabela VI, 31 linhas). Fix I5 (tema[] anti-padrão). Âncora na fixture de domínio. **Pipeline:** 1.909 chunks, 21 leis, 63 MANIFESTO. Eval-domínio I1-I6 VERDE. Gate 17/17 VERDE.
> **PRÓXIMO na fila do cronograma:** (1) gabarito IPTU — calcular VV para 1 SQL do `iptu2026_cedentes.csv` usando tabelas extraídas, comparar com `v_venal_m2` oficial; (2) ingerir mais leis IPTU da `_entrada/` ou do Drive (7 municipais com PDF); (3) itens bloqueados pelo dono (T8, G1, G2, G4, B-4, B-5, B-21).
> **AUD-C05/C06 FEITOS** esta sessão (fatiar.py data_redacao + chunks tipo=anexo).
>
> **★★★★★ PU 18 (2026-07-06) — DRIVE LIMPO: dedup ESCOPADO à PU CONCLUÍDO (robô). FALTA 1 CLIQUE DO DONO.**
> Entregável da sessão = "o Drive limpo e saudável". **Arrumação:** 1.360/1.360 movidos (verificado). **Saneamento
> fase 1:** 13 duplicatas de CSV pesado → lixeira (verificado). **Dedup escopado à subárvore do Potencial Urbano**
> (não tocou outras unidades do MOU — decisão do dono "focar na PU mesmo"): o robô (conta de serviço, Editor) MOVEU
> **2.082 duplicatas** (417 grupos, ~41,52 GB) para a pasta única **`99 — DUPLICATAS-A-EXCLUIR`**
> (id `1tk7qx26pBLj7p0Gvxx4VNC53LlzdhUcl`, dentro do Potencial Urbano). **VERIFICADO** por leitura própria: log da
> Action `dedup-quarentena` run 28803222539 = `para_quarentena=2082 erros=0`; a pasta contém ~2.082 itens (ruído de
> consistência eventual do índice na listagem); as **4 canônicas** (socios/empresas/IPTU_2026/holdings em
> "03 — Tabelas & Engines" `1v4H2Ys...`) confirmadas VIVAS, com tamanho certo, FORA da quarentena.
> **AÇÃO ÚNICA DO DONO (fecha o entregável, libera ~41,52 GB):** abrir/rodar `drive-arrumacao/Trash-Quarentena-DONO-2026-07-06.gs`
> (Apps Script na conta do dono; DRY_RUN=true → confere ~2082 no Log → DRY_RUN=false → roda; depois ESVAZIAR A LIXEIRA).
> Alternativa manual: abrir a pasta `99 — DUPLICATAS-A-EXCLUIR`, selecionar tudo, excluir. O robô é Editor e NÃO pode
> mandar arquivo de outro dono à lixeira (403) — por isso o dono dá o último clique. **Toolchain:** `scripts/dedup_quarentena_sa.py`
> + `.github/workflows/dedup-quarentena.yml` (ensaio→real, escopo por `pastas_sob()` BFS). **Rastro completo abaixo neste bloco.**
>
> **★★★★ PU 18 (2026-07-05, tarde) — DESTRAVE GERAL + DECISÕES DO DONO. LEIA: `docs/DECISOES-2026-07-05.md` (D-DONO-7..13) + `docs/INVENTARIO-DRIVE-VIVO-2026-07-05.md` + rastro do `BACKLOG.md`.**
> O dono respondeu o relatório de pendências ITEM A ITEM. **Decisões:** preço = **preço LEGAL** (margem é
> do usuário — fork c encerrado); o projeto **não julga produto/mercado** e não re-pergunta estratégia
> (forks a/b); **olhar o Drive antes de extrair** (FEITO: inventário vivo via MCP só-leitura). **Pagos com
> prova:** AUD-A01·A10·B01(fixture)·T9·T11·G3-coletivo (ferramenta 6.131→4.360; 1.772 "Light"=1 bem
> COLETIVO) · **B-6 FECHADO** (grafo de remissões + 2 bugs lexicais no tokenizador; eval data-por-remissao
> ATIVO; 18/18) · P3/item-8 (fora-de-escopo ARQUIVADOS; corpus 61 itens). **Inventário do Drive provou:**
> arrumação NUNCA rodou (0/1.360 movidos); **Decreto 57.536 + Quadro 2A + Quadro 6 + AUE/APPa + SIRGAS
> 96 distritos EXISTEM no Drive** (extração da onda TDC destravada); 5 municipais NÃO existem no Drive
> (captura externa); 58.289/18 sem corpo; ~28 GB duplicatas vivas. **PRÓXIMO:** (1) extrair do Drive a onda
> TDC (57.536 → `_entrada` → promover/fatiar/indexar; AUD-A11) + as 7 municipais com PDF; (2) T8/G1 com a
> geometria oficial agora localizada; (3) restam AUD-C05/C06, B08/B09, T12, G5·G6·E1–E5·E7. **DONO:** rodar
> os 2 prompts de `extracao/PROMPT-EXTENSAO-BRANCHES-E-SUPABASE.md` + Apps Scripts da arrumação + chave de
> embeddings (B-5) + revisão humana de ≥1 lei-âncora.
>
> **★★★ ESTADO PÓS-M0 + AUDITORIA 2026-07-05 — LEIA ANTES DE TUDO: `docs/AUDITORIA-PROFUNDA-2026-07-05.md`.**
> **MOTOR ZERO (M0) FECHADO** (`docs/MOTOR-ZERO-M0-FECHAMENTO.md`): T1(C-28), T2, T3, T4 **FEITOS e provados**
> pelo gate (`scripts/fechar-instancia.py` roda `eval-produto`, cobre o PRODUTO, não só a fundação). SEGUEM
> VIVOS: **T8** (vedação só substring) e **G1** (overlay centroide) — ver BACKLOG. A separação **TDC×IPTU**
> foi implementada (domínio como metadado; `--dominio`), a arrumação do Drive tem toolchain provada em
> PLANO (nada movido no Drive ainda — falta o dono rodar os Apps Scripts). A **auditoria 2026-07-05** (7
> lentes) corrigiu falso-verde de gate, doutrina Fi=1,0 stale e a lei-núcleo TDC mistagueada; o **corpus é
> PARCIAL** (19/31 leis; TDC normativo — Decreto 57.536 — AINDA NÃO ingerido). Números do produto: confiáveis
> onde o gate cobre (Fi/PCpt dos cedentes); o resto é PENDENTE declarado. **Não recomeçar o que o gate já prova.**
>
> **★★ HANDOFF 2026-07-03 (Motores 1/2/3 + Escrutínio conjunto + Fase 0 EXECUTADA).** Dossiê completo,
> zero-compressão: **`docs/HANDOFF-2026-07-03-MOTORES-FASE0.md`** — LEIA-O PRIMEIRO. Entregou: `ROADMAP-PU.md`
> + `MOTOR-1/2/3-ESTRATEGIA.md` (cada motor por loop de lentes adversariais; nenhum atingiu triplo limpo —
> resíduo declarado no header) + `docs/ESCRUTINIO-CONJUNTO-MOTORES.md` (48 achados, 5 doenças sistêmicas +
> crítica adversarial) + `docs/INVENTARIO-DRIVE.md`. **Fase 0 FEITA e provada ao vivo no Supabase**
> (`csnalylpvysjvejgsymr`): canonicidade git==banco (7 migrations canônicas + fantasmas receptor arquivados),
> `governanca.de_para` populado (20 fontes, S4), T7 segurança fechado (spend cap + S3 revogadas + RLS deny-all;
> D-SEG-01). **PRÓXIMO LOCAL:** C-28 (T1) → gate de CI (T2/S2) → cadeia de vedação Art.124§2 (T8, âncora
> `montar_base.py` — ver correção adversarial) → conservação 3-estados (T4) → overlay por área (G1). **DONO:**
> 2 verbatim faltam no Drive/repo — Decreto 57.536/16 e Quadro 2A (bloqueiam G2/G4). Escopo: SÓ vendedor/só-tombado.
>
> **★ HANDOFF 2026-07-01 (PU 15 — lente loop de IA · estratégia + ondas locais).** Entregou: (1)
> **`ESTRATEGIA-DE-ENTREGAS-PU.md`** — mapa do processo + roadmap + ondas + separação Classe LOCAL (loop
> destrava sozinho) × Classe EXTERNA (pedido ao MOU). (2) **Executou a Classe LOCAL, tudo provado pelo gate:**
> **B-12** FECHADO (guarda DECIMAL(10,3) do UTXO; R$ OODC monetário não), **B-11c** FECHADO (vigência POR
> CHUNK — o RAG não devolve mais redação revogada como vigente; defeito real do PDE Art. 148 corrigido; eval
> ATIVO novo), **B-7** parte local (verbatim_integral no MANIFESTO + 7.228 datada; 19 verbatim todas datadas),
> **B-10** FEITO (mérito jurídico das 32 juris — laudo `docs/AUDITORIA-MERITO-JURIDICO-B10-2026-07-01.md`;
> lente Gen Advogado + verificação adversarial). (3) Gerou **B-21** (corpus TDC-cego: 0/32, VERIFICADO) e
> **B-22** (dessinc .md/.json). (4) **Pedido único ao MOU** (Classe Externa) em
> `caixa-de-saida/para-escritorio/2026-07-01_potencial-urbano_pedido-unico-classe-externa.md`.
> **Gate VERDE.**
> **★ 2ª onda local (mesma sessão, aprovada):** **eval TDC PROMOVIDO a ATIVO** (destrave P5 — tubo jurídico de
> TDC vira gate rígido; arts. 122/124/129; evals ativos 10→14), **B-11d** (preâmbulo não-citável — B-11 FECHADO
> a/b/c/d), **B-22** (4 notas .md↔.json reconciliadas), **B-3 lado Fs** (`fs_por_categoria` sobre o Quadro 5 real).
> **PRÓXIMO LOCAL (o que resta):** **B-3 Fp** (Quadro 6 — Drive), **B-21** (jurisprudência TDC — captura),
> **B-5/B-6** (camada semântica/remissões — **exigem DECISÃO de doutrina: embeddings vs keyword-puro D-05**; não
> fingir). **PRÓXIMO EXTERNO:** o pedido único ao MOU (dado pesado Drive→Supabase → dono/Atc/preço → Onda 3).


> **★ HANDOFF 2026-06-27 (2 acionamentos — PU 12).** Laudo: `docs/AUDITORIA-PROFUNDA-2026-06-27.md`.
> **Acionamento 1:** pacote de padronização do escritório (caixas v2, REGISTRO/ATA, D128, D119/D120, handoff)
> **consolidado ao `main`** (gate D141) + auditoria 3-lentes + depósito.
> **Acionamento 2 (3 auditorias + PAGUE-TUDO):** PAGOS com gate VERDE — **B-15** (indexei de verdade as 4 leis
> IPTU → **17 leis / 1.571 chunks**; `indexado` virou prova), **B-16** (MANIFESTO honesto), **B-18** (os 2 gates
> concordam), **B-19** (hook não suja/duplica), **B-12(c/d)** (trava FATAL + citação por dispositivo). **Destrave
> de bônus:** indexar a LPUOS 16.402 **ligou TDC no main** (eval `tdc-potencial-construtivo-lpuos` verde, Art. 24).
> Decisões **D-13..D-17** no CODEX §5. **Gate `fechar-instancia.py` = VERDE (exit 0).**
> **ABERTOS (próximos) — ⚠️ atualizado PU 17 (2026-07-03):** **B-17 FECHADO** (produto consolidado no `main`
> pela união `kp9bgr`→main, D141 — não pelo PR; ver rastro do BACKLOG) · **B-11(c) FECHADO** (PU 15). Seguem
> abertos: **B-4/B-9** (Drive — verbatim das 12 municipais + Q14/Quadro 3 na fonte), **B-5/B-6** (camada semântica).
> **Pauta MR-14 (frentes A/B/C/D):** deliberação respondida na caixa-de-saída — **aguarda o MOU consolidar**.
>
> **★ HANDOFF 2026-06-20 (fim da instância de auditoria):** 2 auditorias profundas rodadas. A 1ª
> destravou 12 federais verbatim + engine + ladrão. A **2ª** (`docs/AUDITORIA-PROFUNDA-2-2026-06-20.md`,
> 4 lentes: verbatim·engine·gates·propagação) auditou a superfície nova. Verdict: texto verbatim FIEL,
> matemática do engine CORRETA, mas 3 defeitos sérios — **2 corrigidos na hora** (gate dava FALSO-VERDE →
> piso de evals; engine inventava HMP=0,5 → removido) e o resto em **B-11..B-14** do `BACKLOG.md` com DoD.
> **Comece pelo `BACKLOG.md` (B-11 chunker/citação 1.7 e B-13 endurecer o gate são os mais urgentes).**
>
> **★ BACKLOG + "ladrão" anti-perda (D83, 2026-06-20):** o que falta executar vive em `BACKLOG.md`
> (cada item com DoD = prova mecânica), **surfaçado no boot** (`.claude/hooks/surface-backlog.sh`).
> **Ao fechar, rode `python3 scripts/fechar-instancia.py`** — o GATE mecânico ("declarei feito" ≠
> "provei feito"). Todo trabalho adiado entra no BACKLOG no mesmo instante, ou ele CAI na troca de instância.


> Handoff sem perdas — Escritório do MOU (PMO), 2026-06-20. Estado pós-auditoria triplo-limpo.
> Retome por aqui + `HANDOFF-E-PENDENCIAS.md` + `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md`.
> SSOT do estado de cada item = `MANIFESTO.json` (agora VIVO, gerado por `scripts/consolidar.py`).
> Doutrina: zero-compressão · dialético · agnosticismo · nada se descarta. Não AFINAR sem destravar.

## Estado em 2026-06-20 (verificado, pós-auditoria profunda)
> **⚠️ NOTA PU 17 (2026-07-03): os números DESTE bloco são snapshot de 2026-06-20 (59 itens / 27 leis / 13 indexado / 14 bruto).** Vivo hoje (`MANIFESTO.json`): **63 itens · 31 leis · 19 indexado · 12 municipais bruto**. As 16.050/2014 e 17.844/2022 já saíram de `bruto` (PU 15). Não editei o corpo histórico abaixo — leia-o como registro datado; a verdade viva é o MANIFESTO + o topo ★★★ deste arquivo.
- **Corpus:** 59 itens — 27 leis + 32 jurisprudências verbatim (`tagueado`). 57 no escopo + 2 fora. Das 27 leis: **13 `indexado`** (12 federais re-ingeridas VERBATIM de `_entrada/misto/` + a 7.228/1968 municipal) e **14 `bruto`** (municipais ainda só resumo WebSearch — ver P2). **1.246 dispositivos** em `rag/chunks/`.
- **★ AUDITORIA PROFUNDA (2026-06-20):** laudo dialético em `docs/AUDITORIA-PROFUNDA-2026-06-20.md` (4 lentes adversariais + Supabase vivo). 3 destraves EXECUTADOS (AUD-01 federais verbatim; AUD-04 remoção IRRF/Tema 1130; AUD-03/08/09 engine `engines/tdc/oodc.py`) + ~10 correções de código/corpus. Pendências CRÍTICAS abertas: **AUD-02** (IDs canônicos do Drive trocados — risco de DELETE errado, lane do Drive) e **AUD-03** (tabelas `tabelas/` vazias = combustível do engine).
- **Engine TDC:** `engines/tdc/oodc.py` — Fórmula Mestra (OODC/geração/recepção/travas) agora é CÓDIGO determinístico (1.3), auto-testado no CI. Falta `V`/`CA_max` (tabelas Q14/Quadro 3, ainda no Drive).
- **★ A ESTEIRA RAG EXISTE E FOI PROVADA FIM-A-FIM (2026-06-20).** Antes `rag/` estava a 0%. Agora há tubo determinístico: `scripts/fatiar.py` (chunking por dispositivo 2.5) → `scripts/indexar.py` (índice invertido BM25 + metadados 2.6) → `scripts/consultar.py` (retrieval híbrido com **citação obrigatória 1.7**, gate de cobertura para NÃO-FUNDAMENTADA) → `evals/rodar-evals.py` (gate = citação correta, Parte 3). **6/6 evals ATIVOS passam** sobre a Lei 7.228/1968; 3 evals de TDC ficam como spec `aguardando_verbatim` (ver P5). Sem LLM, sem embeddings, stdlib-only (1.3/1.4). Doc: `scripts/README.md`.
- **MANIFESTO.json:** vivo e idempotente; Action `consolidar.yml` AGORA roda a cadeia inteira (fatiar→indexar→consolidar→**evals como gate**) a cada push, sem loop.
- **Supabase** `potencial-urbano-iptu-tdc` (`csnalylpvysjvejgsymr`, sa-east-1): só `governanca` (de_para, registro_decisoes — vazios) + `public`/PostGIS. Schemas dos artefatos NÃO criados (de propósito, RO-23).
- **Drive:** inventariado; ~16–20 GB de duplicatas mapeadas, executor de exclusão pronto (decisão MOU: EXCLUIR).

## PENDÊNCIAS (prioridade ↓)

> ★ **DESTRAVE-MESTRE — PARCIALMENTE FEITO (2026-06-20, instância orquestradora PU).** A fatia vertical foi construída: o **TUBO** (re-ingestão verbatim → fatiar → indexar → consultar com citação → eval) existe e foi **provado fim-a-fim** sobre a Lei 7.228/1968 (6/6 evals ATIVOS verdes). O que prova: o tubo funciona, é barato (determinístico) e já se sabe ONDE ele quebra (ver "Onde o tubo quebra" abaixo).
> **O QUE FALTA para a fatia ser de PRODUTO (TDC):** a 7.228/1968 é tributária-municipal (IPTU-adjacente), **não TDC** — foi a única lei com verbatim DISPONÍVEL no ambiente (`_entrada/misto/`). O corpus TDC (PDE 16.050/2014 etc.) segue **não-verbatim**, então a guarda-de-verbatim do `fatiar.py` corretamente o recusa. **Bloqueio real e único:** re-ingerir VERBATIM ≥1 norma de TDC. Egress p/ `.gov.br` = HTTP 403 e o Drive é lane exclusiva (cerca) → **esta instância não conseguiu obter verbatim TDC**. Assim que ele chegar, é rodar `fatiar`+`indexar` e os 3 evals `tdc-produto-pendente.json` viram o gate de aceite do produto — zero código novo.
> **Onde o tubo quebra (achados da prova):** (a) TF bruto deixa artigo longo mascarar o relevante → resolvido com **BM25**; (b) match genérico fundamentaria falso-positivo → resolvido com **gate de cobertura** (NÃO-FUNDAMENTADA <34%); (c) **limite declarado do tier keyword**: data-de-vigência por remissão entre artigos (ex.: "a partir de quando vale o art. 3?") exige **grafo de remissões / camada semântica** — extensão futura, vacina gravada em `evals/ground-truth/iptu-7228-1968.json`.
> **Ordem honesta (D26):** P2(verbatim TDC)→(roda o tubo, já pronto)→P5(engines/semântico) é o caminho de PRODUTO. **P1 (Drive), P3 (fora-escopo), P6 (RLS) são HIGIENE — rodam em paralelo, não bloqueiam, não lideram a fila.**

### P1 — Executar a exclusão das duplicatas no Drive (decisão MOU tomada: EXCLUIR)
- Rodar `drive-arrumacao/Sanear-Duplicatas-PotencialUrbano.gs` (Apps Script): `DRY_RUN=true` → conferir Logs → `DRY_RUN=false` → executa (lixeira, recuperável ~30d).
- **O MCP do Drive desta sessão NÃO apaga** — execução é 1 clique no Apps Script da conta do MOU. Mapa+ids: `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md`.
- VACINA: o script só apaga se a cópia canônica existir; Fase 2 só duplicata exata (nome+tamanho). Conferir que SIRGAS_SHP_LOTES (geometrias + `.prj`) ficou com ≥1 cópia.
- Depois: re-rodar o catálogo do Drive e atualizar `docs/INVENTARIO-DRIVE-*.md` (IDs sobreviventes; a árvore foi achatada — os docs de 2026-06-18 descrevem estrutura que não existe mais).

### P2 — Re-ingerir as LEIS em VERBATIM INTEGRAL (lacuna probatória — pré-requisito do RAG)
- **FEITO: 13 leis verbatim/indexadas** — `7228-1968` (municipal) + **12 federais** (re-ingeridas de `_entrada/misto/` via `scripts/promover_entrada.py`, destrave AUD-01). **Faltam 14 MUNICIPAIS** ainda `bruto`/não-verbatim (só resumo WebSearch); a guarda do `fatiar.py` as recusa até virarem verbatim. Para essas, o cru NÃO está local — precisa do Drive (ver abaixo). Use o MESMO `promover_entrada.py` quando o cru chegar a `_entrada/`.
- **Prioridade (D-PU-3 = TDC):** re-ingerir PRIMEIRO o corpus TDC verbatim (PDE 16.050/2014 e correlatas) — é o que destrava a fatia de PRODUTO (os 3 evals `tdc-produto-pendente.json` já esperam por ele). As demais municipais/federais vêm depois.
- Fonte: PDFs no Drive (catálogo `inventario/catalogo-juridico-drive.csv`) — **re-ingestão interna**. **MAS:** neste ambiente o egress p/ `.gov.br` deu 403 E o Drive é **lane exclusiva** (cerca anti-conflito) → para obter verbatim do Drive, **abrir pedido ao Drive** (`escritorio-do-mou/caixa-de-entrada/drive/PEDIDOS-AO-DRIVE.md`) OU rodar de ambiente com egress liberado. **Padrão de re-ingestão já provado:** salvar o cru em `_entrada/`, escrever `leis/<id>.md` com cabeçalho `## Texto integral (verbatim)` + `.json` `confianca:"alta"`, rodar `scripts/fatiar.py`.
- **Gatilho V-2:** ao re-ingerir em lote, avaliar Gemini (contexto grande) p/ enumerar/puxar os links do corpus do Drive de uma vez.
- IDs municipais (3 feitas ✅, **12 a re-ingerir** — atualizado PU 17 2026-07-03): 7228-1968 ✅ · 16050-2014 ✅ · 17844-2022 ✅ · pendentes (12) → 10235-1986, 10365-1987, 11152-1991, 11338-1992, 12350-1997, 13250-2001, 13475-2002, 14865-2008, 15044-2009, 17202-2019, 17577-2021, 17759-2022.

### P3 — Decidir/segregar os 2 itens fora de escopo (decisão MOU)
- `stf-tema-1020` (é ISS, não IPTU) → realocar para corpus ISS ou remover. `stj-resp-1658054` (previdenciário; nº do REsp NÃO verificado) → confirmar o número ou arquivar como ponto cego. Ambos já sinalizados no MANIFESTO; falta a decisão.

### P4 — Base inicial = TDC ✅ (decidido pelo MOU)
- **RESOLVIDO 2026-06-20:** o MOU confirmou **a base inicial é TDC**. O pipeline começa por TDC; o ground-truth e a validação concentram em TDC primeiro; IPTU vem depois (o pipeline replica). Encerra a divergência M-24/M-49. (D-PU-3 = TDC.)

### P5 — Avançar a esteira (trabalho dos Gens)
- [x] **Fatiamento estrutural + índice RAG + consulta com citação — FEITO** (`scripts/fatiar.py`, `indexar.py`, `consultar.py`, `evals/`). Chunking por dispositivo (2.5), retrieval híbrido (2.6), gate 1.7. `consolidar.yml` estendido p/ rodar a cadeia + evals como gate. Doc: `scripts/README.md`.
- [ ] **Replicar o tubo ao corpus TDC** assim que o verbatim chegar (P2): zero código novo — `fatiar`+`indexar`, e os evals `tdc-produto-pendente.json` viram aceite.
- [ ] **Camada semântica (embeddings) + grafo de remissões** — extensão plugável no mesmo índice; destrava perguntas que o keyword puro não resolve (vacina em `evals/ground-truth/iptu-7228-1968.json`).
- [ ] Criar os schemas dos 4 artefatos + geo + rag no Supabase (só após organização aprovada, RO-23) e estender `consolidar.yml` p/ mestres de tese.
- [ ] Engines determinísticos (IPTU progressivo, valuation TDC) — número nasce no engine (1.3).

### P6 — Segurança Supabase (ação física do MOU — não dá pra fazer por SQL)
- Advisory: `public.spatial_ref_sys` com RLS off (tabela de sistema do PostGIS, dado público).
- **CORREÇÃO 2026-06-20 (auditoria):** `ALTER TABLE ... ENABLE RLS` é **BLOQUEADO** — a tabela pertence ao `supabase_admin` e nós (e o SQL Editor do Studio) somos role `postgres` não-superuser. **NÃO é "habilitar RLS com policy".** O **fix real e limpo** (sem superuser): **Dashboard → Project Settings → API → Exposed schemas → remover `public`** (manter `graphql_public`; incluir `governanca` se o app consumir via REST). Todo o dado real do PU vive em `governanca` (RLS deny-all, 0 linhas), então tirar `public` da API fecha a porta sem perder nada. Cross-ref escritório **M-41** (passo a passo). As extensões PostGIS no `public` + `st_estimatedextent` (WARN) ficam intactas de propósito (mexer arrisca o geoprocessamento).

### P7 — Escritório: ratificar o D73 → ✅ FEITO (oficializado como D78)
- O escritório oficializou em produção: o D73 virou **D78** (renumerado por colisão), os hooks foram portados ao template de entrada, e o portfólio do PU foi reconciliado (corpus 59, Supabase próprio, D79 Drive=EXCLUIR, D80 entrada formal proposta). Nada pendente aqui do lado do escritório.

## Vacinas operacionais (recuperadas do chat — auditoria 2026-06-20)
- **V-1 — captura em LOTE que para no 1º item.** A extensão de captura do Drive/jurisprudência parava no primeiro item → capturas incompletas. Ao capturar em lote, CONFERIR que veio tudo, não só o 1º (casa com D24).
- **V-2 — Gemini (contexto grande) para enumerar/puxar os links do corpus inteiro do Drive.** Caminho cogitado e **adiado** — avaliar nesta unidade; não perder a ideia.
- **V-3 — a duplicação do Drive tem CAUSA-RAIZ: upload de máquinas diferentes.** Os ~16–20 GB vieram de uploads repetidos de máquinas distintas. Só excluir (P1/D79) não impede repetir: precisa de **ponto único de upload + dedup no momento do upload**.

## Pontos cegos DECLARADOS (auditoria da CONVERSA, 2026-06-20) — o que NÃO foi auditado
> Honestidade D24: declarar o que ficou de fora vale mais que fingir cobertura.
- **DIMENSÃO DADO/PRODUTO não auditada (a maior).** Todas as auditorias miraram o **corpus jurídico** (artefato Lei/RAG). **Tabela, Fórmula/engine e a base de imóveis ficaram quase intocadas.** O produto real (CODEX Fase 2/3) é cruzar **IPTU 2026 (~1M linhas) × proprietários × ITBI × SQL/endereço**. Os CSVs pesados (`socios`, `IPTU_2026`, `holdings`, série `ITBI`) — os mesmos cujas duplicatas o D79 vai apagar no Drive — **nunca foram auditados/ingeridos/validados**. 3 dos 4 artefatos seguem sem varredura.
- **OCR / legibilidade dos PDFs (gap no P2).** A re-ingestão verbatim das 27 leis assume PDFs de TEXTO. Não verificamos se os PDFs do Drive são texto ou IMAGEM. Se imagem, precisa OCR (RO-13) ANTES de re-ingerir — senão a "re-ingestão" traz lixo de novo.
- **V-2 (Gemini p/ corpus) — agora é TAREFA com gatilho:** ao ir re-ingerir as 27 leis, AVALIAR usar Gemini (contexto grande) para enumerar/puxar os links do corpus do Drive de uma vez. Dono: a instância que rodar o P2.

## Mapa de arquivos-chave (pontos de entrada)
- **Esteira RAG (NOVO 2026-06-20):** `scripts/README.md` (visão) · `scripts/fatiar.py` · `scripts/indexar.py` · `scripts/consultar.py` · `scripts/_texto.py` · `scripts/promover_entrada.py` (promove cru de `_entrada/`→verbatim) · `evals/rodar-evals.py` · `evals/ground-truth/*.json` · artefatos em `rag/chunks/` + `rag/index/`.
- **Engine TDC (NOVO 2026-06-20):** `engines/tdc/oodc.py` (OODC/geração/recepção/travas, determinístico) · `docs/AUDITORIA-PROFUNDA-2026-06-20.md` (laudo).
- `MANIFESTO.json` (estado) · `scripts/consolidar.py` · `.github/workflows/consolidar.yml`
- `docs/AUDITORIA-TRIPLO-LIMPO-2026-06-20.md` (o que mudou e por quê)
- `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md` + `Sanear-Duplicatas-PotencialUrbano.gs`
- `HANDOFF-E-PENDENCIAS.md` · `CODEX-DO-PROJETO.md §ESTADO` · `DO_ESCRITORIO.md` (canal do escritório)
