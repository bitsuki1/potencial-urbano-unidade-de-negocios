# ZEPEC — etapas de afinação e enriquecimento
> PU 14 · 2026-06-28 · direção do MOU. Agnóstico: só fato, sem juízo (nada de "vale/não vale/melhor/pior").
> Doutrina: extrair puro → enriquecer (1.2) · parte a parte (Fase 2) · proveniência por campo · nada se descarta.
> Decisões do MOU já fixadas: **(D-a)** unir as origens **com TAG** · **(D-b)** valor venal **entra** como fato cadastral · **(D-c)** sócios por último.
> **A OBSERVAR** = campo complexo a analisar com calma antes de tocar (não resolver de afobado). Marcado ⏳.

---

## As ETAPAS (o que fazer com os arquivos, em ordem)

**Etapa 0 — Despejo bruto.** ✅ FEITO.
As 4 planilhas oficiais em `zepec/raw/` (CSV) + `PROVENIENCIA.md` (fileId por fonte). Verbatim, nada saneado.

**Etapa 1 — Afinar DENTRO de cada arquivo (sem cruzar nada de fora).** *Isto é "o que afinar nas ZEPECs".*
- **Preâmbulo ≠ dados:** linhas 0–2 das listas SMUL são texto institucional → marcar `contexto-não-citável`, achar a linha de cabeçalho real.
- **Nulos padronizados:** `"não consta"`, `"-"`, `""`, `s/n` → um NULL único.
- **OCR/encoding:** corrigir ruído real (`BAR Ó DO BOROGODÓ` → `BAR DO BOROGODÓ`; ligaduras ti/fi viradas em 7/9 nos itens de PDF).
- **Datas:** formatos MISTOS na MESMA coluna (`9/20/2000` US, `14/11/2020` BR) → ISO `AAAA-MM-DD`.
- **Áreas/m² (`Área cedida`, `Área recebida`):** formatos MISTOS (`46,098.00` US vs `2.380,05` BR) → decimal canônico. ⏳ **A OBSERVAR** (é número-fato; conferir antes de normalizar).

**Etapa 2 — Chave canônica (ainda interno).**
- **SQL → SQL_MESTRE** (10 díg, zero à esquerda; setor/quadra/lote; DV à parte). `benstombados` já vem decomposto ✓; declarações/certidões têm `SQ`(6) + `Lote` → compor.
- **Casos sujos de SQL:** múltiplos lotes na mesma célula (`"0090-2, 0496-7, …"`), `COND 02`, `Vila Inglesa`, SQ sem zero (`16047`), `nº INCRA` (rural). → regra explícita por caso.
- **Endereço → ENDERECO_MESTRE** (DNE): múltiplos números/endereços por célula (`"1475 e 1470"`).

**Etapa 3 — Unir as 3 origens COM TAG (decisão D-a).**
- Base única empilhando `declarações + tombados + ZEPEC-APC`, cada linha com:
  - `origem` = `DECLARACAO_BIR` | `TOMBADO_CADASTRO` | `ZEPEC_APC`
  - `tipo_zepec` = BIR | APC | tombado · `grau_protecao` · `esfera` (municipal/estadual/federal — `benstombados` tem CONPRESP+CONDEPHAAT+IPHAN).
- **Vínculo entre listas** (mesmo imóvel em declaração ↔ certidão ↔ cadastro tombado) → ⏳ **A OBSERVAR**.

**Etapa 4 — Status e saldo.** ⏳ **A OBSERVAR** (inteira — analisar com calma).
- `Situação` / `Status Declaração`; `ESGOTADO`; declaração que gera **certidões sucessivas** (Art. 131) consumindo potencial; **saldo remanescente**. Tudo fato, mas relacional e delicado.

**Etapa 5 — Enriquecer com fontes EXTERNAS (depois do interno pronto).**
- Por SQL: IPTU, geo/zona, ITBI/matrícula, OODC, licenciamento. **Sócios/titularidade por ÚLTIMO** (decisão D-c; PII).

---

## O que dá para ENRIQUECER no arquivo (fontes externas, por SQL — mapa em `inventario/mapa-dados-fase2.md`)
Cada campo entra carimbando `fonte` + `ano` + `oficialidade` (só fato, sem juízo):

| Enriquecimento | De onde (por SQL) | Observação |
|---|---|---|
| Cadastro físico: área terreno/construída, uso, padrão, CEP, endereço oficial | `IPTU_2026` | base ~1M, Drive→Supabase |
| **Valor venal / valor m²** (fato cadastral) | `IPTU_2026`, série ITBI | entra (D-b), sem rótulo |
| Matrícula de cartório | série `GUIAS DE ITBI PAGAS` | única ponte SQL↔matrícula |
| Esfera/datas/categoria do tombamento | `SIRGAS_SHP_benstombados1` (já puxado) | enriquece a declaração com a árvore municipal/estadual/federal |
| Zona / perímetro / polígono do lote | zoneamento + LOTES geo | define CAbas e exclusões (AUE/APPa) |
| Histórico de outorga | série OODC | fato |
| Proprietário → CNPJ → sócios | SISSEL/alvarás → empresas/socios/holdings | ⏳ **POR ÚLTIMO** (D-c, PII, vínculo por NOME = ruidoso) |

---

## Onde vamos guardar (deixar à mão)
- **Git:** `zepec/raw/` (bruto), `zepec/limpo/` (saído da Etapa 1–3) — listas pequenas, versionáveis.
- **Supabase:** só quando entrar o pesado (IPTU/socios/geo) na Etapa 5.
