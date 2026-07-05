> **⚠️ SUPERADO (2026-07-03) por `docs/INVENTARIO-DRIVE.md`** (fontes por proveniência, D-DONO-4). Documento histórico (2026-06-18); descreve a árvore do Drive ANTES do achatamento (estrutura que não existe mais). Fileids antigos têm só valor histórico. _(banner lavrado pela PU 17 — DoD do B-8.)_

MAPA IPTU + TDC — INVENTÁRIO CLASSIFICADO E ESTRATÉGIA DE TRATAMENTO

Escritório do MOU (PMO de portfólio) — Projeto Potencial Urbano

Data: 2026-06-18 | Fonte: Google Drive de eduardo@saobentoservicos.com.br (somente arquivos próprios)

Método: enumeração recursiva D24 (conhecimento total da fonte) por 6 varreduras com subagentes; classificação em 2 dimensões (Tema e Função) + Origem + Formato.

==================================================================

0. COMO LER ESTE DOCUMENTO

==================================================================

- Tema: IPTU | TDC | Ambos | Neutro (insumo compartilhado: mapa, base cadastral).

- Origem: Oficial (lei/órgão público) | Não-oficial (terceiro/web) | Autoral (criado pelo MOU/seus motores de IA).

- Função no projeto: Doc-mestre/Manifesto · Operacional/Motor (Gems, prompts, RAG) · Jurídico (lei/jurisprudência/doutrina) · Memorial/Auditoria · Mapa-geo · Planilha-pesada · Enriquecimento/Descoberta-de-proprietário · Espelho/Carnê IPTU · Certidão/Ato administrativo · Dado oficial TDC (fila FUNDURB) · Comercial/Contrato/CRM · Dado-bruto/Export-IA.

- Os fileId estão entre parênteses para rastreabilidade.

==================================================================

1. SUMÁRIO EXECUTIVO

==================================================================

O acervo IPTU+TDC do MOU é GRANDE e VALIOSO, porém ESTÁ ENTERRADO EM REDUNDÂNCIA. Existem alguns milhares de instâncias de arquivo que resolvem para algumas centenas de artefatos lógicos únicos. O valor real concentra-se em 6 ativos estratégicos:

  (1) Os DOCUMENTOS-MESTRE autorais — a doutrina/estratégia de IPTU (4 docs) e de TDC (codex/holding/memoriais, ~12 docs).

  (2) Os MOTORES DE IA ("Gems" + Livros Mestres + chunks RAG + JSONs de regras) — a inteligência operacional que executa o negócio.

  (3) O CORPUS JURÍDICO oficial (≈50 leis/decretos/INs + jurisprudência STF/STJ/TJSP + doutrina/teses + NBR 14653).

  (4) O ACERVO GEOESPACIAL DE PRECIFICAÇÃO — o GeoSampa praticamente inteiro em shapefile (96 distritos lote-a-lote + zoneamento + ZEPEC + bens tombados + setor fiscal), ~0,7–0,8 GB.

  (5) As BASES DE ENRIQUECIMENTO E DESCOBERTA DE PROPRIETÁRIO — socios.csv (3,44 GB), empresas.csv (2,27 GB), holdings.csv (60 MB), série GUIAS DE ITBI PAGAS 2006–2024, IPTU_2026.csv (≈900 MB), iptu-2020-cep01.csv.

  (6) Os DADOS OPERACIONAIS OFICIAIS DE TDC — fila FUNDURB (backlog R$42,19M), declarações/certidões SMUL, base-mestre "TDC OFICIAL".

DIAGNÓSTICO CENTRAL (D26/D27 — destravar a esteira): o projeto não sofre de FALTA de matéria-prima; sofre de FALTA DE ORGANIZAÇÃO. O mesmo conteúdo foi reprocessado por pipelines de IA várias vezes, gerando 2 árvores-espelho de "data lake", 3 lixeiras, re-uploads triplicados de legislação e fragmentos _PART_/_Pagina_. Há ainda DESPERDÍCIO DE ESPAÇO MASSIVO: bases pesadas (socios/empresas/IPTU_2026) duplicadas entre árvores somam 15–20+ GB recuperáveis. O destravamento prioritário é DEFINIR UM SSOT (fonte única) por ativo e sanear o resto.

