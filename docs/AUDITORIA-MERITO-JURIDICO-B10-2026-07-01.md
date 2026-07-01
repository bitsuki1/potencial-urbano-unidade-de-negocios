# AUDITORIA DE MÉRITO JURÍDICO — B-10 (Potencial Urbano)

> **Lente:** Gen Advogado (subagente) · **Orquestração + verificação adversarial:** PU 15 · **2026-07-01**
> **Backlog:** B-10 (auditar o MÉRITO JURÍDICO das teses — ponto cego DECLARADO da auditoria profunda:
> só proveniência/fidelidade fora auditada, não o conteúdo jurídico).
> **Doutrina:** 1.7 citação obrigatória · 1.2 só o que está no documento · agnosticismo · dialético · nada se descarta.
>
> **★ VERIFICAÇÃO ADVERSARIAL (D-12, lente DIFERENTE) — CONFIRMADA pelo orquestrador (2026-07-01):**
> as três afirmações mais consequentes foram checadas mecanicamente contra o corpus, não aceitas no fiado:
> - **"0/32 juris tratam de TDC"** → `grep -rilE "transferência do direito de construir|outorga onerosa|potencial construtivo|solo criado" jurisprudencia` = **0 arquivos**. **CONFIRMADO.**
> - **stj-tema-262 / stj-tema-399 são stubs não-verificados** → ambos `.md` auto-declaram "Não foi possível confirmar / provável confusão". **CONFIRMADO.**
> - **stj-resp-1112646 ≡ stj-tema-174 (mesmo REsp)** → ambos referenciam o REsp 1.112.646. **CONFIRMADO** (par redundante intencional).
>
> O laudo abaixo é o retorno íntegro da lente Gen Advogado (zero-compressão). As **vacinas** dialéticas
> deste laudo ficam gravadas para o Gen Advogado de produção (tese/antítese/vacina por bloco temático).

---

## ACHADO ESTRUTURAL PRÉVIO — o corpus é TDC-cego

**Decisão do MOU (2026-06-20):** base inicial = **TDC**. **Constatação de mérito:** das 32 jurisprudências,
**0 (zero)** tratam de TDC (Transferência do Direito de Construir / outorga onerosa / potencial construtivo).
As 30 no escopo são **IPTU/execução fiscal**; 2 fora de escopo (ISS e previdenciário). Não é erro item-a-item —
é **lacuna de cobertura do corpus** relativa à prioridade declarada. Registrado como Achado #1 (P0). Material
de TDC existe em `engines/tdc/` (fórmulas/valuation), mas **jurisprudência** de TDC não existe no repo.

---

## (i) TABELA-RESUMO DAS 32

Legenda: **SUSTENTA** · **SUSTENTA-C/RESSALVA** · **NÃO-SUSTENTA** · **FORA-DE-ESCOPO**.
Confiança = confiança de que o holding está corretamente lido **contra o verbatim presente no repo**.

