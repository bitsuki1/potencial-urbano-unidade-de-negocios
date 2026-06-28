# CODEX COMERCIAL TDC
> A memória do projeto comercial: o que cada termo **significa em português simples** + **as decisões que tomamos**.
> Criado por PU 14 · 2026-06-28. Documento VIVO — toda nova decisão ou termo entra aqui no mesmo instante.
> Regra de ouro: **só fato, sem juízo** (nada de "vale/não vale/melhor/pior"). **Preço nasce no engine, nunca é inventado.**
>
> **Os 3 codexes (separados em 2026-06-28):**
> - 🟢 **`CODEX-COMERCIAL-TDC.md`** (este) — quem/onde/estado de venda/negociável/vias de negócio/prospecção. **FOCO ATIVO.**
> - 🔵 **`CODEX-CALCULOS-TDC.md`** — as fórmulas/engines: PCpt, OODC, Fi, CAbas/CAmax (potencial em m²).
> - ⏸️ **`CODEX-PRECIFICACAO-TDC.md`** — conversão para R$ (Art. 128, V, FUNDURB-R$, IPCA). **PARADO** (parkado, não descartado).

---

## PARTE 1 — De-para dos termos (técnico → o que é, na real)

| Termo (como aparece) | O que significa, simples | Onde está nos dados |
|---|---|---|
| **TDC** (Transferência do Direito de Construir) | Vender o direito de construir que um imóvel **não vai usar** | o negócio todo |
| **Cedente** | O imóvel que **vende** o potencial (o tombado) | nossa lista |
| **Receptor** | O imóvel que **compra** o potencial | certidões |
| **Potencial construtivo** | Quantos **m²** a mais se poderia construir ali | engine / certidões |
| **Declaração** | Papel que diz: "este imóvel **tem** potencial para vender". Ainda **não vendeu** | `lista_declaracoes` |
| **Certidão (de Transferência)** | Comprovante de que **vendeu/transferiu** um pedaço para um receptor | `lista_certidao` |
| **Transferir** | Na prática, **vender** (exceto se cedente = receptor, aí é uso próprio) | certidões |
| **Saldo** | Quanto **ainda resta** para vender daquele imóvel | certidões (col. Saldo) |
| **ESGOTADO** | Já vendeu **tudo**, não resta nada | certidões (6 casos) |
| **ZEPEC** | "Selo" de Zona Especial de Preservação Cultural — é o que dá direito ao TDC | todas |
| **ZEPEC-BIR** | Bem tombado individual (gera TDC) — **é o nosso foco** | `lista_declaracoes` |
| **ZEPEC-APC** | Área de proteção cultural (um perímetro, não um lote só) | `SIRGAS_ZEPEC1` |
| **Tombado** | Protegido por lei (não pode demolir/alterar) → por isso ganha o direito de vender o que não pode construir | `benstombados` |
| **Esfera** (municipal/estadual/federal) | **Quem** tombou: CONPRESP (cidade) / CONDEPHAAT (estado) / IPHAN (federal). Mais esferas = mais órgãos na negociação | `benstombados` |
| **Conservação (art. 129)** | Atestado/Termo provando que o imóvel está **bem conservado** — condição para poder vender | certidões |
| **AUE / APPa** | Categorias que a **lei proíbe** de vender potencial (Art. 124 §2º) | `benstombados` |
| **SQL** | O "CPF do imóvel" (setor-quadra-lote) — a chave que liga tudo | todas |
| **SQL_MESTRE** | O SQL no nosso padrão: 10 dígitos, sem pontos | base unificada |
| **V (Quadro 14)** | Valor do **m² do terreno** — entra no preço | já em mãos |
| **CAbas** (coef. básico) | Quanto se pode construir "de graça" — entra no cálculo do potencial | já em mãos (Q3) |
| **OODC** (Outorga Onerosa) | O lado **oposto**: pagar à prefeitura para construir além do básico — **não é nosso foco agora** | — |
| **FUNDURB / teto 5%** | "Fila/limite" de mercado do município — quanto de TDC cabe por período | a observar |

---

## PARTE 2 — Nossas resoluções (o que já foi decidido)

