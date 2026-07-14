# Tese TDC nº 01 — O potencial do imóvel tombado: natureza compensatória e a vedação do Art. 124 §2º

> **STATUS: PROPOSTA v3 — após ESCRUTÍNIO INTENSO + 4 LENTES NOVAS (2026-07-14). Aguarda o gate final do MOU (D-13).**
> _v2 corrigiu o escopo do §2º (só AUE/APPa) e o STF-por-analogia. **v3 dobra três achados das lentes novas:**_
> _**(A) vigência estrita (1.6)** — a Lei 17.975/2023 NÃO tocou o eixo (inciso I, §2º, §3º intactos; só o inciso II ZEPAM e os §§4º-6º mudaram), então a espinha resiste à redação de HOJE; e o transferível é o potencial construtivo **BÁSICO** (Art. 125), não o máximo/bônus._
> _**(B) §3º retroage** — o próprio Art. 124 §3º alcança "declarações já emitidas anteriormente", contraexemplo à ultratividade: a vacina temporal foi nuançada._
> _**(C) "compensatória" é faca de dois gumes** — o mesmo precedente (2257458) que a reconhece MANTÉM PENHORA (o crédito é ativo penhorável do cedente); e essa ficha é metadado interlocutório (agravo, sem trânsito), declarado como resíduo probatório._
> **Artefato (1.1):** camada ARGUMENTATIVA, construída *sobre* o corpus já limpo (1.2). Nenhum número nasce aqui —
> o valor vem do engine (`engines/tdc/art128.py`, 1.3); todo fato carrega dispositivo + fonte (1.7).

## Proveniência (de onde cada peça veio)
**Corpus (leis/):**
- PDE — Lei 16.050/2014 (redação vigente conferida no verbatim, l.4790-4836): **Art. 122** (norma-quadro da TDC,
  remete ao art. 35 do Estatuto), **Art. 124** — quem PODE transferir sem doação: **inciso I** (ZEPEC-BIR e ZEPEC-APC,
  transferem o potencial construtivo **BÁSICO** "definido em razão de sua localização") e **inciso II** (ZEPAM, redação
  dada pela Lei 17.975/2023) — e os LIMITES: **§2º vedação de AUE/APPa** e **§3º parcelamento acima de 50.000 m²
  (alcança as declarações já emitidas)**; **Art. 125** (fórmula: `PCpt = Atc × CAbás × Fi=1` — confirma que o transferível
  é o BÁSICO), **Art. 128** (valor de referência), **Art. 129** (conservação, ZEPEC-BIR).
- **Nota de vigência (1.6):** a Lei 17.975/2023 alterou o inciso II (ZEPAM) e incluiu o inciso III (VETADO) e os §§4º-6º;
  **não tocou** o inciso I, o §2º nem o §3º — os dispositivos-eixo desta tese estão na redação atual.
- Estatuto da Cidade — Lei federal 10.257/2001: **Art. 35** (base federal da TDC).
- Regulamento — Decreto 57.536/2016 (rito da TDC sem doação).

