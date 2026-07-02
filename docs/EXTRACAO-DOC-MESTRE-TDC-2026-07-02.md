# EXTRAÇÃO — DOCUMENTO MESTRE TDC → inventário de multiplicadores/redutores (2026-07-02)
> Fonte: Google Doc 'documento mestre tdc' (1,54M chars, ~40 guias, v66→v90 MASTER). REGRA: doc é MAPA, não FONTE.
> ★ VERIFICADO PELO ORQUESTRADOR contra o verbatim indexado da LPUOS 16.402 Art. 24: o caput aplica os 7 incisos
> do Fi a ZEPEC EM GERAL (§1º é conservação, não parques) → a correção do engine (7 faixas) está CONFIRMADA;
> a tese 'Tribunal Lógico' (2 incisos p/ BIR) é contradita pela lei. §5º = trava 5% FUNDURB (dispositivo confirmado).

# EXTRAÇÃO — Documento Mestre TDC (Google Doc `1LIYQZZeRp1qBPZw7EnZVcK5wJS0WHPOQZ_K5frZnsL0`)
> Extração de multiplicadores/redutores de TDC por área da cidade. Data: 2026-07-02.
> **REGRA DO PROJETO:** este doc é **MAPA, não FONTE** — nenhum fator abaixo entra no engine sem verificação contra o texto oficial da lei (coluna "Qualidade" marca o status da citação NO DOC, não a verdade legal).

## Sumário (10 linhas)

1. O doc (1,54M chars, ~25.200 linhas) NÃO é um documento único: é uma **compilação de ~40 "Guias"** — iterações de uma "Instrução Mestre de Compliance TDC-SP" (linhagem principal v66→**v90.0 MASTER**, a mais completa), uma linhagem paralela v9→v18 ("Hacks da Faria Lima"), e uma família de **memoriais paramétricos de dados** (Guias 26–33: "Bíblia da TDC", Memorial v6.1/v19, Dossiê Golden 5.2).
2. **Li integralmente**: a v90.0 MASTER (última consolidação), os memoriais paramétricos (Guias 26–33), os capítulos densos 1–6 da v75/v88/v89 (todos os vetores O.1–O.28 e R.1–R.47), e varri por grep as versões intermediárias repetidas (v67–v89) e a linhagem v9–v18 — cobertura estimada ≥95% do conteúdo único; o que ficou de fora são repetições literais entre versões.
3. Núcleo do mapeamento: **lado cedente** `PCpt = Atc × CAbas × Fi` (Art. 125 PDE / Art. 24 LPUOS) e **lado receptor** `PCr = (PCpt × VTcd) / (C × CAmaxcd)` com `C = (At/Ac) × V × Fs × Fp` (Art. 128 / Art. 117 PDE) e **constante 4** no divisor para ZEPEC (Art. 128 §1º).
4. Os multiplicadores "por área da cidade" são: **CAbas por zona** (1,0 urbano; 0,1–0,2 ZEPAM/ZPDS), **Fi por faixa de área do lote**, **V por face de quadra** (Quadro 14 + "Regra da Esquina"), **Fp por localização** (até **1,3 nos Eixos/ZEU**; **0** em certas zonas), **Fs por uso** (HIS = 0), e o **estoque distrital** (Quadros 15/16 PDE).
5. **CONFLITO INTERNO MATERIAL**: o próprio doc tem 3 posições sobre o Fi de ZEPEC-BIR — (a) Tribunal Lógico (Teses 7.1/7.17/7.23): **só 2 incisos** (1,2 ≤500m²; 1,0 >500m²), tabela de 7 incisos é EXCLUSIVA de doação de parques (§1º Art. 24); (b) memoriais de dados (Guias 28/29/31): **7 faixas regressivas aplicadas a BIR** (1,2/1,0/0,9/0,7/0,5/0,2/0,1); (c) Guia 35 (v9): Fi=1,0 fixo (refutado internamente). **O engine atual adotou (b) — precisa de verificação urgente contra a LPUOS oficial.**
6. Restrições binárias de recepção mapeadas: **OUC** (veda TDC externa — com dialética interna), **novos PIUs** (Lei 18.081/24: só dinheiro), **ZER**, **ZEPAM** (faixa onerosável inexistente), **APM** (nulidade), **risco geológico R3/R4 (PMRR)**, saturação de estoque distrital, **trava de 5% do FUNDURB**.
7. Áreas com tratamento especial: **fora dos Eixos (ZM/ZC)** +10% de CA só via TDC (Lei 18.081/24); **Arco Pinheiros** (Lei 18.222/24) prioridade/ágio; **Centro** (Requalifica Centro Lei 17.577/21: subvenção 25% + isenções; Retrofit Lei 17.919); raio de influência dos eixos ampliado p/ **700m** (Lei 17.975/23).
8. O "produto financeiro" do doc: **ágio regulatório de ~30%** — a TDC neutraliza o Fp (até 1,3) que incidiria na outorga em dinheiro → fundamenta deságio de 15–20% no balcão; concorrente direto: **10% de desconto na OODC à vista por decreto**.
9. A fórmula da contrapartida no doc (`C = At/Ac × V × Fs × Fp`, Art. 117) **diverge da grafia implementada no oodc.py** (`OO = (Área_Adicional/CA_max) × Fp × Fs × V`) — o engine registra a grafia do doc como "sem fonte"; item nº 1 de verificação contra o Art. 117 oficial.
10. Maior lacuna do engine hoje: **não existe tabela de Fp (Quadro 6 PDE) nem qualquer camada de restrição de recepção por área** — o lado receptor geográfico está inteiro descoberto.

