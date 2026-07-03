# INVENTÁRIO DO GOOGLE DRIVE — Potencial Urbano (fontes oficiais)

> Levantado em 2026-07-03 por lentes sobre o Drive (leitura autorizada pelo dono; escrita CERCA suspensa na mesma data). Classificação por **proveniência** (OFICIAL / ADQUIRIDO / NOSSO-não-confiável, D-DONO-4) e mapeamento por motor. `fileId` de uma cópia canônica por ativo. Nada aqui é fonte antes de revisão humana do que for NOSSO.

---

# Inventário consolidado do Google Drive — Potencial Urbano (TDC / lado cedente, Só-tombado)

> Fonte: 2 buscas em disco (`mcp-Google_Drive-search_files-1783078181287/184646` — 200 registros) + 3 buscas de cobertura de lacuna feitas ao vivo pelo MCP do Drive (ZEPEC/listas, sócios/CNPJ, IPTU/LOTES csv). Owner de tudo: `eduardo@saobentoservicos.com.br`.
> Doutrina D-DONO-4 aplicada: só OFICIAL/ADQUIRIDO entra; o que o time produziu (`_IA`, docs de análise, planilhas-modelo) é marcado **NÃO-CONFIÁVEL** (não usar como fonte).
> "Uma cópia canônica" = a que está em `01 — _entrada` (folder `1grhqYgttj7...`) quando existe, pois é a zona de despejo oficial com o set de componentes completo e sem sufixo de hash.

## Mapa de pastas (id → título)
| parentId | título (inferido/confirmado) | papel |
|---|---|---|
| `1BrM6q36meTtn5guJoiGbqvCtZF11Uau3` | **raiz do projeto** (contém "01 — _entrada" e "05 — Geo") | diretório-mãe do TDC |
| `1grhqYgttj7KnJmiu9U73z-lXFHnFthov` | **01 — _entrada (despejo IPTU+TDC)** | ZONA DE DESPEJO / cópias canônicas oficiais |
| `1ds4u4ZpoLl_ySSIDywPbh_iicRCt6zNI` | pasta-mãe GEO (sob "05 — Geo") | **99 shapefiles** (SIRGAS/ZEPEC/zoneamento) com sufixo de hash |
| `1uQTkzx2fXGMH1J5zrF_K1yD-NsUxxc1i` | 05 — Geo | contêiner geo |
| `1LGrKx7sY8Jot1b1ROG53mhb-yy-zHQLv` | espelho de PDFs IPTU (subpasta jurídica) | duplicatas dos PDFs de _entrada + txts |
| `1rUSsxvtNWY657hqK6dsVBFmOz_BPIM6E` | Quadros/Outorga em .md (chunks) | extração NOSSA de páginas SMUL/PDE |
| `16UUslSV12qD-6f870TvG4Da6tMk6KAUx` | Tabelas .csv extraídas (Quadros PDE/Outorga) | extração NOSSA → input de engine |
| `1M4T65C4ckrccT8YPXWPYWM3XkuvAqpAW` | PNGs de Outorga (screenshots) | capturas NOSSAS |
| `0APQMETkmU9TbUk9PVA` | **Shared Drive root** | Google Docs de análise (NOSSOS) |
| `1loXodqJkdSTvboaGPHA9Ft2r9dSL5Tap` | com_empresa (sprints) | 30+ PDFs de comunicação interna (NOSSO) |
| `1l0MZR786o_qdP0FREoBQMuwzkswGg_8e` | árvore de docs societários (CNPJ 18.510 / 27.720 / 49.183 / ATUALIZADO) | ADQUIRIDO/oficial societário |
| `14jyyL_dSjSjZz41NNRslDuXfmkYEEQ0C` / `1vMUSxjSNjdh7...` / `1PGpHRoAPj4...` / `10FaV4KBGS3...` / `1GvKF0ALRN_...` / `13rAbexq2Gxy...` | pastas-espelho de shapefiles ZEPEC (várias datas) | cópias redundantes do set ZEPEC |
| `1ErIPltUfGYm...` / `1KtUVx6YlRwx...` | pastas com "Cópia de ZEPEC_*" | cópias redundantes |

**Diretório-mãe do TDC:** raiz `1BrM6q36meTtn5guJoiGbqvCtZF11Uau3`; para os motores, os dois nós que importam são `1grhqYgttj7...` (_entrada, canônicos) e `1ds4u4ZpoLl...` (geo-mãe, 99 shp).

---

## (a) Shapefiles ZEPEC oficiais — **camada de tombados / vedação Art.124**
Set completo por camada = `.shp + .dbf + .shx + .cpg`. Cópias canônicas abaixo estão em `01 — _entrada` (`1grhqYgttj7...`); há ≥5 pastas-espelho adicionais + cópias com sufixo de hash na geo-mãe.

