# HANDOFF & PENDÊNCIAS — Projeto RAG IPTU + TDC (Potencial Urbano)

> **Ponto de entrada para uma instância NOVA aberta no repo do projeto.** Estado vive no git, não na
> conversa. Trabalho conduzido pelo Escritório do MOU (PMO) até 2026-06-18; daqui segue a instância do projeto.
> Formato dos artefatos segue convenção do escritório: cada item de corpus tem par `<id>.md` + `<id>.json`
> com `status_pipeline` ∈ {bruto → fatiado → tagueado → validado → indexado} (vocabulário canônico do CLAUDE.md 2.3), registro honesto (sem inflar), vacinas declaradas.

## 0. Como retomar (ordem de leitura)
1. Este arquivo.
2. `PROJETO-RAG-JURIDICO-IPTU-TDC.md` (instanciação/visão).
3. `docs/INVENTARIO-E-LACUNAS-IPTU-TDC.md` — inventário D24 do despejo no Drive + mapa de lacunas + **fileIds** dos ativos (inclui a seção CORREÇÃO/vacina no fim).
4. `docs/PROMPTS-EXTRACAO-EXTENSAO.md` — prompts prontos de captura via extensão (5 lotes).
5. Os corpora: `leis/federal/`, `leis/municipal-sp/`, `jurisprudencia/` (+ `_capturas/` com o verbatim cru).

## 1. Estratégia do projeto (altitude)
RAG consultável **por imóvel (lote/SQL)** que responde: (a) dá pra mexer no IPTU e/ou vender potencial (TDC)? (b) quanto vale? (c) quem é o dono? Três camadas: **Jurídico (o "pode")** · **Precificação (o "quanto")** · **Proprietário/cliente (o "quem")**.
Esteira: **E1 saneamento & corpus (ATUAL)** → E2 indexar preço → E3 base de proprietários → E4 cruzamento (motor) → E5 produto (lista de alvos por imóvel).
Entregável final: o RAG + motor de cruzamento → **dossiê/lista de prospecção por imóvel** (oportunidade + valor + dono).

## 2. FEITO (com referência de commit, branch `claude/iptu-tdc-document-mapping-mjm1sn`)
- **59 stubs honestos** criados (12 federais, 15 municipais SP, 32 jurisprudência), `status_pipeline=bruto`. (commit 3eb7e21) _[nota 2026-06-20: estado do commit inicial; hoje as 32 juris são `tagueado` e as 12 federais já têm texto verbatim — ver linha abaixo e `MANIFESTO.json`.]_
- **Jurisprudência 32/32 INGERIDA verbatim** → `status_pipeline=tagueado` (corrigido de `processado`, que estava fora do vocabulário canônico — auditoria 2026-06-20); cru em `jurisprudencia/_capturas/`. **2 fora de escopo** (`stf-tema-1020`=ISS, `stj-resp-1658054`=previdenciário/não-verificado — sinalizados no `MANIFESTO.json`) + 1 com `revisao_pendente=true` (`stj-resp-1658054`). (5521392, 8c65de7)
  - Correções de qualidade feitas: stj-resp-1130545 (tema 371→387), stf-tema-94 (redação literal), tipos de 1202136/1645832 (acórdão, não repetitivo), stf-tema-155 (texto oficial).
- **Inventário D24 do despejo no Drive + mapa de lacunas + reconciliação com Drive completo.** (b0185a1)
- **Vacina/correção** sobre os PDFs de lei do despejo (ver §5). (286629b)
- Oráculo geográfico V3 com rodapé completado (96 distritos GeoSampa). (785c112)
- **No repo do escritório** (não aqui): processo reutilizável `processos/EXTRACAO_VIA_EXTENSAO.md` (captura via extensão do navegador com fallback de tela) + Regra de Ouro "prompts sempre na tela".

