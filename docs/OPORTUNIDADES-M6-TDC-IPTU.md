# OPORTUNIDADES — Garimpo M6 (melhores condições no TDC e no IPTU)

> **Missão (dono, 2026-07-11):** _"existem inúmeras oportunidades de conseguirmos melhores condições no TDC e no IPTU, através do estudo desses documentos que você dispensou. Vamos começar."_
> Este é o **relatório de oportunidades** do garimpo M6 — a saída viva do estudo dos documentos do Drive com a **lente de oportunidade** (não é faxina; é caça a condição melhor para o vendedor/cedente).
>
> **Regra de método (doutrina 1.2/1.3/1.7 — inegociável):** _achado ≠ tese ≠ preço._ Nada aqui **precifica** nem **argumenta** antes de bater na **lei oficial** com citação de dispositivo. Documentos **NOSSO** (Auditoria TDC V9.0, Memorial Estratégico, etc.) são **pistas** — valiosas para saber ONDE cavar — mas **não são fonte citável**: viram condição melhor só depois de confirmados contra a norma. Cada oportunidade abaixo traz **status** (confirmado · a-conferir · tese) e **de quem é a decisão**.

---

## OP‑1 ★ CARRO‑CHEFE — VTcd (valor do terreno) está uma safra atrasado, e o §2º do Art. 128 abre uma tese grande

**O que é, em dinheiro:** o preço legal do TDC (Art. 128 do PDE) é, no essencial, `PCpt × VTcd ÷ CAmaxcd`. O **VTcd** é o valor do m² do terreno do cedente, tirado do **Quadro 14** (Cadastro de Valor de Terreno para Outorga Onerosa). Se o VTcd que usamos está **defasado**, todo preço que entregamos ao vendedor sai **abaixo** do que a lei já permite. Achei duas alavancas aqui — uma limpa e imediata, outra jurídica e maior.

### Cadeia de fatos (CONFIRMADA no nosso código + na norma oficial)
- **O preço em produção usa o Quadro 14 ano‑ref 2025.** `zepec/lista_prospeccao.py` e `zepec/gerar_dossie.py` leem a coluna `v_outorga_m2_q14` da base enriquecida; `zepec/enriquecer_oficial.py` (linha 178) a preenche a partir de `zepec/oficial/q14_cedentes_2025.csv` — o snapshot **"Quadro 14 jan/2025"**. _(A tabela `tabelas/q14-valor-terreno.csv`, essa sim de base 2014, só alimenta o demo/eval do engine — não o preço ao cliente.)_
- **O ano‑ref 2025 já embute o reajuste de +4,5%** do **Decreto 63.999/2024** (30/12/2024), aplicado **uniformemente a todas as faces de quadra**, formalizado pela **Portaria SMUL 8/2025** (Anexo I, 3.097 páginas), sobre o Quadro 14 anexo à **Lei 16.050/2014, alterada pela Lei 17.975/2023**.
- **Já existe uma safra mais nova que NÃO estamos aplicando:** **Decreto 64.884/2025 + Portaria SMUL 8/2026** reajustaram o Quadro 14 em **+7,18%** para o exercício **2026**.
- **O engine já sabe corrigir por IPCA (Art. 128 §2º),** mas na prospecção ele **não** aplica: `corrigir_vtcd_ipca(..., ipca_fator=None)` devolve "sem correção — prospecção sem data de referência protocolada; usa o Quadro 14 vigente; §2º N/A até haver Declaração protocolada". O fator IPCA **jan/2014 → jun/2026** (série IBGE/SIDRA 1737 já versionada em `tabelas/ipca-numero-indice-ibge.csv`) é **1,9330 (+93,3%)**.

### OP‑1a — LIMPA e imediata: atualizar o VTcd para o ano‑ref 2026 (**+7,18%**)
- **Ganho:** +7,18% no VTcd de **todo** cedente → +7,18% no preço legal de referência. Direto, rastreável ao **Decreto 64.884/2025**, dentro da doutrina 1.6 (preço na vigência do fato gerador: uma avaliação de 2026 deve usar o Quadro 14 de 2026).
- **O que falta (bloqueio de dado, não de lei):** o arquivo oficial **`Atualizacao_Q14_anoref2026.csv`** (mesma fonte SMUL/Storage que gerou o de 2025, via `zepec/pipeline/recorte_q14.py`). É a entrada **exata** — preferível a aplicar o índice "no braço".
- **Por que NÃO apliquei já nesta passada (honestidade):** (1) muda o **número que vai ao cliente** em todo dossiê — isso merece seus olhos e o **arquivo exato**, não uma aproximação por fator; (2) doutrina 1.3 pede o dado rastreável na origem, não um ×1,0718 estimado. **Está pronto para executar** assim que o arquivo 2026 chegar (ou com seu aval para aplicar o índice citado como interino). → **want‑list registrado.**

### OP‑1b — TESE (potencialmente MAIOR): qual base de VTcd maximiza o preço do vendedor
- Na prospecção o engine usa o **Quadro 14 vigente** e trata o **§2º (IPCA) como N/A** até haver Declaração protocolada. Uma vez protocolada, o §2º corrige o VTcd por IPCA **da data‑ref da Declaração** até o mês anterior ao protocolo.
- **A tese:** existem **duas** leituras da base do VTcd, e o vendedor tem interesse na **maior**:
  - (i) **Quadro 14 vigente** (valores SMUL 2025/2026 — reavaliação de mercado via Lei 17.975/2023 + decretos); ou
  - (ii) **anexo original de 2014 + correção IPCA do §2º** (fator até **+93,3%**).
  - Qual é maior é **empírico, por SQL**. O engine deveria carregar **as duas** e a referência ser o **MÁXIMO rastreável** (cada um citado ao seu dispositivo).
