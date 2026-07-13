# Tese TDC nº 01 — O potencial do imóvel tombado: natureza compensatória e a vedação do Art. 124 §2º

> **STATUS: PROPOSTA — aguarda escrutínio do MOU (D-13: uma tese de cada vez, escrutinada antes da próxima).**
> **Artefato (1.1):** camada ARGUMENTATIVA, construída *sobre* o corpus já limpo (1.2). Nenhum número nasce aqui —
> o valor vem do engine (`engines/tdc/art128.py`, 1.3); todo fato carrega dispositivo + fonte (1.7).

## Proveniência (de onde cada peça veio)
**Corpus (leis/):**
- PDE — Lei 16.050/2014: **Art. 122** (hipóteses de TDC), **Art. 124** (TDC de imóvel tombado) e seu **§2º** (vedação),
  **Art. 128** (valor de referência), **Art. 129** (conservação).
- Estatuto da Cidade — Lei federal 10.257/2001: **Art. 35** (base federal da TDC).
- Regulamento — Decreto 57.536/2016 (rito da TDC sem doação).

**Jurisprudência (jurisprudencia/):**
- **STF RE 387.047/SC** (Pleno, 2008) e **RE 226.942/SC** (1ª T., 2008): o "solo criado"/outorga é **ônus urbanístico, não tributo** — parcela do solo criado é **compensação**.
- **TJSP 2257458-20.2024** (5ª C. Dir. Privado): a TDC tem **natureza compensatória** (valores penhoráveis).
- **STJ AgRg no AREsp 179.340/SP** (2ª T., 2012): TDC do **art. 35 do Estatuto** em desapropriação de tombado.
- **TJSP 0000175-39.2017** (12ª C. Dir. Público, 2018): **vedação do Art. 124 §2º confirmada** (segurança denegada).
- **TJSP 0000177-09.2017**: **tombamento provisório equipara-se ao definitivo** para efeito da vedação.
- **TJSP 1070175-76.2019** (13ª C. Dir. Público, 2021): **direito de protocolo / ultratividade** (segurança concedida).

---

## TESE
O **potencial construtivo do imóvel tombado é transferível** (Art. 122 e 124 do PDE; art. 35 do Estatuto da Cidade),
e sua natureza é **compensatória, não tributária**: a restrição ao direito de construir imposta pelo tombamento é
**compensada** pela faculdade de exercer/alienar esse potencial em outro local. O STF, ao julgar o "solo criado"
(RE 387.047 e RE 226.942), fixou que o instrumento é **ônus urbanístico, não tributo** — logo não se lhe aplicam as
limitações tributárias, e o TJSP (2257458-20.2024) reconhece expressamente a **natureza compensatória** do crédito de
TDC. O **valor de referência** dessa compensação é o **piso legal do Art. 128** (calculado no engine, rastreável ao
dispositivo) — não é preço de mercado nem alavanca comercial: **a margem é do proprietário** (D-DONO-7/15).

## ANTÍTESE
A transferibilidade **não é absoluta**. O **Art. 124 §2º do PDE veda a TDC** em hipóteses determinadas, e essa vedação
foi **confirmada judicialmente** (TJSP 0000175-39.2017 — segurança denegada). Mais: o **tombamento provisório equipara-se
ao definitivo** para esse efeito (TJSP 0000177-09.2017), de modo que não se pode presumir liberado o potencial só porque
o tombamento ainda não foi "definitivo". Há ainda o risco **temporal**: regras de potencial mudam (revisões do PDE —
17.975/2023 — e novas leis), e uma Declaração emitida sob regra anterior pode ser questionada.

## VACINA (como blindar a operação)
1. **Testar a vedação ANTES (Art. 124 §2º).** É item de due-diligence obrigatório: enquadrar a hipótese do imóvel no
   §2º antes de precificar. O dossiê do produto já traz o checklist do Art. 129 (conservação) e do rito do Dec. 57.536/2016;
   **acrescentar a verificação explícita do Art. 124 §2º** fecha o flanco. (→ melhoria de produto proposta.)
2. **Protocolar cedo — direito de protocolo/ultratividade.** O TJSP (1070175-76.2019) protege a **Declaração já protocolada**
   contra mudança posterior de regra. A vacina temporal é **antecipar o protocolo da Declaração de Potencial Construtivo**:
   cristaliza a regra vigente na data (coerente com o princípio 1.6 — vigência na data do fato).
3. **Conservação (Art. 129).** Exigir o Atestado de Preservação e Conservação vigente — sem ele, a TDC do tombado trava.
4. **Ancorar no piso legal.** Por ser compensatória (STF/TJSP), a operação parte do **valor de referência do Art. 128**
   (engine) — número citável, não estimativa; blinda contra alegação de subavaliação ou de natureza tributária.

---

### Ganchos para o produto (não-normativos — propostas)
- **Dossiê:** incluir no checklist a linha "**Art. 124 §2º — hipótese de vedação da TDC verificada?**" (hoje ausente).
- **Engine:** nenhum número novo — a tese usa o Art. 128 já implementado. A precisão do §2º do Art. 128 (VTcd histórico da
  Declaração) permanece o resíduo declarado do produto (ver `ENTREGA-TDC.md`).

> _Próxima tese (só após seu escrutínio, D-13):_ candidata — "**Direito de protocolo e a vigência da Declaração**"
> (aprofunda a vacina temporal, sobre TJSP 1070175 + princípio 1.6).
