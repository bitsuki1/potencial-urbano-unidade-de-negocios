# INVENTÁRIO TOTAL (D24) E MAPA DE LACUNAS — Despejo Drive "Potencial Urbano" (RAG IPTU + TDC / SP)

> **⚠️ SUPERADO EM PARTE (2026-07-03).** A estrutura de Drive descrita aqui NÃO existe mais (a árvore foi achatada — ver PROXIMA §P1). Para fontes atuais use `docs/INVENTARIO-DRIVE.md` (proveniência, D-DONO-4). Mantido pelo valor histórico dos fileIds/lacunas. _(banner lavrado pela PU 17.)_

> **Autor:** Inventariante do Escritório do MOU (PMO). **Data:** 2026-06-18.
> **Fonte:** Google Drive — raiz "01 — _entrada (despejo IPTU+TDC)" (id `1grhqYgttj7KnJmiu9U73z-lXFHnFthov`).
> **Método:** enumeração recursiva via MCP Google Drive (`search_files` por `parentId`, `read_file_content`
> nos arquivos autorais pequenos). Doutrina D24: **nada fica de fora** — toda pasta foi percorrida e todo
> arquivo enumerado. Onde a contagem é massiva (shapefiles, resoluções de tombamento), o manifesto registra
> a **camada agregada + os ativos nomeados**, com contagem exata e id de pasta, em vez de repetir centenas de
> componentes `.shx/.dbf/.cpg` linha a linha (esses são partes do MESMO shapefile; o `.shp` é o ativo).
>
> **Registro dialético — honestidade total:** abri e li os arquivos AUTORAIS/estratégicos pequenos (oráculos,
> manifestos, Conhecimento Mestre, fila FUNDURB, catálogos). **NÃO** abri o conteúdo binário dos PDFs de lei,
> dos CSVs gigantes (LOTES/RUAS/ZONEAMENTO, dezenas de MB) nem dos shapefiles — classifiquei-os por
> nome/cabeçalho/contexto, como manda a missão. Onde classifiquei por nome, está marcado *(classif. p/ nome)*.

---

## ÁRVORE REAL DESCOBERTA (todas as pastas, com parentId)

```
01 — _entrada (despejo IPTU+TDC)                         1grhqYgttj7KnJmiu9U73z-lXFHnFthov   (raiz)
├── [60 arquivos .txt/.xlsx soltos na raiz — jurisprudência verbatim STF/STJ + logs]
└── Docs PU                                              1vUCvB3g8vS9yOHrkA5fYSgPurIwh2JtB
    ├── Criados   (oráculos + CSVs pesados + manifestos) 1oLLIkmfqndk2ydAWz0jTWIVbdeuhnDdP
    ├── Todos                                            14L9SKfQij93Jcn5yBmumBp5rCgieWm4-   (+ desktop.ini)
    │   ├── MAPAS                                        1DRBFdApeslDt3AYjsWFhNAGV605oMBe3
    │   │   ├── dados_pericia4  (shapefiles macro/QA)    1BYwp5biaJstdoYTeHdxie_VHACCh5zXN   (21 arq.)
    │   │   └── dados_pericia3  (shapefiles zoneamento)  1Lx3Fm5zAWIX3vK5u29GXuLL7q3whcx55   (300 arq.)
    │   ├── Não Oficiais                                 14fNoQeVi9_blLhEEme06ADJv5wqvjtyE
    │   │   └── dados_pericia5  (tombamento CONPRESP)    1mB_MUXiVuwJs7cCUjjRoeXWstlqcoxqH   (202 arq.)
    │   ├── Novos  (jurisprud./legisl. IPTU PDFs+txt)    16iEDW_3mJ0JFRCgG5x8avH8we8PUZwur   (60 arq.)
    │   ├── XLS1                                         1PFtt1W7JxhMFSU-wfgUJPnL4YLgveDTX
    │   │   └── dados_pericia8  (planilhas SISSEL/QA/OO) 1aUO5U2vSTQNZg-7HYWBu_eKBNXL-l7FX   (~74 arq.)
    │   ├── IPTU                                         1vinWI1b6mXE5V2vaTb1X6-GVgdAHsZBs   (+ desktop.ini)
    │   │   ├── dados_pericia2  (leis/decretos IPTU SP)  1Obz4gMpQMEM13CWjed3C5zSV3wameuum   (10 arq.)
    │   │   └── dados_pericia1  (leis IPTU + NBR/SUREM)  1E1PfwwMEvXaG8ZloKlz-aAObuP0nEfKT   (18 arq.)
    │   └── PDF                                          1xclAZmtrnKst_cAz9BPIKjDQUGSZ8glN   (+ desktop.ini)
    │       ├── dados_pericia6  (corpus legisl. verbatim)1tZf44hRLO7VYVC8KrzCBEoIFrNDf7ft-   (~265 arq.)
    │       └── dados_pericia7  (VAZIA)                  1-71yaHAuvefnKUzc2h0RRSTB_m-n7-Kw   (0 arq.)
    └── Zip  (9 zips = espelho comprimido de pericia1-9) 14QPJ2tZk_PZxq13lv9L_MI6U73GplWD2   (9 zips)
```

**Nota de duplicação (VACINA):** as pastas `dados_periciaN` são a versão DESCOMPACTADA dos 9 zips em `/Zip`.
Os zips somam ~3,2 GB e são **espelho** do que já está expandido — não há informação nova neles, exceto que
`dados_pericia9.zip` (40 MB) não tem pasta expandida correspondente visível (ver Lacuna técnica). Tratar os
zips como BACKUP/DUPLICADO, salvo o pericia9 que precisa ser aberto uma vez para confirmar conteúdo.

---

## A) MANIFESTO COMPLETO (D24)

Legenda de BALDES: **(1)** Corpus Jurídico · **(2)** Insumo de Precificação · **(3)** Descoberta de
Proprietário/Clientes · **(4)** Operacional TDC · **(A)** Autoral/Motor de IA · **(L)** Lixo/Duplicado/Técnico.

### A.1 — Raiz do despejo (id `1grhqYgttj7KnJmiu9U73z-lXFHnFthov`) — 60 arquivos

Captura **verbatim de jurisprudência** (STF + STJ), gerada por extração de tela 2026-06-18. Todos `.txt` pequenos.