- **Camada:** Gen Advogado (tese/antítese/vacina) sobre Art. 128 caput + §1º + §2º. **Precisa:** texto da **Lei 17.975/2023** (o que ela mudou no Quadro 14) + a leitura do §2º. → want‑list.

**Decisão do dono:** ① aval para **refletir o +7,18%** no preço (ou você traz o arquivo ano‑ref 2026); ② abrir a **tese do §2º** (VTcd máximo rastreável). Nenhum dos dois mexe em PII ou muda escopo — são o **preço LEGAL** (Tec & Dados), exatamente o que você pediu ("melhores condições").

---

## OP‑2 — 26 cedentes candidatos a **falso‑positivo** (imóveis que o CONPRESP arquivou)

- **Pista (Auditoria V9.0, NOSSO):** a **Resolução CONPRESP 01/2025** arquivou processos de tombamento de uma leva de imóveis — entre eles a quadra **013.036 (Praça Benedito Calixto)**. Imóvel com tombamento arquivado **não gera TDC por aquele fundamento** → é falso‑positivo na nossa lista de cedentes.
- **Confirmado por nós (grep na lista):** **26 de 4.360** cedentes estão na quadra 013.036; **0** em 013.046/013.055.
- **Oportunidade = melhores condições por subtração:** tirar falso‑positivo **não queima** prospecção em imóvel inelegível e **eleva a confiança** da lista (o vendedor certo, não o impossível).
- **Status:** **a‑conferir** — falta bater os 26 contra o **PDF da Resolução 01/2025** (Drive id `12UzO_2amXtVKmMm1gX_X82nLywiqWj0N`) e ver também a **Res. 03/2025**. A **conferência é read‑only** (posso fazer sob o mandato); a **remoção da lista** é decisão do dono (mexe no entregável).
- **Decisão do dono:** aval para **conferir + sinalizar** (não remover) agora; remoção depois da sua palavra.

---

## OP‑3 a OP‑6 — leads a aprofundar (registrados, ainda pista)

| # | Lead (fonte NOSSO/oficial) | Por que é "melhor condição" | Próximo passo | Status |
|---|---|---|---|---|
| **OP‑3** | **FUNDURB — latência de liquidez** (V9.0: backlog ~R$ 42,19 mi, ~4,4 meses de fila). | Timing de protocolo/opção de estoque muda o preço realizável; argumento de janela. | Confrontar Art. 24 §5º LPUOS (teto 5% FUNDURB) + dados de estoque. | lead |
| **OP‑4** | **"Testadas de papel" (CTLU)** — testada fictícia infla/desinfla VTcd por face. | Corrigir a testada usada muda o VTcd da face → preço mais fiel. | Método CTLU + Regra da Esquina (Dec. 57.536/2016 Art. 3º IV — maior valor da quadra). | lead |
| **OP‑5** | **Arco Pinheiros / AIU‑ACP super‑tier** (Lei 18.222/2024). | Faixa de outorga/coeficiente distinta pode elevar o potencial em recorte específico. | Ler Lei 18.222/2024; cruzar com cedentes no recorte. | lead |
| **OP‑6** | **Portão fiscal CADIN/CND** — regularidade fiscal como gate do protocolo. | Antecipar a exigência evita perder janela/opção; condição de negócio melhor. | Mapear exigência no rito de TDC/OODC. | lead |

_(OP‑3..6 vêm de documento NOSSO — são direção de garimpo, não fonte citável. Viram tese/preço só após bater na norma.)_

---

## O que depende do dono (fechado — recomendação, você decide o COMO)

1. **OP‑1a (+7,18%):** trazer `Atualizacao_Q14_anoref2026.csv` **ou** autorizar aplicar o índice **+7,18%** (Dec. 64.884/2025) citado como interino. → sobe o preço legal de todos.
2. **OP‑1b (tese §2º):** abrir a tese do **VTcd máximo rastreável** (2014+IPCA vs. Quadro 14 vigente). → Gen Advogado.
3. **OP‑2 (26 falso‑positivos):** aval para **conferir + sinalizar** já; **remover** só com sua palavra.

## Want‑list gerado (registrado em `docs/INVENTARIO-E-LACUNAS-IPTU-TDC.md`)
- `Atualizacao_Q14_anoref2026.csv` (Quadro 14 exercício 2026 — Dec. 64.884/2025 / Portaria SMUL 8/2026).
- **Lei 17.975/2023** (o que alterou no Quadro 14 da Lei 16.050/2014) — base da tese OP‑1b.
- **Resolução CONPRESP 01/2025 e 03/2025** — lista de SQLs arquivados (OP‑2), Anexo com os processos.
- **Anexo I da Portaria SMUL 8/2025** (Doc. 117650623, 3.097 pág.) — valores nominais R$/m² por face, se o recorte exato for necessário.

## Fontes oficiais consultadas
- Portaria SMUL 8/2025 — <https://legislacao.prefeitura.sp.gov.br/portaria-secretaria-municipal-de-urbanismo-e-licenciamento-smul-8-de-30-de-janeiro-de-2025>
- Decreto 63.999/2024 (atualiza Quadro 14, +4,5%) — Catálogo de Legislação Municipal SP / SINESP.
- Prefeitura/SMUL — atualização dos valores de terreno p/ Outorga Onerosa (exercício 2026, +7,18%; Dec. 64.884/2025 + Portaria SMUL 8/2026).
- IPCA nº‑índice IBGE/SIDRA tabela 1737 (jan/2014→jun/2026) — já em `tabelas/ipca-numero-indice-ibge.csv`.

---
> _M6 · garimpo de oportunidade · PU 18 · 2026‑07‑11. Vivo: novas oportunidades entram aqui conforme o estudo avança (Task #24 TDC / #26 IPTU)._