---

## 1. Inventário completo de fatores (multiplicadores, redutores e regras por área)

Legenda lado: **CED** = cedente (afeta PCpt/valor do crédito) · **REC** = receptor (onde/quanto recebe e preço) · **BIN** = restrição binária · **PREÇO** = camada de precificação/mercado.
Qualidade: `com_base_legal_citada` / `sem_fonte` / `fonte_duvidosa` (inclui conflito interno do doc).

| # | Fator / Regra | Valor / Faixa | Área / Situação | Lado | Base legal citada NO DOC | Qualidade |
|---|---|---|---|---|---|---|
| 1 | **Fi ZEPEC-BIR (versão Tribunal Lógico)** | 1,2 (lote ≤500m²); 1,0 (>500m²) — **só 2 incisos** | Imóvel tombado ZEPEC-BIR, qualquer zona | CED | Art. 24 *caput* LPUOS (16.402/16) + Art. 125 PDE; Teses 7.1, 7.17, 7.23 (especialidade LINDB) | com_base_legal_citada — **mas conflita com #2** |
| 2 | **Fi ZEPEC-BIR (versão memoriais de dados)** | escala regressiva 7 faixas: ≤500: 1,2 · 501–2.000: 1,0 · 2.001–5.000: 0,9 · 5.001–10.000: 0,7 · 10.001–20.000: 0,5 · 20.001–50.000: 0,2 · >50.000: 0,1 ("antidumping") | idem, por área do lote | CED | "Art. 24 LPUOS (Rev. 2023)" (Guias 28/29/31/32) | **fonte_duvidosa** — contradiz #1 dentro do próprio doc; verificar redação oficial vigente do Art. 24 |
| 3 | Fi ZEPEC = 1,0 fixo | 1,0 | idem | CED | "Art. 125 PDE rev. 17.975/23" (Guia 35, v9.0) | **fonte_duvidosa** — refutado internamente pelas Teses 7.1/7.23 |
| 4 | **Fi de doação — viário/corredor** | 2,0 | doação p/ sistema viário/corredor de ônibus | CED | Art. 127 §1º PDE (Lei 17.975/23); Tese 7.34 | com_base_legal_citada |
| 5 | **Fi de doação — HIS** | 1,9 | doação de lote p/ HIS | CED | Art. 127 §1º PDE; Tese 7.34 | com_base_legal_citada |
| 6 | **Fi de doação — parques** | "tabela regressiva de 7 incisos (1,2 até 0,1 p/ >50.000m²)" | doação p/ parque municipal | CED | Art. 24 **§1º** LPUOS (Tese 7.17: exclusiva de parques) | com_base_legal_citada — diverge do engine (que usa Fi 1,4/1,0 por limiar V≤R$2.000, Art. 127 §1º IV/V); reconciliar |
| 7 | **Doação usa CAmax (não CAbas)** | `PCpt = Atc × CAmax × Fi` | qualquer doação (Art. 126) | CED | Arts. 126/127 PDE; Tese 7.21 | com_base_legal_citada |
| 8 | **CAbas por zona (redutor de origem)** | 1,0 zonas urbanas; **0,1–0,2 em ZEPAM/ZPDS** | por zona do lote cedente | CED | Quadro 3 LPUOS (Guias 28/31/32) | com_base_legal_citada |
| 9 | **Não-abatimento da área construída em BIR** | AC existente NÃO é subtraída do potencial | ZEPEC-BIR (≠ parques) | CED | Art. 124 PDE + Art. 24 LPUOS | com_base_legal_citada |
| 10 | **Regra da Esquina** | adota-se o **MAIOR** valor do Quadro 14 entre todas as testadas do lote | lotes pluri-frentistas (valuation cedente) | CED | Art. 3º, IV do Decreto 57.536/16 | com_base_legal_citada |
| 11 | **Regeneração decenal ZEPAM** | renovação do estoque: **+70% a cada 10 anos** ou **+100% a cada 15 anos** (com Atestado de Conservação) | ativos em ZEPAM | CED | Art. 123 PDE (Guias 28/29) | com_base_legal_citada (percentuais a verificar) |
| 12 | **ZEPEC-AE não gera TDC direta** | geração = 0; canaliza p/ elisão de IPTU ou uso no lote | Áreas Envoltórias | BIN (CED) | Art. 123 PDE; Tese 7.5 | com_base_legal_citada |
| 13 | Glosa preventiva de área | −7% "por segurança" sobre a área | inventário cedente | CED | nenhuma (regra interna do memorial) | **sem_fonte** |
| 14 | Glosa CAPEX restauro | R$ 1.500/m² como provisão se sem atestado de conservação | cedente sem Art. 129 cumprido | CED/PREÇO | estimativa do memorial (âncora: Art. 129 PDE) | **sem_fonte** (o gatilho Art. 129 é legal; o valor não) |
| 15 | **Parcelamento >50.000 m²** | excedente transferido em 10 parcelas anuais | grandes glebas | CED | Art. 124 §3º PDE | com_base_legal_citada (já no engine) |
| 16 | **Constante 4 no divisor** | `CAmaxcd = 4` p/ ZEPEC (densidade máxima teórica de SP); divisor "1" = fraude paramétrica | recepção de TDC de ZEPEC, toda a cidade | REC | Art. 128 §1º PDE; Teses 7.11, 7.19 | com_base_legal_citada |
| 17 | **Contrapartida C** | `C = (At/Ac) × V × Fs × Fp` | lote receptor | REC | Art. 117 PDE; Teses 7.78/7.84/7.90 | com_base_legal_citada — **grafia diverge do oodc.py; verificar Art. 117** |
| 18 | **Fs por uso (Quadro 5)** | HIS = **0** → C=0 → divisão por zero → TDC **intransferível para HIS** (Dead Capital); "double stacking" HIS+TDC = nulo | por tipologia de uso do receptor | REC/BIN | Quadro 5 PDE; Teses 7.16, 7.18, 7.42, 7.105, 7.110 | com_base_legal_citada |
| 19 | **Fp por localização** | até **1,3 nos Eixos (ZEU)**; **= 0 em certas zonas** (interrompe cálculo); alterado por revisões de PDE ("saltos de quadra") | por quadra/zona do receptor | REC | Quadros do PDE ("Quadros 1 a 14... Fatores de Planejamento"); Teses 7.37, 7.105; R.37 | com_base_legal_citada (genérica — o doc NUNCA lista a tabela completa de Fp por macroárea; extrair do Quadro 6 PDE oficial) |
| 20 | **Ágio regulatório de ~30%** | TDC converte m²-por-m² SEM aplicar Fp; outorga em dinheiro paga ×1,3 nos Eixos → título de R$10Mi quita R$13Mi; fundamenta deságio 15–20% no OTC | Eixos de Estruturação (ZEU) | PREÇO | Decreto 57.536/16 (equivalência) | com_base_legal_citada (mecânica) / o "30%" é derivação do memorial |
| 21 | **Bônus fora dos Eixos** | +10% de CA máximo **exclusivamente via TDC** (dinheiro/FUNDURB não opera nessa faixa) — "monopólio paramétrico" | ZM, ZC e zonas fora dos eixos de transporte | REC | Lei 18.081/24 (O.15; Guia 28) | com_base_legal_citada (dispositivo exato não citado — localizar artigo) |
| 22 | **Arco Pinheiros** | "área de prioridade máxima com ágio superior" (filtro de mercado) | perímetro do Arco Pinheiros | REC/PREÇO | Lei 18.222/24 | com_base_legal_citada (sem detalhe de mecanismo — verificar) |
| 23 | **OUC — vedação de TDC externa** | perímetros herméticos: equivalência só via CEPAC | todas as OUCs (Faria Lima, Água Branca etc.) | BIN | Art. 115 PDE; Tese 7.15 | com_base_legal_citada — **dialética interna**: Tese 7.91 admite TDC em OUC condicionada a "Certidão de Compatibilidade de Estoque"; P.3 ("Short no CEPAC") afirma que OUCs específicas "legislaram a conversão". Verificar OUC a OUC |
| 24 | **Novos PIUs — vedação** | contrapartida só em dinheiro; TDC vira "ativo encalhado" | novos Projetos de Intervenção Urbana pós-2024 | BIN | Lei 18.081/24 (linhagem v12–v18) | com_base_legal_citada (dispositivo não citado) |
| 25 | PIUs antigos — arbitragem | "flexibilizações paramétricas" e Fp favoráveis fora de OUC | poligonais de PIU pré-18.081 | REC | genérica (O.8) | **sem_fonte** (estratégico) |
| 26 | **ZER — vedação absoluta** | recepção vedada | Zonas Estritamente Residenciais | BIN | "Art. 131 do PDE e LPUOS" (Guia 35) | **fonte_duvidosa** — o mesmo Art. 131 é citado na Tese 7.41 como "agrupamento de saldos"; citação inconsistente, verificar |
| 27 | **ZEPAM como receptor** | CAmax limitado ao CAbas → faixa onerosável inexistente → recepção impossível (Nível 1) | ZEPAM | BIN | Tese 7.92 (legislação ambiental municipal) | com_base_legal_citada (genérica) |
| 28 | **APM — nulidade absoluta** | injeção de TDC juridicamente nula; sobrepõe-se a qualquer TIR/estoque | Área de Proteção aos Mananciais | BIN | legislação ambiental estadual; R.42, R.29, Teses 7.80/7.85; Art. 126 PDE (R.15: mananciais restringem também a GERAÇÃO) | com_base_legal_citada (genérica) |
| 29 | **Risco geológico R3/R4** | adensamento vedado | áreas mapeadas no PMRR | BIN | PMRR + legislação de edificações; R.44, Tese 7.101 | com_base_legal_citada (genérica) |
| 30 | **Estoque distrital de potencial adicional** | limite rígido por Distrito; saturação = Dead Capital; monitorar Boletim de Estoque SMUL | os 96 distritos | BIN/REC | **Quadros 15 e 16 do PDE** + Art. 115; R.36, Tese 7.35 | com_base_legal_citada |
| 31 | **Trava dos 5% (FUNDURB)** | TDC emitida ≤ 5% da arrecadação do FUNDURB (12 meses) → "fila dos 5%" | município inteiro (macro) | BIN (CED) | Art. 24 §5º LPUOS (Guia 29); Guia 28 sem citação | com_base_legal_citada (verificar §) |
| 32 | **Quota Ambiental (QA)** | injeção de TDC eleva a QA mínima exigida (CAPEX Fe); isenção só ≤500m² (fracionar p/ burlar = fraude topológica); multiplicador ambiental 0,002 → **0,07** (NCQA) | lote receptor, por perímetro de QA | REC | Quadros 3, 3A/3B/3C LPUOS; Tese 7.40; Lei 18.081/24 (NCQA) | com_base_legal_citada |
| 33 | **Cota de Solidariedade** | disparada quando TDC leva o projeto acima dos limiares; fracionar matrículas p/ escapar = desvio (janela de unidade funcional: 60 meses) | grandes empreendimentos receptores | REC | PDE (genérico); Teses 7.95, 7.108 | com_base_legal_citada (genérica) |
| 34 | **Eixo × ZEPEC-BIR (gabarito)** | incentivos de Eixo NÃO cumulam com Fi de BIR se volumetria exceder gabarito do CONPRESP/DPH | lotes tombados dentro de Eixos | BIN parcial | Tese 7.99 (parecer DPH) | com_base_legal_citada (administrativa) |
| 35 | **Faixa onerosável apenas** | TDC opera SÓ entre CAbas e CAmax; básico gratuito consome primeiro | todo receptor | REC | Tese 7.30 | com_base_legal_citada |
| 36 | **Requalifica Centro** | subvenção de até **25% do custo da obra** + isenção de ITBI e IPTU; polígono do Centro (6,4 km²) | centro de SP | CED/PREÇO | **Lei 17.577/2021** (O.17, P.5) | com_base_legal_citada |
| 37 | **Retrofit (empilhamento)** | exaurir isenções gratuitas do Retrofit primeiro; TDC só no topo; áreas isentas expurgadas do Ac ANTES (senão infla C) | centro expandido | REC | **Lei 17.919**; Tese 7.29 | com_base_legal_citada |
| 38 | **Raio de influência dos eixos = 700m** | expansão da área receptora (vetor de liquidez/demanda) | entorno de eixos de transporte | REC/PREÇO | Lei 17.975/23 (Guia 32) | com_base_legal_citada (verificar dispositivo) |
| 39 | **Dedução de garagens** | 32 m²/vaga descontados do Ac | cálculo de C no receptor | REC | Lei 18.081/24 / Art. 62 LPUOS (v75, cap. 2.2) | com_base_legal_citada |
| 40 | **Variável V (hierarquia e reajuste)** | 1º Valor de Terreno p/ Outorga (GeoSampa/Quadro 14); 2º laudo ABNT; NUNCA valor venal de IPTU. Atualização IPCA, mas decretos impõem reajuste real (ex.: Decreto 64.884/2025: +7,18%); teto de tabela citado: R$ 2.352,06/m² | por face de quadra (toda a cidade) | REC/CED | Quadro 14 + Portaria SMUL 08/2025; Teses 7.74, 7.90; R.43 | com_base_legal_citada (Decreto 64.884/2025 e teto: verificar) |
| 41 | Manipulação de testada (receptor) | protocolar com frente principal na via de MENOR V → reduz C | lotes de esquina receptores | REC/PREÇO | nenhuma (O.13 — estratégia; tensão com a Regra da Esquina do cedente) | **sem_fonte** |
| 42 | **Direito de Protocolo (cristalização)** | V, Fp, Fs e regras congelam na data do protocolo; janelas de transição = arbitragem de Fp (O.23) | todo receptor | REC | Teses 7.60, 7.73 | com_base_legal_citada (genérica) |
| 43 | 10% desconto OODC à vista | decretos dão 10% de desconto na outorga em dinheiro — comprime o spread da TDC | concorrente da TDC | PREÇO | "decretos" (linhagem v15) | **sem_fonte** (decreto não numerado) |
| 44 | Arbitragem de parques (P.6) | doar gleba periférica p/ parque → TDC valorada "no teto da tabela" → vender nos eixos (Itaim/Faria Lima) | glebas periféricas marcadas como parque no PDE (Quadro 7) | CED/PREÇO | PDE (genérico) | **fonte_duvidosa** (a indexação "ao teto" não tem dispositivo citado) |
| 45 | Sobreposição de zoneamentos | prevalece SEMPRE a norma mais restritiva (ex.: ZEPAM dentro de APM) | polígonos sobrepostos | BIN | Tese 7.107 (princípio da precaução) | com_base_legal_citada (princípio) |
| 46 | Downgrade de tombamento | reclassificação Nível 3→1 "corta o Redutor Volumétrico" sem aviso | por nível de tombamento | CED | R.27 (autarquia) | **sem_fonte** (mecânica do "redutor volumétrico" por nível nunca é detalhada) |
| 47 | Polos de Economia Criativa (Sé/República, Paulista Luz) | citados apenas como quadros processados do PDE — nenhuma regra TDC específica extraída | setor central | — | Quadros do PDE | sem_detalhe no doc |

