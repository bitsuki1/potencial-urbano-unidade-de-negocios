-- Espelho verbatim da migração aplicada 20260802160142 (motor0_catalogo_motor2_mapa_motor1_busca) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- Motor 0 — "chão": catálogo/registro dos motores (a fundação que os outros referenciam).
create schema if not exists motor0;
comment on schema motor0 is 'Motor 0 — chao/fundacao: catalogo dos motores e seu estado de migracao.';
create table if not exists motor0.catalogo_motores (
  motor        text primary key,
  schema_alvo  text,
  descricao    text,
  status       text,          -- schema_criado | dados_live | pendente
  fonte        text
);
alter table motor0.catalogo_motores enable row level security;
create policy sel_catalogo on motor0.catalogo_motores for select to authenticated using (true);
insert into motor0.catalogo_motores(motor,schema_alvo,descricao,status,fonte) values
 ('motor0','motor0','Chao: catalogo dos motores','schema_criado','este registro'),
 ('motor1','motor1','RAG do corpus juridico (chunks + pgvector)','schema_criado','rag/index/chunks.json+embeddings.json'),
 ('motor2','motor2','Mapa: geometrias PostGIS por sql_mestre','schema_criado','GeoSampa/cadastro (a carregar)'),
 ('motor3','motor3','Base de dados legal (tabelas de referencia vintage)','parcial_live','tabelas/*.csv'),
 ('motor4','motor4','Junção dos cedentes por sql_mestre (consentido)','schema_criado','zepec/oficial/*.csv')
on conflict (motor) do update set status=excluded.status, descricao=excluded.descricao;

-- Motor 2 — "mapa": geometrias por cedente (PostGIS). SRID 31983 = SIRGAS 2000 / UTM 23S (São Paulo).
create schema if not exists motor2;
comment on schema motor2 is 'Motor 2 — mapa: geometrias (PostGIS) por sql_mestre. Dado publico cadastral (sem PII pessoal).';
create table if not exists motor2.cedente_ponto (
  sql_mestre text primary key,
  geom       geometry(Point, 31983),
  endereco   text,
  fonte      text
);
create index if not exists cedente_ponto_gix on motor2.cedente_ponto using gist (geom);
alter table motor2.cedente_ponto enable row level security;
create policy sel_cedente_ponto on motor2.cedente_ponto for select to authenticated using (true);

-- Motor 1 — camada de CONSULTA (Gen RAG): busca hibrida (filtro por dominio + semantico por cosseno).
-- Numero/afirmacao nasce do dispositivo citado (1.7): a funcao devolve o chunk + a citacao, nunca "inventa".
create or replace function motor1.buscar(
  consulta        vector(768),
  dominio_filtro  text default null,
  k               int  default 8
) returns table (
  chunk_id text, lei_id text, dominio_primario text, citacao jsonb, texto text, similaridade float
)
language sql stable as $$
  select c.chunk_id, c.lei_id, c.dominio_primario, c.citacao, c.texto,
         1 - (c.embedding <=> consulta) as similaridade
  from motor1.chunks c
  where c.embedding is not null
    and (dominio_filtro is null or c.dominio_primario = dominio_filtro
         or c.dominio ? dominio_filtro)
  order by c.embedding <=> consulta
  limit k;
$$;
comment on function motor1.buscar is 'Busca hibrida do RAG: filtro por dominio + vizinho mais proximo (cosseno). Retorna chunk + citacao (1.7).';
