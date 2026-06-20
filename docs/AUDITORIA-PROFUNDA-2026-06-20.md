# Auditoria Profunda — Potencial Urbano (RAG Jurídico IPTU/TDC)

> Método: convergência por LENTES adversariais (≈ AUDITORIA-TRIPLO-LIMPO), registro dialético
> (TESE/ANTÍTESE/CONCILIAÇÃO/VACINA), zero-compressão, enumeração total da fonte (D24).
> Data: 2026-06-20. Conduzida pela instância orquestradora do PU. Read-only nas fontes; correções
> aplicadas só onde SEGURO e na própria lane (código desta sessão + corpus + nota de auditoria).
> Esta auditoria NÃO sela verdade: cada conciliação é provisória.

## 0. Cobertura (D24) e como foi feita
Quatro lentes adversariais em paralelo + ground-truth vivo do Supabase + verificação direta:
- **Lente A — Corpus jurídico** (`leis/`, `jurisprudencia/`, `_entrada/misto/`, `MANIFESTO.json`): 59 itens reconciliados item-a-item com o filesystem.
- **Lente B — Esteira RAG/código** (`scripts/`, `rag/`, `evals/`, CI): leitura integral + ~18 consultas adversariais + reconstrução chunk-a-chunk + simulação de loop de CI.
- **Lente C — Dado/Produto** (`engines/`, `tabelas/`, `tese/`, `inventario/`, `extracao/gems/`): a maior lacuna declarada.
- **Lente D — Doutrina/Docs/Governança**: confronto cruzado de todos os docs de topo + `.claude/settings.json`.
- **Supabase vivo** (`csnalylpvysjvejgsymr`): `list_tables` + advisor de segurança (MCP, read-only).

**Pontos cegos declarados:** mérito JURÍDICO das teses (se a tese de cada súmula está correta) não foi auditado — só proveniência/fidelidade/estado. Corpo integral dos 24 `.txt` e dos 30 `.json` municipais foi amostrado, não lido linha-a-linha. Drive e `drive-arrumacao/` intocados (cerca anti-conflito). Os achados de fidelidade do chunker valem sobre N=12 chunks de 1 lei (amostra pequena, mas os achados de gate/tokenização são estruturais).

---

## 1. Veredito de uma linha
A **esteira RAG é real e honesta** (provada fim-a-fim, com defeitos corrigidos nesta passada), mas opera sobre **1 lei de 27**; e o **PRODUTO que dá dinheiro** (lista de alvos por imóvel = "quanto" + "quem") está a **~0%**. A maior alavanca de valor com **custo quase-zero e sem Drive** é promover verbatim que **já está local mas foi declarado inexistente**.

---

## 2. Achados CRÍTICOS