==================================================================

2. NÚMEROS DO ACERVO (com duplicação)

==================================================================

- Universo IPTU (busca por nome/texto): ~190 instâncias → ~95 documentos únicos.

- Universo TDC (busca por nome/texto): ~823 instâncias → ~95–110 itens únicos.

- Árvore "Documentos Novos" (recursiva): ~1.246 arquivos (dados_pericia1–8 + Novos).

- Árvore "POTENCIAL URBANO ATUAL" (recursiva): 909 arquivos in-tree.

- Cluster Inteligência (AI Studio + MOTORES + Certidões + IPTU 12-05 + Chunked): ~333 instâncias → ~158 únicos.

- Pasta MAPAS (geoespacial): 486 arquivos / 162 datasets / ~830 MB (numa das cópias).

- Fator de duplicação dos documentos-âncora: ~16–20× (ex.: "Memorial Estratégica" e "fila_tdc" cada um em 15–20 cópias).

NOTA: as árvores se sobrepõem fortemente (pastas-espelho). O número honesto é: poucas centenas de artefatos únicos, sob milhares de cópias.

==================================================================

3. INVENTÁRIO CLASSIFICADO POR EIXO

==================================================================

----- EIXO A — DOCUMENTOS-MESTRE AUTORAIS (a doutrina e a estratégia) -----

IPTU (Origem: Autoral; Função: Doc-mestre):

  - Mestre IPTU (1h-hlgvqKQQwIcfYwaekTcfdVJYZlNd6Sb3BDdrwB_1c) — o mais completo: 12 teses dialéticas + "Mapa Completo" blocos A–J de teses de redução, marcadas por robustez (consolidada/contestada/agressiva).

  - Estudo_Profundo_IPTU_Documento_Base (1OMDpTd3eWOPep_jp4oPJ6z825my1rg3D9jxK4hYeiSA) — consolidação jurisprudencial STF/STJ + isenções SP.

  - Documento Base: Inteligência Tributária e Otimização Avançada do IPTU (17JXwBrJkZGGBSWuzdb3aSRQ-_F5caHuZuhxHY5MOldk) — versão "motor de IA" do anterior (matriz tese↔gatilho).

  - IPTU-BASE (1rqvg4Fqlm9Edq-46gQZUp6GuZCL_Q0lKPot7IAFxZO0) — arquitetura dos 3 Gems (Auditor/Advogado/Closer). Rascunho.

  OBS: Estudo_Profundo ≈ Documento Base IA (pares irmãos). Mestre IPTU absorve ambos → candidato a SSOT único de IPTU.

TDC (Origem: Autoral; Função: Doc-mestre/Manifesto):

  - DOCUMENTO MESTRE: SISTEMA OPERACIONAL HOLDING TDC (1tbhRdfpD4pHeRl3wHSfusCBoNqCffn2xPJqSDhL05D8) — modelo de negócio "fábrica de 5 estágios" (5 Gems), regra de ouro "vendemos papel, não tijolo", Zero CapEx via Lei Rouanet, unit economics ~R$1,38M/ativo ROI ~6,9×.

  - Manual Operacional Negócio TDC (1ju82YtOpBEWFJVH9py4rajcbSeKb1HwsiwUdYvzErZ4) — manual jurídico-executivo + clusters de imóveis reais (Vila Maria Zélia, Bixiga, Ipiranga, Campos Elíseos, Mooca).

  - CODEX_TDC_MASTER (1bZ3Awl_k78vp1i2RrrpeP9AXzJrQBz8ecwMsv58srYM, 111 KB) + variantes CODEX (1ikVyaN3LFcNHRDDMGoQRGgxRs98LoSVTdV6uO18SQwY), codex omega (1XlNFRYSwekFJXzOOB9nzjCYyYiwYukEmuVmx-HIKyAc), BÍBLIA DA INTELIGÊNCIA HUB TDC-SP (1gx0kxXhPcxd7cB0zr94eItvWs2Vo9pSYh50FFuOk_Yc).

  - manifesto_data_lake_tdc.json (1emeA6wXOKiz0b3u5qLR4Wjw3YA9cAV2XZS1r4akqLzo) — índice mestre do data lake (5 motores).

  RISCO: existem VÁRIAS gerações do "cérebro" TDC (CODEX_TDC_MASTER, CODEX, codex omega, BÍBLIA HUB, CONHECIMENTO_MESTRE_IA V3/V3.1, MANIFESTO_TOTAL_DE_TRANSICAO) SEM um SSOT declarado. Ponto cego a destravar.

