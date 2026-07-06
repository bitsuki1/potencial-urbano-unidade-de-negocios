# ROADMAP — Potencial Urbano (inteligência de TDC, lado cedente)
> Documento-mãe do projeto. Substitui a visão fragmentada (ESTRATEGIA-DE-ENTREGAS-PU.md + backlog espalhado como fonte de sequenciamento).
> Escrito pelo Escritor do Roadmap em 2026-07-03, a partir do ESTADO CONSOLIDADO 2026-07-03 e dos pareceres de **7 especialistas** (íntegros no Apêndice), e **revisado por uma crítica adversarial** que apontou 10 defeitos — todos corrigidos nesta redação (7º parecer restaurado, dissenso do medallion declarado, colisão de nomenclatura M#×área resolvida, dependência M2↔M3 desfeita, dossiê receptor incluído, piso de auditabilidade destacado).
> Marcos de VALOR, não de técnica. Doutrina inviolável do CLAUDE.md manda: número nasce no engine (1.3), citação obrigatória (1.7), só fonte oficial/adquirida (D-DONO-4), pendência declarada, gate mecânico a cada entrega.
> **Honestidade total:** onde os especialistas divergem, o dissenso está DECLARADO no corpo. Nada aqui foi suavizado para agradar.

---

> ## ★★★★★ CORREÇÃO ESTRUTURAL — 2026-07-06 (LER ANTES DE TUDO)
> Fontes: `docs/DECISOES-2026-07-05.md` §2026-07-06 (D-DONO-14/15/16) + `docs/ESCRUTINIO-TAXONOMIA-MOTORES-2026-07-06.md` (loop adversarial, 20 achados sobreviventes).
>
> **1) Taxonomia canônica (D-DONO-14):** **1 chão + 1 selo + 4 motores de valor**, os quatro em **CORRENTE** (não caixas paralelas):
> - **Chão:** **a Esteira de Dados** — banco + pipeline (o número in-scope roda na esteira CSV, git-reconstruível; NÃO toca o Postgres — a reconciliação do banco é off-path e não gateia valor). *(Não se chama "motor".)*
> - **Selo (em volta):** **Honestidade** — citação + rótulo + **vigência** + teste. Não é motor (só confere).
> - **Corrente de valor:** **{Motor da Lei + Motor do Mapa}** → **Motor das Fórmulas** (preço legal) → **Motor Comercial**. **Lei e Mapa correm em PARALELO; só as Fórmulas dependem dos dois.**
> - **Natureza (escrutínio):** os 4 são **lentes de valor sobre um pipeline compartilhado** (`zepec/`+`engines/`), não 4 módulos particionados — há **dívida de costura** declarada (a corrente não flui 1:1 no código; ver laudo). Motor da Lei e Motor do Mapa estão **parcialmente as-built** (RAG não cabeado; Mapa sem eval/fora do selo).
>
> **2) ESCOPO — cliente = VENDEDOR; comprador FORA (D-DONO-15):** *"comprador não nos interessa aqui, apenas vendedores."* **SUPERA** a tese central da Seção 1 abaixo (fosso = match de dois lados; incorporador receptor como cliente) e o **Marco M2 (demanda/matching)**: `receptores.csv`-como-fosso, score de liquidez, re-rank por chance de venda, dossiê do receptor → **fora de escopo**. O **Motor Comercial (D-DONO-16)** é 100% lado-vendedor (originação, qualificação, "achar o dono", dossiê) — o pipeline `zepec/` existente. **Não** faz match com comprador.
>
> *O corpo abaixo é registro histórico (nada se apaga); onde apostava na demanda, vale esta correção.*

## 1. Visão e tese do produto

O Potencial Urbano vende **inteligência acionável de Transferência do Direito de Construir (TDC) em São Paulo, lado cedente** — imóveis tombados/ZEPEC que podem vender potencial construtivo. O ativo defensável **não é a lista de 6.131 cedentes** (a ZEPEC é pública e oficial — commodity), nem o agregado de R$ 8,83 bi (proxy regulatório, ficção de liquidez que o comprador desconta na primeira conversa). O ativo é o **pipeline auditável fator→dispositivo→eval** — cada número derivado de lei indexada, citado e reproduzível — casado com o **lado escasso do mercado: a DEMANDA**. O fato dominante dos próprios dados reordena tudo: o mercado absorve ~54k m²/ano contra ~5,0M m² de oferta (≈92 anos de estoque teórico) e o teto pecuniário do FUNDURB (~R$ 7,8 mi/ano) torna fisicamente impossível monetizar os bilhões exibidos. Logo, o produto-fim não é um catálogo de oferta nem um SaaS de consulta — é o **MATCH**: saber qual cedente tem comprador plausível agora, com o dossiê citável que fecha a transferência. Cliente imediato: a gestora com contrato (OPIT-SP/Bairro Vivo); cliente-alvo de maior urgência e disposição a pagar: o **incorporador receptor** que precisa de crédito para viabilizar um empreendimento específico.

---

## 2. Os 3 forks estratégicos — DECISÃO DO DONO pendente

> Os três forks continuam **NÃO decididos pelo dono**. Abaixo, a recomendação consolidada dos especialistas com os dissensos na cara. O roadmap (Seção 4) foi desenhado para ser **robusto aos três** o máximo possível — mas cada fork tem um ponto de bifurcação real marcado nos marcos.

### Fork (a) — Posição na cadeia: vender inteligência/dados × corretagem/gestão × principal (comprar crédito)
> **⛔ SUPERADO EM PARTE por D-DONO-15 (2026-07-06):** cliente = VENDEDOR; comprador fora de escopo. Cai a via "principal/comprar crédito" e a dependência de demanda. Registro histórico abaixo.

**Recomendação consolidada (maioria):** **Corretagem/gestão como negócio, inteligência como arma (habilitador de originação + matching), principal só back-to-back.** O contrato OPIT-SP/Bairro Vivo já confirma que a operação É gestão comercial. Vender "dados" sobre uma lista pública com agregado fictício tem moat fraco; o moat real é a camada de matching de dois lados. Ser principal neste mercado é warehousing de capital morto (92 anos de estoque, banco recusa TDC como colateral, haircut de iliquidez 30–45%, teto FUNDURB) — só faz sentido com crédito específico e receptor já assinado.

**Dissensos declarados:**
- **Arquiteto RAG** puxa para **inteligência + corretagem**, condicionada a resolver antes a divergência de 27% contra as 167 certidões (comprar/precificar com engine descalibrado é assumir o próprio erro). Sinal fraco a favor: os 92 anos dizem que o gargalo é demanda, não originação.
- **Legal-tech** adverte: corretagem já expõe a unidade a **dever de informação qualificado** sobre saleability — aí os gates de conservação (Art. 129) e vigência deixam de ser "nice to have" e viram dever. Inteligência/dados é a posição de MENOR risco jurídico, **desde que** com disclaimer de decision-support.
- **Geoespacial** é fork-agnóstico: a espinha lote→zona serve corretagem e principal igual — construa independente da escolha.

**Ponto de bifurcação no roadmap:** só depois de **M2 (demanda/matching)** e da calibração do engine (M0) é que "principal back-to-back" fica sequer avaliável.

### Fork (b) — Ordem de expansão: aprofundar via 1 (ZEPEC) × abrir vias 2–6 (ZEPAM/ZEIS/parques/corredores)

**Recomendação consolidada (forte, quase unânime):** **Aprofundar a via 1. NÃO abrir vias 2–6 agora.** Razões convergentes de quatro lentes:
- **Mercado/Produto:** vias 2–6 geram oferta via doação (~8x potencial, Fi até 2,0). Adicionar oferta a um mercado de 92 anos de estoque é **destruição de valor** — o gargalo é demanda.
- **Legal-tech:** a via 1 (Art. 24/125) está verbatim-verificada; as vias 2–6 dependem do lado receptor e das restrições binárias (OUC/ZER/ZEPAM/APM/PIU) que estão inteiras por verificar. Abrir frente nova multiplica superfície de risco antes de fechar a prova da atual.
- **Arquiteto RAG:** as lacunas de corpus bloqueiam a via 1 E as demais; fechada a via 1, as outras reutilizam quase de graça.

**Dissenso construtivo (Geoespacial + Plataforma de dados):** o fork é **falso se a plataforma for feita certa**. Materializar o overlay lote→zona da cidade inteira em PostGIS custa quase o mesmo que refazer só o dos cedentes; depois disso cada via 2–6 é um `WHERE zona=X`. Não escolham "aprofundar vs abrir" — construam a **espinha espacial uma vez**, fechem a via 1, e as vias 2–6 ficam latentes a custo ~zero (não operacionalizar como oferta, mas ter a query pronta). **Exceção admitida:** arbitragem parque-doação demanda-dirigida (doar gleba periférica valorada no teto → vender em Eixo), só com comprador identificado.

**Ponto de bifurcação no roadmap:** **M3** entrega a espinha espacial que torna as vias 2–6 um `WHERE`. A decisão de OPERACIONALIZAR alguma via 2–6 fica congelada até haver sinal de demanda para ela (saída de M2).

### Fork (c) — Régua de preço: proxy regulatório × equivalente-outorga ÷4 × benchmark de mercado

**Recomendação consolidada (maioria):** **Nenhum dos três isolado — pilha obrigatória de 3 números, sempre juntos:** (1) teto regulatório (PCpt×V, **rotulado teto teórico**, com a trava FUNDURB 5% citando Art. 24 §5 LPUOS); (2) âncora regulatória citável (equivalente-outorga ÷4, Art. 128 §1º); (3) **banda de mercado empírica** — os comparáveis FUNDURB (12–25% de V) + os 166 pares de conversão reais (mediana recebida/cedida 1,247). O número que vai ao dono/comprador é a **banda de mercado**, ancorada pelo ÷4 e limitada pelo teto. Proxy ou ÷4 sozinho manda um número 4–8x alto demais e detona credibilidade na primeira auditoria.

**Dissenso declarado (crítico — Legal-tech):** **NÃO publicar NENHUM R$** (nem proxy, nem ÷4) ao cliente **até o Art. 128 estar verbatim-verificado** — a constante 4 (CAmaxcd) e a fórmula C são asserções do doc mestre marcadas como conflito interno, não dispositivos lidos. Entre as três âncoras, a única defensável hoje é o **benchmark das certidões reais** (fato observado, não interpretação), e mesmo esse como **faixa, não ponto**. Convergência prática com a maioria: a banda de mercado é sempre exibida; a diferença é que o Legal-tech **trava o ÷4 e o proxy até M0 fechar** a leitura do Art. 128 — o que o roadmap adota como gate de M0.

**Convergência de todos:** exibir a divergência de 27% na cara (nunca esconder); o PCpt do engine é confiável **só para prospecção nova** (SO_ELEGIVEL); onde a SMUL já declarou, o **m² oficial vence a estimativa** (não "ajustar" o engine para bater 1,27 — é ruído de CAbás na data de protocolo).

---

## 3. Arquitetura — veredito após a crítica do cético

A proposta na mesa era **ETAPAS (Bronze/Silver/Gold) × MOTORES M0–M6**, com "verdade executável por motor + codex fino por motor + visão humana gerada". A **Lente 7 (ceticismo de arquitetura/governança)** foi a voz cética primária — reforçada pela Plataforma de dados (Lente 2) e pelo Arquiteto RAG (Lente 1) na parte de cerimônia. Veredito: **adotar o mínimo que resolve os modos de falha reais, rejeitar a cerimônia.**

> **Dissenso arquitetural DECLARADO (medallion):** a Lente 2 (Plataforma) defende o medallion enxuto (Bronze/Silver/Gold já existe implicitamente, formalizar custa 1 página); a **Lente 7 (cético, rec C-R3) rejeita TAMBÉM o medallion**, ficando só com `fatores-tdc.csv` gateado — o argumento é que `ESTRUTURA_SILVER` e os oráculos M0/M2/M3 JÁ existiram neste repo e viraram cemitério, e o `travas_v6.1.json` canonizou o Fi=1 errado. **Escolha adotada: medallion enxuto, mas só como convenção de PATH + vintage (uma página, zero maquinário novo), e a "verdade executável" mora no `fatores-tdc.csv` gateado (a rec do cético), não no medallion.** Ou seja: a formalização física que o cético teme (21 células de codex, oráculos "inabaláveis") NÃO é adotada; o que sobra do medallion é só a disciplina de vintage nos paths — barata e alinhada ao princípio 1.6. O dissenso fica registrado; a decisão é do dono se quiser ir ainda mais enxuto (rec C-R4, abaixo, em M0).