### AUD-01 (CRÍTICO) — O verbatim de 12 leis FEDERAIS já está no repo, mas 3 docs + 12 `.md` afirmam que NÃO existe ("HTTP 403 / não baixado"). *(Lentes A+C+D convergiram)*
- **TESE (o que o projeto crava):** `MANIFESTO.json` `_nota_verbatim`, `docs/AUDITORIA-ACIONABILIDADE-VALOR-USO` (como "CRÍTICA-1") e `CONSOLIDACAO-2026-06-19` dizem *"NENHUMA das 27 leis tem articulado INTEGRAL verbatim (planalto deu 403)"*; cada `leis/federal/*.md` repete *"Texto INTEGRAL não baixado / HTTP 403"*.
- **ANTÍTESE (evidência física):** o articulado INTEGRAL está em `_entrada/misto/*.txt`, capturado "VERBATIM DE TELA" (upload do MOU 2026-06-19): `lei-federal-6015-1973.txt` = 4.601 linhas; `lei-federal-11101-2005.txt` = 2.774; `4591-1964` = 1.273; `ec-132-2023` = 1.361; `10931-2004` = 1.113; e os 12 trazem o cabeçalho de verbatim. O próprio `_entrada/misto/_PROCESSADOS.md` registra: *"para as 12 federais, este é o ÚNICO verbatim local"*. **Duas afirmações internas em contradição direta; a física confirma a do `_PROCESSADOS.md`.**
- **Causa-raiz:** as auditorias anteriores ("triplo-limpo") olharam `.md`/`.json` e **nunca cruzaram com `_entrada/misto/`**. A construção dos `.md` federais jamais consumiu o `.txt` verbatim. O bloqueio "egress 403 / Drive lane" é **falso para as 12 federais** — não precisam de Drive nem de egress.
- **CONCILIAÇÃO (provisória):** o nº honesto de leis SEM verbatim local é **14** (municipais, exceto 7228), não 27. O MANIFESTO superestima a lacuna em ~2×.
- **VACINA:** "confiança ≠ verbatim" foi gravada; faltou a inversa — **um `.md` dizer "não baixado" ≠ o verbatim não estar no repo.** Antes de declarar uma lei não-citável, `grep` por id em `_entrada/`.
- **DESTRAVE (recomendado, NÃO executado nesta passada):** promover os 12 federais de `_entrada/misto/*.txt` → `leis/federal/*.md` com `## Texto integral (verbatim)` + `.json confianca:"alta"` + `fatiar`+`indexar` (idêntico ao que já foi feito com a 7228). Zero captura externa. Move 12 leis de `bruto`→`indexado` e desmente a narrativa "403". **Tensão a decidir pelo MOU:** estas são IPTU/registral; a base inicial decidida é **TDC** — promover já o IPTU disponível (custo ~0) vs. esperar verbatim TDC (bloqueado). Recomendo executar em paralelo.

### AUD-02 (CRÍTICO, lane do Drive — só RECOMENDAÇÃO) — IDs canônicos trocados entre dois planos de saneamento: arquivo "MANTER" por um é "REMOVER" pelo outro, com executor de DELETE em jogo. *(Lente D)*
- **TESE:** `docs/PLANO-SANEAMENTO-E-DECISOES.md` (2026-06-18): `socios.csv` MANTER = `1ncSTA-P2GfV2cPN-...`.
- **ANTÍTESE:** `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md` elege OUTRO canônico (`1gftoKzFaD-...`) e lista `1ncSTA-P2GfV2cPN-...` na coluna **Remover**. Idem IPTU_2026/empresas/holdings (IDs divergem entre os dois docs).
- **CONCILIAÇÃO:** o Drive foi "achatado" e re-uploadado em 18→20/06, então os IDs de 18/06 podem estar mortos e o doc de 20/06 é o provável vigente — MAS o plano antigo segue no repo **sem marca de superado**. Rodar `Sanear-Duplicatas.gs` (DELETE, lixeira ~30d) contra o mapa errado = perda de ~3 GB.
- **VACINA:** dois De/Para concorrentes com IDs trocados num executor de DELETE = exatamente o erro de "redundância sem linhagem".
- **DESTRAVE (para a lane do Drive / MOU — NÃO toquei, cerca):** marcar `PLANO-SANEAMENTO` e `INVENTARIO-DRIVE-*` como SUPERADOS por `SANEAMENTO-DUPLICATAS-2026-06-20`; antes do `DRY_RUN=false`, confirmar por `get_file_metadata` que cada ID "manter" existe e tem o tamanho esperado.

### AUD-03 (CRÍTICO de PRODUTO) — Dos 4 artefatos (1.1), 3 estão a ZERO; o produto-que-dá-dinheiro não existe como dado. *(Lente C)*
- **TESE:** o projeto construiu de verdade só o artefato **Lei/Norma** (RAG). O produto (imóvel × oportunidade × valor × dono) está a 0 byte.
- **ANTÍTESE (placar git):** `tabelas/` = 0 bytes (só `.gitkeep`); `tese/iptu` e `tese/tdc` = vazias; `engines/iptu` = vazia; **0** código de cruzamento; **0/~1M** imóveis do `IPTU_2026.csv` ingeridos; `MANIFESTO.json` = 59 itens, todos leis+juris, **nenhum** imóvel/tabela/engine.

