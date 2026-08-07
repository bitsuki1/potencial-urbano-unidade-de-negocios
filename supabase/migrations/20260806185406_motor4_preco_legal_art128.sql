-- Espelho verbatim da migração aplicada 20260806185406 (motor4_preco_legal_art128) — reconstruído de supabase_migrations em 2026-08-07 (higiene, varredura noturna)
-- Fila #22 (decisão Opção B, 2026-08-06): o preço legal NASCE no engine (art128/pcpt, princípio 1.3)
-- e é MATERIALIZADO aqui como saída de engine — com memória de cálculo e pendência declarada (1.7).
-- Fonte: zepec/enriquecer_oficial.py (gate: eval-art128 OK + eval-produto 15/15). Sem PII.
create table motor4.c_preco_legal_art128 (
  sql_mestre           text primary key,
  v_outorga_m2_q14     numeric,      -- VTcd vigente 2026 (Quadro 14, piso Art. 128)
  v_outorga_max_q14    numeric,      -- MAX(piso vigente ; Declaração×IPCA §2º) — OP-1b
  fi_aplicado          numeric,
  fsce_aplicado        numeric,      -- 2.0 quando AIU-SCE (Art. 57 Lei 17.844/2022)
  pcpt_m2              numeric,      -- Atc × CAbás × Fi × FSCE
  m2_ja_transferido    numeric,
  saldo_pcpt_m2        numeric,
  preco_proxy_brl      numeric,      -- saldo × VTcd máximo (referência Art. 128; margem é do usuário)
  regime_pcpt          text,
  cobertura_oficial    text,
  qualidade_estimativa text,
  pendencia_calculo    text,         -- fail-closed: por que NÃO há número, quando não há
  memoria_calculo      text          -- rastreio dispositivo-a-dispositivo (1.7)
);
alter table motor4.c_preco_legal_art128 enable row level security;
create policy sel_c_preco_legal_art128 on motor4.c_preco_legal_art128
  for select to authenticated using (true);

comment on table motor4.c_preco_legal_art128 is
'Saída do engine determinístico Art. 128 (zepec/enriquecer_oficial.py + engines/tdc). Número nasce no engine, nunca no LLM (1.3). preco_proxy_brl = referência LEGAL (piso), não preço comercial (D-DONO-7/15). Linha sem número carrega pendencia_calculo (fail-closed).';

create view motor4.carteira_preco_legal as
select
  c.sql_mestre, c.endereco, c.zona, c.ca_basico, c.area_terreno,
  c.valor_m2_venal_iptu2026, c.vtcd_q14_2026_m2, c.uso, c.padrao,
  p.v_outorga_m2_q14, p.v_outorga_max_q14, p.fi_aplicado, p.fsce_aplicado,
  p.pcpt_m2, p.m2_ja_transferido, p.saldo_pcpt_m2, p.preco_proxy_brl,
  p.regime_pcpt, p.cobertura_oficial, p.qualidade_estimativa,
  p.pendencia_calculo, p.memoria_calculo
from motor4.cedentes c
left join motor4.c_preco_legal_art128 p on p.sql_mestre = c.sql_mestre;

comment on view motor4.carteira_preco_legal is
'Carteira p/ o validador: dados oficiais nomeados (view cedentes, Opção B) + saída do engine Art. 128. preco_proxy_brl NULL = pendência declarada em pendencia_calculo, nunca zero.';

grant select on motor4.carteira_preco_legal to authenticated;
