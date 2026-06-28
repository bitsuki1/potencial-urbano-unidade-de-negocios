# CODEX COMERCIAL TDC
> A memória do projeto comercial: o que cada termo **significa em português simples** + **as decisões que tomamos**.
> Criado por PU 14 · 2026-06-28. Documento VIVO — toda nova decisão ou termo entra aqui no mesmo instante.
> Regra de ouro: **só fato, sem juízo** (nada de "vale/não vale/melhor/pior"). **Preço nasce no engine, nunca é inventado.**

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
| R10 | **Preço nasce no engine** (Art. 125: `PCpt = Atc × CAbas × Fi`; valor `= PCpt × V`), nunca no chute | 2026-06-28 |
| R11 | **Transferiu = vendeu** quando o receptor é outro imóvel (nos dados: 155 de 169) | 2026-06-28 |

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
