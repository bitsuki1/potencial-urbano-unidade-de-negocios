# Triagem do HOLD (49 arquivos "ILEGÍVEL") — 2026-07-19 (PU 22)

> Re-verificação dos 49 itens de `HOLD-ILEGIVEL-RECHECAR.csv`, com **tamanho real (fileSize) e mimeType**
> lidos do Drive via conta MCP (somente leitura; nada escrito no Drive — respeita a janela de concorrência
> D-DONO 2026-07-18). Fecha o item "re-extrair os 49 HOLD" do D-DONO.

## Veredito
**NENHUM dos 49 é texto normativo OFICIAL, legível e novo.** Zero itens a ingerir no corpus de `leis/`.
A "ilegibilidade" da vistoria anterior se explica: são **imagens de mapa, dados transacionais (xlsx),
metadados geo, um derivado `_ia`, um acórdão vazio, ou duplicatas de leis que JÁ estão no corpus** —
capturadas (bem) do portal/Planalto, não desses PDFs.

## Distribuição por classe (49)
| Classe | Qtde | Disposição |
|---|---:|---|
| IMAGEM-MAPA (mapas/plantas, sem texto de lei) | 12 | Não é corpus de leis. Camada geo (destino 05). Há pares byte-idênticos (deduplicar). |
| DADO-TRANSACIONAL (Guias de ITBI pagas, xlsx) | 20 | **Não entra no RAG.** Dataset oficial da SF/PMSP → rota **Comercial + Tec&Dados** (ver abaixo). |
| DUPLICATA-JÁ-INGERIDA (LPUOS/PDE) | 12 | Lei já no corpus do portal. **Pior: os próprios PDFs são inúteis** (75 KB = captura do *menu* do site Gestão Urbana; 5.152 bytes = página "500 - Erro interno"). Descartar. |
| GEO-METADADO (`*_geosampa_apas.ods`) | 3 | Metadado de dataset APAs (GeoSampa). Não é lei. |
| CRIADO (`documento_final_ia.pdf`, 34 MB) | 1 | Derivado produzido ("_final_ia" = concatenação de quadros). **SÓ-IDEIA (regra 1.8)** — nunca vira fonte. |
| VAZIO-CORROMPIDO (`ACORDAO_TJSP_2390222-33.2025`, 1.471 bytes) | 1 | Sem conteúdo. Re-capturar do primário (TJSP), não do Drive. |

## Achados que viram AÇÃO / LEAD
1. **Dataset ITBI pago 2006→2025 (20 anos, ~500 MB, xlsx).** Série **contínua e completa**; microdados reais
   de transação: SQL do cadastro, logradouro, natureza, **valor declarado**, **valor venal de referência**,
   data, cartório, matrícula, áreas, uso e padrão IPTU. É fonte **oficial primária** (SF/PMSP) — **não** é um
   derivado nosso (não cai no 1.8). **Rota:** base de comparáveis de mercado para **Comercial** (prospecção) e
   insumo de calibração para **Tecnologia e Dados** (tabelas → valuation, sempre rastreável ao registro).
   NÃO em `leis/`. → nova pendência de backlog (não bloqueia nada).
2. **Acórdão TJSP 2390222-33.2025.8.26.0000** — o PDF do Drive está vazio (1.471 bytes). Se for de interesse,
   re-capturar do ESAJ/TJSP pelo número CNJ e, sendo legível, entra em `jurisprudencia/` (liga-se ao item
   "jurisprudência inteiro teor").
3. **Mapas (12) e geo-metadados (3):** pertencem à camada geo (Motor do Mapa), não ao RAG de leis. Se um dia
   forem tratados, deduplicar os pares idênticos (Mapa03_QUOTA, Mapa1_ZONAS, Mapa_1_ZEPEC, MAPA_18081≡PL_586).

## Método (auditável)
Metadados dos 49 lidos via MCP Google Drive (`get_file_metadata`, `contentSnippet`), 2026-07-19. Classificação
por tamanho + mime + snippet; nenhum download de conteúdo foi necessário (os snippets já revelaram a natureza).
Fonte da lista: `HOLD-ILEGIVEL-RECHECAR.csv` (drive_id por linha).
