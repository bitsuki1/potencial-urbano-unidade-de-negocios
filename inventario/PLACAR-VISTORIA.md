# PLACAR FINAL — Vistoria de proveniência por CONTEÚDO do Drive PU · 2026-07-13
> Os **33.138** arquivos foram ABERTOS (conta de serviço), o texto real extraído (PDF nativo, **OCR** em
> escaneados/imagens, cabeçalho+amostra em planilhas/gigantes via Range, schema de shapefiles) e classificados
> pela EVIDÊNCIA do conteúdo — **nunca por nome/pasta/tag**. Cada linha carrega o trecho que decidiu + o sha256
> (custódia). De-para: `inventario/drive-pu/PROVENIENCIA-DE-PARA.csv`. Regra de ouro: nenhuma classe sem conteúdo inspecionado.

## Placar — 33.138 arquivos abertos e classificados (após a revisão do orquestrador)
| Classe | Qtd | % | O que é / destino |
|---|---:|---:|---|
| **OFICIAL** | 10.673 | 32,2% | fonte oficial auditável → corpus (02/03/05). É o **teto**; a ingestão ainda re-verifica cada um contra a fonte (hash+verbatim+vigência) antes de citar. |
| **ILEGÍVEL** | 12.845 | 38,8% | aberto, sem conteúdo legível — **96% são PNG que NÓS extraímos** → material-bruto (90). |
| **CRIADO** | 7.272 | 21,9% | gerado/derivado por nós (inclui 4.162 fragmentos SILVER reclassificados) → só ideia (90), **NÃO usar como fonte**. |
| **NÃO-OFICIAL-EXTERNO** | 2.348 | 7,1% | base de terceiro (externa) → usável no comercial (06) / apoio. |

**Comercial (flag bruto): 6.159** (ruidoso — ver §06). A fração de baixa confiança (780) foi revisada à mão.

## Revisão do orquestrador (onde precisa de julgamento — feita à mão, sem sub-agente)
- **4.162 "OFICIAL" → CRIADO (correção):** o classificador marcou oficial vários **fragmentos que NÓS extraímos**
  (SILVER: "QUADRO_X_FINAL_Pagina_Y_Tabela", "_Pag_N_Img", "_IA.csv", "LOTES_Parte_*_IA"). O conteúdo é oficial,
  mas a **proveniência é CRIADA** → não são fonte citável (auditabilidade). Corrigido no de-para (confianca=revisado).
- **LOTES_Parte_*_IA:** confirmado **CRIADO** (D-DONO-4: proibido como fonte, substituído pelos SIRGAS oficiais).
- **Lei 18.298/2025** apareceu como OFICIAL (extração vazia) — é o **gap conhecido** do corpus; vale ingerir do portal.
- **OFICIAL restante (10.673)** é o TETO do corpus auditável — ainda contém fragmentos nossos não pegos pelo padrão de nome;
  a ingestão deve re-verificar cada candidato contra a fonte original antes de virar `leis/` citável.

## ILEGÍVEL por extensão (prova: é imagem que NÓS extraímos, não fonte perdida)
| ext | qtd |
|---|---:|
| png | 12.373 |
| jpeg | 246 |
| ods | 94 |
| pdf | 65 |
| xlsx | 40 |
> Só **65 PDFs** são de fato ilegíveis; o resto é imagem (page-crop nossa) sem texto — corretamente fora do corpus.

## 06 — Comercial (achar o proprietário) — CURADO à mão: 43 bases
> O flag automático deu 6.159 (ruidoso: marca qualquer doc com coluna cadastral, incl. jurisprudência e camadas geo).
> Curei às bases REAIS de dados de proprietário → `inventario/drive-pu/DE-PARA-06-COMERCIAL.csv`. Destaques (os 3 que o MOU citou ✓):
> - **socios.csv (3,4 GB)** — quadro societário / QSA
> - **empresas.csv (2,3 GB)** — cadastro CNPJ
> - **iptu-2020-cep01.csv (153 MB)** (+.gz) — o "IPTU não-2026", cadastro histórico
> - **holdings.csv (60 MB)**, **GUIAS DE ITBI PAGAS** (transações→compradores), **extrato_ad**, **listas ZEPEC**, **Cartão CNPJ**
>
> **NÃO entram no 06:** `IPTU_2026` (dado de engine → 03), camadas SIRGAS/geo (→05), fragmentos nossos (→90).
> Restam ~5 falsos-positivos (artigos com "ITBI" no nome) que o MOU tira num olhar.

## Como o MOU audita (nada é "confie em mim")
Qualquer `drive_id` no `PROVENIENCIA-DE-PARA.csv` mostra `classe`, `metodo` (texto_nativo/ocr/planilha/shape/llm),
`confianca` e `evidencia_conteudo` = o **trecho real** que decidiu. Classe sem evidência = erro sinalizado.

## Próximo passo (depende do MOU)
Separar o **06 — Comercial** (as 43 bases) é uma MOVIMENTAÇÃO no Drive → espera o seu **"pode mover"** (com ensaio antes).
Depois: mover CRIADO+ILEGÍVEL→90, re-verificar os OFICIAL contra a fonte antes de ingerir no corpus.