| Conjunto | Arquivos | Balde |
|---|---|---|
| STF Súmulas (verbatim): sumula-539, 589, 668, 670, 724, SV-19 — c/ duplicatas (1)-(5) | ~16 `.txt` | (1) |
| STF Temas (verbatim): tema-94, 155, 523, 1020, 1084 — c/ duplicatas (1)(2) | ~15 `.txt` | (1) |
| STJ Súmulas (verbatim): 314, 392, 393, 397, 399, 409, 481, 614, 626 | 9 `.txt` | (1) |
| STJ REsp (verbatim): 1112646, 1130545, 1202136, 1645832, 1658054 | 5 `.txt` | (1) |
| STJ Temas (verbatim): 174, 262, 399, 566, 1113, 1158, 1350 (prefixo `IPTU-TDC_`) | ~9 `.txt` | (1) |
| Logs de extração: "Todos os 12 arquivos baixados", "Extração concluída 11/14", "7 páginas renderizaram", `test-download.txt` (12 B) | 5 `.txt` | (L) |
| `Notas Nilson Grotti.xlsx` (20 KB) *(classif. p/ nome — planilha pessoal/contábil)* | 1 `.xlsx` | (3?/L) |

> **Confirma o contexto da missão:** a captura verbatim de **jurisprudência STF/STJ JÁ ESTÁ no despejo** (corpus-alvo
> de 32 itens). Os textos verbatim de LEI federal/municipal **não estão soltos na raiz** — estão nos PDFs de
> `dados_pericia6/2/1` (ver A.7/A.5).

### A.2 — Docs PU / **Criados** (id `1oLLIkmfqndk2ydAWz0jTWIVbdeuhnDdP`) — oráculos + CSVs pesados

**Autoral / Motor de IA (A)** — LIDOS verbatim nesta sessão:

| Título | Ext | Tamanho | id | Balde |
|---|---|---|---|---|
| CONHECIMENTO_MESTRE_IA_V3.1_INABALAVEL.md (a "bíblia" do projeto TDC: fórmula OO, Fs/Fp, regra 5% FUNDURB) | md | 1.864 | `1uFZSNRSsgT3Q28dbCJBkPQ51us20L5wp` | A |
| CONHECIMENTO_MESTRE_IA_V3.md (pilar jurídico: 6 estratégias de TDC, OODC) | md | 1.634 | `1nxcd_gfrJvZw61T9FzZT_9zCsvZIUU2m` | A |
| ORACULO_MESTRE_RELACIONAL_V4.md (chaves de JOIN do RAG: SQ=setor+quadra→Valor; ZONA→CA_max; PA→QA) | md | 1.405 | `1OlwxW02z7ilpnXDXoMLpyYeX2Yp-4DtB` | A |
| ORACULO_GEOGRAFICO_DEFINITIVO_V3.md | md | 27.249 | `1P7rW4oWEKPH1OSFpl8TJMrHzHlWdQh4l` | A |
| HIERARQUIA_DE_FONTES_ORACULO.md | md | 242.416 | `1u-IT0cIljHaK56AeRdRzyScXqhkU7uei` | A |
| MANIFESTO_PLATINA_FINAL.md | md | 897.588 | `1c87YpNg_STYzyTZkVtKAk9fqwl_LCre6` | A |
| MANIFESTO_TOTAL_DE_TRANSICAO.md | md | 425.624 | `1e7jZj21Ym8ETr9s2MTx1qRqisycAOto5` | A |
| MANIFESTO_AUDITORIA_PROJETO.md | md | 127.320 | `1jYS_0D3Jw5u6fUFmXz4964VMiRXb1Ki-` | A |
| MASTER_RITOS_E_PROCEDIMENTOS.md | md | 25.841 | `13fO9nEVc1q4erd70-OBu5M5WnFpSljdn` | A |
| MOTOR_3_CATALOGO_ESPACIAL.md | md | 24.934 | `1tb0Au3qmaNL5oAcgOj2IfyUtHhGBngGn` | A |
| ESTRUTURA_SILVER_IA.md (arquitetura RAG bronze/silver — lida; ver síntese) | md | 1.950 | `1GFWoQdXB1TYiA1jOiU1l6hdzjz-lI7Sm` | A |
| RELATORIO_DUPLICADOS_FORENSE.md | md | 844.022 | `1GIuNnePe56CoakybNwRgfpKXN1CcLQO3` | A/L |
| RELATORIO_INTEGRIDADE_MAPAS_FINAL.md | md | 52.983 | `1V2iJMUbGueWMxqU5Eiwfo93OZREvWhtT` | A |
| CONCLUSAO_FASE_DADOS_PERFEITOS.md / CONHECIMENTO...V3.1 (curtos de status) | md | <500 | `1I__PKu...` | A |
| MANUAL DE PADRONIZAÇÃO TÉCNICA - RAG PIPELINE.pdf | pdf | 39.538 | `1vUakYl5y-ca_5obRdcVDN0RHf61sfZu3` | A |
| GUIA DE ESTRUTURA DE PASTAS - GOOGLE DRIVE.pdf | pdf | 33.267 | `1ls2BElzKwT_BLIrcLN-rJM1eYCiNDx6f` | A |
| documento_final_ia.pdf (anulado pelo Conhecimento Mestre V3.1, mas presente) | pdf | 34.017.047 | `1ts_G8HnvfKXTnWvuMcBYDgh0vMu7Zf-e` | A |
| manifesto_datalake / datalake_delta_load / log_extracao_textual_silver (JSON de catálogo do pipeline) | json | 476 KB / 3 KB / 162 B | `1sWKyzs...`,`1k7Vfx...`,`1O4WE...` | A/L |

**Insumo de Precificação (2)** — CSVs/planilhas (classif. p/ nome+cabeçalho):

| Título | Ext | Tamanho | id |
|---|---|---|---|
| MASTER_PARAMETROS_URBANISTICOS.xlsx (parâmetros construtivos consolidados) | xlsx | 201.868 | `1ZcgJAkqOnfS2DN0B2v4oHZbM-O8PeMfb` |
| ZONEAMENTO_IA.csv (zoneamento p/ RAG) | csv | 40.975.342 | `1-MYMZOBWvQrPC3TVyIbUB8kpGgArEpV9` |
| RUAS_Consolidado_IA.csv | csv | 63.601.704 | `1-kcIEA95aNukql6hwu5Hcmd7gEMlshkY` |
| LOTES_Parte_1..5_IA.csv (cadastro de lotes — 5 partes) | csv | ~84–99 MB cada | `1tKyGmF...`,`1tuY-boT...`,`1qOgBD1...`,`1tlQFci...`,`1tLK-nqs...` |
| PCA_Consolidado_IA.csv (Plano de Controle Ambiental / cantos) | csv | 22.342.771 | `1ihfczQ7V9lX0BnG2a7006i2eM7eylW5E` |
| DIVERSOS_IA.csv | csv | 32.676.280 | `1tpnksWulcTtEsoKpUWkONfuAQWsUfcP7` |
| PDE2013_SUBST2_Quadro_1..14_*.csv (Quadros do PDE: CA, Fp, Fs, ZEIS, eixos, macroáreas, parques, equip., viário, **Quadro_14_cadastro** = valores) | csv | 285 B – 5,4 MB | vários (ver lista PDF em A.7) |
| 001..012 - QUADRO_*_FINAL.csv (Quadros LPUOS finais: glossário, CA por zona, QA) | csv | ~700 B – 31 KB | `1oS1M4iS...` etc. |
| MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2.csv / MEGA_PLANILHA_SANEADA_TOMBADOS_V1.csv | csv | 2,8 / 2,7 MB | `1rAqJJ9...`,`1BzjO9G...` |
| Auditoria TDC São Paulo_ Memorial de Fundamentação Estratégica.csv | csv | 1.092 | `10hYtSTidTjmVtzWVq-KyzjmVqKTaYyeg` |
| DEEP_SCAN_BRONZE_ORIGINAIS.csv / DEEP_SCAN_SILVER_MOTOR1.csv / AUDITORIA_1/2 (4 B = vazios) | csv | 62 KB / 33 KB / 4 B | `1RKhYw...` etc. |
| layer_geosampa_apas.gpkg (APAs GeoSampa) | gpkg | 270.336 | `1mYElHzwo9ohQ5sYeNuruu_QTTLwp70oo` |

