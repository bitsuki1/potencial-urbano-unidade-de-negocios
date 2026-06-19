# Decisões da ARRUMAÇÃO FÍSICA do Drive — POTENCIAL URBANO (IPTU/TDC)

> **Subordinado ao `CODEX-DO-PROJETO.md` (SSOT — RO-17).** O registro canônico
> desta arrumação está no **Codex §7**. Aqui fica o **log operacional detalhado**
> deste sub-task (a arrumação física, que o Codex trata como conforto de navegação
> opcional, gerado sob demanda). IDs `AF-xx` para não colidir com as decisões de
> arquitetura `D-xx` do Codex (§5). Status: ✅ vigente · ↩️ revertida · ⏳ pendente.
> Data base: 2026-06-19.

## Regras de ouro que regem este sub-task (canônicas no Codex)
- **RO-09 — Nada se descarta.** O que sai do plano de movimentação **não é
  apagado** — fica onde está no Drive.
- **RO-11 — Operador não lê documentação.** Orientação sempre na tela, no chat.
- **RO-12 — Trazer tudo → identificar → deduplicar com cuidado; versão NÃO é
  duplicata** (linhagem, RO-14). Dedup por nome+tamanho (Drive não expõe hash),
  confirmando por conteúdo.
- **RO-16 — Mestres de IA são insumo de escrutínio, não fonte da verdade nem lixo.**
- **RO-22 — Toda escolha do operador vem como sugestão pronta** (recomendação na frente).
- **Escopo:** projeto é IPTU/TDC em São Paulo capital — a arrumação física segue isso.

---

## A. O que TRAZER para POTENCIAL URBANO
- **AF-01** ✅ Despejo `01 — _entrada`: organizar na estrutura temática (868 itens
  no plano final).
- **AF-02** ✅ Meu Drive (solto): 65 arquivos do projeto (MOTOR 0-66/0-91, mestre
  TDC, MÓDULO I, CÓDICE MESTRE, BASE_TDC_TOMBADOS, PLANO DE NEGÓCIOS, Estudo
  Profundo IPTU, RAG Gap).
- **AF-03** ✅ Meu Drive / "Google AI Studio": 51 itens (39 prompts/Gens de IA do
  projeto + Modelo Reduzido IPTU + IRRF Tema 1130 + Metodologia + Oportunidade
  Tema 1130). Keepee/profinders/casos do AI Studio ficaram FORA.
- **AF-04** ✅ Meu Drive / MAPAS: 1 arquivo.
- **AF-05** ✅ **8 pastas inteiras** (bloco, sem desmembrar):
  | Pasta | ID | Destino |
  |---|---|---|
  | DataLake_TDC | `1XAUTRln1DK48hVTNwtIEZP3AIqvDZEHN` | 03 — Tabelas & Engines |
  | TODOS TDC | `1uMMvR8_PVjNv3hgDjzpA7fm6yoVOvwYg` | 03 — Tabelas & Engines |
  | IPTU 12-05 | `1rcOIT-Kat1ffXeardlfnQwCx6zpNLxhZ` | 03 — Tabelas & Engines |
  | Colab Notebooks (24) | `1ItQzfFV5WsLHBOrNFmSLU4yvu7RVhV72` | 03 — Tabelas & Engines |
  | IRRF Tema 1130 | `1pVWe46Y3PNrCQkhvOm9x99qY2_ZVi0Ty` | 02 — Leis & Jurisprudência |
  | Novos (64 juris/doutrina IPTU) | `1LGrKx7sY8Jot1b1ROG53mhb-yy-zHQLv` | 02 — Leis & Jurisprudência |
  | dados_pericia1 (DOSP) | `1TpZ8r_YPki0wCaQ9H64Qey9_lQDJqy1p` | 02 — Leis & Jurisprudência |
  | Imagens_Extraidas (84 PNGs) | `1M4T65C4ckrccT8YPXWPYWM3XkuvAqpAW` | 05 — Geo / Mapas |
  (Colab→03, Imagens→05, dados_pericia1→02 foram pedidas pelo operador na rodada v4.)

## B. O que NÃO trazer (RO-09: nada apagado, só fica fora da arrumação)
- **AF-06** ✅ **Certidoes** — 41 "CertidaoDigital_*.pdf": fora, por opção do operador.
- **AF-07** ✅ Não tocar: pastas de colegas (alan/tamires), Particular/Médicos/
  Rotary, Bitsuki/Keepee/ERP, Meet Recordings, backup "Lenovo 2026".