| Nome lógico | Componentes (bytes) | nº cópias (pastas) | Proveniência | Motor | Melhor visão? | fileId canônico (.shp em _entrada) |
|---|---|---|---|---|---|---|
| **ZEPEC_BIR** | shp 855.548 · dbf 64.598 · shx (388/...) · cpg 5 | ~6 pastas | OFICIAL (GeoSampa/CONPRESP) | **M3-GEO** | **SIM** — geometria dos lotes tombados p/ o overlay do Motor 3 | `1SMJ5NlYfloTSOKt_PwwI618OToAKZQUk` |
| **ZEPEC_AUE** | shp 1.683.820 (+set) | geo-mãe + espelhos | OFICIAL | **M1-GATE / M3** | **SIM** — camada espacial de Área de Urbanização Especial; ajuda a vedação Art.124 §2 que o Motor 1 (D1) dizia faltar | `1gYeb5cYlFgVlYt87VZhCSFgdja4njttK` (geo-mãe, `ZEPEC_AUE_696911.shp`) |
| **ZEPEC_APP-BIR** | shp 74.568 · dbf 821 · shx 388 · cpg 5 | ~6 pastas | OFICIAL | **M1-GATE / M3** | **SIM** — APP sobre BIR: a camada espacial de vedação (APP+tombado) do Art.124 §2 | `1nSJNIe4lhxSGAuVgdY2bMbr0pkLyoQbN` |
| **ZEPEC_BIR_INDIC** | shp 358.660 · dbf 18.291 · shx 5.708 · cpg 5 | ~6 pastas | OFICIAL | **M3-GEO** | apoio — lotes indicados/em estudo para BIR | `1X0muNAcafJYXqb52GsI5Jn69gSnQ_Arc` |

Obs.: na geo-mãe (`1ds4u4ZpoLl...`) os mesmos aparecem com hash: `ZEPEC_BIR_0db6c0.shp` (`1LTx2DdsLFsytVMHheVkywVxDMuaR1Cuf`), `ZEPEC_AUE_696911.shp`, `ZEPEC_APP-BIR_88b4bb.shp` (`1TqYfBIZRi4w-NorvdkMwPzIOPxRxJNb5`), `ZEPEC_BIR_INDIC_b9f968.shp` (`1xkVIv-bJZyYLlLJ-t20twdQ-U7jrPHc0`). Há também "Cópia de ZEPEC_*.shp" em `1KtUVx6...`/`1ErIPltU...` (redundantes).

## (b) SIRGAS — camadas urbanísticas oficiais (GeoSampa)
Todas OFICIAIS (GeoSampa/PMSP). Nas 2 buscas em disco vieram componentes avulsos (.shp/.dbf/.shx) — o set de cada camada existe no Drive.

**b.1 — SIRGAS_SHP_LOTES_NN_<DISTRITO>** (lotes cadastrais por distrito): **59 distritos** capturados nas buscas (dos 96 de SP), ex.: 03_ANHANGUERA, 17_CAMPO_LIMPO, 43_JARDIM_ANGELA, 70_SANTANA, 72_SAO_LUCAS… todos na geo-mãe `1ds4u4ZpoLl...`. **M3-GEO** — malha de lotes p/ o overlay (cruzamento com ZEPEC_BIR). Ex. canônico: `SIRGAS_SHP_LOTES_70_SANTANA_b42fae.shp` (6.134.788 B) `1vjYfo976BeZOAO893iMIv3dWafjbNXcE`.

**b.2 — SIRGAS temáticos** (na geo-mãe):
| Camada | .shp (bytes) | Motor | fileId |
|---|---|---|---|
| benstombados | 2.538.964 | **M3-GEO / M1** — bens tombados (reforça ZEPEC_BIR) | `1WpeKCsz2EcovMBUVOJH79OPE39iWNDeD` |
| zeup_zemp | 416.724 | M3-GEO — zonas de estruturação | `1ExHL0dLrEoVF4l0aQOqB6zTPUG2AZz6Y` |
| logradouronbl | 30.840.700 | M3-GEO — eixo de logradouros (geocodificação) | `118bVYfXP9mpu8VIbm_4qBazI4fQfcFWG` |
| quadraMDSF (.dbf) | 22.943.110 | M3-GEO — quadras fiscais (join c/ IPTU) | `1VdbAkuqv3p_yKX_rO_ZUzGw5MOfVsxOo` |
| setorfiscal (.dbf) | 14.482 | M2-DADOS/M3 — setor fiscal (chave SQL do IPTU) | `1Cu7SIG_gxzk9ItsmT0dv2qYDDIrh5Ps1` |
| cota_solidariedade | 185.652 | M3 — cota de solidariedade | `1ZvGChaEPT6q7gRWQREJFfgibqSVPE7bp` |
| planomacro / baciahidro / hidrolinha / PLANO_DIRETOR_DRENAGEM / restricaomirantesantana / subvencao_economica / planomacro | vários | M3 (contexto) | (na geo-mãe) |

