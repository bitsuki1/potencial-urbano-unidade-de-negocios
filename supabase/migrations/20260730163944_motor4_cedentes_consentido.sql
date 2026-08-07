-- Espelho verbatim da migração aplicada 20260730163944 (motor4_cedentes_consentido) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- Motor 4 — junção dos CEDENTES pela chave canônica sql_mestre (SQL do imóvel).
-- Migração CONSENTIDA pelo dono (2026-07-30 "consentido migração"). Contém dado sensível
-- (endereço/atributos cadastrais por imóvel) — RLS travado: SELECT só para authenticated
-- (papel único = dono na v1); nada exposto a anon. Fonte primária = zepec/oficial/ (1.8:
-- o derivado zepec/ferramenta/ NÃO é fonte). Colunas text para preservar o dado exato.
create schema if not exists motor4;
comment on schema motor4 is 'Motor 4 — cedentes por chave canônica sql_mestre. Migração consentida (dono 2026-07-30). RLS só-dono.';

create table if not exists motor4.c_q14_cedentes_2026_oficial (
  row_id bigint generated always as identity primary key,
  "sq" text, "codlog" text, "valor_m2_brl" text
);
create table if not exists motor4.c_iptu2026_cedentes (
  row_id bigint generated always as identity primary key,
  "sql_mestre" text, "area_terreno" text, "area_construida" text, "valor_m2_terreno" text,
  "valor_m2_construcao" text, "ano_construcao" text, "fator_obsolescencia_oficial" text,
  "tipo_terreno" text, "esquinas_frentes" text, "fracao_ideal" text, "codlog" text,
  "uso" text, "padrao" text, "endereco" text
);
create table if not exists motor4.c_zona_por_cedente (
  row_id bigint generated always as identity primary key,
  "sql_mestre" text, "zona" text, "ca_basico" text, "fonte" text, "na_aiu_sce" text
);
create table if not exists motor4.c_conservacao_cedentes (
  row_id bigint generated always as identity primary key,
  "sql_mestre" text, "cit_nivel_preservacao" text, "cit_atos_tombamento" text, "cit_situacao" text,
  "cit_denominacao" text, "tipo_zepec_atual" text, "reconciliacao" text
);

do $$
declare t text;
begin
  foreach t in array array['c_q14_cedentes_2026_oficial','c_iptu2026_cedentes','c_zona_por_cedente','c_conservacao_cedentes']
  loop
    execute format('alter table motor4.%I enable row level security;', t);
    execute format('create policy %I on motor4.%I for select to authenticated using (true);', 'sel_'||t, t);
  end loop;
end $$;