| Artefato (1.1) | Existe de verdade no git | Gap |
|---|---|---|
| LEI/Norma | 27 leis (**1** verbatim/indexada) + 32 juris | 26/27 sem verbatim |
| TABELA/Valor | **0** (só 6 F_i em motor00.json) | ~100% (combustível do engine ausente) |
| FÓRMULA/ENGINE | **0 código**; fórmulas só como prosa `.md`/JSON | spec ~70% pronta, execução 0% |
| TESE | **0** | 100% |
| PRODUTO (lista de alvos) | **0 imóveis, 0 cruzamentos** | 100% |

- **CONCILIAÇÃO:** o RAG jurídico funcionando com 1 lei **não é** "produto andando". O gate do produto (`tdc-produto-pendente.json`) é `aguardando_verbatim` — não dispara alarme no CI; produto a zero é silencioso.
- **VACINA:** não confundir "tubo provado" com "produto entregue".
- **DESTRAVE (recomendado):** decidir o próximo marco. Caminho mais curto ao 1º dinheiro (tudo determinístico, sem LLM): **(a)** ingerir `Atualizacacao_Q14_anoref2025.csv` + `005-QUADRO_3_FINAL.csv` para `tabelas/` → **(b)** transcrever a Fórmula Mestra para `engines/tdc/oodc.py` → **(c)** 1º JOIN real sobre 1 distrito de `IPTU_2026`. Os 4 insumos (fórmula, constantes, chaves de JOIN, schema) **já existem no repo** (ver AUD-08/AUD-09).

### AUD-04 (CRÍTICO de escopo) — `extracao/gems/estrategias-restituicao-tributaria.md` (237 KB) é 100% Tema 1130/IRRF — exatamente a VACINA do projeto, plantada no repo. *(Lente C)*
- **TESE/ANTÍTESE:** o arquivo é integralmente sobre restituição de IRRF municipal (STF Tema 1130, "proposta SBA... Assis-SP", "AUDITORIA PERICIAL DE IRRF... DARF/DIRF/PER-DCOMP") — **zero** IPTU/TDC. A vacina oficial (`tdc-produto-pendente.json`): *"Tema 1130 (IRRF) NÃO é Potencial Urbano — nunca associar."* É o 2º maior arquivo do repo.
- **CONCILIAÇÃO:** hoje fora do `fatiar.py` (que só lê `leis/`), então não vaza para o RAG **ainda** — mas é uma mina à espera de um pipeline que varra `extracao/`.
- **VACINA:** "está num gem, não num lei/" não é segurança.
- **DESTRAVE (recomendado, decisão de move — NÃO executei):** mover para o repo da unidade IRRF/Tema 1130 (outro projeto do portfólio) ou para fora do PU; registrar como cumprimento da vacina.

---

## 3. Achados ALTOS

### AUD-05 (ALTO → **CORRIGIDO nesta passada**) — Gate 1.7 era gameável: pergunta curta fora-de-corpus passava como FUNDAMENTADA. *(Lente B / RAG-01)*
- **ANTÍTESE:** `consultar "direito de construir"` → FUNDAMENTADA (batia só em "direito" de "direito à restituição", cobertura 50% > 34%). Conceito TDC, fora do corpus IPTU.
- **CORREÇÃO aplicada:** gate agora exige 3 travas — cobertura ≥34% **E** score BM25 ≥ piso **E** ≥2 termos casados quando a pergunta tem ≥2 termos de conteúdo. Adicionado eval `neg-curto-direito-construir` (passava errado, hoje recusa). Evals: 7/7 ativos verdes.

### AUD-06 (ALTO → **CORRIGIDO**) — Tokenização quebrava número de lei: `6.989` → `["989"]` ≠ `6989`. *(Lente B / RAG-02)*
- **ANTÍTESE:** o separador de milhar fragmentava o número antes do filtro `len>1`; "Lei nº 6.989" e "6989" viravam tokens distintos (viola 2.6, keyword por nº de lei).
- **CORREÇÃO aplicada:** `_texto.normalizar` cola o separador de milhar (`6.989`→`6989`, `1.500.000`→`1500000`) preservando decimal (`20,00`→`20`,`00`). Verificado.

