# Auditoria do Drive — insumos primários para a frente comercial (4 lentes, 2026-07-16)

> Pedido do MOU: "rode uma auditoria no Drive, olhe o que temos, se montaram planilhas é porque tínhamos insumo. Mande lentes, sem preguiça."
> 4 lentes varreram o inventário (`PROVENIENCIA-DE-PARA.csv` 33k arquivos + `DE-PARA-06-COMERCIAL.csv` + catálogo) e confirmaram colunas reais no Drive.
> Regra 1.8: enriquecidas (ENRIQUECIDO/FINAL/DOSSIE/MEGA/BLINDADO/_IA) são SÓ-IDEIA — mapeadas, nunca usadas como fonte.

## O que TEMOS — primários usáveis, cobertura da CIDADE INTEIRA (maior do que se pensava)

| Insumo | id (canônico) | O que dá | Cobertura | Nome do dono? |
|---|---|---|---|---|
| **IPTU_2026.csv** | `1GOBf3pOYrDATCTOfMHLdbG1Iv82kV7Qt` (dup `1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM`) | cadastro IPTU: SQL·nº contribuinte·área·valor venal·uso | **cidade toda, 2026** | ⚠️ **a confirmar** (cabeçalho não aberto — 937 MB) |
| **iptu-2020-cep01.csv(.gz)** | `1AV8v4esuCxGulgxvGskzo595vycDa3U-` / `.gz 1COZabUyMc_qh3cPnEWXleTyz9j8yE9Uf` | SQL → **NOME** do contribuinte (MOU confirmou) | **só CEP 01 / centro**, 2020 | **SIM (nome), sem CPF** |
| **Guias de ITBI** (série anual) | 2019 `1dd1x5JxHS-JAc4Grsuucn1ly-X1NT9KD` … 2024 `1DEzDLix11FtG_1lhKY1qhnXJAu23Nny_` · 2026 snapshot `1IvF7JkpiUWwGMZKaYPM9876ASF_YgjMt` · histórico 2006-2018 | SQL·**valor transação**·data·natureza·**uso(IPTU)**·**matrícula**·**cartório** | **2006→2024 + 2026** (falta **2025**) | **NÃO** (Fazenda anonimiza) |
| **SIRGAS_SHP_LOTES_01..96** | `1WpeKCsz2EcovMBUVOJH79OPE39iWNDeD` (benstombados) + 96 distritos | geometria ↔ SQL (área/quadra/lote) | **96 distritos = cidade toda** | NÃO |
| **socios.csv** | `1gftoKzFaD-NyKClBg3SH8Eo0FYncQYvt` (3,4 GB) | CNPJ → nome_socio + doc | — | CPF do sócio **MASCARADO** (`***NNNNNN**`) |
| **empresas.csv** | `1uRWg7wA4KuppJ1TSdEwRmV3H06fTXlnj` (2,3 GB) | CNPJ → razão social | — | nome de PJ |
| **holdings.csv** | `1BrBRzC3G4atGZ8JqRZhGp4OnvBZTjOgr` | CNPJ → CNPJ controlador (recursão) | — | nome PJ em cascata |
| **OUTORGA_ONEROSA.xlsx** | `17HsQr-OdwJ1wxL3Rw2El_GggZL5njj0X` | SQL·processo·valor·área — quem já compra potencial | citywide | NÃO |
| **extrato Aprova Digital** | `1s_dglYtY8C_aW4h90_rHaqAKPvtuqOEP` (2020-23) + 2024 + **2025** `1xV2lFEme4bY0f1Qqpuy83bm7Bo5d-9NV` | SQL·processo·uso·zona | citywide, **2020→2025** | NÃO |
| **listas DEUSO ZEPEC-BIR** | ago/2025 (declarações + certidões) | potencial oficial + transferências | universo TDC-BIR | parcial |

## As DUAS/TRÊS lacunas estruturais (nada no Drive resolve)
1. **NOME do dono citywide:** só sai de **cadastro IPTU** (centro confirmado; IPTU_2026 a confirmar) **ou** da **cadeia societária** (só para dono PJ). Fora disso, o SQL fica sem dono nomeado. **ITBI não tem nome.**
2. **CPF completo (em massa):** **não existe** em fonte nossa. PF: IPTU dá nome, nunca CPF. PJ: o CPF do sócio vem **mascarado** da Receita → chega-se ao **nome** do controlador, não ao CPF. → **ferramenta externa** (BigDataCorp/Assertiva/Serpro).
3. **CONTATO (telefone/e-mail):** **inexistente** no Drive. → **ferramenta externa**.

