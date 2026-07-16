# Estudo — o lado RECEPTOR sobre os casos reais (subsídio ao gate do MOU)

> Autônomo (2026-07-16). Responde, com **dado real**, à pergunta represada: *"o produto deve calcular o lado
> receptor (comprador)?"*. Base: os **169 casos reais** capturados (`casos-reais/tdc/certidoes-reais-ago2025.csv`),
> lista oficial DEUSO/SMUL ago/2025 — cada linha traz **área cedida-equivalente × área recebida-real**. Reproduzível:
> `python3 scripts/analise_receptor_real.py`. Nenhum número inventado (1.3).

## Veredito
**O produto deve permanecer do lado CEDENTE (vendedor).** A área que o comprador recebe **não é computável** a partir
do crédito do vendedor sem o **projeto do comprador** — porque depende do **Cr do receptor** (contrapartida de outorga,
Art. 117), que é **projeto-específico**. O que é estável, nosso e citável é o **valor do cedente** (Art. 128, piso),
**conservado** na transação. Calcular o receptor só faz sentido **sob demanda**, quando houver um receptor concreto com
seu projeto — não em massa.

## O que os dados mostram (167 transferências com as duas áreas)
| Métrica | Valor |
|---|---|
| Razão **área recebida / cedida** | mín **0,10** · mediana **1,24** · máx **21,62** |
| Receptor com terreno mais barato (recebe MAIS área) | **94** de 167 |
| Receptor com terreno mais caro (recebe MENOS área) | **70** de 167 |
| Agregado | 683.221 m² cedidos → 690.534 m² recebidos (razão **1,011**) |

A **dispersão de ordens de grandeza** (0,10 a 21,6) é o achado central: o mesmo m² de potencial cedido vira de
**um décimo** a **vinte vezes** a área no receptor, conforme o destino.

## Por que — a mecânica do Art. 128
`PCr = (PCpt × VTcd) / (Cr × CAmaxcd)` ⇒ **área recebida / área cedida = VTcd_cedente / (Cr_receptor × CAmaxcd)**.
- **VTcd_cedente** (valor do terreno do vendedor) — **nós temos** (Quadro 14, engine).
- **Cr_receptor** (contrapartida de outorga no imóvel comprador, Art. 117) — **depende do PROJETO do comprador**
  (área pretendida, uso, Fp/Fs, terreno receptor). Não é dado do vendedor.
→ Sem o Cr do receptor, a área recebida é indeterminada. É por isso que a razão real varia tanto.

## A prova nos 7 casos com valor FUNDURB
O **valor R$ é conservado** na transação; a **área converte** pela razão de valor de terreno cedente↔receptor:

| Cedente → Receptor | m² cedido | m² recebido | ×área | R$/m²ced | R$/m²rec |
|---|---:|---:|---:|---:|---:|
| Sé → Jardim Paulista | 2.217,6 | 1.373,3 | 0,62 | 1.759 | 2.841 |
| Ipiranga → Itaim Bibi | 3.870,0 | 683,2 | **0,18** | 605 | 3.429 |
| Bela Vista → Moema (A) | 601,8 | 307,2 | 0,51 | 899 | 1.760 |
| Bela Vista → Moema (B) | 324,0 | 648,0 | **2,00** | 1.797 | 899 |

Note **Bela Vista → Moema** aparecendo com razão **0,51 E 2,00** — mesmo par de distritos, sentidos opostos: prova de
que o fator decisivo é o **Cr do projeto** de cada receptor, não o par de bairros.

## Consequência para o produto (recomendação — o SE é do MOU, D21)
1. **Manter o produto cedente-side.** O dossiê e o preço legal (Art. 128) já entregam o que é estável e conservado.
2. **Receptor só sob demanda.** Se e quando um comprador concreto aparecer com seu projeto (área pretendida + uso +
   terreno receptor), aí sim roda-se o Art. 117 (Cr) + Art. 128 para dar a área recebida daquele caso — não em massa.
3. **Gancho comercial honesto:** ao vendedor, comunicar em **valor** (piso Art. 128, conservado), não em "m² que o
   comprador recebe" (que varia 200×). Isso evita promessa que a mecânica não sustenta.

## O que ficou fora (declarado)
- Não há `Cr`/projeto de receptor na base para os 140 receptores (só 2 estão no nosso cadastro) — por isso o estudo é
  sobre a **razão observada**, não sobre reconstruir cada Cr. Capturar o projeto do receptor é dado novo, sob demanda.