### AUD-07 (ALTO, parcial) — Vigência dos 15 `.json` municipais viola 1.6: só `em_vigor:true`, sem `inicio/fim`. *(Lente A / A-3)*
- **ANTÍTESE:** os 15 municipais têm `vigencia:{em_vigor:true}` e **zero** datas; os 12 federais têm `inicio`. `em_vigor:true` é asserção sem base datada (ex.: 12.350/1997, revogada pela 17.844/2022 conforme o próprio `.md`).
- **CONCILIAÇÃO:** quebra o filtro temporal obrigatório (2.6). O eixo temporal foi implementado no `consultar.py` (`--data`), mas **degrada** a este metadado pobre.
- **DESTRAVE (recomendado):** na re-ingestão municipal, preencher `vigencia.inicio` (ano está no id/ementa) e `fim/revogada_por` na cadeia que se revoga (12.350/1997 ← 17.844/2022).

### AUD-08 (ALTO) — O conhecimento de ENGINE TDC é REAL e quase-executável, mas hoje é 100% PROSA: "número ainda nasce no LLM" (viola 1.3). *(Lente C / DP-2)*
- **ANTÍTESE:** fórmulas literais existem e concordam entre 3 fontes (`OO = (Área_Adicional/CA_max)×Fp×Fs×V`; geração/recepção de potencial em `semantic_chunks_v6.1.json`); constantes literais em `travas_operacionais_v6.1.json` (F_i por uso, trava FUNDURB 5%, precisão [10,3], 9 blocos condicionais em pseudo-SQL). Mas tudo vive em `.md`/`.json` de conhecimento, **fora de qualquer runtime** — um LLM teria que "ler e calcular" (proibido por 1.3).
- **CONCILIAÇÃO:** o legado entregou ~70% do design de um engine TDC. Falta a transcrição para código determinístico (papel Gen Matemática).
- **DESTRAVE (recomendado):** promover `FORMULAS-CONSOLIDADAS.md` + `travas_operacionais_v6.1.json` a `engines/tdc/oodc.py` (função pura: SQL+ZONA+uso+área → valor de outorga/TDC, com citação da fonte).

### AUD-09 (ALTO) — Engine e Tese são VALOR PRESO: fora do pipeline, fora do MANIFESTO, sem dono (D23). *(Lentes C+D / DP-3, ID-06)*
- **ANTÍTESE:** `consolidar.py` só varre `leis/` e `jurisprudencia/`; `MANIFESTO.json` ignora `engines/`, `tabelas/`, `tese/`, `inventario/`, `extracao/`. A enumeração D24 existe para o **Drive** (`INVENTARIO-*`), não para os artefatos do **git**.
- **DESTRAVE (recomendado):** estender `consolidar.py` (ou um índice irmão) para enumerar TODOS os diretórios do repo com status, fechando o D24 do git; atribuir dono ao engine TDC.

---

## 4. Achados MÉDIOS/BAIXOS