----- EIXO B — INTELIGÊNCIA OPERACIONAL (os motores que executam) -----

  - GEMS IPTU (Google AI Studio, .makersuite.prompt; Autoral; Operacional/Motor): Gen 1 IPTU (1A4wqEiQUTb_0by6m-KvOtN988iI1Xn7p), Gen 1 Matemático IPTU (19nZ7YQsex0gyr9r9Dbsnsg_xWj0hE5JG), Gen 2 IPTU (1ZULzWaOZTfiPsklOkjThTyM97-yY4dzc), Gen 2-Advogado IPTU (1obxaKZhXviBv9ij-_KGkMYMVaUbfaV0f), Gen 3 IPTU (1A8RDOZqA1dDM9rIgsxsqT6gEwKMQBzQ5), GEN 3-GOVERNANÇA (1A0anjM_lJ6giTcNDypYUerMrtpA3Hxka), Organização Normativa do IPTU SP (1VuXTd2GG9b7wLClEVq-ONOspHw40xdPe), Estratégias de Restituição Tributária Municipal (1OsFHUrl-YwRYB_BFRt92Goz1D2pNLXKG).

  - MOTOR DE TDC (MOTOR00; Autoral; Operacional/Motor + RAG): semantic_chunks_v6.1.json (1mxpQK6JL859KMiz3pDv557tb-SsknzE7) = NÚCLEO com fórmulas de cálculo de potencial (ZEPEC-BIR/Doação/Recepção) e travas; travas_operacionais_v6.1.json (1gxTzmOreRtRmkthMFwTtT1O3SvnGUnFv); negative_prompts_v6.1.json (13ZC8I_aPVbk66PPzGwskqewPldl73MvQ).

  - LIVROS MESTRES RAG (MOTOR1; Autoral): MOTOR_1_LIVRO_MESTRE_ADMINISTRATIVO_E_GERAL.md (54,9 MB, 1fG_Kp6I8QGh8gI3SGfvjnb6hDxt1wB5U), LEGISLACAO_URBANISTICA.md (11 MB, 1qSXfyjMJdwxKg-6cpVdzhjg1wZSA4_qb), PATRIMONIO_HISTORICO.md (1Mpg6pzBZp-K0hJMKxkoveQMLzs0PM8xk), CERTIDOES_E_ATOS_ADMINISTRATIVOS.md (1iwxoV1UpHxGJMweWMLkHhpdV21BB9cl6).

  - BASES RAG/CHUNK: base_iptu_chunks.json (11,1 MB, 12KV81vYCEbcOZuEYRy5dyx8hYnmRxCCR); Documentos_Chunked_Para_IA (chunk_ia_parte_01..10.txt).

  - ORÁCULOS GEOGRÁFICOS / ENGINES ETL (.md; Autoral): ORACULO_GEOGRAFICO_DEFINITIVO_V3, ORACULO_MESTRE_RELACIONAL_V4, MAPA_EXATO_DATALAKE, HIERARQUIA_DE_FONTES_ORACULO, MANIFESTO_PLATINA_FINAL, MOTOR_3_CATALOGO_ESPACIAL (pasta "Criados").

  - ferramenta_busca_tdc.py (1PwD2BTq_L03S-Ic4b6c9sh90-puCPBCmc2FIA2NpnQg) — script.

  ATENÇÃO: esta inteligência vive em PROMPTS do AI Studio e .md/.json soltos no Drive — FORA de qualquer versionamento git. É o maior ponto cego de continuidade.

  CAPACIDADE: os Gems CALCULAM imposto/potencial e ARGUMENTAM juridicamente. NÃO há motor que faça descoberta de proprietário — isso é feito por cruzamento manual das bases do Eixo E.

