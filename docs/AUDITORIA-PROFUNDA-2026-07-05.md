# AUDITORIA PROFUNDA E HONESTA — Potencial Urbano — 2026-07-05
> Pedido do dono: *"vamos documentar tudo. rode uma auditoria profunda e honesta, olhe cada cantinho, não deixe passar nada, lance diversas lentes em tudo."*
> Método: **7 lentes adversariais locais** (sem tocar o Drive, sem sub-agentes), cada uma varrendo um flanco e RODANDO os scripts para provar cada achado. Nada de estimativa — toda contagem/afirmação saiu de comando executado.
> Regra das lentes: gastar o texto nos PROBLEMAS, não em elogios. Este documento é o registro auditável; a coluna **status** diz o que já foi corrigido nesta rodada, o que virou backlog e o que exige decisão do dono.

## Veredito honesto em uma frase
O **núcleo determinístico é real e funciona** (CI de 16 gates verde, engine `pcpt.py` fiel à lei e provado em 7 cedentes reais, MANIFESTO idempotente batendo 1:1 com os chunks, zero vazamento do id do modelo) — **mas** há **falso-verde em gates que "provam" o número errado**, **doutrina Fi=1,0 stale viva em 4 fontes**, a **separação TDC×IPTU está oca (0 chunks tdc, a lei-núcleo de TDC mistagueada como iptu)**, **`fonte.hash` nulo em 100% do corpus**, e **o handoff primário desmente a si mesmo**. O projeto é mais honesto internamente (BACKLOG/MANIFESTO) do que na vitrine (README/DISCLAIMER não declaram a lacuna TDC).

---

## 🟥 CRÍTICO (falso-verde, citação errada, perda, overclaim)

