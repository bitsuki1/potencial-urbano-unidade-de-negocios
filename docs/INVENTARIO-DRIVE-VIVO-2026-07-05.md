# INVENTÁRIO VIVO DO GOOGLE DRIVE — 2026-07-05

> Levantado ao vivo em 2026-07-05 via MCP `Google_Drive` (somente leitura; nenhum arquivo movido/criado/apagado no Drive).
> Responde ao achado **A-08** da `docs/AUDITORIA-PROFUNDA-2026-07-05.md` ("nenhum check confronta o índice com o Drive real") e à decisão do dono: "antes de extrair qualquer coisa, olhar TUDO que temos no Drive".
> Método: toda contagem/afirmação cita a chamada que a provou (busca `parentId=…` paginada, `get_file_metadata` por ID, busca por título/fullText). Nada estimado.

## Sumário executivo (5 linhas)
1. **A arrumação nunca rodou:** os **1.360** arquivos do `de-para-COMPLETO-2026-07-04.csv` estão TODOS ainda na `01 — _entrada` (0 movidos; diff `comm` = 0 ausentes) e as pastas-alvo 00–05 e 2.1–2.7 estão **todas vazias**. A `_entrada` tem hoje **1.365 itens** (os 1.360 + 5 subpastas novas).
2. **8 das 13 leis municipais pendentes TÊM verbatim/PDF no Drive** (6.989/66, 10.235/86, 11.152/91, 13.250/01, 14.865/08, 15.044/09, 17.202/19, 17.577/21); **5 NÃO existem** em lugar nenhum do Drive (10.365/87, 11.338/92, 12.350/97, 13.475/02, 17.759/22).
3. **Decreto 57.536/2016 (núcleo TDC) ESTÁ no Drive** (2 PDFs de corpo + anexos 1/8/9 + csv), assim como 17.975/23, 18.081/24, 18.222/24, Quadro 2A e Quadro 6 (Fp), e TODAS as camadas geo (ZEPEC_AUE/APP-BIR completas, 96 distritos de LOTES completos, logradouronbl). **Decreto 58.289/2018 só tem os Anexos I e V — o corpo do decreto NÃO está no Drive.**
4. **Duplicatas de ~16–20 GB continuam vivas:** socios.csv 3,4 GB ×≥5, empresas.csv 2,3 GB ×≥5, IPTU_2026.csv 938 MB ×7; a lixeira `99_LIXEIRA_DUPLICADOS` tem 2.757 itens (~11,5 GB). O saneamento de 2026-06-20 também nunca foi executado.
5. Todos os ~52 IDs do `docs/INVENTARIO-DRIVE.md` (2026-07-03) **ainda existem**, mas 4 pastas têm nome/papel divergente do registrado (a "geo-mãe" é na verdade a pasta `99_LIXEIRA_DUPLICADOS` do lago TODOS TDC) e 1 arquivo está bloqueado para leitura por IA.

---

## 1. Árvore de pastas relevante (ao vivo)

Provas: `get_file_metadata` em cada pasta + `search_files parentId='…'` (pageSize 1000, paginado e deduplicado por id).

```
PORTFÓLIO DO MOU  (1DkJl24-tQrLhO-WeuuAjwa8ahws8VbYf, no shared drive 0APQMETkmU9TbUk9PVA)
├── POTENCIAL URBANO  (1BrM6q36meTtn5guJoiGbqvCtZF11Uau3) — 8 subpastas
│   ├── 00 — Governança & Índice        (1zfDGtvhZh1JDUykC6kouDPqm-E3u0bgO)
│   ├── 01 — _entrada (despejo IPTU+TDC)(1grhqYgttj7KnJmiu9U73z-lXFHnFthov)
│   ├── 02 — Leis & Jurisprudência      (1GRvv6Xbi3_rKpZvvIqKIjyByu1LgFjmJ) — subpastas 2.1–2.7
│   ├── 03 — Tabelas & Engines          (1v4H2YsIZSNDwNXiMtOAV1w1qy-5kOuvy)
│   ├── 04 — Tese (Antítese/Vacina)     (1xuq1OpJzSYOGWG6dp7xGfCyDVE-WLVas)
│   ├── 05 — Geo                        (1uQTkzx2fXGMH1J5zrF_K1yD-NsUxxc1i)
│   ├── 05 — Geo / Mapas                (1VxXDspnEwYuiCMXjn9-YPp65h3vtb_pr)
│   └── TODOS TDC (lago legado mar/2026)(1uMMvR8_PVjNv3hgDjzpA7fm6yoVOvwYg) — 15 subpastas
│       └── DataLake_TDC e IPTU         (1XAUTRln1DK48hVTNwtIEZP3AIqvDZEHN)
│           └── 99_LIXEIRA_DUPLICADOS   (1ds4u4ZpoLl_ySSIDywPbh_iicRCt6zNI)  ← a "geo-mãe" do inventário antigo
└── SBA NEGÓCIOS  (1SDrjcLvd9-Mjx5zS0rnszyvGSeVNhMXm) — irmã do Potencial Urbano
    └── 99 — Inbox / Triagem            (1hlGw2hSI2oYf1YL6c_aylOUyPYxpMtwu)
```

