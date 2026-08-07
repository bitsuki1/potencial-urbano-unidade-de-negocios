-- Espelho verbatim da migração aplicada 20260805192857 (c1_expor_motores_ao_titular_logado) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- ============================================================
-- Expor os motores ao front SOMENTE para o titular autenticado.
-- Não-PII (motor0/1/2/3): leitura direta pelo titular logado.
-- PII (motor4): apenas a view 'cedentes' (campos da carteira), titular logado.
-- anon (deslogado) permanece SEM acesso a qualquer motor.
-- ============================================================

-- 1) Views-apelido no motor3 (nomes que o front procura). Views são
--    postgres-owned => ignoram a RLS das tabelas-base; acesso via GRANT.
create or replace view motor3.aliquotas   as select * from motor3.iptu_aliquota_base;
create or replace view motor3.faixas      as select * from motor3.iptu_aliquota_faixa;
create or replace view motor3.atualizacao as select * from motor3.iptu_atualizacao_anual;

-- 2) View de carteira sobre o motor4 (PII): só os campos necessários.
create or replace view motor4.cedentes as
select
  c.sql_mestre,
  c.endereco,
  z.zona,
  c.area_terreno,
  c.valor_m2_terreno as valor_m2,
  c.uso,
  c.padrao
from motor4.c_iptu2026_cedentes c
left join motor4.c_zona_por_cedente z on z.sql_mestre = c.sql_mestre;

-- 3) Tabelas lidas DIRETO pelo front (não via view) precisam de RLS off
--    (dado público de lei; o acesso fica controlado pelo GRANT ao titular).
alter table motor0.catalogo_motores disable row level security;
alter table motor1.chunks           disable row level security;
alter table motor2.cedente_ponto    disable row level security;

-- 4) GRANTs: só o papel 'authenticated' (titular logado) enxerga os motores.
grant usage on schema motor0, motor1, motor2, motor3, motor4 to authenticated;
grant select on motor0.catalogo_motores to authenticated;
grant select on motor1.chunks           to authenticated;
grant select on motor2.cedente_ponto    to authenticated;
grant select on motor3.aliquotas, motor3.faixas, motor3.atualizacao to authenticated;
grant select on motor4.cedentes to authenticated;

-- 5) Blindagem: anon (deslogado) não toca em motor nenhum.
revoke all on schema motor0, motor1, motor2, motor3, motor4 from anon;
revoke all on all tables in schema motor0 from anon;
revoke all on all tables in schema motor1 from anon;
revoke all on all tables in schema motor2 from anon;
revoke all on all tables in schema motor3 from anon;
revoke all on all tables in schema motor4 from anon;

-- 6) Expor os schemas dos motores ao PostgREST (motor4 incluso, mas só a
--    view 'cedentes' tem GRANT; as tabelas c_* cruas seguem sem grant + RLS).
alter role authenticator set pgrst.db_schemas = 'public, graphql_public, motor0, motor1, motor2, motor3, motor4';
notify pgrst, 'reload config';
notify pgrst, 'reload schema';