**Descoberta de Proprietário / Cliente (3)** — o ativo mais valioso deste subgrupo:

| Título | Ext | Tamanho | id | Nota |
|---|---|---|---|---|
| **PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv** | csv | 2.968.042 | `1EhyUwdnBGfv1ztWIo2us_Ym1B1do1oGK` | guias de ITBI já enriquecidas (transações = quem comprou/vendeu) |

### A.3 — MAPAS / dados_pericia4 (id `1BYwp5biaJstdoYTeHdxie_VHACCh5zXN`) — 21 arq. — **Balde (2)**

Shapefiles macro/temáticos. Camadas `.shp` distintas (cada uma acompanha `.dbf/.shx`):
`SIRGAS_SHP_LOTES_*` (Vila Medeiros 92, Tucuruvi 82, Tremembé 81, Sapopemba 76, Santana 70, Sacomã 68,
Pirituba 63, Jabaquara 38, Itaim Paulista 36, Grajaú 30, Freguesia do Ó 29, Cidade Ademar 22, Brasilândia 11),
`SIRGAS_SHP_logradouronbl` (logradouros), `SIRGAS_SHP_hidrolinha`, `SIRGAS_SHP_benstombados` (DBF tombados),
`QA.shp` (Quota Ambiental), `PCA_CANT.shp`, `area_potencial_e_suspeita_de_contaminacao.xlsx.gpkg` (CETESB).

### A.4 — MAPAS / dados_pericia3 (id `1Lx3Fm5zAWIX3vK5u29GXuLL7q3whcx55`) — **300 arq.** — **Balde (2)**

Camada cadastral/zoneamento completa. **135 base-names de camada distintos** (derivados de todos os componentes),
mas **componente-incompleto:** 135 `.shx` × só **31 `.shp`** × 130 `.dbf` × apenas 3 `.prj` — ou seja, **a maioria
das camadas está SEM a geometria `.shp` e/ou sem projeção `.prj`** (ver Lacuna técnica T-5, gap de integridade real,
não erro de contagem). + 1 `.kml` (`datageo-VWM_AREAS_CONTAMINADAS_GEODADOS_CETESB_PTO.kml`, id
`1Eo2WayCA_GKxh8a7jdDqynB10kO77-p1`). Camadas distintas: **SIRGAS_SHP_LOTES_01..96 — TODOS os 96 distritos da
cidade (Água Rasa→Lajeado), cadastro de lotes da cidade inteira**; `SIRGAS_SHP_setorfiscal`,
`SIRGAS_SHP_quadraMDSF`, `SIRGAS_SHP_zeup_zemp`, `SIRGAS_SHP_requalifica_centro`, `SIRGAS_SHP_PLANO_DIRETOR_DRENAGEM`,
`SIRGAS_SHP_baciahidro/hidrolinha`, `SIRGAS_SHP_cota_solidariedade`, `SIRGAS_SHP_subvencao_economica`,
`SIRGAS_SHP_benstombados`, `SAD69-96_SHP_planoacao/planomacro/restricaomirantesantana`, e o **zoneamento LPUOS
completo** `ZER_a/ZER_2, ZEU_a/u, ZEUP_a/u, ZM_a/u, ZMIS_a/u, ZOE, ZPDS_r/u, ZPI_1/2, ZPR` + perímetros
**ZEPEC_APC / APP / APP-BIR / AUE / AUE_INDIC / BIR / BIR_INDIC** (preservação cultural).

### A.5 — IPTU / dados_pericia1 (id `1E1PfwwMEvXaG8ZloKlz-aAObuP0nEfKT`) — 18 arq. — **Baldes (1)+(2)**

**LEIS/DECRETOS MUNICIPAIS DE IPTU — TEXTO VERBATIM (PDF):**
LEI 11.308/1992; LEI 13.776/2004; LEI 14.089/2005; LEI 17.719/2021 (+ Anexo I e Anexo III + Tabela kWh×R\$);
Anexo I da LEI 15.889/2013; DECRETO 52.884/2011; DECRETO 57.770/2017; INs SF/SUREM nº 2, 10 e 14/2019-2020
(base de cálculo IPTU). **Técnico de precificação:** `NBR14653-2_IMVEIS_URBANOS.pdf` (norma de avaliação),
`MON.pdf`. **Jurisprud./atos:** ARQUIP/DOSP decisões; `20250000963993.pdf`.

### A.6 — IPTU / dados_pericia2 (id `1Obz4gMpQMEM13CWjed3C5zSV3wameuum`) — 10 arq. — **Balde (1)**

**LEIS/DECRETOS MUNICIPAIS IPTU — VERBATIM (PDF):** LEI 11.614/1994; LEI 13.698/2003; LEI 17.092/2019;
DECRETO 56.954/2016; DECRETO 58.592/2018; DECRETO 63.698/2024. + `stj-revista-sumulas-2010_cap Súmula 160`
(Súmula 160/STJ — majoração de IPTU por decreto), decisões DOSP. + desktop.ini (L).

### A.7 — PDF / dados_pericia6 (id `1tZf44hRLO7VYVC8KrzCBEoIFrNDf7ft-`) — **~265 arq.** — o CORPUS PRINCIPAL

Este é o **acervo verbatim mais valioso do despejo**. Inventário por sub-balde:

**(1) Corpus jurídico — LEIS FEDERAIS verbatim (PDF):** `L10257.pdf` (Estatuto da Cidade), `L6938.pdf`
(Política Nacional Meio Ambiente), `L12651.pdf` (Código Florestal), `Lei nº 11.428.pdf` (Mata Atlântica),
`Lcp 227.pdf`, `Portaria CAT 15 de 2003.pdf`.

