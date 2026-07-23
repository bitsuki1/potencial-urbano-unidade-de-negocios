# IPTU — faixas do adicional × anexos da PGV (o que é fixo e o que é vintage)

> Investigação primária (2026-07-19, PU 22) do item "anexos absolutos das leis de revisão do IPTU".
> Conclusão em duas partes: **(1)** as FAIXAS do adicional NÃO mudam entre as revisões — o CSV do engine
> já está correto; **(2)** o que muda por exercício são os VALORES da PGV (Tabela VI + terreno), que vivem
> em **PDF separado do DOC** (não no texto compilado do portal) e exigem captura pelo runner.

## (1) As faixas do adicional são de 2013 e NÃO resetam — achado provado
As faixas de desconto/acréscimo do IPTU (Imposto Predial residencial Art. 7º-A; predial não-residencial
Art. 8º-A; territorial Art. 28 da Lei 6.989/1966) foram fixadas pela **Lei 15.889/2013, Arts. 3º/4º/5º**:
`até 150k · 150–300k · 300–600k · 600k–1,2M · >1,2M` com ±0,3%/0,1% (resid.) e ±0,4%/0,2%/0,0% (não-resid./terr.).

**Prova (texto primário no corpus):** as leis de PGV posteriores **17.719/2021** e **18.330/2025** têm
**ZERO** alteração aos Arts. 7º-A / 8º-A / 28 (grep = 0 em ambas). Elas só: (a) atualizam a **Tabela VI**
(valores de construção) e a **Listagem de valores de terreno** via **Anexos I e II** (Art. 1º); e (b) concedem
o **desconto/trava** do Art. 3º (limita o aumento do lançamento ano a ano). **Nenhuma toca as faixas do adicional.**

➡️ **Consequência:** `tabelas/iptu-aliquotas-faixa.csv` (faixas nominais de 15.889/2013) está **CORRETO e
completo para todos os exercícios** (2014→2026). A dúvida aberta no PR ("aplicar atualização às faixas")
resolve-se: as faixas não são corrigidas por decreto nem resetadas — são nominais de 2013 por lei. O fator
de atualização anual (`iptu-atualizacao-anual.csv`) age sobre o **valor venal**, não sobre as faixas.

## (2) O que É vintage (e falta): os valores da PGV, em PDF do DOC
O que muda a cada revisão de PGV são os **valores absolutos** de:
- **Anexo I — Tabela VI** (valor unitário de m² de construção por tipo/padrão) — compacto (~dezenas de linhas);
- **Anexo II — Listagem de valores de m² de terreno** por logradouro/face — **escala Quadro 14** (dezenas de milhares de linhas).

Esses anexos **não estão no texto compilado do portal** — são "Documento Anexo" separado no DOC. Referências primárias já identificadas:
- **Lei 18.330/2025** (exercício 2026): `Documento Anexo nº 145975345`.
- **Lei 17.719/2021** (exercício 2022): Anexos I e II (idem, doc próprio a identificar).
- **Lei 15.889/2013** (exercício 2014): Anexos I e II.

**Avenida de captura:** o endpoint de documento do portal responde JS/500 a HTTP simples (`/documento/145975345`
→ 500). A via correta é o **runner `brasil`** (Playwright/IP-BR, mesma que venceu Imperva no Quadro 14/GeoSampa/CIT)
ou o visualizador do DOC. O Anexo II (terreno) é um **segundo Quadro 14** em porte — merece a mesma esteira
(sonda de layout → parser banda-Y → CSV vintage por exercício), como tarefa própria.

## Estado
- ✔️ Faixas do adicional: corretas e provadas (sem ação pendente).
- ⏳ Valores da PGV (Tabela VI + terreno) por vintage: pendência **precisa e escopada** — captura do DOC pelo
  runner, doc nº 145975345 (2026) como ponto de entrada. Não se inventa valor de imposto (1.3): entra do primário.
- ℹ️ "16.768/2017" não segue a cadência de PGV (as revisões reais são 2013/2021/2025); não localizada no portal
  como lei de PGV — provável rótulo trocado na fila. Fica registrado; não forçar.
