# Fase B — Descoberta de Dono em Escala (runbook)

> **Objetivo:** identificar o **proprietário** (pessoa física controladora) dos ~599 cedentes prontos —
> hoje só ~19 têm dono. **Fase A** (dados oficiais) monta a base; **Fase B** (dados adquiridos) só
> ENRIQUECE por cima (D-DONO-6). Este documento é o mapa para a próxima instância rodar quando o
> dado pesado chegar. **O núcleo (o JOIN) já está construído e no gate** — falta só o dado.

## O que já está PRONTO (construído e gated, 2026-07-10)
- **`zepec/resolver_dono.py`** — o motor do JOIN: sobe a cadeia de titularidade e grava
  `zepec/limpo/donos_encontrados.csv` (mesmo schema de 5 colunas que `donos.py`; `montar_ferramenta.py`
  consome sem mudança). Determinístico, anti-loop, fail-closed (sem documento → sem dono).
- **`evals/ground-truth/fase-b-fixture/`** — fixture SINTÉTICO (CPF/CNPJ/nomes FICTÍCIOS): PF direta,
  PJ→sócio, holding em 2 níveis, conflito, documento ausente.
- **`evals/eval-fase-b.py`** — prova a cadeia sobre o fixture (no `consolidar.yml` + `fechar-instancia.py`).
  Fica VERDE sem os 5,7 GB e sem PII (passa o PII probe, que só varre `zepec/limpo|oficial|raw`).

## A cadeia de titularidade (o JOIN)
```
SQL (IPTU_2026) → contribuinte + documento(CPF/CNPJ)
   ├─ CPF  → pessoa física direta (o próprio contribuinte)
   └─ CNPJ → empresas(razão social) → socios(CNPJ→sócio)
                                        ├─ sócio CPF  → pessoa física controladora
                                        └─ sócio CNPJ → holdings (recursão até a PF no topo)
   ITBI (2006–2024) confirma transação recente.
```
Chave de entrada = **`sql_mestre` 10 dígitos** (setor3+quadra3+lote4), a mesma de `donos.py`/`enriquecer_oficial.py`.

## O dado pesado (de-para) — fonte: `docs/INVENTARIO-DRIVE-IPTU-TDC.md` (com os Drive-IDs)
| Arquivo | ~Tamanho | O que é |
|---|---|---|
| `socios.csv` | 3,44 GB | quadro societário (Receita Federal): CNPJ → sócios |
| `empresas.csv` | 2,27 GB | cadastro CNPJ → razão social |
| `holdings.csv` | 60 MB | controle societário (CNPJ → CNPJ) |
| `iptu-2020-cep01.csv` | 153 MB | histórico (Fase B — não ingerir antes) |
| ITBI 2006–2024 | — | confirma transação recente |

As 4 canônicas vivem no Drive em **"03 — Tabelas & Engines"** (verificadas fora da quarentena de dedup).

## O GATE DE SEGURANÇA (PD-7) — antes de carregar qualquer PII
DoD (registrado FECHADO em `D-SEG-01`, migration `20260703172052`): **spend cap ON · bucket PII privado ·
RLS deny-all provado (curl anônimo → 403; SELECT anon = 0) · rotação de chave**. (D-DONO-17b/D106 tiram a
Fase B do caminho crítico — repo privado/uso único — mas o mecanismo RLS deny-all PERMANECE.)

## Ordem de execução (quando o dado chegar)
1. **Subir** o pesado (Colab `zepec/subir-grandes-colab.py` ou rclone `scripts/transferir-pesados-drive-supabase.md`)
   ao bucket **privado** `dados-produto`, prefixo `dados-pii/` — projeto Supabase `csnalylpvysjvejgsymr` (só este, D-DONO-18).
2. **Recortar** (padrão de `filtro_iptu.py` = `curl url-assinada | filtro`, só os documentos dos cedentes → CSVs pequenos em `zepec/oficial/`):
   - `filtro_contribuinte.py` — extrai `sql_mestre + contribuinte + documento(CPF/CNPJ)` do IPTU_2026 → `iptu_contribuinte.csv`.
     ⚠️ **A construir:** `filtro_iptu.py` hoje mapeia só até a col 25 de 29 e NÃO extrai o nome/documento do contribuinte;
     confirmar o layout das colunas 26–29 do IPTU_2026 (INVENTARIO:239) antes de codar — **não inventar coluna** (1.3).
   - `filtro_empresas.py` / `filtro_socios.py` / `filtro_holdings.py` — recorte por documento → `{empresas,socios,holdings}.csv`.
3. **Resolver:** `python3 zepec/resolver_dono.py --base zepec/oficial` → `donos_encontrados.csv` (PII, gitignored).
4. **`make pipeline`** (o `montar_ferramenta` injeta `proprietario`/`fonte_dono`; `funil.py` mostra "com dono" subir de ~19 → centenas).
5. O `eval-fase-b.py` vira **trava de regressão** da cadeia.

## Schema Supabase (aplicar SÓ sob o gate PD-7)
Promover `supabase/migrations/_nao-aplicadas-receptor/20260624_010_produto_estrutura.sql` a migration viva
`dados.*` com RLS **deny-all**: `dados.iptu_contribuinte(sql_mestre PK, contribuinte, documento)`,
`dados.empresas(cnpj PK, razao_social)`, `dados.socios(cnpj, doc_socio, nome_socio)`,
`dados.holdings(cnpj, controlada)` + `capturado_em`/proveniência; view Gold `dados.dono_por_sql` = o JOIN da cadeia.

## Restrições (invioláveis)
- **PII fora do git** (`.gitignore`: `donos_encontrados.csv`). Exceção só `zepec/ferramenta/` (proprietário esperado, D-DONO-17).
- **Supabase SÓ `csnalylpvysjvejgsymr`** (D-DONO-18; nunca `gestao-integrada-dados`/`lbjudeifksyeqminwlto`).
- **LGPD/postura (D106/D-DONO-17b):** risco aceito para uso próprio; RLS deny-all é mecanismo, não bloqueio.
- **DoD da Fase B:** resolver o dono de uma fração alta dos 599 (meta a fechar com o dono) — medir e reportar, nunca inventar.
