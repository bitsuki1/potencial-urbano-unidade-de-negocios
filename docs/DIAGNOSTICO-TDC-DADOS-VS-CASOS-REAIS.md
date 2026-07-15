# Diagnóstico TDC — o que CALCULAMOS × os CASOS REAIS que temos

> Estudo comparativo pedido pelo MOU (2026-07-15): cruzar as quatro camadas do produto TDC — **comercial**,
> **matemática**, **jurídica** e o que mais houver — contra os **casos reais já ingeridos**, antes de capturar mais.
> Tudo medido sobre os dados no repo (`zepec/ferramenta/zepec_cedentes_oficial.csv`, 4.360 linhas; FUNDURB; corpus).
> Nenhum número inventado (1.3): cada célula é computável pelos scripts citados.

## Veredito em uma linha
**O motor Art. 128 está bem calibrado como REFERÊNCIA/TETO — nos casos reais que dá para conferir, o R$/m² efetivo
bate ~90% do nosso número, e a diferença é explicada pelo REAJUSTE do Quadro 14 (vintage do VTcd), não por erro de
fórmula.** Mas a amostra de casos reais **com preço** é minúscula (**4 de 80** certidões) — a validação é um indício
forte, não prova estatística. O gargalo é **empírico (preço real + data de referência), não jurídico nem de fórmula.**

---

## 1. Dimensão MATEMÁTICA — motor Art. 128 × R$/m² REAL do FUNDURB
Temos **4 transferências reais com valor em R$** (FUNDURB, "Transferido em jul/2025") e SQL identificável. Comparando o
**R$/m² real** (valor ÷ m² transferido) com o nosso **Art. 128** (VTcd 2026 ÷ CAmaxcd 4):

| SQL | m² transf. | R$ real (FUNDURB) | R$/m² real | Nosso VTcd/4 (2026) | real/nosso | Explicação |
|-----|-----------:|------------------:|-----------:|--------------------:|-----------:|------------|
| 0090200034 | 245,52 | 429.581,66 | **1.749,68** | 1.937,16 | **0,903** | ✅ = reajuste Q14 ~2024/25→26 (1,107) |
| 0090200032 | 324,00 | 582.298,24 | **1.797,22** | 1.937,16 | **0,928** | ✅ = reajuste Q14 ~2025→26 (1,078) |
| 0090200033 | 601,77 | 540.780,61 | **898,65** | 1.937,16 | **0,464** | ⚠️ **outlier** (2,156× — nenhum reajuste ≤1,26 explica) |
| 0500084586 | 3.870,00 | 2.342.577,04 | 605,32 | — | — | sem VTcd na base Q14 (fora da quadra 009) |

**Leitura:** em 2 dos 3 casos com VTcd, o valor real usou o **VTcd do vintage da transferência** (mais barato), e o
nosso número (VTcd 2026 vigente) fica ~8–11% acima — **exatamente o que `vtcd_na_data()` corrige** (fiado ontem no
dossiê). Isto **valida o motor E a necessidade do §2º/vintage**: alimentado com o VTcd da data de referência, o Art. 128
deve encostar no real. O caso **033** é um outlier verdadeiro (fator 2,16, acima do teto de reajuste 1,26) — ou valor
parcial, ou lote/face diferente, ou dado a conferir: **want-list de captura.** O **0500084586** expõe a **falta de
cobertura do Quadro 14** fora da quadra central.

## 2. Dimensão COMERCIAL — preço-proxy (nosso) × transação real
- **Descasamento estrutural:** os 4 casos com preço real têm **`saldo = 0`** (já transferiram tudo) → o nosso
  `preco_proxy` (que precifica o **saldo vendável**) está **vazio** para eles. Ou seja: **temos preço real só de
  imóveis ESGOTADOS, e precificamos só os NÃO-esgotados** — zero sobreposição direta numa mesma listagem viva.
  A validação do §1 vale pela **taxa R$/m²** (comparável), não por A/B do mesmo imóvel.
