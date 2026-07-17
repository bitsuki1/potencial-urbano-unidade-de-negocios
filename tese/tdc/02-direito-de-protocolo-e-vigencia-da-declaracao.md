# Tese TDC nº 02 — Direito de protocolo e a vigência da Declaração de Potencial Construtivo

> **STATUS: ✅ AUTO-ESCRUTINADA (2026-07-14) — gate D-13 delegado pelo MOU. PROPOSTA aberta a revisão.**
> _Lentes adversariais aplicadas: **(1) vigência estrita** — Art. 125 §2º e 128 §2º conferidos no verbatim atual; **(2)
> adversário** — a Procuradoria opõe a retroatividade EXPRESSA do Art. 124 §3º, que a antítese incorpora; **(3) sobre-extensão**
> — separei "congela a REGRA" de "congela o VALOR nominal" (o valor corrige por IPCA até a CT); **(4) prova** — TJSP 1070175 é
> ficha/mandado de segurança, não inteiro teor: resíduo declarado; **(5) número** — nenhum valor nasce aqui._
> **Artefato (1.1):** camada ARGUMENTATIVA sobre o corpus limpo (1.2). Todo fato carrega dispositivo + fonte (1.7).

## Proveniência
**Corpus (leis/):**
- PDE — Lei 16.050/2014: **Art. 125 §2º** (verbatim, l.4876-4878) — "Será considerada como **data de referência** a data do
  **protocolo** da solicitação da Declaração de Potencial Construtivo Passível de Transferência à SMDU"; **Art. 128 §2º**
  (l.4978+) — o VTcd é corrigido por **IPCA** entre o mês posterior ao de referência e o mês anterior ao **protocolo do pedido
  de Certidão de Transferência (CT)**; **Art. 124 §3º** — parcelamento que alcança "as declarações **já emitidas anteriormente**"
  (ressalva de retroatividade expressa).
- **Nota de vigência (1.6):** o Art. 125 §2º não foi alterado pela Lei 17.975/2023; o Art. 128 §2º idem — a âncora temporal
  está na redação de hoje.

**Jurisprudência (jurisprudencia/):**
- **TJSP 1070175-76.2019** (13ª C. Dir. Público, rel. Des. Spoladore Dominguez, j. 2021-09-22): **segurança concedida** —
  reconhecido direito líquido e certo a **rerratificar** a Declaração com base no **PDE/2014 (Lei 16.050/2014), AFASTANDO** as
  restrições da LPUOS **Lei 16.402/2016** — teoria do **direito de protocolo / ultratividade**. ⚠️ **Resíduo probatório
  declarado:** peça é **ficha/metadado** (inteiro teor a capturar) e mandado de segurança — suporte forte, mas a íntegra falta.

---

## TESE
A regra e a base de valor aplicáveis à TDC **cristalizam-se na data de referência, que a lei define como a data do protocolo
da Declaração** (Art. 125 §2º). O cedente tem, assim, um **direito de protocolo / ultratividade**: a lei restritiva
**posterior** ao protocolo **não alcança** a Declaração já protocolada — foi exatamente o que o **TJSP (1070175-76.2019)**
assegurou ao permitir rerratificar a Declaração pelo PDE/2014 e afastar as restrições da LPUOS/2016. Isso é a aplicação
direta do **princípio 1.6** (a norma vigente na data do fato gerador rege o fato): protocolar **congela a régua** — o
enquadramento, os fatores e o VTcd-base vigentes naquela data.

## ANTÍTESE
A cristalização **não é total** — tem três frestas.
1. **Retroatividade EXPRESSA fura a ultratividade.** A proteção vale contra mudança *tácita/posterior*; quando a lei
   **declara** que retroage, a Declaração emitida É alcançada. O próprio **Art. 124 §3º** é a prova: parcelou o excedente de
   50.000 m² "**incluindo as declarações já emitidas anteriormente à publicação desta lei**". Ou seja, o legislador pode, e já
   o fez, atingir declaração pretérita.
2. **Congelou a REGRA, não o VALOR nominal.** O Art. 128 §2º manda **corrigir o VTcd por IPCA** entre o mês posterior à data
   de referência e o mês anterior ao protocolo da **CT**. Logo o protocolo da Declaração fixa a *régua* e o *VTcd-base*, mas o
   valor **continua correndo** (monetariamente) até a CT — não se pode prometer valor nominal congelado.
3. **Prova indiciária.** O 1070175 está no corpus como **ficha** (não inteiro teor) e é caso concreto de MS — orienta, mas não
   é súmula nem tema repetitivo: um juízo diverso é juridicamente possível.

## VACINA (como blindar a operação)
1. **Protocolar a Declaração cedo.** É o ato que dispara o Art. 125 §2º — cristaliza régua + VTcd-base na melhor data possível.
2. **Fixar e documentar a data de referência.** É ela que ancora todo o resto (Art. 125 §2º e 128 §2º); registrar no dossiê.
3. **Não confundir "regra congelada" com "valor congelado".** O engine (`art128.py`, §2º IPCA) já corrige o VTcd até a CT — o
   dossiê apresenta o valor **corrigível**, não um nominal estático (evita frustração e alegação de subavaliação).
4. **Monitorar retroatividade expressa.** A única coisa que fura a ultratividade é a lei que se declara retroativa (como o §3º).
   Acompanhar revisões do PDE é a vigilância mínima — a vacina reduz risco de mudança tácita, não imuniza contra a expressa.
5. **Manter a conservação em dia (Art. 129).** O protocolo não dispensa a comprovação de conservação exigida na CT do
   ZEPEC-BIR (ver tese 05) — protocolar cedo e deixar a conservação cair trava a Certidão do mesmo jeito.

---

### Ganchos para o produto (não-normativos — propostas)
- **Dossiê:** destacar a **data de referência (= protocolo)** como campo-âncora, com a régua vigente naquela data.
- **Dossiê:** exibir o valor do Art. 128 como **corrigível por IPCA até a CT** (não nominal fixo) — já suportado pelo engine.
- **Corpus:** capturar o **inteiro teor** do 1070175 para firmar o suporte do direito de protocolo.