**ADOTADO (barato, resolve falha real, metade já existe implicitamente):**

1. **Medallion enxuto, formalizado em 1 página** (`ARQUITETURA-DADOS.md`):
   - **BRONZE** = Storage imutável, path com *vintage* obrigatório (`oficiais/iptu/ano=2026/...`) + manifesto sha256. **Nunca sobrescreve.**
   - **SILVER** = Postgres tipado (`dados.*`, `geo.*`, `tabelas.*`) com colunas de vintage/data_base obrigatórias.
   - **GOLD** = views + CSVs versionados no git (`zepec/ferramenta`).
   - Resolve: o princípio 1.6 (toda norma tem vigência) já é doutrina para LEIS — falta aplicá-lo a DADOS. IPTU_2027 vira "1 linha no manifesto + rodar loader", zero código novo.

2. **A ponte mecânica M1↔M4 — a tabela de 47 fatores como CSV versionado** (`tabelas/fatores-tdc.csv`), colunas `{fator, valor, lado, dispositivo, chunk_id, eval_id, status_verificacao}`. CI falha se `status='verificado'` e o `eval_id` não está verde OU o `chunk_id` não existe. **Esta é a "verdade executável" real** — sem ela os 47 fatores viram um segundo doc-mestre (mapa, não fonte).

3. **Gates de dados no CI (o dbt 80/20 — sem dbt):** `consolidar.yml` cobre `zepec/**`, `engines/**`, `tabelas/**`; re-executa o enriquecimento e falha em byte-diff; asserts de contagem do funil; eval ground-truth de cedente. **Não adotar dbt** com 1 operador + <20 modelos + instâncias efêmeras — atrito de boot que não paga. Reavaliar só acima de ~30 modelos SQL.

**REJEITADO (cerimônia que consome sessões e diverge em silêncio):**

- **"Codex fino POR MOTOR"** (7 codexes append-only, um por M0–M6). Num shop de 1 dono, cada codex é mais um arquivo que toda instância lê no boot e pode divergir — o repo já sofreu disso (COMO-USAR negando o preço, PROVENIENCIA com contagem errada). **Um CODEX de dados único + a tabela de 47 fatores basta.** A matriz ETAPAS×MOTORES fica como **taxonomia de documentação**, não como 21 células com processo próprio. Verdade executável é UMA por artefato e mora na **camada física** (índice/CSV/engine/shapefile), não no codex.
- Não construir maquinário de codex-por-motor **antes** da tabela de 47 fatores existir. A regra do cético: resistir a criar 7 estruturas novas de uma vez.
- **Org-chart de Gens como cerimônia (cético rec C-R6) — decisão registrada:** os 6 papéis (Gen Técnico-RAG, RAG, Estudo, Matemática, Advogado, Orquestrador) com handoffs formais são, na prática, subagentes com um prompt. Adotar: **a lente adversarial triplo-limpo é OBRIGATÓRIA só em entrega que altera número/engine do produto** (`engines/**` ou os CSV de produto); dispensável em edição de doc. Registrar como entrada datada no CODEX (editar a Parte 4 do CLAUDE.md fica fora de escopo deste roadmap — é decisão do dono).

**Modos de falha que a arquitetura mínima precisa fechar (verificados no repo):**
- Pipeline "resgatado" não roda de checkout limpo (`overlay_zona.py` aponta `/tmp` de sessão morta) → **runner parametrizado**.
- Gate verde ignora `zepec/` → regressão no produto passa (C-09) → **gates de dados no CI**.
- Espelho `oficiais.*` diverge em silêncio do git (C-27) → **UMA política de canonicidade: banco reconstruível do git**.
- Chunk da fórmula central rotulado com dispositivo errado (C-28) e nenhum eval pega (o eval confere o rótulo, que mente) → **corrigir chunker + eval sobre conteúdo**.

---

## 4. O roadmap em MARCOS

> 6 marcos sequenciados. Cada um entrega algo **vendável/usável**. Esforço relativo em unidades comparáveis (P/M/G). DoD é mecânica (um comando ou um gate decide). Dependências explícitas.

### M0 — Piso de credibilidade: nenhum número sai sem citação e enquadramento
**O que fica vendável/usável:** a ferramenta pode ser mostrada a um comprador sofisticado **sem detonar credibilidade na primeira auditoria**. Todo R$ exibido carrega dispositivo citado, banda de mercado e disclaimer. O erro material mais caro (citar a fórmula central com dispositivo errado) some.

**Entregas principais:**
- **Corrigir o chunker C-28 (fórmula PCpt hoje citada como "Art. 124")** — regex + monotonicidade de nº de artigo; re-fatiar/re-indexar 16.050 e 16.402; eval sobre CONTEÚDO (`dispositivo_topo='Art. 125'` ∧ `texto_contém='PCpt = Atc × CAbas × Fi'`). *[Arquiteto RAG R1 — discorda do "depois" do loop]*
- **Indexar Art. 128 e Art. 117 do PDE verbatim; verificar OU declarar pendente a constante 4 (CAmaxcd) e a grafia da fórmula C.** Nenhum campo de R$ sai enquanto não citado. *[Legal-tech L1]*
- **DISCLAIMER.md + cabeçalho injetado em todo CSV/Excel/dossiê** (decision-support, não parecer/laudo; proxy ≠ mercado; valor venal ≠ valor de outorga; data-base Q14 jan/2025). *[Legal-tech L5]*
- **Gate de conservação (Art. 24 §1º + Art. 129) como binário de elegibilidade** — separar `ato_tombamento` de `atestado_conservacao_art129`; cedente sem atestado não entra em "pronto para abordar", vira estado `PRE-CONDICAO`. *[Legal-tech L2]*
- **Surfaçar a divergência de 27% (eval `pcpt-vs-certidoes`, 55 pares)** + coluna `qualidade_estimativa='INCONSISTENTE_COM_OFICIAL'`; PCpt rotulado "confiável só p/ prospecção nova". *[Legal-tech L4 / Mercado MKT-3]*
- **Gate de segurança ANTES da Fase B** (spend cap religado; bucket PII segregado privado; RLS deny-all provado; fim de chave hardcoded). Pré-condição mecânica, não bloqueia M0 mas trava M5. *[Plataforma PD-7]*
- **Colapsar as fontes-de-verdade em ≤3 papéis e ARQUIVAR o cemitério ANTES de criar os arquivos novos** — declarar 3 papéis (git=estado · MANIFESTO.json=status do pipeline · BACKLOG.md=trabalho aberto); `git rm` de `engines/tdc/oraculos/` (os oráculos "INABALAVEL"/M0-M6 que canonizaram o Fi=1 errado) e dos docs datados write-once/read-never, recuperáveis pelo histórico; um parágrafo no CODEX define onde cada tipo de fato vive. "Nada se descarta" = "nada se APAGA do histórico git", não "tudo fica no working tree". **Isto vem ANTES das novas fontes (`fatores-tdc.csv`, `receptores.csv`, `funil.csv`…) — senão o roadmap agrava a proliferação que ele mesmo diagnostica.** *[Cético C-R4 — defeito nº3 da crítica]*

**Dependências:** nenhuma externa. Tudo local + índice vivo.
**Esforço:** **M** (baixo por item, vários itens).
**DoD mecânica:** chunk `132-art-125` tem len>1000 contendo a fórmula (eval verde); `grep 'Art. 128'` em `rag/index/chunks.json` > 0; `art128.py --demo` cita §1º OU changelog registra "constante 4 PENDENTE — não emitir R$"; `DISCLAIMER.md` no repo e grep confirma o bloco em cada saída; coluna `elegibilidade_conservacao` com 3 estados citando Art. 24 §1º/Art. 129; eval `pcpt-vs-certidoes.json` roda no gate; `curl` anônimo ao path PII retorna 403; `ls engines/tdc/oraculos/` = vazio (arquivado, recuperável por `git log`) e o working tree tem ≤3 docs de estado ativos.

---

### M1 — Ferramenta religada: o MVP comercial honesto
**O que fica vendável/usável:** o corretor abre um artefato que **reflete tudo que o motor já calculou** (preço 3-stack, saldo líquido, zona, pendência) e leva um **dossiê acionável por imóvel** à conversa. A "porta de entrada" deixa de parecer mais pobre que o engine.

**Entregas principais:**
- **Religar `lista_prospeccao.py` ao `zepec_cedentes_oficial.csv`** (propaga pcpt/saldo/valor_equivalente/zona/pendência); reescrever `COMO-USAR.md` (parar de NEGAR o preço). *[Produto P1]*
- **Preço em pilha de 3 números por linha** (teto PCpt×V rotulado / equivalente-outorga ÷4 Art. 128 / banda de mercado 12–25% de V); implementar `art128.py` calibrado contra os 166 pares (mediana 1,247). Nenhum número isolado. *[Mercado MKT-4 / Produto P4]* — **sujeito ao gate de M0: se Art. 128 sair PENDENTE, exibe só a banda de mercado como faixa (posição Legal-tech).**
- **Dossiê por imóvel (`gerar_dossie.py`)** — 1 página/SQL: identificação, memória de cálculo citada (chunk_ids), à-vista vs parcelado (Art. 124 §3º), checklist Art. 129. Piloto nos 19 INTACTO-com-dono. *[Produto P2 / Legal-tech L6]*
- **Funil como headline, não contagem** (`funil.csv` versionado): 6.131 elegíveis → 4.292 c/ SQL → 2.937 c/ preço → 599 prontos → 19 acionáveis-com-dono; aba RESUMO do Excel. *[Produto P5]*
- **Excel do dono via `make produto`** (abas RESUMO/PROSPECCAO/PENDENCIAS/DICIONARIO). *[Produto P1]*
- **Gates de dados no CI** cobrindo `zepec/` + `pcpt.py` + eval ground-truth de cedente (5–10 conferidos à mão); byte-diff do enriquecimento. *[Plataforma PD-5]*

**Dependências:** M0 (números religados só valem citados/enquadrados).
**Esforço:** **M**.
**DoD mecânica:** `lista_prospeccao.csv` regenerado com ≥1.800 linhas com valor; `grep 'não está aqui' zepec/ferramenta/COMO-USAR.md` = 0; `make produto` roda do zero e gera `.xlsx` datado; `gerar_dossie.py` produz 19 arquivos com dispositivo citado por número; commit de sabotagem (mudar 1 Fi) FALHA o CI; `funil.csv` versionado e na aba RESUMO.

---

### M2 — Lado da demanda / matching: o diferenciador
> **⛔ SUPERADO por D-DONO-15 (2026-07-06):** comprador FORA de escopo. `receptores.csv`-como-fosso, score de liquidez, re-rank por chance de venda, dossiê do receptor e reenquadrar-por-demanda saem. O que RESTA migra para o **Motor Comercial (lado-vendedor, D-DONO-16):** qualificação (apto+saldo), "achar o dono", fila e dossiê. Registro histórico abaixo.
**O que fica vendável/usável:** o produto responde **"este crédito vende?"** e não só "este imóvel pode ceder?". A lista deixa de ser censo e vira **priorização por chance real de fechamento**. É o moat de dois lados e o caminho para vender ao incorporador receptor. **Item mais citado por todas as lentes de mercado/produto.**