## 3. PENDÊNCIAS por etapa
### E1 — Corpus jurídico (fechar)
- [x] **12 leis FEDERAIS — FEITO** (upload do MOU 2026-06-19): texto verbatim ingerido em `leis/federal/` (`status_pipeline=bruto`, aguardando fatiamento). _Supera o item antigo "não estão no despejo"._
- [ ] **Capturar 14/15 leis MUNICIPAIS** — seguem `bruto`. Usar Lote 2.
- [ ] **Ingerir a LEI 11.152/1991** (única com PDF confirmado no despejo) e **criar stubs + ingerir as municipais bônus** já no despejo (com fileId no inventário §CORREÇÃO): 11.308/92, 11.614/94, 13.698/03, 13.776/04, 14.089/05, 17.092/19 + decretos 52.884, 56.954, 57.770, 58.592, 60.939, 63.698.
- [ ] **Capturar a LEI 6.989/66** (institui o IPTU em SP) — ausente em todo lugar; e conferir **11.154/1991**.
- [ ] Resolver os 2 itens fora de escopo: `stf-tema-1020` (é ISS) e `stj-resp-1658054` (é contribuição previdenciária) — ver §4.
### E2 — Insumos de precificação (indexar)
- [ ] Indexar GeoSampa lote a lote (`LOTES_Parte_1–5_IA.csv`), zoneamento, `MASTER_PARAMETROS_URBANISTICOS.xlsx`, quadros PDE/LPUOS. (todos no Drive — fileIds no inventário)
- [ ] **Lacuna real:** PGV / valor venal oficial vigente 2026 por SQL (origem SF-SP — não temos).
- [ ] Integridade GIS: zoneamento com 135 camadas mas ~31 com `.shp` — rebaixar faltantes do GeoSampa.
### E3 — Base de proprietários (montar)
- [ ] Indexar `IPTU_2026.csv` (937 MB — verificar se tem SQL+contribuinte), série `GUIAS_DE_ITBI_PAGAS` 2006–2024, `socios.csv` (3,43 GB). (no Drive)
- [ ] **Lacunas reais:** `empresas.csv` e `holdings.csv` (Receita/CNPJ) — só `socios.csv` localizado.
### E4 — Cruzamento / E5 — Produto
- [ ] Motor que une as 3 camadas por lote (chaves SQL→Valor, ZONA→CA_max já mapeadas no `ORACULO_V4` do legado).
- [ ] Saída: lista de alvos por imóvel.

## 4. DECISÕES aguardando o MOU (com recomendação)
1. **Expandir o corpus** com as leis municipais bônus do despejo + 6.989/66 + 11.154/91? → recomendo **SIM** (núcleo do IPTU paulistano).
2. **`stf-tema-1020`** (ISS, não IPTU) → realocar p/ anexo "correlatos". **`stj-resp-1658054`** (previdenciário, fora de escopo; numeração veio errada do mapa antigo) → remover; se houver precedente de tombamento que era a intenção, capturar o número certo. → recomendo **sim** aos dois.
3. **Prioridade E2/E3 vs fechar E1**: recomendo **paralelo** ("não economizar").

## 5. Vacinas / pegadinhas (não repetir os erros)
- **Não confiar em classificação de PDF por NOME sem abrir.** O 1º agente "viu" leis federais em `dados_pericia6` — FALSO (a pasta é shapefile + tombamento). Sempre abrir/paginar.
- **`status_pipeline=bruto` é honesto** — não declarar "capturado/100% pronto" sobre stub que só tem ementa. (O legado tem PDFs "DADOS PERFEITOS" que mentem; o próprio `ESTRUTURA_SILVER_IA` admite "aguardando extração".)
- **`fonte.url` sempre oficial** (planalto/prefeitura/stf/stj) — terceiro é pista, não fonte.
- **Captura via extensão:** o download do navegador tira a subpasta e cai no Downloads; o robusto é a extensão **colar o verbatim na resposta** (vira Doc no Drive, que a instância lê via MCP do Google Drive). `scon.stj.jus.br` redireciona — abrir via `www.stj.jus.br`.
- **NÃO usar agente-dentro-de-agente** para enumerar Drive (empaca). Um agente single-level com fileIds em mão resolve.

## 6. Canais e ativos
- **Google Drive (MCP) FUNCIONA** nesta conta (eduardo@saobentoservicos) — leitura direta de Docs/PDF/planilha.
- **Pasta de despejo:** "01 — _entrada (despejo IPTU+TDC)" id `1grhqYgttj7KnJmiu9U73z-lXFHnFthov`.
- **Ativos pesados já no Drive (fileIds no inventário §RECONCILIAÇÃO):** `socios.csv`, `IPTU_2026.csv`, série ITBI 2006–2024, FUNDURB (fila fev/2026 + balanços).
