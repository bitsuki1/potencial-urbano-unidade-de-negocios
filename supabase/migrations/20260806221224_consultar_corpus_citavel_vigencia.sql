-- B-11c/B-11d na nuvem: a busca do assistente não pode fundamentar em chunk não-citável
-- (preâmbulo/boilerplate) nem em dispositivo revogado (1.6/1.7). Espelha o gate local
-- (scripts/consultar.py). Mesma assinatura/contrato; só acrescenta os dois filtros.
-- Aplicada via MCP em 2026-08-06 (migração consultar_corpus_citavel_vigencia).
CREATE OR REPLACE FUNCTION public.consultar_corpus(emb double precision[], dominio_f text DEFAULT NULL::text, k integer DEFAULT 8)
 RETURNS TABLE(chunk_id text, lei_id text, dominio_primario text, citacao jsonb, texto text, similaridade double precision)
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public', 'motor1', 'pg_temp'
AS $function$
  select c.chunk_id, c.lei_id, c.dominio_primario, c.citacao, c.texto,
         1 - (c.embedding <=> (emb::vector(768))) as similaridade
  from motor1.chunks c
  where c.embedding is not null
    and coalesce(c.citavel, true)
    and coalesce(c.vigencia_dispositivo->>'status','') <> 'revogado'
    and (dominio_f is null
         or c.dominio_primario = dominio_f
         or (c.dominio is not null and jsonb_exists(c.dominio, dominio_f)))
  order by c.embedding <=> (emb::vector(768))
  limit k;
$function$
