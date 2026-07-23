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
1. **Ler o verbatim** da Lei 15.889/2013 e das revisões (16.768/17.719/18.330) — já ingeridas — procurando
   **cláusula de atualização monetária** dos valores das faixas (termos: "atualização", "corrigidos",
   "índice", "decreto do Executivo", "valores… reajustados").
   - **Achou cláusula** → antítese vence: o engine passa a aplicar o fator às faixas (com citação do artigo)
     e some a sinalização.
   - **Não achou** → tese vence: faixas ficam nominais até revisão-lei; o engine mantém o comportamento atual
     e a nota vira definitiva (com citação da ausência de cláusula + CF 150 I / CTN 97).
2. **Decisão do dono/advogado** registrada aqui e no `MANIFESTO`/`METADATA` (vintage), com o dispositivo que
   fundamentou.

> **Estado:** questão **aberta**; engine **fail-closed** (não aplica). Próximo passo = varredura de cláusula
> de atualização no verbatim das 4 leis (determinístico) → decisão citada. Nada muda no cálculo até isso.
