# CIT / CONPRESP — captura OFICIAL de tombamento por SQL (fonte primária, 1.7/1.8)

> **Fonte:** CIT — Cadastro de Imóveis Tombados, sistema oficial do Departamento do Patrimônio Histórico (DPH) /
> Conpresp — Secretaria Municipal de Cultura e Economia Criativa de São Paulo. `http://www3.prefeitura.sp.gov.br/cit/`
> **Captura:** 2026-07-18, via navegador autenticado do MOU (extensão Claude, IP-BR) — consulta por SQL.
> **Natureza (1.8):** OFICIAL PRIMÁRIA re-extraída do sistema-fonte (NÃO é espelho, NÃO é derivado). Pode alimentar
> o corpus e a camada de conservação (Art. 129). O número/ato nasce daqui, rastreável ao sistema oficial.
> **Limite declarado pelo próprio sistema (verbatim):** "O RESULTADO DA PESQUISA NÃO INDICA A EMISSÃO DE DOCUMENTO
> OFICIAL. Caso seja necessária a emissão de um documento oficial (...) você deverá se dirigir aos órgãos
> competentes (...). Os pedidos (...) deverão ser protocolados através de processo, na Avenida São João, 473,
> 7º andar - das 10 às 16 horas." → a CONSULTA confirma o tombamento; o ATESTADO/CERTIDÃO físico exige protocolo
> presencial (ação do dono, por negócio — não é raspável).

## Resumo estruturado (5 imóveis — todos TOMBADO)
| SQL | Endereço | Nível | Atos de tombamento (resoluções) | Órgão | Denominação |
|---|---|---|---|---|---|
| 020.067.0033 | R. Dr. Cândido Espinheira, 449 (Perdizes) | TOMBADO | RES. 28/18 (Quadro I item 11); RES. 11/11 (APT) | Municipal (CONPRESP) | — |
| 020.036.0016 | R. Parintins, 120 (Perdizes) | TOMBADO | RES. 28/18 (Quadro I item 4); RES. 23/16 (APT ZEPEC) | Municipal (CONPRESP) | — |
| 021.028.0059 | R. Dona Germaine Burchard, 458 (Perdizes) | TOMBADO | RES. 28/18 (Art.1º Quadro I item 26); RES. 11/11 (Anexo I item 21); RES. SC 25/96 (área envoltória CONDEPHAAT — Parque Água Branca) | Municipal (CONPRESP) + Estadual (CONDEPHAAT) | Conjunto de edificações no bairro de Perdizes |
| 009.019.0006 | Al. Joaquim Eugênio de Lima, 164 (Bela Vista) | TOMBADO | RES. 22/02 (Anexo I item 531); RES. 03/22 (ajuste da 22/02 — muros/encostas R. Alm. Marques de Leão; DOC 25.06.2022) | Municipal (CONPRESP) | Bairro da Bela Vista |
| 009.021.0039 | R. Treze de Maio, 734 (Bela Vista) | TOMBADO | RES. 22/02 (Anexo I item 610) | Municipal (CONPRESP) | Bairro da Bela Vista |

## Extrato VERBATIM (preservado exatamente como retornado pelo CIT)

### IMÓVEL 1 — SQL 020.067.0033 — Rua Dr. Cândido Espinheira, 449 — Perdizes
- Código do IPTU (Setor/Quadra/Lote/Dac): 020.067.0033-2
- Nível de preservação: **TOMBADO**
- Atos (verbatim): "RES. 28/18 - TOMBAMENTO IMOVEIS NO BAIRRO DE PERDIZES (QUADRO I - ITEM 11); RES. 11/11 - APT IMOVEIS NO BAIRRO DE PERDIZES"
- Endereço secundário: CANDIDO ESPINHEIRA 445, 449, RUA DOUTOR
- Endereço Oficial (IPTU): R DR CANDIDO ESPINHEIRA, 00445 | Complemento: 449
- Sub-Prefeitura: Subprefeitura da Lapa
- Situação: IPTU ATIVO
- Órgão: Municipal (CONPRESP)
- Link do PDF da resolução: (não consta — o CIT não disponibiliza o PDF, só cita o número)

### IMÓVEL 2 — SQL 020.036.0016 — Rua Parintins, 120 — Perdizes
- Código do IPTU: 020.036.0016-7
- Nível de preservação: **TOMBADO**
- Atos (verbatim): "RES. 28/18 - TOMBAMENTO IMOVEIS NO BAIRRO DE PERDIZES (QUADRO I - ITEM 4); RES. 23/16 - APT DOS IMOVEIS INDICADOS PELA POPULACAO COMO ZEPEC"
- Endereço secundário: PARINTINS 120, R. C/ MARTA S/N, R.
- Endereço Oficial (IPTU): R PARINTINS, 00120
- Sub-Prefeitura: Subprefeitura da Lapa
- Situação: IPTU ATIVO
- Órgão: Municipal (CONPRESP)

