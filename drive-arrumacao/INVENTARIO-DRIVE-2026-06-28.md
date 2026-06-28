# Inventário do Drive do PU + plano de limpeza — 2026-06-28

> Trazido pelo **Escritório do MOU** (varredura a pedido do MOU, 2026-06-28). Read-only; o passo destrutivo é do MOU (AUD-02).
> **Pasta varrida:** `1grhqYgttj7KnJmiu9U73z-lXFHnFthov` — o despejo "_entrada" do Potencial Urbano (dono `eduardo@saobentoservicos.com.br`).
> **Método:** acesso confirmado via MCP Google Drive; varredura por janelas de tempo (a rajada de shapefiles 2026-06-18 19:21–19:23 = ~555 componentes GIS) + leitura direta das súmulas/temas (criados 16:04) + cruzamento com o `LISTA-APAGAR-script.csv` (auditoria 2026-06-20).

## 1. DOCUMENTOS DO PROJETO — MANTER (o acervo real)
Estes são o **insumo do produto** — NÃO apagar. Agrupados por tipo:

| Tipo | O que é | Papel na esteira |
|---|---|---|
| **Camada GEO (SIRGAS shapefiles)** | `SIRGAS_SHP_LOTES_*` + zoneamento (ZEIS, ZCOR, ZDE, ZEM, ZEP, ZEPAM, ZEPEC, ZEU, ZC, VETOS…) — `.shp/.shx/.dbf/.prj/.cpg` por distrito (AGUA RASA…ARTUR ALVIM…) | **E4/H3** — o JOIN espacial lote × zona × IPTU. É o que liga `sql/codlog → zona` para o `oodc_por_imovel`. |
| **PDFs de norma** | Leis municipais: PDE 16.050, LPUOS 16.402, COE 16.642, + 15.889, 16.757, 17.557, 17.719, 18.095, 18.270, 18.330… e o **Quadro 14** (`PDE2013_SUBST2_Quadro_14_cadastro.pdf`) | **E1 corpus** — fonte verbatim das leis + a tabela Q14 de valor de terreno. |
| **Jurisprudência (.txt)** | STF temas (94, 155, 523, 1020, 1084…), STJ súmulas (314, 392, 397, 409, 481, 539, 589, 614, 626, 668, 670, 724…), REsp/RE (1112646, 1130545, 1202136, 1645832, 1658054…), SV-19 | **E1 corpus** — jurisprudência (já parcialmente no repo como `jurisprudencia/`). |
| **Cadastro (CSV grandes — versão canônica)** | `socios.csv` (3.4 GB), `empresas.csv` (2.3 GB), `IPTU_2026.csv` (938 MB), `holdings.csv` (60 MB) — **1 cópia canônica de cada** | **E3 proprietários** — o "quem" do produto (dono por imóvel). |

## 2. LIXO — a limpar (3 classes, todas reversíveis → Lixeira)

### Classe A — duplicatas dos arquivões (CSV) · **JÁ mapeada** · ~7 GB
Cópias exatas de `socios/empresas/IPTU_2026/holdings` + intermediárias de "Arrumacao" + lixo trivial (AUDITORIA vazia 4 B, `test-download.txt`).
- **Lista:** `LISTA-APAGAR-script.csv` (IDs verificados na auditoria 2026-06-20).
- **Script:** `Sanear-Duplicatas-PotencialUrbano.gs` → função `sanearDuplicatas()` (FASE 1 por ID + FASE 2 dedup nome+tamanho).

### Classe B — duplicatas com sufixo " (N)" · **gap novo, coberto agora**
O Drive, ao re-subir arquivo de mesmo nome, cria `stf-tema-1084 (1).txt`, `stf-sumula-589 (2).txt`, etc. — **nome diferente**, então a FASE 2 do script antigo NÃO pega. Dezenas dessas nas súmulas/temas.
- **Script:** `Sanear-Sufixo-N-e-Ruido.gs` → função `sanearSufixoNeRuido()` (FASE 3). Genérico: escaneia a pasta em runtime, e só manda à Lixeira o " (N)" **quando o original (sem sufixo) existe E o tamanho bate** (tamanho diferente = versão diferente → marca INCERTO, não apaga).

### Classe C — ruído de sessão (.txt)
Notas de saída de IA salvas como arquivo: `## Extração concluída — 14 arquivos gerados.txt`, `Todas as 7 páginas renderizaram normalmente.txt`, `Todos os 12 arquivos foram baixados com sucesso.txt`.
- **Script:** mesma `Sanear-Sufixo-N-e-Ruido.gs` → FASE 4 (padrões explícitos + só arquivos pequenos `.txt`).
- **INCERTOS preservados:** nomes truncados/ambíguos (`s.txt`, `r que.txt`) → NÃO apago; você decide.

## 3. COMO RODAR (AUD-02 — dry-run primeiro, sempre)
1. **Apps Script** (script.google.com) na conta `eduardo@…`. Cole os 2 `.gs` (já estão neste repo, `drive-arrumacao/`).
2. **Classe A:** abra `Sanear-Duplicatas-PotencialUrbano.gs`, rode `sanearDuplicatas()` com `DRY_RUN=true`, leia o Log, confira, mude `DRY_RUN=false`, rode de novo.
3. **Classes B+C:** abra `Sanear-Sufixo-N-e-Ruido.gs`, rode `sanearSufixoNeRuido()` com `DRY_RUN=true`, confira o Log (quantos " (N)" e ruído, e os INCERTOS), mude `DRY_RUN=false`, rode de novo.
4. Tudo vai p/ a **Lixeira do Drive** (recuperável ~30 dias). Nada é apagado em definitivo pelo script.

## 4. Registro dialético
- **TESE:** a pasta é majoritariamente acervo legítimo (geo + leis + jurisprudência + cadastro); o lixo é dup técnica + ruído, limpável por 2 scripts reversíveis.
- **ANTÍTESE:** a varredura por tempo cobriu a rajada de shapefiles, não 100% dos `.txt` antigos um a um — por isso a FASE 3/4 é **genérica em runtime** (pega o que existir quando você rodar), não uma lista fixa que poderia desatualizar.
- **VACINA:** nunca apagar " (N)" sem o original presente E mesmo tamanho (poderia ser versão diferente); nunca apagar shapefile/PDF/CSV de norma (não casam os padrões); dry-run obrigatório (AUD-02). O destrutivo é do MOU.
