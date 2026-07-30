# C1 — Migração motor-a-motor para o Supabase (estado vivo)

> Frente aprovada pelo dono (2026-07-23 "arranca C1"; 2026-07-30 "modo autônomo até o término de tudo ao seu
> alcance"). Projeto Supabase: **`potencial-urbano-iptu-tdc`** (`csnalylpvysjvejgsymr`, sa-east-1, PostGIS).
> Ordem do plano: **base/canonicidade → Motor 3 (dados) → Motor 4 (junção/chave) → Motor 0 → Motor 2 (mapa) →
> Motor 1 (RAG)**. Front-end v1 no Lovable por último.

## 🔒 Fronteira de PII (trava fora do meu alcance)
- **Motor 3 (dados legais)** e o corpus são **SEM PII** → migram autonomamente.
- **Motor 4 = junção dos cedentes** carrega **nome/CPF** → **NÃO migra sem consentimento do dono** (é o gate da
  Fase-B). O RLS já fica ligado em tudo; a v1 é papel único (dono), sem mascaramento (decisão D-DONO 2026-07-23).
- **Credencial de poder total** (service_role / connection string do Postgres) **não vive no git** (cofre D106):
  fica em GitHub Secret / painel. O loader lê `SUPABASE_DB_URL` do ambiente.

## Motor 3 — base de dados legal (schema `motor3`)
**19 tabelas de referência (100% oficiais, rastreáveis ao dispositivo/lei; 1.1/1.3/1.7).**

### ✅ Já LIVE no Supabase (carregadas via MCP)
| Tabela | Linhas | Fonte |
|---|---|---|
| `motor3.iptu_aliquota_base` | 3 | `tabelas/iptu-aliquota-base.csv` |
| `motor3.iptu_aliquota_faixa` | 15 | `tabelas/iptu-aliquotas-faixa.csv` (faixas do adicional, nominais 2013) |
| `motor3.iptu_isencao_faixa` | 2 | `tabelas/iptu-isencao-faixa.csv` (vintages 2022/2026) |
| `motor3.iptu_atualizacao_anual` | 14 | `tabelas/iptu-atualizacao-anual.csv` (série 2013–2026) |

### ⏳ Schema criado (DDL aplicada), dado carrega via Action `carregar-supabase`
As 15 tabelas genéricas `motor3.t_<nome>` (fatores TDC, Fi, IPCA, obsolescência, valor de construção, limiar de
parque, Q14 reajuste, **Q14 valor de terreno = 6.715 linhas**, quadros 2A/3/5/6/7). Schema já existe; o **dado**
carrega pelo loader determinístico.

## Ferramentas (reutilizáveis)
- **`scripts/carregar_tabelas_supabase.py`** — loader idempotente (TRUNCATE+INSERT) das 15 tabelas genéricas a
  partir de `tabelas/*.csv`. `--dry-run` valida sem gravar. Lê `SUPABASE_DB_URL` do ambiente.
- **`.github/workflows/carregar-supabase.yml`** — Action de disparo manual que roda o loader.

## ▶️ Passo do dono (uma vez) para completar o Motor 3
Setar o secret **`SUPABASE_DB_URL`** no repo (Settings → Secrets and variables → Actions) com a connection
string do painel Supabase (Settings → Database → Connection string). Depois eu disparo `carregar-supabase`
(`dry_run=false`) e as 15 tabelas restantes (incl. as 6.715 linhas do Q14) ficam LIVE. Sem esse secret, o
loader é o único passo que falta — é credencial (poder de escrita no banco), por isso fica no seu lado.

## Próximas fases (após Motor 3 completo)
- **Motor 0/2/1** (chão · mapa/PostGIS · RAG) — sem PII, migram na sequência.
- **Motor 4 (cedentes)** — **GATE DE PII**: só sob consentimento.
- **Front-end v1 (Lovable)** — Painel · Carteira · Decisões · Assistente · Acessos; papel único (dono).