- **AF-08** ✅ **OPÇÃO A** (operador, "só A"): itens fora de pauta IPTU/TDC **nem
  entram** na arrumação — ficam onde estão. Removidos **52 arquivos** do plano:
  16 IA-infra/.md, 20 logs/artefatos, 13 financeiros, 3 de outro projeto
  (Keepee/BNDES, Contrato de Gestão, Guia de Pastas). 1044 → 992.
  - Proteção: o filtro **nunca remove tipo=pasta** (DataLake_TDC tinha sido pego
    por engano pelo regex "datalake"; corrigido — 8 pastas intactas).
  - **ALERTA (RO-16):** os mestres de IA removidos (CONHECIMENTO_MESTRE, oráculos,
    MÓDULO I) são **insumo** da Etapa 1 — só ficaram fora da ARRUMAÇÃO FÍSICA,
    permanecem no Drive. Não confundir "não organizar junto" com "descartar".

## C. Triagem (99)
- **AF-09** ✅ Triagem é zona neutra: o que não for, sem ambiguidade, lei/
  jurisprudência/dado técnico de IPTU/TDC fica lá.
- **AF-10** ✅ Dos 84 que sobraram no 99 após a opção A, **74 eram claramente
  IPTU/TDC** e foram arquivados nas pastas temáticas (sugestão do agente, aprovada):
  2.2 TDC (23), 2.6 Jurisprudência (13), 05 Geo (11), 2.4 Federal (8), 2.1
  Urbanística (8), 2.3 IPTU (7), 2.5 Infralegal (4). Triagem 84 → 10.
- **AF-11** ✅ **10 ficam no 99** (ambíguos): `02-23 Anexo I`, `02-23 Anexo II`,
  `MON.pdf`, `mover_pdfs_STJ.ps1`, `Novo Relatorio SITE 2021`, `Pedido de
  Reconhecimento de Complexo de Saúde`, `vilas operárias (Migliari)`,
  `tabela_2025_Retificado`, `tributario 2`, `Tributario Cidades 2`.

## D. Decisões REVERTIDAS (registradas pra não repetir)
- **AF-12** ↩️ **Pasta "06 — Financeiro"** — proposta e revertida: com escopo só
  IPTU/TDC, financeiro **saiu do plano** (AF-08), não virou pasta nova.
- **AF-13** ↩️ **Plano "v6"** que dobrava 100 itens da Triagem (incluindo IA-infra
  → Governança): **revertido inteiro** após o operador apontar mistura de coisa
  fora de pauta. Lição: não inventar destino temático para item que não é
  claramente IPTU/TDC.
- **AF-14** ↩️ Respostas iniciais "deixar Keepee/logs na Triagem" foram
  **superadas** pela Opção A (AF-08): nem entram (não ficam no 99).

## E. Motor / ferramenta
- **AF-15** ✅ Apps Script que **MOVE** (não copia/duplica), idempotente, com
  ENSAIO (dry-run) e relatório em planilha.
- **AF-16** ✅ **Motor v5**: trocou o lote fixo de 200 (que travava — ensaios do
  operador pararam em 400 e 800 numa corrida, 620 noutra; todos com **0 ERRO**, mas
  nenhum chegou ao FIM — relatórios "Arrumacao_Potencial_Urbano_v2", runs de 21:22
  e 21:47) por **orçamento de tempo** (~4,5 min), flush a cada 25, trava
  `LockService` e auto-reagendamento no `finally`. Retoma até `=== FIM ===`.
- **AF-17** ✅ Relatório renomeado de "...v2" para "...**FINAL**" (sinal visual).

## F. Auditoria (2 sub-agentes, 2026-06-19)
- **AF-18** ✅ **Integridade: PASSOU.** `.gs` == de-para; 992 (984+8); 0 ID
  duplicado/malformado/em-dois-destinos; 8 pastas corretas. (Agente `afbaa6f52bd431bcd`.)
- **AF-19** ✅ **Catalogação: sólida, 0 enquadramentos claramente errados.**
  (Agente `a1046b443dad46153`.) **Achados completos em `AUDITORIA-ACHADOS.md`**
  (30 inconsistências PDF/CSV, grupos de cópias, borderline geosampa).

## G. Pendentes (trazer como sugestão — RO-22)
- **AF-20** ⏳ **Dedup sob RO-12/14/19:** ~59 cópias por nome+pasta (stf-sumula-539
  6×, SIRGAS_SHP_benstombados1 6×, BASE_TDC_v1_3 4×, PLANO DE NEGÓCIOS 3×...).
  **Versão NÃO é duplicata** — confirmar por conteúdo, preservar linhagem; só
  remover cópia idêntica confirmada, **pós-move**, com OK. Não atrapalha o move.
- **AF-21** ⏳ **Pares PDF + CSV** do mesmo doc (lei PDF no 2.x, extração .csv em
  03): parece proposital. Recomendação: **MANTER**.
- **AF-22** ⏳ `Pedido de Reconhecimento de Complexo de Saúde` (99) → recomendo
  **2.1 Urbanística**.
- **AF-23** ⏳ 6 dicionários/metadados **geosampa** em 03 poderiam ir p/ 05 (opcional).
- **AF-24** ⏳ **Acesso Google Drive MCP** não aprovado — destravaria verificação
  ao vivo (e, segundo `engines/FORMULAS-CONSOLIDADAS.md`, resolveria lacunas
  "Drive não lido / read_file_content negado").

