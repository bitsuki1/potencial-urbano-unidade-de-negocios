# Mapa de Dados — Fase 2 (identificacao de imoveis)

Projeto **Potencial Urbano** (RAG IPTU/TDC). Catalogo de **169 planilhas** (CSV/XLSX/XLS/ODS) do inventario `de-para-entrada.csv`.
Detalhamento campo a campo em `classificacao-planilhas.csv`.

> Metodo: leitura via `get_file_metadata` (campo `contentSnippet` = cabecalho + amostra). `read_file_content` estava negado no ambiente. Arquivos `.xls` legados nao retornam snippet (formato binario) — cabecalho inferido pelo nome/irmaos `.xlsx`. Nada foi movido/copiado/alterado.

---

## 1. A chave mestra: SQL (NUMERO DO CONTRIBUINTE / setor-quadra-lote)

O **SQL** (cadastro do contribuinte / setor+quadra+lote) e a chave de cruzamento central. Quase todas as bases oficiais e derivadas o carregam, o que permite costurar IPTU, ITBI, OODC, tombamento e licenciamento ao mesmo imovel.

## 2. Base IPTU 2026 (a "espinha dorsal")

- **PROVAVEL BASE IPTU 2026**: `IPTU_2026.csv` — id **1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM** — ~**937 MB**, ~1 milhao de linhas, ~60 colunas.
  Entrega: NUMERO DO CONTRIBUINTE (SQL), endereco/logradouro, numero, complemento, bairro, CEP, area terreno/construida, valor m2 terreno e construcao, ano exercicio, uso e padrao. Eh a **tabela-cadastro completa de imoveis** para a Fase 2.
- Recorte historico: `iptu-2020-cep01.csv` (id 1AV8v4esuCxGulgxvGskzo595vycDa3U-, 153 MB) — IPTU 2020 limitado a CEP 01.
- **Lacuna IPTU**: a base traz **valor venal/valor m2 e SQL, mas NAO traz nome do proprietario nem CPF/CNPJ** (padrao da PMSP). O proprietario precisa vir de outras fontes (ver secao 4).

## 3. Planilhas que trazem SQL (cruzaveis direto com o IPTU)

- **IPTU**: `IPTU_2026.csv`, `iptu-2020-cep01.csv`.
- **ITBI**: toda a serie `guias_de_itbi_pagas_*` / `GUIAS DE ITBI PAGAS*` (2006–2026) — SQL + matricula.
- **Outorga Onerosa (OODC)**: `oo_2002-2014.xlsx`, `oo_2014-2023.xlsx`, `OODC_2024-2025.xlsx`, `OUTORGA_ONEROSA.xlsx`, `Atualizacacao_Q14_anoref2025.csv`, `PDE2013_SUBST2_Quadro_14_cadastro.csv`.
- **Licenciamento (Aprova Digital / alvaras)**: `2021.xlsx`, `2022 (4)(1)(1).xlsx`, `Ano_2024_AD.xlsx`, `Ano_2025_AD_12.xlsx`, `Ano_2026_AD_01.xlsx`, `ANUAL - 2022.xlsx`, `Aprova Digital_dezembro2020.xlsx`, `extrato-aprova-digital-1-sem.-2025.csv`, `extrato_ad_2020-2023.csv`, `extrato_ad_2024_1.csv`, `extrato_ad_2024_2.csv`.
- **SISSEL** (processos aprovados, com proprietario): `sissel_ANO_2024.xlsx`, `sissel_ANO_2025_12.xls`, `sissel_ano_2026_01.xls`, `Ano_2023_SISSEL.xls`.
- **Tombamento / preservacao**: `SIRGAS_SHP_benstombados1.csv`, `area_potencial_e_suspeita_de_contaminacao.*`, `DIVERSOS_IA.csv`.
- **TDC / ZEPEC**: `lista_certidao_ZEPEC-BIR_agosto-2025.xlsx`, `lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx`.
- **Geometria/lotes (derivado)**: `LOTES_Parte_1..5_IA.csv` (lotes enriquecidos, ~85–99 MB cada).
- **Consolidados derivados**: `MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2.csv`, `MEGA_PLANILHA_SANEADA_TOMBADOS_V1.csv`, `PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv`.