| # | Decisão | Quando |
|---|---|---|
| R1 | Foco = lado **CEDENTE** (vender créditos), não o receptor | 2026-06-28 |
| R2 | **Agnóstico**: só fato, sem opinião, sem "vale/melhor/pior" | 2026-06-28 |
| R3 | A lista oficial **é** a ZEPEC; nós só **enriquecemos** (não inventamos) | 2026-06-28 |
| R4 | Unir as 4 fontes oficiais **com TAG** de origem | 2026-06-28 |
| R5 | **Valor venal entra** como fato cadastral (sem rótulo de juízo) | 2026-06-28 |
| R6 | **Sócios/PII por último** | 2026-06-28 |
| R7 | **Grão = 1 linha por SQL**; endereço com várias ruas **não explode** (é o mesmo imóvel de esquina). Só o **lote** explode | 2026-06-28 |
| R8 | Endereço **sem tipo** na fonte: manter como veio (não inventar) | 2026-06-28 |
| R9 | Datas → **ISO** (AAAA-MM-DD); série do Excel convertida; US/BR desambiguado; ambíguo = assume BR e marca | 2026-06-28 |
| R11 | **Transferiu = vendeu** quando o receptor é outro imóvel (nos dados: 155 de 169) | 2026-06-28 |
| R12 | **Parâmetro de certeza** (`estado_venda` + `certeza`). **Regra de ouro:** só marca "pular" quando o **ESGOTADO está escrito**; falta de dado = **verificar**, nunca "morto". Evidência real (vendeu/declarou) pesa mais que inferência de categoria | 2026-06-28 |
| R15 | **"Transferiu = vendeu" só vale SEM doação (Art. 125).** Na **doação** (Art. 126/127) transferir **não é venda** — o dono doa o imóvel à PMSP e recebe potencial (fórmula `Atc×CAmax×Fi`, Fi até 2,0). A via de doação é alavanca à parte (auditoria dos agentes 2026-06-28) | 2026-06-28 |
| R18 | **DUAS vias de gerar TDC como ALAVANCA DE NEGÓCIO:** **SEM doação** (dono FICA com o imóvel — caso ZEPEC, nosso foco) e **COM doação** (dono DOA o imóvel e recebe ~8× mais potencial). **⚠️ O universo da doação é DISJUNTO da lista ZEPEC** (doadores de parque/corredor/HIS, **não** tombados) — não confundir. _(Fórmulas no Codex Cálculos.)_ | 2026-06-28 |
| R13 | **Negociabilidade só com PROVA** (`negociavel` = sim/nao/verificar). **NÃO** só por escrito: `esgotado` ou `vedado` (categoria AUE/APPa). **Suspeita** (nome de bairro/bem público, sem lote, marca de Operação Urbana) → **verificar, nunca exclui** — não temos o campo "dono", então "é público" é suspeita, não certeza. **Declarou/vendeu vence a suspeita** (= sim) | 2026-06-28 |

> **Resoluções de cálculo/preço foram REALOCADAS** (2026-06-28): R10, R14 → `CODEX-CALCULOS-TDC.md`; R16, R17 → `CODEX-PRECIFICACAO-TDC.md`. Nada se perdeu, só foi para o codex certo.

**Ainda A OBSERVAR (não mexido):** vínculo declaração↔certidão (49 imóveis) · saldo/ESGOTADO · área em m² (arredondar float) · os 48 SQL inválidos · resolver SQL dos 1.791 sem cadastro (externo).

---

## PARTE 3 — Onde está cada coisa

| Arquivo | É |
|---|---|
| `zepec/raw/` | as 4 planilhas oficiais ZEPEC (verbatim do Drive) + `PROVENIENCIA.md` |
| `zepec/limpo/zepec_unificada.csv` | a base **unificada e limpa** (7.175 linhas, com tag, SQL_MESTRE, endereço e data padronizados) |
| `zepec/montar_base.py` | o programa que monta a base |
| `zepec/ETAPAS-E-ENRIQUECIMENTO.md` | as etapas do trabalho + o que dá para enriquecer |
| `zepec/VERIFICACAO-2026-06-28.md` | o que foi verificado/estudado (SQL inválido, OCR, vínculo…) |
| `zepec/A-OBSERVAR-USOS.md` | os itens a observar e para que servem (venda/precificação) |
| **`zepec/ferramenta/zepec_cedentes.csv`** | **A FERRAMENTA** — 1 linha por imóvel, só o que importa, com estado de venda e certeza |
| `zepec/montar_ferramenta.py` | o programa que monta a ferramenta |

---

## PARTE 4 — A FERRAMENTA (`zepec/ferramenta/zepec_cedentes.csv`)
O destino de tudo: uma planilha **enxuta, 1 linha por imóvel**, com só o que se precisa para agir.
**Colunas:** `sql_mestre · nome_bem · endereco_mestre · distrito · tipo_zepec · esfera · estado_venda · certeza · negociavel · motivo_negociavel · sinais_revisar · tem_declaracao · tem_certidao · esgotado · data_ref · obs`.

