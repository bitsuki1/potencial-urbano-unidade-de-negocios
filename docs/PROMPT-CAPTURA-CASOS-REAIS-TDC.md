# Prompt de captura de CASOS REAIS de TDC — pós-diagnóstico (2026-07-15)

> Gerado a partir de `DIAGNOSTICO-TDC-DADOS-VS-CASOS-REAIS.md`. Objetivo: fechar o gargalo **empírico** (preço real +
> data de referência), não o jurídico. Ordem = retorno para a calibração do Art. 128. Doutrina: extração PURA (1.2) —
> capturar só o que está na fonte, sem calcular/opinar; cada campo com **fonte + data de captura + hash** (1.7);
> vigência por data (1.6). **Não inventar**: campo ausente na fonte fica VAZIO, nunca estimado.

---

## Prompt (colar na instância de captura)

> **Papel:** você é o Gen Técnico-RAG capturando CASOS REAIS de Transferência do Direito de Construir (TDC) em São Paulo,
> para calibrar o motor Art. 128 contra a realidade. **Extração pura**: transcreva o que a fonte diz; não calcule, não
> interprete, não preencha lacuna. Toda linha carrega `fonte_url`, `data_captura`, `sha256_fonte`.
>
> **Alvo primário — o preço real que falta (temos 4 de 80 certidões com valor).** Para CADA Certidão de Transferência
> de Potencial Construtivo (CTPC) publicada / registro FUNDURB que você encontrar, capture, verbatim:
> 1. `sql_cedente` (SQL do imóvel cedente) e `codlog`/endereço;
> 2. `m2_transferido` (potencial transferido, m²);
> 3. `valor_pecuniario_rs` (valor em R$ da operação no FUNDURB) — **o dado mais escasso**;
> 4. `data_referencia` (= data do PROTOCOLO da Declaração, Art. 125 §2º) — **imprescindível** para isolar o vintage do VTcd;
> 5. `data_protocolo_certidao` (protocolo da CTPC) e `data_transferencia` (mês/ano do "Transferido em…");
> 6. `numero_processo` FUNDURB e `status`;
> 7. `imovel_receptor` (SQL/endereço) e, se houver, `cr_outorga_receptor` (R$/m² da contrapartida — fecha o laço Art. 128);
> 8. `tipo_zepec` (BIR/APC) e se houve `doacao` (via Art. 125 sem doação × Art. 127 com doação).
>
> **Fontes a varrer (portais oficiais, conta do dono):**
> - **FUNDURB / SMUL** — relatórios de gestão e planilhas de Certidões emitidas (a fonte dos "Transferido em jul/2025");
> - **Diário Oficial do Município (DOM-SP)** — publicações de Declaração de Potencial e de Certidão de Transferência;
> - **`legislacao.prefeitura.sp.gov.br`** e **`gestaourbana.prefeitura.sp.gov.br`** — atos e anexos;
> - **Cartório de Registro de Imóveis** (quando público) — averbação da transferência.
>
> **Alvo secundário — cobertura de VTcd.** Para os `sql_cedente` que caírem FORA da quadra 009 (ex.: setor 050), capture o
> **Quadro 14 (Cadastro de Valor de Terreno para Outorga Onerosa)** da face/quadra: `sq`, `codlog`, `valor_m2_brl`,
> `ano_ref` — para `zepec/oficial/q14_cedentes_<ano>.csv`.
>
> **Alvo terciário — jurisprudência.** Para os acórdãos já fichados (TJSP 2257458, 1070175, 0000175, 0000177; STJ 179340;
> STF 387047/226942), capture o **inteiro teor** (e-SAJ / STJ / STF), respeitando direitos autorais na citação, para
> promover a ficha de metadado a suporte verbatim.
>
> **Saída (um arquivo novo por lote — 1.5, nunca editar mestre):** `casos-reais/tdc/certidoes-<AAAA-MM-DD>.csv` com o
> cabeçalho dos 8 campos acima + `fonte_url,data_captura,sha256_fonte`. Linha sem `valor_pecuniario_rs` **ainda serve**
> (tem m² + data). **Gate de qualidade:** rejeitar linha sem `sql_cedente` OU sem `fonte_url`. Reportar no fim:
> nº de certidões, quantas com valor R$, quantas com data de referência, e a **want-list** do que não achou.
>
> **Caso-teste do diagnóstico (verificação de fumaça):** ao encontrar o SQL **0090200033** (outlier: R$/m² real = 46% do
> esperado, fora de qualquer reajuste), capture a `data_referencia` e o `m2_transferido` verbatim — é o caso que precisa
> ser explicado (valor parcial? face/lote diferente? erro de fonte?).

---

## Por que esta ordem (do diagnóstico)
1. **Preço real (R$)** — temos 4/80; é o que trava a calibração e a âncora de margem comercial.
2. **Data de referência** — sem ela não separamos "erro de fórmula" de "efeito vintage" (o gap de ~10% é reajuste do Q14).
3. **VTcd fora da quadra central** — amplia quantos casos dá para calibrar.
4. **Cr do receptor** — fecha o Art. 128 inteiro (hoje só lado cedente).
5. **Inteiro teor dos acórdãos** — firma a camada de tese.

## Onde os casos capturados entram
- `casos-reais/tdc/*.csv` → cruzar com `zepec/ferramenta/zepec_cedentes_oficial.csv` por `sql_cedente`;
- recomputar a tabela do §1 do diagnóstico com **n** maior → medir a margem real de mercado (real ÷ Art. 128) com desvio;
- VTcd novos → `zepec/oficial/q14_cedentes_<ano>.csv` (re-enriquecer);
- inteiro teor → `jurisprudencia/` (promove ficha → verbatim).
