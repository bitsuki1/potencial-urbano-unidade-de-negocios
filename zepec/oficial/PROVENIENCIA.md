# Proveniência — camada OFICIAL dos cedentes (Fase A, D-DONO-6)
> Recortes LEVES de fontes OFICIAIS para o produto TDC (dado pesado fica no Supabase Storage; recorte fica no git).
> Extraídos em 2026-07-02 pela instância PU 15 a partir dos arquivos subidos pelo MOU ao bucket `dados-produto/oficiais/`.

| Arquivo | Fonte oficial | O que é |
|---|---|---|
| `iptu2026_cedentes.csv` | `IPTU_2026.csv` (PMSP, 3.920.972 linhas, 894 MB no Storage) | Recorte dos cedentes ZEPEC (match por SQL 10 díg.): **área do terreno (Atc)**, área construída, valor venal do m², codlog, uso, padrão, endereço. 3.905 de 4.292 SQLs casados (91%). |
| `q14_cedentes_2025.csv` | `Atualizacao_Q14_anoref2025.csv` (Quadro 14, Anexo Lei 16.050/2014, atualização jan/2025; 179.586 faces no Storage) | Recorte das faces (SQ×Codlog) das quadras dos cedentes: **V = valor do m² de terreno para outorga**. 3.676 faces / 895 SQs. |

**Vacina (dois "V" homônimos):** `v_venal_m2` (IPTU, planta genérica) ≠ `valor_m2_brl` (Quadro 14, valor de outorga).
O engine TDC/OODC usa o **Quadro 14**; o venal é fato cadastral. Não intercambiar.

**Espelho no Supabase:** tabelas `oficiais.iptu2026_cedentes` e `oficiais.q14_valor_terreno_2025` (projeto `csnalylpvysjvejgsymr`), RLS deny-all, com campo `fonte`.