**Observação de escopo:** o doc **não mapeia ZEIS nominalmente** (a palavra não ocorre) — HIS só aparece via Fs=0 e Fi de doação 1,9. Macroáreas do PDE também não são tabeladas fator-a-fator; o doc trata "área" via zona (LPUOS), eixo, distrito (estoque) e perímetros especiais.

## 2. Classificação por lado (resumo)

- **Cedente (PCpt / valor do crédito):** #1–15, 44, 46 — Fi (por área do lote e por finalidade de doação), CAbas por zona, CAmax na doação, não-abatimento BIR, Regra da Esquina, regeneração ZEPAM, ZEPEC-AE, parcelamento 50k, trava 5% (fila de emissão), Requalifica Centro (subvenção de CAPEX).
- **Receptor (onde/quanto/preço):** #16–22, 25, 30–43, 45 — constante 4, C (V·Fs·Fp), bônus 10% fora dos eixos, Arco Pinheiros, estoque distrital, QA, Cota de Solidariedade, garagens, faixa onerosável, retrofit, 700m, protocolo, ágio 30%.
- **Restrição binária:** OUC (#23), novos PIUs (#24), ZER (#26), ZEPAM (#27), APM (#28), R3/R4 (#29), estoque saturado (#30), trava 5% (#31), Fs=0/Fp=0 → C=0 (#18/19), gabarito DPH em eixo (#34), norma mais restritiva (#45).

## 3. Confronto com o engine atual (`engines/tdc/`)

**JÁ coberto** (pcpt.py, oodc.py, tabelas/):
- Fi escalonado Art. 24 LPUOS por área de lote (pcpt.py, correção 2026-07-02) — ⚠️ **o Tribunal Lógico do doc (Teses 7.1/7.17/7.23) sustenta que as 7 faixas valem SÓ para doação de parques (§1º) e que ZEPEC-BIR tem só 2 incisos**. Conflito direto com a correção recém-entrada. Prioridade máxima de verificação no verbatim oficial do Art. 24 (caput vs §1º, redação 18.081/24).
- Fi de doação Art. 127 §1º I–V (pcpt.py + `tabelas/fi-incentivo-doacao.csv`) — engine é MAIS completo que o doc (tem regularização 0,8 e parques 1,4/1,0 por limiar V); o doc manda parques para a "tabela regressiva de 7 incisos da LPUOS" — reconciliar as duas vias (Art. 127 §1º IV/V do PDE × Art. 24 §1º LPUOS).
- CAbas/CAmax por zona (`tabelas/quadro3-ca-por-zona.csv`) — cobre o redutor ZEPAM/ZPDS 0,1–0,2 se o CSV tiver essas zonas.
- Parcelamento >50.000 m² Art. 124 §3º (pcpt.py).
- Fs por uso (`tabelas/quadro5-fator-social-fs.csv`, HIS=0 presente) — mas o **curto-circuito C=0** (interromper e sinalizar, não calcular) não está implementado como comportamento.
- V por SQ/Codlog (`tabelas/q14-valor-terreno.csv` + `oodc_por_imovel`).
- Fórmula de recepção `PC_r = (PC_pt × VT_cd)/(C_r × CA_maxcd)` (oodc.py) — mas `CA_maxcd` é entrada livre; a **constante 4 para ZEPEC (Art. 128 §1º)** não é default nem validada.

**FALTA** (por ordem de materialidade):
1. **Fp — Fator de Planejamento por área (Quadro 6 PDE)**: nenhuma tabela no repo; é a variável geográfica central do receptor (1,3 eixos; 0 em zonas; volatilidade de transição; cristalização por protocolo). Sem ela não existe C nem o "ágio de 30%".
2. **Camada de restrições binárias de recepção por geografia**: OUC (Art. 115), novos PIUs (18.081/24), ZER, ZEPAM-receptor, APM, R3/R4 PMRR, sobreposição "mais restritiva". Hoje o engine aceita qualquer receptor.
3. **Estoque distrital (Quadros 15/16 PDE)** + Boletim de Estoque SMUL — gate de viabilidade por distrito.
4. **Trava 5% FUNDURB** (Art. 24 §5º LPUOS, a confirmar) — gate macro de emissão.
5. **Constante 4** como default/validação para ZEPEC no divisor.
6. **Divergência de fórmula C**: doc usa `C=(At/Ac)×V×Fs×Fp` (Art. 117); oodc.py implementa `OO=(Área_Adicional/CA_max)×Fp×Fs×V` e marca a outra grafia como sem fonte. Resolver contra o Art. 117 oficial (inclui a definição de Ac = "área computável total pretendida", Tese 7.90, e o CGO = C × área onerosável, Tese 7.106).
7. **Regra da Esquina** (Art. 3º IV Decreto 57.536/16): `oodc_por_imovel` recebe UM codlog; deveria tomar o MAX(V) entre todas as faces do SQ.
8. **Bônus +10% fora dos eixos via TDC** (Lei 18.081/24) — faixa exclusiva de demanda.
9. **Dedução de garagens 32m²/vaga** no Ac (Lei 18.081/24) e segregação de uso misto (Teses 7.22/7.47).
10. **Regeneração ZEPAM +70%/+100%** (Art. 123) e congelamento do V (o engine já nota Art. 123 §5º, mas não modela a renovação).
11. Quota Ambiental (recalc pós-TDC), Cota de Solidariedade, validade da DPC (5 anos, Decreto 57.536/16), vigência/cristalização por data de protocolo como parâmetro de TODAS as variáveis (Tese 7.73).

## 4. Outros materiais que o doc tem e o produto não considera (lista curta)

- **Art. 129 PDE (conservação)**: emissão condicionada a Bom Estado de Conservação + Atestado periódico; CAPEX de restauro ~R$1.500/m² como glosa; "Catch-22" DPH × Bombeiros (IT 08/2025, TRRF) que gera "ativo natimorto" — mitigação via Decreto Estadual 63.911/18 + medidas compensatórias (Tese 7.39).
- **Trâmite/prazos**: DPC caduca em 5 anos e arquiva em 30 dias de inércia (Decreto 57.536/16, R.6); latência ITCMD na SEFAZ-SP em doações (Tese 7.31); fila dos 5% do FUNDURB; CQP como quitação urbanística (não civil — Art. 618 CC, Teses 7.61/7.69).
- **Due diligence cadastral**: GDA — Gatilho de Divergência de Área (matrícula × GeoSampa; matrícula prevalece, Lei 6.015/73; >1% suspende); semáforo de liquidez (verde/amarelo/vermelho — o doc tem DUAS calibragens: 1%/5% e 5%/10% via LC 09/2003); CADIN/CNIB; não-remembramento pós-tombamento.
- **Tributário**: CTPC = intangível (IRPJ presumido base 32%, ~14% efetivo, SC COSIT 176); ITBI inexigível em balcão puro, mas incide em permuta física (segregação contratual, Teses 7.32/7.38); Tema 1113 STJ contra pauta do Quadro 14 no ITBI; Tema 796 STF (integralização); ITCMD até 8% em permuta sem torna; Art. 116 CTN antielisão.
- **Mercado/estruturação**: bancos recusam TDC como colateral ("veto da Faria Lima", R.2/R.4); risco CADE (gun-jumping por acúmulo de TDC nos eixos); CVM 175/88 (Howey, mark-to-market semestral, haircuts de iliquidez 30–45% em Monte Carlo); estratégias P.1–P.8 (endowment, escrow B3+performance bond, short CEPAC, stacking brownfield+TDC+IPTU Verde, Requalifica, landbank de parques, FII exclusivo, CRI de TDC).
- **Uso no próprio lote** (Lei 18.081/24, O.11): consome o potencial no terreno cedente sem transferência — modalidade inteira fora do produto atual.

## 5. Fração lida e ressalvas

- Conteúdo total: 1.535.481 chars / 25.214 linhas. Lidos integralmente: v90.0 MASTER (consolidação final), Guias 26–33 (memoriais paramétricos), capítulos densos 1–6 de v75/v88/v89 (O.1–O.28, R.1–R.47 completos), estratégias P.1–P.8 e vetores 2.x da linhagem v9–v18. Varredura por grep dirigido (multiplicador/redutor/Fi/Fp/Fs/eixo/arco/macroárea/OUC/PIU/ZEIS/quadro/CEPAC/desconto) sobre 100% do arquivo.
- **Potencialmente fora**: nuances de redação exclusivas das versões intermediárias v67–v89 (Guias 6–25), que são iterações do mesmo conteúdo — risco baixo de fator inédito, pois a v90 declara consolidá-las e os greps de fatores não acusaram valores fora dos já inventariados. As Teses 7.45, 7.49, 7.51–7.55, 7.65, 7.68 (revogada), 7.70–7.72, 7.81, 7.86 e 7.114–7.119 não aparecem no doc compilado (numeração com lacunas na própria fonte).
- O doc é **auto-contraditório por design** (versões dialéticas empilhadas). Os 3 conflitos que TRAVAM parametrização até verificação na lei: (a) Fi ZEPEC 2 incisos × 7 faixas × 1,0 fixo; (b) fórmula C (At/Ac × ...) × grafia do oodc.py; (c) OUC vedação total × conversão condicionada.