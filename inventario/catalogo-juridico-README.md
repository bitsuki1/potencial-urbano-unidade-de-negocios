# Catálogo Jurídico do Drive — verificação de completude

**Data:** 2026-06-18 · **Arquivo:** `catalogo-juridico-drive.csv`

## Por que este arquivo existe
Resposta à cobrança do operador: *"você já cravou que o documento não existe? se
não existir mesmo me manda os links"*. Em vez de afirmar de memória, fez-se a
**varredura direcionada no Drive** (MCP `search_files`, por `title` + `fullText`)
e a enumeração da pasta-cofre **"01 — _entrada (despejo IPTU+TDC)"**
(`drive_id 1grhqYgttj7KnJmiu9U73z-lXFHnFthov`).

## Veredito
**O backbone normativo está COMPLETO no Drive.** Nada falta baixar; nenhuma
captura externa (extensão/anti-bot) é necessária — a fonte verbatim das leis é o
próprio Drive. (Codex RO-21 e §7.)

> **CONCILIAÇÃO (2026-06-20, auditoria triplo-limpo):** completo no Drive ≠ ingerido
> no repo. As 12 federais já estão verbatim em `leis/federal/`; **15 municipais-SP em
> `leis/municipal-sp/` ainda são resumos não-verbatim** (`confianca: baixa`) — falta
> RE-INGERIR dos PDFs do Drive (fatiamento interno, não captura externa).

## Conteúdo do CSV
Uma linha por arquivo da pasta de entrada (920 únicos), com `drive_id` e
`view_url`. Colunas: `categoria, titulo, drive_id, mime, tamanho_bytes, pasta,
view_url`.

| categoria | nº | o que é |
|---|---|---|
| URBANISTICA_PDE_LPUOS_COE | 71 | PDE 16.050, LPUOS 16.402, COE 16.642, SMUL/CTLU/CEUSO |
| PATRIMONIO_ZEPEC_TDC | 100 | tombamento/ZEPEC-APC/CONPRESP — origem da TDC |
| LEI_MUNICIPAL_IPTU | 57 | Lei 6.989/66 + cadeia de alterações do IPTU |
| IPTU_TRIBUTARIO_DOUTRINA | 63 | doutrina/análises tributárias (IPTU/ITBI) |
| DECRETO_MUNICIPAL | 41 | decretos 52.884 → 64.018 |
| ATO_INFRALEGAL | 22 | Instruções Normativas SF/SUREM, portarias, resoluções |
| FEDERAL_E_CF | 16 | Estatuto da Cidade, CTN, CF art. 156, L6.015/6.830/8.009/9.514/10.931/11.101 |
| JURISPRUDENCIA | 69 | acórdãos TJSP, STF Tema 1062, STJ Súmula 160, REsp |
| NORMA_TECNICA | 2 | ABNT NBR 14653-2 (avaliação de imóveis urbanos) |
| TABELA_DADO | 109 | planilhas (XLSX/XLS/ODS/CSV) |
| TEXTO_AUXILIAR | 31 | .txt/.md/.json |
| OUTRO_BINARIO_GEO | 339 | binários, geo (octet-stream) e PDFs de processo |

## Ressalva honesta
O catálogo cobre a pasta de entrada (o despejo consolidado). Cobre tudo que os
mestres referenciam. Não é prova de "toda lei concebível do universo": se faltar
um item específico, basta nomeá-lo que se verifica no Drive em segundos (RO-21).
