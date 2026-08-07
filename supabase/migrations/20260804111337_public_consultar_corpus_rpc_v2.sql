-- Espelho verbatim da migração aplicada 20260804111337 (public_consultar_corpus_rpc_v2) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
create or replace function public.consultar_corpus(
  emb float8[], dominio_f text default null, k int default 8
) returns table (
  chunk_id text, lei_id text, dominio_primario text, citacao jsonb, texto text, similaridade float
)
language sql stable security definer set search_path = public, motor1 as $$
  select c.chunk_id, c.lei_id, c.dominio_primario, c.citacao, c.texto,
         1 - (c.embedding <=> (emb::vector(768))) as similaridade
  from motor1.chunks c
  where c.embedding is not null
    and (dominio_f is null
         or c.dominio_primario = dominio_f
         or (c.dominio is not null and jsonb_exists(c.dominio, dominio_f)))
  order by c.embedding <=> (emb::vector(768))
  limit k;
$$;
comment on function public.consultar_corpus is 'RAG: busca hibrida (filtro dominio + cosseno) exposta ao PostgREST. Retorna chunk + citacao (1.7).';
grant execute on function public.consultar_corpus(float8[], text, int) to authenticated, service_role;
