# PROMPTS DE EXTRAÇÃO VIA EXTENSÃO DO CLAUDE — Corpus jurídico IPTU/TDC

> Gerado pelo Escritório do MOU em 2026-06-18. Método reutilizável documentado em
> `escritorio-do-mou/processos/EXTRACAO_VIA_EXTENSAO.md`.
> Objetivo: capturar VERBATIM o texto oficial dos 59 artefatos cujos stubs já existem no repo
> com `status_pipeline=bruto` (só ementa+síntese). Cada arquivo baixado mapeia 1:1 com um stub.

## ANTES DE COMEÇAR (você, humano)
1. **Pasta de destino:** você já criou `IPTU-TDC` na Área de Trabalho. ✅
2. **Onde os arquivos caem:** ajuste a pasta de downloads do navegador para `Área de Trabalho/IPTU-TDC`
   **ou** escolha essa pasta no diálogo "Salvar como" a cada arquivo. O clique de "Salvar" é esperado —
   pode dar sem medo.
3. **Paralelismo:** pode abrir vários navegadores/abas e colar um LOTE diferente em cada um.
4. **Nome do arquivo = o `id`** indicado em cada item (ex.: `lei-federal-9514-1997.txt`). NÃO renomeie —
   é o que deixa a ingestão automática depois.

## REGRA DO FALLBACK (vale para todo item)
- Se a página oferecer um arquivo baixável (PDF/DOC), baixe o arquivo oficial e renomeie para o `id`.
- Se NÃO houver download (a maioria — planalto/prefeitura/stf/stj servem HTML), faça o **fallback de tela**:
  selecione o TEXTO PRINCIPAL renderizado (o corpo da lei/súmula/tese, sem menus), salve como `.txt` com o
  cabeçalho:
  ```
  FONTE: <URL>
  CAPTURA: 2026-06-18 — VERBATIM DE TELA
  ID: <id>
  ```
- Sites do STF/STJ com busca: se a página abrir um formulário, digite o número (da súmula/tema) e capture
  o resultado. Se o texto não renderizar, anote no arquivo "PÁGINA NÃO RENDERIZOU O TEXTO" e siga — não invente.

---

## LOTE 1 — LEIS FEDERAIS (planalto.gov.br) — 12 itens

> Cole na extensão: "Para cada item da lista abaixo, abra a URL, capture o texto integral da norma
> (verbatim de tela, com o cabeçalho FONTE/CAPTURA/ID) e baixe como `<id>.txt` na pasta IPTU-TDC."

| id (nome do arquivo) | URL oficial |
|---|---|
| `dl-57-1966.txt` | https://www.planalto.gov.br/ccivil_03/decreto-lei/del0057.htm |
| `ec-29-2000.txt` | https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc29.htm |
| `ec-116-2022.txt` | https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc116.htm |
| `ec-132-2023.txt` | https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm |
| `lei-federal-4591-1964.txt` | https://www.planalto.gov.br/ccivil_03/leis/l4591.htm |
| `lei-federal-6015-1973.txt` | https://www.planalto.gov.br/ccivil_03/leis/l6015consolidado.htm |
| `lei-federal-6830-1980.txt` | https://www.planalto.gov.br/ccivil_03/leis/l6830.htm |
| `lei-federal-8009-1990.txt` | https://www.planalto.gov.br/ccivil_03/leis/l8009.htm |
| `lei-federal-8668-1993.txt` | https://www.planalto.gov.br/ccivil_03/leis/l8668.htm |
| `lei-federal-9514-1997.txt` | https://www.planalto.gov.br/ccivil_03/leis/l9514.htm |
| `lei-federal-10931-2004.txt` | https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l10.931.htm |
| `lei-federal-11101-2005.txt` | https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11101.htm |

---

## LOTE 2 — LEIS MUNICIPAIS SP (legislacao.prefeitura.sp.gov.br) — 15 itens

> Cole na extensão: "Para cada item, abra a URL, capture o texto integral da lei (verbatim de tela,
> com cabeçalho) e baixe como `<id>.txt` na pasta IPTU-TDC. Capture TAMBÉM as tabelas/anexos se houver."

