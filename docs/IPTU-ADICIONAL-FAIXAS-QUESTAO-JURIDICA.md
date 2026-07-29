# IPTU — as faixas do adicional se corrigem por decreto? (questão jurídica aberta)

> **Item 8 do backlog (dono, 2026-07-23: "faça também").** Este documento **não decide** — ele **estrutura
> a questão** (tese · antítese · vacina) para que a decisão seja tomada com base no verbatim, e registra o
> que o **engine faz enquanto isso** (fail-closed). Número/valor continua nascendo no engine (1.3) e a
> definição jurídica é do dono/advogado — a instância propõe, o dono decide (D21).

## O problema, em uma frase
A **atualização anual do IPTU** (série de decretos, `tabelas/iptu-atualizacao-anual.csv`) corrige o **valor
venal** (a base). Pergunta: esse mesmo fator **também** corrige os **limiares das faixas** que disparam
alíquotas maiores / o **adicional** progressivo — ou as faixas ficam **congeladas no valor nominal** da lei
que as fixou (15.889/2013 e suas revisões)?

**Por que importa (efeito "bracket creep"):** se o valor venal sobe pelo fator mas o limiar da faixa fica
nominal, mais imóveis **cruzam** para a faixa de cima a cada ano — pagam a alíquota/adicional maior **sem que
nenhuma lei tenha aumentado a faixa**. O efeito é puramente aritmético e recai sobre o contribuinte.

## Tese — as faixas NÃO se corrigem por decreto (ficam nominais até lei nova)
- **Legalidade tributária estrita** (CF art. 150, I; CTN art. 97, II e §§): alíquota e base de cálculo — e os
  **limiares que definem qual alíquota incide** — só se alteram por **lei**. Decreto não cria nem majora
  tributo, nem desloca faixa.
- As faixas do IPTU-SP nasceram em **valores absolutos** na Lei 15.889/2013 e foram **substituídas por
  valores absolutos** nas leis de revisão (15.889 → 16.768 → 17.719 → 18.330). O legislador escolheu
  **reescrever os números** a cada revisão — sinal de que a correção é **por lei**, não automática por decreto.
- **Consequência:** entre uma revisão-lei e a seguinte, a faixa fica **congelada em nominal**; o fator do
  decreto corrige a base, não o limiar. Bracket creep é real e (nesta leitura) **legal**.

## Antítese — o decreto PODE alcançar as faixas (se a lei autorizar a atualização monetária)
- Se a **própria lei das faixas** trouxer cláusula de **atualização monetária anual** dos valores nela
  fixados (por índice/decreto), então o decreto que aplica esse índice **alcança também os limiares** — não
  é "majorar por decreto", é **mera atualização monetária** (CTN art. 97 §2º: atualização do valor monetário
  **não** é majoração), permitida.
- Vários regimes municipais preveem exatamente isso para valores expressos em moeda. **Se** houver essa
  cláusula na 15.889/2013 (ou nas revisões), a antítese vence para o período entre revisões.

## Vacina / o que o ENGINE faz hoje (fail-closed, 1.3)
- O `engines/iptu/iptu.py` **expõe** o fator de atualização (`fator_atualizacao_iptu(ano_ref)`) mas **NÃO o
  aplica por padrão às faixas do adicional**. Ele calcula sobre a **faixa em valor nominal do ano-lei** e
  **sinaliza** que "correção da faixa por decreto = questão jurídica aberta".
- Isso é o comportamento **honesto**: o motor não presume onde o dono ainda não decidiu, e não inventa um
  número que dependeria de uma tese não fechada.

## Passo para FECHAR (determinístico, não por chute)
1. **Ler o verbatim** da Lei 15.889/2013 e das revisões (16.768/17.719/18.330) procurando
   **cláusula de atualização monetária** dos valores das faixas (termos: "atualização", "corrigidos",
   "índice", "decreto do Executivo", "valores… reajustados").
   - **Achou cláusula** → antítese vence: o engine passa a aplicar o fator às faixas (com citação do artigo)
     e some a sinalização.
   - **Não achou** → tese vence: faixas ficam nominais até revisão-lei; o engine mantém o comportamento atual
     e a nota vira definitiva (com citação da ausência de cláusula + CF 150 I / CTN 97).