## 4. Quem traz PROPRIETARIO / CPF / CNPJ

- **Nome do proprietario (NOME)**:
  - `sissel_*` (SISSEL alvaras/processos) — proprietario + SQL + endereco.
  - `ANUAL - 2022.xlsx` (alvaras detalhado) — proprietario + SQL.
  - `OODC_2024-2025.xlsx` — proprietario na OODC.
  - `SIRGAS_SHP_benstombados1.csv` / `SIRGAS_SHP_ZEPEC*.csv` — denominacao do bem (nao necessariamente pessoa fisica).
  - Consolidados derivados: `MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2.csv`, `PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv` (campo proprietario_consolidado / proprietario_encontrado).
- **CNPJ**:
  - `empresas.csv` (~2,2 GB) — cadastro de empresas (CNPJ).
  - `socios.csv` (~3,4 GB) — socios (CPF/CNPJ + nome).
  - `holdings.csv` (~60 MB) — holdings societarias.
  - Derivados que ja trazem CNPJ/socios cruzados: `MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2.csv` (cnpj_socia, razao_social_socia), `PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv`.
- **CPF**: aparece somente nas bases societarias `socios.csv` (e potencialmente `empresas.csv`). **Nenhuma base imobiliaria oficial traz CPF do proprietario diretamente.**

## 5. Quem traz ITBI (valor de transacao)

- Serie completa **GUIAS DE ITBI PAGAS** (anos 2006 a 2026), ~20–46 MB cada, ~27–28 colunas:
  SQL + endereco + CEP + **matricula** + valor de transacao/venal + ano.
- Serie **anual_*.xls / Anual*.xls / 20xx - anual.xls** (2000–2021) — guias ITBI anuais em `.xls` legado (cabecalho nao extraido pelo snippet, tema ITBI confirmado pelos irmaos `.xlsx`).
- Derivado: `PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv`.

## 6. Quem traz MATRICULA (registro imobiliario)

- **Apenas a serie GUIAS DE ITBI PAGAS** traz `matricula` de cartorio, alem do derivado `PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv`.
- IPTU, OODC e licenciamento **nao** trazem matricula. A serie ITBI eh a unica ponte SQL <-> matricula.

## 7. Quem traz VALOR VENAL

- `IPTU_2026.csv` e `iptu-2020-cep01.csv` (valor m2 terreno/construcao).
- Serie ITBI (valor venal/transacao).
- OODC (`oo_*`, `OODC_2024-2025.xlsx`, `OUTORGA_ONEROSA.xlsx`).
- `Atualizacacao_Q14_anoref2025.csv` e `PDE2013_SUBST2_Quadro_14_cadastro.csv` (valor m2 de terreno por SQ/Codlog — base de calculo de outorga).

## 8. Tabelas de parametros / engines (regras, nao imoveis)

Tabelas-motor para calculo de potencial construtivo, NAO cadastros de imoveis (sem SQL):
`001..012 QUADRO_*` (Lei 16.402/2016), `PDE2013_SUBST2_Quadro_1..10`, `2014-07-31 - LEI 16050`, `SIMULADOR_QA_*`, `MASTER_PARAMETROS_URBANISTICOS.xlsx`.
Servem ao engine de calculo (CA/TO/QA/outorga), nao ao matching de imovel.

## 9. Como as chaves conectam (modelo de juncao)

```
                         empresas.csv / socios.csv / holdings.csv
                              (CNPJ, CPF, NOME do socio)
                                        |  (CNPJ/NOME)
                                        v
  SISSEL / ANUAL / OODC  --NOME-->  proprietario
        |  (SQL)                        ^
        v                               |  (NOME do proprietario)
  +------------------ SQL (chave mestra) ------------------+
  |          |              |               |              |
IPTU_2026   GUIAS_ITBI    OODC          benstombados   LOTES_IA / Aprova Digital
(venal,     (ITBI,        (outorga,     /ZEPEC         (geometria,
 endereco,   MATRICULA,    valor venal)  (preservacao)  licenciamento)
 CEP)        endereco)
                |
                +-- MATRICULA (so via ITBI) --> cartorio / registro
```

