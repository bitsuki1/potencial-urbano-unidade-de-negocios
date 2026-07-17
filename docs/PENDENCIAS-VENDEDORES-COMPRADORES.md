# Pendências das duas frentes — VENDEDORES e COMPRADORES (para destravar e decidir)

> Pedido do MOU (2026-07-16): "lista de pendências das duas frentes bem explicadas, com descritivo e sugestões, zero síntese — vamos destravar e decidir."
> Base real (nada de memória): `casos-reais/tdc/LISTA-VENDEDORES.csv` (**4.292** imóveis) e `casos-reais/tdc/LISTA-COMPRADORES.csv`
> (**169** compras reais, **140** receptores distintos). Todos os números abaixo foram contados nos próprios arquivos hoje.
> Regra de ouro **1.8** em vigor: a planilha ITBI **enriquecida** (derivada) é VEDADA como fonte — só o **ITBI bruto** (guia oficial) entra.

---

## Como ler isto
Cada pendência tem cinco linhas fixas:
- **O que é** — o campo/entrega que falta.
- **Estado hoje** — quantos dos registros já estão preenchidos (número real).
- **O que falta** — o dado/acesso concreto que está faltando.
- **O que destrava** — o que passa a ficar pronto quando você liberar.
- **Caminho + decisão sua** — como eu executo, e o que preciso que você decida/autorize.

---

# FRENTE A — VENDEDORES (imóveis cedentes) · 4.292 imóveis

### O que JÁ está pronto na lista (não é pendência — é o chão firme)
- **Imóvel:** SQL, endereço, distrito, zona, tipo ZEPEC, esfera, nome do bem — **4.292/4.292**.
- **Metragem:** área de terreno, PCpt (potencial), saldo vendável — **4.292/4.292** (engine `pcpt.py`).
- **Preço legal (piso Art. 128):** **3.334/4.292** têm valor de referência calculado. Os **958** sem valor são, quase todos,
  imóveis `SO_ELEGIVEL` sem saldo declarado ou sem VTcd na base do Quadro 14 — o motor **não inventa** (1.3).
- **Estado de venda:** `SO_ELEGIVEL` 3.659 · `INTACTO` 501 · `TEM_SALDO` 95 · `VEDADO_LEI` 28 · `ESGOTADO` 9.
- **Já vendidos:** **80** imóveis com m² já transferido (da lista de Certidões DEUSO ago/2025).

---

### PENDÊNCIA A1 — PROPRIETÁRIO (o dono, PF no topo da cadeia)
- **O que é:** o nome de quem é dono de cada imóvel cedente — a coluna que transforma a lista de imóveis em lista de **pessoas para prospectar**.
- **Estado hoje:** **0 de 4.292** (100% marcado `(PENDENTE-ACESSO)`).
- **O que falta:** o **nome/CPF/CNPJ do contribuinte por SQL não existe em nenhuma fonte primária que temos aberta.** O IPTU_2026 tem
  colunas de contribuinte (26–29), mas o **recorte que usamos hoje não as extrai**; e o ITBI **bruto** (guia oficial) que inspecionei
  **não traz nome** — só SQL + valor + data. Portanto o nome exige montar a **cadeia**: contribuinte (do IPTU_2026 completo) → CNPJ →
  `socios.csv`/`empresas.csv`/`holdings.csv` → PF no topo.
