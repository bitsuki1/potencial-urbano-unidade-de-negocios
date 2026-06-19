# FÓRMULAS CONSOLIDADAS — ENGINE CANÔNICA "POTENCIAL URBANO" (IPTU / TDC — São Paulo)

> **Artefato:** FÓRMULA (determinística). Separado dos artefatos LEI, TABELA e TESE.
> **Gerado em:** 2026-06-18
> **Escopo:** consolidação de TODAS as versões de matrizes/oráculos que foi possível LER, com citação de fonte
> por fórmula e sinalização de divergências entre versões.
> **Regra de ouro aplicada:** nenhum número ou fórmula entra sem fonte literal; conflitos entre versões são
> sinalizados, NUNCA resolvidos; valores de tabela citados mas não presentes na fonte são marcados
> "VALOR NÃO CAPTURADO (tabela)". Fontes não lidas são registradas, não descartadas (ver seção final).

---

## 0. INVENTÁRIO DE FONTES (lidas vs. não lidas)

### 0.1 Fontes LIDAS (branch git `origin/claude/iptu-tdc-document-mapping-mjm1sn`, via `git show`, sem checkout)
| ID interno | Caminho na branch | Conteúdo relevante |
|---|---|---|
| F-A | `engines/tdc/oraculos/CONHECIMENTO_MESTRE_IA_V3.1_INABALAVEL.md` | Fórmula mestra OO; Fs/Fp; regra 5% FUNDURB; Fórmula Master |
| F-B | `engines/tdc/oraculos/CONHECIMENTO_MESTRE_IA_V3.md` | OODC (gratuidade no CA_bas); OO; 5% FUNDURB (cita Art. 24 LPUOS) |
| F-C | `engines/tdc/oraculos/ORACULO_MESTRE_RELACIONAL_V4.md` | Custo de Outorga; chaves de JOIN (SQ→V, ZONA→CA_max, PA→QA) |
| F-D | `engines/tdc/motor00/semantic_chunks_v6.1.json` | Fórmulas TDC geração/recepção (CHK_03); base legal (CHK_01) |
| F-E | `engines/tdc/motor00/travas_operacionais_v6.1.json` | Valores literais de F_i; travas (5% FUNDURB, tolerância 5%, etc.) |
| F-F | `engines/tdc/motor00/negative_prompts_v6.1.json` | Regras negativas (ZEPEC F_i estático = 1.0; base IPTU em equivalência) |
| F-G | `extracao/gems/gen1-matematico-iptu.md` (≡ `gen1-iptu.md`) | Variáveis IPTU: VVT, VVC, VMQ, Fatores Profundidade/Esquina/Obsolescência; base legal |
| F-H | `docs/CORRECOES-E-VACINAS-IPTU.md` | Correções de base legal IPTU; cadeia PGV; teto valor venal; Ross-Heidecke |
| F-I | `extracao/gems/organizacao-normativa-iptu-sp.md` | Base legal estrutural IPTU-SP |
| F-J | `docs/INVENTARIO-E-LACUNAS-IPTU-TDC.md` | Confirma OO/Fs/Fp/5% como conteúdo do MESTRE; lacunas de tabela |

### 0.2 Fontes NÃO LIDAS (Google Drive — leitura NEGADA neste ambiente)
A ferramenta `mcp__Google_Drive__read_file_content` retornou **Permission denied** para todos os file_ids.
Registradas como pendência (não descartadas):
- `CONHECIMENTO_MESTRE_IA_V3.1_INABALAVEL.md` (Drive ids divergentes entre inventários: `1cc1wa0PmSfyXfWXp7OGoFviUhmAJOD1T` no `inventario/de-para-entrada.csv`; `1uFZSNRSsgT3Q28dbCJBkPQ51us20L5wp` no `docs/INVENTARIO-E-LACUNAS`). **Conteúdo recuperado via cópia idêntica na branch git (F-A).**
- `CONHECIMENTO_MESTRE_IA_V3.md` (Drive `17gBHBK2-...` / `1nxcd_gfrJvZw61T9FzZT_9zCsvZIUU2m`). **Recuperado via branch (F-B).**
- `ORACULO_MESTRE_RELACIONAL_V4.md` (Drive `1S1r4a6fJLSXAfSwrBeZNvlSlRI0EyB2L`). **Recuperado via branch (F-C).**