## (c) Listas ZEPEC-BIR oficiais (xlsx) — **fonte de verdade das certidões/declarações**
| Nome lógico | bytes | nº cópias | Proveniência | Motor | Melhor visão? | fileId canônico (_entrada) |
|---|---|---|---|---|---|---|
| **lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx** | 225.063 | ≥3 pastas | **OFICIAL (Prefeitura)** | **M1-GATE** | **SIM** — lista oficial de declarações; fonte de verdade p/ o gate de certidão | `17j94xkgVk4eberaRpRLK2j_ekz480Lny` |
| **lista_certidao_ZEPEC-BIR_agosto-2025.xlsx** | 194.082 | ≥3 pastas | **OFICIAL (Prefeitura)** | **M1-GATE** | **SIM** — lista oficial de certidões ZEPEC-BIR emitidas | `1en2WC2A-Wd21NNDhZ8ThheAyHmODIOl-` |

## (d) IPTU — dados brutos oficiais (PMSP)
| Nome lógico | bytes | nº cópias | Proveniência | Motor | Melhor visão? | fileId canônico (_entrada) |
|---|---|---|---|---|---|---|
| **IPTU_2026.csv** | 937.865.216 (~937 MB) | ≥8 pastas | **OFICIAL (PMSP cadastro IPTU 2026)** | **M2-DADOS** | **SIM** — base fiscal completa; input do engine de valor venal/IPTU | `1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM` |
| **iptu-2020-cep01.csv** | 152.926.077 (~153 MB) | ≥10 pastas | OFICIAL (PMSP IPTU 2020, recorte CEP01) | M2-DADOS | histórico p/ série temporal | `1AV8v4esuCxGulgxvGskzo595vycDa3U-` |
| PDFs de jurisprudência/doutrina IPTU (STF/STJ, PUCSP, UFC, Migalhas…) ~30 | 0,1–4,7 MB | duplicados em `1grhqYgttj7` e `1LGrKx7sY8` | OFICIAL (acórdãos) / PÚBLICO (doutrina) | Jurisprudência (Gen RAG) | acervo p/ tese, não p/ motor | ex. "Jurisprudência do STF sobre IPTU nos contratos de concessão.pdf" `1ZwsVFcClncSUaYLCQSDc1u0fX2m8unDY` |
| IPTU-TDC_stj-tema-*.txt (temas 174,262,399,566,1113,1158,1350) | <1,2 KB | _entrada | extração de temas STJ (oficial resumido) | Jurisprudência | mapeamento de temas repetitivos | `11BR6tZ4zPXIcaIBeRRQz4P5D4j61RSgy` (tema-1158) |

## (e) Quadros / Outorga (tabelas normativas → engine)
| Nome lógico | formato | Proveniência | Motor | Melhor visão? | fileId |
|---|---|---|---|---|---|
| PDE2013_SUBST2_Quadro_3_CA_ZEIS — Tab_1/Tab_2 | csv (122 / 161 B) | derivado de OFICIAL (PDE 2013, Quadro 3) — extração NOSSA | **M-VALOR (CA/coef.)** | tabela de CA p/ cálculo de potencial | `154dJZeFloDrPrYXd8WMjaJErd9i168ER` / `1c-1nteUrPFHkF6HHKQ1mF3P4mKDsfxk3` |
| PDE2013_SUBST2_Quadro_5_Fator_interesse_social_Fs | md (1.527 B) | derivado de OFICIAL (PDE Quadro 5) | M-VALOR (fator Fs da outorga) | fator social da fórmula de outorga | `1LHT2NfOmbzDS05gLytYY7i7iwyaKPShm` |
| Outorga Onerosa do Direito de Construir (SMUL) | 12 .md + 4 .csv + 6 .png | scrape NOSSO de página oficial SMUL | M-VALOR (contexto outorga) | texto/tabela da OODC; validar contra fonte | md `1QnyVTxZ2Z0kVPMYr4cI0CK2EikCnjuCg`; csv `1TkHq9ti4VWXqTnd04GE5JilBxg0NIvma` |

> Estas tabelas são **input de engine**, mas foram produzidas por nós (extração/scrape): usar como dado, mantendo rastreio ao dispositivo (PDE 2013 / SMUL) e revisão humana.

