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

## RESULTADO Etapa 1–3 (FEITO 2026-06-28) — `zepec/limpo/zepec_unificada.csv`
`zepec/montar_base.py` juntou as 4 fontes **com tag `origem`**, canonizou **SQL→SQL_MESTRE** (10 díg, decomposto, DV à parte) e **estruturou o endereço** (tipo DNE + logradouro + números). Multi-lote por célula **explodido** (1 linha = 1 imóvel).
- **7.175 linhas:** DECLARACAO_BIR 565 · CERTIDAO_BIR_CEDENTE 196 · TOMBADO_CADASTRO 6.409 · ZEPEC_APC 5.
- **SQL_MESTRE: 5.336 ok · 1.791 ausente · 48 inválido.**
- **Endereço: 5.307 com tipo reconhecido · 1.168 multi (vários nºs/ruas).**
- Esfera derivada (municipal/estadual/federal) e categoria (BIR/APPa/AUE) trazidas do cadastro de tombados.

## O QUE MAIS ARRUMAR (só com estes arquivos — sem cruzar nada externo)
1. **Casing:** benstombados vem em CAIXA ALTA, declarações em mista → padronizar capitalização (cuidando de acentos) — ⏳ a decidir se mexe (fidelidade vs leitura).
2. **1.791 sem SQL** (1.784 tombados de bairro/monumento/logradouro sem lote cadastral + 5 APC) → resolver SQL exige endereço→cadastro = **externo** (marcado).
3. **48 SQL inválidos** (quadra 2-díg, lote faltando) → conferir caso a caso.
4. **1.168 endereços multi** (vários nºs/ruas na célula) → decidir grão (imóvel × conjunto); hoje mantidos juntos com flag `end_multi`.
5. **32 endereços sem tipo** (não começam por tipo conhecido) → revisar.
6. **Datas ainda não normalizadas** (certidões/tombados, formatos M/D/YYYY × D/M/YYYY) → ISO. ⏳
7. **Duplicata / 2ª via + vínculo** (mesmo imóvel em declaração E certidão; "2ª via") → dedup/vínculo ⏳ **A OBSERVAR**.
8. **OCR/encoding** residual (ex.: APC "BAR Ó DO BOROGODÓ").
9. **Categoria AUE/APPa** marcada como fato no cadastro (a lei exclui da cessão — Art. 124 §2º; regra é downstream, não juízo aqui).
10. **Distrito vazio** em 1.773 tombados → preencher por geo/endereço = **externo**.

## Onde vamos guardar (deixar à mão)
- **Git:** `zepec/raw/` (bruto), `zepec/limpo/` (saído da Etapa 1–3) — listas pequenas, versionáveis.
- **Supabase:** só quando entrar o pesado (IPTU/socios/geo) na Etapa 5.
