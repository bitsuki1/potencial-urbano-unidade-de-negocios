# Ideias, Estratégia e Arquitetura colhidas dos documentos (Potencial Urbano)

> Apanhado das melhores ideias, regras de negócio e decisões de arquitetura encontradas nos ~116 documentos de texto classificados.
> Fonte de leitura: snippets de conteúdo via Google Drive (`get_file_metadata`). Cada ideia traz atribuição ao arquivo de origem.
> Data da varredura: 2026-06-18.

---

## 0. Como este material foi lido (limitação importante)
A ferramenta de leitura plena (`read_file_content`) foi **negada por permissão** neste ambiente. Toda a colheita abaixo veio do campo `contentSnippet` retornado por `get_file_metadata`, que entrega aproximadamente os **primeiros ~1.800-4.000 caracteres** de cada arquivo (e o texto integral, quando o arquivo é curto). Para os documentos estratégicos curtos (Conhecimento Mestre, Oráculos, Relatórios de Inteligência) isso capturou praticamente todo o conteúdo útil. Para os arquivos muito grandes (manifestos de 200KB-900KB, leis federais de 100KB+), só vimos o início — eles são, porém, majoritariamente **catálogos/inventários repetitivos** ou **texto legal verbatim**, cuja natureza já está clara pelo início.

---

## 1. O ATIVO MAIS VALIOSO: a "Fórmula Mestra" e os motores de cálculo TDC/OODC

Vários documentos convergem para o **mesmo motor de cálculo** da contrapartida financeira (Outorga Onerosa do Direito de Construir / valor de TDC):

> **OO = (Área_Adicional / CA_max) × Fp × Fs × V**

- `CA_max` = Coeficiente de Aproveitamento Máximo (vem da **ZONA**, Quadro 3 da LPUOS).
- `Fp` = Fator de Planejamento; `Fs` = Fator de interesse Social (vêm dos Quadros 5 e 6 do PDE).
- `V` = Valor do m² da terra (vem do **Quadro 14**, `Atualizacacao_Q14_anoref2025`).

Atribuição: `CONHECIMENTO_MESTRE_IA_V3.md`, `CONHECIMENTO_MESTRE_IA_V3.1_INABALAVEL.md`, `ORACULO_MESTRE_RELACIONAL_V4.md`.

**Constantes capturadas** (`CONHECIMENTO_MESTRE_IA_V3.1`):
- Fator Social (Fs): HIS = 0,0 | HMP = 0,4 a 0,6 | Residencial > 70 m² = 1,0.
- Fator Planejamento (Fp): Arco Pinheiros / Centro / Eixos = 1,2 (R) e 1,3 (nR); Macroárea de Qualificação = 0,6.
- A gratuidade do potencial construtivo termina no **Coeficiente Básico (CA_bas)**; acima dele paga-se outorga.

> **Decisão de arquitetura derivada:** o cálculo é determinístico e tabular. O RAG não precisa "inventar" o cálculo — precisa **buscar as constantes certas** (Fs, Fp, V, CA_max) cruzando ZONA + perímetro + uso, e aplicar a fórmula. Isto justifica separar "Tabelas&Engines" das "Leis".

---

## 2. A REGRA DE OURO FINANCEIRA: teto de 5% do FUNDURB (sensor de liquidez)

> O potencial transferido por TDC nos **últimos 12 meses não pode exceder 5% da arrecadação anual do FUNDURB**.
> Referência 2025: arrecadação Jan-Dez/24 ≈ R$ 43,4 Mi → **limite TDC ≈ R$ 7,8 Mi por período**.

Atribuição: `CONHECIMENTO_MESTRE_IA_V3.1`, `CONHECIMENTO_MESTRE_IA_V3` (cita Art. 24 LPUOS).

**Ideia operacional (muito forte):** tratar o arquivo `fila_tdc_5porcento_fundurb_dez_2025` como um **"Sensor de Liquidez de Mercado"** — antes de sugerir a venda/emissão de uma TDC, consultar o estoque disponível no FUNDURB. Atribuição: `MANIFESTO_TOTAL_DE_TRANSICAO.md`, `ORACULO_MESTRE_RELACIONAL_V4.md`. Este é um diferencial de produto: não basta calcular o potencial, é preciso saber se **há janela de mercado** para liquidá-lo.

---

## 3. AS 6 VIAS DE GERAÇÃO DE TDC (o "mapa de oportunidades" do negócio)