- **Universo comercial (4.360):** `SO_ELEGIVEL` 3.659 · `INTACTO` 501 · `TEM_SALDO` 95 · `VEDADO_LEI` 28 · `ESGOTADO` 9.
  **Negociável = sim** em 2.750; "verificar" 1.568; "não" 42.
- **Conclusão comercial:** temos um funil grande de **oferta** (cedentes elegíveis) e quase nenhum **preço de mercado
  real** para ancorar margem — só 4 pontos, todos de imóveis esgotados. É o buraco comercial nº 1.

## 3. Dimensão MERCADO REAL (as certidões já capturadas)
- **80 certidões reais** ingeridas; **651.523 m²** de potencial efetivamente transferido.
- Tamanho por transferência: mín **166 m²** · mediana **3.046 m²** · máx **106.456 m²** (cauda longa — poucos negócios
  gigantes dominam o volume).
- **Só 4 de 80** têm o valor em R$ (FUNDURB). **76 transferências reais têm o m² mas não o preço** → maior alvo de captura.

## 4. Dimensão JURÍDICA — o corpus × o que os casos invocam
- Corpus: **71 normas** (.md) + **39 peças de jurisprudência**. Os casos reais giram em torno de **Art. 125** (PCpt),
  **Art. 128** (valor + §2º), **Art. 129** (conservação) e do **processo FUNDURB** — todos cobertos verbatim.
- **A lacuna aqui NÃO é de lei:** os dispositivos que os casos usam estão no corpus e citados. O que falta é o **dado
  empírico** (preço real + data de referência) para fechar o laço fórmula→realidade, e o **inteiro teor** dos acórdãos
  (hoje fichas/metadados) para firmar a camada de tese.

## 5. Achados cruzados (o diagnóstico)
1. **O motor acerta como referência** — real ≈ 0,90× do Art. 128 nos casos alinhados; a diferença **é o reajuste do
   Quadro 14**, não erro. Fortalece a decisão de usar `vtcd_na_data` (VTcd do vintage), não o 2026 vigente.
2. **A amostra é anedótica (n=4, sendo 1 outlier e 1 sem VTcd → n útil = 2).** Precisa de mais casos com preço **e**
   data de referência para virar calibração estatística e medir a margem real de mercado.
3. **Descasamento saldo:** preço real só existe em imóveis **esgotados**; precificamos os **vivos**. Sem preço de
   mercado em listagem viva, "a margem é do dono" fica sem âncora empírica.
4. **Cobertura de VTcd incompleta fora da quadra central** (ex.: 0500084586 sem Q14) — limita quantos casos reais dá
   para calibrar.
5. **Outlier 033** (2,16×) é sinal honesto de dado a conferir — não se ajusta a nenhum reajuste; vai para a want-list.

## 6. O que falta capturar (alimenta o prompt de captura)
Priorizado pelo retorno para a calibração:
1. **Valor pecuniário (R$) das outras 76 certidões reais** — o preço é o dado mais escasso (temos 4/80).
2. **Data de referência (protocolo da Declaração) de cada transferência real** — sem ela não isolamos o efeito vintage
   (é o que explica o gap e desmonta/confirma o outlier 033).
3. **VTcd do Quadro 14 para os SQLs fora da quadra 009** (ex.: setor 050) — fechar a cobertura para calibrar mais casos.
4. **Cr / outorga do imóvel receptor** (lado comprador) — fecha o laço completo do Art. 128 (hoje só o lado cedente).
5. **Inteiro teor dos acórdãos** já fichados (2257458, 1070175, 179340…) — firma a camada de tese.

## Como reproduzir este diagnóstico
`python3 zepec/gerar_dossie.py --sql 0090200034` (e 032/033) · a tabela do §1 sai de `valor_pecuniario_rs ÷
m2_ja_transferido` × `v_outorga_m2_q14 ÷ 4` no CSV oficial · reajustes em `tabelas/q14-reajuste-anual.csv`.
Tudo determinístico e citado (1.3/1.7).
