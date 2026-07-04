# BACKLOG — Potencial Urbano (determinações em aberto)

> **O "ladrão" do escritório aplicado aqui (mecanismo D83, importado em 2026-06-20).** Metáfora do
> MOU: o *ladrão* (extravasor da caixa d'água) captura o que escaparia. O modo de falha nº1 é
> *"uma instância recebe uma determinação, adia para 'a próxima janela', e ela CAI"* — some num
> registro que ninguém relê no boot. Este arquivo é a **fonte única do que falta executar no PU**,
> **surfaçado no boot** (`.claude/hooks/surface-backlog.sh`) e validado no fechamento
> (`python3 scripts/fechar-instancia.py` — GATE mecânico: *"declarei feito" ≠ "provei feito"*).
>
> **REGRA:** todo item adiado entra AQUI no mesmo instante, com uma **DoD (Definition of Done) =
> como PROVAR que foi feito** (mecânica, não "achei que fechei"). Resolvido → move para o rastro com
> a data. Se esta lista estiver desatualizada, o mecanismo falhou — corrigir antes de seguir.
>
> Prioridade: 🟥 produto/valor · 🟦 corpus/RAG · 🟨 higiene/governança · ⬜ qualidade.
> **Estratégia de entregas (lente de loop de IA) que SEQUENCIA estas ABERTAS em ondas:** `ESTRATEGIA-DE-ENTREGAS-PU.md`
> (PU 15, 2026-07-01). Separa **Classe LOCAL** — o loop de IA destrava sozinho, roda já: B-3·B-5·B-6·B-7·B-10·B-11c·B-12 —
> da **Classe EXTERNA** — pedido único ao MOU: B-1·B-2·B-4·B-9·B-17 + dado pesado/geo/FUNDURB/despausar-preço.
> **Substância das ABERTAS INALTERADA** (esta linha só as agrupa por quem destrava).
> **★ ROADMAP-MÃE DO PROJETO (2026-07-03): `ROADMAP-PU.md`** — painel de 7 lentes especialistas (RAG, dados, legal-tech, geo, mercado TDC, produto, cético-governança) + crítica adversarial (10 defeitos, todos corrigidos). Organiza TODAS as ABERTAS em **6 marcos de VALOR (M0–M5)** e passa a ser a fonte de SEQUENCIAMENTO (substitui `ESTRATEGIA-DE-ENTREGAS-PU.md` NESSE papel; a substância das ABERTAS aqui segue INALTERADA). **3 forks do dono ainda em aberto** (posição na cadeia · ordem de expansão · régua de preço) — Seção 2 do roadmap, aguardando decisão.
> **★ ESTRATÉGIAS DE MOTOR + ESCRUTÍNIO CONJUNTO (2026-07-03):** `MOTOR-1-ESTRATEGIA.md` (Travas, 12 travas), `MOTOR-2-ESTRATEGIA.md` (Dados/Infra), `MOTOR-3-ESTRATEGIA.md` (Espacial) — cada um por loop de lentes adversariais (Sonnet+Opus, limites anti-loop); **nenhum atingiu triplo limpo** (resíduo declarado no header de cada). `docs/ESCRUTINIO-CONJUNTO-MOTORES.md` = visão do todo (48 achados) + crítica adversarial; `docs/INVENTARIO-DRIVE.md` = fontes oficiais do Drive por proveniência. **Achado sistêmico nº1 a resolver ANTES do resto (caminho crítico): crise de canonicidade do schema Supabase** — migrations vivas `oficiais.*` sem `.sql` no git; migrations do git nunca aplicadas. **Reconciliação-Drive nº1:** camada AUE/APPa e lotes SIRGAS oficiais existem no Drive (ingerir; trocar `LOTES_*_IA` nosso por oficial).
> **Atualizado: 2026-07-04** (PU 17 — organização/processos em ordem + Fase 1 dos MOTORES em andamento: **T1·T2·T4 FEITOS e provados** (ver tabela FASE 1); prompt dos 2 verbatims do dono entregue. Ver rastro.)
> **Atualizado: 2026-07-03** (PU 16 — ROADMAP-PU.md escrito por painel de 7 especialistas + crítica adversarial; ver linha ★ acima. Sequenciamento das ABERTAS agora em 6 marcos M0–M5. Estratégias por MOTOR + escrutínio conjunto + inventário do Drive escritos — ver linha ★ acima.)
> **Atualizado: 2026-07-02** (PU 15 — LOOP DE MELHORIA multi-lente rodou COMPLETO: 14 lentes, 85 achados, laudo `docs/LOOP-MELHORIA-H1-2026-07-02.md`. **3 correções JÁ APLICADAS e provadas:** (1) **Fi escalonado LPUOS Art.24 I–VII** no engine (era Fi=1 fixo, ERRADO — verificado no verbatim; agregado R$17,5bi→R$8,8bi, Pinel 10×); (2) **saldo líquido** (abate m² já transferido; 55 abatidos, Dona Veridiana→saldo 0 c/ flag REVISAR); (3) **esgotado/vedado des-precificado** (15). Parcelamento Art.124§3º exposto. Ferramenta re-gerada: 2.937 c/ preço do SALDO. CODEX-CALCULOS corrigido. Restante do loop (matriz+top-3) no laudo — priorizar c/ dono.)_

## 🔴 ABERTAS

> **★ PAGOS nesta sessão (2026-06-27, pague-tudo):** B-15 ✅ (indexei de verdade as 4 IPTU → 17 leis/1.571
> chunks; "indexado" virou prova), B-16 ✅ (MANIFESTO honesto), B-18 ✅ (gates concordam), B-19 ✅ (hook não
> suja/duplica), B-12(c/d) ✅ (FATAL + citação por dispositivo) — ver rastro. **Destrave de bônus:** indexar a
> LPUOS 16.402 ligou TDC no main (eval `tdc-potencial-construtivo-lpuos` verde). **ABERTOS:** B-17 (produto
> preso na branch — cross-repo/MOU), B-11(c) (vigência-por-chunk), e os dependentes de Drive (B-1..B-4, B-9).

> **🔧 FASE 1 — CÓDIGO DOS MOTORES (aberto, 2026-07-03; NÃO começou — auditoria profunda `docs/AUDITORIA-PROFUNDA-E-ENCERRAMENTO-2026-07-03.md`).**
> Todos os defeitos abaixo estão **VIVOS no código** (verificado em `arquivo:linha`). **DoD mecânica completa de cada item em `docs/HANDOFF-2026-07-03-MOTORES-FASE0.md` §8** + estratégia em `MOTOR-1/2/3-ESTRATEGIA.md`. Ordem de ataque: **T1 → T2 → T8 → T4 → G1**.
>
> | id | Item (defeito vivo) | DoD (resumo — completa no handoff §8) | Bloqueio |
> |---|---|---|---|
> | ~~**T1/C-28**~~ ✅ | **FEITO (PU 17, 2026-07-03).** `fatiar.py`: guarda de REMISSÃO line-initial (`eh_remissao_line_initial` — conectivo de remissão/vírgula/continuação minúscula, SEM monotonicidade de número) + `header_raw` por chunk. `rodar-evals.py`: comparação de dispositivo endurecida de SUBSTRING→igualdade normalizada (`_norm_disp`; prova adversarial: "Art. 12"≠"Art. 125", "Art. 156"≠"Art. 156-A"). | ✅ **PROVADO:** `133__art-124.json` sumiu; fórmula `PCpt = Atc x CAbas x Fi` agora sob **Art. 125** (`× CAmax ×` sob Art. 127); 0 chunks-remissão restantes; espúrios (16402:114, 17844:108, 126) ausentes; duplo "Art.124" resolvido; novo eval `tdc-formula-pcpt` (conteúdo) verde; 19 leis re-fatiadas; gate VERDE 15/15. | — |
> | ~~**T2/S2**~~ ✅ | **FEITO (PU 17, 2026-07-03).** `consolidar.yml` agora dispara em `engines/**`,`zepec/**`,`tabelas/**`,`supabase/**` (push E pull_request) e roda 2 gates novos: `pcpt.py --demo` + `evals/eval-produto.py`. `eval-produto.py` = golden-assert ANCORADO NA LEI (faixas Art.24 hardcoded no teste, não-circular) sobre **7 cedentes REAIS** (um por faixa I–VII, SQL+área verbatim do CSV oficial), provando engine E produto entregue (`fi_aplicado`). Adicionado ao gate local (`fechar-instancia.py`). | ✅ **PROVADO:** eval-produto 7/7 PASS; **sabotar faixa I 1,2→1,5 no engine ⇒ gate FALHA** (cedente 378 m²: 453,60→567,00, exit 1); restaurado ⇒ verde. CI cobre push+PR nos paths do produto. | — |
> | **T8** 🟥 | Vedação Art.124§2 só substring (`montar_base.py:104`), sem geometria; fail-closed só-preço | usa geometria AUE/APPa do Drive; guard ANTES de atc/cabas zera pcpt/saldo nas vedadas; CONFLITO(4)≠vedado(32) | — |
> | **T3** 🟥 | Escalonado por default ao já-declarado (`enriquecer_oficial.py:81`) | engine exige Fi da certidão ou PENDENTE (Art.24 caput, novas decl.); fixture prova | — |
> | ~~**T4**~~ ✅ | **FEITO (PU 17, 2026-07-04).** `montar_base.py`: classificador `elegibilidade_conservacao()` 3-estados (Art. 129) + `_autoteste_conservacao()` (fixtures: Termo→PENDENTE, RES→SEM_ATESTADO, nunca ELEGÍVEL); campo mal-rotulado corrigido (bp_compres/RES = tombamento → `ato_tombamento`, não `ato_conservacao`); coluna materializada no base. Gate local + CI. | ✅ **PROVADO:** base regenerado = **31 ELEGÍVEL (Atestado) · 111 PENDENTE (Termo) · 7033 SEM_ATESTADO**; 0 linha de tombamento/RES marcada ELEGÍVEL; **sabotar Termo→ELEGÍVEL faz o autoteste FALHAR** (exit 1). Diff cirúrgico (só `ato_conservacao`→`ato_tombamento`). RESTA (M1): propagar `PRÉ-CONDIÇÃO` à ferramenta ao cliente. | — |
> | **T5·T9·T11·T6·T12** ⬜ | disclaimer+27%; parcelamento>50k; saldo por conjunto; arquivar oráculos; endurecer DoDs | ver handoff §8 | — |
> | **G1** 🟦 | Overlay por centroide/1ª feature (`overlay_zona.py:77`) | overlay por ÁREA + `unary_union` + `representative_point`; SIRGAS oficial no lugar do `_IA` | — |
> | **G3** 🟦 | 1.839 "sem SQL" tratados como geocode (1.772 = "Light" coletivo) | geocodificar só os 63 reais contra IPTU_2026 COMPLETO; modelar o bem coletivo | — |
> | **G2** 🟦 | Zona-base sob selo (454); **ZOE usa Quadro 2A**, não Q3 | overlay N:N + FLAG; ZOE só após Quadro 2A | **DONO: Quadro 2A** — prompt de extração pronto: `extracao/PROMPT-EXTRACAO-DECRETO57536-E-QUADRO2A.md` → salvar no Drive `01 — _entrada` |
> | **G4** 🟦 | V por 1 face; Regra da Esquina | RANGE v_min/v_max + flag; MAX só após Decreto 57.536 verbatim | **DONO: Decreto 57.536/16** — prompt de extração pronto: `extracao/PROMPT-EXTRACAO-DECRETO57536-E-QUADRO2A.md` |
> | **G5·G6·E1·E2·E3·E4·E5·E7** ⬜ | materializar overlay em `oficiais.*`; eval geo; runner reproduzível+vintage+dedup+loaders | ver handoff §8 (E6 canonicidade JÁ feito) | — |

| # | Item | DoD (como PROVAR que foi feito) | Bloqueio |
|---|---|---|---|
| **B-2** ⬜ | **[DESCOPADO por D-ESCOPO-01, 2026-07-03 — histórico, não-ativo]** ~~1º JOIN do PRODUTO~~ — `IPTU_2026` (1 distrito) ⋈ LOTES (SQL/geo) ⋈ Q14 (valor) ⋈ zoneamento (CA) → engine → **1ª lista de alvos por imóvel**. | script de cruzamento (`engines/` ou `scripts/`) + saída com ≥N imóveis reais {SQL, valor, oportunidade TDC/IPTU, dono} no git (recorte leve) ou no Supabase `governanca` (bruto pesado fora do git). | DESCOPADO (receptor/alvos/OODC fora do escopo vigente D-ESCOPO-01) — preservado p/ retomada se o escopo reabrir |
| **B-20** 🟥 | **Frente COMERCIAL — lista de cedentes ZEPEC + ferramenta.** Direção MOU 2026-06-28: AGNÓSTICO, sem preço. **MUITO FEITO (sessão PU 14):** 4 planilhas ZEPEC puxadas verbatim → base unificada `zepec/limpo/zepec_unificada.csv` (7.175 linhas, SQL_MESTRE/endereço/datas padronizados) → **ferramenta** `zepec/ferramenta/zepec_cedentes.csv` (6.131 imóveis: estado_venda·certeza·negociável·dono·m²·FUNDURB). **3 codexes** separados (Comercial/Cálculos/Precificação). **Engine cedente** `engines/tdc/pcpt.py` (2 vias, Art.125/127). **Escrutínio por agentes** (várias rodadas triplo-limpo) corrigiu bugs silenciosos (multi-lote, dono OODC, sensor liquidez invertido). | **Aberto:** (a) dono em escala = **Supabase ITBI/IPTU** (pesado, infra/MOU); (b) **Atc do IPTU** destrava o engine de preço (Codex Precificação, PARADO por ora); (c) **resolver SQL dos 1.791 sem cadastro** (geo); (d) **confirmar semântica FUNDURB** (teto/somatória) na fonte SMUL; (e) vias 2-6 de expansão (Quadro 7 parques já extraído: `tabelas/quadro7-parques.csv`, 147 propostos). | local: feito o grosso · Drive/Supabase: dono+Atc em escala (B-9) · fonte SMUL: semântica FUNDURB |
| **B-3** 🟥 | **Fs/Fp no `oodc.py` — ✅ lado Fs FEITO (PU 15, 2026-07-01); Fp bloqueado.** ✅ `fs_por_categoria()` lê o **Quadro 5 REAL** (`tabelas/quadro5-fator-social-fs.csv`) por categoria de uso, citado (Fs nasce da tabela, não do chute — 1.3); LEVANTA em categoria inexistente/ambígua. Auto-teste: HIS=0,0 · Outras Atividades=1,0 · inexistente/ambígua LEVANTA. **NOTA honesta:** 'HMP' NÃO consta neste extrato do Quadro 5. RESTA: **Fp (Quadro 6)** — não está em `tabelas/` (Drive, B-4). | Fs provado no `_autoteste`; Fp aguarda Quadro 6 do Drive. | resíduo Fp = Drive (B-4) |
| **B-4** 🟦 | **Re-ingerir as 14 leis MUNICIPAIS em verbatim integral** (só resumo WebSearch hoje). | cada `.md` com `## Texto integral (verbatim)` + `.json confianca:alta` + fatiada/indexada; rodar `python3 scripts/promover_entrada.py <id>` quando o cru chegar a `_entrada/`. MANIFESTO: `indexado` sobe de 13. | cru NÃO está local — Drive (B-9) |
| **B-5** 🟦 | **Camada semântica (embeddings) + filtro por `tema`** no `consultar.py`. **✅ DESTRAVADO por D-DONO-2 (2026-07-01):** embeddings PERMITIDOS (revisa a doutrina D-05). | consulta "direito de construir" deixa de citar Lei 4.591/1964 Art. 68 (match lexical) — ou recusa, ou cita o dispositivo TDC real; novo eval de "armadilha lexical" como gate. | provedor de embeddings (chave API Voyage/OpenAI **ou** modelo local) — pedir ao dono |
| **B-6** 🟦 | **Grafo de remissões / vigência por remissão** (limite declarado do tier keyword). **Destravado junto com B-5 (D-DONO-2).** | consulta "a partir de quando vale o art. 3?" cita o **Art. 11** (que fixa 1/jan/1969), não o Art. 3; eval do tipo data-por-remissão vira positivo. | mesmo provedor de embeddings do B-5 (o grafo de remissões em si é local) |
| **B-7** 🟦 | **Vigência municipal DATADA (1.6) + `verbatim_integral` — ✅ FEITO na parte LOCAL (PU 15, 2026-07-01).** ✅ `consolidar.py` deriva `verbatim_integral` do marcador do `.md` (19 verbatim) + resumo/alerta no MANIFESTO. ✅ 7.228/1968 datada por Art. 11 (`inicio:1968-12-12`; efeito Art. 3º→1969-01-01, que também alimenta B-6). ✅ **todas as 19 verbatim/indexadas agora têm `vigencia.inicio`** (alerta `indexado_verbatim_sem_vigencia_datada` = vazio). RESTA: datar as **13 municipais `bruto`** — depende do verbatim do Drive (B-4); datar de resumo = inventar. | 19 verbatim datadas (alerta vazio); consolidar populando `verbatim_integral`. Provado no MANIFESTO. | resíduo (13 municipais) = Drive (B-4) |
| **B-21** 🟦 | **Construir jurisprudência de TDC** (achado B-10: corpus é TDC-cego — 0/32 tratam de TDC, VERIFICADO, apesar de TDC ser a base prioritária do MOU). | capturar acórdãos/temas STF/STJ/TJSP sobre outorga onerosa / solo criado / potencial construtivo / TDC → `jurisprudencia/` verbatim + fatiado/indexado; ≥1 eval de tese TDC-jurisprudencial verde. | captura (egress .gov.br=403 / Drive) |
| **B-8** 🟨 | **AUD-02 — conflito de IDs canônicos do Drive ANTES de qualquer DELETE** (risco de perder ~3 GB). | docs antigos (`docs/PLANO-SANEAMENTO-E-DECISOES.md`, `docs/INVENTARIO-DRIVE-*.md`) marcados **SUPERADOS** por `SANEAMENTO-DUPLICATAS-2026-06-20`; antes do `DRY_RUN=false`, cada ID "manter" conferido por `get_file_metadata`. | lane do Drive (NÃO tocar — relayar via B-9) |
| **B-9** 🟨 | **PEDIDO AO DRIVE** consolidando o que depende do Drive: Q14+Quadro 3 (B-1), cru verbatim das 14 municipais (B-4), e o alerta AUD-02 (B-8). | arquivo de pedido depositado no canal do escritório para o MOU relayar à lane do Drive; referência cruzada anotada aqui. | canal: a definir com o MOU (cerca: `caixa-de-entrada/drive/**` é lane do Drive) |
| **B-23** 🟨 | **Deletar 6 branches remotas redundantes** (conteúdo único JÁ RESGATADO ao main — nada se perde; dono autorizou 2026-07-03). **PARCIAL (extensão externa, 2026-07-03): 3/6 DELETADAS** ✅ `escritorio-instance-organization-4zpyoh` · `potencial-urbano-strategy-kp9bgr` · `pu-drive-saneamento-sufixoN`. **RESTAM 3:** (i) `project-audit-roadmap-2thi1g` — 0 arquivos únicos, deletável JÁ; (ii+iii) `pu-14-instances-ey91o2` e `backlog-audit-separation-w1vu4b` — a extensão CORRETAMENTE recusou (safety-check: têm arquivos únicos vs `origin/main` porque o resgate está na branch `jsgvth`, ainda NÃO consolidada ao main). | `git ls-remote --heads origin` mostra só `main` + branch de trabalho. **Ordem correta:** (1) consolidar `jsgvth`→`main` (resgates aterrissam) → (2) então deletar `pu-14` + `backlog-audit` (safety-check passa) + `project-audit-roadmap`. | (i) egress 403 desta sessão → dono na UI/`gh`; (ii+iii) depende de `jsgvth`→`main` primeiro |

## ✅ RESOLVIDAS RECENTES (rastro)
- **2026-07-03 — PU 17 (organização/processos em ordem): consolidação do rastro + reconciliação de escopo.**
  **Movidos de 🔴 ABERTAS → rastro** (estavam presos com ✅/FECHADO, violando a regra "resolvido→rastro"):
  **B-17** (produto consolidado no `main` pela UNIÃO `kp9bgr`→main / D141 — não pelo PR `project-audit-roadmap`;
  `engines/tdc/`, `zepec/**`, `tabelas/q14`+`quadro3` versionados; verificado no boot), **B-1** (tabelas Q14/Quadro 3
  no git — a validação OODC sobre V/CA_max reais que restava está DESCOPADA por D-ESCOPO-01, receptor fora do escopo),
  **B-10·B-11·B-12·B-13·B-14·B-22** (já eram "(resolvido)" com rastro próprio abaixo — só faltava sair da tabela).
  **Reconciliação de escopo:** **B-2** (1º JOIN → lista de alvos/receptor/OODC) marcado **DESCOPADO por D-ESCOPO-01**
  (escopo vigente = SÓ vendedor/cedente, SÓ já-tombado) — preservado como histórico, não descartado. Callout "PAGOS
  2026-06-27" corrigido (não lista mais B-17 como aberto). **Branches redundantes: conteúdo único RESGATADO ao main**
  (auditoria "nada se descarta"): 3 docs 06-29 + tabela Fi + xlsx. A DELEÇÃO física das 6 branches (dono autorizou)
  ficou BLOQUEADA por política de egress (HTTP 403) → **B-23** (ação do dono na UI do GitHub). Gate VERDE.
- **2026-07-01 — PU 15 (lente loop de IA): estratégia + ondas locais de auditabilidade.** `ESTRATEGIA-DE-ENTREGAS-PU.md`
  (mapa do processo + Classe LOCAL × EXTERNA). **PAGOS com gate VERDE:** **B-12** (guarda DECIMAL(10,3) do UTXO;
  R$ OODC monetário livre), **B-11c+d** (vigência por chunk — não devolve revogado como vigente; preâmbulo
  não-citável — 3 evals ATIVOS novos), **B-7** local (`verbatim_integral` no MANIFESTO + 7.228 datada; 19 verbatim
  todas datadas), **B-10** (mérito jurídico das 32 juris — laudo `docs/AUDITORIA-MERITO-JURIDICO-B10-2026-07-01.md`,
  lente Gen Advogado + verificação adversarial), **B-22** (4 notas de confiança .md↔.json reconciliadas).
  **Destrave P5:** `tdc-produto-pendente.json` promovido `aguardando_verbatim → ATIVO` (o tubo jurídico de TDC
  virou gate rígido — 3 itens citando PDE arts. 122/124/129; evals ativos 8→14). Achados novos: **B-21** (corpus
  TDC-cego, verificado), **B-22** (feito). **Pedido único ao MOU** (Classe Externa) em
  `caixa-de-saida/para-escritorio/2026-07-01_potencial-urbano_pedido-unico-classe-externa.md`.
- **2026-06-27 — pague-tudo (3 auditorias: profunda·beta·decisões).** Laudo `docs/AUDITORIA-PROFUNDA-2026-06-27.md`.
  **B-15** (rótulo `indexado` falso): indexei DE VERDADE as 4 leis IPTU (16402/16642/17733/decreto-57443) →
  17 leis / 1.571 chunks; **destrave de bônus:** LPUOS 16.402 ligou TDC no main (eval `tdc-potencial-construtivo-lpuos`
  verde, Art. 24 cobertura 86%). **NV-1:** `consolidar.py` deriva `indexado` do índice + alerta `indexado_sem_chunks`.
  **B-16:** MANIFESTO honesto (63 itens, 31 leis, indexado 17). **B-18:** `gate-fechamento.sh` checa idempotência
  do MANIFESTO (fim do falso-verde F-1; os dois gates concordam). **B-19 (H-1/H-2):** hook deduplica por branch
  em qualquer estado (não suja/duplica). **NV-2:** hook aborta auto-consolidação ao main se MANIFESTO não-idempotente.
  **B-12(c/d):** trava FATAL de gabarito em campo próprio + executada; citação por dispositivo (D-17). Decisões
  **D-13..D-17** lavradas no CODEX §5; §ESTADO e BETA-CONTINUO atualizados.
- **2026-06-20 — 3ª auditoria (FECHAMENTO da sessão).** `docs/AUDITORIA-FECHAMENTO-SESSAO-2026-06-20.md` + 2 verificadores independentes (gate/CI sob teste adversarial = 8 furos F-1..F-8 FECHADOS, sem regressão; completude = PU consistente, gate verde). Lavrados **D-10..D-12** no CODEX (fecha o F6 — decisão sem registro); banner SUPERADO no doc stale que o B-14 perdeu (A-6); **depósito #3** ao escritório corrige o #2 stale. Pendência só do maestro (triar/relayar Drive/atualizar MAPA).
- **2026-06-20 — 2ª auditoria + correções (eu tenho a caneta no projeto).** Laudo `docs/AUDITORIA-PROFUNDA-2-2026-06-20.md`. Corrigidos: gate falso-verde (F-1/F-2, piso de evals ATIVOS); valor inventado HMP=0,5; **B-13 inteiro** (gate/CI endurecido); **B-14 inteiro** (8 docs stale saneados, exceto DO_ESCRITORIO=escritório); **B-11 parcial** (sufixo -A/-B + redação-aspas; 409→280 dups); **B-12 parcial** (decimal BR + guardas de sinal). Resta: B-11(c/d) vigência-por-chunk + B-12 (decimal-total/FATAL/citação-dispositivo).
- **2026-06-20 — Esteira RAG construída e provada fim-a-fim** (`scripts/fatiar+indexar+consultar`, evals, gate 1.7). `rag/` saiu de 0%.
- **2026-06-20 — 13 leis verbatim/indexadas** (12 federais via `promover_entrada.py` + 7.228/1968), 1.246 dispositivos. Destrave AUD-01.
- **2026-06-20 — Engine TDC vira código** (`engines/tdc/oodc.py`, determinístico, 1.3). Destrave AUD-03/08/09.
- **2026-06-20 — Material IRRF/Tema 1130 removido** (cumpre a vacina). Destrave AUD-04.
- **2026-06-20 — Auditoria profunda** (`docs/AUDITORIA-PROFUNDA-2026-06-20.md`, 4 lentes + Supabase vivo) + ~10 correções de código/corpus.

---
> **Ao FECHAR a sessão:** `python3 scripts/fechar-instancia.py` — o GATE mecânico. Sai 0 = verde (pode
> fechar). Sai 1 = pendência → resolva ANTES de declarar "fechado". E atualize a data acima + mova o
> que ficou pronto para o rastro. Estado completo: `PROXIMA-INSTANCIA.md` + `HANDOFF-E-PENDENCIAS.md`.
