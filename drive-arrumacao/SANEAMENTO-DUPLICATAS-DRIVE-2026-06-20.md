# Saneamento de duplicatas no Drive — manifesto PRONTO (NÃO executado)

> Auditoria triplo-limpo do Escritório do MOU — 2026-06-20. Lente single-level via MCP.
> **DECISÃO DO MOU (2026-06-20): EXCLUIR** (lixeira do Drive, recuperável ~30 dias), mantendo 1 cópia canônica de cada grupo.
>
> **EXECUTOR PRONTO:** `drive-arrumacao/Sanear-Duplicatas-PotencialUrbano.gs` (Apps Script).
> Como rodar (o MCP do Drive não apaga — quem apaga é o Apps Script na sua conta):
> 1. Abra o projeto Apps Script da arrumação (mesmo do `Arrumar-Drive-PotencialUrbano.gs`); cole/adicione este arquivo.
> 2. Rode `sanearDuplicatas()` com `DRY_RUN=true` (padrão) → leia **Ver > Execuções/Logs**: ele lista o que APAGARIA sem tocar em nada.
> 3. Confira; mude `DRY_RUN=false` no topo; rode de novo → manda as duplicatas para a Lixeira.
> O script só apaga uma cópia depois de CONFIRMAR que a canônica do grupo existe; a Fase 2 só apaga duplicata exata (nome+tamanho).

## Quadro
- A pasta de despejo `1grhqYgttj7KnJmiu9U73z-lXFHnFthov` foi **achatada** (subpastas
  `dados_periciaN/...` dissolvidas) — os docs `docs/INVENTARIO-DRIVE-*.md` (2026-06-18)
  descrevem uma árvore que **não existe mais**. Dois re-uploads em 2026-06-18 (16h/19h).
- **Espaço recuperável estimado nas pesadas: ~16–20 GB.**

## VACINA antes de apagar (ler!)
1. Confirmar que o conjunto **SIRGAS_SHP_LOTES** (96 distritos, `.shp/.shx/.dbf/.cpg` +
   conferir `.prj`) tem ≥1 cópia íntegra preservada — o flatten de 18/06 pode ser a
   única com geometria real.
2. O plano `Arrumacao Potencial Urbano FINAL` está em **DRY-RUN** e aponta para a árvore
   ANTIGA — **não** usá-lo como mapa do despejo achatado sem revalidar IDs.
3. Excluir = lixeira do Drive (recuperável ~30 dias). Preferir MOVER p/ pasta `99 — Lixeira-triagem` se houver qualquer dúvida.

## Grupos de duplicata (id a MANTER em **negrito**)

### Heavy assets (maior ganho)
| Grupo | Manter | Remover (ids) | Ganho |
|---|---|---|---|
| socios.csv (3,4 GB) | **1gftoKzFaD-NyKClBg3SH8Eo0FYncQYvt** | 1Lffz6w6OvS-5KqakDT71ZqIzsudRLnoI · 1ncSTA-P2GfV2cPN-y1f2cnjqFDGSqa9e | ~6,9 GB |
| empresas.csv (2,3 GB) | **1uRWg7wA4KuppJ1TSdEwRmV3H06fTXlnj** | 18Q-_8iD5ZihVh-UnmD4itZ8WEa19g02a · 1u0ZaQCqfG0Moq2eroL-8_E1njnHJbgP5 | ~4,5 GB |
| IPTU_2026.csv (938 MB) | **1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM** | 1oX6BDTF_MJhrt8es4xh3N-cFtDbeoNGt · 1EubfSLtbGNF5G2MLS9eT_DiAsVCtv0fM · 1A3NK8K6wAn4ZjGCl5rqb2mCB8j50t0Pl · 1GOBf3pOYrDATCTOfMHLdbG1Iv82kV7Qt · 1Uvb9CYQNomG00MJo0kLAgOL3F2Xb8ay- | ~4,7 GB |
| holdings.csv (60 MB) | **1BrBRzC3G4atGZ8JqRZhGp4OnvBZTjOgr** | 1lBfWs1FCsxCTgpAu_5WzbZJ8WnLodxi9 · 1LGUIQysj-1_8deN8AeQi5ChwORjyoWHR · 17WdJjyVAg6macYZ9DjM-xIiR5bEFqjQo · 1fdabbNncuOexRrmIEvP1N2L-oNyZmk-j · 1H3-gburttjEyLYmBBUH1qM7DH1fxUEZL | ~0,3 GB |
| Série GUIAS ITBI 2006–2024 | conjunto em parent **1GvKF0ALRN_B…** | cópias-hash em `1ds4u4ZpoLl_…` + duplicatas na raiz do despejo + `13rAbexq2Gxy…` | dezenas de MB |
| MASTER_PARAMETROS_URBANISTICOS.xlsx | **1ZcgJAkqOnfS2DN0B2v4oHZbM-O8PeMfb** | cópias em `1ds4u4ZpoLl_`, `1KtUVx6YlRwx`, `1gzcwv9Fvuiz` | pequeno |

### Arrumacao Potencial Urbano (byproduto do Apps Script — dry-run)
- **Manter:** `1Wt2eFe-05D5fU8FsjeH0UiGFyokBcAa6U-sqDxFx0k8` (FINAL 01:20, mais recente).
- **Remover intermediárias:** 1mFJdqwz…(23:17) · 15GmJ2Nk…(00:22) · 1Bcyd37A…(00:47) · 1LgVwo5x…(01:00) · 13V2r0oS…(01:03) · 1rYAJMQo…(01:08) · 1-u2l3VK…(01:15).
- **CSV duplos idênticos (67.586 B):** remover `1Cp1Fl7QSR_Vr34wOvtIv7yVu_IIvkvIl` **ou** `1nRkAywkknccPHIRM8ve1PFh3eJUiKCwh` (manter 1). Export maior `1CEdO2f8gj9vcBlGQXqXMmSU5-LzstIGj` (117 KB) pode ficar.

### Jurisprudência STF/STJ `.txt` com sufixo `(1)…(5)`
~30 duplicatas na raiz do despejo (ex.: `stf-sumula-539` ×6). Manter 1 por súmula/tema/REsp.

### Lixo técnico (remoção segura)
- AUDITORIA vazias 4 B: `1JM7spa4…`, `1k-zbLK3…`
- `test-download.txt` `1--RLUIR…`, `Nova_test.txt`, `mover_pdfs_STJ.ps1`, logs `.txt`, `documento_final_ia.pdf` (auto-invalidado), GatewayPDF ×4 (`1MIWFnN…`,`1YiWDsj_…`,`1qmjICeF…`,`14glqKHH…` → manter 1).

## Achados POSITIVOS (lacunas dos docs RESOLVIDAS no Drive)
- **T-2 resolvida:** `Atualizacacao_Q14_anoref2025.csv` (5,3 MB, **1Q499wCFws3H1d3w0jY1PFYOkCD5PjieF**) — o "valor V por SQ" do Oráculo V4 EXISTE.
- **T-5 resolvida:** os 96 `SIRGAS_SHP_LOTES_01..96` têm `.shp` reais na raiz (conferir `.prj`).

## Discrepância docs↔Drive a propagar
Os `docs/INVENTARIO-DRIVE-*.md` registram IDs antigos; após o flatten surgiram **novos
IDs** para os mesmos ativos (cópias). Nenhum ativo SUMIU — mudou a estrutura e multiplicaram-se cópias. Atualizar os inventários após o saneamento (rodar de novo o catálogo com os IDs sobreviventes).