### 0.3 Fontes-alvo do pedido que NÃO EXISTEM no inventário acessível
Busca textual em TODOS os CSVs de `inventario/` (`de-para-entrada.csv`, `classificacao-*.csv`) **não** encontrou
nenhum arquivo cujo nome contenha: **`MOTOR_091`**, **`MOTOR_066`**, **`documento_mestre_tdc`**, **`Mestre_IPTU`**,
**`MODULO`/`M_DULO`**, **`MATEMATICA DO LANCAMENTO`**. As "matrizes TDC v89/v90/v91" referidas no pedido **não foram
localizadas** sob esses nomes. O equivalente funcional encontrado e lido é o conjunto **motor00 v6.1** + oráculos
**V3 / V3.1 / V4** na branch git. Ver seção CONFLITOS E LACUNAS, item **L-0**.

---

# BLOCO 1 — TDC / POTENCIAL CONSTRUTIVO

## 1.1 Geração de Potencial Construtivo — ZEPEC-BIR (preservação/tombamento)

**Prosa.** Para imóvel enquadrado como ZEPEC-BIR (Bens de Interesse de Restauro / tombados), o potencial passível de
transferência é gerado pelo **Coeficiente Básico** sobre a área computável líquida, com Fator de Incentivo estático
igual a 1,0. As versões lidas são explícitas em **revogar** a antiga subtração de área `(CA_max − CA_ut)`.

```
PC_pt = Atc_Liquido × CA_bas × F_i        (com F_i = 1,0 para ZEPEC-BIR)
Atc_Liquido = Atc_Matricula − Area_Desapropriada_Averbada
```

**Variáveis:**
- `PC_pt` — Potencial Construtivo passível de Transferência (m²).
- `Atc_Liquido` — Área de Terreno Computável líquida.
- `Atc_Matricula` — área de terreno conforme matrícula.
- `Area_Desapropriada_Averbada` — área já desapropriada e averbada (subtraída).
- `CA_bas` — Coeficiente de Aproveitamento Básico do lote.
- `F_i` — Fator de Incentivo; **literal = 1,0** para ZEPEC-BIR.

**Base legal:** PDE Lei 16.050/2014; LPUOS Lei 16.402/2016; F_i estático atribuído à **Lei 17.975/2023** (F-F).
**Fonte:** F-D (CHK_03), F-E (`fator_incentivo_fi.zepec_bir = 1.0`), F-F (negative prompt nº 2 e nº 3).
**Divergência:** ver §1.5 (conflito de redação OO vs. geração) — sem conflito interno nesta fórmula entre as versões lidas.

## 1.2 Geração de Potencial Construtivo — DOAÇÃO (HIS / Viário / Parques)

**Prosa.** Na modalidade com doação, o potencial é gerado pelo Coeficiente Máximo aplicado à área, multiplicado por
um Fator de Incentivo que varia conforme a finalidade da doação.

```
PC_pt = Atc × CA_max × F_i
```

**Variáveis:**
- `PC_pt` — Potencial Construtivo passível de Transferência (m²).
- `Atc` — Área de Terreno Computável objeto da doação.
- `CA_max` — Coeficiente de Aproveitamento Máximo do lote.
- `F_i` — Fator de Incentivo, conforme finalidade.

**Valores literais de `F_i` (F-E, `travas_operacionais_v6.1.json`):**
| Modalidade | F_i (literal) |
|---|---|
| ZEPEC-BIR | 1,0 |
| Doação HIS | **1,9** |
| Doação Viário | **2,0** |
| Doação Parques (faixa de baixo valor) | 1,4 |
| Doação Parques (faixa de alto valor) | 1,0 |

Os semantic_chunks (F-D) declaram em prosa "F_i variam de 1.0 a 2.0 dependendo da modalidade" — consistente.
**Base legal:** art. 125 e 128 da Lei 16.050/2014 (PDE); Decretos 57.536/2016, 58.289/2018, 64.884/2025 (F-D CHK_01).
**Fonte:** F-D (CHK_03), F-E.
**Nota — alinhamento com o pedido:** o pedido cita "Fi 2,0/1,9" para doação — **confere** literalmente (Viário 2,0; HIS 1,9).

## 1.3 Recepção / Equivalência de Potencial Construtivo

**Prosa.** Ao receber potencial em outro lote, converte-se o potencial gerado para o potencial recebido por uma
relação de valores de terra e coeficientes entre lote cedente e lote receptor.

```
PC_r = (PC_pt × VT_cd) / (C_r × CA_maxcd)
```