- **AUD-10 (MÉDIO → CORRIGIDO)** — Filtro TEMPORAL ausente apesar de 2.6 ("sempre com filtro temporal") e docstring que anunciava `--vigente` inexistente. *(RAG-03)* → implementado `--data AAAA-MM-DD` (filtra por `vigencia.inicio/fim`; degrada honestamente quando faltam datas) + docstring corrigido.
- **AUD-11 (MÉDIO → CORRIGIDO)** — Lixo de captura `</invoke>` (artefato de tool-call) entrou no verbatim da 7228 e propagou para chunks/índice. *(RAG-04)* → removido da `.md`, índice reconstruído, corpus limpo (grep zero).
- **AUD-12 (BAIXO → CORRIGIDO)** — `fatiar.py` abortava todo o CI com 1 arquivo não-UTF-8. *(RAG-05)* → `try/except` por arquivo (reporta e pula o malformado).
- **AUD-13 (BAIXO → CORRIGIDO)** — Rótulo "Art. 10º/11º" (ordinal incorreto). *(RAG-06)* → ordinal só ≤9 ("Art. 10", "Art. 11").
- **AUD-14 (MÉDIO → CORRIGIDO)** — Título de `stj-resp-1130545.md` ainda dizia "Tema 371" (correção 371→387 ficou pela metade). *(A / M-4)* → título corrigido para Tema 387.
- **AUD-15 (MÉDIO → CORRIGIDO)** — Nota "gen3 é byte-idêntico (mesmo md5)" se auto-falsificou (a nota só foi anexada a um dos pares). *(D / ID-05)* → nota reescrita para falar do CORPO, não do arquivo total.
- **AUD-16 (BAIXO → CORRIGIDO)** — `stj-resp-1658054`: MANIFESTO dizia "nº não verificado", mas a captura já o verificou (previdenciário, REsp 1.658.054/RS). *(A / B-5)* → motivo de fora-de-escopo atualizado no `consolidar.py`.
- **AUD-17 (MÉDIO, recomendado)** — Falta campo `verbatim_integral:true/false` no schema (2.4) e no MANIFESTO; o estado "citável no RAG" não é derivável por máquina (causa-raiz de AUD-01). *(D / ID-07)* → adicionar flag populada por `consolidar.py` detectando o marcador no `.md`.
- **AUD-18 (BAIXO, recomendado)** — Contradição de estado entre docs do mesmo dia: `AUDITORIA-ACIONABILIDADE` diz "`rag/` vazio / 0%", superada no mesmo dia por `PROXIMA-INSTANCIA` ("esteira provada"). *(D / ID-02)* → anexar nota datada "superado" no doc antigo (não apagar — registro histórico).
- **AUD-19 (BAIXO, recomendado)** — Reversão Drive "só mover" (D-2, 18/06) → "EXCLUIR" (D79, 20/06) não está amarrada ao ponto que reverte. *(D / ID-04)* → anotar "D-2 REVOGADA por D79" nos docs antigos (lane do Drive).
- **AUD-20 (REFUTADO)** — Suspeita de que `PROJETO-RAG-JURIDICO-IPTU-TDC.md` (fundação, Partes 5–6) estaria ausente: **falso** — está versionado (18 KB). Agnosticismo confirmou a presença. *(D / ID-08)*

---

## 5. O que está LIMPO (anti-viés do escrutinador — não é só achar defeito)
- **D24/pareamento:** 59/59 itens com par `.md`+`.json`; 0 órfãos; MANIFESTO reconcilia 100% com o filesystem.
- **Fidelidade do chunker:** reconstrução chunk-a-chunk vs `.md` = 100% das linhas, nada perdido/duplicado/reordenado; os "Art. 77/126/128/130" CITADOS dentro do Art. 1º **não** fragmentaram (o regex exige início de linha + aspas protegem). O cenário-pesadelo não se concretizou.
- **Índice ≡ consulta:** tokenização canônica compartilhada; `doclen/avgdl/df` batem; BM25 correto; idempotência (rodar 2× = git limpo); CI não entra em loop.
- **Supabase vivo (verificado):** `governanca.de_para` e `governanca.registro_decisoes` = 0 linhas, RLS on; `public.spatial_ref_sys` = RLS off, 8.500 linhas (tabela de sistema PostGIS) — advisory crítico ativo. **Os docs (CODEX/PROXIMA P6/BETA-CONTINUO) descrevem isso com precisão**, inclusive a correção certa ("remover `public` dos Exposed schemas", não `ENABLE RLS`). Coerente. *(Obs.: há um 2º projeto na org, `gestao-integrada-dados` — não confundir com o do PU.)*
- **Inventário de dados maduro:** `mapa-dados-fase2.md` + `classificacao-planilhas.csv` trazem schema real (flags `tem_SQL/tem_CNPJ/...`) e o grafo de junção (SQL liga IPTU↔ITBI↔OODC; NOME→CNPJ liga imóvel↔sócios). O design de dados do produto está pronto; falta a execução.
- **`.claude/settings.json`:** 4 permissões Google Drive **read-only**, zero segredo, zero hook. Coerente com "Drive não apaga/não move".
- **Doutrina:** vacinas "Tema 1130 IRRF ≠ PU" e "número nasce no engine" preservadas; base=TDC (D-PU-3) registrada sem conflito; registro dialético aplicado de verdade em vários docs.

---

