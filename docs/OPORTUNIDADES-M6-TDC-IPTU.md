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

### OP‑1a — ✅ FEITO (2026‑07‑11, autorizado pelo dono "sim, tudo oficial"): VTcd no ano‑ref 2026 (**+7,18%**)
- **Ganho aplicado:** +7,18% no VTcd de **todo** cedente → +7,18% no preço legal de referência de **todos** (o preço é linear no VTcd: `referência = PCpt × VTcd ÷ CAmaxcd`). Prova: cedente `0200670033` — R$ 647.122,77 → **R$ 693.586,15 (razão 1,0718)**.
- **Por que é "tudo oficial" (não aproximação):** o **Decreto 64.884/2025** (29/12/2025) DEFINE o valor 2026 como o do exercício anterior **× 1,0718, uniforme para todas as faces**. Como o ano‑ref 2025 já veio do arquivo **oficial** `Atualizacao_Q14_anoref2025` (via `recorte_q14.py`), `2026 = 2025_oficial × 1,0718` **reproduz** o Anexo I da Portaria SMUL 8/2026 face a face — é o próprio ato oficial (1.3).
- **Como foi feito:** gerador `zepec/pipeline/reajuste_q14_2026.py` (determinístico, citado) → `zepec/oficial/q14_cedentes_2026.csv` (3.676 faces); `enriquecer_oficial.py` passa a ler o ano‑ref 2026 (vigência 1.6; o arquivo 2025 fica para auditoria). Pipeline regenerado, **gate 32/32 verde** (nenhum eval quebrou — o eval‑art128 valida a equação, então o VTcd maior flui consistente).
- **Resíduo declarado (want‑list):** reconciliar centavo‑a‑centavo com o **Anexo I nominal da Portaria SMUL 8/2026** quando o arquivo estiver à mão (a multiplicação já bate ao centavo por construção; é conferência de fidelidade, não bloqueio).

### OP‑1c — 💡 novo lead do mesmo decreto: **Fp (parques) oficial 2026 = R$ 2.352,06/m²**
- O **Decreto 64.884/2025** também atualiza, para fins do **Art. 127** da Lei 16.050/2014, o **valor de referência do fator de incentivo à TDC na implantação de parques → R$ 2.352,06/m²**. Isso toca o **motor Fp** (`engines/tdc/fp.py`). **A conferir:** se o Fp em uso está nesse valor 2026; se não, é outra "condição melhor" (do lado do comprador/eixo). → registrado no want‑list.

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

- ✅ **CONFERIDO NA FONTE OFICIAL (2026‑07‑11) — e a pista NOSSO estava exagerada.** Detalhe em `docs/CONPRESP-01-2025-BENEDITO-CALIXTO.md`.
- **A norma:** **Res. SMC/CONPRESP nº 1, de 27/01/2025** ARQUIVOU a APT de **PARTE** da Mancha Heterogênea **Benedito Calixto (I)** (Anexo II da Res. 11/CONPRESP/2023), mas **MANTEVE** os elementos **1I, 2I, 4I, 10I, 11I** (e 1J, 3J). **Não é blanket.**
- **Na nossa lista:** os **26 cedentes** da quadra 013.036 são todos da Mancha "I". Como o arquivamento é **parcial**, alguns viraram **falso‑positivo** (APT arquivada) e outros **seguem válidos** (mantidos). **Confirmar na fonte evitou descartarmos os válidos** — essa é a condição melhor real (nem vender o inválido, nem jogar fora o válido).
- ✅ **SINALIZADO (não removido):** os 26 ganharam a pendência *"REVISAR TOMBAMENTO — CONPRESP Res. 01/2025 …"* no entregável (`enriquecer_oficial.py`, prefixo 013036 → 26/26 no `zepec_cedentes_oficial.csv`). **Remoção fica para depois do mapa** (você autorizou conferir+sinalizar; remover exige saber QUAIS).
- **O que falta p/ fechar (want‑list):** Anexo II da Res. 11/2023 (elemento‑ID → endereço) + lista de arquivamento da Res. 01/2025 → cruzar com nossos codlog/SQL → marcar cada um arquivado (remover) vs mantido (fica).

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

1. ~~**OP‑1a (+7,18%)**~~ → ✅ **FEITO** (autorizado "sim, tudo oficial", 2026‑07‑11): preço legal de todos os cedentes subiu +7,18% (Dec. 64.884/2025), gate verde.
2. **OP‑1b (tese §2º):** ✅ autorizado — em construção: tese do **VTcd máximo rastreável** (2014+IPCA vs. Quadro 14 vigente), com Lei 17.975/2023 oficial. → Gen Advogado.
3. **OP‑2 (26 falso‑positivos):** ✅ autorizado — conferindo contra a **Resolução CONPRESP 01/2025** oficial e sinalizando.

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