**Variáveis:**
- `PC_r` — Potencial Construtivo Recebido no lote receptor (m²).
- `PC_pt` — Potencial Construtivo passível de Transferência (do cedente).
- `VT_cd` — Valor de Terra do lote cedente.
- `C_r` — coeficiente/valor de referência do lote receptor (no chunk: `C_r`; pedido grafa `C`).
- `CA_maxcd` — Coeficiente de Aproveitamento Máximo do lote cedente (grafia literal da fonte: `CA_maxcd`).

**Base legal:** PDE Lei 16.050/2014, **art. 128** (equivalência); reforçada pelo veto a usar Valor Venal de IPTU
na equivalência — usar **Quadro 14** (Valores de Terra), em conformidade com **STJ Tema 1113** e **PDE Art. 128** (F-F).
**Fonte:** F-D (CHK_03: `Recepção: PC_r = (PC_pt * VT_cd) / (C_r * CA_maxcd)`).
**Constante "4" para ZEPEC citada no pedido:** **NÃO CAPTURADA** em nenhuma fonte lida — ver L-1.
**Valor de `VT_cd` (Quadro 14):** VALOR NÃO CAPTURADO (tabela) — é insumo de CSV externo (`Atualizacacao_Q14_anoref2025.csv`, F-C), não presente como número nas fontes lidas.

## 1.4 Outorga Onerosa do Direito de Construir (OODC)

**Prosa.** A gratuidade de construção termina no Coeficiente Básico; acima dele, paga-se contrapartida ao FUNDURB.
A **mesma fórmula mestra** aparece, com grafia idêntica, em F-A, F-B e F-C.

```
OO = (Área_Adicional / CA_max) × Fp × Fs × V
```

**Variáveis:**
- `OO` — valor da contrapartida de Outorga Onerosa.
- `Área_Adicional` — área construída acima do potencial básico (a gratuidade termina em `CA_bas`, F-B).
- `CA_max` — Coeficiente de Aproveitamento Máximo.
- `Fp` — Fator de Planejamento.
- `Fs` — Fator Social.
- `V` — Valor do m² de terreno (Quadro 14 / coluna SQ; F-C).

**Valores literais de fatores (F-A, "TABELAS DE CÁLCULO (CONSTANTES)"):**
- **Fator Social (Fs):** HIS = **0,0** | HMP = **0,4 a 0,6** | R > 70 m² = **1,0**.
- **Fator Planejamento (Fp):** Arco Pinheiros/Centro/Eixos = **1,2 (R)** e **1,3 (nR)** | Macroárea de Qualificação = **0,6**.
  - (F-A grafa a faixa intermediária dos demais setores como tabela — demais valores: VALOR NÃO CAPTURADO (tabela).)

**Sobre a fórmula `C = (At/Ac) × V × Fs × Fp` citada no pedido:** essa grafia **NÃO aparece** em nenhuma fonte lida.
As três versões mestre (F-A/F-B/F-C) usam unanimemente `OO = (Área_Adicional / CA_max) × Fp × Fs × V`. Ver L-2.

**Base legal:** art. 125/128 da Lei 16.050/2014 (PDE); Lei Federal 10.257/2001 (Estatuto da Cidade); destinação ao
FUNDURB ou fundos de Operações Urbanas (F-B). 
**Fonte:** F-A (Fórmula Master + constantes), F-B, F-C, F-J (confirmação).
**Divergência inter-versões:** nenhuma na fórmula; os **valores de Fs/Fp só constam em F-A (V3.1)**; F-B/F-C citam a
fórmula sem tabelar os fatores (remetem aos "Quadros 5 e 6" — F-C). Ver L-3.

## 1.5 Regra dos 5% — Trava de Estoque FUNDURB (TDC)

**Prosa.** O potencial transferido por TDC em janela de 12 meses não pode exceder 5% da arrecadação do FUNDURB.
Há **divergência de redação** sobre a janela temporal entre as versões.

```
Σ(TDC transferida, período) ≤ 5% × Arrecadação_FUNDURB(período)
```

**Variáveis:**
- `Σ(TDC transferida, período)` — soma do potencial transferido no período de referência.
- `Arrecadação_FUNDURB(período)` — arrecadação do FUNDURB no período.
- Constante = **5%** (literal em todas as fontes; F-E `trava_estoque_fundurb_pct = 5.0`).

**Base legal:**
- F-B atribui a regra ao **Art. 24 da LPUOS** (Lei 16.402/2016) — *"Restrição FUNDURB: Limite de 5% da arrecadação anual ... (Art. 24 LPUOS)"*.
- F-A e F-D não citam artigo; F-D ancora a base normativa geral (CF 150/155; Lei 10.257/2001; PDE 16.050/2014; LPUOS 16.402/2016).
**Fonte:** F-A (II.2), F-B (III), F-D (CHK_05), F-E, F-F (negative prompt nº 6).

