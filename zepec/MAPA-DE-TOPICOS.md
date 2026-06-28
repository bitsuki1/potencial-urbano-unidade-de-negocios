# ZEPEC — mapa de tópicos (tudo que há para tratar)
> PU 14 · 2026-06-28. O painel do que falta, para escolher a próxima com clareza.
> Legenda: ✅ feito · 🔶 parcial · ⬜ a fazer · 🔒 depende de dado externo (Drive/Supabase).

## A. Dentro das planilhas ZEPEC (local, sem depender de nada)
| # | Tópico | O que falta | Status |
|---|---|---|---|
| A1 | **Saldo em m²** | **já transferido** ligado por imóvel (`m2_ja_transferido`); *quanto resta* depende do potencial original (engine/C2) | 🔶 |
| A2 | **Vínculo declaração↔certidão** | ✅ 49 imóveis ligados → `zepec/limpo/vinculo_por_imovel.csv` | ✅ |
| A3 | **Área em m²** | arredondado na ferramenta (0 ruído) | ✅ |
| A4 | **48 SQL inválidos** | em fila `zepec/limpo/_revisar_sql_invalido.csv` (ancorada no endereço; resolver por geo) — não inventamos | 🔶 |
| A5 | **1 OCR suspeito** | APC "Bar Ó do Borogodó" sinalizado (provável "Bar do Borogodó") | 🔶 |
| A6 | **1.723 datas ambíguas** | convenção fixada: BR (dia/mês), padrão PMSP; marcadas em `data_amb`; amostra confere | ✅ |

## B. Negociabilidade — fechar os "verificar" (3.336)
| # | Tópico | O que falta | Status |
|---|---|---|---|
| B1 | **Confirmar dono público** | hoje é suspeita por nome; precisa de fonte de **titularidade** para virar "não" com prova | 🔒 |
| B2 | **Perímetros de Operação Urbana (OUC)** | mapear os perímetros reais (quem está dentro usa **CEPAC**, não TDC) — só achamos 4 por certidão | 🔒 |
| B3 | **Confirmar AUE/APPa por geo** | hoje vem da categoria do cadastro; cruzar com o overlay de zoneamento confirma | 🔒 |

## C. Enriquecer com fontes externas (por SQL)
| # | Tópico | Para quê | Status |
|---|---|---|---|
| C1 | **Resolver SQL por endereço** | dar SQL aos 1.791 sem cadastro (geocodificar) | 🔒 |
| C2 | **IPTU: Atc (área do terreno)** | **destrava a precificação** (entra na fórmula Art.125) | 🔒 |
| C3 | **IPTU: uso, área construída, valor venal, CEP** | qualificar e completar endereço | 🔒 |
| C4 | **Zoneamento: CAbas por imóvel** | entra na fórmula de potencial | 🔶 (Q3 já temos por zona; falta a zona do lote) |
| C5 | **Proprietário → CNPJ → sócios** | contato/abordagem (PII) | 🔒 **por último (R6)** |
| C6 | **Matrícula (via ITBI)** | due diligence/cartório | 🔒 |

## D. Precificação (engine — número nasce aqui, R10)
| # | Tópico | O que falta | Status |
|---|---|---|---|
| D1 | **Engine de potencial** | `PCpt = Atc × CAbas × Fi` (Art.125) — falta só o **Atc** (C2) | 🔒 |
| D2 | **Valor** | `= PCpt × V` (V do Quadro 14, **já temos**) na data de referência | 🔶 |
| D3 | **Comparáveis de mercado** | usar as **167 áreas transacionadas** das certidões como referência factual | ⬜ (local!) |

## G. Descobrir os PROPRIETÁRIOS (pergunta-chave — como achar o dono)
> **Fato duro:** a planilha **IPTU 2026 NÃO traz o dono** (nem nome, nem CPF/CNPJ) — é padrão da PMSP. O dono vem por outras vias, e a cobertura é **parcial**.
| # | Via | O que entrega | Limite |
|---|---|---|---|
| G1 | **SISSEL / alvarás / OODC** (por SQL) | nome do proprietário onde houve processo | só quem teve processo |
| G2 | **Processo do TDC** (o `N. processo` que já temos) | o requerente da declaração/certidão **é o dono** | precisa consultar o processo SEI |
| G3 | **Nome → empresas/socios/holdings** | CNPJ e sócios (PJ) | match por nome = ruidoso |
| G4 | **ITBI** (por SQL) | matrícula + quem transacionou | só imóveis com ITBI |
| — | **PF sem processo** | — | **não há fonte direta de CPF** |
> Estratégia: cruzar nosso universo ZEPEC (por SQL) com G1/G4 → nome; nome → G3 → CNPJ/sócios; o resto fica **"dono a descobrir"**. **R6: sócios/PII por último.**

## H. O que o IPTU 2026 agrega (resposta direta)
Muito — é a espinha. Por SQL entrega: **Atc (área do terreno)** → destrava o preço · área construída (quanto já se usou) · **uso e padrão** · **valor venal** · CEP e endereço oficial. **Só não traz o dono** (ver G).