## H. Varredura das PASTAS VIVAS do Drive (2026-06-19, acesso liberado)
- **AF-27** ✅ **Mapa de pastas vivo** (dentro de POTENCIAL URBANO `1BrM6q…`):
  | Pasta | ID |
  |---|---|
  | 00 — Governança & Índice | `1zfDGtvhZh1JDUykC6kouDPqm-E3u0bgO` |
  | 00/Prompts & Gens (IA) | `1PvLBgMdl1GJJANKuCx6nW8rBdkFIb6Vh` |
  | 01 — _entrada (despejo) | `1grhqYgttj7KnJmiu9U73z-lXFHnFthov` |
  | 02 — Leis & Jurisprudência | `1GRvv6Xbi3_rKpZvvIqKIjyByu1LgFjmJ` |
  | 02/2.1..2.7 | `1WO6Gyv…`,`1WdUk6Q…`,`1ugoTke…`,`1vOw1BF…`,`1nb5IfA…`,`1Aw4KZC…`,`1bU9Hl7…` |
  | 03 — Tabelas & Engines | `1v4H2YsIZSNDwNXiMtOAV1w1qy-5kOuvy` |
  | 04 — Tese (Antítese/Vacina) | `1xuq1OpJzSYOGWG6dp7xGfCyDVE-WLVas` |
  | **05 — Geo / Mapas** (canônica, vazia) | `1VxXDspnEwYuiCMXjn9-YPp65h3vtb_pr` |
  | **99 — Inbox / Triagem** (canônica, vazia) | `1p8d2Cx-qbLO0nRicRjbZ7h47cp2jqb7t` |
- **AF-28** ✅ **BUG ACHADO E CORRIGIDO.** `_getOrCreateByPath_` fazia `split('/')`.
  As pastas canônicas têm a barra **no próprio nome** (`05 — Geo / Mapas`,
  `99 — Inbox / Triagem`), então o script criava aninhado `05 — Geo › Mapas` e
  `99 — Inbox › Triagem` (errado), deixando as canônicas vazias — no real, os 212
  arquivos de Geo iriam pro lugar errado. **Fix:** `CONFIG.FOLDER_IDS` ancora os
  destinos aos IDs reais; resolver usa o ID direto quando o destino inteiro está
  mapeado (cobre nomes com "/"). 02/2.x continua resolvendo por nome sob o 02 fixo.
- **AF-29** ✅ **Pastas órfãs a remover** (vazias, criadas pelo bug): `05 — Geo`
  (`1uQTkzx2fXGMH1J5zrF_K1yD-NsUxxc1i`, contém sub vazia "Mapas") e `99 — Inbox`
  (`19ERTHqSPsn5pCq6bxTfAhhzaQAyAir2N`, contém sub vazia "Triagem"). **PENDÊNCIA
  DO MOU/escritório** (2026-06-19): operador apaga quando conveniente; **não
  bloqueia o triplo-limpo** (resíduo vazio, fora do plano; agente sem ferramenta
  de deleção no Drive). NÃO confundir com as canônicas
  `05 — Geo / Mapas` (`1VxXDsp…`) e `99 — Inbox / Triagem` (`1p8d2Cx…`), que ficam.
- **AF-30** ✅ Observação: o **ENSAIO (dry-run) já cria as pastas-destino vazias**
  (`_getOrCreateByPath_` roda antes do check de DRY_RUN). Por isso a árvore
  (00, 02/2.1-2.7, Prompts & Gens, etc.) já existe no Drive — esperado, não é erro.

## Composição do plano final (992 itens)
- Origem: 868 despejo `01 — _entrada` · 65 Meu Drive (solto) · 51 AI Studio ·
  7 Meu Drive (pasta) · 1 MAPAS.
- Por destino: ver **ESTRUTURA.md**. Fonte da verdade dos IDs: **de-para-final.csv**.
- Contexto: o inventário de ENTRADA (1.398 itens, `inventario/de-para-entrada.csv`)
  é o universo de onde este recorte de 992 foi reorganizado.

## Nota de escopo do artefato De/Para
- **AF-25** ✅ O `de-para-final.csv` deste sub-task é um **localizador simples**
  (drive_id→destino) para a movimentação física. O **livro-razão completo da
  RO-14** (vigência · linhagem substitui/substituído-por · proveniência · o que
  foi aproveitado) é artefato da **Etapa 1 / Fase 0 canônica**, não deste sub-task.
  Não confundir os dois De/Para.
- **AF-26** ✅ Distinção de escopo na IA: os **39 prompts/Gens do AI Studio** entram
  (são produto de trabalho sobre IPTU/TDC), enquanto os **mestres de IA-infra** (.md
  ORACULO/MANIFESTO/CONHECIMENTO) ficam fora da arrumação física (RO-16: insumo, no
  Drive). Critério: conteúdo de pauta entra; tubulação de pipeline não é organizada.