As 6 estratégias mestras / vias de geração de potencial transferível (`CONHECIMENTO_MESTRE_IA_V3` e `V3.1`):
1. Preservação Histórica/Cultural (imóveis **tombados** – ZEPEC).
2. Preservação Ambiental (ZEPAM na Macrozona de Estruturação).
3. Regularização Fundiária.
4. Provisão de HIS (Habitação de Interesse Social).
5. Implantação de Parques Planejados (Quadro 7 do PDE).
6. Melhoramentos Viários (corredores de ônibus).

> **Ligação direta com o modelo de negócio:** o `Contrato de Gestão Comercial` (OPIT-SP / Bairro Vivo) foca na via 1 — **captação de imóveis tombados para emitir TDC**. As outras 5 vias são mercados adjacentes ainda não explorados comercialmente — oportunidade de expansão.

---

## 4. INTELIGÊNCIA GEOGRÁFICA E "SCORE DE OPORTUNIDADE"

- **Prioridade absoluta** para lotes no **Arco Pinheiros (Lei 18.222/24)** e nos **Eixos de 700m (Lei 17.975/23)** — são onde Fp é maior (1,2/1,3), logo maior valor de outorga/TDC. Atribuição: `CONHECIMENTO_MESTRE_IA_V3`/`V3.1`.
- **Protocolo Geográfico — "SQL LIMPO":** chave de **10 dígitos obrigatória** para todos os JOINs. A chave de mapa é `lo_setor` (3 díg) + `lo_quadra` (3 díg) = **SQ**, que casa com a coluna `SQ` da tabela de valor de terra (Q14). Atribuição: `CONHECIMENTO_MESTRE_IA`, `ORACULO_MESTRE_RELACIONAL_V4.md`.
- **Datum oficial: SIRGAS 2000** (obrigatório); correção automática de SAD69 para camadas de 2014/2016. Atribuição: `ORACULO_GEOGRAFICO_DEFINITIVO_V3.md`.
- Cruzamento obrigatório com Mapas 5 (Hidrografia) e 12 (Drenagem) do PDE antes de validar um lote. Atribuição: `CONHECIMENTO_MESTRE_IA_V3`.

> **Decisão de arquitetura:** os mapas viram **GeoJSON em EPSG:4326** (camada GOLD) para análise com `geopandas`; o catálogo espacial (`MOTOR_3_CATALOGO_ESPACIAL.md`) é o índice desses GeoJSON.

---

## 5. AS TRÊS CHAVES DE JOIN (modelo relacional do RAG) — `ORACULO_MESTRE_RELACIONAL_V4.md`

1. **Lote ↔ Valor de Terra:** chave `SQ` (setor+quadra) → define `V`.
2. **Zoneamento ↔ Parâmetros Construtivos:** atributo `ZONA` → coluna `ZONA (a)` do Quadro 3 → define `CA_max` e gabarito.
3. **Qualificação Ambiental ↔ Quota Ambiental:** atributo `PA` (perímetro) → Quadro 3A → define pontuação mínima de QA.

> Este é, na prática, o **esquema de dados** do produto. Vale formalizá-lo como contrato de dados (data contract) entre as camadas mapa e tabela.

---

## 6. ARQUITETURA DE DADOS: medallion + hierarquia de confiança

- **Camadas Bronze / Silver / Gold** (medallion):
  - Bronze (`01_BRONZE_RAW`): ingestão crua, versionada `v01`, tag `Oficial_Pendente_Validacao` (`manifesto_datalake_*.json`: 1140 ativos).
  - Silver (`02_SILVER_STAGED`): árvore de domínios (Certidoes_e_Atos, Economia_Urbana_e_Financas, Geoprocessing_e_Mapas, Legislacao_Urbanistica, Patrimonio_Historico) — pipeline OCR de PDF→Markdown, limpeza de tabelas, SHP→GeoJSON (`ESTRUTURA_SILVER_IA.md`; log: 389 ok, 28 precisam OCR avançado).
  - Gold: índices/motores prontos (`MOTOR_3_CATALOGO_ESPACIAL.md` traz front-matter `layer: GOLD`).
- **Hierarquia de Fontes / Verdade dos Dados em 3 níveis** (`HIERARQUIA_DE_FONTES_ORACULO.md`):
  - **Nível 1 – OFICIAL (PMSP/DOSP):** definições legais (leis, quadros oficiais, shapefiles SIRGAS oficiais).
  - **Nível 2 – cálculos rápidos** (motores/tabelas derivadas).
  - **Nível 3 – NÃO VALIDADO** (rascunhos, fontes secundárias).
  > **Ideia central para o RAG jurídico:** o Oráculo deve **priorizar N1 para afirmações legais** e só usar N2 para estimativas. Isto é uma política de citação/grounding — diretamente aplicável ao desenho atual.