----- EIXO C — CORPUS JURÍDICO OFICIAL -----

  Legislação (Oficial; Jurídico) ≈50 diplomas únicos: Lei 6.989/66 (IPTU-SP), 10.235/86, 11.614/94, 15.889/13 (PGV), 17.719/21 (+Anexos), 18.330/25; PDE 16.050/14, LPUOS 16.402/16, 17.975/23, 18.081/24; Estatuto da Cidade 10.257/01; CTN 5.172/66; Art.156 CF; Decretos 52.884/56.954/57.536/58.592/60.939/63.698/62.466/63.728; INs SF/SUREM 2/10/14; Portarias SMUL 172/2024 e 08/2026; NBR 14653.

  Jurisprudência/Doutrina (Oficial/Não-oficial): acórdãos TJSP, REsp 1.949.182, ARE 1.216.078 (Tema 1062), STJ Tema 1113, ADI Arco Pinheiros, Súmula 160 STJ; artigos Migalhas/Jusbrasil; teses PUCSP/UFC.

  Localização principal: pasta "Novos" (1LGrKx7sY8Jot1b1ROG53mhb-yy-zHQLv), dados_pericia1/2/7, IPTU-Sergio, e re-uploadado 3× no AI Studio.

----- EIXO D — ACERVO GEOESPACIAL DE PRECIFICAÇÃO (os "mapas") -----

  Pasta MAPAS (Neutro; Mapa-geo; Oficial GeoSampa) — 162 datasets shapefile, ~0,7–0,8 GB:

   - 96 conjuntos SIRGAS_SHP_LOTES_01..96_<DISTRITO> — geometria de LOTES de todos os 96 distritos de SP. (Núcleo cadastral-geográfico.)

   - 7 conjuntos ZEPEC (APC, APP, APP-BIR, AUE, AUE_INDIC, BIR, BIR_INDIC) — elegibilidade de TDC.

   - Camadas-chave: SIRGAS_SHP_quadraMDSF (.shp 82,7 MB), logradouronbl (.dbf 76,8 MB), benstombados (.dbf 41,6 MB), setorfiscal (chave p/ IPTU), hidrolinha, PLANO_DIRETOR_DRENAGEM, cota_solidariedade, requalifica_centro; zoneamento PDE/LPUOS completo (ZEIS, ZEU, ZEPAM, ZC, ZM, ZPI...).

   - GeoPackage area_potencial_e_suspeita_de_contaminacao.gpkg (passivo ambiental); KML CETESB áreas contaminadas; layer_geosampa_apas.gpkg.

  Mapas em PDF pesados (pasta PDF de POTENCIAL URBANO ATUAL): Mapa1_ZONAS_com_perimetros_vetados.pdf (90,7 MB), Mapa03_QUOTA.pdf (40,2 MB), Mapas 1 a 9.pdf, Mapa02_ZEPEC.pdf, MAPA Lei 18081.

  DERIVADOS-IA (pasta "Criados"): LOTES_Parte_1..5_IA.csv (84–99 MB cada), ZONEAMENTO_IA.csv (41 MB), RUAS_Consolidado_IA.csv (64 MB), PCA_Consolidado_IA.csv, DIVERSOS_IA.csv — extrações dos shapefiles em CSV para a IA.

  DUPLICAÇÃO: o acervo geo existe em ≥2 árvores (POTENCIAL URBANO ATUAL/MAPAS e Documentos Novos/MAPAS/dados_pericia3+4), com fragmentação .cpg deslocada para pastas PDF.

