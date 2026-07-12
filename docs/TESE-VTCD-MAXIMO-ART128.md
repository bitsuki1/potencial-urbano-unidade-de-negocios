# TESE (OP-1b) — VTcd máximo rastreável no preço do TDC (Art. 128 §2º)

> **Status: ABERTA (dossiê de handoff).** Autorizada pelo dono (2026-07-11 "sim, tudo oficial"). Este é o
> arranque da tese (camada Gen Advogado). Traz o argumento, a base legal já OFICIAL, a antítese, a vacina
> e a **materialização no engine** (próximo passo concreto). NÃO altera preço sozinha — o preço em produção
> hoje usa o Quadro 14 vigente 2026 (OP-1a, feito). Esta tese é o **teto** que o vendedor pode reivindicar.

## 1. A tese (o que se quer sustentar)
Para o cedente ZEPEC-BIR, o **VTcd** (valor do m² do terreno cedente, Art. 128 §1º) que entra no preço do
TDC deve ser o **MÁXIMO rastreável** entre:
- **(A) Quadro 14 vigente** (ano-ref 2026 — Dec. 64.884/2025; é o que o engine usa hoje, OP-1a); e
- **(B) valor do terreno na Declaração corrigido por IPCA** — Art. 128 **§2º**: o VTcd é corrigido pelo IPCA
  acumulado entre o mês seguinte ao **mês de referência da Declaração** e o mês anterior ao protocolo.
Cada base é citável ao seu dispositivo; a referência final é `MAX(A, B)`, **por SQL**, sempre com a memória
de cálculo (1.3). O vendedor não deve receber menos que o maior valor que a própria lei lhe assegura.

## 2. Base legal (OFICIAL — já no corpus)
- **Art. 128, caput e §1º, Lei 16.050/2014 (PDE):** `PCr = (PCpt × VTcd)/(Cr × CAmaxcd)`; VTcd = valor do
  m² do terreno cedente, do Cadastro de Valor de Terreno para Outorga Onerosa (Quadro 14). Engine: `art128.py`.
- **Art. 128 §2º:** correção do VTcd pelo **IPCA** acumulado (mês seguinte ao mês de referência da Declaração
  → mês anterior ao protocolo da Certidão). Engine: `corrigir_vtcd_ipca()`.
- **Lei 17.975/2023 (revisão intermediária do PDE — 08/07/2023), art. que dá NR ao ZEPEC-BIR:** _"§ 1º A
  transferência do direito de construir de imóveis classificados como ZEPEC-BIR se dará de acordo com o
  disposto nos **arts. 124, 125, 128 e 133** desta Lei."_ → **confirma que o preço do NOSSO cedente (BIR)
  roteia pelo Art. 128** — a base do engine é **vigente** (checagem de vigência 1.6: OK, sem quebra).
- **IPCA jan/2014 → jun/2026** (série IBGE/SIDRA 1737, já em `tabelas/ipca-numero-indice-ibge.csv`): fator
  **1,9330 (+93,3%)**. É o tamanho do §2º se a referência da Declaração remontar a 2014.

## 3. Por que isto é "melhores condições"
Hoje a prospecção usa a base (A) sem §2º ("prospecção sem data protocolada, §2º N/A"). Correto como PISO,
mas **subvaloriza** quando (B) > (A). Em imóveis cujo valor de referência da Declaração é antigo, o IPCA do
§2º pode levar (B) muito acima de (A) — até ~+93% no limite 2014. Entregar `MAX(A,B)` citado = o maior preço
**que a lei já assegura**, sem inventar nada (1.3).

## 4. Antítese (o que a Prefeitura/comprador dirá) e Vacina
- **Antítese 1:** "§2º só vale após Declaração protocolada; em prospecção usa-se o Quadro 14 vigente." →
  **Vacina:** verdade para o PISO de prospecção; a tese NÃO nega isso — sustenta que, **havendo Declaração
  com mês de referência**, o §2º é **direito do cedente** e a referência passa a `MAX(A,B)`. O produto deve
  mostrar os DOIS (piso vigente + teto §2º) com a data-ref como parâmetro explícito (nunca "adivinhar hoje").
- **Antítese 2:** "o mês de referência da Declaração é recente (Quadro 14 atual), logo IPCA≈0." →
  **Vacina:** é caso a caso; quando a Declaração/instrução remonta a referência antiga, o IPCA é devido.
  A tese entrega o cálculo rastreável para CADA data-ref; não afirma +93% universal.
- **Antítese 3 (vigência):** "Lei 17.975/2023 mudou o Art. 128." → **Vacina:** o texto capturado mostra a NR
  mantendo o roteamento ZEPEC-BIR pelos arts. 124/125/**128**/133; não reescreveu o §2º. Confirmar o §2º
  vigente no verbatim já ingerido (`leis/municipal-sp/lei-municipal-saopaulo-16050-2014.md` + 17.975/2023).

## 5. Materialização no engine (PRÓXIMO PASSO concreto — para a próxima instância)
1. `art128.referencia_art128(...)` passa a aceptar **data-ref da Declaração** (parâmetro explícito) e, quando
   presente, computar (B) = VTcd_declaração × fator_ipca(data_ref → protocolo) e devolver `referencia = MAX(A,B)`
   com a memória de qual base venceu (cada uma citada). Sem data-ref → mantém o PISO (A) de hoje (compatível).
2. Eval novo (`evals/ground-truth/` ou `eval-art128`): casos onde (B)>(A) e (A)≥(B), provando o MAX e a citação.
3. Produto (dossiê): exibir **piso (Quadro 14 vigente)** e **teto (§2º IPCA)** lado a lado, com a data-ref como
   entrada — nunca "hoje" implícito (1.3).
4. Gate + regenerar.

## 6. Ligação com OP-1c (mesmo eixo, do lado do parque/Fp)
Lei 17.975/2023 **art. 50** deu NR ao **Art. 127 §1º** do PDE (Fp de parque): **IV = 1,4** se o valor de terreno
no Quadro 14 **≤ R$ 2.000/m²**; **V = 1,0** se **> R$ 2.000/m²** ("observadas as atualizações subsequentes"). O
**Decreto 64.884/2025** fixa a referência do Art. 127 em **R$ 2.352,06/m²**. ⇒ conferir se `engines/tdc/fp.py`
aplica esse limiar e valor 2026 (outra "condição melhor" possível, do lado comprador/eixo). **A conferir.**

---
> M6 · OP-1b (tese) · PU 18 · 2026-07-11. Fontes: corpus (Art. 128/§1º/§2º Lei 16.050/2014; Lei 17.975/2023 já
> ingerida); IPCA IBGE em repo; Dec. 64.884/2025. Próximo: materializar o MAX no engine + eval + produto.