**Entregas principais:**
- **`receptores.csv` das 167 certidões** (SQ, lote, endereço, distrito, m² recebida real, ano, cedente de origem) — dado 100% oficial DEUSO, hoje intacto e não usado. *[Mercado MKT-1 / Produto P3]*
- **Score de liquidez por distrito** (absorção histórica m²/ano; concentração em Jd. Paulista, V. Mariana, Moema, Itaim, Pinheiros) → coluna `score_liquidez_distrito` na prospecção. *[Mercado MKT-1]*
- **Re-ranquear a prospecção por chance de venda** (liquidez_distrito × proximidade a Eixo/Arco × estado INTACTO/TEM_SALDO × atestado Art. 129 em mãos). *[Mercado MKT-5]*
- **Reenquadrar o headline:** de "carteira R$ 8,83 bi" para **absorção anual / anos-de-estoque por distrito**, com teto FUNDURB (~R$ 7,8 mi/ano) ao lado. *[Mercado MKT-2]*
- **Dossiê inverso (lado receptor) — a monetização concreta do "virar para o receptor" (defeito nº9 da crítica):** dado um lote/empreendimento receptor, `gerar_dossie_receptor.py` retorna os créditos cedentes casáveis (por distrito/proximidade/estado) + o preço em pilha-3 + o que a lei permite receber ali. A Seção 1 nomeia o incorporador receptor como o cliente de maior disposição a pagar; **sem este artefato o roadmap prega o receptor e entrega só ferramenta de cedente.** Piloto: 1 empreendimento receptor real das 167 certidões. *[Estrategista P3 estendido / Mercado MKT-1 lado demanda]*
- **`art128.py` calibrado contra os 166 pares** como eval (mediana 1,247). *[Mercado MKT-4]*
- **Merge do Produto B (receptor/OODC) — condicionado** à verificação verbatim da fórmula C (M0/L1) E a uma camada de restrição binária de recepção (OUC/ZER/ZEPAM/APM/PIU/estoque distrital Q15-16). Sem ela, `oodc.py` calcula outorga onde a lei VEDA. *[Legal-tech L8 — gate do B-17/D-DONO-3]*

**Dependências (M2 é DIVIDIDO em duas trilhas — defeito nº7 da crítica):**
- **M2-core (o diferenciador, NÃO depende de M3):** `receptores.csv`, score de liquidez, re-rank, reenquadramento do headline, `art128.py` calibrado. Depende só de M0 (calibração/citação) + M1 (produto religado). O `receptores.csv` não precisa de PostGIS.
- **M2-merge (o Produto B/OODC, GATED em M3):** o merge só entra quando a **camada de vedação espacial (GEO-5, em M3)** existir — sem ela `oodc.py` calcularia outorga onde a lei VEDA. Este item é explicitamente **gated em GEO-5**, não paralelo a ele.
**Esforço:** **M** (core) **/ G** (merge, gated).
**DoD mecânica (core):** `zepec/oficial/receptores.csv` commitado com nº de linhas = nº de operações (167), 146 receptores distintos; `lista_prospeccao` com `score_liquidez_distrito` preenchido e ordenação reproduzível por script; aba RESUMO exibe série de absorção ~54k→25k m²/ano; `art128-vs-certidoes` reporta mediana 1,247.
**DoD mecânica (merge, só após GEO-5):** `oodc.py` retorna `RECEPCAO_VEDADA` citando dispositivo antes de calcular (eval por tipo vedado, alimentado por `COBERTURA-RECEPTORA.md`) — pré-condição do merge do B-17.
**Bifurcação do Fork (a):** a saída de M2 (existe demanda casável? em quantos distritos?) é o que torna "principal back-to-back" avaliável.

---

### M3 — Espinha espacial: cobertura e vias latentes
> **Natureza do marco (defeito nº5 da crítica):** M3 é uma **trilha HABILITADORA**, não um marco de valor puro. O valor real ao cliente é o **ganho de COBERTURA** (49%→70%+ = mais linhas vendáveis) — e esse ganho **conta como entrega quando entra no produto via M1/M2**, não isolado aqui. A parte de infra-pura (dedup rclone 40,6%, parametrizar paths, canonicidade banco-do-git) tem DoD 100% técnico e **serve ao gate de reprodutibilidade de M0**, não ao cliente. O "overlay que ninguém no mercado tem" é ativo defensável **potencial**, não valor realizado até casar com demanda.

**O que fica vendável/usável:** a cobertura de cálculo salta de ~49% para ~70%+ (entra no produto por M1/M2), o overlay vira reprodutível (fim do "reconstruir a sessão"), e **as vias 2–6 viram um `WHERE zona=X`** (latentes, custo ~zero — a decisão de operacionalizar fica com o dono/demanda).

**Entregas principais:**
- **Overlay por ÁREA (max interseção lote×zona), não centroide** — corrige 113 zonas erradas (88 com CAbás diferente = erro de VALOR) e expõe multi-zona hoje silencioso; `representative_point()` como fallback. *[Geo GEO-1]*
- **Resolver zona-base sob o selo ZEPEC/ZOE (overlay N:N) — os 454** (355 APC + 77 ZOE + 9 APP + 8 AUE + 5 BIR); confirmar juridicamente se o CAbás da zona-base se aplica a APC/APP (senão, FLAG, nunca fabricar). *[Geo GEO-2]*
- **Geocodificar endereço→SQL dos 1.839 sem SQL** (30% da base — maior buraco isolado): fuzzy `endereco_mestre` × strings do IPTU_2026 (pg_trgm), fallback espacial SIRGAS. *[Geo GEO-3]*
- **Regra da Esquina: V = MAX entre todas as faces do lote** (Art. 3º IV Decreto 57.536/16) — hoje o join por 1 face subavalia 15% dos lotes de esquina. *[Geo GEO-6]*
- **PostGIS: materializar `geo.lote_zona` da cidade inteira** (migration + loader idempotente, GIST). **Conflito de viabilidade resolvido (defeito nº8 da crítica):** GEO-1 exige precisão de área (corrige 88 erros de VALOR de CAbás), mas os ~3,9M lotes podem estourar 8GB e a saída fácil (`ST_Simplify`) degrada justamente essa precisão. Regra: **a tolerância do `ST_SimplifyPreserveTopology` é amarrada ao eval `geo-overlay.json`** — qualquer simplificação escolhida para caber em 8GB TEM de continuar passando o eval na tolerância adotada; se não passar, não simplifica (particiona por distrito ou sobe o tier). Overlay vira JOIN <2s; vias 2–6 viram `WHERE`. *[Geo GEO-4 / Plataforma PD-3]*
- **IPTU_2026 e Q14 completos como tabelas Postgres com vintage** (mata re-stream de 894MB; view `q14_max_face`). *[Plataforma PD-2]*
- **Eval da camada espacial (`geo-overlay.json`, 30–50 cedentes conferidos no GeoSampa)** — a camada espacial é a ÚNICA sem eval (viola 1.7). *[Geo GEO-7]*
- **Auditoria de cobertura RECEPTORA (`COBERTURA-RECEPTORA.md`)** — mapear cada restrição de recepção contra os shapefiles já subidos; a lista do que FALTA é pequena e enumerável (OUC, PIU, PMRR R3/R4, APRM, Quadro 6 Fp). *[Geo GEO-5]* — alimenta a camada de vedação de M2.
- **Fechar o resgate do pipeline** (parametrizar paths, canal único rclone, dedup 40,6% do bucket, política de canonicidade banco-reconstruível). *[Plataforma PD-1 / PD-4]*

**Dependências:** M0 (banco canônico/gates). Roda em paralelo a M1/M2 na parte de infra, mas os ganhos de cobertura entram no produto depois de M1.
**Esforço:** **G**.
**DoD mecânica:** `grep -rn 'tmp/claude' zepec/pipeline/` = 0 e `refazer_oficial.sh` reproduz as contagens de regressão em checkout limpo; `geo.lote_zona` cobre os ~3,9M lotes e re-gerar `zona_por_cedente.csv` recupera ≥400 dos 454 sem CAbás e ≥250 dos 293 sem zona; contagem de PCpt sobe de 3.014 para ≥3.400; `geo-overlay.json` no CI morde ao injetar zona errada; `q14_max_face` consumida pelo enriquecimento; query de duplicatas no bucket = 0; `db reset + migrations + loaders` reconstrói o banco com contagens batendo.
**Bifurcação do Fork (b):** M3 dissolve o trade-off — as vias 2–6 ficam prontas como `WHERE`, operacionalizadas só sob demanda (saída de M2), nunca como expansão de oferta.

---

### M4 — Corpus TDC completo + auditabilidade fim-a-fim
> **Piso de auditabilidade NÃO refém da lane externa (defeito nº10 da crítica):** a defensibilidade central não pode ficar pendurada em M4, cujo corpus verbatim + jurisprudência estão bloqueados fora do controle do dono (MOU/Drive + egress .gov.br 403). **O piso mínimo já é entregue por M0+M1 sozinhos** — ponte dos 47 fatores (`fatores-tdc.csv` gateado) + chunk C-28 corrigido + citação por dispositivo do que JÁ está indexado. Com esse piso a venda tem base auditável mesmo sem M4. O corpus externo de M4 é **enhancement** (aprofunda a defensibilidade), **não é gate** da tese de valor.

**O que fica vendável/usável:** **cada linha da lista e cada um dos 47 fatores fica contestável-e-defensável em cartório/negociação** — o RAG cobre as leis que o engine efetivamente usa, e a jurisprudência dá munição TDC ao Gen Advogado (hoje 0/32). É o que **aprofunda** os forks (a) e (c) numa negociação real (o piso já vem de M0+M1).

**Entregas principais:**
- **Corpus TDC-crítico verbatim: os 5–6 diplomas que o engine cita e o RAG não tem** — Decreto 57.536/2016 (Regra da Esquina, rito, DPC 5 anos), Decreto 58.289/2018, Lei 17.975/2023, Lei 18.081/2024 (+10% CA fora dos eixos, exclusivo TDC), Lei 17.577/2021, Lei 18.222/2024. Prioridade ACIMA das 13 municipais genéricas. *[Arquiteto RAG R2 / Legal-tech L7]*
- **Grafo de remissões (B-6) DESACOPLADO de embeddings** — regex puro, 100% local, sobre os 19 verbatim (`Redação dada por`, `Revogado por`, `Regulamentado por`, `art. N desta lei`) → `rag/grafo/remissoes.csv`; `consultar.py` exibe `alterado_por`/`regulamentado_por`. *[Arquiteto RAG R4]*
- **Vigência por redação datada para o cohort já-declarado** (Art. 25 reescrito por 18.081/2024) — o engine não pode aplicar o Fi escalonado por default a quem declarou sob outro regime; exigir Fi da certidão. *[Legal-tech L3]*
- **Endurecer vigência-por-chunk** (só 2/1.877 revogados num corpus com PDE compilado é sub-detecção): marcar §§/incisos revogados dentro de artigo vigente; nos 293 `compilado`, não rankear pela redação superada. *[Arquiteto RAG R5]*
- **Tabela de 47 fatores como `fatores-tdc.csv` versionado** (a ponte M1↔M4 da Seção 3) + CI que falha se `verificado` sem eval verde/chunk existente. *[Arquiteto RAG R8]*
- **Escalar o eval suite: nenhuma lei "indexada" sem ≥2 evals próprios** (`MIN_ITENS` = função do corpus, ≥2×leis). *[Arquiteto RAG R6]*
- **Jurisprudência TDC (B-21)** — lista de captura nominal para o MOU (egress .gov.br = 403): Temas STF/STJ sobre outorga onerosa/solo criado/limitação administrativa de tombamento, apelações TJSP (Lei 16.050 arts. 122–133); ≥8 acórdãos verbatim + ≥2 evals de tese. *[Arquiteto RAG R7 / Legal-tech L7]*
- **Camada semântica (opcional, D-DONO-2) — só como expansão de RECALL, gate 1.7 continua lexical**: degrau barato primeiro (stemmer PT + filtro `tema` que já existe, 454 chunks TDC); se não bastar, Voyage via API com vetores persistidos no git + fusão RRF. Embedding **nunca fundamenta sozinho**. *[Arquiteto RAG R3]*

**Dependências:** captura dos verbatim depende do MOU/Drive (lane externa B-9) e egress .gov.br (externo). O grafo de remissões e a tabela de 47 fatores são 100% locais e podem começar antes.
**Esforço:** **G** (bloqueado em parte por lane externa).
**DoD mecânica:** MANIFESTO lista os 5–6 diplomas como `indexado` com ≥1 eval por diploma citando o dispositivo de carga; `rag/grafo/remissoes.csv` commitado com ≥1 aresta por lei com marcador (eval `data-por-remissao` verde); `fatores-tdc.csv` com as 47 linhas e CI que quebra ao sabotar; `rodar-evals.py` falha se lei indexada tem <2 evals (ativos ≥38); ≥8 acórdãos TDC verbatim indexados + ≥2 evals verdes.

---