2. **Decisão do dono/advogado** registrada aqui e no `MANIFESTO`/`METADATA` (vintage), com o dispositivo que
   fundamentou.

## VARREDURA — resultado (2026-07-29, determinístico; fato, não juízo)
> A varredura é **fato/citação** (o que o texto diz), não a decisão jurídica — esta continua do dono/advogado
> (D21, 1.3). O engine **não** foi alterado. Onde as faixas moram: **Arts. 7º-A/8º-A/28 da Lei 6.989/1966**,
> com as **tabelas dadas pelos Arts. 3º/4º/5º da Lei 15.889/2013** (confirmado no `engines/iptu/iptu.py`).

**O que a varredura verbatim encontrou (leis ingeridas 15.889/2013, 17.719/2021, 18.330/2025):**
1. **Lei 15.889/2013, Arts. 3º/4º/5º** — fixam as faixas do adicional em **valores nominais** (limiares
   R$ 150.000 / 300.000 / 600.000 / 1.200.000; acréscimo por porção). O texto é "passa a vigorar na seguinte
   conformidade" seguido da tabela — **sem** qualquer cláusula de atualização anexa a esses artigos.
2. **Única cláusula de auto-atualização na 15.889/2013 (Art. 15, §2º)** — atualiza a **importância fixa do
   teto da isenção de aposentado/pensionista** (Art. 1º da Lei 11.614/1994, "na forma do art. 2º da Lei
   13.105/2000"). É **outra rubrica** (isenção), **não** as faixas do adicional.
3. **Caminho de atualização da base é por LEI** — Art. 13 da 15.889/2013 (nova redação do Art. 10 da Lei
   15.044/2009) **obriga o Executivo a encaminhar projeto de lei** para atualizar os valores unitários de m².
   Reforça legalidade tributária estrita: base/limiar se mexem por **lei**, não por decreto.
4. **Lei 17.719/2021** — **não** reescreve os Arts. 7º-A/8º-A/28 nem toca os limiares das faixas. Suas
   cláusulas de "atualização de importâncias" (Art. 13, §5º) são das **faixas de ISS de sociedade
   uniprofissional** (outro imposto); o teto de IPCA do §6º/§8º limita o **aumento do lançamento** (valor
   venal) nos exercícios 2022-2024 — **não** desloca faixa do adicional.
5. **Lei 18.330/2025** — **não** reescreve os Arts. 7º-A/8º-A/28 nem os limiares das faixas do adicional; os
   valores que aparecem são de **isenção/desconto** do Imposto Predial (Arts. 2º/3º), outra rubrica.

**Leitura do resultado (para a decisão do dono/advogado):** nas 3 leis ingeridas, **nenhuma cláusula de
atualização monetária alcança as faixas do adicional** — elas seguem nos valores nominais de 2013 (13 anos sem
reescrita), e o caminho de atualização é explicitamente por lei. Isso **sustenta a TESE** (faixas nominais até
lei nova) e **confirma o comportamento atual do engine** (fail-closed) como o correto por padrão.

**Lacuna que impede fechar em 100%:** a **Lei 16.768** (uma das 4 nomeadas) **não está no corpus** (não
ingerida) — não pôde ser varrida verbatim. O `iptu.py` cita **só** a 15.889/2013 para as faixas, e elas
seguem inalteradas por 17.719/18.330 — indício forte de que a 16.768 também não as reescreveu — mas isso **não
é verbatim-verificado**. **Passo restante:** ingerir a Lei 16.768 e varrer os mesmos termos; se confirmar a
ausência de cláusula, a TESE fecha e o dono/advogado ratifica (a nota do engine vira definitiva com citação
CF art. 150, I / CTN art. 97).

> **Estado:** questão **aberta** (pendente ratificação do dono/advogado + varredura da 16.768); engine
> **fail-closed** (não aplica) — **inalterado**. Evidência da varredura das 3 leis ingeridas: **nenhuma
> cláusula de atualização alcança as faixas** → sustenta a tese. Nada muda no cálculo até a decisão citada.
