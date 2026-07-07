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

## O gap de CAbás, dimensionado (2026-07-09)
`zepec/oficial/zona_por_cedente.csv`: **454 cedentes sem CAbás** — partem em DOIS caminhos independentes:
- **377 selo ZEPEC** (355 APC + 9 APP + 8 AUE + 5 BIR) → precisam da **zona-base sob o selo** (SISZON/GeoSampa = **VPS**, bloqueado no label). Alvo: `zepec/pipeline/alvos/siszon_zepec_sem_cabas.csv`.
- **77 ZOE** → regime próprio por **Quadro 2A** (macroárea) = **extração LOCAL, sem bloqueio**. Alvo: `zepec/pipeline/alvos/zoe_sem_cabas.csv`.
- O gabarito 006/2026 (Líbero Badaró) é ZEPEC_APC → está nos 377 (caminho VPS).

## ZOE destravado sem VPS (2026-07-09)
Extraí o **Quadro 2A** verbatim (`_entrada/tdc/pde2013-subst2-quadro-2a-ca-macroareas.txt`) → **`tabelas/quadro2a-ca-macroarea.csv`**.
Resultado: o **CA básico = 1** em TODAS as macroáreas com valor (exceto "Preservação de Ecossistemas" = NA e
"Contenção Urbana"-mananciais = 0,1). Logo, para os 77 ZOE, **CAbás = 1** — salvo se estiverem naquelas 2
macroáreas de exceção (verificação por macroárea, geo, é refinamento; o núcleo urbano dos ZOE não é preservação).
*Nada aplicado ao motor ainda (aguarda o "vai" da produção); a TABELA está pronta.*

## Estado
- [x] 1º gabarito registrado + **cruzado com o repo** → status BLOQUEADO_POR_CABAS_AUSENTE (caminho VPS).
- [x] Índice oficial de declarações localizado (407 linhas, sem m²) — worklist do OCR.
- [x] Gap de CAbás dimensionado (454 = 377 ZEPEC + 77 ZOE) + listas-alvo em `zepec/pipeline/alvos/`.
- [x] **ZOE: Quadro 2A extraído** → `tabelas/quadro2a-ca-macroarea.csv` (CAbás=1). *(item 3, sem bloqueio)*
- [ ] **377 ZEPEC:** rodar a Action `geosampa-siszon` no VPS (aguarda label `brasil`).
- [ ] **m² das declarações:** OCR (aguarda `GEMINI_API_KEY`) sobre a coleção do dono + índice.
- [ ] Fp/Quadro 6 (a outra tabela do D10) — verificar se há verbatim local; senão captura.
- [ ] Ligar o acervo ao gate de CI (tolerância ±5%).