| id | achado | evidência | status |
|---|---|---|---|
| **A-01** | `pcpt.py` **hardcoda** os valores de Fi (Art. 24) em Python e **não lê** `tabelas/fi-*.csv` — a doutrina 1.1 ("tabela é input de engine") está invertida; o gate `--demo` testa hardcode contra si mesmo → **drift CSV×engine passa verde**. `oodc.py` faz certo (lê CSV). | `pcpt.py:51-79`; `grep csv pcpt.py`=∅; CSVs têm os mesmos valores | BACKLOG (refactor + gate compara engine×CSV) |
| **A-02** | **Fi=1,0 stale** vivo em 4 fontes que ainda "ensinam" o número ERRADO: `motor00/negative_prompts_v6.1.json:5` (proíbe a regra correta, cita lei errada 17.975/2023); `oodc.py:151-168` (`potencial_gerado_zepec` Fi=1,0 fixo + miscitação); `FORMULAS-CONSOLIDADAS.md:54-66`; docstrings `pcpt.py:8`/`enriquecer_oficial.py:11` dizem "Fi=1". | verbatim `l16402.txt:316-330` (Art.24 escalonado) | **CORRIGIDO** (docstrings + FORMULAS + negative_prompts + oodc alinhados/apontam p/ pcpt) |
| **A-03** | **eval-produto não gateia o número entregue.** Confere só `fi_aplicado`; nunca lê `pcpt_m2`/`saldo_pcpt_m2`/`preco_proxy_brl`. Sabotar `pcpt_m2` no CSV passa VERDE. | `eval-produto.py:98-105`; sabotagem confirmada | **CORRIGIDO** (eval agora assere pcpt_m2 = Atc×CAbás×Fi do próprio CSV) |
| **A-04** | **RE_ARTIGO come o "O" inicial do corpo** (classe ordinal `[ºoO°...]`) → artigo cardinal cujo corpo começa com "O/Os" é fundido no anterior sob rótulo ERRADO. **Art. 54 da 4591/1964 está dentro do chunk do Art. 53** → consulta retorna citação errada (viola 1.7). | `fatiar.py:40`; consulta "sindicatos custos unitários" → cita Art.53 | **CORRIGIDO** (regex não engole mais 'o/O' isolado; re-fatiado/indexado) |
| **A-05** | **Lei 17.844/2022 (TDC — o objeto inicial do projeto) mistagueada `dominio: iptu`** → `--dominio tdc` a EXCLUI silenciosamente, e o veredito segue FUNDAMENTADA (vindo da 16050) sem sinalizar que a lei mais on-point foi filtrada. | `--dominio tdc "potencial construtivo passível de transferência"` some 17844 | **CORRIGIDO** (17844→tdc; 17733 revisada) |
| **A-06** | **Separação TDC×IPTU oca: 0 chunks `tdc` em todo o corpus** (`iptu:868 · compartilhado:996 · tdc:0`). `--dominio tdc` é, na prática, "só compartilhado" — nunca devolve dispositivo TDC-exclusivo. O facet anuncia um valor que não seleciona nada próprio. | `rag/index/metadados.json` | **CORRIGIDO parcial** (17844 + 16050 arts.122-129 → tdc via per-dispositivo; ver F-plan) |
| **A-07** | **Gate de arrumação C5 (prova do hash) vazado pelo literal `"PENDENTE"`** — `MOVE_LINHA id,folder,,,moved` (md5 vazio, Organizer com Drive API off) deixa `hash_md5='PENDENTE'` e **C5 fica VERDE**: move 1.360 sem hash e o gate diz "arrumação provada". | `gate-arrumacao.py:113-115` + `semear:184` | **CORRIGIDO** (C5 trata PENDENTE/'' como ausente) |
| **A-08** | **Nenhum check confronta o índice com o Drive real; C2 anunciado não existe.** Docstring diz "8 checagens"; há 7. `C3` só verifica campos não-vazios, nunca toca o Drive. O dono *pode* chegar a "VERDE — Drive executado" sem um arquivo ter se movido — a "prova" é um `.txt` colável. | `gate-arrumacao.py` (sem `c2_*`); docstring:14 | **CORRIGIDO parcial** (docstring honesta 7 checks + rótulo explícito "prova = log do dono, não confronto com o Drive"; C2-real = backlog) |
| **A-09** | **Organizer NÃO trata multi-pai** — `file.moveTo(dest)` sem `getParents()` arranca um arquivo da `_entrada` de uma pasta boa (perda silenciosa). A correção F3 só entrou no Sanear; o §10 lista F3 "resolvido" mas não alcança a onda que move 1.360 arquivos. | `Organizar-Entrada.gs:1414-1427` | **CORRIGIDO** (Organizer agora emite MULTI_PAI_MANUAL, não move multi-pai) |
| **A-10** | **`fonte.hash` = `null` em 100% (31/31 leis + 32/32 juris)** — o Gate 1 de ingestão ("hash confere") nunca teve como rodar; a proveniência D-DONO-4 não é auditável campo-a-campo. | `grep '"hash": null' leis/**/*.json`=31 | BACKLOG (backfill sha256 na ingestão + ligar o gate) |
| **A-11** | **TDC normativo AUSENTE apesar de "base inicial = TDC"** — Decreto 57.536/2016 (núcleo TDC) não está em `leis/`; as tabelas TDC citam dispositivos cujo texto-fonte não está no RAG (viola 1.7). Gap declarado no BACKLOG **mas não** no README/DISCLAIMER/MANIFESTO → vitrine aparenta base TDC que não existe. | `dominio` leis = 25 iptu + 6 compart + 0 tdc | **CORRIGIDO parcial** (lacuna declarada no README + DISCLAIMER + MANIFESTO alerta; ingestão do 57.536 = backlog) |
| **A-12** | **Handoff primário `PROXIMA-INSTANCIA.md` desatualizado e autodesmentindo** — banner "LEIA ANTES DE TUDO" diz "ZERO fix de produto / Fase 1 não começou / T2-T3 vivos", mas T1–T4 estão FEITOS e o gate roda eval-produto. | `git log` PROXIMA=07-03 vs M0=07-04 | **CORRIGIDO** (banner reescrito p/ pós-M0) |

## 🟦 IMPORTANTE (cobertura parcial, tautologia, buraco de loop)