- **O que destrava:** a lista de vendedores vira **lista de leads reais** (quem procurar, e se é PF ou holding).
- **Caminho + decisão sua:** o motor `resolver_dono.py` **já está pronto e verde no CI**, e a Action `fase-b-donos.yml` que o roda está
  **construída e segurada no scratchpad**. Para eu ligar, preciso de **três coisas suas** (gate PD-7 de PII):
  1. **Consentimento explícito** de rodar o pipeline de PII (você já consentiu "dono+comprador" — falta o gate operacional).
  2. **Nomear as 2 pastas privadas do Drive** — uma de **entrada** (onde estão os recortes) e uma de **saída** (onde cai a lista final com nomes).
  3. **Confirmar os recortes de entrada:** ou você aponta `socios.csv`/`empresas.csv`/`holdings.csv` + um recorte do IPTU_2026 **com a coluna
     de contribuinte**, ou eu extraio esse recorte do IPTU_2026 completo (preciso do id do arquivo + confirmar as colunas 26–29).
  A saída é **PII** → fica **fora do git**, em bucket privado com RLS deny-all; só a lista final enriquecida, nunca o dado bruto.

### PENDÊNCIA A2 — INDÍCIO DE PROCESSO EM ANDAMENTO (litígio real)
- **O que é:** sinal de que o imóvel/dono tem processo judicial ou administrativo em curso (útil para priorizar e para a due diligence).
- **Estado hoje:** **2.747 de 4.292** marcados `(PENDENTE-ACESSO)`. Os outros **1.545** já carregam algum sinal que temos (status FUNDURB,
  intercorrência, tombamento CONPRESP) — mas isso **não é** processo judicial de verdade, é o que deu para inferir.
- **O que falta:** duas buscas externas: **e-SAJ/TJSP** (litígio judicial, busca por CPF/CNPJ/imóvel) e **SEI** (processo administrativo, por nº de processo).
- **O que destrava:** troca o "indício inferido" por **processo real citado** (nº do processo, vara, status).
- **Caminho + decisão sua:** o **SEI** já dá para puxar agora pelos nºs de processo que a lista de Certidões traz — **posso começar por aí sem depender de nada**.
  O **e-SAJ** rende muito mais **depois da A1** (buscar por nome/documento do dono). **Decisão:** autorizo começar a varredura SEI pelos nºs que já temos? (o e-SAJ eu encadeio após os nomes).

### PENDÊNCIA A3 — DATAS DE RENOVAÇÃO + ATESTADO DE CONSERVAÇÃO (Art. 129)
- **O que é:** os marcos de recarga de potencial (70% aos 10 anos, 100% aos 15 anos) e o status do Atestado de Conservação — o que diz se e quando
  o imóvel **recarrega** o crédito vendável.
- **Estado hoje:** **550 de 4.292** têm data de Declaração (a âncora dos marcos); **104** têm data de Certidão. Conservação: **4.209** `SEM_ATESTADO`,
  **66** `PENDENTE_CONSERVACAO`, **17** `ELEGIVEL`.
- **O que falta:** (a) as **datas de Declaração faltantes** (3.742 imóveis) — só vêm da lista de **Declarações** da SMUL/DEUSO; (b) o **status do Atestado
  de Conservação** por imóvel — vem do **DPH/CONPRESP** (órgão do patrimônio).
- **O que destrava:** a coluna "data de renovação" sai do "derivado quando dá" para **cravada** na maioria; e o `conservacao_art129` deixa de ser
  majoritariamente `SEM_ATESTADO` (que hoje quer dizer "não sabemos", não "não tem").
- **Caminho + decisão sua:** o dado é o **refresh SMUL/DEUSO 2026** (lista de Declarações atualizada) + uma consulta ao **DPH** para o Atestado.
  **Decisão:** você consegue puxar a lista de **Declarações** atualizada pelo mesmo canal que trouxe as de 2025? (é o que preenche isto em massa).

### PENDÊNCIA A4 — PREÇO REAL (calibrar o piso Art. 128 com valor de transação)
- **O que é:** hoje o valor na lista é o **piso legal** (Art. 128, saída de engine). O **preço realmente praticado** nas vendas é outro número —
  serve para calibrar e para o argumento comercial (o piso é o chão; o mercado paga acima).
