# Proveniência — camada OFICIAL dos cedentes (Fase A, D-DONO-6)
> Recortes LEVES de fontes OFICIAIS para o produto TDC (dado pesado fica no Supabase Storage; recorte fica no git).
> Extraídos em 2026-07-02 pela instância PU 15 a partir dos arquivos subidos pelo MOU ao bucket `dados-produto/oficiais/`.

| Arquivo | Fonte oficial | O que é |
|---|---|---|
| `iptu2026_cedentes.csv` | `IPTU_2026.csv` (PMSP, 3.920.972 linhas, 894 MB no Storage) | Recorte dos cedentes ZEPEC (match por SQL 10 díg.): **área do terreno (Atc)**, área construída, valor venal do m², codlog, uso, padrão, endereço. 3.905 de 4.292 SQLs casados (91%). |
| `q14_cedentes_2025.csv` | `Atualizacao_Q14_anoref2025.csv` (Quadro 14, Anexo Lei 16.050/2014, atualização jan/2025; 179.586 faces no Storage) | Recorte das faces (SQ×Codlog) das quadras dos cedentes: **V = valor do m² de terreno para outorga**. 3.676 faces / 895 SQs. |
| `zonas_v5_geosampa.csv` | GeoSampa/WFS, camada **`geoportal:perimetro_zona_lei_18177_24`** (zoneamento VIGENTE, Lei 18.177/2024), consultada por `INTERSECTS` no **centroide OFICIAL do lote** (`geoportal:lote_cidadao`, EPSG 31983) | Rodada **v5** dos 168 cedentes sem zona provada. Coleta de IP brasileiro pelo runner `brasil` do hub — workflow `pu-zona-v5`, **run 31235867658**, 2026-08-08 02:51Z (o GeoSampa fica atrás de bot-defense Imperva e só responde a navegador real com IP-BR). **151/157 pontos** com zona na camada vigente; **150/150 dos que tinham centroide oficial** resolveram. Colunas: `zona_18177` (vigente, a que vale) · `zona_v3` (camada ANTIGA 2004, só diagnóstico quando a vigente não responde) · `status` · `origem_ponto`. |

**Por que o centroide do lote e não o endereço (achado da rodada v5):** a rodada v4 partia do endereço geocodificado (Nominatim/OSM), cujo ponto cai no **eixo da via**. A camada vigente é de *polígono de zona* e não tem feição sobre a via — por isso 105 cedentes voltavam "só na camada antiga". Partindo do **centroide oficial do lote**, a taxa foi de 0% para **100%** (150/150). O mesmo ponto oficial derrubou 3 zonas erradas que a v4 lera a 20 km, 14 km e 1,8 km do lote.

**Vacina (dois "V" homônimos):** `v_venal_m2` (IPTU, planta genérica) ≠ `valor_m2_brl` (Quadro 14, valor de outorga).
O engine TDC/OODC usa o **Quadro 14**; o venal é fato cadastral. Não intercambiar.

**Espelho no Supabase:** tabelas `oficiais.iptu2026_cedentes` e `oficiais.q14_valor_terreno_2025` (projeto `csnalylpvysjvejgsymr`), RLS deny-all, com campo `fonte`.