| Pasta | ID | Itens (contados ao vivo) | Prova |
|---|---|---|---|
| POTENCIAL URBANO (raiz) | `1BrM6q36…` | 8 subpastas (nenhum arquivo solto) | busca `parentId='1BrM6q36…' and mimeType=folder` → 8 |
| **01 — _entrada** | `1grhqYgttj7…` | **1.365 itens únicos** (1.360 arquivos + 5 subpastas: `IPTU`, `IPTU-Sergio`, `NOVOS`, `Todos`, `Outros`) | busca `parentId` em 2 páginas (1000+440), dedup por id = 1.365 |
| 00 — Governança & Índice | `1zfDGtvhZh1…` | 1 item: subpasta "Prompts & Gens (IA)" (`1PvLBgMdl1…`), que está **vazia** | 2 buscas `parentId` |
| 02 — Leis & Jurisprudência | `1GRvv6Xbi3…` | 7 subpastas 2.1–2.7, **todas vazias** (0 arquivos) | busca `parentId` (7 folders) + busca OR nos 7 parentIds → `{}` |
| 03 — Tabelas & Engines | `1v4H2YsIZ…` | **vazia** | busca `parentId` → `{}` |
| 04 — Tese | `1xuq1OpJz…` | **vazia** | busca `parentId` → `{}` |
| 05 — Geo | `1uQTkzx2…` | **vazia** | busca `parentId` → `{}` |
| 05 — Geo / Mapas | `1VxXDspn…` | **vazia** | busca `parentId` → `{}` |
| TODOS TDC (lago) | `1uMMvR8_…` | 15 subpastas (DataLake, 00_INBOX_TRIAGEM, 00_LOGS, 01_BRONZE_RAW, 01A/01B/01C_BRONZE, 02_SILVER_STAGED, 04_ORIGINAIS, 06_CRIADOS, PASTA UNICA, Anexo Foto capa IPTU, 99_LIXEIRA, 99_QUARENTENA, 99_PARA_DELETAR) | busca `parentId` → 15 |
| **99_LIXEIRA_DUPLICADOS** (sob DataLake) | `1ds4u4ZpoLl…` | **2.757 itens únicos, ~11,49 GB** (3 páginas 1000+1000+801, dedup) | 3 buscas `parentId` paginadas + jq |
| 99 — Inbox / Triagem (sob SBA NEGÓCIOS, fora do projeto) | `1hlGw2hSI…` | 5 arquivos (mailing/apresentações — alheios ao corpus) | busca `parentId` → 5 |

Observação: a pasta `99 — Inbox / Triagem` que o `de-para-COMPLETO-2026-07-04.csv` usa como destino (`1p8d2Cx-qbLO0nRicRjbZ7h47cp2jqb7t`) retornou erro do MCP: *"ineligible to be used in generative AI contexts"* — não foi possível confirmar nome/local dela por esta lente.

---

## 2. Verificação dos IDs do `docs/INVENTARIO-DRIVE.md` (2026-07-03)

Todos os ~52 IDs citáveis do documento foram verificados: **13 confirmados vivos na própria listagem da `_entrada`** (IPTU_2026.csv 937.865.216 B; iptu-2020-cep01.csv 152.926.077 B; listas ZEPEC-BIR xlsx 225.063/194.082 B; ZEPEC_BIR.shp 855.548 B; ZEPEC_APP-BIR.shp 74.568 B; ZEPEC_BIR_INDIC.shp 358.660 B; LOTES_Parte_1/5_IA.csv; tema-1158.txt; capa IPTU Líbero Badaró; Formulário docx; PDF juris STF) e os demais por `get_file_metadata`. **Nenhum ID deixou de existir.** Divergências encontradas:

| ID | O que o inventário dizia | O que é DE FATO (metadata ao vivo) | Status |
|---|---|---|---|
| `1ds4u4ZpoLl_…` | "pasta-mãe GEO **sob 05 — Geo**" | título real **`99_LIXEIRA_DUPLICADOS`**, parent = `DataLake_TDC e IPTU` (dentro do lago TODOS TDC). 2.757 itens (~11,5 GB), maioria com sufixo de hash (553 de 1000 na pág. 1) | **NOME/PAPEL NÃO BATE** — os shapefiles-com-hash "canônicos na geo-mãe" estão numa LIXEIRA de duplicados |
| `16UUslSV12qD…` | "Tabelas .csv extraídas" | título real `MOTOR_2_Tabelas_Staged` (parent `1jVY1lKiWLMU…`, no lago) | existe; nome difere |
| `1M4T65C4ckrcc…` | "PNGs de Outorga (screenshots)" | título real `Imagens_Extraidas` (parent `1xRBewJ2Fvt…`) | existe; nome difere |
| `1loXodqJkdSTv…` | "com_empresa (sprints)" | título real `slides_follow_up` (parent `17jaSkmtiRSeg…`) | existe; **nome não bate** |
| `1OoX3rcSrQeWs…` | "Minuta … Shopping" | título real `Minuta Contratual, Quadro Resumo e Propostas Tecnica - Shopee e Keepee 19.12.2024.pdf`; parent novo `15qjR4QsWrcsz…` (createdTime 2026-07-02 — foi movida/recriada) | existe; nome e pasta diferem |
| `1KAvM0NuHZzDo…` | Modelo Reduzido IPTU.xlsx | MCP recusa: *"ineligible to be used in generative AI contexts"* | **não confirmável por esta lente** |
| Todos os demais (~46) | — | existem, nome e tamanho batem (ex.: ZEPEC_AUE_696911.shp 1.683.820 B; SIRGAS_SHP_logradouronbl_9ce340.shp 30.840.700 B; quadraMDSF 22.943.110 B; setorfiscal 14.482 B; benstombados 2.538.964 B; zeup_zemp 416.724 B; cota_solidariedade 185.652 B; LOTES_70_SANTANA 6.134.788 B; Quadro_3 CSVs 122/161 B; Quadro_5_Fs.md 1.527 B; DOCUMENTO MESTRE HOLDING TDC gdoc; CNPJ.pdf ×2; pastas CNPJ 18.510/49.183/ATUALIZADO/CARTÃO) | OK |

---

## 3. Busca dirigida — o que EXISTE e o que NÃO EXISTE no Drive

### 3a. As 12 leis municipais pendentes + a lei-mãe 6.989/1966

Prova: grep na listagem completa da `_entrada` (1.365 itens) + buscas Drive-wide `title contains` e `fullText contains` para as ausentes.

