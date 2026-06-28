# ENRIQUECIMENTO — Planilhas ZEPEC (a lista oficial de cedentes)
> Orquestrador do Potencial Urbano (PU 14) · 2026-06-28 · direção do MOU.
> **Princípio (1.2):** a lista oficial **é** a planilha ZEPEC. Nós **só enriquecemos** — extrair puro → enriquecer, sem argumentar.
> **Restrições do MOU (2026-06-28):** **AGNÓSTICO** — sem opinião, sem **valor** (nada de OODC/PCpt/score/preço aqui), sem **cruzar com lista receptora**.
> **Doutrina aplicada:** proveniência temporal **por campo** (Fase 2) · conflito → mais recente vence, guarda histórico · oficialidade como lei, derivado como alerta (D-03/D-04) · nada se descarta · citação da fonte por campo.
> **Natureza:** PLANO de enriquecimento (schema + camadas + ordem). Não executa nada — desenha o quê/de-onde/como-provar.

---

## 1. A fonte canônica (o que estamos enriquecendo)
A "planilha ZEPEC" oficial não é um arquivo único — é um **conjunto oficial** já catalogado no Drive (`inventario/classificacao-planilhas.csv`, oficialidade `oficial`):

| Papel | Arquivo (Drive) | Colunas | O que traz (verbatim do catálogo) |
|---|---|---|---|
| **Lista-base (cedente)** | `lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx` | 10 | Declarações de potencial construtivo — **SQ, lote, endereço** |
| **Status emitido** | `lista_certidao_ZEPEC-BIR_agosto-2025.xlsx` | 18 | Certidões de transferência — cedente/receptor, **SQ, lote** |
| **Universo APC** | `SIRGAS_SHP_ZEPEC1.csv` (ZEPEC-APC) | 9 | Zonas Especiais de Preservação Cultural — **processo/endereço/nome** |
| **Cadastro tombados** | `SIRGAS_SHP_benstombados1.csv` | 30 | Bens tombados — **setor/quadra/lote, endereço, ZEPEC** |
| **Atos de classificação** | `_entrada/tdc/*zepec*`, resoluções CONPRESP (local) | — | Resolução/nº, processo SEI, data, denominação do bem |

> **Decisão pendente do MOU (não invento):** confirmar **qual** é a lista-base canônica a enriquecer — a hipótese é `lista_declaracoes_ZEPEC-BIR` (declarações = quem já tem potencial reconhecido) **unida** ao cadastro de tombados/ZEPEC-APC (universo elegível ainda sem declaração). Ver §7.

**Chave mestra (CODEX §3):** **SQL_MESTRE** (10 dígitos `SSSQQQLLLL`, zero à esquerda), guardado decomposto (setor/quadra/lote) + `SQL_DV` em campo à parte. Toda planilha entra normalizada para SQL_MESTRE **antes** de cruzar. É o que costura todas as camadas abaixo.

---

## 2. Camadas de enriquecimento (o schema a acrescentar) — parte a parte, nunca de uma vez (1.2)
Cada camada = um bloco de colunas adicionado por JOIN via SQL (ou via NOME quando não há SQL), **carimbando a fonte e o ano de cada campo**. Nenhuma camada calcula valor.

**C-a — Normalização / chaves** *(local; sem dado novo, só forma)*
`sql_mestre`, `setor`, `quadra`, `lote`, `sql_dv`, `endereco_mestre` (estrutura Correios/DNE normalizada — CODEX §3). Resolve SQL a partir de endereço quando faltar (D-02).

**C-b — Identidade & vigência da classificação ZEPEC** *(das resoluções/atos — fonte oficial)*
`denominacao_bem`, `tipo_zepec` (BIR / APC / tombado), `ato_classificacao` (Resolução CONPRESP nº/ano), `processo_sei`, `data_classificacao`, `grau_protecao`. → dá **vigência da classificação** (1.6: desde quando, por qual ato).

**C-c — Cadastro físico (IPTU 2026)** *(oficial, por SQL)*
`endereco_iptu`, `cep`, `area_terreno`, `area_construida`, `uso`, `padrao`, `ano_exercicio`. Atributos **factuais de cadastro**. *(Campos monetários do IPTU — valor venal/valor m² — existem na base mas ficam FORA por ora: respeitam "sem valor"; reabrir só se o MOU pedir, como atributo cadastral, nunca como cálculo.)*

**C-d — Titularidade** *(oficial + derivado, cadeia por SQL→NOME→CNPJ)*
`proprietario` (de SISSEL/OODC/alvarás por SQL), `cnpj`, `razao_social`, `socios` (de empresas/socios/holdings por NOME/CNPJ). **Cada campo com `proveniencia` (arquivo+ano) e `confianca`** — o vínculo CNPJ↔SQL nas bases oficiais é **indireto via NOME** (ruído declarado, §5).

**C-e — Status do potencial** *(oficial, factual — não é valor)*
`tem_declaracao` (consta em `lista_declaracoes`?), `tem_certidao` (consta em `lista_certidao`?), `data_declaracao`, `data_certidao`. Marca o que **já foi declarado/transferido** — para não tratar como inédito quem já movimentou. Sem cifra.

