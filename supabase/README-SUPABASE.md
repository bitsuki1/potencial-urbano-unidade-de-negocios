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

## Leitura direta dos motores pelo front — SÓ titular logado (2026-08-05)
O front v1 (Lovable) lê os schemas dos motores direto (`supabase.schema("motorX")`). Para servir isso **sem abrir
PII ao público**, migração `c1_expor_motores_ao_titular_logado`:
- **`db_schemas` = `public, graphql_public, motor0, motor1, motor2, motor3, motor4`** (schemas dos motores expostos).
- **GRANT só ao papel `authenticated`** (titular logado); **`anon` teve tudo REVOGADO** nesses schemas →
  deslogado recebe `permission denied` (401). Verificado ao vivo.
- **motor0/1/2** (não-PII): RLS desabilitada nas 3 tabelas lidas direto (`catalogo_motores`, `chunks`,
  `cedente_ponto`) — dado público de lei; acesso controlado pelo GRANT.
- **motor3**: views-apelido `motor3.aliquotas`/`faixas`/`atualizacao` (nomes que o front procura) sobre as tabelas
  reais; as tabelas-base mantêm RLS (as views são postgres-owned e a ignoram).
- **motor4 (PII)**: exposto **apenas** via `motor4.cedentes` (view com os campos da carteira:
  sql_mestre, endereco, zona, area_terreno, valor_m2, uso, padrao) com GRANT **só** a `authenticated`. As tabelas
  cruas `motor4.c_*` seguem **sem GRANT + RLS** (não legíveis via REST). _Decisão de PII do dono (revogável)._

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
  `schema "pg_pgrst_no_exposed_schemas" does not exist`. **Atualizado 2026-08-05:** a lista agora inclui
  `motor0..4` para o front do titular logado (ver seção "Leitura direta dos motores"). **A PII do `motor4` só é
  alcançável via a view `motor4.cedentes` com GRANT a `authenticated`; as tabelas `motor4.c_*` cruas seguem sem
  superfície REST (sem GRANT + RLS) e `anon` não toca em motor nenhum.** Nunca dê GRANT de `motor4.c_*` a anon.
- **Pooler:** o projeto vive no fleet **`aws-1-sa-east-1.pooler.supabase.com`** (Session pooler, 5432). O loader
  auto-corrige `aws-0`↔`aws-1` no erro "tenant not found".
