# HANDOFF — Arrumação FÍSICA do Drive "POTENCIAL URBANO" (IPTU/TDC)

> **Runbook + próximos passos** deste sub-task. Para o próximo Claude ou para o
> Eduardo retomar. Branch: `claude/exciting-tesla-rwyzks` — tudo commitado/pushado.
>
> **SSOT = `CODEX-DO-PROJETO.md` (RO-17).** Registro canônico no **Codex §7**;
> decisões detalhadas em `DECISOES.md` (AF-xx). Este sub-task é o que o Codex §7
> chama de arrumação física opcional (conforto de navegação), gerada sob demanda.

---

## 1. Objetivo
Organizar a pasta **POTENCIAL URBANO** no Google Drive, trazendo o material
espalhado e arrumando o despejo `01 — _entrada` numa estrutura temática.
A ferramenta é um **Google Apps Script** que MOVE (não copia, não duplica) os
arquivos para as pastas-destino, com ensaio (dry-run), relatório e retomada.

`PROJECT_ROOT_ID` (pasta POTENCIAL URBANO) = `1BrM6q36meTtn5guJoiGbqvCtZF11Uau3`

## 2. REGRAS DE OURO (canônicas no Codex — aplicadas aqui)
- **RO-09** nada se descarta · **RO-11** orientação na tela · **RO-12** versão não
  é duplicata · **RO-16** mestres de IA são insumo · **RO-22** sugestão pronta.
- **Escopo:** organização **só da pauta IPTU/TDC** (decisão "só A"); nada fora de
  pauta entra (IA-infra, financeiro, outro projeto, logs) — e nada é apagado (RO-09).

## 3. Estado FINAL do plano — 992 itens (984 arquivos + 8 pastas)
| Itens | Destino |
|---:|---|
| 34 | 00 — Governança & Índice |
| 39 | 00 — Governança & Índice/Prompts & Gens (IA) |
| 6 | 02 — Leis & Jurisprudência (raiz) |
| 58 | 02 .../2.1 Urbanística (PDE-LPUOS-COE) |
| 159 | 02 .../2.2 TDC-Patrimônio-ZEPEC |
| 63 | 02 .../2.3 IPTU-Tributário Municipal |
| 24 | 02 .../2.4 Federal e Constituição |
| 66 | 02 .../2.5 Infralegal |
| 92 | 02 .../2.6 Jurisprudência |
| 57 | 02 .../2.7 Doutrina-Estudos-Avaliação |
| 172 | 03 — Tabelas & Engines |
| 212 | 05 — Geo / Mapas |
| 10 | 99 — Inbox / Triagem (ambíguos, decisão manual depois) |

**8 pastas inteiras** trazidas como bloco: DataLake_TDC, TODOS TDC, IPTU 12-05,
IRRF Tema 1130, Novos, Colab Notebooks (→03), Imagens_Extraidas (→05),
dados_pericia1 (→02). **Certidoes** ficou FORA por opção do usuário.

## 4. Arquivos deste pacote (`drive-arrumacao/`)
- **`Arrumar-Drive-PotencialUrbano.gs`** — o script. Cole inteiro no
  script.google.com. Contém `PLAN_FILES` + `PLAN_FOLDERS` (= os 992 destinos).
- **`de-para-final.csv`** — FONTE DA VERDADE (drive_id, titulo, destino, origem,
  tipo). O `.gs` reflete isso exatamente (auditado, ver §7).
- **`auditar-relatorio.py`** — confere o CSV de saída do script contra o de-para.
  Uso: `python3 auditar-relatorio.py <relatorio.csv>`. Dá veredito "COMPLETO"
  só com 992 itens, 0 erro e linha `=== FIM ===`.
- **`triagem-classificar.py`** + **`triagem-sugestoes.csv`** — ferramenta/saída da
  pré-classificação da Triagem (histórico do raciocínio).
- **`ESTRUTURA.md`** — mapa da árvore final. **`INSTRUCOES.md`** — como usar.

## 5. Como o MOTOR funciona (v5)
- Roda por **orçamento de tempo** (`TIME_BUDGET_MS` ~4,5 min), abaixo do limite de
  6 min do Apps Script. Grava progresso a cada 25 itens (`FLUSH_CADA`).
- **Retoma sozinho**: guarda `cursor` em ScriptProperties e reagenda gatilho a
  cada ~1 min (no `finally`, à prova de falha). Trava com `LockService` (sem
  execução dupla). **Idempotente**: item já no destino vira `JA_OK`.