----- EIXO E — ENRIQUECIMENTO E DESCOBERTA DE PROPRIETÁRIO -----

  (Função crítica do negócio: a partir do imóvel, achar o DONO para abordar.)

  - socios.csv (3,44 GB) — quadro societário de empresas (Receita Federal). Cópias: dados_pericia5 (1Lffz6w6OvS-5KqakDT71ZqIzsudRLnoI) E POTENCIAL URBANO ATUAL/Não Oficiais (1ncSTA-P2GfV2cPN-y1f2cnjqFDGSqa9e).

  - empresas.csv (2,27 GB) — cadastro CNPJ. Cópias: 18Q-_8iD5ZihVh-UnmD4itZ8WEa19g02a e 1u0ZaQCqfG0Moq2eroL-8_E1njnHJbgP5.

  - holdings.csv (60 MB) — holdings/controle (1lBfWs1FCsxCTgpAu_5WzbZJ8WnLodxi9 / 1LGUIQysj-1_8deN8AeQi5ChwORjyoWHR).

  - iptu-2020-cep01.csv (153 MB) — IPTU 2020 por CEP (~8 cópias).

  - IPTU_2026.csv (≈900–938 MB) — cadastro IPTU integral por SQL (contribuinte/endereço). ~7 cópias (937,9 MB em IPTU 12-05 1A3NK8K6...; 894 MB em XLS1 1EubfSLt...; etc.).

  - Série GUIAS DE ITBI PAGAS 2006–2024 (~22 xlsx, 14–47 MB) — transmissões: transmitente/adquirente/valor/SQL (descoberta de proprietário PF). Pasta XLS1.

  - Planilhas autorais consolidadas (pasta "Criados"): MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2.csv, PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv, MEGA_PLANILHA_SANEADA_TOMBADOS_V1.csv, DEEP_SCAN_SILVER_MOTOR1.csv, BASE_AUDIT_FINAL_CONSOLIDADA_V19.csv.

  CADEIA DE DESCOBERTA: SQL/imóvel (IPTU_2026) → contribuinte/CNPJ → empresas.csv → socios.csv → holdings.csv → pessoa física controladora. ITBI confirma transações recentes.

  IMPORTANTE: a pasta "DADOS CADASTRAIS" está VAZIA — não há base curada de descoberta de proprietário; ela existe apenas como matéria-prima bruta a cruzar.

----- EIXO F — DADOS OPERACIONAIS OFICIAIS DE TDC -----

  - TDC OFICIAL (Sheet 1,7 MB; 1QmHE2DSV7_5iosTo7JDrtwAUnUf0VM89b2ViCjHDFNI) — BASE-MESTRE: merge IPTU×ZEPEC (SQL, CODLOG, área, valor/m², nº do contribuinte, bp_zepec, processos de tombamento).

  - fila_tdc_5porcento_fundurb_dez_2025 e -2026-fevereiro (Oficial; pdf/csv) — fila FUNDURB, backlog R$42,19M (argumento de iliquidez ~133 dias).

  - Declaração de Potencial Construtivo / Certidão de Transferência (SMUL) — formulários/normas oficiais (~22 e ~11 cópias).

  - Certidoes (40 × CertidaoDigital_*.pdf) — certidões digitais (1R_j2KeVkI4tnxUKsekjC6xnFvM6n3aYP).

  - oo_2014-2023.xlsx (Outorga Onerosa), MASTER_PARAMETROS_URBANISTICOS.xlsx.

----- EIXO G — COMERCIAL / CONTRATOS / CRM -----

  - Comissão PU (Sheet; 1gqifq9iiZab1hEn8PLhImVXa5qH_Xy_izbd1QcSgwlk) — CRM de clientes reais + tabela de comissões + simuladores IPTU/TDC. (Contém nota: "O Sírio pediu pra esperar... até o fim da CPI do TDC".)

  - Contrato de Parceria - TDC Revisada (1mA67L8RO01a3F8w7mTXFE7V1sZdXFb02Fm4qdo_dgqE) — Bairro Vivo × Carlos Eduardo Braga; + Contrato de Gestão Comercial (V1/V2); Análise_CONTRATO_Sírio (OPIT).

  - Levantamento Preliminar TDC (Google Form) + Forms TDC Preliminar; Formulário para levantamento de IPTU.docx.

  - ICP-POTENCIAL URBANO, RQG-Potencial Urbano, Anotações Gemini.

  - Projeto Olga de Sá (restauro Solar Conde de M. Lima — orçamento + zips); apresentações OPIT/patrocínio.