| Lei | Existe? | Arquivo(s) — ID · bytes | Texto × imagem (inferência) |
|---|---|---|---|
| **6.989/1966** (lei-mãe IPTU) | **SIM** | `LEI Nº 6.989 de 29 de Dezembro de 1966.pdf` `1XU4Ol06BrfVp3xhUepIr26nhZaKNo0UW` · 12.503.958 B | 12,5 MB p/ uma lei → **provável scan/imagem** (OCR necessário) |
| **10.235/1986** | **SIM** | `LEI Nº 10.235 de 16 de Dezembro de 1986.pdf` `1Z96DTndx0o9ZLLZBtTjlYeUM9pCPdPJV` · 8.369.649 B | 8,4 MB → **provável scan/imagem** |
| 10.365/1987 | **NÃO** | busca `title contains '10.365' or '10365'` → só 1 PNG irrelevante; sem lei | — |
| **11.152/1991** | **SIM** (2 versões) | `1RJPQk_iHUwxHO6jTdFLeebP83gO6oIc5` · 2.400.988 B; versão «Catálogo de Legislação Municipal» `1FqcbmhH1qDV1BDqgpnTAmFx2i48FCS0c` · 334.176 B | Catálogo = **PDF-texto** (padrão indexado pelo fullText do Drive) |
| 11.338/1992 | **NÃO** | busca título → `{}` | — |
| 12.350/1997 | **NÃO** | busca título → `{}` (só homônimos CNPJ/cartilha) | — |
| **13.250/2001** | **SIM** | `LEI Nº 13.250 de 27 de Dezembro de 2001.pdf` `1g9F7BcvKwkrw5QnCihwWMYsFz6gF-ILn` · 1.595.902 B | tamanho médio; verificar OCR |
| 13.475/2002 | **NÃO** | busca título → `{}`; `fullText contains '13.475'` só acha menções dentro de outros docs (Gap Analysis, catálogo da 15.044) | — |
| **14.865/2008** | **SIM** | `1Sr46ue7GTXpZdiq8dmhR5WJkejPcQ5yn` · 2.403.709 B | verificar OCR |
| **15.044/2009** | **SIM** (2 versões) | `1TsB_KCsjokGYNtN1ZH2hA4L117113UBn` · 2.848.647 B; catálogo `1a9Y5eAQUrWHzWQQY_rjEeYR5sa6LqHjL` · 178.280 B | catálogo = **PDF-texto comprovado** (foi retornado por busca fullText) |
| **17.202/2019** | **SIM** | catálogo `1BzJm7JV5mrEZzmCmLSjTWoixYn7rmcz9` · 218.171 B | **PDF-texto** (padrão catálogo) |
| **17.577/2021** | **SIM** | catálogo `1LCqgXQmT8HIcVSaa0-WGezxDAPvF1bOh` · 217.541 B | **PDF-texto** (padrão catálogo) |
| 17.759/2022 | **NÃO** | busca título → `{}`; `fullText contains '17.759'` → só o gdoc "Gap Analysis" | — |

**Placar: 8 de 13 no Drive; faltam 5 (10.365/87, 11.338/92, 12.350/97, 13.475/02, 17.759/22) — precisam vir de fora (Catálogo de Legislação Municipal / Cadlem).**

### 3b. Decretos e leis recentes

| Norma | Existe? | Evidência |
|---|---|---|
| **Decreto 57.536/2016** (regulamento TDC) | **SIM — corpo + anexos** | `DECRETO Nº 57.536 … « Catálogo….pdf` `1hLFR5EZWVUOi4rS9gMvkynudDLjUekFk` · 182.513 B; `D57536.pdf` `1O6swdMMqOCE86d3EllLWcGLws0JMZU6a` · 254.792 B; `Anexo 1` `1zGE-_IvO0C4Z…` · 56.512 B; `Anexo 8` `1jrbCc3xZXsih…` · 13.992 B; `Anexo 9` `1Tf-tV2TmeIxD…` · 12.454 B; `D57536.csv` `1ZyjtHHUDe4To…` · 689 B (tudo na `_entrada`) |
| **Decreto 58.289/2018** | **PARCIAL — só anexos** | busca Drive-wide `title contains '58.289'/'58289'/'58_289'`: apenas `Anexo I` (121.684 B, ≥8 cópias; canônica na `_entrada` `1ADStSbYhp9byERMW2vvEBuLuuAvxG1Mb`) e `Anexo V` (93.231 B, ≥3 cópias; `1XwbeX64SbWTeAIdRotqmFydZAa6FcPPs`) + .md fatiados. **O corpo do decreto NÃO está no Drive.** |
| **Lei 17.975/2023** | **SIM** | catálogo `1xoEiPW-wqmsPFpLqM_Ybp-Q7A1WH2UU3` · 687.512 B |
| **Lei 18.081/2024** | **SIM + extras** | catálogo `1l6BEAUryN8TIW3KSqpEIAUXjbvu2FA6I` · 675.351 B; `MAPA da Lei nº 18081_2024.pdf` `1ekB9Ufwq_xA05…` · 14.395.495 B; `SIMULADOR_QA_atualizado_lei_18081_24_v4.xls` `1wx5xEoCv6wImh…` · 142.848 B |
| **Lei 18.222/2024** | **SIM** | catálogo `1k8ezfvkmMOiUsoL_pzA-vBIUhm44SvmC` · 448.283 B |
| Bônus: Lei 17.844/2022 (TDC) | SIM | catálogo `1LaCDRmdJ41EWnQbrt3WzOMouDIceQs6Z` · 632.288 B |
| Bônus: PDE 16.050/2014 | SIM (3 versões) | `1jX3lzgyYGjXe…` · 71.302.444 B (scan); catálogo `1wOSDStL2wPYQ…` · 2.656.698 B; `2014-07-31 - LEI 16050….pdf` `1sAr3lqpTPQiz…` · 927.810 B |
| Bônus: LPUOS 16.402/2016 | SIM (2 corpos) | `LEI Nº 16.402.pdf` `1HgiTJnG418wI6…` · 531.255 B; catálogo `1PfVAfD0Pxukeb…` · 1.436.029 B; `L16402.pdf` `13uonwxQCxVzsSw…` · 5.127.351 B |

