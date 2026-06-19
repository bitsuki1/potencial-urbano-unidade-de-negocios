# Arrumar o Drive — Potencial Urbano (IPTU/TDC) · FINAL

> **Plano final: 992 itens (984 arquivos + 8 pastas).** Escopo: **só IPTU/TDC**
> (52 itens fora de pauta foram retirados — opção A). Documentos irmãos:
> **DECISOES.md** (todas as decisões), **HANDOFF.md** (registro + próximos passos),
> **ESTRUTURA.md** (árvore final).

## Motor (v5) — roda sozinho até o fim
Trabalha por **tempo** (~4,5 min por execução, abaixo do limite de 6 min do Apps
Script), grava progresso a cada 25 itens e **se reagenda sozinho** (a cada ~1 min)
até gravar `=== FIM. 992 itens. ===`. Trava contra execução dupla; idempotente
(item já no lugar vira `JA_OK`); se você fechar o navegador, continua pelos
gatilhos. Recomeçar do zero: `resetProgresso`.

> Se um relatório parar antes do `=== FIM ===`, **clique ▶ Executar de novo** —
> ele retoma de onde parou e **nunca duplica**.

## O que ele faz
- **(A) Organiza** os **868** arquivos do despejo `01 — _entrada` na estrutura temática.
- **(B) Traz** do "Meu Drive" o material do projeto que estava solto:
  - **65** arquivos soltos (MOTOR 0-66/0-91, mestre TDC, MÓDULO I, CÓDICE MESTRE,
    BASE_TDC_TOMBADOS, PLANO DE NEGÓCIOS, Estudo Profundo IPTU, RAG Gap).
  - **51** do "Google AI Studio" (39 prompts/Gens de IA + Modelo Reduzido IPTU +
    IRRF Tema 1130 + Metodologia + Oportunidade Tema 1130). **1** de MAPAS.
  - **8 pastas inteiras**:
    - → **03 Tabelas**: DataLake_TDC, TODOS TDC, IPTU 12-05, Colab Notebooks (24).
    - → **02 Leis**: IRRF Tema 1130, **Novos** (64 juris/doutrina IPTU), dados_pericia1 (DOSP).
    - → **05 Geo**: Imagens_Extraidas (84 PNGs de mapas).

**Fora do plano (opção A — só IPTU/TDC):** 52 arquivos fora de pauta (IA-infra/.md,
financeiros, Keepee/BNDES, logs/artefatos) e **Certidoes** NÃO entram.
**Não toca em:** colegas (alan/tamires), Particular/Médicos/Rotary, Bitsuki/Keepee/
ERP, Meet Recordings, backup Lenovo 2026.

## Arquivos deste pacote
- `Arrumar-Drive-PotencialUrbano.gs` — o script (motor v5, plano 992). Cole inteiro.
- `de-para-final.csv` — **fonte da verdade** (992 linhas: drive_id, titulo, destino, origem, tipo).
- `auditar-relatorio.py` — confere o relatório de saída vs o plano.
- `triagem-classificar.py` / `triagem-sugestoes.csv` — histórico da triagem.
- `DECISOES.md` · `HANDOFF.md` · `ESTRUTURA.md`.

## Estrutura de destino (dentro de POTENCIAL URBANO)
```
00 — Governança & Índice                 34
   Prompts & Gens (IA)                   39
02 — Leis & Jurisprudência                6   (+ pastas: IRRF Tema 1130, Novos, dados_pericia1)
   2.1 Urbanística (PDE-LPUOS-COE)        58
   2.2 TDC-Patrimônio-ZEPEC             159
   2.3 IPTU-Tributário Municipal         63
   2.4 Federal e Constituição            24
   2.5 Infralegal                        66
   2.6 Jurisprudência                    92
   2.7 Doutrina-Estudos-Avaliação        57
03 — Tabelas & Engines                  172   (+ pastas: DataLake_TDC, TODOS TDC, IPTU 12-05, Colab)
05 — Geo / Mapas                        212   (+ pasta: Imagens_Extraidas)
99 — Inbox / Triagem                     10   (ambíguos — você decide depois)
```

## Como rodar
1. **script.google.com** → seu projeto → cole o `.gs` inteiro.
2. `DRY_RUN: true`. Rode **`resetProgresso`** (zera ensaios antigos) e depois
   **`arrumarDrive`** (autorize o Drive na 1ª vez).
3. Abra a planilha **"Arrumacao Potencial Urbano FINAL — …"**. Confira a coluna
   `status` (tudo `PLANEJADO`, nada movido). Se não terminou no
   `=== FIM. 992 itens. ===`, rode `arrumarDrive` de novo até fechar.
4. Aprovou (0 `ERRO`)? → `resetProgresso`, mude `DRY_RUN: false`, rode
   `arrumarDrive`. Move de verdade (`MOVIDO`/`PASTA_MOVIDA`/`JA_OK`), até o FIM.
5. Conferir: `python3 auditar-relatorio.py <relatorio.csv>`.

## Conferência automática
`auditar-relatorio.py` cruza o relatório com `de-para-final.csv` e dá veredito
"COMPLETO" só com **992 itens, 0 erro e a linha `=== FIM ===`** — listando o que
faltou, ERROs, destino divergente e o que ficou na Triagem.
