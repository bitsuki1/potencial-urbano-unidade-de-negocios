-- Espelho verbatim da migração aplicada 20260804111455 (public_views_frontend) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- Views públicas (expostas ao PostgREST) para o front-end ler dados não-PII.
-- Catálogo dos motores (status da migração) — o Painel mostra isto já com dado real.
create or replace view public.v_catalogo_motores as
  select motor, schema_alvo, descricao, status from motor0.catalogo_motores;
comment on view public.v_catalogo_motores is 'Front-end: status dos 5 motores (sem PII).';

-- Faixas do adicional do IPTU (dado legal público) — exemplo de tabela do Motor 3 p/ o app.
create or replace view public.v_iptu_faixas as
  select uso, faixa_de_brl, faixa_ate_brl, aliquota_pct, dispositivo, lei
  from motor3.iptu_aliquota_faixa order by uso, faixa_de_brl;
comment on view public.v_iptu_faixas is 'Front-end: faixas do adicional do IPTU (dado legal, sem PII).';

grant select on public.v_catalogo_motores, public.v_iptu_faixas to authenticated;