**Jurisprudência (jurisprudencia/):**
- **STF RE 387.047/SC** (Pleno, 2008) e **RE 226.942/SC** (1ª T., 2008): o "solo criado"/**OUTORGA ONEROSA** é **ônus
  urbanístico, não tributo** — parcela do solo criado é **compensação**. _(Julgados sobre a outorga onerosa — instrumento
  IRMÃO da TDC no mesmo regime do solo criado; aplicados à TDC por ANALOGIA, não como decisão direta sobre TDC.)_
- **TJSP 2257458-20.2024** (5ª C. Dir. Privado): a TDC tem **natureza compensatória** — porém o julgado a fixa para
  **MANTER PENHORA** de valores (o crédito é ativo penhorável do cedente). ⚠️ **Resíduo probatório declarado:** a peça no
  corpus é **ficha/metadado** (inteiro teor a capturar) e é **agravo de instrumento** (interlocutório, sem trânsito em
  julgado) — suporte indiciário, não definitivo.
- **STJ AgRg no AREsp 179.340/SP** (2ª T., 2012): TDC do **art. 35 do Estatuto** em desapropriação de tombado.
- **TJSP 0000175-39.2017** (12ª C. Dir. Público, 2018): **vedação do Art. 124 §2º confirmada** (segurança denegada).
- **TJSP 0000177-09.2017**: **tombamento provisório equipara-se ao definitivo** para efeito da vedação.
- **TJSP 1070175-76.2019** (13ª C. Dir. Público, 2021): **direito de protocolo / ultratividade** (segurança concedida).

---

## TESE
O **potencial construtivo básico do imóvel tombado é, em regra, transferível** — o Art. 124, I, do PDE autoriza
expressamente o tombado enquadrado como **ZEPEC-BIR/APC** a transferir seu **potencial construtivo básico** ("definido em
razão de sua localização"; Art. 122 e 124, I; fórmula no Art. 125, `PCpt = Atc × CAbás × Fi=1`; art. 35 do Estatuto).
Note-se o escopo: é o **básico**, não o potencial máximo nem o bônus de outorga. Sua natureza é **compensatória, não
tributária**: a restrição ao direito de construir imposta pelo tombamento é **compensada** pela faculdade de exercer/alienar
esse potencial em outro local. Diretamente sobre a TDC, o **TJSP (2257458-20.2024) reconhece a natureza compensatória** do
crédito — observando que o fez para **manter penhora** (o crédito é ativo econômico do cedente; ver a antítese). Por
ANALOGIA, o STF, ao julgar o "solo criado"/outorga onerosa (RE 387.047 e RE 226.942) — instrumento irmão no mesmo regime —,
fixou que se trata de **ônus urbanístico, não tributo**, reforço de que não se lhe aplicam as limitações tributárias. O
**valor de referência** dessa compensação é o **piso legal do Art. 128** (calculado no engine, rastreável ao dispositivo) —
não é preço de mercado nem alavanca comercial: **a margem é do proprietário** (D-DONO-7/15).

## ANTÍTESE
A transferibilidade **não é absoluta** — há limites reais, de três ordens.
1. **Escopo (Art. 124 §2º), estreito mas real.** O §2º veda a TDC **apenas** de potencial "originário de **bairros tombados
   em Área de Urbanização Especial (AUE)** e das **Áreas de Proteção Paisagística (APPa)**" (verbatim) — **não** dos tombados
   em geral: o ZEPEC-BIR/APC (inciso I), cedente típico, **não** é alcançado. Confirmado judicialmente (**TJSP 0000175-39.2017**,
   segurança denegada); e o **tombamento provisório equipara-se ao definitivo** para esse efeito (**TJSP 0000177-09.2017**, c/c
   art. 10, parágrafo único, do Decreto-lei 25/1937) — não se presume liberado o potencial só porque o tombamento não é ainda
   "definitivo".
2. **Quantidade (§3º) e retroatividade expressa.** O que exceder **50.000 m²** transfere-se em **10 parcelas anuais** — e o
   §3º alcança, na letra, "**as declarações já emitidas anteriormente à publicação desta lei**". Ou seja: **a própria norma
   mostra que o legislador PODE atingir declaração já emitida** — o que relativiza a ideia de que protocolar cristaliza tudo
   (ver vacina 2).
3. **Risco temporal, calibrado.** O Art. 124 foi revisto pela Lei 17.975/2023 — mas a lente de vigência (1.6) mostra que a
   revisão **não tocou** o inciso I, o §2º nem o §3º (só o inciso II ZEPAM e os §§4º-6º). Logo o risco temporal **existe** (o
   §3º é a prova de que retroatividade expressa acontece), mas **não recai** sobre os dispositivos-eixo desta tese — é um risco
   a monitorar, não uma nulidade atual.

## VACINA (como blindar a operação)
1. **Testar a vedação ANTES (Art. 124 §2º) — mas sabendo o alvo certo.** Due-diligence obrigatória e **objetiva**: o
   imóvel é **bairro tombado em AUE** ou **APPa**? Só nesses dois casos a TDC é vedada. Para o ZEPEC-BIR/APC (a esmagadora
   maioria dos cedentes) a transferência é **permitida** — a verificação serve para **descartar o falso-positivo**, não
   para presumir vedação. Acrescentar ao checklist do dossiê a linha "**imóvel em AUE/APPa? (Art. 124 §2º)**" fecha o flanco.
2. **Protocolar cedo — ultratividade, com a ressalva do §3º.** O TJSP (1070175-76.2019) protege a **Declaração já
   protocolada** contra mudança *posterior e tácita* de regra (cristaliza a regra vigente na data — coerente com o princípio
   1.6). **Ressalva honesta:** essa proteção **cede quando a lei retroage de forma EXPRESSA** — o próprio Art. 124 §3º é o
   exemplo (parcelou até declarações já emitidas). Então a vacina temporal reduz o risco de mudança tácita, **não** imuniza
   contra retroatividade que a lei declare expressamente. Protocolar cedo continua valendo — é a melhor defesa disponível —
   mas vende-se como *redução de risco*, não como blindagem absoluta.
3. **Conservação (Art. 129).** Exigir o Atestado de Preservação e Conservação vigente — sem ele, a TDC do tombado trava.
4. **Ancorar no piso legal.** Por ser compensatória (STF por analogia/TJSP), a operação parte do **valor de referência do
   Art. 128** (engine) — número citável, não estimativa; blinda contra alegação de subavaliação ou de natureza tributária.
5. **Checar constrição sobre o crédito (o duplo-gume da "compensatória").** Como o **2257458** admite **penhora** do crédito
   de TDC (é ativo do cedente), a due-diligence do negócio deve verificar se o crédito está **livre de penhora/constrição**
   antes da cessão — a mesma natureza que favorece o cedente o **expõe aos credores dele**.

---

### Ganchos para o produto (não-normativos — propostas)
- **Dossiê:** incluir no checklist a linha "**Art. 124 §2º — hipótese de vedação da TDC verificada?**" (hoje ausente).
- **Dossiê:** incluir a linha "**crédito de TDC livre de penhora/constrição? (TJSP 2257458)**" — due-diligence do duplo-gume.
- **Corpus:** capturar o **inteiro teor** do 2257458 (hoje só ficha/metadado) para promover o suporte de indiciário a firme.
- **Engine:** nenhum número novo — a tese usa o Art. 128 já implementado. A precisão do §2º do Art. 128 (VTcd histórico da
  Declaração) permanece o resíduo declarado do produto (ver `ENTREGA-TDC.md`).

> _Próxima tese (só após seu escrutínio, D-13):_ candidata — "**Direito de protocolo e a vigência da Declaração**"
> (aprofunda a vacina temporal 2, agora com a ressalva da retroatividade expressa do §3º, sobre TJSP 1070175 + princípio 1.6).
