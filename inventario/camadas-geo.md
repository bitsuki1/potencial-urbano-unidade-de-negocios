# Camadas GEOESPACIAIS — Motor 3 (Potencial Urbano)

Catálogo temático da base GIS do projeto. Fonte: `de-para-entrada.csv`.
Total: **648 arquivos GIS** = 645 componentes de shapefile + 2 GeoPackage (.gpkg) + 1 .tgz (Tabela VI).
Agrupados em **165 itens distintos**: 162 camadas shapefile + 2 GeoPackage + 1 Tabela VI.
Destino de arquivamento: `05-Geo = 1VxXDspnEwYuiCMXjn9-YPp65h3vtb_pr`.

Detalhamento item a item em `classificacao-gis.csv`.

> Um shapefile = um conjunto de arquivos com o mesmo nome-base e extensões diferentes
> (.shp = geometria, .shx = índice, .dbf = atributos, .cpg = codepage, .prj = projeção/CRS).
> Mínimo funcional: .shp + .shx + .dbf.

---

## 1. Zoneamento (Lei 16.402/2016) — 43 camadas
Uma camada por tipo de zona. Polígonos com a delimitação de cada zona na cidade.
Cada zona define os parâmetros urbanísticos: **Coeficiente de Aproveitamento (CA) básico e máximo**,
taxa de ocupação, gabarito, etc. — base direta para cálculo de **Potencial Construtivo / TDC**.

- **Centralidade:** ZC, ZC_a, ZC_u (incompleta), ZC_ZEIS
- **Corredor:** ZCOR_1, ZCOR_2, ZCOR_3, ZCOR_a
- **Mista:** ZM_a, ZM_u, ZMIS_a, ZMIS_u
- **Eixo / urbanização:** ZEU_a, ZEU_u, ZEUP_a, ZEUP_u
- **Estruturação metropolitana:** ZEM, ZEMP
- **Exclus. residencial:** ZER_1, ZER_2, ZER_a
- **Predom. industrial:** ZPI_1, ZPI_2
- **Desenv. sustentável / econômico:** ZPDS_r, ZPDS_u, ZDE_1, ZDE_2
- **Preservação / proteção ambiental:** ZPR, ZEP, ZEPAM
- **Ocupação especial:** ZOE

### ZEIS — Zonas Especiais de Interesse Social (5 camadas)
ZEIS_1, ZEIS_2, ZEIS_3, ZEIS_4, ZEIS_5. Relevantes para gravame social e regras de uso diferenciadas.

### ZEPEC — Zonas Especiais de Preservação Cultural (7 camadas)
ZEPEC_APC, ZEPEC_APP, ZEPEC_APP-BIR, ZEPEC_AUE, ZEPEC_AUE_INDIC, ZEPEC_BIR, ZEPEC_BIR_INDIC.
Imóveis/áreas tombados ou de interesse cultural — **fonte de imóveis geradores de TDC** (Transferência do Direito de Construir).

---

## 2. Lotes — SIRGAS_SHP_LOTES_01..96 (96 camadas)
Uma camada por **distrito** (Água Rasa, Mooca, Sé, Pinheiros, …, Lajeado).
Polígonos de cada lote com **número de SQL** (Setor/Quadra/Lote) no .dbf.
**Chave geográfica do imóvel** — permite cruzar geometria/área de terreno com IPTU (por SQL)
e calcular potencial construtivo por lote. Datum SIRGAS2000.

---

## 3. Quadras e cadastro fiscal
- **SIRGAS_SHP_quadraMDSF** — quadras (Mapa Digital).
- **QA** — quadras/áreas.
- **SIRGAS_SHP_setorfiscal** — setores fiscais (agregação de SQL; ponte direta com IPTU).
- **SIRGAS_SHP_logradouronbl** — logradouros (endereçamento).

---

## 4. Plano Diretor / macroescala
- **SIRGAS_SHP_planomacro_polygon** / **SAD69-96_SHP_planomacro_polygon** — macrozonas/macroáreas.
- **SIRGAS_SHP_planoacao_polygon** (INCOMPLETA, falta .dbf) / **SAD69-96_SHP_planoacao_polygon**.
- **SIRGAS_SHP_PLANO_DIRETOR_DRENAGEM** (tem .prj).
- **SAD69-96_SHP_restricaomirantesantana_polygon** / **SIRGAS_SHP_restricaomirantesantana_polygon** — restrição de gabarito (mirante Santana).

