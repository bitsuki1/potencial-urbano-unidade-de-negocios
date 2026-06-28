# Proveniência — fontes externas (titularidade / Atc) puxadas VERBATIM do Drive
> PU 14 · 2026-06-28. Leitura MCP autorizada. `.xlsx` = bytes verbatim do Drive; `.csv` = cópia de trabalho (parse stdlib). Nada alterado no Drive.

| Arquivo | Drive fileId | Tamanho | Traz | Uso |
|---|---|---|---|---|
| `ANUAL-2022.xlsx` (+`.csv`) | `17AgTa3aSavPSZyhkzq8cUClOHpYamT94` | 614 KB · 2.884 linhas · 257 col | **Proprietário** · SQL_Incra · **Área do terreno** · uso · zona · endereço | dono + Atc por SQL (alvarás 2022) |
| `sissel_ANO_2024.xlsx` (+`.csv`) | `1xS2NCo3w5lFCSM3LHXaRYjTeQ6SxTdEb` | 553 KB · 1.638 linhas | proprietário + processo (cabeçalho com preâmbulo — mapear) | dono (pendente: achar linha de cabeçalho) |

> Cruzamento por SQL em `zepec/donos.py` → `zepec/limpo/donos_encontrados.csv` → ligado à ferramenta (`proprietario`/`fonte_dono`).
> **Próximas fontes a somar** (mesmo método): SISSEL 2024 (mapear cabeçalho) · OODC_2024-2025 · OUTORGA_ONEROSA · série ITBI (45 anos) · IPTU_2026 (Atc de todos → **Supabase**, é pesado).