**Valor de referência citado (NÃO normativo, apenas exemplo em F-A):** "Arrecadação Jan-Dez/24 ≈ R$ 43,4 Mi →
Limite TDC ≈ R$ 7,8 Mi por período." Registrado como exemplo ilustrativo da fonte, **não** como constante de engine.

**CONFLITO — requer decisão humana (janela temporal):**
- **F-A (V3.1):** "últimos **12 meses**" (janela móvel implícita).
- **F-F (negative_prompts v6.1) + F-D (CHK_05):** proíbem **janela móvel**; o teto de 5% aplica-se **estritamente à
  receita do ANO FISCAL FECHADO**, respeitando o congelamento do Q1 ("Epoch Hashing").
→ V3.1 (12 meses móveis) ⟂ v6.1 (ano fiscal fechado). **CONFLITO — requer decisão humana.**

---

# BLOCO 2 — IPTU / LANÇAMENTO

> **Aviso de cobertura.** Nenhuma fonte LIDA traz a fórmula completa do IPTU escrita como equação fechada
> (`IPTU = (VVT + VVC) × alíquota` com decomposição de VVT/VVC). As fontes lidas (F-G, F-H, F-I) trazem a
> **estrutura conceitual** (Base de Cálculo × Alíquota), a **definição das variáveis e fatores**, e a **base legal**.
> A equação algébrica detalhada do pedido NÃO foi confirmada literalmente — ver L-4. O abaixo registra apenas o
> que está literalmente nas fontes, marcando o restante como não capturado.

## 2.1 Estrutura do Lançamento (Base de Cálculo × Alíquota)

**Prosa.** O IPTU é apurado como Base de Cálculo (Valor Venal) multiplicada pela alíquota. A fonte F-G (GEN-1
Matemático) define a missão como *"Desconstruir a fórmula do IPTU (Base de Cálculo × Alíquota)"* e lista as
variáveis e fatores de correção que compõem o Valor Venal.

```
IPTU = Base_de_Cálculo × Alíquota          (forma conceitual — F-G)
Base_de_Cálculo (Valor Venal) = VVT + VVC  (decomposição implícita pelas variáveis listadas em F-G; ver L-4)
```

**Variáveis e fatores (literais em F-G):**
- `VVT` — Valor Venal do Terreno.
- `VVC` — Valor Venal da Construção.
- `VMQ` — Valor Unitário de Metro Quadrado (de terreno e de construção; F-I distingue VMQ de terreno e construção).
- `Fator de Profundidade` (Profundidade Equivalente) — correção do terreno.
- `Fator de Esquina` — correção do terreno.
- `Fator de Obsolescência` — correção da construção (idade/depreciação; ver §2.4).
- `Padrão Construtivo` / Tipologia — classe da construção.
- `Área` (terreno e construída) e `Idade`.

**A composição algébrica detalhada** (`VVT = área terreno × VMQ-T × F.Profundidade × F.Esquina` e
`VVC = área construída × VMQ-C × F.Obsolescência`) **proposta no pedido NÃO aparece literalmente** em nenhuma fonte
lida — apenas as variáveis individuais. Marcada como **NÃO CAPTURADA (estrutura)** em L-4.

**Base legal (F-G, F-I):**
- **Lei 10.235/1986** — Lei-mãe da Planta Genérica de Valores (PGV) e regras de apuração do IPTU.
- **Lei 11.152/1991** — altera legislação do IPTU.
- **Lei 15.044/2009** — atualiza valores unitários de m² (VMQ) e insere novos padrões de construção.
- **Lei 6.989/1966** — lei base histórica do IPTU-SP (F-I).
- **Art. 156 da CF/1988** e **CTN (Lei 5.172/1966)** — competência tributária (F-I).
**Fonte:** F-G, F-I.

## 2.2 Valor Venal do Terreno (VVT)

**Prosa.** O VVT decorre da área do terreno e do valor unitário de m² de terreno (PGV), corrigido por fatores
geométricos do lote (profundidade, esquina). As fontes lidas **nomeiam** estes componentes, mas **não escrevem** a
multiplicação fechada.