**(1) Corpus jurídico — LEIS MUNICIPAIS SP verbatim (PDF, "Catálogo de Legislação Municipal"):**
**16.402** (LPUOS) [`LEI Nº 16.402.pdf` + `L16642`], **16.050/2014** (PDE) [`2014-07-31 - LEI 16050...pdf`],
**17.975/2023** (revisão PDE — eixos 700m), **18.222/2024** (Arco Pinheiros), **18.081/2024** (ZEU),
**18.177/2024**, **18.209/2024**, **18.298/2025**, **17.202/2019**, **17.217/2019**, **17.104/2019**,
**17.577/2021**, **17.733/2022**, **17.734/2022**, **17.844/2022**, **17.853/2022**, **15.044/2009**,
**15.150/2010**, **15.723/2013**, **16.642/2017**, **14.094/2005**, **11.154/1991** (IPTU!), e **DECRETOS**
57.299/57.443/57.521/57.536 (regulamento TDC/OODC)/57.565/57.776/58.028/58.094/58.176/58.707/58.955/59.163/
59.164/59.671/59.886/60.581/61.137/61.218/62.175/63.423/63.437/63.504/63.728/63.999/64.018, + `D57536.pdf`.

**(4) Operacional TDC — formulários e atos SMUL/DEUSO (PDF, verbatim das páginas de serviço):**
"Transferência do Direito de Construir", "Certidão de Transferência de Potencial Construtivo", "Declaração de
Potencial Construtivo Passível de Transferência", "Outorga Onerosa do Direito de Construir", "Certidão de Uso e
Ocupação do Solo", "Ativação de ZEUP/ZEMP", "Projeto de Intervenção Urbana", "Enquadramento CNAE", + INs/Portarias
SMUL (IN nº 1/2024, Portaria SMUL nº 8/2025 = Quadro 14, Portaria SMUL nº 172/2024), Resoluções CTLU/CEUSO/CAEHIS.
**Quadros do PDE em PDF** (Quadro_1..14: definições, CA eixos/macroáreas/ZEIS, Fp, Fs, parques, equip., drenagem).

**(4) Operacional TDC — estoque/fila FUNDURB:** **`fila_tdc_5porcento_fundurb-2026- fevereiro.pdf`**
(id `1dKRk9L2uPMz_9N9d3DSso1QBEEDqRHv9`, fila ATUALIZADA fev/2026), `fila_tdc_5porcento_fundurb_dez_2025-pdf.pdf`,
`FUNDURB_Balanco_Financeiro_Consolidado_01JAN_2026.pdf`, série `Balanco_Financeiro_01JAN..11NOV2025.pdf`,
`OUAguaBranca*Outorga*.pdf` (estoque OU Água Branca), `tabela_2025_Retificado_em_12-02-25.pdf`.

**(4) Operacional TDC — fonte de GERAÇÃO (tombamento, ~120 resoluções CONPRESP/CONSPRESP + RAEs CONDEPHAAT):**
dezenas de PDFs `NN-AA - APT/Tombamento/Registro ... - Página.pdf` e `AAAA_NN_*_RAE_*.pdf` — cada imóvel tombado
é um POTENCIAL CONSTRUTIVO transferível. `Resolucao 04/07 CONSPRESP 2023`, `Resolucao 01_22 CONPRESP`, mapas.

**(3) Descoberta de proprietário:** `dados de advogado.pdf`, `metadados smul.pdf`, `Requerimento DEUSO(1).pdf`,
`Portal de Serviços e-SAJ*.pdf` (consulta processual). `Cnae_X_Item_Lista_Servicos.pdf`.

**Quadros LPUOS em .doc/.docx/.pdf** (`1..12-QUADRO_*_FINAL`) — versões editáveis dos quadros de cálculo.
+ `desktop.ini` (L).

### A.8 — Não Oficiais / dados_pericia5 (id `1mB_MUXiVuwJs7cCUjjRoeXWstlqcoxqH`) — 202 arq. — **Balde (4)**

160 `.cpg` (5 B cada = só o codepage; **são stubs ÓRFÃOS — NÃO há `.shp/.shx/.dbf` que os acompanhe nesta pasta**;
os "160 nomes de camada" são nominais, não shapefiles utilizáveis → balde L). 7 `.docx` (Quadros 2..4B FINAL —
duplicata dos de pericia6) e **35 PDFs de tombamento/ZEPEC** (o payload real desta pasta) (APT Capela Dom Bosco, Terreiros de Candomblé, Escadarias Cristiano
Viana/Alves Guimarães, Sindicato Metroviários, Santa Marina A.C., Festa do Divino Freguesia do Ó, RAE Ramos de
Azevedo, ACÓRDÃO ADI 2187640 Arco Pinheiros, Anexos do D 57.536/2016, Balanços Financeiros FUNDURB jul-nov/2025,
OU Água Branca estoque/outorga, Resolução SMUL/CTLU nº 4/2024). Tudo (4) geração TDC + alguns (1).

### A.9 — Novos (id `16iEDW_3mJ0JFRCgG5x8avH8we8PUZwur`) — 60 arq. — **Baldes (1)+(2)**

Dossiê de **inteligência jurídica IPTU** (curado): `RELATORIO_INTELIGENCIA_TRIBUTARIA_IPTU.txt` (+v1/2026/(1))
— varredura ConJur/JOTA/Migalhas 36 meses sobre IPTU (imunidade concessões, IPTU retroativo, revisão de
lançamento, PGV Piracicaba, base de cálculo Harada/EC 132). PDFs de notícia correspondentes. **Acórdãos TJSP**
(1568276-30.2023, 2390222-33.2025 AI/ED, 1509864-53.2016 AC/ED, 1025594-05.2021, 1053798-54.2024, 1054600-28.2019),
`ARE_1216078_Acordao_Tema1062_STF.pdf`, `RESP-1949182-2025`, `RESP/downloadPeca`. **Leis municipais IPTU verbatim:**
`LEI 11.152/1991` (IPTU base), DECRETO 52.884/2011 (+Anexo Único), DECRETO 63.698/2024 (+Cópia, duplicata),
DECRETO 60.939/2021, Anexo III da Lei 15.889/2013, `Tabela VI - Tipos e padrões de construção - Lei 16768-2017.tgz`.
Teses/mineração: `MINERACAO_IPTU_SP_Teses_Impugnacao_Base_Calculo.txt`, `Pesquisa_*_IPTU_*.txt`,
`Sumulas_Vinculantes_*`, dissertações acadêmicas (UFC, PUCSP, Salvador, Campinas APP). `mover_pdfs_STJ.ps1` (L),
`Nova_test.txt`/`browse.pdf` (L). `ABNT.pdf`.

### A.10 — XLS1 / dados_pericia8 (id `1aUO5U2vSTQNZg-7HYWBu_eKBNXL-l7FX`) — ~74 arq. — **Baldes (2)+(4)+(3)**

