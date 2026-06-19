# Estrutura do Drive — POTENCIAL URBANO (IPTU / TDC) · FINAL

Mapa da organização aplicada (motor v5, escopo A). Total: **992 itens**
= 984 arquivos + 8 pastas inteiras. **Escopo: só pauta IPTU/TDC** — itens fora de
pauta (IA-infra, financeiro, outro projeto, logs) foram retirados do plano.

## Árvore final (contagem planejada)

```
POTENCIAL URBANO/
├── 00 — Governança & Índice .............................. 34
│   └── Prompts & Gens (IA) ............................... 39
├── 02 — Leis & Jurisprudência ........................... 6  (+3 pastas inteiras)
│   ├── 2.1 Urbanística (PDE-LPUOS-COE) .................. 58
│   ├── 2.2 TDC-Patrimônio-ZEPEC ........................ 159
│   ├── 2.3 IPTU-Tributário Municipal ................... 63
│   ├── 2.4 Federal e Constituição ...................... 24
│   ├── 2.5 Infralegal .................................. 66
│   ├── 2.6 Jurisprudência .............................. 92
│   └── 2.7 Doutrina-Estudos-Avaliação .................. 57
├── 03 — Tabelas & Engines .............................. 172 (+4 pastas inteiras)
├── 05 — Geo / Mapas .................................... 212 (+1 pasta inteira)
└── 99 — Inbox / Triagem ................................ 10
```

> **Pastas inteiras (8):** DataLake_TDC, TODOS TDC, IPTU 12-05, IRRF Tema 1130,
> Novos, Colab Notebooks (→03), Imagens_Extraidas (→05), dados_pericia1 (→02).
> **Certidoes** ficou fora por opção do usuário.

> Também existem no root do projeto, mas **não são destino de movimentação**:
> `01 — _entrada` (o despejo de origem) e `04 — Tese (Antítese/Vacina)` (Etapa 1,
> ainda a forjar). Ver Codex §7.

## O que cada pasta guarda
- **00 — Governança & Índice** — documentos-mestre do projeto (PLANO DE NEGÓCIOS,
  BASE_TDC, MOTOR, CÓDICE, MÓDULO I) e, em *Prompts & Gens (IA)*, material do AI Studio.
- **02 — Leis & Jurisprudência** — base legal e decisória por tema (urbanística,
  TDC/patrimônio, IPTU, federal, infralegal, jurisprudência, doutrina/avaliação).
- **03 — Tabelas & Engines** — planilhas, bases e notebooks de cálculo.
- **05 — Geo / Mapas** — shapefiles (SIRGAS), camadas geográficas, mapas e quadros.
- **99 — Inbox / Triagem** — 10 itens ambíguos, sem assinatura temática clara.
  Revisão manual depois — nada se perde.

## Itens FORA de pauta (não entram no projeto — opção A)
52 arquivos removidos do plano (ficam onde estão no Drive do usuário): 16 IA-infra
(.md ORACULO/MANIFESTO/CONHECIMENTO/RAG), 20 logs/artefatos de download, 13
financeiros (Balanço mensal/FUNDURB), 3 de outro projeto (Keepee/BNDES, Contrato,
Guia de Pastas).

## Conferir o resultado
Depois do `=== FIM. 992 itens. ===`:
`python3 auditar-relatorio.py <relatorio.csv>` → diz se faltou algo, ERRO, destino
divergente e o que ficou na Triagem.
