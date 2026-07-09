# Triagem — `_entrada/iptu/`

> Triagem deterministica (Pipeline Etapa 2 — CLAUDE.md Parte 3).
> Classifica os 7 arquivos despejados pelo MOU na zona de entrada IPTU.
> Data: 2026-07-09.

## Resultado

| # | Arquivo | IPTU? | Classificacao real | Observacao |
|---|---------|-------|--------------------|------------|
| 1 | `anexo-i-integrante-da-lei-no-15-889-de-5-de-novembro-de-2013.txt` | **SIM** | Lei Municipal 15.889/2013 — revisao da PGV, aliquotas progressivas IPTU, Tabela VI (valor m2 construcao) | **CHAVE para o corpus IPTU.** Verbatim integral. Ingerida em `leis/municipal-sp/`. |
| 2 | `base-de-calculo-do-iptu-migalhas.txt` | **SIM** (doutrina) | Artigo doutrinario (Kiyoshi Harada, Migalhas, set/2025) sobre base de calculo do IPTU pos-EC 132/23 | NAO e lei/norma. Referencia doutrinaria util; nao entra no corpus de leis. Manter aqui como material de estudo. |
| 3 | `lei-no-17-733-de-11-de-janeiro-de-2022-catalogo-de-legislacao-municipa.txt` | **NAO** | Lei Municipal 17.733/2022 — Infraestrutura de suporte para ERBs (antenas de telecomunicacao) | Tema: telecomunicacoes/antenas, sem relacao com IPTU. |
| 4 | `lei-no-17-844-de-14-de-setembro-de-2022-catalogo-de-legislacao-municip.txt` | **NAO** | Lei Municipal 17.844/2022 — PIU Setor Central (Projeto de Intervencao Urbana) | Tema: urbanismo/intervencao urbana. Ja existe no corpus como TDC (lei-municipal-saopaulo-17844-2022). |
| 5 | `lei-no-11-428.txt` | **NAO** | Lei Federal 11.428/2006 — Mata Atlantica (bioma) | Tema: meio ambiente/bioma. Esfera federal, sem relacao com IPTU municipal. |
| 6 | `lei-no-14-094-de-6-de-dezembro-de-2005-catalogo-de-legislacao-municipa.txt` | **NAO** | Lei Municipal 14.094/2005 — CADIN Municipal (cadastro de inadimplentes) | Tema: cadastro de inadimplentes. Tangencial (cobranca), mas NAO e IPTU. |
| 7 | `decreto-no-57-443-de-10-de-novembro-de-2016-catalogo-de-legislacao-mun.txt` | **NAO** | Decreto Municipal 57.443/2016 — Posturas | Tema: posturas municipais. Ja existe no corpus (decreto-saopaulo-57443-2016). |

## Resumo

- **2 de 7** arquivos sao relevantes para IPTU (1 lei + 1 doutrina).
- **5 de 7** NAO sao IPTU — foram despejados na pasta errada ou capturados por engano.
- Nenhum arquivo foi movido ou excluido. Esta triagem DOCUMENTA a classificacao para o pipeline (Principio 1.2: extrai puro, sem misturar).
- Os 5 arquivos nao-IPTU permanecem aqui intocados. Se necessario, podem ser reclassificados para outra zona de entrada ou descartados pelo dono.

## Acao tomada

- `anexo-i-integrante-da-lei-no-15-889-de-5-de-novembro-de-2013.txt` → ingerida como `leis/municipal-sp/lei-municipal-saopaulo-15889-2013.md` + `.json`.
- `base-de-calculo-do-iptu-migalhas.txt` → mantida aqui como referencia doutrinaria (nao e norma, nao entra no corpus de leis).