## Reenquadramento estratégico (o que a auditoria muda)
- **Fundação (temos, citywide):** SQL + valor + uso + geometria + tombamento + processo/outorga + datas. Robusto.
- **Camada dono+CPF+contato:** as **três** dependem de **ferramenta externa** (não só o contato — o **CPF também**). Logo a ferramenta (BigDataCorp/Assertiva/Serpro) não é o "último passo": é o **núcleo** da resolução de dono/contato. Alimentamos ela com **SQL/endereço** (que temos citywide) e ela devolve **dono+CPF+contato**.
- **Insumo resgatado (estava fora do radar comercial):** `SIRGAS_SHP_benstombados` (processos CONPRESP/CONDEPHAAT/IPHAN) — o gerador das colunas `bp_*` das enriquecidas; vive na camada geo, não em "06 — Comercial".

## Pendências de infra (recaptura)
- **ITBI 2025** (única lacuna da série; puxar da Fazenda).
- **ITBI 2023/2024** grandes vieram ILEGÍVEIS no catálogo (timeout) → reler via parser de xlsx.
- **IPTU_2026 (937 MB):** confirmar o cabeçalho (tem NOME ou só nº do contribuinte?) — precisa da Action (aguenta o tamanho).
- Canônicas societárias estão em "03 — Tabelas", não em "06 — Comercial" (sub-arquivadas).

## Veredito
**O Drive entrega a FUNDAÇÃO da cidade inteira (SQL·valor·uso·geometria·tombamento·processo) e o caminho até o NOME (centro via IPTU; PJ via cadeia societária).** Mas **CPF completo e CONTATO — de PF e de PJ — nunca estiveram no Drive** e exigem ferramenta externa. A conclusão prática: usar o Drive como base determinística e a ferramenta externa como núcleo de dono+CPF+contato, alimentada por SQL/endereço.

---

## Adendo — caça no GitHub público (2026-07-16): o IPTU 2020 TEM nome do dono

**Achado decisivo (prova por cabeçalho real lido em repo público):** a safra **IPTU 2020 do GeoSampa/PMSP tem 35 colunas, incluindo `NOME DO CONTRIBUINTE 1` e `2` (nome COMPLETO, em claro) + `CPF/CNPJ DO CONTRIBUINTE 1/2` (CPF MASCARADO, CNPJ tende a inteiro).** Fonte: repo `learning-crawlers/Dados-Publicos` (`GEOSAMPA/IPTU_2020.csv`), confirmado pelo repo oficial `geoinfo-smdu/cadastro-fiscal` (SMDU/PMSP). Amostra real: `... PESSOA FISICA (CPF) ; XXXXXX0214XXXX ; MARCIO MOURCHED ; ...`.

**Corrige um erro nosso:** `inventario/mapa-dados-fase2.md` dizia "IPTU não traz nome/CPF" — **errado para a safra 2020**; a causa foi ninguém ter aberto o cabeçalho (arquivo grande, "snippet vazio"), assumindo anonimização.

**Nuance crítica (muda a estratégia):** a PMSP **ANONIMIZOU** o download entre 2020 e 2026 (LGPD). Então:
- **IPTU 2020 (e 2016):** SQL → **NOME** do contribuinte + CPF parcial. ✅ (é o `iptu-2020-cep01` do dono — mas só o recorte do centro).
- **IPTU_2026:** só `NÚMERO DO CONTRIBUINTE` (anonimizado). ❌ sem nome.
→ **A safra ANTIGA (2020/2016) é mais valiosa para NOME do que a de 2026.** E ela existe citywide (todos os setores) em espelhos GeoSampa/GitHub — não só o CEP 01.

**Repos úteis achados:**
- `learning-crawlers/Dados-Publicos` — IPTU 2020 completo (35 col, com nome).
- 🔴 `hugonbgg/hugonbgg.github.io` — GeoJSON com **SQL + NOME_PROPRIETARIO + IPTU_QtdDono + IPTU_ImovelPublico** já JOINado (alguém já cruzou lote→dono).
- `geoinfo-smdu/cadastro-fiscal` (oficial SMDU), `cem-usp/dash-iptu`, `h-pgy/*`, `mateuspicanco/project-atlas-sao-paulo`, `Riverfount/ds_iptu`, `jvcanavarro/Realoque` (2016) — IPTU SP com nome no raw.
- Receita/CNPJ: `turicas/socios-brasil`, `rictom/rede-cnpj`, `basedosdados/br_rf_cnpj` — CNPJ inteiro, nome do sócio inteiro, **CPF do sócio mascarado**.

**O muro que o GitHub NÃO fura (barreira legal):** CPF **completo** e **contato** (telefone/e-mail) não existem em dado aberto — só cartório ou agregador comercial (BigDataCorp/Assertiva/Serpro).

**Ação de maior alavancagem:** conseguir a **safra 2020/2016 do IPTU citywide (todos os setores, com nome)** — dá SQL→nome da cidade inteira, de graça. O `iptu-2020-cep01` do dono é só a fatia central dessa base.