----- EIXO H — MEMORIAIS / AUDITORIAS (a pesquisa profunda) -----

  - Auditoria TDC SP: Memorial de Fundamentação Estratégica (1VM5iOyzkVSiQxqjp1O8t6c3EzfdYYNlPKYXgqHWeObk) — memória de cálculo do motor (fórmula BIR, travas Art.24, "pulo do gato" do Fp, ágio de 30%).

  - Auditoria TDC SP: Stress-Test Metodologia (1cNAFJ2_bk1umCCEzni7ZJfkYSNVbDufcVmoJRtLOywA) — auditoria adversarial; aponta inclusão de ZEPEC-APC.

  - Validação Memorial Técnico TDC SP (1QyrOayOt5AeNxaw3nUytdRlFgBxQfJ9KN8Soa_vdXkQ) — valida 3.821 ativos (~R$3,1 bi teórico); protocolo SQL_LIMPO; sistema de Selos.

  - Auditoria TDC V8.0/V9.0: Relatório de Profundidade (1hY7I4CMKiKkN0RhQMSwIJ7WvChg_6RruSbR3ayr6cEw) — 3 gaps 2026: preço +7,18% (R$2.352,06/m²), colapso de liquidez FUNDURB, falsos-positivos (tombamentos arquivados).

  - Imóveis Tombados e Elegíveis para TDC (1gS2rONEUKB_0npohXGmnPtNpjB_OkorOuU5bj6gSjLM) — inteligência de mercado dos 2.011 tombados.

  - Análise e Correção de Dados TDC (1zF0dKxP3AmeYgsuFKHZlgaO4hFg3eyTwz99oklWPmZs) — auditoria forense do CSV.

==================================================================

4. MAPA DE DUPLICAÇÃO E SANEAMENTO

==================================================================

Estrutura: 2 árvores-espelho de "data lake" (DataLake_TDC e TODOS TDC), arquitetura medalhão (Bronze/Silver/Gold) replicada, + 3 lixeiras (99_LIXEIRA_DUPLICADOS, 99_QUARENTENA, 99_PARA_DELETAR), + re-upload triplicado de legislação no AI Studio, + fragmentos _PART_/_Pagina_ de ingestão.

Clusters de duplicação (cópias → 1 original):

  - "Memorial de Fundamentação Estratégica": ~15–36 cópias (pdf/csv/md/doc) → 1 Google Doc (1VM5iOyz...).

  - "fila_tdc_5porcento_fundurb": ~26 cópias → 1 pdf+csv oficial.

  - "manifesto_data_lake_tdc.json": ~11–21 cópias → 1 Google Doc.

  - "GatewayCertificaPDF/GatewayPDF": ~55 cópias → 1–2 PDFs originais.

  - Legislação no AI Studio: ~28 leis × 3 uploads = ~57 PDFs redundantes.

Desperdício de espaço (maior ganho rápido):

  - socios.csv 3,44 GB × 2 cópias ≈ 6,9 GB.

  - empresas.csv 2,27 GB × 2 ≈ 4,5 GB.

  - IPTU_2026.csv ~0,9 GB × ~7 ≈ 6,5 GB.

  - iptu-2020-cep01.csv 153 MB × ~8.

  TOTAL recuperável estimado: 15–20+ GB consolidando cada base pesada em 1 cópia.

Pastas a colapsar (após triagem): escolher UMA árvore canônica entre DataLake_TDC e TODOS TDC; esvaziar as 3 lixeiras; remover MOTOR_1_Markdown_Limpo, 00_TABELAS_EXTRAIDAS, PASTA UNICA. PRESERVAR a camada 02_SILVER_STAGED (única com taxonomia temática).