### M5 — Dono em escala: de 19 para centenas de acionáveis
**O que fica vendável/usável:** o gargalo do produto vendável não é cálculo, é **identificação do proprietário** (hoje só 19 dos 599 prontos têm dono conhecido). M5 move isso para centenas — o corretor passa a ter a quem abordar em escala.

**Entregas principais:**
- **Fase B (dados adquiridos, D-DONO-6 oficiais primeiro):** `socios.csv` 3,4GB + `empresas.csv` 2,3GB + holdings + iptu-2020, subidos DEPOIS do gate de segurança de M0. *[Produto P6]*
- **Resolver dono da maioria dos 599 prontos** (join socios/empresas/holdings). *[Produto P6]*
- **Consolidar geocodificação (degrau 0)** de M3 na base — os 1.839 recuperados entram no funil.
- **Decisões estratégicas registradas** (referência para o dono decidir os forks): posição na cadeia (MKT-6), no-go das vias 2–6 como oferta (MKT-7) — **como entradas datadas no CODEX, não como fato consumado; a decisão é do dono.**

**Dependências:** M0 (gate de segurança PII — pré-condição MECÂNICA); M2 (score de liquidez para priorizar quais 599 resolver primeiro); M3 (geocodificação).
**Esforço:** **M** (o peso é externo: carga de 5,7+ GB, passo do MOU em escala).
**DoD mecânica:** `SELECT count(*) FROM dados.socios` bate o esperado com RLS deny-all provado; dono resolvido para ≥X% dos 599 (baseline honesto medido, não prometido); funil atualizado com os 1.839 geocodificados; carga da Fase B só autorizada no BACKLOG com o DoD de segurança (PD-7) verde.

---

### Sequenciamento e paralelismo

```
M0 (piso credibilidade) ──┬──> M1 (ferramenta religada) ──> M2 (demanda/matching) ──┐
                          │                                                          ├──> M5 (dono em escala)
                          └──> M3 (espinha espacial) ─────────────────────────────────┘
                                    │
M4 (corpus TDC) ── parte local começa junto de M0; parte verbatim/juris depende do MOU ── alimenta M1/M2 continuamente
```
- **M0 é gate de tudo** (credibilidade + segurança).
- **M1 e M3 rodam em paralelo** após M0 (produto vs infra).
- **M2 é o diferenciador** — não atrasar por M3; o `receptores.csv` não precisa de PostGIS.
- **M4** tem trilha local (grafo, tabela de fatores) que começa cedo e trilha externa (verbatim/juris) que corre no tempo do MOU.
- **M5** fecha o loop de identificação, gated por segurança (M0) e priorizado por M2.

---

## 5. Riscos e apostas (top 5)

| # | Risco / Aposta | Probabilidade × Impacto | Mitigação |
|---|---|---|---|
| **1** | **O mercado é ilíquido (92 anos de estoque) — a oferta que catalogamos não vende.** É a aposta central: se a demanda não for mapeável/casável, o produto de cedente vale pouco. | Alta prob. de ser verdade × Impacto existencial | **M2 primeiro-classe:** provar com `receptores.csv` que há demanda casável em ≥5 distritos; re-ranquear por liquidez; virar para o receptor (lado com dinheiro/urgência). Se M2 mostrar demanda nula, o Fork (a) fecha em "inteligência/dados para a gestora", não corretagem em escala. |
| **2** | **Publicar R$ derivado de número não-lido (constante 4, fórmula C) detona credibilidade na 1ª auditoria.** Divergência de 27% vs certidões reais já é sinal. | Média × Alto (credibilidade = o produto) | **Gate de M0 (L1):** nenhum R$ sai sem Art. 128 verbatim; pilha de 3 números sempre junta; divergência de 27% na cara; PCpt só para prospecção nova; **dissenso Legal-tech honrado** (banda de mercado como faixa se Art. 128 sair pendente). |
| **3** | **Risco jurídico de saleability:** vender "você tem R$X a transferir" a quem não pode transferir sem conservação (Art. 129) ou sob regime revogado (Art. 25/18.081) = afirmação materialmente incorreta; o cliente age e falha. | Média × Alto (responsabilização) | **Gate de conservação binário (M0/L2)** + vigência por redação datada (M4/L3) + DISCLAIMER de decision-support (M0/L5) + checklist de due diligence por imóvel (L6). |
| **4** | **Infra não reprodutível / dados sem vintage:** pipeline aponta `/tmp` de sessão morta, espelho diverge do git, re-stream de 894MB por pergunta. Quando IPTU_2027 chegar, reescrever tudo. | Alta × Médio (velocidade e confiança) | **M3 + arquitetura mínima:** medallion com vintage, banco reconstruível do git, canal único rclone, gates de dados no CI. |
| **5** | **Vazamento de PII (socios.csv 3,4GB de CPF) por bucket público** — histórico recente de bucket geo servido por URL aberta e chave hardcoded. Mata o produto comercial independente de compliance. | Baixa-média × Catastrófico (reputacional) | **Gate de segurança mecânico ANTES da Fase B (M0/PD-7):** bucket PII privado, RLS deny-all provado, spend cap, revogação de chave ao fim da carga. Carga só autorizada com DoD verde. |

**Aposta de fundo declarada:** o roadmap aposta que **o valor está no matching (demanda) + auditabilidade (pipeline citável)**, não na completude do catálogo de oferta. Se o dono decidir o Fork (a) como "principal/comprar crédito", boa parte de M2/M4 vira pré-condição de balanço (calibração + jurisprudência + gate de conservação) antes de qualquer compra — e o roadmap não muda de ordem, só de finalidade.

---

## 6. Backlog consolidado por motor/área

> Fundido dos 7 pareceres, deduplicado. Esforço: P (baixo) / M (médio) / G (alto). Lente de origem citada. IDs originais entre colchetes para rastreabilidade.
> **Nota de nomenclatura (defeito nº6 da crítica):** as ÁREAS abaixo usam prefixo **A-** (A-RAG, A-REL, A-GEO, A-CALC, A-MKT, A-GATE, A-INFRA). "M#" nesta tabela significa **exclusivamente MARCO** (Seção 4). A taxonomia de MOTORES M0-M6 foi REJEITADA (Seção 3) — não é reintroduzida aqui.

### A-RAG — Jurídico / RAG (corpus, chunking, evals, remissões)
| Item | Marco | Esforço | Lente [id] |
|---|---|---|---|
| Corrigir chunker C-28 (fórmula PCpt rotulada "Art. 124") + eval sobre conteúdo | M0 | P | Arquiteto RAG [R1] |
| Indexar Art. 128/117 verbatim; verificar constante 4 e fórmula C | M0 | M | Legal-tech [L1] |
| Corpus TDC-crítico: 57.536, 58.289, 17.975, 18.081, 17.577, 18.222 verbatim | M4 | M | Arquiteto RAG [R2] / Legal [L7] |
| Grafo de remissões (regex local, desacoplado de embeddings) | M4 | P | Arquiteto RAG [R4] |
| Vigência por redação datada — cohort já-declarado (Art. 25/18.081) | M4 | M | Legal-tech [L3] |
| Endurecer vigência-por-chunk (§§/incisos revogados; compilado não rankeia velho) | M4 | M | Arquiteto RAG [R5] |
| Tabela de 47 fatores como `fatores-tdc.csv` + CI (ponte M1↔M4) | M4 | M | Arquiteto RAG [R8] |
| Política mecânica: ≥2 evals por lei indexada; MIN = f(corpus) | M4 | M | Arquiteto RAG [R6] |
| Jurisprudência TDC (B-21) — lista de captura + ≥8 acórdãos + evals | M4 | G (lane externa) | Arquiteto RAG [R7] / Legal [L7] |
| Camada semântica recall-only (stemmer+tema primeiro; Voyage+RRF depois) | M4 | M | Arquiteto RAG [R3] |

### A-REL — Relacional (proprietário, sócios, holdings)
| Item | Marco | Esforço | Lente [id] |
|---|---|---|---|
| Fase B: socios/empresas/holdings/iptu-2020 (após gate de segurança) | M5 | M (peso externo) | Produto [P6] |
| Resolver dono da maioria dos 599 prontos | M5 | M | Produto [P6] |

### A-GEO — Espacial (overlay, PostGIS, cobertura, geocode)
| Item | Marco | Esforço | Lente [id] |
|---|---|---|---|
| Overlay por ÁREA (não centroide) + flag multi-zona | M3 | M | Geo [GEO-1] |
| Zona-base sob selo ZEPEC/ZOE (overlay N:N) — os 454 | M3 | M | Geo [GEO-2] |
| Geocodificar endereço→SQL dos 1.839 sem SQL | M3 | G | Geo [GEO-3] |
| Regra da Esquina: V = MAX entre faces do lote | M3 | M | Geo [GEO-6] |
| PostGIS: `geo.lote_zona` cidade inteira materializada | M3 | G | Geo [GEO-4] / Plataforma [PD-3] |
| IPTU_2026 + Q14 completos como tabelas Postgres com vintage | M3 | M | Plataforma [PD-2] |
| Eval da camada espacial vs GeoSampa (`geo-overlay.json`) | M3 | P | Geo [GEO-7] |
| Auditoria de cobertura RECEPTORA (`COBERTURA-RECEPTORA.md`) + Quadro 6 Fp | M3→M2 | P | Geo [GEO-5] |

### A-CALC — Cálculo (engines, fatores, calibração)
| Item | Marco | Esforço | Lente [id] |
|---|---|---|---|
| Implementar `art128.py` (equivalente-outorga ÷4) citando §1º | M1 | M | Legal [L1] / Mercado [MKT-4] |
| Calibrar art128 contra 166 pares (mediana 1,247) como eval | M2 | M | Mercado [MKT-4] |
| Eval `pcpt-vs-certidoes` (55 pares) + `qualidade_estimativa` | M0 | M | Legal [L4] / Mercado [MKT-3] |
| Merge Produto B (oodc) gated por fórmula C + camada de vedação binária | M2 | G | Legal [L8] |

### A-MKT — Mercado / Comercial (demanda, matching, preço, produto)
| Item | Marco | Esforço | Lente [id] |
|---|---|---|---|
| `receptores.csv` das 167 certidões (146 receptores) | M2 | M | Mercado [MKT-1] / Produto [P3] |
| Score de liquidez por distrito | M2 | M | Mercado [MKT-1] |
| Re-ranquear prospecção por chance de venda (matching) | M2 | M | Mercado [MKT-5] |
| Reenquadrar headline: absorção/anos-de-estoque, não R$ bi | M2 | P | Mercado [MKT-2] / Produto [P5] |
| Religar `lista_prospeccao` ao oficial; reescrever COMO-USAR | M1 | P | Produto [P1] |
| Preço em pilha de 3 números por linha | M1 | M | Mercado [MKT-4] / Produto [P4] |
| Dossiê por imóvel (`gerar_dossie.py`) — piloto nos 19 | M1 | M | Produto [P2] / Legal [L6] |
| Funil como headline (`funil.csv` + aba RESUMO) | M1 | P | Produto [P5] |
| Excel do dono via `make produto` | M1 | P | Produto [P1] |
| Decisão registrada: corretagem primeiro, principal back-to-back | M5 | P | Mercado [MKT-6] |
| Decisão registrada: no-go vias 2–6 como oferta (latente) | M5 | P | Mercado [MKT-7] |

### A-GATE — Travas / Gates (segurança, disclaimer, conservação, canonicidade)
| Item | Marco | Esforço | Lente [id] |
|---|---|---|---|
| DISCLAIMER.md + cabeçalho em toda saída | M0 | P | Legal [L5] |
| Gate de conservação binário (Art. 24 §1º + Art. 129) | M0 | P | Legal [L2] |
| Checklist de due diligence por imóvel (GDA, DPC 5 anos, CADIN…) | M1 | M | Legal [L6] |
| Gate de segurança pré-Fase B (PII privado, RLS, spend cap) | M0 | P | Plataforma [PD-7] |

