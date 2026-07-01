# CATÁLOGO-MESTRE DE DADOS — o que temos e o que subir (2026-07-01)

> Produzido pelo workflow `ler-inventario-dados` (4 lentes: imobiliário · geo · motor/jurídico · cético-procedência),
> sob a régua **D-DONO-4**: *adquirido de fora (confiável) × produzido por nós (não confiável)*; oficial também sobe.
> Fonte = inventário já puxado (nomes/colunas/tamanhos/procedência). O conteúdo bruto (GB) é lido depois, no Supabase.

## ✅ SUBIR — as 3 ADQUIRIDAS que o dono pediu (confirmadas)
| Arquivo | drive_id | Tamanho | Entrega |
|---|---|---|---|
| **socios.csv** | `1gftoKzFaD-NyKClBg3SH8Eo0FYncQYvt` | 3,4 GB | nome + CPF + CNPJ dos sócios (cadastro nacional adquirido) → dono/beneficiário final |
| **empresas.csv** | `1uRWg7wA4KuppJ1TSdEwRmV3H06fTXlnj` | 2,2 GB | cadastro nacional de empresas por CNPJ (par de `socios`) |
| **iptu-2020-cep01.csv** | `1AV8v4esuCxGulgxvGskzo595vycDa3U-` | 153 MB | **a "IPTU não-oficial adquirida"** (vintage 2020, recorte CEP01) — SQL/endereço/valor venal |

> ⚠️ **holdings.csv** (`1BrBRzC3G4atGZ8JqRZhGp4OnvBZTjOgr`, 60 MB) ficou **AMBÍGUO** entre as lentes — não é arquivo padrão da Receita nem tem cara das nossas consolidações. **Precisa do dono confirmar:** foi adquirido (→ sobe) ou montado por nós (→ não)?

## ✅ SUBIR — OFICIAIS (PMSP/SMUL/GeoSampa/PDE/SIRGAS), por função
**Cadastro & valor**
- `IPTU_2026.csv` (937 MB) — SQL, **área do terreno (Atc)**, valor venal, endereço. A base-mãe.
- **Quadro 14** (valor do m² para outorga): `Atualizacacao_Q14_anoref2025.csv` (vigente) + `PDE2013_SUBST2_Quadro_14_cadastro.csv` (base histórica p/ vigência 1.6).

**Transação & matrícula**
- **Série ITBI (Guias Pagas):** xlsx 2006–2024 + dumps recentes (a mais rica: SQL + **matrícula** + valor venal + ITBI) · xls legado 2000–2021.

**Proprietário (processos oficiais)**
- OODC: `oo_2002-2014.xlsx`, `oo_2014-2023.xlsx`, `OODC_2024-2025.xlsx` (traz proprietário+geo), `OUTORGA_ONEROSA.xlsx`.
- `ANUAL - 2022.xlsx` (alvarás detalhado, proprietário+SQL), série **Aprova Digital** e **SISSEL** (2023–2026).

**TDC (núcleo do projeto)**
- `lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx` + `lista_certidao_ZEPEC-BIR_agosto-2025.xlsx` + fila FUNDURB dez/2025.

**Motor de cálculo (quadros PDE) — ⭐ inclui o Fp que eu achava faltar**
- `PDE2013_SUBST2_Quadro_5_Fator_interesse_social_Fs.csv` (Fs) + **`PDE2013_SUBST2_Quadro_6_Fator_planejamento_Fp.csv` (Fp — EXISTE!)**.
- Série CA: Quadros 1/2/2A/2B/3/3A/3B/3C/4/4A/4B (CA básico/máximo por zona, eixos, macroáreas, ZEIS).

**Geo/zoneamento (a fonte OFICIAL da zona)**
- `SIRGAS_SHP_LOTES_01..96` (96 camadas, polígono do lote **com SQL**) + **Zoneamento Lei 16.402/2016** (42 camadas: ZC/ZM/ZEU/ZER/ZEIS/ZEPEC/…) + setor fiscal, quadra, logradouro.
- **Como a zona nasce (oficial):** sobreposição espacial `lote (SIRGAS_LOTES, tem SQL) ∩ zoneamento (16.402)` → zona → CA básico/máximo → engine. **Zona vinda de `*_IA` é derivada — só confere, nunca substitui (1.3).**

## ❌ NÃO SUBIR — produzidas por nós (não confiáveis, D-DONO-4)
`MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2` · `MEGA_PLANILHA_SANEADA_TOMBADOS_V1` · `PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2` · todos os `*_IA.csv` (LOTES_IA, ZONEAMENTO_IA, RUAS/PCA_Consolidado_IA, DIVERSOS_IA) · `DEEP_SCAN_*` · `AUDITORIA_1/2_*` · `MASTER_PARAMETROS_URBANISTICOS.xlsx` · `catalogo_oficiais_para_preenchimento_*` · `Notas Nilson Grotti.xlsx`.

## 3 correções que as lentes trouxeram
1. **`socios`/`empresas` NÃO são nossas** — o catálogo errou; são cadastros nacionais adquiridos → sobem.
2. **A "outra IPTU" = `iptu-2020-cep01.csv`** (adquirida, 2020, recorte CEP).
3. **O Fp (Quadro 6) EXISTE no Drive** (`PDE2013_SUBST2_Quadro_6…`) — então o B-3 (Fp) não estava bloqueado; só faltava subir. Idem toda a série de quadros CA.

## Cuidado registrado (vacina)
Dois "V" homônimos: **V-outorga** (Quadro 14, valor de referência do terreno) ≠ **V-venal** (IPTU, planta genérica). NÃO intercambiar — o engine de OODC/TDC usa o **Quadro 14**.
