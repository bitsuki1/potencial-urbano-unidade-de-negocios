-- Aviso do advisor (C-02 de 06/08, autorizado pelo dono): tabelas sem RLS.
-- motor0/motor1: conteúdo não-sensível (catálogo e texto de lei), mas RLS on + SELECT p/
-- authenticated fecha a API anônima sem quebrar o front logado (RPCs SECURITY DEFINER seguem).
-- motor2.cedente_ponto: já tinha policy sel_cedente_ponto pronta — RLS on a ativa.
-- public.spatial_ref_sys: NÃO aplicado — tabela do PostGIS, dona = extensão (erro 42501
-- "must be owner"); é tabela pública de sistemas de coordenadas, sem dado sensível.
-- Aplicada via MCP em 2026-08-06 (migração rls_4_tabelas_advisor).
alter table motor0.catalogo_motores enable row level security;
drop policy if exists sel_catalogo on motor0.catalogo_motores;
create policy sel_catalogo on motor0.catalogo_motores for select to authenticated using (true);

alter table motor1.chunks enable row level security;
drop policy if exists sel_chunks on motor1.chunks;
create policy sel_chunks on motor1.chunks for select to authenticated using (true);

alter table motor2.cedente_ponto enable row level security;
