# GeoSampa WFS — descoberta do endpoint e das camadas (2026-07-08)

> Como o Potencial Urbano puxa a **zona-base de uso sob o selo ZEPEC** (o CAbás que falta).
> Provado ao vivo pelo runner `brasil` (hub `portfolio-automacoes`, run #6 geosampa-siszon).
> Passa o Imperva; IP-BR `24.152.37.11`.

## O endpoint
GeoServer WFS via proxy do GeoSampa:
```
https://geosampa.prefeitura.sp.gov.br/PaginasPublicas/map.geo
  ?hc=<token-de-sessão>&tipoServico=DWFS1&service=wfs&version=1.0.0
  &request=GetCapabilities | DescribeFeatureType | GetFeature
  &typeName=geoportal:<camada>&outputFormat=json
```
- `hc` = token por sessão (aparece nas chamadas map.geo da página; capturar do 1º request).
- Só um navegador real (com cookie TSPD do Imperva) alcança — daí rodar no runner `brasil`.
- 400 FeatureTypes no catálogo. `capabilities.xml` fica no artefato `geosampa-probe`.

## Camadas que importam
| typeName | o que é | atributos-chave |
|---|---|---|
| `geoportal:perimetro_zoneamento_v3` | **zona de uso** (perímetros de zona, base) | `cd_zoneamento_perimetro` (ex "ZM-1"), `tx_zoneamento_perimetro`, `an_legislacao_zoneamento`, `ge_poligono` |
| `geoportal:perimetro_zona_lei_18177_24` | **zona de uso — Lei 18.177/2024** ("Mapa 1") | `cd_zoneamento_perimetro` (ex "ZEPAM"), `tx_zoneamento_perimetro`, `ge_poligono` |
| `geoportal:zoneamento_corredor_uso_v2` | corredores (ZC...z) | `cd_zoneamento_corredor` |
| `geoportal:lote_cidadao` | **lote fiscal** (busca por SQL) | `cd_setor_fiscal`, `cd_quadra_fiscal`, `cd_lote`, `cd_digito_sql`, `ge_poligono`, `nm_logradouro_completo` |

**A zona-base é uma dessas camadas de perímetro de zona** — elas NÃO trazem o selo ZEPEC por cima
(o selo é camada à parte). É exatamente o que faltava no nosso overlay (que só tinha o selo).

## Método (por imóvel)
1. `GetFeature lote_cidadao` filtrando por SQL (setor/quadra/lote) → `ge_poligono` → centroide (EPSG:31983).
2. `GetFeature perimetro_zoneamento_v3` (e/ou `_lei_18177_24`) com `CQL_FILTER=INTERSECTS(ge_poligono, POINT(x y))`
   → `cd_zoneamento_perimetro` = **zona-base**.
3. zona-base → CAbás via `tabelas/quadro3-ca-por-zona.csv` (quase toda básico=1; zonas centrais até 2).

## Gabarito de conferência (Termo 006/2026, SQL 0010800016, Sé/Centro)
PCpt 717,60 = Atc 299 × (CAbás×Fi) → **CAbás×Fi ≈ 2,40**. Encaixe provável: zona central **CAbás=2 × Fi=1,2**.
A zona-base real (v4) confirma se é básico 1 ou 2 — é o que fecha (ou não) o gabarito.

## Estado
- v1/v2: Imperva ok, app carrega, busca por SQL dispara. v3: catálogo WFS (este doc).
- v4 (a rodar): teste fim-a-fim do SQL de teste (lote→centroide→zona). v5: lote dos 377 → CAbás → gabarito.
- Runner/coleta vivem no hub `portfolio-automacoes` (D-DONO-19).
