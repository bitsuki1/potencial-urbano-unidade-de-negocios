-- Namespaces dos 4 artefatos separados (RO-03) + governança + geo
create schema if not exists leis;        -- LEI / norma -> RAG
create schema if not exists tabelas;     -- TABELA / dado -> input de engine
create schema if not exists engine;      -- FÓRMULA / engine determinístico
create schema if not exists tese;        -- TESE / Antítese / Vacina
create schema if not exists geo;         -- camadas espaciais (PostGIS)
create schema if not exists governanca;  -- De/Para, decisões, registro

-- De/Para localizador = livro-razão vivo (RO-14): vigência, linhagem, proveniência
create table if not exists governanca.de_para (
  drive_id        text primary key,
  titulo          text not null,
  destino         text not null,
  origem          text,
  tipo            text check (tipo in ('arquivo','pasta')),
  vigencia_inicio date,
  vigencia_fim    date,
  substitui       text,
  substituido_por text,
  proveniencia    text,
  oficialidade    text check (oficialidade in ('OFICIAL','NAO-OFICIAL','CRIADO-POR-NOS','CRIADO-POR-TERCEIROS')),
  confianca       text check (confianca in ('alta','media','baixa')),
  observacao      text,
  criado_em       timestamptz default now()
);

-- Registro de decisões (espelha CODEX §7 / DECISOES AF-xx e as RO)
create table if not exists governanca.registro_decisoes (
  id        text primary key,                 -- ex.: RO-22, D-01, AF-08
  categoria text check (categoria in ('regra_ouro','arquitetura','arrumacao','stack','pendente')),
  titulo    text not null,
  descricao text,
  status    text check (status in ('vigente','revertida','pendente')) default 'vigente',
  fonte     text,                              -- ex.: 'CODEX §7'
  data      date default current_date
);

-- Padrão canônico SQL_MESTRE (§3): 10 dígitos, validação
create or replace function governanca.is_sql_mestre(t text)
  returns boolean language sql immutable as $$ select t ~ '^[0-9]{10}$' $$;

-- Trava de segurança: RLS ligada (acesso só via service role; sem API pública ainda)
alter table governanca.de_para            enable row level security;
alter table governanca.registro_decisoes  enable row level security;

comment on schema governanca is 'Beta contínuo: De/Para (RO-14), decisões e padrões canônicos do projeto IPTU/TDC.';