### 3c. Quadro 2A e Quadro 6 (Fp)

Tudo na `_entrada` (grep na listagem de 1.365):

| Quadro | Arquivos — ID · bytes |
|---|---|
| **Quadro 2A (série LPUOS "QUADRO_N_FINAL")** | `003 - QUADRO_2A_FINAL.pdf` `14tYpbfw2q_FDS3EAuEUzeRNsKIks2wgU` · 365.180 B; `003 - QUADRO_2A_FINAL.csv` `1wX-koAPK9UKC9XyTvsSnsvsby-uPwnIW` · 940 B; `3-QUADRO_2A_FINAL.docx` `1qIhCeMImfdCRgLv8…` · 30.115 B (há também 2B, 1, 2, 3A… da mesma série) |
| **Quadro 2A do PDE (CA por macroárea)** | `PDE2013_SUBST2_Quadro_2A_CA_Macroareas.pdf` `1D0bge5O8yc60b8pHV4foQSrXF1kuw-Ax` · 268.150 B + `.csv` `1vTorsekskSqMQmYqMWx0l_v7xoAzv3qZ` · 1.880 B |
| **Quadro 6 — Fator de planejamento Fp** | `PDE2013_SUBST2_Quadro_6_Fator_planejamento_Fp.pdf` `1DET4erUd7b1uBmJi-sMqmK7QcznIBbag` · 188.812 B + `.csv` `1oakoO1ZyCwclapUWWed8SXEJD_6v1qMk` · 825 B |

Nota de precisão: o Quadro 6 (Fp) e o Quadro 5 (Fs) são quadros do **PDE 16.050/2014** (aqui na versão SUBST2 do PL de 2013); o pedido citava "da LPUOS 16.402", mas o Fp pertence ao PDE — os dois conjuntos (PDE e série QUADRO_N_FINAL) estão presentes. Conteúdo não foi aberto (lente restrita a existência/nome/tamanho); validar contra o anexo oficial na extração.

### 3d. Camadas geo

Grep na listagem da `_entrada` (todas lá, sem hash no nome):

| Camada | Status | Evidência |
|---|---|---|
| **ZEPEC_AUE** | **COMPLETA** (shp+dbf+shx+cpg) | shp `1o8kSDTfd-c3WqhjYE2Q_mX3w7PcU_ClZ` · 1.683.820 B; dbf 15.626; shx 6.028; cpg 5. Há também `ZEPEC_AUE_INDIC` completa |
| **ZEPEC_APP-BIR** ("APPa"/APP sobre tombado, vedação Art.124 §2) | **COMPLETA** | shp `1nSJNIe4lhxSGAuVgdY2bMbr0pkLyoQbN` · 74.568 B; dbf 821; shx 388; cpg 5 |
| ZEPEC_BIR / BIR_INDIC | COMPLETAS | shp 855.548 (`1SMJ5NlYfloTSOKt…`) / 358.660 (`1X0muNAcafJYXqb…`) |
| **SIRGAS_SHP_LOTES (oficial)** | **96 distritos, todos com os 4 componentes** shp/dbf/shx/cpg | grep na listagem: 96 `.shp` distintos; checagem por distrito: nenhum grupo ≠ 4 componentes. **ALERTA: nenhum LOTES tem `.prj`** — só existem 3 `.prj` em toda a `_entrada` (zeup_zemp, requalifica_centro, PLANO_DIRETOR_DRENAGEM); a projeção dos LOTES terá de ser assumida (SIRGAS 2000 / EPSG:31983) ou obtida de fora |
| **logradouro NBL** | **COMPLETA** | `SIRGAS_SHP_logradouronbl.shp` `1wWIKVfwaH9cLQSwmIHNaP2PO0c2u76U7` · 30.840.700 B; dbf 76.820.868; shx 1.755.996; cpg 5 |
| Extras confirmados | quadraMDSF.dbf, setorfiscal.dbf, benstombados, zeup_zemp, cota_solidariedade, Atualizacacao_Q14_anoref2025.csv (5.299.450 B, `1Q499wCFws3H1d3w0jY1PFYOkCD5PjieF`) e .pdf (9.390.252 B) | metadata/grep |

