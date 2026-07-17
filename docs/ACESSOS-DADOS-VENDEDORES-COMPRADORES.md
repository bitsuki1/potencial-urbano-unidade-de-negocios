# Quais dados liberar acesso — listas de VENDEDORES e COMPRADORES (TDC)

> Pergunta do MOU (2026-07-15): "quais dados são importantes para eu ter acesso, para vendedores e compradores?"
> Aqui está o mapa: cada campo que você pediu → **temos?** → **fonte** → **o que falta liberar**. No fim, a lista de
> compras de acesso, priorizada pelo quanto destrava. As listas v1 (com o que já temos) já estão geradas:
> `casos-reais/tdc/LISTA-VENDEDORES.csv` (4.292 imóveis) e `LISTA-COMPRADORES.csv` (169 compras reais).

## Legenda
✅ temos e está na lista · 🟡 temos parcial/precisa refresh · 🔴 falta acesso (campo sai marcado `(PENDENTE-ACESSO)`).

---

## FRENTE A — VENDEDORES (imóveis cedentes)
| Campo que você pediu | Status | Fonte | O que falta liberar |
|---|---|---|---|
| **Imóvel** (SQL, endereço, distrito, zona, tombamento) | ✅ | IPTU 2026 + ZEPEC/DEUSO + GeoSampa | — |
| **Metragem** (terreno, PCpt, saldo vendável) | ✅ | IPTU 2026 (Atc) + engine `pcpt.py` | — |
| **Valor** (piso legal Art. 128) | ✅ | engine `art128.py` (VTcd Quadro 14) | 🟡 calibrar c/ preço real (ver Compradores) |
| **Os que JÁ foram vendidos** (m² transferido, nº operações) | ✅ | lista de Certidões DEUSO ago/2025 (80 imóveis) | 🟡 refresh 2026 p/ vendas recentes |
| **Os que NÃO foram vendidos** (INTACTO / TEM_SALDO / elegível) | ✅ | estado de venda derivado | — |
| **Data de renovação** (marcos Art. 129: 70% aos 10a, 100% aos 15a) | 🟡 | derivado da data da Declaração (554 têm) | 🔴 **datas da Declaração faltantes** + status do **Atestado de Conservação** (DPH/CONPRESP) |
| **Proprietário** (quem é o dono, PF no topo) | 🔴 | cadeia SQL→CNPJ→sócios→holdings→PF (motor PRONTO) | 🔴 **canônicas PII (sócios/empresas/holdings 5,7 GB) + ITBI** — gate PD-7, 1 disparo seu |
| **Indícios de processo em andamento** | 🟡 | temos status FUNDURB + intercorrência + CONPRESP | 🔴 **e-SAJ/TJSP (judicial) + SEI (administrativo)** — busca por CPF/CNPJ/SQL |

## FRENTE B — COMPRADORES (imóveis receptores)
> Novidade: a captura de ontem já trouxe **158 receptores reais (140 distintos)** da lista de Certidões — antes tínhamos zero.

| Campo que você pediu | Status | Fonte | O que falta liberar |
|---|---|---|---|
| **Metragem de compra** (área recebida real) | ✅ | lista de Certidões (167 de 169) | — |
| **Localização da compra** (SQL, endereço, distrito do receptor) | ✅ | lista de Certidões (158 receptores) | — |
| **Valor** (pecuniário da operação) | 🟡 | informe FUNDURB (só **7** — os grandes do teto de 5%) | 🔴 **ITBI** (valor+comprador de TODA transação) ou refresh FUNDURB completo |
| **Nome** (quem comprou) | 🔴 | mesma cadeia PII do proprietário, sobre o SQL receptor | 🔴 **canônicas PII + ITBI** (mesma liberação da Frente A) |
| **De uso** (residencial/comercial, o que fez com o potencial) | 🔴 | IPTU do receptor (só 2 de 140 no nosso recorte) | 🔴 **IPTU_2026 completo** (uso/zona por SQL) + projeto/EIV se quiser o "para quê" |

---

## O que liberar acesso — lista de compras, por prioridade (quanto destrava)

**1. Canônicas de titularidade + ITBI (o maior destrave — libera 3 campos de uma vez).**
- **Arquivos:** `socios.csv` (3,44 GB), `empresas.csv` (2,27 GB), `holdings.csv` (60 MB), **ITBI 2006–2024**. Você **já tem**
  no Drive ("03 — Tabelas & Engines").
- **Destrava:** **proprietário** (vendedor) + **nome do comprador** (receptor) + **valor+data real da compra** (ITBI).
- **Como liberar:** 1 disparo da Action `fase-b-donos.yml` no hub `portfolio-automacoes` (`confirmar=SIM` + 2 secrets) —
  carrega sob o **gate PD-7** (bucket privado, RLS deny-all). O motor `resolver_dono.py` já está pronto e verde no CI.
- **Por que é PII:** nome/CPF/CNPJ. Fica FORA do git; só a lista final enriquecida.

**2. IPTU_2026 completo (libera "de uso" do comprador + um sinal barato de dono PF).**
- **Arquivo:** `IPTU_2026.csv` (894 MB, 3,9 M linhas) — você **já tem** no Drive. Hoje usamos só o recorte dos cedentes.
- **Destrava:** **uso/zona do receptor** (o "de uso" que você pediu p/ compradores) + **contribuinte/documento** por SQL
  (colunas 26–29, que o recorte atual não extrai) — um dono-PF direto sem precisar da cadeia societária inteira.

**3. Refresh SMUL/DEUSO 2026 (libera vendas e datas recentes).**
- **Arquivos:** lista de **Certidões** + lista de **Declarações** + **informe FUNDURB** — os nossos são **ago/2025 / dez/2025**.
- **Destrava:** **quem vendeu recente**, **novas datas de referência** (marcos de renovação Art. 129) e mais **preço real**.
- **Como liberar:** o canal SMUL/DEUSO que você usou para obter as versões de 2025 (portal/gestão urbana/solicitação).

**4. e-SAJ (TJSP) + SEI (processos) — libera "processo em andamento" de verdade.**
- **Destrava:** litígio judicial (e-SAJ, busca por CPF/CNPJ/imóvel) + processo administrativo (SEI, por nº de processo).
- **Dependência:** o judicial rende mais **depois** do item 1 (buscar por nome/documento do dono). O SEI já dá para
  puxar pelos nºs de processo que a lista de Certidões traz.

**5. (Ouro, opcional) Cartório / matrícula — ARISP.**
- **Destrava:** dono **definitivo** + **ônus/penhora** sobre o imóvel e sobre o crédito de TDC (a "faca de dois gumes" da
  tese 01) + confirmação da venda. É o padrão-ouro, mas é certidão paga por imóvel — usar nos alvos quentes, não em massa.

---

## Resumo em 1 frase
Para as duas listas ficarem **completas**, o acesso nº 1 a liberar é o **pacote PII (sócios/empresas/holdings + ITBI)**
— ele sozinho preenche proprietário, nome do comprador e valor/data real da compra; o **IPTU_2026 completo** preenche o
"de uso"; o resto (SMUL 2026, e-SAJ/SEI, cartório) é refinamento e atualização. Nada disso é bloqueio de fórmula ou de
lei — é **dado**, e o motor que consome cada um já está construído e verde.