## (f) PDFs de enquadramento / documentos de imóvel
| Nome | formato | bytes | Proveniência | Uso |
|---|---|---|---|---|
| Paulo prédio Libero capa IPTU 2025 Libero Badaro 306 e 310.pdf | pdf | 586.378 | ADQUIRIDO (doc do imóvel-alvo) | M2/PROP — capa IPTU do imóvel | `1RSoqcK42sLTXXMElT-dH-N4j3XIhgtpb` |
| Minuta Contratual, Quadro Resumo e Propostas Técnica - Shopping | pdf | 1.562.498 | ADQUIRIDO (negócio) | contexto TDC | `1OoX3rcSrQeWsGRybrRZVXNleJNR_b87J` |
| Formulário para levantamento de IPTU.docx | docx | 13.845 | NOSSO (template de campo) | operacional | `1kc3gUMGDJV1m-hkmAWAPsxVWFiu_odN_` |

(Não apareceu PDF de enquadramento CONPRESP individual nas buscas; a camada de enquadramento está coberta pelos shapefiles ZEPEC + listas oficiais.)

## (g) Dados ADQUIRIDOS — societário (Motor 6 / PROP; registrado, fora de M1-M3)
| Nome lógico | tipo | Proveniência | fileId |
|---|---|---|---|
| Pastas CNPJ 18.510 / 27.720 / 49.183 / ATUALIZADO / CARTÃO CNPJ | folders | ADQUIRIDO/oficial (Receita) | `11FRe9B_DuzW-U_EibFDlqX7LSG-AvZrh`, `1x5ASfxTwspCnWH-HqRNamk09fBOg8Oeu`, `19_12hxHqbn-54dSivV2Z1oFn279vpClz`, `12AfpaCRy3BkaOdcbpmcxjlxyHSlHzgx2`, `12EjdZ0GZmQdzePjHwXCfaL1L8BhPxm5p` |
| CNPJ.pdf (cartões) | pdf | ADQUIRIDO/oficial | `1kAEK9IWno7c3bvIzkekMOCFF5jv81qhQ`, `1jkmbn6wAVoyB2QofC6W2iaGLSlPCfpDq` |
| CNPJ SB SOLUCOES E OBRAS | gdoc | ADQUIRIDO | `19LqQ8kHRMPr4WGpZvZwKwfRkw8ih230KobxZXTA6tKc` |

## (h) NOSSO / NÃO-CONFIÁVEL (não usar como fonte)
| Nome | tipo | por que NÃO-CONFIÁVEL | fileId |
|---|---|---|---|
| **LOTES_Parte_1..5_IA.csv** (~90 MB cada, 5 partes) | csv | sufixo `_IA` = derivado por nós dos lotes; **usar o shapefile SIRGAS_LOTES oficial no lugar** | `1EyzQ9O6HTbiUSBgotHYBun_haesZHGC_` … `1zQeOweWGTpizppN8owIv_p1qh4EH6jio` |
| DOCUMENTO MESTRE: SISTEMA OPERACIONAL HOLDING TDC | gdoc | doc de análise NOSSO | `1tbhRdfpD4pHeRl3wHSfusCBoNqCffn2xPJqSDhL05D8` |
| RAG IPTU — Gap Analysis / PLANO DE SANEAMENTO / MAPA IPTU+TDC / Estudo_Profundo_IPTU / Documento Base Inteligência Tributária | gdocs | análises NOSSAS (shared drive `0APQ…`) | `1Ubi7bjAQkJTX1OXa8e2JC_20Llad9NcIAVt0Re-YntY` etc. |
| Modelo Reduzido IPTU.xlsx/.csv (+ Converted) | xlsx/csv | planilha-modelo NOSSA | `1KAvM0NuHZzDo6jE-4BUX_CDBmIWXfi2m` |
| com_empresa_*_sprintN.pdf (30+) | pdf | comunicação interna NOSSA | `1loXodqJkdSTvboaGPHA9Ft2r9dSL5Tap` (pasta) |
| RELATORIO_INTELIGENCIA_TRIBUTARIA_IPTU*.txt, MINERACAO_IPTU_SP_*.txt, Pesquisa_*_IPTU_*.txt, "## Extração concluída…".txt | txt | relatórios/pesquisa NOSSOS | `14LiLMbTL5WzECJ1QUXvAUXU2lN6s7dOE` etc. |
| Mestre IPTU (pasta IPTU-Sergio), Quadros/Outorga .md e Outorga .csv/.png (cat. e) | vários | extração/scrape NOSSO — dado só após revisão | — |

---
### Nota de cobertura
- As 2 buscas em disco (200 regs) cobriram sobretudo componentes avulsos de shapefiles; as listas oficiais xlsx, o `ZEPEC_BIR.shp`, os CSV brutos de IPTU e os `_IA` **não** estavam nelas e foram recuperados ao vivo pelo MCP do Drive.
- Há paginação restante (nextPageToken) nas 3 buscas ao vivo — cópias/duplicatas adicionais das mesmas famílias; nenhum ativo lógico novo esperado.