**(2/4) Outorga Onerosa e simuladores:** `OODC_2024-2025.xlsx`, `oo_2002-2014.xlsx`, `oo_2014-2023.xlsx`,
`SIMULADOR_QA_atualizado_lei_18081_24_v4.xls`, `Ano_*_AD_*.xlsx` (Alvará Direto), `Aprova Digital_dez2020.xlsx`.
**(4) Fila/certidões TDC:** `fila_tdc_5porcento_fundurb_dez_2025-pdf.csv`, `lista_certidao_ZEPEC-BIR_agosto-2025.xlsx`,
`lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx`, `aceleracoes_proponentes.xlsx`, `Balanco_Financeiro_05MAI2025.ods`.
**(2) Ambiental/CETESB:** `area_potencial_e_suspeita_de_contaminacao.*` (xlsx/ods/csv/gpkg) + dicionários/metadados,
`geoportal_area_contaminada_reabilitada_svma.xlsx`. **(2) GeoSampa APAs** dicionários. **(2) Zoneamento/PDE:**
`ANEXOS_DO_PL_586_23.csv`, quadros SMUL csv (TDC, OODC, PIU, certidões), `catalogo_oficiais_para_preenchimento_*.csv`
(catálogo mestre dos shapefiles). **Série histórica de produção (SISSEL/Alvarás) `anual2004..2026`, `sissel_*`,
`Ano_2023..2026`** — *(classif. p/ nome: indicadores de licenciamento; valor (2) marginal)*. `ddf-12.25/01.26.xlsx`.

### A.11 — Zip (id `14QPJ2tZk_PZxq13lv9L_MI6U73GplWD2`) — 9 zips — **Balde (L) duplicado**

`dados_pericia1.zip` (110 MB) … `dados_pericia9.zip` (40 MB) — espelho comprimido. **`dados_pericia9.zip`
(40.402.986 B) é o único SEM pasta expandida** → conteúdo desconhecido (ver Lacuna técnica T-1).

---

## B) SÍNTESE POR BALDE — o que temos de bom

**(1) CORPUS JURÍDICO — FORTE.** Temos verbatim: (a) jurisprudência STF/STJ (súmulas, SV-19, temas, REsp) na
raiz; (b) **leis federais-chave em PDF** (Estatuto da Cidade 10.257, Cód. Florestal 12.651, PNMA 6.938, Mata
Atlântica 11.428); (c) **dezenas de leis e decretos municipais de SP em PDF** cobrindo IPTU (11.152/1991,
11.154/1991, 11.308/1992, 11.614/1994, 13.698/2003, 13.776/2004, 14.089/2005, 17.092/2019, 17.719/2021 +
decretos 52.884, 56.954, 57.770, 58.592, 63.698 + INs SUREM) E urbanismo/TDC (16.402 LPUOS, 16.050 PDE,
17.975, 18.081, 18.222 + ~25 decretos); (d) um **dossiê de inteligência jurídica curado** (ConJur/JOTA/Migalhas,
36 meses) + acórdãos TJSP/STF reais. Ativos-chave: `LEI Nº 16.402.pdf`, `2014-07-31 - LEI 16050.pdf`,
`L10257.pdf`, `LEI 11.152/1991`, `RELATORIO_INTELIGENCIA_TRIBUTARIA_IPTU.txt`, `Súmula 160/STJ` (revista STJ).

**(2) INSUMO DE PRECIFICAÇÃO — MUITO FORTE em base espacial; MÉDIO em valor venal oficial.** Temos: cadastro de
**LOTES da cidade inteira** (96 distritos em shapefile + 5 CSVs LOTES_Parte), zoneamento completo (ZER/ZEU/ZEPEC/
etc. em shp + ZONEAMENTO_IA.csv), todos os **Quadros do PDE e LPUOS** (CA, Fp, Fs, ZEIS, eixos, macroáreas) em
csv/pdf/docx, `MASTER_PARAMETROS_URBANISTICOS.xlsx`, GeoSampa APAs, CETESB contaminadas, QA/PCA. Ativos-chave:
`SIRGAS_SHP_LOTES_*` (pericia3), `PDE2013_SUBST2_Quadro_14_cadastro.csv` (= os **valores V** por SQ),
`005 - QUADRO_3_FINAL.csv` (CA por zona). **Porém o "Quadro 14" do despejo é o do PDE 2013** — ver lacuna L-2.

**(3) DESCOBERTA DE PROPRIETÁRIO / CLIENTES — FRACO/PARCIAL.** O único ativo direto é
**`PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv`** (2,9 MB — guias de ITBI enriquecidas = transações imobiliárias com
partes). `MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2.csv` e `..._TOMBADOS_V1.csv` provavelmente cruzam lote↔proprietário
de tombados (classif. p/ nome). `dados de advogado.pdf` e `metadados smul.pdf` são pontuais. **Não há base de
sócios/CNPJ/holdings, nem cadastro de contribuinte IPTU por SQL.**

**(4) OPERACIONAL TDC — MUITO FORTE.** Temos a base "TDC OFICIAL" inteira: formulários/certidões SMUL verbatim,
**fila FUNDURB 5% atualizada até fev/2026** (pdf+csv), balanços FUNDURB mensais 2025–jan/2026, listas de
certidões/declarações ZEPEC-BIR (ago/2025), simulador QA (lei 18.081/24), série OODC 2002–2025, e a **fonte de
geração**: ~120 resoluções CONPRESP/CONSPRESP + RAEs CONDEPHAAT (cada tombado = potencial transferível). Ativos-
chave: `fila_tdc_5porcento_fundurb-2026- fevereiro.pdf`, `lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx`,
`OODC_2024-2025.xlsx`, Decreto 57.536/2016 (rito).

**(A) AUTORAL / MOTOR DE IA — FORTE e ACIONÁVEL.** O `CONHECIMENTO_MESTRE_IA_V3.1` traz a **fórmula mestra**
`OO = (Área_Adicional / CA_max) · Fp · Fs · V`, os fatores Fs (HIS 0,0 / HMP 0,4–0,6 / R>70m² 1,0), Fp (eixos
1,2–1,3; qualificação 0,6) e a **regra dos 5% do FUNDURB** (art. 24 LPUOS). O `ORACULO_MESTRE_RELACIONAL_V4`
entrega as **chaves de JOIN do RAG**: SQ (setor 3 díg + quadra 3 díg) → Valor de terra (Quadro 14); ZONA → CA_max;
PA → pontuação QA. `ESTRUTURA_SILVER_IA` define a arquitetura bronze→silver com a contagem-alvo por domínio.

**(L) LIXO / DUPLICADO / TÉCNICO.** Os 9 zips (espelho), 160 `.cpg` (5 B), componentes `.shx/.dbf/.prj` isolados,
`test-download.txt`/`Nova_test.txt` (4–12 B), AUDITORIA_1/2 (4 B vazios), `desktop.ini` (×4), `mover_pdfs_STJ.ps1`,
duplicatas com sufixo `(1)(2)` e `- Copia`, logs de extração. `documento_final_ia.pdf` está **autoinvalidado**.

