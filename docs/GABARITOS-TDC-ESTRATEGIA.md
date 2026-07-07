# GABARITOS (ground-truth) do TDC — estratégia
> PU 18 · 2026-07-06. Liberado pelo dono (D-DONO-17a). Define COMO provamos que os motores acertam:
> testando o pipeline contra **respostas certas oficiais**. Sem gabarito, todo "já funciona" é prosa
> (o defeito nº1 que o escrutínio 2026-07-06 achou nos 5 motores).

## Por que existe
O Motor do Mapa e o das Fórmulas produzem números (zona, m², preço) que **hoje ninguém confere**.
Um gabarito é um punhado de imóveis onde **sabemos a resposta certa, da fonte oficial** — vira a folha
de respostas contra a qual o pipeline é testado a cada mudança (gate de CI). Analogia: conferir 5 contas
de uma calculadora nova na mão antes de confiar nas outras 6.000.

## Duas camadas de gabarito
| Camada | Testa | Fonte oficial | Como se obtém |
|---|---|---|---|
| **1 — Zona por SQL** | Motor do **Mapa** (lote→zona→CAbás) | **GeoSampa** (API pública/WFS; consulta de zona de uso por nº de contribuinte) | automatizável — referência oficial da Prefeitura; humano só faz spot-check |
| **2 — m² transferível** | **Fórmulas** + fim-a-fim (Mapa→Fórmulas) | **Termos de Compromisso (CONPRESP)** e **Declarações de Potencial Construtivo (SMUL/DEUSO)** | atos públicos (Diário Oficial da Cidade / resoluções CONPRESP) + coleção do dono |

## Tolerância (D-DONO-17a) — o que é "bateu"
Aceita quando **os dois**:
1. **Zona idêntica** à do GeoSampa (é categórica — tem que estar certa).
2. **m² dentro de ±5%** do valor do termo, **com o gap explicado pela data de protocolo** (o CAbás/valores
   mudam por data — a diferença é registrada, nunca escondida).

Zona errada, ou m² fora de ±5% sem explicação = **bug real, build vermelho**.

## Alvo do acervo
~**15–30 processos** cobrindo variedade de zonas (Centro, eixos, ZEPEC variadas). Cada um vira um fixture
em `evals/ground-truth/gabaritos/<id>.json` e uma linha do eval do produto.

## Fontes para colher mais (públicas)
- **Declaração de Potencial Construtivo Passível de Transferência** — serviço SMUL (prefeitura.sp.gov.br/web/licenciamento/w/servicos/343175).
- **Certidão de Transferência de Potencial Construtivo** — serviço SMUL (…/servicos/343176).
- **Resoluções e Termos do CONPRESP** — publicados no Diário Oficial da Cidade (ex.: Res. SMC/CONPRESP nº 16/2025 atualizou o Termo).
- **GeoSampa** — WFS `wfs.geosampa.prefeitura.sp.gov.br/geoserver/…`; download SHP/GPKG/GeoJSON; catálogo de metadados (GeoNetwork). *(Tarefa de preparação: fixar a camada exata de lote/zoneamento por SQL — o workspace `geoportal` tem viária; a de lote/SISZON está em outro endpoint.)*

## Achados da preparação (2026-07-09)
1. **O índice oficial JÁ está no repo:** `zepec/raw/lista_declaracoes_ZEPEC-BIR_agosto-2025.csv` — **~407 declarações** (colunas: N.processo · SQ · Lote · Endereço · Distrito · **N.Declaração** · Data · Ano · Situação · Status). **NÃO traz o m²** — é catálogo de QUAIS imóveis têm declaração, não dos valores. Logo o acervo de gabaritos = pegar o **m²** de uma amostra desses (dos documentos: coleção do dono + termos/declarações publicados). O termo 006/2026 confere no índice (decl. 0539/23, SQ 001080-0016-8, 2024).
2. **O gabarito já pegou o furo nº1 (ao vivo):** para o SQL do termo, nosso pipeline atribui **zona = `ZEPEC_APC`** (o SELO de preservação) com **CAbás VAZIO** (`zepec/oficial/zona_por_cedente.csv`). Sem CAbás, o motor **não reproduz** os 717,60 m². É o gap **GEO-2** do escrutínio, agora concreto. (Nosso Atc=299 m² → CAbás×Fi implícito ≈ 2,40.)
3. **O que o GeoSampa resolve, exatamente:** a consulta **SISZON por SQL** devolve a **ZONA-BASE de uso** (Lei 16.402) sob o selo — o **CAbás que falta**. É o valor concreto que precisamos e não temos. (Alternativa/complemento: **Quadro 2A** para ZOE/macroárea — ver D10.)
4. **Acesso:** `curl` alcança GeoSampa (app/WFS/download = 200); **navegador headless NÃO passa pelo proxy** (reset até em example.com). Então o pull da zona-base é **script curl** (WFS/portal) — follow-up focado — ou 30s do dono pela consulta web.

## Estado
- [x] 1º gabarito registrado + **cruzado com o repo** → `evals/ground-truth/gabaritos/termo-006-2026.json` (status: BLOQUEADO_POR_CABAS_AUSENTE).
- [x] Índice oficial de declarações localizado no repo (407 linhas, sem m²).
- [ ] **Resolver a zona-base sob o selo ZEPEC** (SISZON/Quadro 2A) → CAbás. *É o desbloqueio nº1 — vale mais que colher mais processos.*
- [ ] Colher o **m²** de ~15–29 declarações (coleção do dono + documentos publicados) → completar a Camada 2.
- [ ] Ligar o acervo ao gate de CI (build vermelho se o pipeline sair da tolerância).