| id | achado | status |
|---|---|---|
| **B-01** | **Gate de domínio tautológico**: `carimbar_dominio --check` compara o JSON contra o MESMO mapa hardcoded que o escreveu; `eval-dominio I1` (tdc→iptu) é **vácuo** (0 tdc-puro). Prova consistência, não correção. | **CORRIGIDO parcial** (I1 deixa de ser vácuo com chunks tdc reais; fixture independente = backlog) |
| **B-02** | **Fechamento local nunca regenera `rag/chunks`+`rag/index`** — índice adulterado à mão passa localmente; só o CI regenera. | **CORRIGIDO** (check_indice_rag: fatiar+indexar+git diff HEAD -- rag/) |
| **B-03** | **19/31 leis indexadas; Lei 6.989/1966 (lei-mãe do IPTU-SP) ausente** — o RAG responde IPTU citando a 7.228/1968 (que só altera a 6.989); nenhuma saída declara "corpus 19/31". | **CORRIGIDO parcial** (consultar emite cobertura no veredito; ingerir as 12 municipais = backlog) |
| **B-04** | **Gate 1.7 gameável (cobertura sem peso IDF)** — pergunta de 8 termos passa FUNDAMENTADA casando 3 palavras comuns, com todos os termos-tema ausentes. | **CORRIGIDO** (exige o termo de maior IDF da pergunta no top-1) |
| **B-05** | **MOVE_LINHA de id fora do SEED não é classificado** → `destino_path=''` e `hash_md5=''` → C3+C5 VERMELHO eterno; `nativo_ignorado` é estado-fantasma (nenhum script emite). | **CORRIGIDO** (reconciliar classifica upsert de MOVE; Organizer emite status nativo) |
| **B-06** | **reconciler conta `jaLa` como moved, e `jaLa` sai no DRY_RUN** → colar log de ENSAIO vira fase 'execucao'. | **CORRIGIDO** (jaLa só conta se não-dryrun; Organizer marca dryrun no jaLa) |
| **B-07** | **C4 sub-aplica**: só flagra `status=='quarentena'`; OFICIAL em `98`/`99`/triagem escapa. | **CORRIGIDO** (C4 cobre 98/99/quarentena) |
| **B-08** | **Schema 2.4 incompleto**: 0/31 leis completas; 6 federais sem 7 campos; `jurisprudencia_relacionada` vazio em 19/31 (elo lei↔acórdão quase inexiste). | BACKLOG |
| **B-09** | **Vigência (1.6)**: 19/31 com `inicio` datado, 0/31 com `fim`; as 12 sem `inicio` = as 12 `bruto`. Declarado no MANIFESTO/DISCLAIMER (honesto), mas invariante descumprido p/ 39%. | BACKLOG (datar na ingestão das 12) |
| **B-10** | **Sem tag tri-estado D-DONO-4 (OFICIAL/ADQUIRIDO/NOSSO) nos .json** — `fonte.origem` só `web-oficial`/`Drive`; se um dado NOSSO entrar em `leis/`, nada o distingue. | BACKLOG |
| **B-11** | **CI não dispara em PR que só mexe em `jurisprudencia/**` ou `rag/**`** (faltam nos `paths` do `pull_request`). | **CORRIGIDO** (paths do PR alinhados ao push) |

## 🟨 MENOR (higiene, docstrings stale, órfãos)

