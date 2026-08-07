-- Espelho verbatim da migração aplicada 20260805155554 (c1_hardening_search_path_e_schemas_expostos) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- Endurece o WARN function_search_path_mutable e fixa a superfície REST exposta.
-- search_path pinado (imune a hijack por objeto de mesmo nome em schema no caminho).
alter function motor1.buscar(vector, text, integer) set search_path = motor1, public, pg_temp;
alter function public.consultar_corpus(double precision[], text, integer) set search_path = public, motor1, pg_temp;

-- Reafirma os schemas expostos ao PostgREST (só public + graphql_public; motores NÃO expostos).
-- Corrige o estado 'sem schemas expostos' que derrubava a API REST inteira do projeto.
alter role authenticator set pgrst.db_schemas = 'public, graphql_public';
notify pgrst, 'reload config';
notify pgrst, 'reload schema';
