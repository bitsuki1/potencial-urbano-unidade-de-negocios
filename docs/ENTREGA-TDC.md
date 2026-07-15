# ENTREGA — TDC (Transferência do Direito de Construir) · Potencial Urbano

> Selo de entrega do domínio **TDC** (base inicial, decisão do MOU 2026-06-20). Consolida os quatro artefatos
> (norma · tabela · engine · tese) + o produto, com a PROVA de cada elo e os **resíduos declarados** (nada de "confie em mim").
> Gerado 2026-07-13. Cada número é rastreável ao dispositivo (1.3/1.7); toda norma carrega vigência (1.6).

## Veredito
**O TDC está ENTREGUE no que é a espinha dorsal do produto: corpus completo, engine fechado e provado, e o
produto (dossiê do cedente) em escala.** A camada de **tese** começou (1ª tese proposta, sob o ritmo D-13) e os
**resíduos** abaixo são melhorias de precisão/escopo — declarados, não escondidos.

## 1. Corpus normativo (artefato LEI) — ✅ completo
32 normas TDC‑relevantes indexadas com citação por dispositivo (verbatim de fonte oficial: portal SP + Planalto):
- **Fundamento:** Estatuto da Cidade (Lei federal 10.257/2001, art. 35 — base federal), **PDE Lei 16.050/2014**
  (arts. 122‑129 TDC; 117‑118 OODC), **LPUOS Lei 16.402/2016**, revisões 17.975/2023 e 18.081/2024.
- **Regulamentos da TDC:** Dec. 57.536/2016 (sem doação), 58.289/2018 (com doação), 58.176/2018; **Lei‑núcleo 17.844/2022**.
- **OODC:** regime geral **Dec. 63.504/2024** (a fórmula) + cadeia do **Quadro 14** (63.999/2024, 64.884/2025).
- **PIU/AIU Arco Pinheiros:** 18.222/2024, 18.298/2025 (vigência: Arts. 3‑5 suspensos por ADI 2007332‑76.2026).
- **Jurisprudência TDC:** 9 acórdãos (STF/STJ/TJSP) — natureza, vedação, protocolo.

## 2. Tabelas (artefato DADO) — ✅ 14 tabelas vintage
Quadro 2A (CA macroárea), Quadro 3 (CA/zona), Quadro 5 (Fs), Quadro 6/7 (Fp/parques), Fi‑doação, Fi‑ZEPEC (LPUOS
Art. 24), limiar‑parque (Art. 127), **q14‑reajuste‑anual** (2014→2026), q14‑valor‑terreno, IPCA (série IBGE, Art. 128 §2º).
Cada uma com `data_base` no METADATA (rastreada pelo consolidar; 0 sem data_base).

## 3. Engine (artefato FÓRMULA) — ✅ fechado e provado (lado cedente)
- **`pcpt.py`** — PCpt = Atc×CAbás×Fi (Art. 125) e via doação (Art. 124); FSCE (Art. 57, 17.844/2022).
- **`art128.py`** — valor de referência: VTcd vigente (vintage Q14) + §2º IPCA; MAX(A;B).
- **`oodc.py`** — outorga onerosa / contrapartida (Art. 117); `oodc_por_imovel`.
- **`fp.py`** — fator de planejamento.
- **Loop de auditoria FECHADO:** o incentivo de parque (R$ 2.194,50/2025 · R$ 2.352,06/2026) e o fator do Quadro 14
  (+4,5% · +7,18%) nascem no engine a partir da tabela, rastreáveis ao Dec. 63.999/2024 e 64.884/2025 (1.3).
- **Prova:** autotestes dos 4 motores verdes; `eval-art128` e `eval-art117` OK (verbatim).

## 4. Produto (assistente / parecer ao cliente) — ✅ em escala
- **`zepec/gerar_dossie.py`** — dossiê de 1 página por cedente: identificação, potencial (memória citada),
  **preço legal Art. 128** (piso regulatório — "a margem é sua", D‑DONO‑7/15), datas/vigência, checklist de
  due‑diligence (Dec. 57.536/2016), pendências. Cada número com o dispositivo de origem (1.7).
- **Escala:** **3.334 dossiês** de cedentes reais; `eval-produto` 15/15 e o autoteste do dossiê batem o Art. 128
  (sabotar 1 Fi da tabela FALHA o gate — não é circular).

## 5. Consulta RAG (artefato de entrega ao usuário) — ✅ robusta
- **`consultar.py`** — RAG híbrido com citação obrigatória; devolve o dispositivo verbatim + fonte + vigência.
- **Gate 1.7 = REGRA COMPOSTA** (`cobertura‑IDF ≥ 0,41 OU cobertura ≥ 0,55`) — robusta ao crescimento do corpus
  (aguentou +32 normas). **33/33 ground‑truth** verdes.