**C-f — Geo / zoneamento** *(geo, por ST_Within)*
`zona` (em qual zona o lote está), `perimetro` (TICP/operação urbana/AUE/APPa — inclusive os que a lei EXCLUI da cedência, Art. 124 §2º), `geom` (polígono do lote). Fato locacional, não juízo.

---

## 3. Regra de proveniência por campo (o que torna o enriquecimento confiável)
- **Uma linha = um imóvel (SQL_MESTRE)**, mas **cada campo carrega sua origem**: `<campo>__fonte` (arquivo/fileId), `<campo>__ano` (ano em que a informação aparece), `<campo>__oficialidade` (oficial/derivado), `<campo>__confianca`.
- **Conflito entre fontes:** a **mais recente vence**, mas o histórico **não se descarta** (vai para um campo de histórico/observação) — CODEX Fase 2.
- **Derivado nunca vira lei** (D-03/D-04): campo vindo de planilha derivada/IA entra **marcado como alerta**, gatilhando busca da fonte oficial; não substitui o oficial silenciosamente.

---

## 4. Prior art a auditar (não reinventar — mas não confiar cego)
Já existem consolidados **derivados** focados exatamente nisto (prova de conceito do pipeline):
- `MEGA_PLANILHA_ENRIQUECIDA_FINAL_V2.csv` (70 col — tombados × IPTU × ZEPEC × OODC × proprietário × CNPJ × sócios).
- `MEGA_PLANILHA_SANEADA_TOMBADOS_V1.csv` (47 col), `PLANILHA_ENRIQUECIDA_FINAL_ITBI_V2.csv`.

**Tratamento (D-03/D-04):** são **insumo/alerta**, não verdade. O enriquecimento **rebuild a partir das fontes oficiais** com proveniência por campo, usando as MEGA_PLANILHAS para (a) auditar cobertura, (b) recuperar o método de match já tentado, (c) achar campos úteis que esquecemos. Nunca como base canônica.

---

## 5. Lacunas declaradas (honestidade D24 — o que o enriquecimento NÃO resolve sozinho)
1. **CPF do proprietário PF:** nenhuma base imobiliária oficial traz; só `socios.csv` (PF em empresas). Para pessoa física, match só por NOME (fraco/ambíguo).
2. **Cobertura proprietária parcial:** IPTU_2026 (~1M) **não tem proprietário**; só o subconjunto que passou por SISSEL/OODC/alvará/ITBI. Para ZEPEC isso pode bastar (universo pequeno), mas a cobertura é a **medir**, não a presumir.
3. **Matrícula** só chega via série ITBI — imóvel sem ITBI fica sem ponte ao cartório.
4. **CNPJ↔SQL** nas bases oficiais é indireto (via NOME) → ruído; só os derivados trazem o vínculo direto (e são alerta, não lei).
5. **`.xls` legados não lidos** (SISSEL/ITBI antigos) — cabeçalho não confirmado; exige conversão do binário antes de cruzar.

---

## 6. Ordem de execução (parte a parte) e o que é local × Drive
| Passo | Camada | Onde |
|---|---|---|
| 1 | Fixar a lista-base canônica (§1, decisão MOU) + extração pura das colunas nativas | Drive (as 4 planilhas ZEPEC) |
| 2 | **C-a** normalização para SQL_MESTRE/ENDERECO_MESTRE | **local** (regra determinística) |
| 3 | **C-b** identidade/vigência da classificação | local (resoluções já em `_entrada/tdc/`) + Drive (faltantes) |
| 4 | **C-c** cadastro IPTU por SQL | Drive→Supabase (IPTU_2026 ~937 MB) |
| 5 | **C-d** titularidade (cadeia NOME/CNPJ) | Drive→Supabase (SISSEL/empresas/socios) |
| 6 | **C-e** status declaração/certidão | Drive (as 2 listas ZEPEC-BIR) |
| 7 | **C-f** geo/zoneamento | Drive/geo (lotes + zoneamento SIRGAS) |

> **Desbloqueado já:** o **schema do enriquecimento** e o **normalizador C-a** (determinístico, sem dado pesado) podem ser escritos e testados localmente sobre uma amostra das colunas nativas ZEPEC.
> **Bloqueado (lane do Drive):** as cargas pesadas (IPTU/SISSEL/socios/geo) — consolidar no pedido B-9.

---

## 7. Para a decisão do MOU (não invento)
1. **Qual é a lista-base canônica?** Só `lista_declaracoes_ZEPEC-BIR`? Ou unir com tombados/ZEPEC-APC (universo elegível sem declaração)?
2. **Campos monetários do IPTU** (valor venal) entram como atributo cadastral factual, ou ficam fora para honrar "sem valor"?
3. **Quais camadas** entram nesta volta (C-b..C-f) e em que ordem de prioridade comercial.
4. **PII (C-d):** confirmar o regime (D-106 risco aceito / RLS deny-all) antes de costurar sócios/CPF.

> Registrado no BACKLOG como **B-20** (frente comercial — enriquecimento ZEPEC). Cross-ref: `inventario/mapa-dados-fase2.md` (modelo de junção), `inventario/classificacao-planilhas.csv` (catálogo das fontes).