### 3e. Jurisprudência TDC / outorga / solo criado

| Item | Status | Evidência |
|---|---|---|
| **Acórdão que trata de TDC** | **1 encontrado**: `ACORDAO_ADI_2187640_ARCO_PINHEIROS.pdf` `11Qr4MUacbITsyRhfHhmHruZ7jCvYZjnC` · 42.841 B (+ 3 `.md` fatiados) | busca `title contains 'ACORDAO' and fullText contains 'transferência do direito de construir'` — só ele retorna |
| Acórdãos TJSP salvos (tema não-TDC pelo título; acervo IPTU) | 9+ PDFs: `ACORDAO_TJSP_2390222-33.2025…` (ED/AI), `1568276-30.2023`, `1053798-54.2024`, `1509864-53.2016` (AC/ED), `1054600-28.2019`, `1025594-05.2021` + `ARE_1216078_Acordao_Tema1062_STF.pdf` | busca `title contains 'acórdão'/'TJSP'…` — todos na pasta-espelho `1LGrKx7sY8Jot1b1ROG53mhb-yy-zHQLv` |
| Temas repetitivos STJ rotulados "IPTU-TDC" | txt temas 174, 262, 1158 etc. na `_entrada` (ex. `IPTU-TDC_stj-tema-1158.txt` `11BR6tZ4zPXIcaIBeRRQz4P5D4j61RSgy` · 782 B) | grep listagem |
| Súmulas STF/STJ | 27 arquivos com "sumula" no título na `_entrada` (com duplicatas `(1)…(5)`) | grep listagem (count 27) |
| Acórdão específico de outorga onerosa/solo criado | **NÃO identificado por título**; material de outorga existe como páginas SMUL (pdf/csv), `OUTORGA_ONEROSA.xlsx` (1.311.524 B) e estoques OUC Água Branca | greps "outorga"/"solo criado" |

---

## 4. Confronto de arrumação — o "C2 real" (A-08)

| Medida | Índice local (`drive-arrumacao/`) | Drive AO VIVO (2026-07-05) | Veredito |
|---|---|---|---|
| Arquivos na `01 — _entrada` | 1.360 (`de-para-COMPLETO-2026-07-04.csv`, 1.361 linhas − header) | **1.365 itens únicos** (busca `parentId='1grhqYgttj7…'`, 2 páginas dedup) | +5 |
| Arquivos do de-para que SAÍRAM da `_entrada` | esperado 1.360 movidos após execução | **0** (`comm`: todos os 1.360 IDs continuam lá) | **arrumação 0% executada** |
| Itens a mais na `_entrada` | — | 5 subpastas: `IPTU` (`1-fFkfJg0XTZiDLywmxhEhcFMOFigecAC`), `IPTU-Sergio` (`1BwXNDWYu57Zxr…`), `NOVOS` (`1_dpkw5DzyyXSvze…`), `Todos` (`1m3CiWeK72A_DHX…`), `Outros` (`1u1kbl7ZCzhyKnQ…`) — pastas antigas (criadas 2024-12/2026-04/05) que apareceram na `_entrada` depois do censo de 04/07; o de-para só listava arquivos | triagem pendente |
| Pastas-destino 00–05 | Organizer moveria 54/468/166/666/6 itens | **todas vazias** (00: 1 subpasta vazia; 2.1–2.7: 0; 03, 04, 05, 05—Geo/Mapas: 0) | consistente com 0 movidos |
| Quarentenas/lixeiras `99_*` | Sanear-Duplicatas (2026-06-20) previa apagar/mover | `99_LIXEIRA_DUPLICADOS` (DataLake) = **2.757 itens ~11,5 GB**; `99_LIXEIRA`/`99_QUARENTENA`/`99_PARA_DELETAR` do lago intactas | **saneamento também nunca rodou** |

Conclusão A-08: agora existe confronto real índice×Drive, e ele prova que **nenhum script de arrumação/saneamento foi executado até hoje** — o estado do Drive é o mesmo despejo achatado de 18/06, acrescido de material novo.

## 5. Duplicatas (~16–20 GB) — ainda vivas? SIM