- Função principal: **`arrumarDrive`**. Reset total: **`resetProgresso`**
  (zera cursor, reportId e gatilhos). Relatório = planilha nova chamada
  "**Arrumacao Potencial Urbano FINAL — <data>**". Termina com `=== FIM. 992 itens. ===`.
- `CONFIG.DRY_RUN`: `true` = ENSAIO (só lista, status PLANEJADO). `false` = MOVE
  de verdade (status MOVIDO/PASTA_MOVIDA/JA_OK).

## 6. Linha do tempo das decisões
- v2→v4: montado o plano e trazidas pastas a pedido (Colab→03, Imagens→05,
  dados_pericia1→02). Certidoes fora.
- v5: reescrita do motor (parava no meio antes; agora vai até o FIM sozinho).
- **Escopo A**: removidos do plano **52 arquivos fora de pauta** (16 IA-infra/.md,
  20 logs/artefatos, 13 financeiros, 3 outro projeto). 1044 → 992. As 8 pastas
  foram PROTEGIDAS (nunca remove tipo=pasta — DataLake_TDC tinha sido pego por
  engano pelo regex "datalake"; corrigido).
- **Triagem refinada**: dos 84 que sobraram no 99, **74 eram claramente IPTU/TDC**
  e foram arquivados nas pastas temáticas (2.1-2.6, 05). Triagem 84 → 10.

## 7. Auditoria (2 sub-agentes, 2026-06-19) — APROVADO
- **Integridade:** PASSOU. `.gs` == de-para exatamente; 992 (984+8); 0 ID
  duplicado, 0 malformado, 0 ID em dois destinos; 8 pastas corretas.
- **Catalogação:** sólida. **0 enquadramentos claramente errados.**
- **Achados (não aplicados):**
  - **~59 cópias por nome+pasta** (stf-sumula-539 6×, SIRGAS_SHP_benstombados1 6×,
    BASE_TDC_v1_3 4×, PLANO DE NEGÓCIOS 3×...). Não atrapalha o move. **Sob RO-12:
    versão NÃO é duplicata** — confirmar por conteúdo e preservar linhagem (RO-14).
    Só remover cópia **idêntica confirmada**, pós-move, com OK do operador.
  - **Pares PDF+CSV** do mesmo doc (lei em PDF no 2.x, extração .csv em 03): parece
    proposital → recomendação MANTER.
  - 6 dicionários geosampa em 03 poderiam ir p/ 05 (borderline, opcional).

## 8. PENDÊNCIAS / próximos passos
1. **[USUÁRIO]** Rodar o ENSAIO da versão FINAL até o relatório fechar em
   `=== FIM. 992 itens. ===` com **0 ERRO**. (Estava rodando; último relatório
   chegou a 620 do plano ANTIGO de 1044 — descartar, rodar a FINAL com
   `resetProgresso` antes.) Regra: enquanto não tiver FIM, clicar ▶ Executar de
   novo (retoma, nunca duplica).
2. **[CLAUDE]** Receber o CSV do FIM → rodar `auditar-relatorio.py` → dar veredito.
3. **[USUÁRIO]** Aprovado o ensaio → trocar `DRY_RUN: false`, `resetProgresso`,
   `arrumarDrive` → MOVE de verdade.
4. **[CLAUDE, pós-move]** Auditar o CSV real (MOVIDO/JA_OK); preparar lista de
   deduplicação (59 cópias) se o usuário quiser.
5. **Decisões abertas (trazer como sugestão):** aplicar `Pedido de Reconhecimento
   de Complexo de Saúde` → 2.1 Urbanística (recomendado); deduplicação pós-move.
6. **Desbloqueio disponível:** acesso ao **Google Drive MCP** não foi aprovado.
   Com ele dá pra verificar AO VIVO (pastas-fonte, árvore, e o move real).

## 9. Os 10 itens que ficam na Triagem (99) — ambíguos de propósito
`02-23 Anexo I` · `02-23 Anexo II` · `MON.pdf` · `mover_pdfs_STJ.ps1` (script) ·
`Novo Relatorio SITE 2021` · `Pedido de Reconhecimento de Complexo de Saúde`
(candidato a 2.1) · `vilas operárias (Migliari)` · `tabela_2025_Retificado` ·
`tributario 2` · `Tributario Cidades 2`.