| id (nome do arquivo) | URL oficial |
|---|---|
| `lei-municipal-saopaulo-7228-1968.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-7228-de-12-de-dezembro-de-1968 |
| `lei-municipal-saopaulo-10235-1986.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-10235-de-16-de-dezembro-de-1986 |
| `lei-municipal-saopaulo-10365-1987.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-10365-de-22-de-setembro-de-1987 |
| `lei-municipal-saopaulo-11152-1991.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-11152-de-30-de-dezembro-de-1991 |
| `lei-municipal-saopaulo-11338-1992.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-11338-de-30-de-dezembro-de-1992 |
| `lei-municipal-saopaulo-12350-1997.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-12350-de-6-de-junho-de-1997 |
| `lei-municipal-saopaulo-13250-2001.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-13250-de-27-de-dezembro-de-2001 |
| `lei-municipal-saopaulo-13475-2002.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-13475-de-30-de-dezembro-de-2002 |
| `lei-municipal-saopaulo-14865-2008.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-14865-de-29-de-dezembro-de-2008 |
| `lei-municipal-saopaulo-15044-2009.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-15044-de-03-de-dezembro-de-2009 |
| `lei-municipal-saopaulo-16050-2014.txt` | https://legislacao.prefeitura.sp.gov.br/lei-16050-de-31-de-julho-de-2014 |
| `lei-municipal-saopaulo-17202-2019.txt` | https://legislacao.prefeitura.sp.gov.br/lei-17202-de-16-de-outubro-de-2019 |
| `lei-municipal-saopaulo-17577-2021.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-17577-de-20-de-julho-de-2021 |
| `lei-municipal-saopaulo-17759-2022.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-17759-de-15-de-marco-de-2022 |
| `lei-municipal-saopaulo-17844-2022.txt` | https://legislacao.prefeitura.sp.gov.br/leis/lei-17844-de-14-de-setembro-de-2022 |

---

## LOTE 3 — STF (súmulas + temas de repercussão geral) — 11 itens

> Cole na extensão: "Para cada item, abra a URL. Para SÚMULAS, capture o enunciado completo. Para TEMAS,
> capture a TESE de repercussão geral e a situação (mérito julgado/pendente). Baixe como `<id>.txt`."

| id (nome do arquivo) | URL oficial |
|---|---|
| `stf-sumula-539.txt` | https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=30&sumula=3338 |
| `stf-sumula-589.txt` | https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=30&sumula=2300 |
| `stf-sumula-668.txt` | https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=30&sumula=1521 |
| `stf-sumula-670.txt` | https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=26&sumula=2218 |
| `stf-sumula-724.txt` | https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=30&sumula=1644 |
| `stf-sv-19.txt` | https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=26&sumula=1248 |
| `stf-tema-94.txt` | https://portal.stf.jus.br/jurisprudenciaRepercussao/verAndamentoProcesso.asp?incidente=2617543&numeroProcesso=586693&classeProcesso=RE&numeroTema=94 |
| `stf-tema-155.txt` | https://portal.stf.jus.br/jurisprudenciaRepercussao/verAndamentoProcesso.asp?incidente=2613544&numeroProcesso=712743&classeProcesso=AI&numeroTema=155 |
| `stf-tema-523.txt` | https://portal.stf.jus.br/jurisprudenciaRepercussao/verAndamentoProcesso.asp?incidente=4178349&numeroProcesso=666156&classeProcesso=RE&numeroTema=523 |
| `stf-tema-1020.txt` | https://portal.stf.jus.br/jurisprudenciaRepercussao/verAndamentoProcesso.asp?incidente=5563078&numeroProcesso=1167509&classeProcesso=RE&numeroTema=1020 |
| `stf-tema-1084.txt` | https://portal.stf.jus.br/jurisprudenciaRepercussao/verAndamentoProcesso.asp?incidente=5813878&numeroProcesso=1245097&classeProcesso=ARE&numeroTema=1084 |

---

## LOTE 4 — STJ súmulas + REsps — 14 itens