---

## 5. Instrumentos urbanísticos e incentivos
- **SIRGAS_SHP_cota_solidariedade** — Cota de Solidariedade (contrapartida HIS).
- **SIRGAS_SHP_requalifica_centro** (tem .prj) — programa Requalifica Centro.
- **SIRGAS_SHP_subvencao_economica** — subvenção econômica.
- **INCENTIVO_GARAGEM** — incentivo a garagem.
- **SIRGAS_SHP_zeup_zemp** (tem .prj) — ZEUP/ZEMP consolidado.
- **AC_1, AC_2** — áreas de controle/AC.
- **PCA_CANT** — PCA (perímetro/cantos).
- **VETOS_TODOS** — vetos legislativos georreferenciados.

---

## 6. Ambiental / hidrografia / patrimônio
- **SIRGAS_SHP_baciahidro_polygon** — bacias hidrográficas.
- **SIRGAS_SHP_hidrolinha** — rede hídrica (linhas).
- **SIRGAS_SHP_benstombados** — bens tombados (patrimônio).

---

## 7. GeoPackage (.gpkg) — 2 arquivos (listados à parte)
Formato GeoPackage (SQLite espacial) — pode conter múltiplas camadas internas.
- **layer_geosampa_apas.gpkg** — APAs (Áreas de Proteção Ambiental), origem GeoSampa.
- **area_potencial_e_suspeita_de_contaminacao.xlsx.gpkg** — áreas potenciais/suspeitas de contaminação (restrição ambiental ao uso/edificação).

---

## 8. Tabela VI — Tipos e padrões de construção (Lei 16.768/2017)
Arquivo `Tabela VI - Tipos e padrões de construção - Lei 16768-2017.tgz`
(id `1PgtgfPMxPc_S7k4vIh4o-jsj0VaYkyNu`, mimeType application/x-compressed).

**Não é um tar.gz.** Os bytes baixados são um **PDF de 1 página escaneado** (Lexmark MX711,
Title="Scanned Document", imagem 2480×3507 px ≈ A4 300dpi, **sem camada de texto / sem fontes**).
→ **Precisa OCR / extração manual** para virar dado estruturado. **Não descartar.**
Conteúdo esperado: tabela de tipos e padrões de construção (parâmetros de edificação) da Lei 16.768/2017.

---

## Camadas INCOMPLETAS (sinalizadas — NÃO descartar)
| Camada | Tem | Falta | Gravidade |
|---|---|---|---|
| `ZC_u` | .cpg | .shp, .shx, .dbf | Crítica — sem geometria nem atributos |
| `SIRGAS_SHP_planoacao_polygon` | .cpg, .shp, .shx | .dbf (atributos) | Alta — abre no GIS sem tabela |
| `PCA_CANT` | .shp, .shx, .dbf | .cpg | Baixa — núcleo OK, só codepage |
| Tabela VI (.tgz) | PDF-imagem | texto/OCR | Precisa extração manual |

> Apenas **3 camadas** possuem `.prj` (CRS explícito): `SIRGAS_SHP_PLANO_DIRETOR_DRENAGEM`,
> `SIRGAS_SHP_requalifica_centro`, `SIRGAS_SHP_zeup_zemp`. As demais 159 não têm `.prj` —
> o CRS é inferível pelo prefixo (`SIRGAS` = SIRGAS2000; `SAD69` = SAD69). Atribuir o CRS
> manualmente ao importar no GIS.

---

## Como cruzar com IPTU / TDC
- **Geometria por SQL → IPTU:** `SIRGAS_SHP_LOTES_*` (.dbf traz SQL) + `setorfiscal` + `quadraMDSF`.
  Liga cada lote ao cadastro de IPTU e fornece área de terreno.
- **CA básico/máximo → Potencial construtivo:** camadas de **Zoneamento** (item 1).
  Sobrepor o lote à zona define os coeficientes aplicáveis.
- **Imóveis geradores de TDC:** `ZEPEC_*` e `benstombados` (preservação cultural) e `ZEIS_*`.
- **Restrições que reduzem potencial:** APAs (.gpkg), áreas contaminadas (.gpkg), `restricaomirante`
  (gabarito), `baciahidro`/`hidrolinha` (drenagem).
- **Parâmetros de edificação:** Tabela VI (após OCR).