- **Estado hoje:** o preço real **não está na lista de vendedores** (só o piso). Do lado comprador temos **7** valores (FUNDURB).
- **O que falta:** os **valores reais de transação por SQL** — que **existem no ITBI bruto** (guia oficial, SQL + valor + data), fonte **primária**, **sem nome** (não é PII).
- **O que destrava:** uma coluna "preço real observado" (quando houve ITBI) ao lado do piso legal — nas duas frentes.
- **Caminho + decisão sua:** isto é **não-PII** (SQL+valor+data, igual aos 7 FUNDURB que já estão no git). Eu baixo o ITBI bruto (guias 2006–2024),
  cruzo por SQL e preencho. **Decisão:** (1) autorizo enriquecer com o valor real do ITBI agora? (2) a saída (SQL+valor+data, **sem nome**) vai
  **no git** como os 7 FUNDURB, ou você prefere **pasta privada**? — *É a única pendência das duas frentes que eu resolvo sem tocar PII.*

### PENDÊNCIA A5 — REFRESH DE VENDAS 2026 (quem vendeu recentemente)
- **O que é:** a lista do "já vendido" e "novas datas" está no retrato de **ago/2025** (Certidões) e **dez/2025** (FUNDURB).
- **Estado hoje:** **80** imóveis marcados como já transferidos (base ago/2025).
- **O que falta:** o **refresh 2026** das listas de **Certidões** e **Declarações** da SMUL/DEUSO.
- **O que destrava:** vendas e datas recentes (2026) — mantém a lista viva em vez de um retrato de 2025.
- **Caminho + decisão sua:** mesmo canal SMUL/DEUSO do item A3. **Decisão:** vale já pedir o pacote 2026 completo (Certidões + Declarações + FUNDURB)? — resolve A3 e A5 de uma vez.

---

# FRENTE B — COMPRADORES (imóveis receptores) · 169 compras · 140 receptores distintos

### O que JÁ está pronto na lista
- **Metragem de compra** (área recebida real): **167/169**.
- **Localização** (SQL, endereço, distrito do receptor): **158/169** (11 compras antigas sem SQL legível na fonte).
- **De quem comprou** (SQL do cedente de origem): presente em todas — é o elo que liga comprador↔vendedor.
- **Quando** (nº e ano da Certidão, data de publicação): presente.

---

### PENDÊNCIA B1 — NOME DO COMPRADOR
- **O que é:** quem comprou o potencial (a pessoa/empresa do lado receptor).
- **Estado hoje:** **0 de 169** (100% `(PENDENTE-ACESSO)`).
- **O que falta:** exatamente a **mesma cadeia PII da A1**, só que aplicada ao **SQL do receptor** (contribuinte do IPTU_2026 → CNPJ → sócios → PF).
- **O que destrava:** a lista de compradores vira **lista de quem já comprou TDC** (perfil de demanda: incorporadoras, fundos, etc.).
- **Caminho + decisão sua:** **cai junto com a A1** — a mesma liberação (consentimento PD-7 + 2 pastas privadas + recortes) resolve as duas de uma vez.
  Não é um segundo pedido; é o mesmo pipeline rodando também sobre os 140 SQLs receptores.

### PENDÊNCIA B2 — VALOR DA OPERAÇÃO (quanto pagou)
- **O que é:** o valor pecuniário de cada compra de potencial.
- **Estado hoje:** **7 de 169** (só os grandes, que passaram pelo teto de 5% e viraram informe FUNDURB).
- **O que falta:** os **valores reais por SQL** — de novo, o **ITBI bruto** (primário, sem nome).
- **O que destrava:** preço real em ~toda compra que teve ITBI, não só nas 7 grandes.
- **Caminho + decisão sua:** **é a mesma A4** (ITBI bruto, não-PII). Uma decisão sua resolve A4 (vendedor) e B2 (comprador) juntas.