> Cole na extensão: "Para cada item, abra a URL. SÚMULA: capture o enunciado. REsp: capture a ementa e,
> se a página abrir o inteiro teor, capture o acórdão. Baixe como `<id>.txt`. Se a página for um formulário
> de busca, digite o número e capture o resultado."

| id (nome do arquivo) | URL oficial |
|---|---|
| `stj-sumula-314.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22314%22.num.&b=SUMU |
| `stj-sumula-392.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22392%22.num.&b=SUMU |
| `stj-sumula-393.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22393%22.num.&b=SUMU |
| `stj-sumula-397.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22397%22.num.&b=SUMU |
| `stj-sumula-399.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22399%22.num.&b=SUMU |
| `stj-sumula-409.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22409%22.num.&b=SUMU |
| `stj-sumula-481.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22481%22.num.&b=SUMU |
| `stj-sumula-614.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22614%22.num.&b=SUMU |
| `stj-sumula-626.txt` | https://scon.stj.jus.br/SCON/sumstj/doc.jsp?livre=%22626%22.num.&b=SUMU |
| `stj-resp-1112646.txt` | https://scon.stj.jus.br/SCON/jurisprudencia/toc.jsp?b=ACOR&livre=(('RESP'.clas.%20e%20@num='1112646')) |
| `stj-resp-1130545.txt` | https://www.stj.jus.br/websecstj/cgi/revista/REJ.cgi/ITA?seq=1098748&nreg=201100996000&dt=20111027&formato=HTML |
| `stj-resp-1202136.txt` | https://scon.stj.jus.br/SCON/jurisprudencia/toc.jsp?b=ACOR&livre=(('RESP'.clas.%20e%20@num='1202136')) |
| `stj-resp-1645832.txt` | https://scon.stj.jus.br/SCON/jurisprudencia/toc.jsp?b=ACOR&livre=(('RESP'.clas.%20e%20@num='1645832')) |
| `stj-resp-1658054.txt` | https://scon.stj.jus.br/SCON/jurisprudencia/toc.jsp?b=ACOR&livre=(('RESP'.clas.%20e%20@num='1658054')) |

---

## LOTE 5 — STJ temas repetitivos — 7 itens

> Cole na extensão: "Para cada item, abra a URL (consulta de tema repetitivo do STJ), capture a TESE
> firmada, a questão submetida e a situação. Baixe como `<id>.txt`."

| id (nome do arquivo) | URL oficial |
|---|---|
| `stj-tema-174.txt` | https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=174&cod_tema_final=174 |
| `stj-tema-262.txt` | https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=262&cod_tema_final=262 |
| `stj-tema-399.txt` | https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=399&cod_tema_final=399 |
| `stj-tema-566.txt` | https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=566&cod_tema_final=566 |
| `stj-tema-1113.txt` | https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=1113&cod_tema_final=1113 |
| `stj-tema-1158.txt` | https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=1158&cod_tema_final=1158 |
| `stj-tema-1350.txt` | https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=1350&cod_tema_final=1350 |

---

## CHECKLIST DE RETORNO (59 arquivos)

Quando a pasta `IPTU-TDC` estiver cheia, devolva-a (commit no repo ou nova sessão). O escritório
ingere cada `.txt` cru sobre o stub `.md`/`.json` correspondente, sobe `status_pipeline` de `bruto`
para `processado` e marca a confiança. **Não precisa vir tudo de uma vez** — pode mandar lote a lote.

- [ ] Lote 1 — Federais (12)
- [ ] Lote 2 — Municipais SP (15)
- [ ] Lote 3 — STF (11)
- [ ] Lote 4 — STJ súmulas + REsps (14)
- [ ] Lote 5 — STJ temas (7)

### Notas de fidelidade
- Os REsps (Lote 4) podem abrir uma LISTA de resultados; clique no acórdão correto (confira o nº do
  recurso) antes de capturar. Se só vier a ementa, está ótimo — capture a ementa.
- Os Temas STF/STJ que ainda estiverem "pendentes de julgamento" — capture o que houver e anote o status.
- Se algum link tiver mudado de endereço no portal, capture pela busca do número e ajuste a URL no `.txt`.
