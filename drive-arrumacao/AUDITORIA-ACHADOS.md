# Achados da Auditoria — Arrumação Física (2 sub-agentes, 2026-06-19)

> Registro fiel dos achados, para não se perder (RO-09). Subordinado ao Codex §7.
> Dedup aqui é **candidato**, não ordem: **versão NÃO é duplicata** (RO-12/14);
> confirmar por conteúdo antes de qualquer eliminação, sempre pós-move e com OK.
> Agentes reutilizáveis: integridade `afbaa6f52bd431bcd` · qualidade `a1046b443dad46153`.

## 1. Integridade do plano — PASSOU
- `PLAN_FILES` + `PLAN_FOLDERS` do `.gs` == `de-para-final.csv` exatamente.
- 992 itens (984 arquivos + 8 pastas). 0 ID duplicado, 0 malformado, 0 ID em dois
  destinos. IDs batem `^[A-Za-z0-9_-]{25,44}$` (32–44 chars).
- 8 pastas: ver tabela em `DECISOES.md` (AF-05).

## 2. Catalogação — sólida
- **0 enquadramentos de alta confiança errados.** Todo `.shp/.shx/.dbf/.cpg/.prj`
  e SIRGAS já em 05 Geo (geo prevalece sobre tema, inclusive ZEPEC/tombados). Nenhum
  `ec-…/dl-57-1966/emenda` fora de 2.4. PDFs de doutrina/jurisprudência IPTU em
  2.7/2.6, PDFs "MAPA" de processo de tombamento junto do processo em 2.2 — corretos.

## 3. Inconsistências de destino — mesmo título em pastas diferentes (30 grupos / 61 itens)
Padrão dominante: a versão **.pdf** foi p/ a pasta temática de Leis e a versão
**.csv** (extração tabular do mesmo doc) foi p/ **03 Tabelas**. Política recomendada
(AF-21): **manter** (PDF = norma; CSV = tabela extraída — artefatos distintos, RO-03).

**PDE — Quadros (PDF em 2.1 / CSV em 03) — 14 grupos:**
PDE2013_SUBST2_Quadro_ 1_CA_Definicoes · 2_CA_Eixos · 2A_CA_Macroareas · 3_CA_ZEIS ·
4_percentuais_ZEIS · 5_Fator_interesse_social_Fs · 6_Fator_planejamento_Fp · 7_Parques ·
8_Residuos_solidos · 9_viario-estrutural · 10_Equipamentos · 14_cadastro.

**Formulários/serviços SMUL (PDF em 2.1/2.2 / CSV em 03) — 8 grupos:**
Análise de Omissões da Legislação · Ativação de Zonas de Estruturação (ZEUP/ZEMP) ·
Certidão de Uso e Ocupação do Solo · Outorga Onerosa do Direito de Construir ·
Projeto de Intervenção Urbana · PRONUNCIAMENTO SMUL.ATECC.CTLU_001_2024 ·
RESOLUÇÃO SMUL_CTLU Nº 4/2024 · INSTRUÇÃO NORMATIVA SMUL Nº 1/2024.

**TDC/Patrimônio (PDF em 2.2 / CSV em 03) — 4 grupos:**
Auditoria TDC São Paulo_ Memorial · Declaração de Potencial Construtivo Passível de
Transferência · Transferência do Direito de Construir · fila_tdc_5porcento_fundurb_dez_2025.

**Outros cross-destino — 4 grupos:**
2014-07-31 LEI 16050 PDE (2.1/03) · Atualizacacao_Q14_anoref2025 (2.3 IPTU/03) ·
D57536 (2.5 Infralegal/03) · ANEXOS_DO_PL_586_23 (2.1/03) · `Pedido de Reconhecimento
de Complexo de Saúde` (PDF em **99** — deveria sair p/ 2.1, ver AF-22 / CSV em 03).

## 4. Cópias por nome+pasta (mesmo destino) — candidatas a dedup (RO-12: confirmar!)
- `BASE_TDC_TOMBADOS_FINAL_v1_3.csv` — 4 entradas idênticas (00).
- `SIRGAS_SHP_benstombados1` — 6 (2 sem extensão + 4 ".csv" idênticas) (05).
- `stf-sumula-539` — 6 (`(1)..(5)` + base) (2.6).
- 3 cada (`(1)(2)` + base, 2.6): stf-sumula-589/668/670/724, stf-sv-19,
  stf-tema-94/155/523/1020/1084.
- Pares `(1)`+base: IPTU-TDC_stj-tema-174, stj-tema-262,
  RELATORIO_INTELIGENCIA_TRIBUTARIA_IPTU, dl-57-1966, d833c_05_TEO_89_itens.
- Duplas exatas: Anexo_Cobranca_Recebidos_Formulas.xlsx, Gen 1 Matematico IPTU,
  Gen 2-Advogdo IPTU, PLANO DE NEGÓCIOS 5.0.pdf, Validação Memorial Técnico TDC,
  Novo TDC (3×).
- **NÃO são duplicata (linhagem/anos — RO-12/14, preservar):**
  `GUIAS_DE_ITBI_PAGAS_(2019/2020/2021)` (anos distintos); `anual_2016`+`(1)`;
  `DECRETO 63.698 ... - Copia`; `Modelo Reduzido IPTU.xlsx`+`(Converted ...)`.

## 5. Borderline (opcional — AF-23): geosampa em 03 Tabelas → poderiam ir p/ 05 Geo
biosampa_geosampa_apas.ods · dicionario_geosampa_apas.ods/.xls ·
dicionario_geosampa_apas_arquivo.csv · dicionario_geosampa_apas_variaveis.csv ·
metadados_geosampa_apas.ods. (São tabulares mas descrevem camadas geo.)
