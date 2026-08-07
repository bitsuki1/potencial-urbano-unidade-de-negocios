-- Espelho verbatim da migração aplicada 20260806192644 (motor4_ferramenta_cedentes_e_views_preco) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- Saída do ENGINE do preço legal (Art.128 L16.050): zepec/ferramenta/zepec_cedentes_oficial.csv.
-- Não é "derivado-como-fonte" (1.8): é o RESULTADO do engine determinístico (1.3 — número nasce
-- no engine), com memória de cálculo e citação por linha. Text-only como as irmãs c_* (dado exato).
drop table if exists motor4.c_preco_legal_art128 cascade;  -- leva junto a view carteira_preco_legal (recriada abaixo)
create table motor4.c_zepec_cedentes_ferramenta (
  "sql_mestre" text,"setor" text,"quadra" text,"lote" text,"nome_bem" text,"endereco_mestre" text,
  "distrito" text,"proprietario" text,"fonte_dono" text,"tipo_zepec" text,"esfera" text,
  "estado_venda" text,"certeza" text,"negociavel" text,"motivo_negociavel" text,"sinais_revisar" text,
  "m2_ja_transferido" text,"n_transferencias" text,"conjunto_certidao" text,"valor_pecuniario_rs" text,
  "status_fundurb" text,"intercorrencia_fundurb" text,"base_periodo_fundurb_rs" text,
  "tem_declaracao" text,"tem_certidao" text,"esgotado" text,"elegibilidade_conservacao" text,
  "data_declaracao_iso" text,"data_certidao_iso" text,"data_tombamento_iso" text,"data_ref" text,
  "origens" text,"obs" text,"area_terreno_m2" text,"area_construida_m2" text,
  "valor_m2_terreno_iptu" text,"v_outorga_m2_q14" text,"v_outorga_max_q14" text,"zona" text,
  "ca_basico" text,"fi_aplicado" text,"fsce_aplicado" text,"pcpt_m2" text,"saldo_pcpt_m2" text,
  "parcelas_anuais" text,"preco_proxy_brl" text,"uso_iptu" text,"cobertura_oficial" text,
  "memoria_calculo" text,"pendencia_calculo" text,"regime_pcpt" text,"qualidade_estimativa" text,
  "cit_nivel_preservacao" text,"cit_atos_tombamento" text,"cit_reconciliacao" text,
  "v_q14_origem" text,"conservacao_diverge_oficial" text
);
alter table motor4.c_zepec_cedentes_ferramenta enable row level security;  -- sem policy = só service/postgres

-- View tipada do preço legal (rastreável: memória + pendência + regime vêm juntas)
create or replace view motor4.preco_legal as
select
  sql_mestre,
  nullif(v_outorga_m2_q14,'')::numeric   as v_outorga_m2_q14,
  nullif(v_outorga_max_q14,'')::numeric  as v_outorga_max_q14,
  nullif(fi_aplicado,'')::numeric        as fi_aplicado,
  nullif(fsce_aplicado,'')::numeric      as fsce_aplicado,
  nullif(pcpt_m2,'')::numeric            as pcpt_m2,
  nullif(m2_ja_transferido,'')::numeric  as m2_ja_transferido,
  nullif(saldo_pcpt_m2,'')::numeric      as saldo_pcpt_m2,
  nullif(preco_proxy_brl,'')::numeric    as preco_proxy_brl,
  nullif(regime_pcpt,'')                 as regime_pcpt,
  nullif(cobertura_oficial,'')           as cobertura_oficial,
  nullif(qualidade_estimativa,'')        as qualidade_estimativa,
  nullif(pendencia_calculo,'')           as pendencia_calculo,
  nullif(memoria_calculo,'')             as memoria_calculo
from motor4.c_zepec_cedentes_ferramenta;

-- Carteira do front: acrescenta o preço legal à view consumida (GRANT authenticated preservado)
create or replace view motor4.cedentes as
select c.sql_mestre,
       c.endereco,
       z.zona,
       z.ca_basico,
       c.area_terreno,
       c.valor_m2_terreno as valor_m2_venal_iptu2026,
       q.valor_m2_brl     as vtcd_q14_2026_m2,
       c.uso,
       c.padrao,
       p.pcpt_m2,
       p.saldo_pcpt_m2,
       p.preco_proxy_brl,
       p.regime_pcpt,
       p.qualidade_estimativa,
       p.cobertura_oficial,
       p.memoria_calculo,
       p.pendencia_calculo
from motor4.c_iptu2026_cedentes c
left join motor4.c_zona_por_cedente z on z.sql_mestre = c.sql_mestre
left join motor4.c_q14_cedentes_2026_oficial q
       on q.sq = left(c.sql_mestre,6)
      and replace(q.codlog,'-','') = replace(c.codlog,'-','')
left join motor4.preco_legal p on p.sql_mestre = c.sql_mestre;

-- Recria a carteira_preco_legal (mesmo contrato de antes, agora sobre a view tipada)
create view motor4.carteira_preco_legal as
select c.sql_mestre, c.endereco, c.zona, c.ca_basico, c.area_terreno,
       c.valor_m2_venal_iptu2026, c.vtcd_q14_2026_m2, c.uso, c.padrao,
       p.v_outorga_m2_q14, p.v_outorga_max_q14, p.fi_aplicado, p.fsce_aplicado,
       p.pcpt_m2, p.m2_ja_transferido, p.saldo_pcpt_m2, p.preco_proxy_brl,
       p.regime_pcpt, p.cobertura_oficial, p.qualidade_estimativa,
       p.pendencia_calculo, p.memoria_calculo
from motor4.cedentes c
left join motor4.preco_legal p on p.sql_mestre = c.sql_mestre;

grant select on motor4.cedentes to authenticated;
grant select on motor4.carteira_preco_legal to authenticated;

-- Mapa (motor2): view pública p/ o front (Leaflet quer lat/lon WGS84). Dono postgres ignora RLS;
-- GRANT só authenticated (decisão de PII do dono: carteira atrás do login).
create or replace view public.v_cedentes_mapa as
select pt.sql_mestre,
       st_y(st_transform(pt.geom, 4326)) as lat,
       st_x(st_transform(pt.geom, 4326)) as lon,
       coalesce(pt.endereco, c.endereco) as endereco,
       c.zona,
       c.preco_proxy_brl,
       c.saldo_pcpt_m2,
       c.regime_pcpt
from motor2.cedente_ponto pt
left join motor4.cedentes c on c.sql_mestre = pt.sql_mestre;
revoke all on public.v_cedentes_mapa from anon, public;
grant select on public.v_cedentes_mapa to authenticated;