### Negociável por nós? (R13 — só com prova)
| negociavel | Quando | Nº (2026-06-28) |
|---|---|---|
| **nao** | prova escrita: `esgotado` (6) ou `vedado` AUE/APPa (32) | **38** |
| **sim** | declarou/vendeu (prova) ou lote limpo sem sinal contrário | **2.757** |
| **verificar** | tem **sinal** (sem lote · nome de bairro/área · nome de bem público · marca de Operação Urbana) mas **não prova** → conferir, não excluir | **3.336** |

> **Por que tantos "verificar":** "Bairro da X" (área inteira, sem lote) e bens com cara de público. Como **não temos o dono**, não dá para afirmar — vai para conferência. **Prontos para abordar** (negociável=sim + INTACTO/TEM_SALDO) = **599**.

### Os 6 estados de venda (o que cada um quer dizer e o que fazer)
| estado_venda | O que é | Fazer | Certeza | Nº (2026-06-28) |
|---|---|---|---|---|
| **INTACTO** | Declarou e **nunca vendeu** — potencial cheio | abordar | alta | **501** |
| **TEM_SALDO** | Vendeu parte, **ainda resta** | abordar (calcular o que resta) | média | **98** |
| **SO_ELEGIVEL** | Tombado que **ainda não declarou** | abordar (precisa declarar antes) | média | **3.659** |
| **INCERTO** | Falta dado/SQL | **verificar antes** — não dispensar | baixa | **1.839** |
| **VEDADO_LEI** | Categoria AUE/APPa — lei proíbe ceder | pular | alta | **28** |
| **ESGOTADO** | Vendeu **tudo** | pular | alta | **6** |

> Total: **6.131 imóveis**. Só **6** estão provadamente esgotados — o resto **não** está, então quase ninguém se dispensa de cara.

---

## PARTE 5 — Vias de negócio e prospecção (garimpado dos codexes antigos, 2026-06-28)

### 5.1 — As 6 vias de geração de TDC = 6 linhas de negócio
São as 6 formas de um imóvel gerar potencial transferível. **Hoje só a via 1 é explorada comercialmente** — as outras 5 são **mercado de expansão** (substrato geográfico já mapeado nos oráculos):
| Via | Fonte de potencial | Status comercial |
|---|---|---|
| **1. Preservação cultural (tombados/ZEPEC)** | nossa lista de 6.131 | **explorada** (contrato vigente) |
| 2. Preservação ambiental (ZEPAM) | camadas ZEPAM | expansão |
| 3. Regularização fundiária | ZEIS/baixa renda | expansão |
| 4. Provisão de HIS | ZEIS | expansão |
| 5. Parques planejados | Quadro 7 do PDE | expansão |
| 6. Melhoramentos viários (corredores de ônibus) | perímetros viários | expansão |
> Vias 2-6 = doadores de terreno (via COM doação, Codex Cálculos R18), **público disjunto do ZEPEC**.

### 5.2 — Modelo de negócio vigente
**Contrato de Gestão Comercial (OPIT-SP / Bairro Vivo)** foca na **via 1** (captação de tombados para emitir TDC). _(Origem: `inventario/ideias-estrategia.md`.)_

### 5.3 — FUNDURB como SENSOR DE LIQUIDEZ (passo de processo comercial)
Antes de **sugerir uma venda**, consultar o estoque/janela do FUNDURB (`zepec/limpo/fundurb_processos.csv`): se a fila está saturada (teto 5%), não há janela de mercado agora. **Não basta ter o potencial — é preciso haver liquidez para vendê-lo.** _(O valor em R$ é regulatório e vive no Codex Precificação; aqui é só o sinal "tem janela?".)_

### 5.4 — Score de Oportunidade geográfico (quem abordar primeiro)
Prioridade de prospecção por localização: **Arco Pinheiros** (Lei 18.222/2024) e **Eixos de 700m** (Lei 17.975/2023) — onde o Fp é maior, o crédito vale mais. Regra ortogonal aos 6 estados de venda. _(Origem: `CONHECIMENTO_MESTRE_IA_V3/V3.1`.)_

### 5.5 — Timing de mercado
- **Arco Pinheiros = "Vetor de Valorização 2026"** (Lei 18.222/2024) — janela de timing.
- **Setor Central = isenção de outorga** (Lei 17.844/2022).
