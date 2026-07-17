# PLACAR FINAL — Vistoria de proveniência por CONTEÚDO do Drive PU · 2026-07-13
> Os **33.138** arquivos foram ABERTOS (conta de serviço), o texto real extraído (PDF nativo, **OCR** em
> escaneados/imagens, cabeçalho+amostra em planilhas/gigantes via Range, schema de shapefiles) e classificados
> pela EVIDÊNCIA do conteúdo — **nunca por nome/pasta/tag**. Cada linha carrega o trecho que decidiu + o sha256
> (custódia). De-para: `inventario/drive-pu/PROVENIENCIA-DE-PARA.csv`. Regra de ouro: nenhuma classe sem conteúdo inspecionado.

## Placar — 33.138 arquivos abertos e classificados (após a revisão do orquestrador)
| Classe | Qtd | % | O que é / destino |
|---|---:|---:|---|
| **OFICIAL** | 7.465 | 22,5% | fonte oficial auditável → corpus (02/03/05). É o **teto**; a ingestão ainda re-verifica cada um contra a fonte (hash+verbatim+vigência) antes de citar. |
| **ILEGÍVEL** | 12.845 | 38,8% | aberto, sem conteúdo legível — **96% são PNG que NÓS extraímos** → material-bruto (90). |
| **CRIADO** | 10.480 | 31,6% | gerado/derivado por nós (inclui 4.162 fragmentos SILVER + 3.208 .md/.json de camada nossa) → só ideia (90), **NÃO usar como fonte**. |
| **NÃO-OFICIAL-EXTERNO** | 2.348 | 7,1% | base de terceiro (externa) → usável no comercial (06) / apoio. |

**Comercial (flag bruto): 6.159** (ruidoso — ver §06). A fração de baixa confiança (780) foi revisada à mão.

## Revisão do orquestrador (onde precisa de julgamento — feita à mão, sem sub-agente)
- **4.162 "OFICIAL" → CRIADO (1ª correção):** o classificador marcou oficial vários **fragmentos que NÓS extraímos**
  (SILVER: "QUADRO_X_FINAL_Pagina_Y_Tabela", "_Pag_N_Img", "_IA.csv", "LOTES_Parte_*_IA"). O conteúdo é oficial,
  mas a **proveniência é CRIADA** → não são fonte citável (auditabilidade). Corrigido no de-para (confianca=revisado).
- **3.208 ".md/.json OFICIAL → CRIADO (2ª correção — item 2):** ao re-verificar o OFICIAL contra a fonte, cada
  `.md`/`.json` marcado oficial carregava, na própria evidência, marcas da **nossa camada** ("layer: SILVER",
  "chunk_id", "Trabalhe apenas com os fatos extraídos"). São saídas do NOSSO pipeline (extração/chunk), não a norma
  original → **CRIADO**. Isso derrubou o OFICIAL de 10.673 → **7.465** (o teto auditável verdadeiro).
- **LOTES_Parte_*_IA:** confirmado **CRIADO** (D-DONO-4: proibido como fonte, substituído pelos SIRGAS oficiais).
- **OFICIAL restante (7.465)** é o TETO do corpus auditável (majoritariamente **PDF** de portal oficial — masthead
  "PREFEITURA DO MUNICÍPIO", "Catálogo de Legislação"). A ingestão re-verifica cada um contra a fonte antes de citar.

## Fila de ingestão (item 2 — cruzamento OFICIAL-pdf × corpus `leis/`)
> Determinístico (`scripts/gerar_fila_ingestao.py`, sem LLM — triagem, Parte 3 etapa 2). Extrai o nº da norma do
> conteúdo dos **OFICIAL-pdf**, descarta o que já existe em `leis/` (36 números ingeridos) e enfileira o que falta.
> Saída: `inventario/drive-pu/FILA-INGESTAO-OFICIAL.csv` (nº · ano · ocorrências · melhor `drive_id` p/ puxar).

- **70 normas** distintas detectadas nos OFICIAL-pdf · **16** já no corpus · **54 FALTANTES** enfileiradas.
- **Lei 18.298/2025** (Revisão do PDE) — o **gap conhecido**: confirmado presente como fonte OFICIAL (drive) e AUSENTE
  do corpus. Entra na fila.
- Destaques faltantes (por ocorrências): Decreto 63.504/2024 · Lei 10.257/2001 (Estatuto da Cidade, federal) ·
  Lei 18.177/2024 · Decreto 58.955/2019 · Lei 17.104/2019 · Lei 15.150/2010 · série de decretos regulamentares 2016–2025.
- **Gate (Parte 1.6/1.7):** a fila só APONTA; nenhuma vira `leis/` sem re-verificação verbatim + vigência + hash da fonte.
  Ingestão espera o **"pode"** do MOU (é escrita no corpus citável).

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

## Estado (o que já foi FEITO)
- ✅ **06 — Comercial** separado: 43 bases de achar-proprietário movidas (run 29245816119, 0 erros).
- ✅ **90 — Material bruto**: 522 CRIADO/imagens movidos (ensaio 522 → move real DRY_RUN=false).
- ✅ **Item 2** (re-verificar OFICIAL): 3.208 .md/.json corrigidos p/ CRIADO; OFICIAL real = 7.465; **fila de 54 normas faltantes** gerada.

## Próximo passo (depende do "pode" do MOU — é escrita no corpus)
Ingerir da fila `FILA-INGESTAO-OFICIAL.csv` (começando por TDC + o gap Lei 18.298/2025), cada norma re-verificada
verbatim + vigência + hash contra a fonte antes de virar `leis/` citável. Os **49 ILEGÍVEL** em HOLD
(`HOLD-ILEGIVEL-RECHECAR.csv`, pdf/xlsx/ods) aguardam re-extração dedicada.