```
VVT  ←  função(Área_terreno, VMQ_terreno, Fator_Profundidade, Fator_Esquina)
        [forma multiplicativa NÃO confirmada literalmente — ver L-4]
```
**Variáveis:** `Área_terreno`; `VMQ_terreno` (PGV); `Fator_Profundidade`; `Fator_Esquina`.
**Base legal:** Lei 10.235/1986 (PGV); cadeia PGV vigente — ver §2.5.
**Fonte:** F-G (variáveis), F-I (VMQ por m² de terreno).
**Valores de VMQ / fatores:** VALOR NÃO CAPTURADO (tabela) — são as PGVs/anexos (Lei 18.330/2025 etc.), não numéricos nas fontes lidas.

## 2.3 Valor Venal da Construção (VVC)

```
VVC  ←  função(Área_construída, VMQ_construção, Fator_Obsolescência, Padrão_Construtivo)
        [forma multiplicativa NÃO confirmada literalmente — ver L-4]
```
**Variáveis:** `Área_construída`; `VMQ_construção` (por padrão construtivo); `Fator_Obsolescência`; `Padrão_Construtivo/Tipologia`.
**Base legal:** Lei 10.235/1986; Lei 15.044/2009 (padrões de construção e VMQ).
**Fonte:** F-G, F-I.
**Valores:** VALOR NÃO CAPTURADO (tabela).

## 2.4 Fator de Obsolescência (depreciação da construção)

**Prosa.** F-H confirma que o método de depreciação aplicável é o **Ross-Heidecke**, via NBR 14653-2 (imóveis urbanos),
que é o método por trás do "Fator de Obsolescência" (idade + estado de conservação).
**Base legal/normativa:** NBR 14653-2 (imóveis urbanos, método Ross-Heidecke) — F-H, item C-6. (ABNT é paga;
registrada como pendência na fonte; a fórmula numérica do Ross-Heidecke **não** é transcrita — VALOR/EQUAÇÃO NÃO CAPTURADO.)
**Fonte:** F-H (C-6), F-G (Fator de Obsolescência como variável).

## 2.5 Cadeia da PGV (Planta Genérica de Valores) — vigência por data do fato gerador

**Prosa.** A PGV é encadeada e deve ser amarrada à redação vigente na DATA do fato gerador.
```
Lei 10.235/1986 (lei-mãe das tabelas de valores unitários)
   → Lei 15.889/2013 (revisão geral)
      → Lei 18.330/2025 (revisão vigente a partir do exercício 2026)
```
**Base legal:** Leis 10.235/1986, 15.889/2013, 18.330/2025.
**Fonte:** F-H (C-3), F-I.
**VACINA (F-H):** a 15.889/2013 é um **elo**, não "a" lei da PGV; não tratar 15.889/2013 como base única.

## 2.6 Trava / Cap do Valor Venal (benefícios)

**Prosa.** A única "trava/cap" do lançamento IPTU literalmente registrada nas fontes lidas é o **teto de valor venal
para o benefício de aposentados/pensionistas**, não um cap geral do imposto.
- **Teto de valor venal (aposentados/pensionistas):** atualizado por IPCA, **≈ R$ 1,5 milhão**; renda até 3 SM (isenção total)
  / 3–5 SM (isenção parcial). **Base legal:** Lei 11.614/1994 (consolidada pela 15.889/2013; alterada pela 17.719/2021).
- **Isenção por enchente:** limite **≈ R$ 20 mil** — Lei 17.202/2019 (+ 17.759/2022).
**Fonte:** F-H (C-5, C-1).
**Trava/cap GERAL do IPTU (limitador anual de variação do lançamento) citada no pedido:** **NÃO CAPTURADA** em
nenhuma fonte lida — ver L-5. Não inventar valor.

---

# CONFLITOS E LACUNAS

## Conflitos entre versões (CONFLITO — requer decisão humana)

- **CONF-1 — Janela da regra dos 5% FUNDURB (TDC).**
  V3.1 (F-A): "últimos **12 meses**" (janela móvel). v6.1 (F-D CHK_05 + F-F negative prompt nº 6): **proíbe janela móvel**;
  teto de 5% sobre **ano fiscal fechado** (Epoch Hashing / congelamento Q1). → **CONFLITO — requer decisão humana.**