---

## C) MAPA DE LACUNAS (para um RAG de altíssimo nível)

### Balde (1) Corpus Jurídico
- **L-1.1 — Verbatim do texto articulado das leis federais ainda em STUB no repo.** O repo
  `leis/federal/*.md` está **status_pipeline=bruto** (só ementa; planalto.gov.br devolveu 403 in-session).
  **MAS o despejo já contém os PDFs verbatim** de várias (`L10257`, `L6938`, `L12651`, `Lei 11.428`).
  → *Onde conseguir:* **extrair texto desses PDFs do próprio despejo** (OCR/parse) e preencher os stubs.
  Para as federais sem PDF (CTN, CF art. 156/182/156-A, EC 29/116/132, DL 57/66, Leis 6.015, 6.830, 8.009,
  8.668, 9.514, 10.931, 11.101, 4.591): capturar de planalto.gov.br **fora deste ambiente** (a extensão de
  navegador do MOU consegue; o WebFetch da sessão não).
- **L-1.2 — Verbatim das leis MUNICIPAIS em stub.** Idem: os PDFs verbatim de 16.402, 16.050, 17.975, 18.081,
  18.222, 11.152, 11.154, 17.092, 17.719 etc. **já estão no despejo** (pericia6/1/2) → parsear e casar com os
  stubs `leis/municipal-sp/*`. Faltam conferir cobertura: 17.759/2022, 17.844, 13.250/2001, 13.475/2002,
  14.865/2008, 10.235/1986, 7.228/1968, 12.350/1997 (alguns presentes, outros não — auditar 1:1).
- **L-1.3 — Catálogo de Legislação Municipal como índice canônico.** Temos PDFs individuais, mas não o índice
  navegável. → *Onde:* `legislacao.prefeitura.sp.gov.br` (Catálogo) — capturável por extensão.
- **L-1.4 — Jurisprudência atualizada e íntegra dos acórdãos.** Temos ementas/notícias; faltam inteiros teores
  recentes (TJSP, STF Tema 1062/437, REsp recentes). → *Onde:* esaj/STF/STJ — capturável por extensão.

### Balde (2) Insumo de Precificação
- **L-2.1 — PLANTA GENÉRICA DE VALORES (PGV) OFICIAL VIGENTE 2026.** O despejo traz `PDE2013_SUBST2_Quadro_14`
  e `Atualizacacao_Q14_anoref2025` (citado no oráculo, **não localizado como arquivo** no despejo). Falta a PGV
  vigente do IPTU (Lei 10.235/86 e atualizações; valores do m² de terreno e construção por SQL/face de quadra).
  → *Onde:* Secretaria Municipal da Fazenda / Lei da PGV + anexos; GeoSampa "valor de m²". **Crítico p/ precificar.**
- **L-2.2 — Tabela de VALORES VENAIS / m² oficial casada por SQL.** Falta o cruzamento lote(SQL)→valor venal IPTU.
  → *Onde:* base de "valor venal de referência" SF-SP (publicada anualmente) + join pelo SQL de 10 dígitos.
- **L-2.3 — Quadro 14 do PDE/LPUOS **vigente** com preços reais 2025/2026** (o oráculo diz que a Portaria SMUL
  nº 8/2025 traz isso — o PDF `PORTARIA ... SMUL Nº 8 DE 30 DE JANEIRO DE 2025` ESTÁ no despejo). → parsear esse PDF.
- **L-2.4 — Shapefiles servidos como dados estruturados.** Estão em `.shp` cru (silver previu conversão p/ GeoJSON,
  status "aguardando extração"). → converter shp→GeoJSON/parquet e indexar; é trabalho, não falta de dado.
- **L-2.5 — Outorga onerosa / CA: parâmetros pós-18.081/2024 e 18.222/2024** consolidados (temos as leis e um
  simulador; falta a tabela final consolidada vigente). → derivar das leis já presentes.

### Balde (3) Descoberta de Proprietário / Clientes
- **L-3.1 — Base de PROPRIETÁRIOS por SQL (cadastro de contribuinte IPTU).** É a maior lacuna do balde. Temos
  lotes (geometria) mas não o NOME/CPF/CNPJ do proprietário por SQL. → *Onde:* não é dado aberto; obtém-se via
  guias de ITBI (parcial, já temos), consulta cadastral SF, ou enriquecimento. **MOU precisa subir do legado se
  existir base cadastral.**
- **L-3.2 — Base de SÓCIOS / EMPRESAS / HOLDINGS (Receita/CNPJ).** Ausente. → *Onde:* dados abertos CNPJ da
  Receita Federal (download em massa) + QSA; cruzar com proprietários PJ. Capturável por download, não por extensão.
- **L-3.3 — Guias de ITBI COMPLETAS (não só a amostra enriquecida).** Temos `PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2`.
  Falta a série histórica completa de ITBI. → *Onde:* SF-SP (ITBI) / portal de transparência; ou legado do MOU.
- **L-3.4 — Enriquecimento por CEP/endereço↔CPF/CNPJ.** Ausente. → serviço de enriquecimento externo.

### Balde (4) Operacional TDC
- **L-4.1 — Fila FUNDURB SEMPRE-ATUAL.** Temos até **fev/2026** (ótimo), mas é snapshot. → *Onde:* DEUSO/SMUL
  publica periodicamente — recapturar mensalmente por extensão.
- **L-4.2 — Base "TDC OFICIAL" de Declarações/Certidões COMPLETA e atual.** Temos listas ZEPEC-BIR ago/2025.
  → atualizar e completar (todas as vias de geração, não só BIR).
- **L-4.3 — Memoriais de potencial construtivo por imóvel tombado (cálculo já feito).** Temos as resoluções de
  tombamento (geração) mas não o memorial quantificado (m² transferível) por imóvel. → derivável (lote tombado ×
  CA × fatores) com os dados que já temos; é processamento.

### Lacunas técnicas / de integridade
- **T-1 — `dados_pericia9.zip` (40 MB) sem pasta expandida.** Conteúdo não enumerável sem abrir o zip. → abrir 1×.
- **T-2 — Arquivos referenciados pelos oráculos e NÃO encontrados no despejo:** `Atualizacacao_Q14_anoref2025.csv`
  (Valor V por SQ — citado no Oráculo V4) e os mapas 5/12 do PDE (hidro/drenagem) como tabela. → localizar/subir.
- **T-3 — CSVs de auditoria vazios (4 B)** e `documento_final_ia.pdf` autoinvalidado → descartar do RAG.
- **T-4 — Duplicação massiva** (zips × pastas; sufixos (1)(2); Copia) → deduplicar antes de ingerir (o próprio
  `RELATORIO_DUPLICADOS_FORENSE.md` já mapeia isso — usar).