---

## 7. GOVERNANÇA: "nunca deletar", protocolo Platina e auditoria forense

- **Princípio "NENHUM ARQUIVO FOI DELETADO"** — repetidos e rascunhos guardados para auditoria limpa na próxima sessão (`MANIFESTO_TOTAL_DE_TRANSICAO.md`). Alinha-se com a regra de ouro deste próprio trabalho.
- **Protocolo Platina** (`MANIFESTO_PLATINA_FINAL.md`): roteia cada ativo para `01_FONTES_OFICIAIS_N1` (leis/mapas oficiais) ou `02_MOTORES_CALCULO_N2` (quadros/CSVs de cálculo); duplicados explícitos vão para o lixo com rastro.
- **Auditoria de duplicados forense** (`RELATORIO_DUPLICADOS_FORENSE.md`): identifica arquivos de conteúdo idêntico espalhados — útil porque o inventário atual tem **muitas duplicatas** (ver §9).
- **Pacto de Soberania / versionamento por anulação:** cada nova versão do Conhecimento Mestre declara que "anula e integra" as anteriores (V3.1 anula V3, V2, V1 e o `documento_final_ia.pdf`). Ou seja: existe uma **única fonte da verdade vigente por vez**.

---

## 8. TESES JURÍDICAS DE IPTU colhidas (matéria-prima do RAG jurídico)

Dos relatórios de inteligência (`RELATORIO_INTELIGENCIA_TRIBUTARIA_IPTU*.txt`, `Relatorio_Inteligencia_Tributaria_IPTU_2026.txt`, `MINERACAO_IPTU_SP_Teses_Impugnacao_Base_Calculo.txt`) e pesquisas acadêmicas (`Pesquisa_Academica_*`, `Pesquisa_IPTU_*`). Estas são **teses de impugnação/economia tributária** que dão valor ao produto:

1. **APP / contaminação ambiental reduz/elimina base de cálculo** — limitação de uso esvazia o valor venal e a capacidade contributiva (inclui decisão TJ-SP/comarcas que afastaram IPTU em imóvel majoritariamente APP). [IPTU Verde como extrafiscalidade].
2. **Desapropriação indireta / imissão na posse extingue o fato gerador** — sem posse/fruição não há contribuinte (Harada; art. 130 e 156 CTN; bis in idem).
3. **Tema 1062/STF (ARE 1216078):** juros de mora do IPTU municipal **não podem superar a SELIC** da União — base para repetição de indébito e exceção de pré-executividade contra a Lei Municipal 6.989/1966 quando cobra juros acima da SELIC.
4. **Responsabilidade propter rem não é retroativa ilimitada:** adquirente não responde por IPTU de exercícios anteriores (TJ-SP, terreno do Metrô).
5. **Alienação fiduciária:** o credor fiduciário (incorporadora) **não é contribuinte** do IPTU antes de consolidar a propriedade (TJ-GO/STJ).
6. **Loteamento sem TVEO:** IPTU sobre lotes só é exigível após individualização no cadastro (que pressupõe o TVEO) — lançamento antecipado é ilegal.
7. **EC 132/23 + LC 214/25:** permitem atualização da base do IPTU por decreto segundo critérios de lei municipal → **controvérsia** com a Súmula 160/STJ e a estrita legalidade (art. 97, IV, CTN) — risco de inconstitucionalidade na ausência de lei municipal específica (Harada; JOTA; Migalhas).
8. **PGV defasada é violação constitucional / e também gera renúncia de receita:** dissertações (UFC, UFS, PUC-SP) mostram defasagem da Planta Genérica de Valores, depreciação baseada só na data de construção, e defendem método evolutivo/regressão hedônica para avaliação em massa mais justa (NBR 14.653).
9. **Imunidade recíproca em concessões** (ferrovias, estatais reversíveis, imóveis federais cedidos) — Temas 437/STF e RE 1.412.662 — área em disputa.
10. **Lacuna a pesquisar:** "anulação IPTU drone/MDC" (uso de drones e Mapa Digital da Cidade para recadastramento) — string não retornou resultados; recomendado ampliar busca em TJSP/STJ.