### A-INFRA — Infra transversal + governança (plataforma, canonicidade, gate)
| Item | Marco | Esforço | Lente [id] |
|---|---|---|---|
| Colapsar fontes-de-verdade em ≤3 + `git rm` oráculos/docs datados (arquivar cemitério) | M0 | P | Cético [C-R4] |
| Estender o gate ao produto (`pcpt.py`/`art128.py`/eval cedente no `fechar-instancia.py`) | M1 | M | Cético [C-R1] / Plataforma [PD-5] |
| `make produto` reproduzível (mata a FOTO e o drift; contagens de regressão como assert) | M1 | M | Cético [C-R2] / Plataforma [PD-1] |
| Fechar resgate do pipeline (paths parametrizados, rclone único, dedup) — **gate de reprodutibilidade de M0** | M0/M3 | P | Plataforma [PD-1] |
| Política de canonicidade: banco reconstruível do git (migrations) | M3 | P | Plataforma [PD-4] |
| Gates de dados no CI (byte-diff, contagem de funil, eval cedente) | M1 | P | Plataforma [PD-5] |
| Formalizar medallion enxuto (`ARQUITETURA-DADOS.md`, 1 pág) — **só vintage nos paths; dissenso Lente 7 declarado** | M3 | P | Plataforma [PD-6] × Cético [C-R3] |
| Visão humana GERADA da verdade executável (dossiê/README por script, nunca à mão) + 1 log de decisões | M1 | P | Cético [C-R5] |
| Org-chart de Gens: lente adversarial obrigatória só onde número toca produto | M0 | P | Cético [C-R6] |

---
---

# APÊNDICE — Diagnósticos integrais das lentes (zero-compressão)

> Reproduzidos na íntegra, sem edição, para preservar o raciocínio e os dissensos de cada especialista. Ordem: Arquiteto RAG · Plataforma de dados · Legal-tech · Geoespacial · Mercado real TDC · Estrategista de produto · Ceticismo de governança (Lente 7, reaberto append-only).

## Lente 1 — Arquiteto sênior de sistemas RAG/LLM jurídicos (10+ sistemas em produção)

**Diagnóstico:** O que está CERTO (e é raro no mercado): chunking por dispositivo com caminho hierárquico, vigência POR CHUNK com exclusão de revogado por default, gate 1.7 com 3 travas combinadas (cobertura+piso BM25+≥2 termos), guarda de verbatim (só indexa `confianca:alta`), normalização de milhar para nº de lei, evals com exit-code como gate de CI e piso anti-falso-verde. Para 1.877 chunks, BM25 stdlib determinístico é a escolha correta — não é ingenuidade, é adequação de escala. O que está QUEBRADO e eu VERIFIQUEI no índice vivo: (1) C-28 está ATIVO — o chunk `16050::132-art-125` tem 131 chars truncados em "incisos do", e a fórmula PCpt (o dispositivo mais importante do produto inteiro) vive num chunk ROTULADO "Art. 124"; causa-raiz visível no `fatiar.py`: `RE_ARTIGO` é IGNORECASE e casa a remissão "art. 124 desta lei," que caiu em início de linha — o loop classificou como "QUE/depois" e EU DISCORDO: é correção de regex + re-index, e hoje qualquer consulta pela fórmula central do TDC cita dispositivo errado (violação material do 1.7, e NENHUM eval pega porque o eval confere o rótulo — que mente). (2) Composição do corpus: 12 das 19 leis são federais da era IPTU; o corpus TDC-relevante são ~5 leis, e FALTAM exatamente as que o engine e a tabela de 47 fatores CITAM: Decreto 57.536/2016 (o rito inteiro, Regra da Esquina, DPC 5 anos), 17.975/2023, 18.081/2024, 17.577/2021, 18.222/2024 — o RAG não consegue verificar as leis que o produto usa. Isso importa MAIS que embeddings. (3) Só 2/1.877 chunks marcados `revogado` num corpus que inclui o PDE alterado pela 17.975 — a regra conservadora (só revogação integral no início do corpo) deixa §§/incisos revogados passarem como vigentes, e os 293 `compilado` indexam TAMBÉM o texto antigo citado (BM25 pode rankear pela redação superada). (4) 14 evals ativos para 19 leis é fino demais; leis indexadas sem nenhum eval próprio. (5) A armadilha lexical (B-5) é em parte problema de STEMMING PT ausente e de não usar o filtro `tema` que JÁ EXISTE e está populado (454 chunks TDC) — há degrau determinístico barato antes de pagar embeddings. (6) B-6 está acoplado errado no BACKLOG ao "mesmo provedor de embeddings": o grafo de remissões é regex puro, 100% local, zero dependência. Veredito sobre produto-fim vs infra: o RAG é INFRAESTRUTURA do produto-lista — o comprador do Potencial Urbano compra a lista/dossiê defensável, não uma caixa de consulta; o papel do RAG é tornar mecânica a verificação dos 47 fatores e a citação de cada linha. Como produto-fim não tem comprador demonstrado e o corpus é TDC-cego em jurisprudência.

**Posição nos forks:** (a) Posição na cadeia: pela minha lente, o ativo defensável que vocês têm é o PIPELINE AUDITÁVEL (fator→dispositivo→eval), que vale tanto para vender inteligência quanto para corretagem — mas ser PRINCIPAL exige antes resolver a divergência de 27% contra as 167 certidões reais (C-16): comprar crédito com engine descalibrado é assumir o risco do próprio erro. Sinal fraco a favor de inteligência+corretagem: o achado dos 92 anos de estoque teórico diz que o gargalo é DEMANDA, não originação. (b) Ordem de expansão: APROFUNDAR a via 1 primeiro — as lacunas de corpus (decretos do rito, 17.975, 18.081, jurisprudência TDC) bloqueiam a via 1 E todas as outras; abrir vias 2-6 multiplica trabalho geográfico sem adicionar corpus jurídico novo. Fechado o trilho na via 1, as vias 2-6 o reutilizam quase de graça (o C-15 do laudo já mostra isso no geo). (c) Preço: pela disciplina 1.7, todo número exibido carrega dispositivo — o equivalente-outorga ÷4 TEM dispositivo (Art. 128 §1º), o proxy PCpt×V como "preço" NÃO tem. Publicar ÷4 como âncora citável, o benchmark das certidões como EVAL de calibração (não como número de vitrine enquanto a divergência de 27% não for explicada), e o proxy renomeado a teto teórico.

**Recomendações:**
- **R1 — Corrigir o chunker C-28 AGORA (discordo do 'depois' do laudo).** Em fatiar.py: impedir que remissão em início de linha abra chunk — exigir 'Art' com maiúscula E/OU guarda de monotonicidade (novo nº de artigo deve ser > último do mesmo corpo; remissão 'art. 124' dentro do Art. 125 viola e não abre chunk). Re-fatiar/re-indexar 16.050 e 16.402. Eval novo exigindo topo rotulado 'Art. 125' com texto contendo 'PCpt = Atc x CAbas x Fi'. *Por quê:* a fórmula central do TDC hoje é citada como 'Art. 124' — citação juridicamente errada na consulta mais importante do produto (violação material do 1.7). Custo ~1 hora. *Esforço: baixo · quando: agora.*
- **R2 — Corpus TDC-crítico antes de embeddings: os 5 diplomas que o engine cita e o RAG não tem.** Ingerir verbatim: Decreto 57.536/2016, Decreto 58.289/2018, Lei 17.975/2023, Lei 18.081/2024, Lei 17.577/2021 (+18.222/2024). Prioridade ACIMA das 13 municipais genéricas. *Por quê:* a Regra da Esquina, o +10% exclusivo-TDC, o Fi pós-17.975 e o rito da DPC são citados pelo engine SEM que o texto exista no índice. *Esforço: medio · depende de MOU/Drive.*
- **R3 — Camada semântica: RRF como expansão de RECALL, gate 1.7 continua lexical; sem vector DB.** Degrau barato primeiro (stemmer PT RSLP-lite + roteador passando --tema). Se não bastar: voyage-3-large via API, vetores persistidos como artefato versionado, cosseno numpy brute-force, fusão BM25 por RRF. REGRA INVIOLÁVEL: o semântico só ADICIONA candidatos; FUNDAMENTADA continua decidida pelas 3 travas lexicais. *Esforço: medio · depende de R2 + chave Voyage.*
- **R4 — Grafo de remissões (B-6) DESACOPLADO de embeddings — é regex, é local, roda já.** Extrator determinístico sobre os 19 verbatim → rag/grafo/remissoes.csv. *Por quê:* o BACKLOG amarra B-6 ao provedor de embeddings — acoplamento errado que atrasa trabalho 100% local. *Esforço: baixo · quando: agora.*
- **R5 — Endurecer vigência-por-chunk: granularidade sub-artigo + não rankear pela redação superada.** Auditar os 2 chunks 'revogado' contra a lista dos dispositivos do PDE alterados pela 17.975/18.081; marcar §§/incisos revogados dentro de artigo vigente; nos 293 'compilado', indexar para BM25 só a redação vigente. *Esforço: medio · depende de R2.*
- **R6 — Escalar o eval suite como política mecânica: nenhuma lei é 'indexada' sem eval próprio.** Lei indexada com <2 evals FALHA o gate; MIN_ITENS = f(corpus). *Esforço: medio.*
- **R7 — Jurisprudência TDC (B-21) via pedido único com lista de captura EXATA.** Temas STJ/STF sobre outorga onerosa/solo criado/tombamento, apelações TJSP sobre TDC-SP, pareceres TCM-SP. *Esforço: medio · depende de MOU.*
- **R8 — Posicionar o RAG como motor de verificação do produto: fator→dispositivo→eval, não chat.** Materializar a tabela de 47 fatores como tabelas/fatores-tdc.csv; CI cruza fator 'verificado' sem eval verde = gate vermelho. Sobre ETAPAS×MOTORES: direção certa, mas NÃO construir codex-por-motor antes desta tabela; resistir a criar 7 estruturas de uma vez. *Esforço: medio · depende de R1, R2.*

## Lente 2 — Engenharia de plataforma de dados (geo/cadastral — medallion, PostGIS, pipelines idempotentes)

**Diagnóstico:** O produto H1 é um RESULTADO, não um pipeline — e o repo já sabe disso (C-01/EF-1), mas o resgate para zepec/pipeline/ ficou incompleto: overlay_zona.py linha 8 ainda tem DL apontando para o scratchpad efêmero da sessão, colunas do IPTU resolvidas por posição, e não existe um runner que reproduza a cadeia de um checkout limpo. A distorção de infra mais gritante: vocês PAGAM um PostGIS de 8GB que usa 21MB, enquanto re-streamam 894MB de IPTU por pergunta e re-baixam 457MB de shapefiles por run — e o custo disso não é só egress: é que cada re-execução vira "reconstruir a sessão", o oposto de idempotência. O overlay atual é tecnicamente errado (centroide da 1ª feature, 1 zona/lote, join Q14 por 1 face quando a Regra da Esquina do Decreto 57.536/16 Art.3 IV exige MAX entre faces — subavaliação sistemática); PostGIS resolve as três coisas nativamente (ST_PointOnSurface, interseção N:N com fração de área, GROUP BY face). Não existe conceito de vintage em lugar nenhum: quando IPTU_2027 e Q14-2026 chegarem, o desenho atual obriga a reescrever recortes em vez de dar APPEND com coluna de exercício — e o princípio 1.6 (toda norma tem vigência) já é doutrina do projeto para LEIS, só falta aplicá-lo a DADOS. O bucket tem 40,6% de duplicatas byte-identicas porque existem 3 canais de upload ad-hoc com colagem manual de chave, enquanto o runbook rclone de 1 comando (24/06) nunca rodou. O espelho oficiais.* diverge em silêncio do git (C-27) porque ninguém decidiu UMA política de canonicidade. Sobre a proposta Bronze/Silver/Gold x 7 motores: a metade medallion está CERTA e já existe implicitamente (Storage=bronze, oficiais.*=silver, zepec/ferramenta=gold) — formalizar custa 1 página; a metade "codex fino por motor + visão humana gerada" é cerimônia que, num shop de 1 dono + instâncias, corre o risco de consumir sessões que deveriam ir para a camada física. E dbt agora seria purismo: o valor do dbt (DAG declarado, modelos idempotentes, testes de contagem) vocês obtêm com SQL idempotente em migrations + runner + gates de contagem no CI, sem adicionar uma toolchain que as instâncias teriam que reaprender a cada boot.