## 6. Tese (artefato ARGUMENTATIVO) — ✅ camada cedente-side completa (gate D‑13 delegado)
> **Gate D‑13 delegado pelo MOU (2026-07-14):** liberou a 1ª tese e autorizou o **auto-escrutínio** das seguintes em modo
> autônomo até o fim da camada. Roadmap + lentes de escrutínio em `tese/tdc/ROADMAP-TESES.md`.
- **01 ✅ APROVADA v3** — `01-tdc-tombado-natureza-e-vedacao.md`: natureza compensatória (STF por analogia/TJSP) × vedação do
  Art. 124 §2º (só AUE/APPa) + vacina; escrutínio intenso + 4 lentes aplicadas.
- **02 ✅** — `02-direito-de-protocolo-e-vigencia-da-declaracao.md`: data de referência = protocolo (Art. 125 §2º),
  ultratividade (TJSP 1070175), ressalva da retroatividade expressa (§3º), valor corrige por IPCA até a CT.
- **03 ✅** — `03-valor-art128-piso-legal-nao-teto.md`: o valor do Art. 128 é **piso/referência legal, não teto e não tributo**
  (STF por analogia; número do engine; a margem é do dono, D‑DONO‑7/15).
- **04 ✅** — `04-tdc-lei-municipal-art35-federal-e-moldura.md`: TDC é **lei municipal** (art. 35 §2º delega); foro = TJSP
  (STJ não reexamina lei local, Súmula 280 — AgRg AREsp 179.340).
- **05 ✅** — `05-conservacao-art129-condicao-e-alavanca-de-recarga.md`: conservação (Art. 129, pós‑17.975/2023) é condição
  **e** alavanca de **recarga** de potencial (70% aos 10 anos / 100% aos 15, não cumulativos).
- **Resíduo declarado (probatório):** as fichas de TJSP/STJ são **metadados** (resumo próprio), não inteiro teor — capturar a
  íntegra é gancho de produto. **Escopo:** todas cedente-side; o lado receptor fica fora até o gate do MOU.

## Resíduos declarados (o honesto "o que ainda melhora")
1. **Precisão do Art. 128 §2º (já‑declarados) — ✅ FIADO (gate do MOU dado 2026‑07‑15).** `gerar_dossie.py` agora aplica
   o **MAX(A piso vigente ; B VTcd da Declaração×IPCA)** nos já‑declarados **com Declaração E Certidão protocoladas**,
   reconstruindo o VTcd histórico por **`vtcd_na_data()`** (razão de reajuste uniforme do Quadro 14, 2026→ano‑ref). O
   dossiê mostra as duas bases lado a lado + a vencedora citada; o cedente fica com o **maior valor assegurado** (OP‑1b).
   **Fail‑closed (1.3):** sem Certidão protocolada (o §2º não cristalizou) ou Declaração pré‑2014 (fora da série IPCA),
   mantém a base A vigente com nota honesta — o motor **não inventa 'hoje'**. Prova: `gerar_dossie --autoteste` (3.334
   batem; 2 já‑declarados reais exercitam a base B + **fixture não‑vácuo determinístico**); `eval‑produto` 15/15. _Achado
   de brinde: o rótulo "Data de referência" do bloco 5 usava `data_ref` (agregado `max` de todas as origens); corrigido
   para `data_declaracao_iso` (protocolo da Declaração — a data legal do §2º)._ Cobertura real hoje: **2 de 615**
   já‑declarados têm Certidão datada na base; cresce quando o campo `data_certidao_iso` for preenchido em mais linhas.
2. **Lado RECEPTOR (comprador):** 2 leads mapeados (Fp=2 nas ZEM/ZEMP; +5% na regularização) — fora do produto do
   vendedor (o Cr do receptor cancela no Art. 128). Aplicar só se o produto passar a calcular o outro lado.
3. **Dado pesado:** valores nominais do Quadro 14 (Portaria SMUL) e plantas/mapas dos PIUs (GIS) — o motor os recebe
   como entrada; um produto "cliente‑final sem fricção" exigiria ingeri‑los.
4. **Completude de borda:** 4 decretos 57.5xx (só‑anexo, sem texto no portal) e Mata Atlântica (Lei federal 11.428,
   remissão da 18.298) não ingeridos — baixo valor para o núcleo TDC.
5. **Revisão fina:** 14 normas do lote entraram por scaffold (`revisado_por_humano=false`) — dispositivos/remissões a curar.

## Como o MOU audita
`python3 engines/tdc/{pcpt,art128,oodc,fp}.py --demo` · `python3 evals/eval-produto.py` · `python3 zepec/gerar_dossie.py --sql <SQL>`
· `python3 scripts/consultar.py --dominio tdc "<pergunta>"`. Tudo determinístico e citado.
