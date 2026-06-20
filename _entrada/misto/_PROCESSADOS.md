# _entrada/misto/ — crus já PROCESSADOS (accounting, não apagar)

> Auditoria triplo-limpo do Escritório do MOU — 2026-06-20.
> **ATUALIZADO 2026-06-20 (2ª auditoria):** os 12 federais + a 7228 foram **PROMOVIDOS a verbatim
> integral** (`promover_entrada.py`) e estão **`indexado`** — os `.md` agora carregam o verbatim
> (não só `fonte.url`). Status abaixo reflete isso.
> Os 24 `.txt` aqui são o **upload bruto do MOU (2026-06-19)**, JÁ processados para `leis/` e
> `jurisprudencia/`, e mantidos como **fonte verbatim de proveniência** (RO-09 nada se descarta).
> Para os 11 STF existe TAMBÉM uma captura anterior em `jurisprudencia/_capturas/` — **conteúdo DIFERE**
> (duas renderizações do mesmo ato), por isso ambas preservadas.
>
> A "zona de despejo" está **contabilizada** (não vazia): tudo abaixo tem destino.

| cru (_entrada/misto/) | destino | status_pipeline |
|---|---|---|
| dl-57-1966, ec-29-2000, ec-116-2022, ec-132-2023, lei-federal-{4591-1964,6015-1973,6830-1980,8009-1990,8668-1993,9514-1997,10931-2004,11101-2005} | `leis/federal/` (12) | **indexado** (verbatim, 2026-06-20) |
| lei-municipal-saopaulo-7228-1968 | `leis/municipal-sp/` | **indexado** (verbatim) |
| stf-{sumula-539,sumula-589,sumula-668,sumula-670,sumula-724,sv-19,tema-94,tema-155,tema-523,tema-1020,tema-1084} | `jurisprudencia/` (11) | tagueado |

**Fora de escopo (sinalizados no MANIFESTO.json):** `stf-tema-1020` (ISS, não IPTU); `stj-resp-1658054` (previdenciário).
**Pendência real:** as **14** municipais-SP de `leis/municipal-sp/` que NÃO vieram neste upload (todas
menos a 7228, já indexada) seguem como **resumos não-verbatim** (`confianca: baixa`) — re-ingerir dos
PDFs do Drive e rodar `promover_entrada.py` (BACKLOG B-4).