- **CONF-2 — Grafia/identidade da fórmula de Outorga vs. equivalência (pedido × fontes).**
  O pedido sugere uma variante `C = (At/Ac) × V × Fs × Fp` para outorga e `(PC_pt × VT_cd)/(C × CA_maxcd)` para recepção.
  As fontes lidas usam **apenas** `OO = (Área_Adicional / CA_max) × Fp × Fs × V` (outorga) e
  `PC_r = (PC_pt × VT_cd)/(C_r × CA_maxcd)` (recepção). A variante `(At/Ac)` **não tem fonte** entre os documentos lidos.
  Como pode existir em matriz não localizada (v89/v90/v91), registra-se como **divergência potencial não resolvível**
  com as fontes atuais → **requer decisão humana / leitura das matrizes ausentes.**

## Lacunas e valores não capturados

- **L-0 — Matrizes/oráculos do pedido NÃO LOCALIZADOS.** Não há, em nenhum CSV de `inventario/`, arquivo com nome
  `MOTOR_091`, `MOTOR_066`, `documento_mestre_tdc`, `Mestre_IPTU`, `MODULO`/`M_DULO`, `MATEMATICA DO LANCAMENTO`.
  As "matrizes TDC v89/v90/v91" não foram encontradas sob esses rótulos. Consolidou-se a partir dos equivalentes
  funcionais lidos (motor00 v6.1 + oráculos V3/V3.1/V4). **Impacto:** não foi possível comparar v89↔v90↔v91; as
  divergências "v89 diz X / v91 diz Y" não puderam ser auditadas. Pendência de localização/entrega dessas fontes.

- **L-Drive — Google Drive não lido (permissão negada).** `read_file_content` negado para todos os file_ids.
  As 3 fontes-mestre do Drive foram recuperadas por **cópia idêntica na branch git**; demais PDFs de lei/tabela do
  Drive permanecem não lidos (não impactam fórmulas, impactam valores de tabela).

- **L-1 — Constante "4" para ZEPEC (equivalência/recepção).** Citada no pedido; **NÃO CAPTURADA** em nenhuma fonte lida.

- **L-2 — Variante de fórmula de outorga `(At/Ac)`.** Sem fonte (ver CONF-2).

- **L-3 — Tabelas Fs/Fp completas.** Só F-A (V3.1) tabela parcialmente Fs (HIS 0,0; HMP 0,4–0,6; R>70m² 1,0) e Fp
  (1,2/1,3; Qualificação 0,6). Demais faixas remetem a "Quadros 5 e 6" (CSVs) → **VALOR NÃO CAPTURADO (tabela)**.

- **L-4 — Decomposição algébrica do IPTU.** A equação fechada `IPTU = (VVT+VVC) × alíquota` com
  `VVT = área × VMQ-T × F.Profundidade × F.Esquina` e `VVC = área × VMQ-C × F.Obsolescência` **não consta literalmente**
  nas fontes lidas — apenas as variáveis isoladas (F-G) e a forma conceitual "Base × Alíquota". A montagem
  multiplicativa exata é **NÃO CAPTURADA (estrutura)**; requer parse das leis-fonte (10.235/86, 15.889/13, 18.330/25)
  ou do "Mestre IPTU" (L-0).

- **L-5 — Trava/cap geral do IPTU.** Limitador anual de variação do lançamento citado no pedido **NÃO CAPTURADO**.
  Só há os tetos de benefício (§2.6): valor venal ≈ R$ 1,5 mi (aposentados, Lei 11.614/94) e ≈ R$ 20 mil (enchente, Lei 17.202/19).

- **L-6 — Valores de VMQ e fatores IPTU (PGV).** Todos os valores numéricos de m² de terreno/construção e os
  multiplicadores de Profundidade/Esquina/Obsolescência são **VALOR NÃO CAPTURADO (tabela)** — residem nos anexos das
  leis de PGV (15.889/2013, 18.330/2025) e na NBR 14653-2, não transcritos nas fontes lidas.

- **L-7 — Quadro 14 (Valores de Terra V / VT_cd).** Insumo de OO e da recepção TDC; numérico ausente
  (CSV externo `Atualizacacao_Q14_anoref2025.csv`) → **VALOR NÃO CAPTURADO (tabela)**.

## Correções de base legal a NÃO herdar (vacinas — F-H), relevantes às fórmulas/teses IPTU
- Enchente: usar **17.202/2019 (+17.759/2022)**, não 14.493/2007.
- Tombamento: **não** há isenção genérica de IPTU; usar 12.350/1997 ("Lei das Fachadas") / Requalifica Centro 17.577/2021.
- PGV: 10.235/1986 → 15.889/2013 → 18.330/2025 (não tratar 15.889 como base única).
- STF Tema 1.084 = ARE **1.245.097** (não confundir com ARE 1.216.078 = Tema 1.062, SELIC).