## 6. Destrave priorizado (D26 — o que fazer a seguir)
1. **AUD-01 — promover os 12 federais verbatim de `_entrada/` (custo ~0, sem Drive).** Maior valor imediato; desmente a narrativa "403". *(precisa do aval IPTU-vs-TDC do MOU)*
2. **AUD-02 — travar o conflito de IDs canônicos ANTES de qualquer DELETE no Drive.** Risco de perda de 3 GB. *(lane do Drive)*
3. **AUD-03/08/09 — primeira fatia de PRODUTO TDC:** `tabelas/` (Q14+Quadro 3) → `engines/tdc/oodc.py` → 1º JOIN sobre 1 distrito. Os insumos já existem no repo.
4. **AUD-04 — remover o material IRRF/Tema 1130 do PU** (cumpre a própria vacina).
5. **AUD-07/17 — vigência municipal datada + flag `verbatim_integral`** no schema/MANIFESTO.
6. **AUD-18/19 — marcar docs de estado/Drive superados** (anti-engano da próxima instância).

## 6.1 EXECUTADO pós-laudo (2026-06-20, aprovado pelo MOU) — 3 destraves
- **AUD-01 ✅ FEITO** — `scripts/promover_entrada.py` (novo, determinístico e reutilizável) promoveu os **12 federais** de `_entrada/misto/*.txt` → `leis/federal/*.md` verbatim (`confianca:alta`), saneando lixo de captura ("Stop Claude" na 8009). `fatiar`+`indexar` rodaram: **corpus saltou de 1 → 13 leis indexadas, 1.246 dispositivos**. Consulta federal real funciona (ex.: Lei 6.830 Art. 6º — Certidão de Dívida Ativa, 100% cobertura). MANIFESTO: `indexado:13, bruto:14, tagueado:30`. `_nota_verbatim` corrigida.
  - **Efeito colateral honesto nos evals:** ao crescer o acervo, 2 negativos deixaram de ser "fora-de-corpus" — "ISS" entrou via EC-132/2023 e "direito de construir" casa LEXICALMENTE a Lei 4.591/1964 Art. 68 ("construir habitações", 100% cobertura) sem ser o conceito de TDC. **Vacina nova gravada** (`evals/.../iptu-7228-1968.json`): *match lexical ≠ relevância semântica*; negativos foram escopados por `--lei` e adicionado um negativo absoluto. Reforça a necessidade da camada semântica + filtro por `tema`.
- **AUD-04 ✅ FEITO** — `estrategias-restituicao-tributaria.md` (237 KB, Tema 1130/IRRF, 210 menções IRRF × 1 IPTU) **removido** do PU (`git rm`), com marcador de linhagem `extracao/gems/_REMOVIDO-tema-1130-irrf.md` (recuperável do histórico; pertence à unidade IRRF). Cumpre a vacina "Tema 1130 ≠ PU".
- **AUD-03/08/09 ✅ FEITO** — `engines/tdc/oodc.py` (novo): a Fórmula Mestra virou **CÓDIGO determinístico** (1.3) — OODC `(Aa/CA_max)×Fp×Fs×V`, geração ZEPEC/Doação, recepção, e os `conditional_blocks` (travas HIS/contaminação/CNIB...) executáveis; DECIMAL(10,3); constantes lidas de `travas_operacionais_v6.1.json` (fonte única); cada resultado com memória de cálculo + citação (1.7). Auto-teste no CI. **Dependência declarada:** `V`/`CA_max` são tabela (Q14/Quadro 3) ainda no Drive (AUD-04) → entradas obrigatórias, engine NÃO inventa número. `consolidar.py` agora **enumera os 4 artefatos** no MANIFESTO (`artefatos_nao_corpus`) — fecha o "valor preso" (AUD-09).

## 7. Correções JÁ aplicadas nesta passada (commitadas)
Verbatim limpo (AUD-11) · gate endurecido (AUD-05) · número de lei tokenizado (AUD-06) · filtro temporal `--data` + docstring honesto (AUD-10) · guarda de encoding (AUD-12) · rótulo ordinal (AUD-13) · título Tema 387 (AUD-14) · nota gen3 (AUD-15) · motivo fora-de-escopo (AUD-16) · novo eval adversarial curto. Pipeline + 7/7 evals ativos verdes; corpus sem stray tags.
