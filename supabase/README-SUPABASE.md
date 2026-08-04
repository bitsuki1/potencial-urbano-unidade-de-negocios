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

## Carga de dados (o que falta)
Setar o secret **`SUPABASE_DB_URL`** no repo → rodar a Action `carregar-supabase` (loader
`scripts/carregar_tabelas_supabase.py`) → popula Motor 3 (15 tabelas) + Motor 4 (cedentes) + Motor 1
(4.236 chunks). O Motor 2 (geometrias) aguarda fonte (GeoSampa/geocode).