- **SQL** liga IPTU <-> ITBI <-> OODC <-> licenciamento <-> tombamento (cadastro do imovel).
- **MATRICULA** so existe na serie ITBI — unica ponte para o registro de cartorio.
- **NOME do proprietario** liga as bases de processo (SISSEL/OODC/alvaras) as bases societarias (empresas/socios/holdings) via **CNPJ/razao social**, fechando a cadeia imovel -> proprietario -> socios.
- Os tres consolidados **MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2**, **MEGA_PLANILHA_SANEADA_TOMBADOS_V1** e **PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2** ja realizam parte desse cruzamento (foco: bens tombados/ZEPEC) e servem de prova de conceito do pipeline.

## 10. Lacunas de dados (o que ainda falta)

1. **CPF do proprietario de imovel**: nenhuma base imobiliaria oficial traz CPF. So ha CPF em `socios.csv` (pessoas em empresas). Para pessoa fisica proprietaria de imovel nao ha fonte direta — depende de match por NOME (fraco/ambiguo).
2. **Nome do proprietario na base IPTU**: IPTU_2026 (universo de ~1M imoveis) **nao tem proprietario**. Proprietario so existe para o subconjunto que passou por SISSEL/OODC/alvaras/ITBI. Cobertura proprietaria sobre o universo IPTU eh **parcial**.
3. **MATRICULA** so chega via ITBI — imoveis sem ITBI registrado ficam sem ponte para cartorio.
4. **.xls legados nao lidos** (cabecalho nao confirmado): serie `anual_*`/`Anual*`/`20xx - anual` (ITBI), `Ano_2023_SISSEL.xls`, `sissel_ANO_2025_12.xls`, `sissel_ano_2026_01.xls`, `dic_*.xls`, `metadados_*.xls`, `SIMULADOR_QA_*.xls`. Tema inferido por nome/irmaos; confirmar colunas exige conversao do binario.
5. **Vinculo direto CNPJ <-> SQL** so existe nos derivados; nas bases oficiais o vinculo eh indireto (via NOME), portanto sujeito a ruido.
6. **Geometria** (poligonos WKT) esta em arquivos IA derivados (`ZONEAMENTO_IA`, `PCA_Consolidado_IA`, `RUAS_Consolidado_IA`, `LOTES_*_IA`) — uteis para geo-match mas nem todos com SQL legivel no snippet.

## 11. Arquivos ilegiveis / limitacoes (nunca descartados)

- `AUDITORIA_1_BASE_ORIGINAL_COMPLETA.csv` (id 1JM7spa4En4KmicoL5_HVVXp-E7ZNgs6T) — **vazio (4 bytes, so BOM)**.
- `AUDITORIA_2_MOTOR_1_ATUAL.csv` (id 1k-zbLK3o1Oo41bfPVDJ1SsDoxDld_cPZ) — **vazio (4 bytes, so BOM)**.
- `RESOLUCAO SMUL_CTLU N4 2024.csv` (id 1SQ7KIqf4FobhvtfumvJCp5NSsHv_Q0Wc) — **praticamente vazio (30 bytes, snippet so com aspas)**.
- `RUAS_Consolidado_IA.csv` e `socios.csv` — snippet vazio por **tamanho** (63 MB / 3,4 GB); tema inferido, cabecalho nao confirmado.
- Toda a serie `.xls` legada (ver lacuna 4) — sem snippet; tema inferido.

## 12. Oficialidade e destino

- **Oficiais** (PMSP/SMUL/SISSEL/GeoSampa/PDE/SIRGAS): IPTU, ITBI, OODC, alvaras, SISSEL, tombamento, quadros PDE.
- **Derivados** (internos/IA/consolidados): `*_IA.csv`, `MEGA_PLANILHA_*`, `PLANILHA_ENRIQUECIDA_*`, `holdings.csv`, `socios.csv`, `empresas.csv`, `Notas Nilson Grotti.xlsx`.
- **Destino padrao**: `03-Tabelas&Engines` (id 1v4H2YsIZSNDwNXiMtOAV1w1qy-5kOuvy), exceto dicionarios/metadados (marcados `dicionario`: glossarios QUADRO_1, dicionarios `dic_*`, `metadados_*`, catalogos DEEP_SCAN, MASTER_PARAMETROS).
