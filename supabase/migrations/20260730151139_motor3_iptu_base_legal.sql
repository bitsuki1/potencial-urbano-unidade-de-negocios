-- Espelho verbatim da migração aplicada 20260730151139 (motor3_iptu_base_legal) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- Motor 3 (dados/base legal do IPTU) — tabelas de referencia vintage, 100% oficiais, SEM PII.
-- Numero nasce no engine (1.3); cada linha rastreavel ao dispositivo/lei (1.7). Fonte primaria = tabelas/*.csv do repo.
-- RLS ligado: dado de referencia legal, leitura liberada a authenticated; escrita so por service_role (migracao).

create schema if not exists motor3;
comment on schema motor3 is 'Motor 3 — base de dados legal (tabelas de referencia vintage do IPTU/TDC). Sem PII.';

-- 1) Aliquota base por uso (Arts. 7/8/27 da Lei 6.989/1966, redacao 13.250/2001)
create table if not exists motor3.iptu_aliquota_base (
  uso           text primary key,
  aliquota_pct  numeric not null,
  dispositivo   text not null,
  lei           text not null
);
comment on table motor3.iptu_aliquota_base is 'Aliquota base do IPTU por uso. Fonte: tabelas/iptu-aliquota-base.csv';

-- 2) Faixas do adicional (Arts. 3/4/5 da Lei 15.889/2013 -> Arts. 7-A/8-A/28 da Lei 6.989/1966). Valores NOMINAIS 2013.
create table if not exists motor3.iptu_aliquota_faixa (
  id                 bigint generated always as identity primary key,
  uso                text not null,
  faixa_de_brl       numeric not null,
  faixa_ate_brl      numeric,            -- null = faixa aberta (ultima)
  aliquota_pct       numeric not null,   -- desconto/acrescimo por porcao
  parcela_deduzir_brl numeric,
  dispositivo        text not null,
  lei                text not null
);
comment on table motor3.iptu_aliquota_faixa is 'Faixas do adicional do IPTU (valores nominais 2013). Fonte: tabelas/iptu-aliquotas-faixa.csv. Nao corrigidas por decreto (item 8, varredura 4/4).';

-- 3) Faixas de isencao por vintage (Art. 2 das leis de PGV: 17.719/2021 vig.2022; 18.330/2025 vig.2026)
create table if not exists motor3.iptu_isencao_faixa (
  vigencia_de                  int primary key,
  limite_isencao_total_brl     numeric not null,
  limite_residencial_abc_brl   numeric not null,
  lei                          text not null,
  dispositivo                  text not null,
  vigencia_inicio              date not null,
  prova                        text
);
comment on table motor3.iptu_isencao_faixa is 'Limites de isencao do IPTU por vintage. Fonte: tabelas/iptu-isencao-faixa.csv';

-- 4) Atualizacao anual do valor venal (serie decreto-a-decreto 2013-2026)
create table if not exists motor3.iptu_atualizacao_anual (
  ano_ref            int primary key,
  tipo               text not null,      -- base_lei | reajuste_decreto | revisao_lei
  percentual         numeric,
  fator_anual        numeric,
  fator_acum_regime  numeric,
  regime_base_ano    int,
  norma              text not null,
  vigencia_inicio    date,
  dispositivo        text,
  fonte_url          text
);
comment on table motor3.iptu_atualizacao_anual is 'Atualizacao anual do valor venal do IPTU (base por LEI, reajuste por DECRETO). Fonte: tabelas/iptu-atualizacao-anual.csv';

-- RLS: leitura para authenticated; escrita apenas service_role
alter table motor3.iptu_aliquota_base      enable row level security;
alter table motor3.iptu_aliquota_faixa     enable row level security;
alter table motor3.iptu_isencao_faixa      enable row level security;
alter table motor3.iptu_atualizacao_anual  enable row level security;

do $$
declare t text;
begin
  foreach t in array array['iptu_aliquota_base','iptu_aliquota_faixa','iptu_isencao_faixa','iptu_atualizacao_anual']
  loop
    execute format('create policy %I on motor3.%I for select to authenticated using (true);', 'sel_'||t, t);
  end loop;
end $$;
