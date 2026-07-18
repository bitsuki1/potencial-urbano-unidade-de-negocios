# Quadro 14 × GeoSampa — descoberta (o valor de terreno NÃO está no GeoSampa) e roteamento dos 483 sem valor

> Status: **AVENIDA GEOSAMPA FECHADA para o Quadro 14** (descoberta concluída 2026-07-18).
> Sonda: `portfolio-automacoes/tools/geosampa/q14_probe.js` (runner `brasil`, IP-BR, bypass Imperva).
> Runs de prova (hub `portfolio-automacoes`, workflow `capturar-q14`):
> - passo-1 (dump lote + capabilities): run 29649716834 — sucesso.
> - passo-2 (esquema DescribeFeatureType das camadas reais): run 29650166095 — sucesso.
> Doutrina: 1.3/1.7 (valor rastreável ao dispositivo) e 1.8 (nada de derivado como fonte).

## O que se procurava
Preencher o **VTcd (V do Art. 128 — art128.py)** dos cedentes cujo SQL/codlog **não está** no nosso
extrato parcial do Quadro 14 (`tabelas/q14-valor-terreno.csv`, 6.716 SQLs). Hipótese: o GeoSampa
exporia o valor de terreno como camada WFS consultável por lote.

## O que a sonda achou (fatos, SQL de prova 001.080.0016-8 / R. Líbero Badaró 306)
1. **`lote_cidadao` NÃO tem campo de valor.** Props do lote trazem só geometria + cadastro físico
   (`qt_area_terreno=299`, `qt_area_construida=2082`, uso, logradouro). Nenhum `valor/venal/pgv`.
2. **Não existe camada `valor_terreno`/`pgv`/`quadro_14`/`valor_venal`.** Das 523 camadas WFS, as
   "candidatas" por nome são administrativas ou ruído (`selo_valor_cultural`, `centro_referencia_...`).
3. **Camadas reais checadas por esquema (DescribeFeatureType):**
   | Camada | Campos de valor? | Natureza |
   |---|---|---|
   | `geoportal:outorga_onerosa` | **`qt_valor_contrapartida`** (+ `cd_codlog`, `cd_setor_quadra`, `qt_area_terreno`, `qt_area_excedente`, `cd_coeficiente_*`, `cd_processo`, `cd_numero_alvara`) | **Transacional** — outorgas JÁ executadas, geom de PONTO. É o valor PAGO numa outorga concreta, não o cadastro de valor de terreno por SQL. |
   | `geoportal:zona_fiscal` | nenhum | geometria (ZF-1 etc.) |
   | `geoportal:quadra_fiscal_v2` / `_gsc` | nenhum | geometria da quadra fiscal |
   | `geoportal:setor_fiscal_gsc` | nenhum | geometria do setor fiscal |

**Conclusão:** o GeoSampa **não publica o Cadastro de Valor de Terreno (Quadro 14) por SQL**. A única
camada com valor é `outorga_onerosa`, que é **demanda executada** (quem pagou outorga, quanto, onde) —
não serve para o VTcd base do cedente.

## Roteamento (o que fazer com os 483 sem Quadro 14)
Cobertura atual do VTcd nos cedentes oficiais (`zepec/ferramenta/zepec_cedentes_oficial.csv`, 4.360):
- **3.877 com `v_outorga_m2_q14`** (Quadro 14) · **483 sem** · desses, **455 sem valor algum** (nem proxy IPTU).

Fonte primária correta para os 483 = **Portaria SMUL anual "Cadastro de Valor de Terreno para fins de
Outorga Onerosa"** (o anexo COMPLETO; a nossa `q14-valor-terreno.csv` é extrato parcial de 6.716 SQLs).
Caminho fechado (recomendação): obter o anexo completo da Portaria SMUL vigente (Drive do MOU ou
publicação oficial), extrair puro (1.2), casar por SQL/codlog e recompor o VTcd dos 483 — **nascendo do
primário** (1.3/1.8), nunca do proxy IPTU nem de derivado. Até lá, os 483 seguem marcados como PENDENTE
de valor (nunca chutados).

## Achado colateral (não é Quadro 14, mas vale ouro para o Comercial)
`geoportal:outorga_onerosa` é a **base de outorgas onerosas executadas** de São Paulo, com codlog,
área excedente, coeficientes e **valor de contrapartida pago**, capturável pela mesma sonda (IP-BR).
É o retrato da **DEMANDA real por potencial construtivo** — complementar aos compradores de TDC
(`LISTA-COMPRADORES-ENRIQUECIDA.csv`). Sugestão: dataset separado (Comercial & Marketing), fora do
corpus de leis (1.1 — é dado transacional, não norma).