### IMÓVEL 3 — SQL 021.028.0059 — Rua Dona Germaine Burchard, 458 — Perdizes
- Código do IPTU: 021.028.0059-8
- Nível de preservação: **TOMBADO**
- Atos (verbatim): "RES. 28/18 - TOMBAMENTO, PELO CONPRESP, DE CONJUNTO DE EDIFICAÇÕES NO BAIRRO DE PERDIZES (ART. 1º - QUADRO I - ITEM 26); RES. 11/11 - ABERTURA DE PROCESSO DE TOMBAMENTO, PELO CONPRESP, DE CONJUNTO DE EDIFICAÇÕES NO BAIRRO DE PERDIZES (ANEXO I - ITEM 21); RES. SC 25/96 - ÁREA ENVOLTÓRIA, PELO CONDEPHAAT, DO PARQUE DOUTOR FERNANDO COSTA OU PARQUE DA ÁGUA BRANCA, RESTAURADA POR LIMINAR JUDICIAL"
- Endereço secundário: GERMAINE BURCHARD 458, RUA DONA
- Denominação: CONJUNTO DE EDIFICAÇÕES NO BAIRRO DE PERDIZES
- Endereço Oficial (IPTU): R DONA GERMAINE BURCHARD, 00458
- Sub-Prefeitura: Subprefeitura da Lapa
- Situação: IPTU ATIVO
- Órgão: Municipal (CONPRESP) + Estadual (CONDEPHAAT, área envoltória)

### IMÓVEL 4 — SQL 009.019.0006 — Alameda Joaquim Eugênio de Lima, 164 — Bela Vista
- Código do IPTU: 009.019.0006-0
- Nível de preservação: **TOMBADO**
- Atos (verbatim): "RES. 22/02 - TOMB. DO BAIRRO DA BELA VISTA (ANEXO I - ITEM 531); RES. 03/22 - AJUSTAMENTO E DETALHAMENTO DA RESOLUCAO 22/02 QUANTO AS DIRETRIZES RELATIVAS AOS MUROS E ENCOSTAS NA RUA ALMIRANTE MARQUES DE LEAO - INCLUI ALTERACOES NOS ARTIGOS 3º, 7º, 9º (PUBLICACAO NO DOC DE 25.06.2022, P. 22 e 23)"
- Endereço secundário: JOAQUIM EUGENIO DE LIMA 164, AL. C/ FRANCESES 518, R. DOS
- Denominação: BAIRRO DA BELA VISTA
- Endereço Oficial (IPTU): AL JOAQUIM EUGENIO DE LIMA, 00164
- Sub-Prefeitura: Subprefeitura da Sé
- Situação: IPTU ATIVO
- Órgão: Municipal (CONPRESP)

### IMÓVEL 5 — SQL 009.021.0039 — Rua Treze de Maio, 734 — Bela Vista
- Código do IPTU: 009.021.0039-4
- Nível de preservação: **TOMBADO**
- Atos (verbatim): "RES. 22/02 - TOMB. DO BAIRRO DA BELA VISTA (ANEXO I - ITEM 610)"
- Endereço secundário: TREZE DE MAIO 734, R.
- Denominação: BAIRRO DA BELA VISTA
- Endereço Oficial (IPTU): R TREZE DE MAIO, 00734 | Bairro: BELA VISTA
- Sub-Prefeitura: Subprefeitura da Sé
- Situação: IPTU ATIVO
- Órgão: Municipal (CONPRESP)

## Observação oficial do sistema (verbatim, repetida em toda consulta)
"O RESULTADO DA PESQUISA NÃO INDICA A EMISSÃO DE DOCUMENTO OFICIAL. Caso seja necessária a emissão de um documento
oficial sobre as informações contidas no Cadastro, você deverá se dirigir aos órgãos competentes com a documentação
necessária. Dúvidas deverão ser esclarecidas com as respectivas Subprefeituras e/ou CONPRESP (quando for o caso).
Os pedidos de licença e/ou informações deverão ser protocolados através de processo, na Avenida São João, 473,
7º andar - das 10 às 16 horas."

---
> **Alavanca descoberta:** o CIT é consultável **por SQL** e retornou os 5 sem captcha. Se o CIT abrir do runner
> `brasil` (IP-BR), dá para confirmar tombamento + capturar os atos (resoluções) de **TODOS os 4.360 cedentes** em
> lote — vira a base legal (qual resolução tomba cada um) da camada de conservação/Art.129. A avaliar (passo-1 sonda).