### PENDÊNCIA B3 — USO DO RECEPTOR (para quê usaram o potencial)
- **O que é:** o uso/zona do imóvel comprador (residencial/comercial) — o "de uso" que você pediu.
- **Estado hoje:** **0 de 169** (100% `(PENDENTE-ACESSO)`). Só **2 dos 140** receptores estão no nosso recorte de IPTU atual.
- **O que falta:** o **IPTU_2026 completo** (uso/zona por SQL). Não é PII (é uso do solo), mas é o arquivo grande (894 MB).
- **O que destrava:** o perfil de destino do potencial comprado (o "para quê") + de brinde, ajuda a A1/B1 (a coluna de contribuinte do mesmo arquivo).
- **Caminho + decisão sua:** eu preciso do **id do `IPTU_2026.csv` no Drive** (o antigo `1oX6BDTF…` do inventário **não é mais encontrado** — pode ter sido movido/renomeado
  na arrumação do Drive). **Decisão:** me confirma o id/local atual do IPTU_2026 completo? (destrava B3 e é a fonte da coluna de contribuinte da A1/B1).

### PENDÊNCIA B4 — 2 compras sem SQL / metragem
- **O que é:** 11 compras sem SQL legível e 2 sem metragem, todas certidões **antigas** (anos 1980–2000) da lista oficial.
- **Estado hoje:** 158/169 com SQL, 167/169 com metragem.
- **O que falta:** a fonte antiga não traz o dado legível; recuperar exige a Certidão física/processo daquela época.
- **O que destrava:** completude marginal (11 de 169). **Sugestão:** deixar como resíduo declarado — baixo valor, alto custo. Não recomendo caçar agora.

---

# PAINEL DE DECISÃO — o que cada "SIM" seu destrava (ordenado por quanto abre)

| # | Decisão sua | Destrava | É PII? | Depende de |
|---|---|---|---|---|
| **1** | **Preço real via ITBI bruto** (autorizar + dizer git ou pasta privada) | **A4 + B2** (preço real nas duas frentes) | **NÃO** | nada — eu já faço |
| **2** | **Ligar o pipeline PII** (consentir PD-7 + nomear 2 pastas + recortes) | **A1 + B1** (proprietário + nome do comprador) | **SIM** | recortes sócios/empresas/holdings + IPTU contribuinte |
| **3** | **Confirmar o id do IPTU_2026 completo** | **B3** (uso do receptor) + coluna de contribuinte p/ a #2 | não (uso) | id/local atual do arquivo |
| **4** | **Refresh SMUL/DEUSO 2026** (Certidões + Declarações + FUNDURB) | **A3 + A5** (datas de renovação, conservação, vendas recentes) | não | seu canal SMUL |
| **5** | **Autorizar varredura SEI** pelos nºs de processo que já temos | **A2** (processo administrativo real) | não | nada — eu já faço |
| **6** | **e-SAJ (TJSP)** por documento do dono | **A2** (litígio judicial) | usa PII | roda **após** a #2 |
| **7** | (ouro, opcional) **Cartório/matrícula ARISP** nos alvos quentes | dono definitivo + ônus/penhora | pago | só nos leads quentes |

## Minha recomendação fechada (o COMO; o SE é seu — D21)
1. **Comece pela #1** (preço real ITBI) — é a única que eu entrego **sem tocar PII**, e já melhora as duas listas. Só me diga **git ou privada**.
2. **Depois a #3** (id do IPTU_2026) — é barata, destrava o "uso" e ainda entrega a coluna de contribuinte que a #2 precisa.
3. **Então a #2** (pipeline PII) — com a coluna de contribuinte em mãos, ligo a `fase-b-donos.yml` e entrego proprietário + nome do comprador em saída privada.
4. **#4 e #5 em paralelo** (refresh SMUL + SEI) — não dependem de nada e enchem A2/A3/A5.
5. **#6 e #7** ficam para depois, sobre os leads que já estiverem quentes.

> Nada disso é bloqueio de fórmula ou de lei — **todos os motores que consomem cada dado já estão construídos e verdes**. O que falta é **dado + seu OK**.