> **Correção importante no passo 1:** o **saldo *remanescente* em m²** (quanto AINDA resta) **não sai destas planilhas** — falta o potencial *original* da declaração (que não está na lista; nasce do engine `Atc × CAbas`). O que É local: **quanto cada um JÁ transferiu** (feito: coluna `m2_ja_transferido`) + os comparáveis. O "quanto resta" entra junto com o engine (C2/D1).

## I. Inventário do Drive — o que temos e para que serve (já catalogado: 170 planilhas)
> Fonte: `inventario/classificacao-planilhas.csv` + `inventario/mapa-dados-fase2.md` (instâncias anteriores). **Não precisamos de extensão de navegador** — temos o catálogo + leitura MCP do Drive.
| Acervo | Qtd | Serve para |
|---|---|---|
| **ITBI** (2000–2024 + 2026) | **45** | **dono que transacionou** · **data da venda** · valor de transação · **matrícula** |
| Lote / geo / zoneamento (SIRGAS) | 38 | resolver SQL por geo · zona/CAbas por lote · perímetros (AUE/APPa/OUC) |
| Quadros / parâmetros / simuladores | 31 | tabelas do engine (CA, Fp, Fs, QA) |
| Licenciamento (Aprova Digital) | 16 | proprietário · obras · uso |
| Áreas contaminadas | 13 | due diligence ambiental (ZEPAM/risco) |
| Tombado / ZEPEC | 13 | nosso universo (+ extras a conferir) |
| Alvarás | 12 | proprietário |
| Outorga / OODC | 9 | histórico de outorga · valores |
| **FUNDURB / fila TDC** | 8 | **teto/estoque de mercado** · prestação de contas |
| IPTU (2026 + recortes) | 6 | **Atc** · uso · valor venal · CEP |
| Sócios / empresas / holdings | 6 | CNPJ · sócios (R6, por último) |
| SISSEL | 5 | proprietário + processo |

**Como "ver" tudo sem extensão:** (1) o catálogo já é o índice; (2) leitura direta via MCP do Drive (autorizada); (3) para puxar/filtrar séries grandes (ex.: cruzar ITBI com nossos SQL), **subagentes** fazem a leitura pesada e devolvem só o recorte — sem inchar o contexto. Browser-extension só se você quiser; não é necessário.

## J. Data da venda → RENOVAÇÃO e vigência (você levantou)
A data que já temos (`data_pub_iso`) serve para: **(a)** idade da declaração; **(b)** **janela de renovação** (ZEPAM: Art.123 §5º — 70% aos 10 anos, 100% aos 15 anos); **(c)** qual **V (Quadro 14)** vale (o da data de referência, Art.125 §1º). → relevante para reabordar quem está perto de renovar.

## K. Intercorrências / red flags (você levantou — risco do lead)
| Sinal de risco | Onde achar | Status |
|---|---|---|
| Declaração/processo **arquivado, indeferido, cancelado** | `Situação`/`Status` + processo SEI (já temos o nº) | 🔶 (campo local + consulta) |
| **Falta de conservação** (Art.129) → não emite certidão | coluna `Conservação` (Atestado×Termo×vazio) | 🔶 local |
| **TCA/obrigação ambiental** não cumprida (ZEPAM) | FUNDURB/SVMA | 🔒 |
| **Falta de prestação de contas** | planilhas FUNDURB (8) | 🔒 |
| **IPTU em dívida ativa** | IPTU/dívida | 🔒 |
| Embargo / fiscalização de obra | licenciamento | 🔒 |
> Regra mantida (R13): red flag só vira "não/risco" **com prova**; suspeita → verificar.

## D4. m² transferido = VALIDAÇÃO do engine (você levantou — importante)
As **167 áreas já transferidas** (col `m2_ja_transferido`) são **gabarito real**: quando o engine calcular `PCpt = Atc × CAbas`, o resultado tem de **bater** com o que foi efetivamente transferido. Vira o **teste do método** (como `evals/ground-truth` do projeto). → eleva para resolução **R14**.

## E. Produto / entrega
| # | Tópico | O que falta | Status |
|---|---|---|---|
| E1 | **Formato de entrega** | como o time comercial usa a ferramenta (filtros/visão/planilha final) | ⬜ |
| E2 | **Atualização** | as planilhas são de **agosto/2025**; rotina de re-puxar quando a Prefeitura atualizar | ⬜ |

## F. Governança
| # | Tópico | Status |
|---|---|---|
| F1 | Atualizar B-20 no BACKLOG com o estado real | ⬜ |
| F2 | Fechar a instância (registro + gate `fechar-instancia.py`) ao encerrar | ⬜ |

---
## Recomendação de ordem (do mais valor com menos dependência)
1. **A1+A2+D3 (local, agora):** fechar **saldo em m²** + vínculo + **comparáveis** das 167 transações → a ferramenta passa a dizer *quanto* cada um ainda tem para vender e *a quanto* o mercado transaciona. Tudo sem depender do Drive.
2. **A3/A4/A5/A6 (local, rápido):** higiene final (float, SQL inválido, OCR, datas).
3. **C2 → D1/D2 (externo):** abrir o **Atc do IPTU** para ligar o **engine de preço** — é o maior destravamento, mas precisa de dado pesado.
4. **B1/B2 (externo):** fechar os "verificar" com titularidade + perímetros OUC.
5. **E1 (entrega)** e **F (fechar instância)**.
