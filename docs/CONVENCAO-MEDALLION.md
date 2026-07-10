# Convenção Medallion — Potencial Urbano

> 1 página. Só convenção de path. Sem governança por camada.
> E3 · PU 18 · 2026-07-10.

## Três camadas, uma árvore canônica

| Camada | Onde mora | Formato | Regra |
|--------|-----------|---------|-------|
| **Bronze** | Supabase Storage, balde `dados-produto` | Arquivo bruto (CSV/XLSX/SHP) | Imutável. Path: `oficiais/<fonte>/ano=<AAAA[-MM]>/<arquivo>`. sha256 no manifesto. Loader recusa carga sem `ano=` (abort). |
| **Silver** | Postgres, schema **`oficiais.*`** | Tabela tipada com PK + proveniência | UMA árvore canônica. Toda tabela carrega `capturado_em` e vintage por família (ver E2). RLS deny-all. |
| **Gold** | Git, `tabelas/*.csv` + saídas do pipeline | CSV versionado | Derivado de Bronze/Silver. `data_base` + hash no MANIFESTO. Inclui agregações de apresentação (ex.: `data_ref=max()`). |

## Árvore Silver: `oficiais.*`

Schemas canônicos com dado vivo (E6-fase-0):

| Schema | Papel | Tabelas vivas |
|--------|-------|---------------|
| `oficiais` | Dados oficiais do produto (Silver) | `iptu2026_cedentes`, `q14_valor_terreno_2025` |
| `governanca` | Registro de decisões + de-para de proveniência | `de_para`, `registro_decisoes` |

Schemas vazios (`engine`, `geo`, `leis`, `rag`, `tese`, `tabelas`) existem por legado de scaffold — população deliberada em `oficiais.*`, não nesses schemas. Migrations canônicas: 5 vivas em `supabase/migrations/` (E6-fase-0, reconciliadas).

## Convenção de path Bronze

```
dados-produto/oficiais/<fonte>/ano=<AAAA[-MM]>/<arquivo>
```

Exemplos:
- `oficiais/iptu/ano=2026/IPTU_2026.csv`
- `oficiais/q14/ano=2025/Atualizacacao_Q14_anoref2025.csv`
- `oficiais/zepec-bir/ano=2025-08/lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx`

Loader (Apps Script / Colab) emite `ano=` no `dest` — sem ele, a próxima safra sobrescreve a atual.

## O que esta convenção NÃO é

- **Não é governança por camada.** O cemitério de migrations paralelas mostrou que cerimônia excessiva gera artefatos que ninguém aplica. A convenção de path basta.
- **Não é codex/oráculo por camada.** O oráculo dos engines é o CODEX do projeto (raiz). Cada camada segue a mesma doutrina (1.1–1.7).
- **Não é schema de validação por layer.** A validação é do pipeline (Parte 3 do CLAUDE.md): hash no Bronze, schema tipado no Silver, eval no Gold.