- **T-5 — Shapefiles COMPONENTE-INCOMPLETOS em dados_pericia3.** 135 `.shx` mas só 31 `.shp` e 3 `.prj`: a maioria
  das camadas de zoneamento/perímetros **não tem a geometria `.shp`** (e quase nenhuma tem `.prj`). Os 96 LOTES e
  algumas camadas-base têm `.shp`; o zoneamento (ZER/ZEU/ZEPEC etc.) em grande parte **não**. → conferir no zip
  `dados_pericia3.zip` se as geometrias existem lá; senão, **rebaixar do GeoSampa** as camadas de zoneamento
  faltantes (download oficial, por extensão). Sem `.shp` + `.prj` a camada não georreferencia.
- **T-6 — `dados_pericia5` = 160 `.cpg` órfãos (sem geometria).** Não confundir com cobertura GIS: ali só há
  PDFs/docx úteis. Descartar os `.cpg` do RAG.

---

## D) LISTA DE COMPRAS PRIORIZADA (Top 15)

| # | O que buscar | Impacto | Caminho de obtenção |
|---|---|---|---|
| 1 | **PGV oficial vigente 2026 (valor m² terreno/construção por SQL)** | PRECIFICAR | Lei da PGV + anexos SF-SP / GeoSampa "valor venal"; capturar por extensão; senão legado MOU |
| 2 | **Parsear os PDFs de lei do despejo p/ preencher os stubs `leis/*` (verbatim)** | BLINDAR JURÍDICO | já no despejo (pericia6/1/2) — OCR/parse local; trabalho interno, custo zero de captura |
| 3 | **Base de proprietários por SQL (cadastro contribuinte IPTU)** | ACHAR PROPRIETÁRIO | SF-SP cadastral / legado MOU; não é dado aberto |
| 4 | **Dados abertos CNPJ Receita (sócios/QSA) p/ cruzar com proprietários PJ** | ACHAR PROPRIETÁRIO | download em massa Receita Federal; cruzar por CNPJ |
| 5 | **Quadro 14 vigente (Portaria SMUL 8/2025) — Valor V por SQ** | PRECIFICAR | parsear PDF já presente `PORTARIA...SMUL Nº 8...2025.pdf` |
| 6 | **Converter shapefiles LOTES/zoneamento → GeoJSON/parquet indexado** | PRECIFICAR | processamento dos `.shp` já presentes (pericia3/4) |
| 7 | **Série ITBI completa (não só amostra enriquecida)** | ACHAR PROPRIETÁRIO | SF-SP/ITBI ou legado MOU |
| 8 | **Verbatim leis federais sem PDF (CTN, CF, EC 29/116/132, DL 57/66 etc.)** | BLINDAR JURÍDICO | planalto.gov.br por extensão (sessão dá 403) |
| 9 | **Memorial de potencial construtivo por tombado (m² transferível)** | OPERAR TDC | derivar dos tombamentos + lotes já presentes |
| 10 | **Fila FUNDURB + Declarações/Certidões ZEPEC atualizadas (todas as vias)** | OPERAR TDC | DEUSO/SMUL por extensão (recorrente mensal) |
| 11 | **Catálogo de Legislação Municipal (índice canônico navegável)** | BLINDAR JURÍDICO | legislacao.prefeitura.sp.gov.br por extensão |
| 12 | **Inteiro teor dos acórdãos recentes (TJSP/STF Tema 1062/437; REsp 1949182)** | BLINDAR JURÍDICO | esaj/STF/STJ por extensão |
| 13 | **Abrir `dados_pericia9.zip` (40 MB) e enumerar conteúdo** | INTEGRIDADE | descompactar 1× e inventariar |
| 14 | **Localizar/subir `Atualizacacao_Q14_anoref2025.csv` (Valor V por SQ)** | PRECIFICAR | legado MOU (referenciado pelo Oráculo V4, ausente no despejo) |
| 15 | **Deduplicar acervo (usar `RELATORIO_DUPLICADOS_FORENSE.md`) antes de ingerir** | ESTEIRA/QUALIDADE | processamento interno |

---

### Nota de método e ressalvas (registro dialético)
- **TESE:** o despejo cobre muito bem (1) corpus jurídico, (2) base espacial e (4) operacional TDC; é fraco em (3).
- **ANTÍTESE:** não abri o interior dos PDFs/CSVs/SHP — classificações marcadas *(classif. p/ nome)* podem conter
  surpresas (ex.: alguma MEGA_PLANILHA pode já ter proprietários). A PGV vigente pode estar embutida num CSV grande
  não lido (ZONEAMENTO_IA/DIVERSOS_IA). O `dados_pericia9.zip` é ponto cego declarado.
- **CONCILIAÇÃO (provisória):** tratar este inventário como mapa de superfície fiel e completo em ENUMERAÇÃO (D24);
  a próxima passada deve ser de CONTEÚDO sobre os 5–6 CSVs grandes e o pericia9, antes de cravar lacunas do balde (2).
- **VACINA:** já se afirmou (no `documento_final_ia.pdf` e em "DADOS PERFEITOS") que a base estaria "perfeita/100%
  integrada"; isso está **errado** — o próprio `ESTRUTURA_SILVER_IA` admite "AGUARDANDO EXTRAÇÃO" e os stubs de lei
  seguem brutos. Não reafirmar "dados perfeitos": o que existe é matéria-prima rica, ainda não processada para RAG.