Amostra por busca exata de título (mesmo nome + mesmo tamanho em pastas diferentes):

| Grupo | Tamanho unitário | Cópias vistas | Prova |
|---|---|---|---|
| `socios.csv` | 3.435.677.749 B (3,4 GB) | **≥5** (pág. 1 cheia com `nextPageToken`) — parents: `_entrada`, `1gmAOmJUDx…`, `1rzGUduCCz…`, `99_LIXEIRA`, `01B_BRONZE` | busca `title = 'socios.csv'` |
| `empresas.csv` | 2.269.763.986 B (2,3 GB) | **≥5** (idem) | busca `title = 'empresas.csv'` |
| `IPTU_2026.csv` | 937.865.216 B | **7** (exato, sem token) — inclusive 1 no root do shared drive `0APQMETkmU9TbUk9PVA` | busca `title = 'IPTU_2026.csv'` |
| `LEI Nº 15.044 … Catálogo.pdf` | 178.280 B | 3 pastas (`_entrada`, `114dBRSf3NWspqQ…`, `1PGpHRoAPj4iall…`) | busca fullText '13.475' |
| `Anexo I do Decreto 58_289_2018.pdf` | 121.684 B | **≥8** pastas | busca título '58.289' |
| `99_LIXEIRA_DUPLICADOS` inteira | ~11,49 GB / 2.757 itens (553/1000 da pág. 1 com sufixo de hash) | — | 3 buscas `parentId` |

Só nos 3 grupos pesados: ~4×3,4 + ~4×2,3 + 6×0,94 ≈ **28 GB em cópias redundantes** (excedente além da canônica) — coerente com (e acima de) a estimativa de 16–20 GB de 20/06.

---

## O QUE DESTRAVA O QUÊ

**ENCONTRADO no Drive → extraível na próxima onda (sem depender de ninguém):**
- **TDC core:** Decreto 57.536/2016 (corpo+anexos+csv) → destrava a ingestão A-11 (`leis/` TDC) e o rastreio das tabelas TDC já existentes; Lei 17.844/2022 e PDE 16.050 (corpo) já disponíveis de apoio.
- **IPTU histórico:** 8 leis verbatim (6.989/66, 10.235/86, 11.152/91, 13.250/01, 14.865/08, 15.044/09, 17.202/19, 17.577/21) → destrava B-08/B-09 (schema+vigência) para 8 das 12+1; as de 1966/1986 são scans grandes → rota com OCR.
- **Engines de valor:** Quadro 2A (LPUOS FINAL + PDE macroáreas) e Quadro 6-Fp (pdf+csv), Quadro 5-Fs, OUTORGA_ONEROSA.xlsx, Q14 ano-ref 2025 → destrava conferência do PCpt/OODC contra fonte.
- **Motor 3 GEO completo:** ZEPEC_AUE + APP-BIR + BIR (+INDIC), 96 distritos SIRGAS_LOTES (sets 4/4), logradouronbl, quadraMDSF, setorfiscal → destrava o overlay lote×tombamento×vedação. Ressalva: **sem `.prj`** nos LOTES (assumir EPSG:31983 ou baixar de novo do GeoSampa).
- **Jurisprudência:** ADI 2187640 (Arco Pinheiros — única peça com texto de TDC), acervo TJSP/STF/STJ de IPTU, temas STJ, súmulas → destrava tese IPTU; base jurisprudencial TDC segue rala.

**NÃO está no Drive → precisa vir de fora (Cadlem/GeoSampa/tribunais):**
1. Verbatim das leis **10.365/1987, 11.338/1992, 12.350/1997, 13.475/2002, 17.759/2022** (5 das 12 pendentes).
2. **Corpo do Decreto 58.289/2018** (só Anexos I e V existem).
3. `.prj` oficiais das camadas SIRGAS (só 3 no Drive).
4. Acórdãos específicos de TDC/outorga além da ADI Arco Pinheiros.

**Pré-condição operacional que este censo prova:** os scripts `Organizar-Entrada-2026-07-04.gs` e `Sanear-Duplicatas-*.gs` **nunca rodaram** — o Drive continua 100% no despejo, com ≥28 GB de duplicatas pesadas vivas. Qualquer extração pode partir da `_entrada` como cópia canônica (é onde está tudo), mas a arrumação/saneamento continua sendo execução pendente do dono (Apps Script).
