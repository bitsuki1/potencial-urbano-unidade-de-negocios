# zepec/pipeline — os GERADORES do dado oficial (resgate do loop de melhoria, 2026-07-02)
> Achado EF-1/C-01 do `docs/LOOP-MELHORIA-H1-2026-07-02.md`: os scripts que geram `zepec/oficial/*`
> viviam SÓ no scratchpad efêmero da sessão. Resgatados para cá — o pipeline deixa de ser uma FOTO.

## A cadeia (na ordem)
| # | Script | Entrada | Saída |
|---|---|---|---|
| 1 | `subir-oficiais-para-supabase.gs` (App Script) + `subir-grandes-colab.py` (Colab) | Drive do dono | Supabase Storage `dados-produto/oficiais/` e `geo-shapefiles/oficial/` |
| 2 | `filtro_iptu.py` | stdin = IPTU_2026.csv (Storage) + `cedentes_sqls.txt` | `zepec/oficial/iptu2026_cedentes.csv` (uso: `curl -sS <url_iptu> \| python3 filtro_iptu.py`) |
| 3 | (recorte Q14 — lógica em `zepec/enriquecer_oficial.py`/sessão: filtra `Atualizacacao_Q14_anoref2025.csv` pelos SQs dos cedentes) | Q14 do Storage | `zepec/oficial/q14_cedentes_2025.csv` |
| 4 | `overlay_zona.py` | shapefiles LOTES+zonas (Storage, baixados p/ ./dl) | `zepec/oficial/zona_por_cedente.csv` |
| 5 | `zepec/enriquecer_oficial.py` | os 3 CSVs acima + `zepec/ferramenta/zepec_cedentes.csv` | `zepec/ferramenta/zepec_cedentes_oficial.csv` |
| 6 | `gerar_xlsx.py` | CSV final | Excel do produto |

## Contagens de regressão (2026-07-02, para provar re-execução fiel)
IPTU: 3.905 · Q14: 3.676 · zonas: 3.693 · PCpt: 3.014 · preço (saldo, s/ esgotado): 2.937.

## Dívidas conhecidas (do laudo)
- Paths de sessão ainda hardcoded em partes (parametrizar); resolver colunas do IPTU por NOME do header.
- Unificar canal de upload no runbook rclone (`scripts/transferir-pesados-drive-supabase.md`).
- requirements: shapely>=2.0, pyshp, openpyxl (pip install).