| # | id | Tema jurídico | Holding (1 linha) | Veredito | Conf. |
|---|---|---|---|---|---|
| 1 | stf-sumula-539 | IPTU — benefício social imóvel único | Lei municipal pode reduzir imposto predial de imóvel residencial único do proprietário | SUSTENTA | Alta |
| 2 | stf-sumula-589 | IPTU — vedação adicional por nº de imóveis | Inconstitucional adicional progressivo do IPTU em função do número de imóveis | SUSTENTA | Alta |
| 3 | stf-sumula-668 | IPTU — progressividade antes da EC 29 | Inconstitucional progressividade fiscal do IPTU por lei anterior à EC 29/2000 (salvo função social) | SUSTENTA | Alta |
| 4 | stf-sumula-670 | Taxa iluminação pública (bloco "carnê") | Iluminação pública (uti universi) não pode ser custeada por taxa | SUSTENTA-C/RESSALVA | Alta |
| 5 | stf-sumula-724 | IPTU — imunidade art. 150 VI c + locação | Imóvel de entidade imune locado a 3º permanece imune se aluguel aplicado nas finalidades essenciais | SUSTENTA | Alta |
| 6 | stf-sv-19 | Taxa de coleta de lixo (bloco "carnê") | Taxa exclusiva de coleta/remoção/tratamento de lixo de imóveis é constitucional | SUSTENTA-C/RESSALVA | Alta |
| 7 | stf-tema-1020 | **ISS** (cadastro prestador / retenção) | Inconstitucional obrigar cadastro de prestador de fora + retenção de ISS pelo tomador | **FORA-DE-ESCOPO** | Alta |
| 8 | stf-tema-1084 | IPTU — avaliação individualizada fora da PGV | Constitucional delegar avaliação de imóvel novo fora da PGV, se critérios em lei + contraditório | SUSTENTA | Alta |
| 9 | stf-tema-155 | IPTU — progressividade antes da EC 29 (RG) | Reafirma Súmula 668 em repercussão geral | SUSTENTA | Alta |
| 10 | stf-tema-523 | IPTU — seletividade antes da EC 29 | Constitucional diferenciar alíquota por edificado/não-edificado, R/nR antes da EC 29 | SUSTENTA | Alta |
| 11 | stf-tema-94 | IPTU — progressividade depois da EC 29 | Constitucional a EC 29/2000 ao permitir alíquotas progressivas de IPTU pelo valor | SUSTENTA | Alta |
| 12 | stj-resp-1112646 | IPTU×ITR — destinação rural | Não incide IPTU (mas ITR) sobre imóvel urbano comprovadamente em exploração rural (art. 15 DL 57/66) | SUSTENTA | Alta |
| 13 | stj-resp-1130545 | IPTU — revisão lançamento por erro de fato | Retificação cadastral (erro de fato, art. 149 VIII CTN) autoriza revisão dentro da decadência | SUSTENTA | Alta |
| 14 | stj-resp-1202136 | IPTU — taxas ilegais no carnê | Taxa ilegal no carnê não anula o IPTU; abate-se por cálculo aritmético (preserva CDA) | SUSTENTA | Alta |
| 15 | stj-resp-1645832 | IPTU — publicidade da PGV | PGV deve ter publicação oficial; afixação no átrio não supre | SUSTENTA | Alta |
| 16 | stj-resp-1658054 | **Previdenciário** | Monocrática sobre contribuição previdenciária s/ 13º do aviso prévio — não é IPTU | **FORA-DE-ESCOPO** | Alta |
| 17 | stj-sumula-314 | Exec. fiscal — prescrição intercorrente | Não achados bens, suspende 1 ano; após, corre prescrição quinquenal intercorrente | SUSTENTA | Alta |
| 18 | stj-sumula-392 | Exec. fiscal — substituição da CDA | Fazenda pode substituir CDA por erro material/formal até sentença de embargos; vedado mudar sujeito passivo | SUSTENTA | Alta |
| 19 | stj-sumula-393 | Exec. fiscal — exceção de pré-executividade | Cabível para matérias conhecíveis de ofício sem dilação probatória | SUSTENTA | Alta |
| 20 | stj-sumula-397 | IPTU — notificação pelo carnê | Envio do carnê ao endereço notifica o contribuinte do lançamento | SUSTENTA | Alta |
| 21 | stj-sumula-399 | IPTU — sujeito passivo por lei municipal | Cabe à legislação municipal estabelecer o sujeito passivo do IPTU | SUSTENTA | Alta |
| 22 | stj-sumula-409 | Exec. fiscal — prescrição de ofício | Prescrição anterior à propositura pode ser decretada de ofício | SUSTENTA-C/RESSALVA | Alta |
| 23 | stj-sumula-481 | Processual — justiça gratuita a PJ | PJ faz jus à gratuidade se comprovar impossibilidade de arcar com encargos | SUSTENTA-C/RESSALVA | Alta |
| 24 | stj-sumula-614 | IPTU — locatário sem legitimidade | Locatário não tem legitimidade ativa para discutir IPTU/taxas nem repetir indébito | SUSTENTA | Alta |
| 25 | stj-sumula-626 | IPTU — área urbanizável/expansão | IPTU incide em área urbanizável/expansão sem exigir os melhoramentos do art. 32 §1º CTN | SUSTENTA | Alta |
| 26 | stj-tema-1113 | ITBI — base de cálculo ≠ IPTU | Base do ITBI é valor de mercado da transação; não vinculada à do IPTU (nem piso) | SUSTENTA | Alta |
| 27 | stj-tema-1158 | IPTU — alienação fiduciária | Credor fiduciário não é sujeito passivo do IPTU antes de consolidar propriedade e ser imitido na posse | SUSTENTA | Alta |
| 28 | stj-tema-1350 | Exec. fiscal — emenda da CDA (fund. legal) | Vedado substituir/emendar CDA para incluir/modificar o fundamento legal do crédito | SUSTENTA-C/RESSALVA | Média |
| 29 | stj-tema-174 | IPTU×ITR — destinação rural | (idêntico ao #12 — mesmo leading case REsp 1.112.646) | SUSTENTA | Alta |
| 30 | stj-tema-262 | (não verificado) | Objeto/tese não confirmado como IPTU; provável confusão c/ Tema 122 | **NÃO-SUSTENTA** (stub) | Baixa |
| 31 | stj-tema-399 | (não verificado) | Objeto/tese não confirmado; provável confusão numérica c/ Súmula 399 | **NÃO-SUSTENTA** (stub) | Baixa |
| 32 | stj-tema-566 | Exec. fiscal — marco da prescrição intercorrente | Prazo de 1 ano + prescrição correm da ciência da Fazenda sobre não-localização | SUSTENTA | Alta |

**Contagem:** SUSTENTA 22 · SUSTENTA-C/RESSALVA 5 (itens 4, 6, 22, 23, 28) · NÃO-SUSTENTA 2 (stubs 30, 31) ·
FORA-DE-ESCOPO 2 (7, 16). Par redundante (12≡29). **Zero TDC.**

---

## (ii) FICHAS DIALÉTICAS — TEMAS CENTRAIS (tese · antítese · vacina)

### Ficha 1 — Progressividade do IPTU (668/155/94 + 523/589)
- **Tese:** progressividade **fiscal** (por valor venal) só vale **a partir da EC 29/2000**; lei municipal anterior é inconstitucional (Súmula 668; Tema 155). Adicional por **nº de imóveis** é inconstitucional (Súmula 589).
- **Antítese (fisco):** (a) o que se ataca é **seletividade** por destinação — válida mesmo antes da EC 29 (Tema 523); (b) pós-EC 29 a progressividade é constitucional (Tema 94).
- **Vacina:** separar na peça os três institutos — progressividade **fiscal** (pós-EC 29, Tema 94), **extrafiscal/no tempo** (função social, art. 182 §4º II CF), **seletividade** por destinação (sempre válida, Tema 523). Conferir a **data da lei municipal** contra 10/09/2000 (vigência EC 29) — a vigência é o divisor (1.6).

### Ficha 2 — Valor venal / PGV / avaliação individualizada (1084/1645832/1113)
- **Tese:** base = **valor venal** (CTN art. 33); a PGV exige **publicação oficial** (REsp 1.645.832 — átrio não supre); avaliação **fora da PGV** exige critérios **em lei** + **contraditório** (Tema 1084).
- **Antítese (fisco):** valor venal do IPTU serve de piso/parâmetro a outras exações; avaliação administrativa é regular.
- **Vacina:** Tema 1113 **dissocia** as bases (valor venal IPTU não é piso nem teto do ITBI); contra arbitramento fora da PGV, exigir a **dupla condição cumulativa** do Tema 1084 (lei **E** contraditório) — falta de uma = lançamento nulo.

### Ficha 3 — Sujeito passivo (399/614/1158 + 397)
- **Tese:** cabe à **lei municipal** eleger o sujeito passivo entre os do art. 34 CTN (Súmula 399); **locatário não** (Súmula 614); **credor fiduciário não** antes de consolidar propriedade + imissão (Tema 1158).
- **Antítese (fisco):** havendo pluralidade do art. 34, cobra-se de qualquer figura (banco, locatário).
- **Vacina:** art. 34 CTN é **taxativo**; convenção particular é **inoponível ao Fisco** (CTN art. 123). Banco fiduciário: marco = **imissão na posse** (Tema 1158).

### Ficha 4 — Cobranças indevidas no carnê (670/SV19/1202136)
- **Tese:** serviço **uti universi** (iluminação — Súmula 670; limpeza de vias — REsp 1.202.136) não entra no carnê; se entrou, **abate-se** a parcela sem anular o IPTU (REsp 1.202.136).
- **Antítese (fisco):** coleta **domiciliar** de lixo É específica/divisível — taxa **constitucional** (SV 19); ilegalidade de taxa não contamina a CDA.
- **Vacina:** distinguir **lixo domiciliar** (válido, SV 19) de **varrição de logradouros** (inválido, uti universi). Pedir **abatimento da parcela**, nunca nulidade total. Iluminação → **COSIP/CIP** (art. 149-A CF).
- **Ressalva (Achado #3):** Súmula 670 e SV 19 decidem **taxas**, não IPTU — pano de fundo, não holding de IPTU.

### Ficha 5 — IPTU × ITR (174≡1112646 + 626)
- **Tese:** prevalece a **destinação econômica** — imóvel urbano em exploração rural sofre **ITR** (art. 15 DL 57/66; Tema 174).
- **Antítese (fisco):** critério do art. 32 CTN é **topográfico**; em área urbanizável/expansão o IPTU incide sem os melhoramentos (Súmula 626).
- **Vacina:** ônus do contribuinte **comprovar** exploração rural efetiva (Tema 174 exige "comprovadamente"); 626 e 174 convivem.

### Ficha 6 — Execução fiscal (314/566/409/392/393/1350)
- **Tese:** intercorrente corre **automaticamente** (Súmula 314 + Tema 566); prescrição de **ofício** (Súmula 409); **exceção de pré-executividade** sem garantia (Súmula 393); Fazenda **não** emenda CDA para trocar **fundamento legal** (Tema 1350).
- **Antítese (fisco):** CDA tem presunção de liquidez; substituição por erro **material/formal** até sentença de embargos (Súmula 392).
- **Vacina:** delimitar **erro material/formal** (permitido, 392) × **mudança de sujeito passivo** (vedado, 392) × **mudança de fundamento legal** (vedado, Tema 1350 — estreita a 392). Marcar a data de ciência da Fazenda (Tema 566).
- **Ressalva (Achado #4):** Súmulas 314/392/393/409/481 são de **execução fiscal/processo** genérico — aplicáveis ao IPTU, mas o holding não menciona IPTU.

---

## (iii) ACHADOS / RESSALVAS — PRIORIZADOS

**P0 — bloqueantes de mérito / cobertura**
1. **Corpus não cobre TDC, base prioritária (MOU 2026-06-20).** 0/32. **[VERIFICADO CONFIRMADO.]** Ação: capturar jurisprudência de TDC (STF/STJ/TJSP sobre outorga onerosa, solo criado, TDC) — hoje inexistente. → **novo item de backlog B-21.**
2. **stj-tema-262 e stj-tema-399 são stubs NÃO-VERIFICADOS.** Ambos `.md` auto-declaram falha de confirmação. **[VERIFICADO CONFIRMADO.]** **NÃO-SUSTENTA** enquanto stub; **não citar em peça** até confirmar no STJ (262→provável Tema 122; 399→provável Súmula 399, já coberta).

**P1 — classificação / risco de citação incorreta**
3. **Súmulas 670 e SV 19 decidem TAXAS, não IPTU** — pano de fundo do bloco "carnê". Rotular no uso como "correlato/periférico", nunca holding de IPTU. (Nada se descarta — mantidas.)
4. **Súmulas processuais (409, 481) e de execução fiscal genérica (314, 392, 393)** aplicam-se ao IPTU mas não o mencionam. Citar como "regra de execução fiscal **aplicável** ao IPTU".
5. **Dessincronização .md × .json** (ruído de confiança, não erro de mérito): vários `.md` mantêm auto-ressalva "confiança média" que o `.json` já resolveu via `verificacao_verbatim` (Tema 94, 155, REsp 1.202.136, 1.645.832). Sincronizar as notas .md ↔ .json. → **novo item de backlog B-22.**

**P2 — housekeeping**
6. **Par redundante 12≡29** (REsp 1.112.646 = leading case do Tema 174) — **intencional** (indexado por REsp e por Tema). São ~29 teses distintas, não 32.
7. **Fora-de-escopo (2) confirmados no mérito:** stf-tema-1020 (ISS) e stj-resp-1658054 (previdenciário). Realocar/arquivar.

---

## (iv) PENDENTE DE CONFIRMAÇÃO EXTERNA (declarado, não inventado — sem egress)
1. **stj-tema-262** — número/tese reais (hipótese: Tema 122). Não citar até verificar no portal de repetitivos STJ.
2. **stj-tema-399** — existência/objeto como tema (hipótese: confusão com Súmula 399).
3. **stj-resp-1658054** — número correto e tese (capturado é previdenciário/monocrático).
4. **stj-resp-1645832** — só a **ementa** capturada; inteiro teor confirmaria a redação literal (ementa já basta ao uso).
5. **stf-tema-94 / stf-tema-155** — leitura do acórdão de mérito fecharia a última margem (baixo risco; teses de RG estáveis).
6. **stj-tema-1350** — tema recente (trânsito 22/12/2025); confirmar redação exata no acórdão.
7. **Meta:** nenhum número de acórdão/Tema/holding foi inventado. Onde faltou verbatim (262, 399, 1658054), o veredito é NÃO-SUSTENTA/FORA-DE-ESCOPO — a lacuna **não** foi preenchida com suposição.

---

### Síntese honesta (1.2 · 1.7)
Dos 32: **27** sustentam com solidez o uso de IPTU (22 plenos + 5 com ressalva de "regra de execução fiscal/taxa
aplicável, não holding de IPTU"). **2** não sustentam (stubs 262/399). **2** fora de escopo (1020=ISS,
1658054=previdenciário). O maior achado **não** é item-a-item: é que o corpus jurisprudencial **não cobre TDC**,
a base declarada como prioritária. Citações batem com o verbatim onde há verbatim; onde não há (3 itens), está
declarado, não maquiado.
