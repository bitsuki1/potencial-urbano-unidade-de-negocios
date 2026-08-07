-- Espelho verbatim da migração aplicada 20260801200424 (motor1_rag_chunks) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- Motor 1 — RAG do corpus jurídico (chunk por dispositivo; 1.1/2.5). SEM PII.
-- Habilita pgvector (embeddings gemini-embedding-001, dim 768) e cria a tabela de chunks
-- com os metadados de filtro (tema/domínio/vigência/jurisdição) do retrieval híbrido (2.6).
create extension if not exists vector;

create schema if not exists motor1;
comment on schema motor1 is 'Motor 1 — RAG do corpus juridico (chunk por dispositivo). Sem PII.';

create table if not exists motor1.chunks (
  chunk_id            text primary key,
  lei_id              text not null,
  tipo_dispositivo    text,
  rotulo              text,
  numero              text,
  header_raw          text,
  caminho_hierarquico jsonb,
  texto               text not null,
  citavel             boolean,
  vigencia_dispositivo jsonb,
  citacao             jsonb,
  tema                jsonb,
  dominio             jsonb,
  dominio_primario    text,
  jurisdicao          text,
  ementa              text,
  embedding           vector(768)
);
comment on table motor1.chunks is 'Chunks do corpus (um por dispositivo). Fonte: rag/index/chunks.json + embeddings.json. Numero nasce no engine (1.3); aqui e o texto normativo + metadados de filtro (2.6). embedding: gemini-embedding-001 (768d); NULL onde ainda sem vetor.';

-- filtros de metadado (pre-busca) do retrieval hibrido
create index if not exists chunks_lei_id_idx      on motor1.chunks (lei_id);
create index if not exists chunks_dominio_prim_idx on motor1.chunks (dominio_primario);
create index if not exists chunks_tema_gin         on motor1.chunks using gin (tema);
create index if not exists chunks_dominio_gin      on motor1.chunks using gin (dominio);
-- busca semantica (cosseno). ivfflat exige ANALYZE/dados; criamos depois da carga se preferir.
create index if not exists chunks_embedding_hnsw   on motor1.chunks using hnsw (embedding vector_cosine_ops);

alter table motor1.chunks enable row level security;
create policy sel_chunks on motor1.chunks for select to authenticated using (true);
