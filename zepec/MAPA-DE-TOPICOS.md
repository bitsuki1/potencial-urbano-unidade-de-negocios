# ZEPEC — mapa de tópicos (tudo que há para tratar)
> PU 14 · 2026-06-28. O painel do que falta, para escolher a próxima com clareza.
> Legenda: ✅ feito · 🔶 parcial · ⬜ a fazer · 🔒 depende de dado externo (Drive/Supabase).

## A. Dentro das planilhas ZEPEC (local, sem depender de nada)
| # | Tópico | O que falta | Status |
|---|---|---|---|
| A1 | **Saldo em m²** | hoje só sabemos esgotado sim/não; falta **quanto resta** (ligar declaração→certidões sucessivas, Art.131, e subtrair) | 🔶 |
| A2 | **Vínculo declaração↔certidão** | 49 imóveis com os dois; ligar formalmente por `N. Declaração` (cadeia A→B→C) | 🔶 |
| A3 | **Área em m²** | arredondar ruído de float (`4314.14000003 → 4314.14`) — é número-fato | ⬜ |
| A4 | **48 SQL inválidos** | conferir caso a caso (SQ não-numérico, 7 díg, quadra 2 díg) | ⬜ |
| A5 | **1 OCR suspeito** | APC "Bar Ó do Borogodó" — confirmar grafia | ⬜ |
| A6 | **1.723 datas ambíguas** | dia e mês ambos ≤12; assumimos BR — confirmar amostra | ⬜ |

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
