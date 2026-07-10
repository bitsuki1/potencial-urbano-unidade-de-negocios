# Achado — 25 gabaritos TDC coletados do Diário Oficial (2026-07-08)

Fonte: extensão do Claude no navegador do dono varreu o Diário Oficial da Cidade e baixou ~28
publicações (ARQUIP/DOSP); a extração está em `coletados/gabaritos-doc-extraidos.{csv,json}` e o
consolidado em `gabaritos-tdc-doc.csv`. **25/28 com m² transferível, 19 com SQL, 20 deferidos.**
Todos os cedentes são **ZEPEC-BIR**; a zona de USO sob o selo varia (ZC, ZM, ZEU, ZEM, ZPR, AC-1).

## O que isso PROVA (e muda a régua)
1. **O m² é DECLARADO, não calculado.** O cálculo Atc×CA **não aparece em nenhum** documento — o número
   sai da frase "dispõe de <m²> de potencial construtivo passível de transferência" (Declaração SMUL/DEUSO).
   → confirma a doutrina 1.3 (número nasce da fonte determinística, não do LLM) e o **regime JÁ_DECLARADO**
   do `enriquecer_oficial.py` (T3): quando existe Declaração, o PCpt É o declarado; o Atc×CAbás×Fi é só
   ESTIMADOR para prospecção NOVA.
2. **O multiplicador implícito (m²/área-terreno) varia caso a caso** — mesmo dentro de ZC: {1,0; 1,6; 2,0; 2,4; ...}.
   Não é função simples da zona. Há regra especial "renovação de 70% do saldo" (Art.129 §I, Lei 16.050/2014
   red. 17.975/2023) em ≥3 casos. Logo, reproduzir o declarado por fórmula única é impossível — por isso o
   gabarito trava o m² por DOCUMENTO, e o estimador é medido contra ele (não o contrário).
3. **Confirma o método GeoSampa:** a zona-base sob o selo ZEPEC-BIR é ZC/ZM/ZEU/ZEM — exatamente o que a
   consulta WFS (perimetro_zona_lei_18177_24) devolveu para os 377 (ex.: gabarito 0010800016 → ZC).

## Uso
- Estes 25 são o **conjunto de gabaritos fim-a-fim** (Camada 2). Cada linha com SQL vira caso de teste:
  o pipeline deve, para aquele SQL, casar a zona-base (Camada 1, GeoSampa) e — quando JÁ_DECLARADO —
  devolver o m² declarado; a divergência do estimador vira métrica, não erro.
- Próximo: cruzar os 19 SQLs com nossos 377 cedentes + a zona-base do WFS; medir estimador×declarado.

## Ressalva
Alguns `area_terreno_m2` capturados podem ser área de gleba/remanescente (ex.: id 148191953 terreno 35.011 → m² 67),
gerando multiplicador degenerado — conferência humana por caso antes de usar como âncora dura de fórmula.
