# Tese TDC nº 01 — O potencial do imóvel tombado: natureza compensatória e a vedação do Art. 124 §2º

> **STATUS: PROPOSTA revisada após ESCRUTÍNIO INTENSO (2026-07-14) — aguarda o gate final do MOU (D-13).**
> _Escrutínio verificou cada citação contra o verbatim do corpus. Correções aplicadas: (1) o §2º veda SÓ AUE/APPa —
> a antítese não mais superdimensiona a vedação (ZEPEC-BIR/APC é permitido); (2) STF 387.047/226.942 são sobre outorga
> onerosa, aplicados à TDC por analogia (o suporte direto é o TJSP 2257458); (3) Art. 122 = norma-quadro; (4) incluídos
> o §3º (parcelamento) e a revisão do Art. 124 pela Lei 17.975/2023. Íntegros: Art. 129 e os 3 acórdãos do eixo._
> **Artefato (1.1):** camada ARGUMENTATIVA, construída *sobre* o corpus já limpo (1.2). Nenhum número nasce aqui —
> o valor vem do engine (`engines/tdc/art128.py`, 1.3); todo fato carrega dispositivo + fonte (1.7).

## Proveniência (de onde cada peça veio)
**Corpus (leis/):**
- PDE — Lei 16.050/2014: **Art. 122** (norma-quadro da TDC no PDE, remete ao art. 35 do Estatuto), **Art. 124** (quem
  PODE transferir sem doação — incisos I ZEPEC-BIR/APC e II ZEPAM — e os LIMITES: **§2º vedação de AUE/APPa** e **§3º
  parcelamento acima de 50.000 m²**), **Art. 128** (valor de referência), **Art. 129** (conservação, ZEPEC-BIR).
- Estatuto da Cidade — Lei federal 10.257/2001: **Art. 35** (base federal da TDC).
- Regulamento — Decreto 57.536/2016 (rito da TDC sem doação).

**Jurisprudência (jurisprudencia/):**
- **STF RE 387.047/SC** (Pleno, 2008) e **RE 226.942/SC** (1ª T., 2008): o "solo criado"/**OUTORGA ONEROSA** é **ônus
  urbanístico, não tributo** — parcela do solo criado é **compensação**. _(Julgados sobre a outorga onerosa — instrumento
  IRMÃO da TDC no mesmo regime do solo criado; aplicados à TDC por ANALOGIA, não como decisão direta sobre TDC.)_
- **TJSP 2257458-20.2024** (5ª C. Dir. Privado): a TDC tem **natureza compensatória** (valores penhoráveis).
- **STJ AgRg no AREsp 179.340/SP** (2ª T., 2012): TDC do **art. 35 do Estatuto** em desapropriação de tombado.
- **TJSP 0000175-39.2017** (12ª C. Dir. Público, 2018): **vedação do Art. 124 §2º confirmada** (segurança denegada).
- **TJSP 0000177-09.2017**: **tombamento provisório equipara-se ao definitivo** para efeito da vedação.
- **TJSP 1070175-76.2019** (13ª C. Dir. Público, 2021): **direito de protocolo / ultratividade** (segurança concedida).

---

## TESE
O **potencial construtivo do imóvel tombado é, em regra, transferível** — o Art. 124, I, do PDE autoriza expressamente o
tombado enquadrado como **ZEPEC-BIR/APC** a transferir seu potencial (Art. 122 e 124; art. 35 do Estatuto da Cidade). Sua
natureza é **compensatória, não tributária**: a restrição ao direito de construir imposta pelo tombamento é **compensada**
pela faculdade de exercer/alienar esse potencial em outro local. Diretamente sobre a TDC, o **TJSP (2257458-20.2024)
reconhece a natureza compensatória** do crédito (admitindo, inclusive, sua penhora). Por ANALOGIA, o STF, ao julgar o
"solo criado"/outorga onerosa (RE 387.047 e RE 226.942) — instrumento irmão no mesmo regime —, fixou que se trata de **ônus
urbanístico, não tributo**, reforço de que não se lhe aplicam as limitações tributárias. O **valor de referência** dessa
compensação é o **piso legal do Art. 128** (calculado no engine, rastreável ao dispositivo) — não é preço de mercado nem
alavanca comercial: **a margem é do proprietário** (D-DONO-7/15).

## ANTÍTESE
A transferibilidade **não é absoluta** — há um limite **de escopo estreito, mas real**. O **Art. 124 §2º do PDE veda a TDC
apenas** de potencial "originário de **bairros tombados em Área de Urbanização Especial (AUE)** e das **Áreas de Proteção
Paisagística (APPa)**" (verbatim) — **não** dos tombados em geral: o ZEPEC-BIR/APC (inciso I), cedente típico, **não** é
alcançado pela vedação. Essa vedação **estreita** foi confirmada judicialmente (**TJSP 0000175-39.2017** — segurança
denegada em caso de área tombada alcançada pelo §2º); e o **tombamento provisório equipara-se ao definitivo** para esse
efeito (**TJSP 0000177-09.2017**, c/c art. 10, parágrafo único, do Decreto-lei 25/1937), de modo que não se pode presumir
liberado o potencial só porque o tombamento ainda não é "definitivo". Somam-se dois outros limites: o **§3º** (o que
exceder **50.000 m²** transfere-se em **10 parcelas anuais** — já modelado no engine) e o **risco temporal**: o próprio
Art. 124 foi **revisto pela Lei 17.975/2023** (novos incisos e §§4º-6º), e uma Declaração emitida sob regra anterior pode
ser questionada.

## VACINA (como blindar a operação)
1. **Testar a vedação ANTES (Art. 124 §2º) — mas sabendo o alvo certo.** Due-diligence obrigatória e **objetiva**: o
   imóvel é **bairro tombado em AUE** ou **APPa**? Só nesses dois casos a TDC é vedada. Para o ZEPEC-BIR/APC (a esmagadora
   maioria dos cedentes) a transferência é **permitida** — a verificação serve para **descartar o falso-positivo**, não
   para presumir vedação. O dossiê já traz o checklist do Art. 129 e do rito do Dec. 57.536/2016; **acrescentar a linha
   "imóvel em AUE/APPa? (Art. 124 §2º)"** fecha o flanco sem assustar o cedente elegível. (→ melhoria de produto proposta.)
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
