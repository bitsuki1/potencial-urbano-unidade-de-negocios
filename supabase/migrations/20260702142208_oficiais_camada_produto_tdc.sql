-- Camada OFICIAL do produto TDC (Fase A — D-DONO-6: oficiais primeiro).
-- Toda tabela carrega proveniência. RLS deny-all (acesso só via service/backoffice).

create schema if not exists oficiais;

-- 1) IPTU 2026: recorte dos CEDENTES (área do terreno = Atc, o insumo do engine PCpt)
create table if not exists oficiais.iptu2026_cedentes (
  sql_mestre      text primary key,
  area_terreno_m2 numeric,
  area_construida_m2 numeric,
  v_venal_m2      numeric,
  codlog          text,
  uso             text,
  padrao          text,
  endereco        text,
  fonte           text not null default 'IPTU_2026.csv (PMSP, oficial) — recorte cedentes ZEPEC, extraido 2026-07-02'
);
comment on table oficiais.iptu2026_cedentes is 'Recorte OFICIAL do IPTU 2026 para os cedentes ZEPEC. Atc (area do terreno) = insumo do engine PCpt = Atc x CAbas x Fi (PDE Art. 125). Proveniencia: dados-produto/oficiais/IPTU_2026.csv.';

-- 2) Quadro 14 (valor do m2 de terreno para outorga) — CIDADE INTEIRA, vigente 2025
create table if not exists oficiais.q14_valor_terreno_2025 (
  sq       text not null,
  codlog   text not null,
  valor_m2_brl numeric not null,
  fonte    text not null default 'Atualizacao Q14 jan/2025 (Quadro 14, Anexo Lei 16.050/2014) — oficial',
  primary key (sq, codlog)
);
comment on table oficiais.q14_valor_terreno_2025 is 'Quadro 14 do PDE (valor de terreno p/ outorga), atualizacao jan/2025, cidade inteira (~179k faces). NAO confundir com valor venal do IPTU (dois V homonimos — vacina do catalogo-mestre).';

alter table oficiais.iptu2026_cedentes enable row level security;
alter table oficiais.q14_valor_terreno_2025 enable row level security;