> **Súmulas-base** já capturadas verbatim (fontes N1): STF 539, 589, 668, 670→SV41, 724→SV52, SV 19; Temas STF 94, 155, 523, 1020, 1084; Temas STJ 174 (DL 57/66 IPTU×ITR), 262, 399, 566, 1113 (base ITBI ≠ IPTU), 1158, 1350; Súmulas STJ 314/392/393/397/399/409/481/614/626; REsp 1112646/1130545/1202136/1645832/1658054; Súmulas Vinculantes do CMT-SP 1 a 8.

---

## 9. FAMÍLIAS DE VERSÕES IDENTIFICADAS (linhagens)

| Família | Versões / instâncias vistas neste inventário | Observação |
|---|---|---|
| **Conhecimento Mestre IA** | V3 e V3.1 ("INABALAVEL") presentes aqui; menções a V1, V2 e `CONHECIMENTO_MESTRE_IA.md`/`V2` em logs | Cada versão "anula" a anterior. V3.1 é a vigente. |
| **Oráculos (estratégicos)** | `ORACULO_GEOGRAFICO_DEFINITIVO_V3.md`, `ORACULO_MESTRE_RELACIONAL_V4.md` | Linhagem geográfica chegou ao "Definitivo V3"; relacional ao "V4". |
| **Oráculos de Mapas** | citados nos manifestos: `ORACULO_DE_MAPAS_V1`, `_PERFEITO`, `_DEFINITIVO`, `ORACULO_SUPREMO_DE_MAPAS` (4+ variantes) | Não estão entre os 116 de texto, mas a linhagem é grande; `RELATORIO_INTEGRIDADE_MAPAS_FINAL.md` os audita. |
| **Motores** | `MOTOR_3_CATALOGO_ESPACIAL.md` (motor espacial). Manifestos citam "02_MOTORES_CALCULO_N2" e "02_MOTORES_FINANCEIROS" | Há pelo menos 3 motores conceituais: cálculo, financeiro, espacial. |
| **Manifestos** | Auditoria, Platina Final, Total de Transição | Três gerações de governança/inventário. |
| **Quadros LPUOS (16.402/2016)** | Quadros 1, 2, 2A, 2B, 3, 3A, 3B, 3C, 4, 4A, 4B, 5 — em .docx e .doc ("FINAL") + PDFs citados | Anexos oficiais; base das tabelas de cálculo. |
| **Relatórios de Inteligência Tributária IPTU** | 3 instâncias (base, "(1)", "2026" curado) | Mesma pesquisa, graus de curadoria diferentes. |
| **Pesquisa Acadêmica IPTU** | 2 instâncias (variações de palavras-chave) | Conteúdo acadêmico BDTD/USP/IBDT. |
| **Jurisprudência STF/STJ** | dezenas de arquivos, muitos com sufixo `(1)..(5)` | **Duplicatas massivas** — ex.: `stf-sumula-539` aparece 6x; `dl-57-1966` 2x. Candidatos a dedupe. |

---

## 10. RECOMENDAÇÕES PRÁTICAS DERIVADAS (para desenhar o projeto)
1. Adotar a **Fórmula Mestra OO** e suas constantes (§1) como o engine canônico; versioná-la em 03-Tabelas&Engines.
2. Implementar o **Sensor FUNDURB 5%** (§2) como check de viabilidade comercial — diferencial de produto.
3. Formalizar as **3 chaves de JOIN** (§5) como data contract e padronizar a **chave SQ de 10 dígitos**.
4. Codificar a **Hierarquia de Fontes N1/N2/N3** (§6) como política de citação/grounding do RAG — só afirmar a lei a partir de N1.
5. Rodar **dedupe** guiado por `RELATORIO_DUPLICADOS_FORENSE` antes da ingestão (há muitas duplicatas `(1)..(5)` e variantes de manifesto).
6. Mapear as **6 vias de TDC** (§3) como linhas de negócio; hoje só a via "tombados" tem contrato.
7. Manter os **logs de extração** (JSON e `## ...txt`) em 00-Governança/99-Inbox como rastro de proveniência, não descartar.

---

## 11. Arquivos sem snippet legível (registrar, nunca em silêncio)
- `datageo-VWM_AREAS_CONTAMINADAS_GEODADOS_CETESB_PTO.kml` (text/xml, 1.920 bytes): `get_file_metadata` **não retornou contentSnippet** (KML não é mime de leitura nativa). Classificado por nome como geodado CETESB de áreas contaminadas (insumo da tese §8.1). Conteúdo interno não verificado — recomenda-se abrir com parser KML/`geopandas`.

Nenhum outro arquivo ficou ilegível: todos os demais 115 retornaram snippet utilizável via `get_file_metadata`.
