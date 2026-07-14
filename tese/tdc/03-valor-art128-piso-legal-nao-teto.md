# Tese TDC nº 03 — O valor do Art. 128 é piso/referência legal, não teto — e não é tributo

> **STATUS: ✅ AUTO-ESCRUTINADA (2026-07-14) — gate D-13 delegado pelo MOU. PROPOSTA aberta a revisão.**
> _Lentes adversariais: **(1) vigência** — Art. 128 conferido no verbatim atual; **(2) adversário** — a Procuradoria tentaria
> tratar o valor como TETO regulatório ou como base tributável, a antítese responde; **(3) sobre-extensão** — deixei explícito
> que o Art. 128 dá EQUIVALÊNCIA (PCr) e ancora o valor no VTcd do cadastro OODC, NÃO um "preço de mercado"; **(4) número
> (1.3)** — nenhum valor nasce nesta tese: tudo remete a `engines/tdc/art128.py`; **(5) D-DONO-7/15** — a margem é do dono._
> **Artefato (1.1):** camada ARGUMENTATIVA (1.2); citação obrigatória (1.7). É a tese que faz a ponte tese↔engine.

## Proveniência
**Corpus (leis/):**
- PDE — Lei 16.050/2014, **Art. 128** (verbatim, l.4978+): `PCr = (PCpt × VTcd) / (Cr × CAmaxcd)`; **§1º** (nos casos do
  Art. 125, adota-se **CAmaxcd = 4**); **§2º** (o **VTcd** — valor do terreno cedente pelo **Cadastro de Valor de Terreno para
  fins de Outorga Onerosa**, vigente na data de referência — é **corrigido por IPCA** até o mês anterior ao protocolo da CT);
  **Art. 125** (o PCpt transferível = `Atc × CAbás × Fi=1`).
- **Natureza do VTcd:** é o **valor do cadastro OODC** (dado regulatório, publicado), **não** avaliação de mercado. É âncora
  legal rastreável ao dispositivo.

**Jurisprudência (jurisprudencia/):**
- **STF RE 387.047/SC** e **RE 226.942/SC** (2008): o "solo criado"/outorga onerosa é **ônus urbanístico, não tributo**
  (aplicado à TDC por **analogia** — instrumento irmão no mesmo regime). ⚠️ Suporte por analogia, declarado.

## Engine (a fonte do número — 1.3)
`engines/tdc/art128.py` computa o valor de referência a partir do **VTcd vintage (Quadro 14)** + correção **IPCA §2º**, com a
regra **MAX(A;B)**; autotestes verdes; `eval-art128` OK. **Nenhum número desta tese é redigido à mão** — todos saem do engine,
rastreáveis ao Dec. 63.999/2024 e 64.884/2025 (cadeia do Quadro 14).

---

## TESE
O **valor de referência do Art. 128 é um PISO legal, rastreável, não um teto e não um tributo.** É *piso/referência* porque
nasce do **VTcd do cadastro OODC** corrigido por IPCA (§2º) — um **dado regulatório publicado**, não uma estimativa de
mercado; serve de **âncora mínima citável** para a operação. É **não-tributo** porque a TDC integra o regime do "solo criado",
que o **STF (RE 387.047/226.942, por analogia)** qualificou como **ônus urbanístico** — logo não se lhe aplicam as amarras da
base de cálculo tributária. E **não é teto**: a lei fixa a *equivalência* (quanto o receptor recebe) e a *referência de valor*,
mas **não tabela o preço** pelo qual o cedente aliena seu crédito — **a margem é do proprietário** (D-DONO-7/15). O produto,
por isso, entrega o número do Art. 128 como **piso citável + "a margem é sua"**, jamais como preço de mercado.

## ANTÍTESE
1. **A Procuradoria tentará usá-lo como TETO ou como base tributável.** Poderia sustentar que o valor do cadastro OODC "é o
   valor" (impedindo margem) ou que a operação gera tributo. **Resposta:** o Art. 128 §2º só define a **correção monetária** de
   uma **referência**; e o STF (analogia) afasta a natureza tributária. Não há dispositivo que fixe o valor de alienação.
2. **O suporte de "não-tributo" é analógico.** RE 387.047/226.942 são sobre **outorga onerosa**, não TDC direta. É analogia
   forte (mesmo regime do solo criado) mas não decisão direta — declarado.
3. **"Piso" pressupõe cadastro correto.** Se o VTcd do cadastro estiver defasado, o piso desanda. O engine mitiga com a cadeia
   vintage do Quadro 14, mas o **dado bruto** (Portaria SMUL) é entrada externa (resíduo declarado em `ENTREGA-TDC.md`).

## VACINA
1. **Sempre citar dispositivo + engine.** Todo valor no dossiê remete a Art. 128 (+ §1º/§2º) e à memória de cálculo do
   `art128.py` — nunca um número solto (1.7 + 1.3).
2. **Apresentar como PISO + margem do dono.** A moldura verbal do produto é "**piso legal do Art. 128 — a margem é sua**"
   (D-DONO-7/15): blinda contra alegação de subavaliação (há piso citável) e contra a leitura de teto (o preço é livre).
3. **Blindar a natureza não-tributária.** Ancorar no regime do solo criado (STF por analogia) sempre que a outra parte tentar
   puxar a operação para lógica de imposto.
4. **Rastrear o VTcd à Portaria.** Exibir a data-base do VTcd e o fator do Quadro 14 usados — se o cadastro estiver defasado, o
   dossiê o sinaliza, em vez de fingir precisão.

---

### Ganchos para o produto (não-normativos — propostas)
- **Dossiê:** rótulo padronizado "**Piso legal Art. 128 — a margem é sua (D-DONO-7/15)**" já em uso; manter e reforçar.
- **Dossiê:** expor a **data-base do VTcd** + o fator do Quadro 14 aplicado (transparência do piso).
- **Engine:** resíduo declarado — fiar `vtcd_na_data()` para o §2º histórico (sob o gate do MOU, toca número de 3.334 dossiês).