VACINA (não apagar às cegas): dentro das lixeiras há SHAPEFILES/GPKG que podem ser geodados únicos — triar antes. Filtro por NOME subconta proprietário/CPF/CNPJ (estão DENTRO de IPTU_2026/ITBI/OUTORGA, sem dizer no título) — tratar como candidatos de enriquecimento.

==================================================================

5. PONTOS CEGOS DECLARADOS (D24)

==================================================================

  - Sem SSOT declarado do "cérebro" TDC (múltiplos codex/manifestos paralelos).

  - Inteligência operacional (Gems/prompts) vive no AI Studio, fora do git — risco de continuidade.

  - Pasta "DADOS CADASTRAIS" vazia: a descoberta de proprietário não está materializada como base curada.

  - Arquivos pesados (IPTU_2026 938 MB; socios 3,44 GB; Livros Mestres .md 55 MB) NÃO tiveram conteúdo amostrado — enumerados, não lidos.

  - Dentro de IPTU-Sergio há subpastas com owner sergio.finger@potencialurbano.com.br (terceiro dentro de pasta sua).

  - Há material relevante em "compartilhados comigo" (ex.: PROSPECCAO_TDC_MULTI_CHAVES.xlsx, owner atendimento@potencialurbano) — fora do escopo "meus arquivos" desta rodada.

==================================================================

6. ESTRATÉGIA DE TRATAMENTO E TRABALHO (recomendação faseada)

==================================================================

Princípio (D26/D27): destravar a esteira e ARRUMAR antes de avançar. Mede-se por bloqueio removido, não por documento produzido.

FASE 0 — DECIDIR O SSOT (1 sessão). Escolher a árvore canônica única e o doc-mestre canônico de cada tema (recomendado: Mestre IPTU para IPTU; e CONSOLIDAR um único "CODEX TDC" a partir de CODEX_TDC_MASTER + Holding + Memoriais). Sem isso, todo saneamento é cego.

FASE 1 — SANEAMENTO PESADO (ganho rápido, baixo risco). Consolidar cada base pesada (socios/empresas/holdings/IPTU_2026/ITBI) em 1 cópia canônica; triar geodados nas lixeiras; arquivar as cópias. Recupera 15–20+ GB e dá clareza. (Requer sua autorização para EXCLUIR — por padrão só movo para uma pasta "_ARQUIVO_SANEAMENTO".)

FASE 2 — INVENTÁRIO VIVO + TAXONOMIA. Criar a estrutura curada única por EIXO (A–H deste doc) e um índice mestre (este Doc vira o índice). Migrar 02_SILVER_STAGED para essa taxonomia.

FASE 3 — VERSIONAR A INTELIGÊNCIA. Tirar Gems/prompts/.md/.json do AI Studio e colocá-los sob git (repo potencial-urbano) — destrava o ponto cego de continuidade.

FASE 4 — PIPELINE DE DESCOBERTA DE PROPRIETÁRIO. Materializar a base curada (hoje vazia em DADOS CADASTRAIS): cruzar IPTU_2026 → empresas → socios → holdings + ITBI, gerando uma planilha enriquecida única (substituindo as MEGA_PLANILHA_* dispersas).

FASE 5 — ATUALIZAÇÃO REGULATÓRIA. Incorporar os gaps do V9.0 (preço +7,18% R$2.352,06/m²; tombamentos arquivados; iliquidez FUNDURB) ao motor e à base TDC OFICIAL.

==================================================================

7. DECISÕES PENDENTES (perguntas ao MOU) — ver chat

==================================================================

(1) Foco primário do trabalho agora: TDC operacional, IPTU contencioso, ou saneamento/organização primeiro?

(2) Saneamento: autoriza EXCLUIR duplicatas pesadas, ou só MOVER para "_ARQUIVO_SANEAMENTO"?

(3) Versionar a inteligência (Gems/motores) no git do Potencial Urbano?

(4) Incluir na próxima rodada os arquivos "compartilhados comigo" (PROSPECCAO_TDC_MULTI_CHAVES etc.)?
