# Mapa das fontes de PROPRIETÁRIO — busca profunda (frota de lentes, 2026-07-17)

> Pedido do MOU: "busca profunda, lance inúmeras lentes até achar os proprietários todos com 100% de certeza; procure em dívida, isenção, leilão, falência, inventário, empréstimos, eventos — onde mais aparecem proprietários?"
> 7 lentes varreram fontes públicas + agregadores. Este é o mapa consolidado (o dado em si nasce da fonte primária, 1.8).

## Verdade de base (o que dá "100% de certeza")
Só **um** documento prova o dono com fé pública: a **matrícula do Registro de Imóveis** (nome + CPF + ônus). Todo o resto é **pista / chave de cruzamento**. A arquitetura vencedora = **barato em massa para nomear e achar a matrícula; a certidão paga só confirma a fração que vira negócio** (espelha a doutrina 1.4 do funil de custo). **A chave-mestra que costura tudo é o SQL.**

## As fontes, por eixo (público? nome+CPF? liga ao imóvel? escala?)

### Eixo CADASTRAL (o motor de massa)
- **IPTU cadastral com NOME (safra pré-anonimização 2016/2020, GeoSampa):** SQL→**nome** (CPF completo em 2016; mascarado em 2020; anonimizado em 2026). **É o único que nomeia ~toda a lista de uma vez, de graça, por SQL.** ★★★★★ — *fonte e cobertura em decisão (ver §Decisão).*
- **IPTU_2026 (que temos):** anonimizado (só nº do contribuinte). Não nomeia.

### Eixo TRIBUTÁRIO/FISCAL
- **Diário Oficial da Cidade — Decisões de Isenção de IPTU + Decisões Tributárias:** publicam **nome + SQL** em massa (Diário Aberto JSON/CSV/API + corpus histórico 2003-2016 CC0). ★★★★ público-alvo já segmentado (idoso/entidade/templo).
- **Dívida Ativa / CADIN / CENPROT:** 1-a-1, captcha, entrada por CPF → só **qualifica** (tem dívida?) um alvo já conhecido, não descobre.

### Eixo JUDICIAL/PATRIMONIAL (leads quentes)
- **Leilões (judicial + extrajudicial Lei 9.514):** editais com **nome + CPF + matrícula + endereço**; raspável; sinal de venda forçada. ★★★ (parser de PDF).
- **Inventário/espólio (CESDI/SIGNO, grátis, por nome):** tombado em espólio = negociável. ★★★ (sinal).
- **Falência/RJ (TJSP/JUCESP):** mais CNPJ que PF.
- **Usucapião extrajudicial / desapropriação (DOE):** nomeia possuidor/ex-dono; desapropriação traz **SQL** (nome intermitente).
- **Escavador API** (~R$4,50/consulta): reverso — nome do dono → está em execução/leilão/inventário? ★★★ enriquecimento.

### Eixo SOCIETÁRIO / INSTITUCIONAL
- **JUCESP** (empresa por endereço → sócios com CPF parcial): ótimo p/ tombado que é **sede de empresa** (comum no Centro). ★★★★
- **FII/CVM:** tombados de fundo (nome do fundo).
- **Dossiês de tombamento (DPH/CONPRESP/IPHAN):** muitos **nomeiam o proprietário** no processo. ★★★★

### Eixo CONTATO/CPF (a parte que só ferramenta externa faz)
- **TSE — doações eleitorais (dado ABERTO, CSV em massa):** casa **nome → CPF** de graça (cuidado com homônimo). ★★★★ para resolver CPF.
- **Assertiva Localize:** nome/CPF/**nome+endereço** → telefone/WhatsApp/e-mail. **Vencedor do contato.**
- **BigDataCorp Pessoas:** segundo fornecedor de contato.
- **Infosimples:** **API self-service** (R$0,05–0,20/consulta, R$100 grátis) que **robotiza** IPTU-SP, Dívida Ativa, TJSP e **matrícula (ONR/ARISP)** — a camada de automação, contratar de qualquer jeito.

### Eixo REGISTRAL (a prova final)
- **ARISP/ONR (SAEC "Pesquisa de Bens" por CPF → cartório+matrícula; Matrícula Online ~R$12; Certidão ~R$77):** robotizável **pela chave do CPF/nome**, não pelo endereço/SQL puro. **GeoSampa** dá o cartório de cada SQL de graça, em lote. É a camada de "100% de certeza" para os leads quentes.

## O FUNIL recomendado (barato→caro, espelha 1.4)
```
1. IPTU cadastral com nome (safra antiga) × nossa lista, por SQL  → nomeia ~toda a lista, grátis
2. Bifurca:  PJ → JUCESP (sócios+CPF)  ·  PF/espólio → DO full-text + CESDI (inventário/usucapião)
3. Contato/CPF:  TSE (nome→CPF grátis)  +  Assertiva/BigDataCorp (telefone/e-mail)
4. Leads quentes:  cruzar com leilão/execução (Escavador) → dono motivado
5. Fecho 100%:  matrícula (ONR/ARISP via Infosimples) só nos alvos que viram negócio  → dono + ônus + espólio
```

## Decisões que sobram para o MOU
1. **Fonte do IPTU citywide-com-nome** (ver relatório no chat) — decisão de fonte + escopo.
2. **Contratar a camada externa:** Infosimples (self-service, já) + Assertiva (piloto de contato) + Escavador (leads em crise). Só o MOU contrata.
3. **Orçamento cartório:** ~R$12/matrícula nos leads quentes (ordem de R$70–150k p/ 1.700, robotizável).

## Ativos de automação a construir (dentro do nosso alcance, sem PII de terceiros em massa)
- Ingestor do **Diário Oficial** (isenções/decisões tributárias → nome+SQL) — fonte de massa legal.
- Cruzador **JUCESP por endereço** (tombado-sede → sócios).
- Cliente **Infosimples** (matrícula/IPTU/dívida por API) quando o MOU contratar.
