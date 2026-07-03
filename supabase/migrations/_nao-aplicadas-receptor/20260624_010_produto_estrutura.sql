-- ============================================================================
-- Estrutura do PRODUTO (H3) — Potencial Urbano. Orquestrador PU, 2026-06-24.
-- DDL APENAS (RO-23: estrutura pode existir; DADO só após organização aprovada).
-- Aplicar no projeto Supabase potencial-urbano-iptu-tdc (ref csnalylpvysjvejgsymr).
-- Schemas já existentes (scaffold 2026-06-19): governanca, geo, leis, tabelas, tese, engine, rag.
-- ============================================================================

create schema if not exists dados;   -- brutos pesados (IPTU, socios) — espelho do Storage no relacional

-- ---- TABELAS (combustível do engine — já temos os CSVs no git) -------------
create table if not exists tabelas.q14_valor_terreno (
  setor        char(3)  not null,
  quadra       char(3)  not null,
  sq           char(6)  not null,                 -- setor+quadra (chave da quadra)
  codlog       char(6)  not null,                 -- face de logradouro
  valor_m2_brl numeric(12,2) not null,            -- V (R$/m²) — Quadro 14 PDE
  primary key (sq, codlog)
);
comment on table tabelas.q14_valor_terreno is 'Quadro 14 (PDE 16.050/2014) — V do m² de terreno por SQ+Codlog. Fonte: Drive, extraido 2026-06-24.';

create table if not exists tabelas.quadro3_ca_zona (
  zona      text primary key,
  ca_min    numeric(6,3),
  ca_basico numeric(6,3),
  ca_max    numeric(6,3)                           -- NULL quando '(k)' variável/NA
);
comment on table tabelas.quadro3_ca_zona is 'Quadro 3 (LPUOS 16.402/2016) — CA min/basico/max por zona.';

create table if not exists tabelas.quadro5_fator_social (
  categoria_uso text primary key,
  fs            numeric(4,2) not null
);

-- ---- GEO (a ponte lote -> SQ/Codlog/zona; geom vem dos shapefiles SIRGAS) ---
create table if not exists geo.lote (
  sql_mestre char(10) primary key,                 -- setor+quadra+lote (CODEX SQL_MESTRE)
  sq         char(6)  not null,
  codlog     char(6),
  zona       text references tabelas.quadro3_ca_zona(zona),
  area_lote_m2 numeric(14,2),
  geom       geometry(MultiPolygon, 31983)          -- SIRGAS 2000 / UTM 23S
);
create index if not exists ix_lote_sq      on geo.lote(sq);
create index if not exists ix_lote_zona    on geo.lote(zona);
create index if not exists ix_lote_geom    on geo.lote using gist(geom);
comment on table geo.lote is 'Lote cadastral com a chave SQL_MESTRE (10) + SQ/Codlog/zona + geometria. Liga Q14 (por SQ+Codlog) e Quadro 3 (por zona).';

-- ---- DADOS pesados (espelho do Storage; carga só após aprovacao, RO-23) -----
create table if not exists dados.iptu_2026 (
  sql_mestre   char(10),
  contribuinte text,
  area_terreno numeric(14,2),
  area_construida numeric(14,2),
  valor_venal  numeric(16,2),
  uso          text
);
create index if not exists ix_iptu_sql on dados.iptu_2026(sql_mestre);

create table if not exists dados.socios (
  documento  text,                                 -- CPF/CNPJ (D106: PII = risco aceito)
  nome       text,
  empresa    text
);
-- ============================================================================
-- Próximo: 20260624_020_carga_tabelas_pequenas.sql (q14/q3/q5 do git) e
--          20260624_030_view_feed_alvos.sql (JOIN -> entrada do engine).
-- ============================================================================