| id | achado | status |
|---|---|---|
| **C-01** | `quadro7-parques.csv` sem cabeçalho de proveniência; `quadro5-fator-social-fs.csv` com 1ª linha de dados corrompida (legenda concatenada). | **CORRIGIDO** (cabeçalho add; linha limpa) |
| **C-02** | Trava D120/D119 só cobre Edit/Write, não Bash — CLAUDE.md afirma "trava em settings.json" além do que o mecanismo entrega. | **CORRIGIDO** (deny de Bash p/ os 2 repos + texto CLAUDE.md rebaixado ao que a trava garante) |
| **C-03** | `git pushado`/`git limpo` são SOFT no fechamento — dado que "perda de dados" é o modo de falha nº1. | **CORRIGIDO** (promovidos a HARD) |
| **C-04** | Números de doc desatualizados: BACKLOG B-4 "indexado sobe de 13" (→19); ESTRATEGIA "17 leis" (→19); MOTOR-3 "fato confirmado" que envelheceu (consolidar.yml JÁ cobre engines/zepec/tabelas). | **CORRIGIDO** |
| **C-05** | `compilado` usa a data da lei-mãe, não a da redação nova (293 chunks) — `--data` pode devolver redação futura como vigente no passado. | BACKLOG |
| **C-06** | Art. 174 do PDE = 6.888 tokens (absorve Anexos/Quadros no fecho) — anexos irrecuperáveis como dispositivos. | BACKLOG (chunk tipo=anexo) |
| **C-07** | `consultar.py` docstring stale ("municipais só em_vigor, degrada") — na verdade `--data` funciona. `revisado_por_humano`=False em 100% (0/63). `§2` do plano desenha Opção B que ninguém executa; `gate-arrumacao.py:17` comentário ainda diz `hash_sha256`. | **CORRIGIDO** (docstring+comentário; §2 marcado "NÃO-EXECUTADO"; revisão humana = backlog) |
| **C-08** | Ladrão (D83) guarda BACKLOG mas não `PROXIMA-INSTANCIA.md` — lacuna que deixou A-12 passar. Hook referencia `processos/consolidar.sh` inexistente (inócuo, guardado por `[ -f ]`). | **CORRIGIDO** (gate `check_handoff_nao_stale` afere o handoff) |
| **C-09** | **DISCLAIMER/COMO-USAR diziam divergência "~1,27× / ~27%"** mas o eval mede **mediana 1,655× (~66%)** — número ao cliente inconsistente com a prova. (Achado durante a síntese, além das 7 lentes.) | **CORRIGIDO** (DISCLAIMER + COMO-USAR → ≈1,66×, ancorado no eval) |

---

## O que está SÓLIDO (confirmado por execução — não são elogios vazios)
- **CI real:** 16 gates de `consolidar.yml` existem e rodam; gates ANTES do commit dos derivados.
- **1.3 no `oodc.py`/`pcpt.py`:** o engine se recusa a inventar (levanta se faltar insumo); Fi escalonado bate EXATO com o verbatim Art. 24; 7/7 cedentes reais.
- **MANIFESTO:** gerado (não editado), idempotente, `status_pipeline` bate 1:1 com `rag/chunks` (0 mismatch).
- **Divergência PCpt×certidões:** 55 pares, mediana 1,66×, **100% flagada** — surfaçada, nunca escondida.
- **Chunking (o resto):** remissão line-initial 12/13 correta (a fórmula PCpt→Art.125 não vira "Art.124"); `header_raw↔rótulo` 0 divergências; revogado/preâmbulo corretos.
- **Segurança:** **zero vazamento** do id do modelo em arquivos versionados; `deny` precede `allow`.
- **Idempotência da arrumação:** SEED≡MESTRE prova que nada foi movido; reconciliar 2× = idêntico; Sanear aborta sem Drive API; eval-arrumacao restaura o estado.

## Plano de correção — 3 ondas
1. **CORRIGIDO nesta rodada** (ver coluna status): A-02..A-05, A-07, A-09, A-12, B-02, B-04, B-06, B-07, B-11, C-01..C-04, C-07, C-08 + parciais.
2. **BACKLOG (código, sem dono)** — entram no `BACKLOG.md` com DoD mecânica: A-01 (pcpt lê CSV + gate compara), A-10 (backfill fonte.hash), B-08/B-09 (schema+vigência das 12), B-10 (tag D-DONO-4), C-05/C-06 (data de redação; anexo do PDE), fixture de domínio independente (B-01), C2-real do gate de arrumação (A-08).
3. **DECISÃO DO DONO** — A-11 (ingerir Decreto 57.536 + as 12 municipais IPTU e/ou declarar o corpus como parcial na vitrine): é escopo/prioridade, não mecânica.

> **Honestidade final:** esta auditoria achou falso-verde no meu próprio trabalho (o gate de arrumação e a separação de domínio). Documentei tudo e corrigi os 🟥 tratáveis na mesma rodada; o que exige mais trabalho ou sua decisão está listado acima, não varrido para baixo do tapete.
