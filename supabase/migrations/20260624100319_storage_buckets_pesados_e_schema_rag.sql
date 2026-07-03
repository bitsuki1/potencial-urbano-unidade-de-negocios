-- Scaffold de Storage para os brutos pesados (RO-23: estrutura vazia, sem dado) + schema rag faltante.
-- Trazido pelo orquestrador do PU — 2026-06-24, autorizado pelo MOU ("pesados no Supabase ja").

create schema if not exists rag;

insert into storage.buckets (id, name, public)
values
  ('dados-produto',   'dados-produto',   false),
  ('geo-tabelas',     'geo-tabelas',     false),
  ('geo-shapefiles',  'geo-shapefiles',  false)
on conflict (id) do nothing;
