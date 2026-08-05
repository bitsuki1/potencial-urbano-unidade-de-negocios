# Supabase — projeto `potencial-urbano-iptu-tdc` (`csnalylpvysjvejgsymr`, sa-east-1)

Backend do C1 (migração motor-a-motor) e do front-end v1. Todas as migrações estão no histórico
de migrações do Supabase; este README é o mapa. Chaves de poder total (service_role, DB URL) **fora do git**
(cofre D106) — em GitHub Secret / painel.

## Schemas (por motor)
- **`motor0.catalogo_motores`** — "chão": registro dos 5 motores + status. RLS só-dono.
- **`motor1.chunks`** — RAG do corpus (chunk por dispositivo) + `embedding vector(768)` (pgvector,
  `gemini-embedding-001`). Índices GIN (tema/domínio), HNSW cosseno. RLS só-dono.
- **`motor2.cedente_ponto`** — mapa: `geometry(Point,31983)` por `sql_mestre` (PostGIS, GiST). RLS só-dono.
- **`motor3.*`** — base de dados legal (alíquotas, faixas, atualização, Q14, IPCA, quadros…). RLS só-dono.
- **`motor4.c_*`** — cedentes por `sql_mestre` (**PII/sensível**, migração consentida 2026-07-30). RLS só-dono.

## Funções / RPC
- **`motor1.buscar(consulta vector, dominio, k)`** — busca híbrida (filtro domínio + cosseno) → chunk + citação.
- **`public.consultar_corpus(emb float8[], dominio_f, k)`** — wrapper exposto ao PostgREST (SECURITY DEFINER)
  que casta o embedding e roda a busca. É o que a Edge Function chama.

## Views públicas (para o front-end, sem PII)
- **`public.v_catalogo_motores`** — status dos 5 motores.
- **`public.v_iptu_faixas`** — faixas do adicional do IPTU (dado legal).

## Edge Function
- **`consultar-rag`** (`supabase/functions/consultar-rag/index.ts`) — recebe `{pergunta, dominio?, k?}`,
  embeda a pergunta no Gemini (768d) e chama `public.consultar_corpus` → devolve trechos **com citação**
  (fail-closed: sem hit, `fundamentada:false` + aviso). `verify_jwt` on.
  - **Secret necessário:** `GEMINI_API_KEY` (painel Supabase → Edge Functions → Secrets; chave no cofre).

## Carga de dados ✅ FEITA (2026-08-05)
Secret **`SUPABASE_DB_URL`** setado → Action `carregar-supabase` (loader `scripts/carregar_tabelas_supabase.py`)
populou **Motor 3 (15 tabelas) + Motor 4 (4 tab. cedentes) + Motor 1 (4.236 chunks, 2.805 com embedding)**.
Secret **`GEMINI_API_KEY`** setado → `consultar-rag` responde `fundamentada:true` com citação. Motor 2
(geometrias) aguarda fonte (GeoSampa/geocode).

## ⚠️ Config crítica do projeto (não reverter)
- **Exposed schemas** do PostgREST = **`public, graphql_public`** (`alter role authenticator set pgrst.db_schemas`,
  migração `c1_hardening_search_path_e_schemas_expostos`). Se a lista ficar **vazia**, a API REST inteira cai com
  `schema "pg_pgrst_no_exposed_schemas" does not exist`. Os schemas `motor0..4` **NÃO** são expostos de propósito
  (alcançados só pelo wrapper `public.consultar_corpus`); **nunca** exponha `motor4` (PII).
- **Pooler:** o projeto vive no fleet **`aws-1-sa-east-1.pooler.supabase.com`** (Session pooler, 5432). O loader
  auto-corrige `aws-0`↔`aws-1` no erro "tenant not found".