```

---

## RECONCILIAÇÃO COM O DRIVE COMPLETO (ativos fora do despejo) — adendo do maestro 2026-06-18

> O inventário acima é do DESPEJO (`01 — _entrada`). Vacina (escopo): vários ativos que o mapa de
> lacunas marcou como "ausentes" NÃO estão ausentes do **Drive** — estão fora da pasta de despejo,
> já localizados por busca direta. Registrados aqui com fileId para ficarem no radar (D24).

**Localizados no Drive (não precisam re-upload):**
- `socios.csv` — **3,43 GB** — id `1Lffz6w6OvS-5KqakDT71ZqIzsudRLnoI` (pasta `1gmAOmJUDxRf0HHi2ROSNz850FbUVX8h7`).
  → atende parcialmente a LACUNA #3 (sócios/CNPJ); ainda faltam `empresas.csv`/`holdings.csv`.
- `IPTU_2026.csv` — **937 MB** — id `1oX6BDTF_MJhrt8es4xh3N-cFtDbeoNGt` (pasta `1GvKF0ALRN_BITFwAvxjfgL-u-eRuOvtW`).
  → CANDIDATO à LACUNA #2 (base de proprietários/cadastro IPTU por SQL) — **verificar colunas** (SQL, contribuinte, valor venal) antes de cravar.
- Série **`GUIAS_DE_ITBI_PAGAS` 2006→2024** (12+ arquivos, ~15–46 MB cada) — mesma pasta `1GvKF0ALRN_…`.
  → transações reais = sinal de preço de mercado + descoberta de proprietário/adquirente.
- **FUNDURB**: `FUNDURB_Balanco_Financeiro_Consolidado_01JAN_2026.pdf` (id `106thxeqv30CMOrMX4Dlk1qo7k9YRTfAb`) e
  `fila_tdc_5porcento_fundurb` dez/2025 + fev/2026 (PDF e CSV) — pastas `1-71yaHAuvefnKUzc2h0RRSTB_m-n7-Kw` / `114dBRSf3NWspqQ-OQN3eyPd4gKsZbF74`.

**Lacunas que PERMANECEM reais após reconciliação:**
- #1 PGV / valor venal oficial vigente 2026 por SQL (não está no Drive — origem SF-SP).
- #3 `empresas.csv` e `holdings.csv` (Receita/CNPJ) — só `socios.csv` localizado.
- Núcleo do corpus IPTU: conferir se **Lei 6.989/66** (institui o IPTU) e **Lei 11.154/91** estão no corpus de 59 stubs — o despejo tem PDFs de leis IPTU (11.152/91, 11.154/91, 11.614/94) que podem NÃO estar mapeadas nos stubs.

---

## CORREÇÃO (vacina) — o que está REALMENTE confirmado nos PDFs de lei do despejo — 2026-06-18

> O 1º agente classificou os PDFs **pelo nome do arquivo, sem abrir** (declarou isso). Uma enumeração
> posterior, que PAGINOU as pastas de verdade, CONTRADIZ parte daquilo. Prevalece a paginada. Registro:
>
> - **dados_pericia6 NÃO contém os PDFs de LEI FEDERAL** (Estatuto da Cidade L10257, Cód. Florestal
>   L12651, PNMA L6938 etc.). A pasta é majoritariamente **shapefiles (.cpg/.shp) + resoluções de
>   tombamento + acórdãos + balanços**. A lista de leis federais atribuída a ela em A.7 é **NÃO
>   confirmada** (provável alucinação de filename). ⇒ os 12 stubs FEDERAIS seguem dependendo de captura.
> - **LEIS/DECRETOS MUNICIPAIS confirmados no despejo (fileId real, prontos para ingestão):**
>   - LEI 11.152/1991 (IPTU base) — `1IRnVuH0ANDCwT-9MZiLBNg0sBoOsz7Gf`  ← casa com stub `lei-municipal-saopaulo-11152-1991`
>   - LEI 11.308/1992 — `1piK-8O4ioRrg5tpyT5qxmBkqfSUll8sQ` (sem stub)
>   - LEI 11.614/1994 — `1j45B7yNJZaw7ZB7z_CCv2OXzCT_ZrfMy` (sem stub)
>   - LEI 13.698/2003 — `1Py3r3u5NHJXoR8H2AQHuyY0AqDwpAuKT` (sem stub)
>   - LEI 13.776/2004 — `1tppGK3DB9UnhbBvmnPnduxNb-YtwUh_s` (sem stub)
>   - LEI 14.089/2005 — `1Iw1V_L8S0rai6MjMcr7ATlUA3hCNi1hq` (sem stub)
>   - LEI 17.092/2019 — `1QGIIj8XlzC6ViMApn2yaNlfHeMOPogwP` (sem stub)
>   - DECRETOS: 52.884/2011 `15y2Lym2zh-NtoIX58sgk8teZ5ii9KrAA`; 56.954/2016 `1Rbzp_azDcvFRa9N7AQP_ROhtbqcWPHyT`;
>     57.770/2017 `1cibQb6DHglEQY7cBIJEhsl3dwAduD7lL`; 58.592/2018 `1XIQYL5O-wN_WZtIAhq_-auzxiopc_Kh2`;
>     60.939/2021 `1dJnKDR7YOddClqW0U2A6kV5LP0rtY6n8`; 63.698/2024 `1Fb760oZPAGRE7KL02s1ajQ1s0VSMx0OF`.
>   - Anexos/tabelas (não é corpo de lei): Anexo I/III da Lei 17.719/2021; Anexo I da Lei 15.889/2013;
>     INs SF/SUREM 2, 10, 14 (normas administrativas — úteis p/ base de cálculo IPTU).
> - **Dos 15 stubs municipais, só a 11.152/1991 tem PDF confirmado no despejo.** Os outros 14 seguem
>   dependendo de captura (Lotes 2). A 6.989/66 (institui o IPTU) **não foi vista** no despejo — buscar.

---

## WANT-LIST DO GARIMPO M6 (lente de oportunidade) — 2026-07-11

> Referências que o estudo M6 provou que **precisamos buscar** para converter oportunidade em condição melhor
> (preço/tese). Cada item aponta a oportunidade que destrava (ver `docs/OPORTUNIDADES-M6-TDC-IPTU.md`).

| Referência a buscar | Para quê (oportunidade) | Onde procurar | Prioridade |
|---|---|---|---|
| **`Atualizacao_Q14_anoref2026.csv`** (Quadro 14 exercício 2026) | **OP-1a**: aplicar +7,18% (Dec. 64.884/2025 + Portaria SMUL 8/2026) -> sobe o preco legal de todo cedente | SMUL/Storage (mesma fonte do recorte 2025, `zepec/pipeline/recorte_q14.py`) ou portal SMUL | **ALTA** |
| **Lei 17.975/2023** (texto) | **OP-1b**: o que alterou no Quadro 14 da Lei 16.050/2014 - base da tese "VTcd maximo rastreavel" | `legislacao.prefeitura.sp.gov.br` (`scripts/capturar_lei_portal.py`) | ALTA |
| **Resolucao CONPRESP 01/2025 e 03/2025** (SQLs arquivados) | **OP-2**: confirmar os 26 falso-positivos (quadra 013.036) e demais | Drive id `12UzO_2amXtVKmMm1gX_X82nLywiqWj0N` (01/2025) + DOC | ALTA |
| **Anexo I da Portaria SMUL 8/2025** (Doc. 117650623, 3.097 pag.) | valores nominais R$/m2 por face - so se o recorte exato do VTcd 2025 precisar de reconciliacao | Portal SMUL / DOC | MEDIA |
| **Lei 18.222/2024** (AIU-ACP / Arco Pinheiros) | **OP-5**: faixa/coeficiente de outorga super-tier no recorte | `legislacao.prefeitura.sp.gov.br` | MEDIA |
| Rito fiscal **CADIN/CND** no protocolo de TDC/OODC | **OP-6**: antecipar o portao fiscal (janela/opcao) | normas SF/SUREM + rito SMUL | BAIXA |
