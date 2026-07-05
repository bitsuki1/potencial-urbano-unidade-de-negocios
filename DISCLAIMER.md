# DISCLAIMER — ferramenta de cedentes TDC (Potencial Urbano)
> Bloco canônico. É INJETADO no topo das saídas ao cliente (ex.: `zepec/ferramenta/COMO-USAR.md`) e referenciado nos dossiês/Excel. Marca de verificação no gate (`check_disclaimer`). PU 17 · 2026-07-04 (M0 — piso de credibilidade).

<!-- DISCLAIMER-BLOCO-INICIO -->
**AVISO — natureza e limites desta ferramenta (leia antes de usar qualquer número):**

1. **Decision-support, NÃO parecer/laudo.** Esta ferramenta apoia a originação comercial; não é parecer jurídico, avaliação (NBR 14653) nem laudo. Todo uso externo (proposta, cartório, negociação) exige conferência humana da fonte citada.
2. **Preço-proxy ≠ preço de mercado.** Onde há `preco_proxy_brl`, ele é um **proxy regulatório** (PCpt × V de outorga), NÃO o valor que o mercado paga. A banda de mercado real é outra coisa e não sai isolada.
3. **Valor venal ≠ valor de outorga.** `v_venal_m2_iptu` (IPTU) e `v_outorga_m2_q14` (Quadro 14) são grandezas distintas — nunca somar/trocar.
4. **PCpt: estimativa só para PROSPECÇÃO NOVA (T3).** Para o cohort **JÁ-DECLARADO** (`regime_pcpt=JA_DECLARADO`), o potencial é o que **consta na Declaração** (Art. 125 §1º I) — o número aqui é ESTIMATIVA (`qualidade_estimativa=PENDENTE_FI_DECLARADO`), não o valor declarado. Confiável só para tombado ainda sem declaração.
5. **Divergência conhecida (~66%).** A estimativa de PCpt diverge dos m² das certidões reais — **mediana da amostra ≈ 1,66×** (55 pares; valor vivo em `evals/eval-divergencia-pcpt.py`, corrigido na auditoria C-09 2026-07-05; a redação antiga "~1,27×/~27%" estava desatualizada). Onde há certidão, o **m² oficial vence a estimativa**.
6. **Data-base.** O `V` do Quadro 14 é **jan/2025**; protocolos posteriores podem exigir atualização (sem base/IPCA declarados na fonte).
7. **Conservação (Art. 129).** `elegibilidade_conservacao`: só **Atestado de Conservação** elegibiliza; **Termo de Compromisso** = PENDENTE (compromisso de remediar); tombamento (RES.) ≠ conservação.
8. **Número nasce no engine, com citação (1.3/1.7).** Todo valor é rastreável ao dispositivo citado. Onde a fonte não ampara, o campo diz **PENDENTE / NÃO CONSTA** — nunca um número inventado.
9. **Corpus RAG PARCIAL (A-11).** O acervo indexado cobre 19/31 leis e é majoritariamente IPTU; a massa normativa **TDC** (Decreto 57.536/2016, decretos ZEPEC) **ainda não foi ingerida**. As tabelas TDC e o engine PCpt estão provados, mas consultas ao **texto** de dispositivos TDC podem não ser fundamentáveis pelo RAG — conferir a fonte citada antes de uso externo.
<!-- DISCLAIMER-BLOCO-FIM -->