**Posição nos forks:** (b) ordem de expansão: da minha lente, este fork é FALSO se a plataforma for feita certa — materializar lote→zona da cidade inteira no PostGIS (C-15) custa quase o mesmo que refazer o overlay só dos cedentes, e depois disso cada via 2-6 é um WHERE; não escolham "aprofundar vs abrir", escolham "plataforma uma vez, vias de graça". (c) preço: dado que o engine diverge 27% na mediana das 55 certidões verificáveis, um produto de dados sério NÃO publica ponto — publica as 3 colunas com proveniência (proxy regulatório, equivalente-outorga /4, benchmark de certidões) + faixa v_min/v_max por SQ (C-11); a âncora comercial default deveria ser o equivalente-outorga /4 (único com dispositivo citável, Art.128 §1) até o benchmark ser calibrado. (a) posição na cadeia: opino de leve — a plataforma que vocês já têm (auditável, citada, reprodutível-em-breve) é exatamente o ativo de "vender inteligência"; ser principal exige a camada de demanda/liquidez que os próprios dados mostram ser péssima (54k m2/ano vs 5M m2 = 92 anos de estoque), então principal é a opção com pior suporte de dado hoje.

**Recomendações:**
- **PD-1 — Fechar o resgate do pipeline: parametrizar paths + canal único rclone + dedup do bucket.** Remover path de scratchpad, resolver colunas por NOME de header com abort, criar refazer_oficial.sh; executar rclone como CANAL ÚNICO com manifesto CSV versionado (sha256); rodar delete das 253 duplicatas + guarda anti-duplicata. *Esforço: baixo · quando: agora.* DoD: `grep -rn 'tmp/claude' zepec/pipeline/` = 0; refazer_oficial.sh reproduz contagens (3.905/3.676/3.693/3.014/2.937); query de duplicatas = 0.
- **PD-2 — IPTU_2026 e Quadro 14 COMPLETOS viram tabelas Postgres com coluna de vintage.** dados.iptu (894MB, 3,9M linhas, ano_exercicio=2026, pg_trgm no endereço); tabelas.q14 com TODAS as 179k faces. Loader idempotente. *Esforço: medio · depende de PD-1.* DoD: view q14_max_face existe; rodar loader 2x não altera contagens.
- **PD-3 — Geo no PostGIS: lote→zona da cidade inteira, N:N, materializado uma vez.** ogr2ogr dos 96 SIRGAS_LOTES + 42 camadas → geo.lote/geo.zona (SRID 31983); geo.lote_zona com ST_Intersection N:N, ST_PointOnSurface fallback. *Esforço: medio · depende de PD-1.* DoD: cobre ~3,9M lotes; recupera ≥400 dos 454 sem CAbás.
- **PD-4 — Decidir e executar UMA política de canonicidade: banco reconstruível do git.** Todo schema via migrations + loaders idempotentes; 'supabase db reset + loaders' reconstrói tudo. *Esforço: baixo · depende de PD-2.*
- **PD-5 — Gates de DADOS no CI (a versão 80/20 do dbt — sem dbt).** consolidar.yml ganha zepec/**, engines/**, tabelas/** + pcpt/oodc autoteste + byte-diff do enriquecimento + asserts de contagem do funil + eval zepec-h1. NÃO adotar dbt agora. *Esforço: baixo · quando: agora.*
- **PD-6 — Formalizar o medallion ENXUTO e conter a cerimônia dos 7 motores.** ARQUITETURA-DADOS.md de 1 página; matriz ETAPAS×MOTORES como taxonomia de DOCUMENTAÇÃO, não 21 células de codex. Discordo da parte 'codex fino POR MOTOR': um CODEX de dados único + tabela de 47 fatores basta. *Esforço: baixo.*
- **PD-7 — Gate de segurança ANTES da Fase B (socios.csv 3,4GB com CPF).** Spend cap religado; bucket PII segregado privado; RLS deny-all provado; INFRA-SEGURANCA.md; fim de chave hardcoded. *Esforço: baixo · quando: agora.* DoD: curl anônimo ao path PII = 403; SELECT com anon key = 0 linhas.

## Lente 3 — Legal-tech / Direito urbanístico (risco jurídico de produto auditável)

**Diagnóstico:** Verifiquei contra o verbatim indexado, não confiei no doc mestre. Achado central que muda o roadmap: o Fi escalonado (LPUOS Art. 24, I-VII) do pcpt.py está CORRETO. O caput do Art. 24 aplica os 7 incisos a "imóveis enquadrados como ZEPEC" em geral (novas declarações via art. 125 PDE) — a tese "Tribunal Lógico" (2 incisos só p/ BIR; 7 incisos exclusivos de parques no §1º) é REFUTADA pelo texto: o §1º é conservação, não tabela de parques. Mais: os incisos I-VII NÃO carregam marcador "Redação dada" — são texto original de 2016, estáveis. Logo o conflito (c) do doc mestre está RESOLVIDO a favor do engine, e a variação "2x no número" não foi capricho: foi correção de um Fi=1 que era erro. Isso é uma boa notícia e reduz o risco jurídico do cedente.

Mas o mesmo verbatim expõe o risco real: Arts. 22 e 25 da LPUOS foram REESCRITOS pela Lei 18.081/2024. O Art. 25 governa imóveis ZEPEC-BIR "para os quais JÁ tenha sido emitida Declaração" — regime diferente do Art. 24 (novas). O pipeline em massa aplica o escalonado a TODOS por default; para o cohort já-declarado (TEM_SALDO=98, ESGOTADO=6, e qualquer certidão pré-2024) o Fi correto é o da certidão sob o regime vigente à época — não o escalonado de hoje. É a instância concreta onde "vigência por chunk" (B-11c, feito) não basta e falta "vigência por redação-de-dispositivo datada".

Três exposições que TRAVAM ida a mercado: (1) preço foi despausado (D-DONO-1) mas a constante 4 (CAmaxcd) e a fórmula C (Art. 117/128) NÃO foram verificadas contra o verbatim — o doc mestre marca ambas como conflito interno; publicar qualquer R$ antes disso é o maior risco. (2) O gate de conservação (Art. 24 §1º + Art. 129 PDE) é pré-condição LEGAL de transferência e não está modelado como binário — vender "você tem R$X para vender" a quem não pode transferir sem restaurar é afirmação materialmente incorreta. (3) O gabarito real (C-16) mostra PCpt divergindo das 55 certidões oficiais em mediana 1,27x (até 12x) — o engine só vale para PROSPECÇÃO NOVA e isso precisa estar NA CARA do produto, não enterrado. Some-se o corpus TDC-cego (0/32 juris, B-21 verificado) e a ausência total de disclaimer/enquadramento de responsabilidade no repo (grep = zero): o produto hoje afirma fato com citação, o que é defensável, mas não tem a camada que o protege quando a afirmação vira recomendação de venda.

**Posição nos forks:** Fork (c) PREÇO — pela lente jurídica: NÃO publicar proxy regulatório (PCpt×V) nem equivalente-outorga (÷4) como número ao cliente até Art. 128 estar verbatim-verificado. A constante 4 é asserção do doc mestre ("densidade máxima teórica de SP"), não dispositivo lido. Entre as três âncoras, a única defensável hoje é o BENCHMARK das 167 certidões reais (fato observado, não interpretação) — e mesmo esse como faixa, não ponto. Recomendo: mercado (benchmark) para falar de R$ com cliente; equivalente-outorga só como teto interno depois de verificar Art. 128; proxy PCpt×V nunca sai como "valor". Fork (b) ORDEM — aprofundar a via 1 (ZEPEC) antes de abrir vias 2-6. A via 1 (Art. 24/125, sem doação) está verbatim-verificada e é o único terreno onde o engine bate com a lei. As vias 2-6 dependem do lado RECEPTOR e das restrições binárias que estão por verificar. Fork (a) POSIÇÃO — vender INTELIGÊNCIA/DADOS é a posição de menor risco jurídico DESDE QUE com disclaimer de decision-support (não parecer). Corretagem/gestão já expõe a unidade a dever de informação qualificado sobre saleability. Principal só depois de B-21 + gate de conservação + Art. 128 fechados.

**Recomendações:**
- **L1 — Travar qualquer R$ até Art. 128 PDE ser lido verbatim (constante 4 + fórmula C).** Indexar Art. 128 e Art. 117 verbatim; reescrever art128.py citando §1º; confirmar OU marcar como pendência a constante CAmaxcd=4 e a grafia da fórmula C. Nenhum R$ sai sem dispositivo citado. *Esforço: medio · quando: agora.*
- **L2 — Gate de conservação (Art. 24 §1º + Art. 129) como binário de elegibilidade.** Separar ato_tombamento de atestado_conservacao_art129; cedente sem atestado vira estado 'PRE-CONDICAO'. *Esforço: baixo · quando: agora.*
- **L3 — Vigência por redação datada para o cohort já-declarado (Art. 25 reescrito por 18.081/2024).** Impedir o engine de aplicar o Fi escalonado por default quando o imóvel JÁ tem declaração; citar Art. 25 (redação 18.081) em vez de Art. 24. *Esforço: medio · depende de L1/B-7.*
- **L4 — Surfaçar a divergência de 27% do gabarito real — PCpt só vale para PROSPECÇÃO NOVA.** Materializar eval pcpt-vs-certidoes (55 pares) + coluna qualidade_estimativa. *Esforço: medio.*
- **L5 — DISCLAIMER e enquadramento de responsabilidade no produto.** DISCLAIMER.md + cabeçalho no CSV/Excel/dossiê (decision-support, não parecer; proxy ≠ mercado; valor venal ≠ valor de outorga — vacina R16; data-base Q14 jan/2025). *Esforço: baixo · quando: agora.*
- **L6 — Checklist de due diligence mínima por imóvel antes da abordagem.** GDA, validade da DPC (5 anos, Decreto 57.536/16), Atestado Art. 129, CADIN/CNIB, não-remembramento, esfera de tombamento; semáforo citado. *Esforço: medio.*
- **L7 — B-21: capturar jurisprudência de TDC e registrar os 3 conflitos do doc mestre com status verbatim.** Fi (RESOLVIDO), fórmula C/Art. 117 (PENDENTE, ver L1), OUC vedação × conversão condicionada (PENDENTE). *Esforço: alto · depende de egress/Drive.*
- **L8 — Gate jurídico para o merge do Produto B (receptor/OODC) ao main.** Condicionar o merge à verificação verbatim da fórmula C E à camada de restrição binária (OUC/Art.115, ZER, ZEPAM, APM, novos PIU, R3/R4, estoque distrital Q15/16). Sem ela oodc.py calcula outorga onde a lei VEDA. *Esforço: alto · depende de L1; D-DONO-3.*

## Lente 4 — Engenharia Geoespacial (PostGIS, overlay urbano, cadastro)

**Diagnóstico:** A camada espacial hoje é um SCRIPT DE FOTO, não um sistema. `overlay_zona.py` faz o join correto na intenção (STRtree + prefere zona-base com CA sobre o selo ZEPEC, linhas 88-94), mas comete quatro erros geoespaciais clássicos que custam cobertura e correção: (1) usa `.centroid` (linha 77) — para lotes em L/côncavos/multipart o centroide cai FORA do próprio polígono (14 casos medidos) e fora de qualquer zona (293 casos); `representative_point()` já resolveria os fora-do-lote, mas o certo é overlay POR ÁREA (max ST_Area da interseção lote×zona), que ainda expõe e sinaliza os lotes multi-zona que hoje pegam zona única em silêncio (113 mudam de zona com o ponto certo, 88 com CAbás diferente — isso é erro de VALOR, não cosmético). (2) O bloco dos 454 (355 APC + 77 ZOE + 9 APP + 8 AUE + 5 BIR) não é bug de join: o centroide só intersecta o selo ZEPEC/ZOE e NENHUMA zona-base foi carregada/existe sob aquele ponto — precisa overlay N:N (devolver todas as camadas) + garantia de que TODAS as zonas-base entraram no DL + confirmação jurídica de que o CA da zona-base se aplica ao lote tombado (ressalva dialética: APC/APP podem legitimamente não ter CA simples — parâmetro caso-a-caso do CONPRESP; sinalizar, nunca fabricar). (3) O degrau 0 — 1.839 sem SQL (30% da base) — é o maior buraco isolado e NÃO é problema de geometria pura: o caminho de maior rendimento é casar `endereco_mestre` contra as strings de endereço do próprio IPTU_2026 (relacional/fuzzy, sem geometria), com fallback espacial via `SIRGAS_SHP_logradouronbl`. (4) A "Regra da Esquina" está violada: o V casa por UM codlog (`sql[:6]` + codlog único do IPTU, enriquecer_oficial.py L57), subavaliando 15% dos lotes de esquina e deixando ~25 linhas sem V. Infra: ZERO PostGIS apesar do instância paga usar 21MB de 8GB — tudo re-baixa 457MB/414 shapefiles e reconstrói unary_union de 46 camadas a cada run. E, contra a doutrina 1.7, a camada espacial é a ÚNICA sem eval: a zona nunca foi validada contra amostra GeoSampa.

**Posição nos forks:** (b) ORDEM DE EXPANSÃO é onde a geoespacial tem a fala mais forte, e ela quase DISSOLVE o fork: as vias 2-6 precisam da query INVERSA (zona→lotes). Se você materializar o overlay lote→zona da cidade inteira UMA vez em PostGIS (GEO-4), a via 2 (ZEPAM), 5 (parques) e 6 (corredores) viram literalmente um `WHERE zona=X` — custo marginal ~zero. Logo a recomendação não é "aprofundar vs abrir": é construir a ESPINHA espacial primeiro (comum a tudo), depois fechar a cobertura da via 1 (os 454 + 1.839), e aí as vias 2-6 caem de graça. (a) POSIÇÃO NA CADEIA: a espinha (lote→zona→CA→restrições, cidade inteira, com vigência) É o ativo de dado diferenciado — ninguém no mercado tem esse overlay materializado e auditável. Isso pesa para VENDER INTELIGÊNCIA/DADOS. Mas é fork-agnóstica — construa independente da escolha. (c) PREÇO: fora da minha lente decidir a base, mas os INSUMOS do preço são espaciais e estão errados hoje — MAX(V) da esquina (subavalia) e Fp por macroárea (Quadro 6, nem carregado). Fixe o insumo espacial ANTES de discutir a âncora de preço.

**Recomendações:**
- **GEO-1 — Overlay por ÁREA em vez de centroide (max interseção lote×zona).** Colunas zona_2, pct_area_zona1, flag_multi_zona; representative_point() como fallback. *Esforço: medio · quando: agora.* DoD: ≥250 dos 293 recuperam zona ou flag; N≥30 conferidos à mão.
- **GEO-2 — Resolver zona-base sob o selo ZEPEC/ZOE (overlay N:N) — os 454.** Devolver TODAS as camadas; zona-base de maior área; fallback quadra. Confirmação jurídica se o CA da zona-base se aplica a APC/APP (senão FLAG). *Esforço: medio · quando: agora.* DoD: zona_base para ≥400 dos 454; PCpt sobe de 3.014 para ≥3.400.
- **GEO-3 — Geocodificar endereço→SQL dos 1.839 sem SQL (degrau 0).** Fuzzy endereco_mestre × IPTU_2026 (pg_trgm); fallback SIRGAS. Nunca sobrescrever SQL oficial. *Esforço: alto · curto.* DoD: taxa de recuperação medida; ≥20 conferidos à mão.
- **GEO-4 — Materializar o overlay lote→zona da cidade inteira em PostGIS.** lotes 3,9M + 46 camadas, GIST, tabela lote_zona. Caveat: pode estourar 8GB — avaliar ST_SimplifyPreserveTopology. *Esforço: alto · medio.* DoD: overlay de cedente novo = SELECT <2s; WHERE zona='ZEPAM' retorna a lista.
- **GEO-5 — Auditoria de cobertura da camada RECEPTORA.** TEMOS: eixos ZEU/ZEUP, ZER/ZEPAM/ZEP, ZOE, macroáreas, cota_solidariedade, APAs. FALTAM: OUC, novos PIU, R3/R4 (PMRR), APM/APRM, Quadro 6 Fp. zepec/COBERTURA-RECEPTORA.md com tabela fator→camada→status. *Esforço: baixo · quando: agora.*
- **GEO-6 — Regra da Esquina espacial: V = MAX entre todas as faces do lote.** MAX(V) sobre faces adjacentes; v_face_usada, v_min_sq, v_max_sq, flag_v_sensivel. Cita Art. 3º IV Decreto 57.536/16. *Esforço: medio · curto.* DoD: ≥24 das 25 sem V recuperam por face vizinha.
- **GEO-7 — Eval da camada espacial contra amostra GeoSampa (gate de auditabilidade).** evals/ground-truth/geo-overlay.json com 30-50 cedentes conferidos; step no consolidar.yml. *Esforço: baixo · quando: agora.* DoD: teste falha ao injetar zona errada.

## Lente 5 — Especialista no mercado real de TDC/outorga de São Paulo (lado da DEMANDA)

**Diagnóstico:** O produto foi construído como um CATÁLOGO DE OFERTA (6.131 cedentes, 5,0M m² de PCpt, agregado R$8,83bi) num mercado onde a oferta NÃO é o recurso escasso — a demanda é. O fato dominante do repo, e que reordena tudo, está nos próprios dados: o mercado absorveu ~54k m²/ano (2017-2025) e caiu para ~25k em 2023-2025, contra 5,0M m² de portfólio = ~92 anos de estoque teórico; e o teto pecuniário do FUNDURB (Art.24§5 LPUOS, ~R$7,8mi/ano) torna fisicamente impossível monetizar os bilhões exibidos. Conclusão de mercado: a lista de cedentes é COMMODITY (a ZEPEC é pública e oficial) e o agregado R$8,83bi é uma ficção regulatória que qualquer incorporador desconta na primeira conversa. O valor escasso — e portanto o negócio — é o MATCH: saber qual cedente tem comprador plausível AGORA, e ter a relação com o receptor. Discordo frontalmente do enquadramento "carteira de R$8,83bi" e da narrativa de inventário: é o erro estratégico mais caro do projeto porque destrói credibilidade com o comprador sofisticado. Verifiquei direto na fonte (lista_certidao_ZEPEC-BIR): a demanda inteira está lá, intacta e não usada — 167 operações, receptor com SQ/lote/endereço/distrito, área cedida equivalente × área recebida REAL, ano. Isso é o ativo de maior alavanca do repo e está no raw. A concentração é nítida (Jardim Paulista, Vila Mariana, Moema, Itaim Bibi, Pinheiros) — ou seja, o crédito só limpa em ~5 distritos; um cedente de periferia sem comprador em 8 anos vale uma fração de um cedente cujo crédito é usável perto de um Eixo. Sobre a proposta de MOTORES: M5 (Mercado/Comercial) está listado como um motor entre sete iguais — para este mercado isso está invertido. Num mercado de 92 anos de estoque, a demanda/matching é o motor PRIMÁRIO que ordena todos os outros; catalogar oferta (M2/M3/M4) com mais precisão sem saber onde há comprador é polir o lado abundante. As correções de número honesto já aplicadas (Fi escalonado, saldo líquido, ÷4, esgotado/vedado des-precificado) estão certas e são pré-condição de credibilidade — mas corrigir o número derruba o número, e isso é a realidade do mercado, não bug. O contrato OPIT-SP/Bairro Vivo já é gestão comercial da via 1: confirma que o negócio JÁ é corretagem, e o produto deve servir a fechar TRANSFERÊNCIAS, não a engordar catálogo.

**Posição nos forks:** (a) POSIÇÃO NA CADEIA — Corretagem/gestão é a resposta, e o contrato OPIT-SP/Bairro Vivo já a confirma. A inteligência/dados deste repo é o HABILITADOR (originação + matching), não um SaaS standalone. PRINCIPAL (comprar crédito) é financeiramente perigoso — 92 anos de estoque, banco recusa TDC como colateral ("veto da Faria Lima"), haircuts de iliquidez 30-45%, teto FUNDURB — só faz sentido BACK-TO-BACK (crédito específico com receptor já assinado). (b) ORDEM — Aprofundar a VIA 1, mas o aprofundamento certo é construir o LADO DA DEMANDA da via 1, NÃO catalogar mais cedentes. Abrir vias 2-6 agora é destrutivo: elas geram oferta via doação (~8x potencial, Fi até 2,0) e adicionar oferta a um mercado de 92 anos de estoque piora o problema. Única exceção admissível é demanda-dirigida: a arbitragem parque-doação (P.6), e só quando houver comprador identificado. (c) PREÇO — Nenhum dos três isolado. Pilha obrigatória de 3 números, sempre juntos: teto regulatório (PCpt×V, rotulado teto), âncora regulatória (÷4, Art.128§1º) e BANDA DE MERCADO empírica — que é a única verdade: os 3 comparáveis pecuniários FUNDURB saem a 12-25% de V, e os 166 pares de conversão têm mediana recebida/cedida 1,247. O número que vai ao dono/comprador é a banda de mercado, ancorada pelo ÷4 e limitada pelo teto.

**Recomendações:**
- **MKT-1 — Construir o lado da DEMANDA: receptores.csv + camada de absorção/liquidez por distrito.** Extrair das 167 certidões (SQ, lote, endereço, distrito, m² recebida, ano, cedente de origem) + taxa de absorção anual + score de liquidez por distrito. *Esforço: medio · quando: agora.* DoD: receptores.csv com 167 linhas, 146 receptores distintos; coluna score_liquidez_distrito; RESUMO exibe absorção 2017-2025.
- **MKT-2 — Reenquadrar o headline: de 'carteira R$8,83bi' para 'taxa de absorção / anos-de-estoque'.** R$ agregado rotulado 'teto regulatório teórico — não realizável'; métrica de topo = absorção anual + anos-de-estoque por distrito + teto FUNDURB citando Art.24§5. *Esforço: baixo · quando: agora.*
- **MKT-3 — Calibrar o engine contra as 167 certidões com régua de mercado (oficial vence estimativa).** Cedente COM certidão exibe m² OFICIAL, não estimativa; PCpt confiável só para SO_ELEGIVEL. Não 'ajustar' para bater 1,27 (ruído de datas de protocolo). *Esforço: medio · depende de MKT-1.*
- **MKT-4 — Preço em pilha de 3 números, ancorado na banda de mercado (12-25% de V).** teto (PCpt×V), ÷4 (Art.128§1º), banda de mercado (166 pares + FUNDURB). Implementar art128.py calibrado (mediana 1,247). *Esforço: medio · depende de MKT-1.*
- **MKT-5 — Priorização por chance de venda (matching), não por m² bruto.** score composto: liquidez_distrito × proximidade a Eixo/Arco × estado INTACTO/TEM_SALDO × atestado Art.129. Atestado (63 cedentes) como estágio de funil. *Esforço: medio · depende de MKT-1.*
- **MKT-6 — Fixar a posição na cadeia: corretagem/gestão primeiro, principal só back-to-back.** Entrada datada no CODEX-COMERCIAL-TDC.md; métrica-norte = transferências fechadas. *Esforço: baixo · quando: agora.*
- **MKT-7 — Não abrir vias 2-6 agora — congelar como opção latente demanda-dirigida.** No-go para operacionalizar vias 2-6 como expansão de OFERTA. Exceção: arbitragem parque-doação (P.6) só com comprador identificado. *Esforço: baixo · quando: agora.*

## Lente 6 — Estrategista de Produto (B2B, nicho imobiliário / TDC São Paulo)

**Diagnóstico:** O projeto confunde "base de dados grande" com "produto vendável". O deliverable de hoje (zepec_cedentes.csv, 6.131 linhas) é um CENSO, não um produto. O produto só começa quando uma linha vira uma AÇÃO que um corretor executa. Medido no próprio repo: dos 6.131, apenas 599 estão "prontos para abordar" (negociável=sim + INTACTO/TEM_SALDO) e apenas 19 têm dono conhecido. O universo acionável real é 19, não 6.131 — e o produto nunca comunica isso. Pior: a porta de entrada do produto está desligada do valor. lista_prospeccao.csv está dessincronizada (28/06 vs 02/07), sem preço/PCpt, e o COMO-USAR.md NEGA que exista preço ("Preço: não está aqui"). Todo o avanço do H1.4 (Fi escalonado, saldo líquido, 2.937 preços) é invisível para quem usa a ferramenta. O comercial abre um arquivo que parece mais pobre do que o motor já calculou. O fato mais duro do domínio — e o que deveria reorganizar TODO o roadmap — é a liquidez: absorção ~54k m²/ano contra ~5,0M m² de oferta = ~92 anos de estoque teórico. TDC de cedente é um mercado estruturalmente ilhado de compradores. Uma lista de 6.131 cedentes "para ligar" vale pouco se 99% do estoque não tem comprador. O lado da DEMANDA (167 certidões, 146 receptores reais) está nos nossos dados e é ignorado. Esse é o maior erro de produto do projeto: construímos o lado abundante (oferta) e ignoramos o lado escasso e urgente (demanda), que é onde mora o dinheiro e a diferenciação. O número-vitrine (R$8,83bi proxy) é uma bomba de credibilidade: é proxy regulatório PCpt×V, ~4x acima do teto do Art.128, e diverge da mediana das certidões reais em 27%. A peça que fecha negócio — o dossiê por imóvel — não existe. A arquitetura de "motores M0-M6 + tabela de 47 fatores" é boa engenharia interna mas não é produto, e cria risco de gold-plating: perseguir completude de cálculo enquanto o artefato que fecha venda (dossiê + sinal de liquidez) não é entregue.

**Posição nos forks:** (a) — Ficar como INTELIGÊNCIA/DADOS servindo a gestora (contrato OPIT-SP/Bairro Vivo) no curto prazo, mas construir para VENDER AO RECEPTOR (incorporador). O lado cedente tem 92 anos de sobre-oferta — baixa urgência, baixa disposição a pagar. O lado receptor tem demanda recorrente, com prazo, e sem mercado transparente — é o lado com dinheiro e urgência. NÃO virar principal. O moat é a camada de MATCHING/liquidez de dois lados, não o inventário de oferta. (b) — APROFUNDAR via 1 até virar produto que fecha, e ADICIONAR o lado receptor. NÃO abrir vias 2-6 agora — abrir mais fontes de OFERTA quando a oferta já excede a demanda em 92x é destruição de valor. (c) — Publicar o EQUIVALENTE-OUTORGA ÷4 (Art.128, citável) como âncora, mas LIDERAR com o benchmark das 167 certidões reais como realidade de mercado, e rotular o PCpt×V como "teto teórico". Divulgar a divergência de 27% em vez de esconder. Nunca usar o R$8,83bi como headline comercial.

**Recomendações:**
- **P1 — Religar a entrega comercial ao valor já calculado (MVP honesto).** lista_prospeccao.py lê zepec_cedentes_oficial.csv e propaga pcpt/saldo/valor_equivalente/zona/pendência; reescrever COMO-USAR.md (parar de negar o preço); Excel do dono via make produto. *Esforço: baixo · quando: agora.* DoD: ≥1.800 linhas com valor; grep 'não está aqui' = 0; make produto gera .xlsx datado.
- **P2 — Definir a UNIDADE DE VALOR = dossiê por imóvel (a peça que fecha).** gerar_dossie.py: 1 página/SQL com memória de cálculo citada, à-vista vs parcelado (Art.124§3), checklist Art.129. Piloto nos 19 INTACTO-com-dono. *Esforço: medio · depende de P1.*
- **P3 — Virar o produto para a LIQUIDEZ (lado da demanda) — o maior diferenciador.** receptores.csv das 167 certidões; score de liquidez por distrito; RE-RANQUEAR por 'tem comprador agora?'. *Esforço: medio · depende de P1.*
- **P4 — Corrigir o número-vitrine e a mensagem de preço.** valor_equivalente_outorga = PCpt*V/4 (Art.128§1) como âncora citável; PCpt*V rotulado teto teórico; expor divergência de 27%; nunca R$8,83bi como headline. *Esforço: baixo · quando: agora.*
- **P5 — Trocar a métrica-headline de 'contagem' para 'FUNIL de acionabilidade'.** 6.131 elegíveis → 4.292 com SQL → 2.937 com preço → 599 prontos → 19 acionáveis-com-dono; funil.csv versionado. *Esforço: baixo · quando: agora.*
- **P6 — Dono em escala para mover 19 → centenas de acionáveis (Fase B).** Carregar socios/empresas/holdings/iptu-2020 após as oficiais; resolver dono da maioria dos 599; geocodificar os 1.839 sem cadastro. *Esforço: medio (peso externo) · depende de gate de segurança.*

## Lente 7 — Ceticismo de arquitetura/governança (anti-complexidade) para projeto IA-driven de 1 dono

> **Reaberto append-only em 2026-07-03 pela crítica adversarial.** O 7º parecer CHEGOU íntegro (diagnóstico + 7 recomendações); a primeira redação do roadmap o tratou como ausente e creditou o veredito cético a outras duas lentes (defeito nº1 da crítica). Reproduzido aqui sem corte, e a Seção 3 foi corrigida para lhe devolver a autoria e declarar o dissenso do medallion.

**Diagnóstico:** O projeto tem uma base técnica boa (RAG determinístico com citação, vigência-por-chunk, 14 evals verdes, engine com auto-teste) e um mecanismo de governança REALMENTE valioso: o gate "declarei feito != provei feito" (`fechar-instancia.py`) e o BACKLOG-ladrão. Esse núcleo eu defendo. O resto é sobrepeso, e a proposta de motores PIORA. Evidência dura de sobrepeso já instalado: 159 arquivos .md / 45.167 linhas para 1 dono; decisões numeradas até D141; 8 documentos que reivindicam ser "o estado" (MANIFESTO, BACKLOG, PROXIMA-INSTANCIA, HANDOFF-E-PENDENCIAS, ESTRATEGIA, ATA-VIVA, REGISTRO-DE-INSTANCIAS, BETA-CONTINUO); 20 docs datados write-once/read-never; 4 CODEX. O loop-melhoria sozinho tem 119KB. Onde o projeto REALMENTE quebrou (histórico, não especulação): (1) Fi=1 errado em 89% das linhas, agregado 2,5x inflado; (2) scripts geradores só no /tmp — pipeline era uma FOTO irreproduzível; (3) lista comercial dessincronizada e COMO-USAR.md NEGANDO que existe preço; (4) preço nascendo no script, não no engine (viola 1.3); (5) o gate NÃO cobre zepec/pcpt/art128 (confirmei: grep vazio) — regressão de produto sai com gate verde; (6) gabarito R14 nunca rodou e diverge 27% do real. NENHUM desses é falta de abstração de motores. Todos são: coisa construída não foi ligada ao gate, ou não foi commitada, ou não foi conferida contra a realidade. O ataque decisivo aos motores M0-M6: eles JÁ EXISTIRAM neste repo e viraram lixo. Em `engines/tdc/oraculos/` estão CONHECIMENTO_MESTRE_IA_V3.1_INABALAVEL, ORACULO_MESTRE_RELACIONAL_V4 ("INTELIGENCIA TOTAL / PERFEICAO ABSOLUTA"), MOTOR_3_CATALOGO_ESPACIAL, ESTRUTURA_SILVER (medallion Bronze/Silver/Gold) e motor00/travas_operacionais_v6.1.json — literalmente M0 travas, M2 relacional, M3 espacial, etapas Bronze/Silver/Gold. Pior: aquele `travas_v6.1.json` CANONIZOU "zepec_bir: 1.0" — o Fi errado que inflou o produto 2,5x nasceu de uma "camada de verdade verificada". A camada de travas não preveniu o erro; ela o ENTERROU como verdade. O doc-mestre é uma compilação de ~40 "Guias" v66→v90 sem SSOT declarado. A doutrina "zero-compressão / nada se descarta" é a CAUSA desse cemitério, não a proteção contra ele. Reconstruir M0-M6 é redesenhar o mapa que já produziu a bagunça.

**Posição nos forks:** (c) PREÇO — o único caminho defensável por governança é: equivalente-outorga PCpt×V/4 (Art.128, citado, C-03) como ÂNCORA + calibração contra as 167 certidões reais (C-16) como trava de realidade ANTES de qualquer R$ sair. O proxy regulatório sozinho já produziu o vexame dos R$17,5bi que viram ~R$2,4bi. Número que não reproduz o real (diverge 27%) não é opção de precificação, é defeito não-medido. Invariante: nenhum R$ vira produto antes de bater no gabarito. (b) ORDEM — aprofundar via-1 (ZEPEC) primeiro. Abrir vias 2-6 multiplica a superfície que o gate (já fino, nem cobre a via-1) tem de proteger, antes de a via-1 passar no próprio teste de realidade (R14 falha a 27%). Governança: não se alarga um pipeline não-validado. (a) POSIÇÃO NA CADEIA — fora da minha lente, mas registro o risco de org-cosplay e de capital: virar "principal (comprar crédito)" adiciona risco financeiro e um domínio de dado novo enquanto o ativo atual (a inteligência) ainda não passou no ground-truth. Ficar em dados/inteligência até a via-1 reproduzir o real.

**Recomendações:**
- **C-R1 — Estender o gate ao produto (a falha #1 real: engine fora do juiz).** `fechar-instancia.py` e `consolidar.yml` passam a rodar `pcpt.py --demo` e `art128.py`, um eval `zepec-h1.json` com 5-10 cedentes conferidos à mão, e um step que re-roda `enriquecer_oficial.py` e FALHA se o CSV divergir do commitado. Absorve C-09. *Esforço: médio · quando: agora.*
- **C-R2 — UM comando `make produto` reproduzível — matar a FOTO e o drift do deliverable.** Consolidar C-01 + C-07/08/19 num único alvo que regenera a cadeia inteira do zero, sem paths de /tmp, com contagens de regressão como assert. *Esforço: médio · quando: agora.*
- **C-R3 — REJEITAR M0-M6 × Bronze/Silver/Gold; adotar só o átomo útil: `fatores-tdc.csv` gateado.** Não construir a matriz motores×etapas nem codex-fino-por-motor. UM `tabelas/fatores-tdc.csv` {fator, valor, dispositivo_citado, lado, status_verificacao, eval_id}; o engine LÊ o CSV; linha `verificado` tem eval que falha se o engine divergir. **Este é o dissenso do medallion:** o cético rejeita TAMBÉM Bronze/Silver/Gold, ficando só com o CSV gateado. *Esforço: médio · quando: curto.*
- **C-R4 — Colapsar 8 fontes-de-verdade em 3 e ARQUIVAR o cemitério.** 3 papéis únicos: git=estado, MANIFESTO.json=status do pipeline, BACKLOG.md=trabalho aberto. `git rm` de `engines/tdc/oraculos/` e dos 20 docs datados (recuperáveis pelo histórico). Reinterpretar "nada se descarta" como "nada se APAGA do histórico git", não "tudo fica no working tree". *Esforço: baixo · quando: curto.*
- **C-R5 — Adotar a ÚNICA boa ideia dos motores: visão humana GERADA da verdade executável.** README/dossiê humano GERADO por script a partir do CSV/engine (C-20), nunca à mão. UM log de decisões datado append-only — não 6 codex-fino-por-motor. *Esforço: baixo · quando: curto.*
- **C-R6 — Aposentar o org-chart de Gens como cerimônia; lente adversarial só onde número toca produto.** Parar de modelar 6 papéis com handoffs formais (são subagentes com um prompt). Manter a lente adversarial triplo-limpo OBRIGATÓRIA só em entrega que altera número/engine do produto; opcional em edição de doc. *Esforço: baixo · quando: agora.*
- **C-R7 — Trava de realidade: nenhum R$ vira produto antes de bater nas 167 certidões.** Eval `pcpt-vs-certidoes` (55+ pares, C-16); coluna `qualidade_estimativa=INCONSISTENTE_COM_OFICIAL` onde diverge; `art128.py` calibrado contra os 166 pares antes de publicar R$. *Esforço: médio · quando: médio.*

> **Nota sobre o Apêndice (corrigida 2026-07-03):** as SETE lentes do painel chegaram e estão agora reproduzidas sem corte. A primeira redação omitiu a Lente 7 (ceticismo/governança) e atribuiu mal o seu veredito — a crítica adversarial pegou, e a correção está tanto aqui (parecer íntegro) quanto na Seção 3 (autoria + dissenso do medallion declarados). Nada aqui se joga fora; o apêndice é append-only.
