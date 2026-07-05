# 🏛️ ORÁCULO MESTRE RELACIONAL V4 - INTELIGÊNCIA TOTAL
> **STATUS:** PERFEIÇÃO ABSOLUTA. MAPAS E TABELAS SINCRONIZADOS.

## 🔗 MOTOR DE CRUZAMENTO (JOINS)

### 1. MAPA (Lotes) <-> TABELA (Valor de Terra)
- **Chave de Mapa:** `lo_setor` (3 dígitos) + `lo_quadra` (3 dígitos) = **SQ**.
- **Chave de Tabela:** Coluna `SQ` no arquivo `Atualizacacao_Q14_anoref2025.csv`.
- **Inteligência:** Define o Valor V para o cálculo da contrapartida de Outorga Onerosa.

### 2. MAPA (Zoneamento) <-> TABELA (Parâmetros Construtivos)
- **Chave de Mapa:** Atributo `ZONA`.
- **Chave de Tabela:** Coluna `ZONA (a)` no arquivo `005 - QUADRO_3_FINAL.csv`.
- **Inteligência:** Define o Coeficiente Máximo (CA_max) e Gabarito.

### 3. MAPA (Qualificação Ambiental) <-> TABELA (Quota Ambiental)
- **Chave de Mapa:** Atributo `PA` (Perímetro Ambiental).
- **Chave de Tabela:** Coluna `Perímetro` no arquivo `006 - QUADRO_3A_FINAL.csv`.
- **Inteligência:** Define a pontuação mínima de QA necessária para o lote.

## 🧮 ALGORITMOS DE CÁLCULO INTEGRADOS
- **Custo de Outorga:** `(Área_Adicional / CA_max) * Fp * Fs * V`
  - `Fp` e `Fs` extraídos dos Quadros 5 e 6 (CSVs).
  - `V` extraído do Quadro 14 (CSV).

## 📊 VIGÊNCIA DE MERCADO
- **TDC Teto:** Consultar `fila_tdc_5porcento_fundurb_dez_2025-pdf.csv` para verificar o estoque disponível no FUNDURB antes de sugerir a venda de créditos.
