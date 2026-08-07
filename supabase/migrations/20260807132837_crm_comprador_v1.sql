-- CRM lado COMPRADOR (receptores de potencial construtivo) — v1. Fecha a task #24
-- ("executar os dois CRMs"): o vendedor entrou em 2026-08-06 (crm_vendedor_v1); esta é a
-- tabela PRÓPRIA do comprador exigida pelo escopo D-DONO-15/16 ("cliente = vendedor;
-- comprador FORA, vem depois, tabela própria").
-- Mesmo padrão do vendedor: public com prefixo crm_, RLS authenticated-only, zero grant a
-- anon, trilha imutável de estágio, PII sempre com fonte primária anotada (1.7/1.8).
-- Estudo do receptor (PU 19, dados reais): a ÁREA que o comprador recebe depende do Cr do
-- projeto DELE (Art. 117 — projeto-específico) — por isso demanda_m2 é DECLARAÇÃO do
-- interessado (dado comercial), nunca cálculo nosso; nenhum número legal nasce aqui (1.3).

create table public.crm_comprador (
  id uuid primary key default gen_random_uuid(),
  nome text not null,                            -- razão social ou nome do interessado
  tipo text not null default 'incorporadora'
    check (tipo in ('incorporadora','construtora','investidor','pessoa_fisica','outro')),
  estagio public.crm_estagio not null default 'novo',   -- reusa o enum do vendedor
  demanda_m2 numeric,                            -- quanto potencial declara querer (declaração dele)
  regiao_interesse text[],                       -- bairros/distritos declarados
  sq_receptor text,                              -- SQL do imóvel receptor, se já existir projeto
  fonte_nome text,                               -- de onde veio o lead: 'site' | 'indicacao' | 'manual' | ...
  responsavel uuid references auth.users(id),
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

create table public.crm_comprador_contato (
  id uuid primary key default gen_random_uuid(),
  comprador_id uuid not null references public.crm_comprador(id) on delete cascade,
  tipo text not null check (tipo in ('telefone','whatsapp','email','endereco')),
  valor text not null,
  fonte text not null,
  payload jsonb,                                 -- resposta bruta (auditoria; nunca exposta a anon)
  consultado_em timestamptz not null default now()
);

create table public.crm_comprador_nota (
  id uuid primary key default gen_random_uuid(),
  comprador_id uuid not null references public.crm_comprador(id) on delete cascade,
  autor uuid references auth.users(id) default auth.uid(),
  texto text not null,
  criado_em timestamptz not null default now()
);

create table public.crm_comprador_estagio_historico (
  id bigint generated always as identity primary key,
  comprador_id uuid not null references public.crm_comprador(id) on delete cascade,
  de public.crm_estagio,
  para public.crm_estagio not null,
  autor uuid default auth.uid(),
  motivo text,
  criado_em timestamptz not null default now()
);

-- O NEGÓCIO: match comprador ↔ lead vendedor (cedente). Um comprador pode olhar N cedentes
-- e vice-versa; o fechamento de TDC é sempre um par. m2/valor aqui = TERMOS NEGOCIADOS
-- (dado comercial declarado) — o preço LEGAL de referência segue nascendo só no engine
-- Art. 128 e já está materializado em motor4.cedentes (preco_proxy_brl, memoria_calculo).
create table public.crm_match (
  id uuid primary key default gen_random_uuid(),
  comprador_id uuid not null references public.crm_comprador(id) on delete cascade,
  lead_id uuid not null references public.crm_lead(id) on delete cascade,
  status text not null default 'sugerido'
    check (status in ('sugerido','apresentado','negociacao','fechado','descartado')),
  m2_negociado numeric,
  valor_negociado_brl numeric,
  nota text,
  autor uuid references auth.users(id) default auth.uid(),
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now(),
  unique (comprador_id, lead_id)
);

-- índices (incl. FKs desde já — lição do advisor na varredura #3 do vendedor)
create index crm_comprador_estagio_idx on public.crm_comprador (estagio);
create index crm_comprador_responsavel_idx on public.crm_comprador (responsavel);
create index crm_comprador_contato_fk_idx on public.crm_comprador_contato (comprador_id);
create index crm_comprador_nota_fk_idx on public.crm_comprador_nota (comprador_id);
create index crm_comprador_nota_autor_idx on public.crm_comprador_nota (autor);
create index crm_comprador_hist_fk_idx on public.crm_comprador_estagio_historico (comprador_id);
create index crm_match_comprador_idx on public.crm_match (comprador_id);
create index crm_match_lead_idx on public.crm_match (lead_id);
create index crm_match_status_idx on public.crm_match (status);
create index crm_match_autor_idx on public.crm_match (autor);

-- trilha imutável de estágio + atualizado_em automático (espelho do crm_lead_trilha)
create or replace function public.crm_comprador_trilha() returns trigger
language plpgsql security definer set search_path = public, pg_temp as $$
begin
  new.atualizado_em := now();
  if tg_op = 'UPDATE' and new.estagio is distinct from old.estagio then
    insert into public.crm_comprador_estagio_historico (comprador_id, de, para, autor)
    values (new.id, old.estagio, new.estagio, auth.uid());
  end if;
  return new;
end $$;
create trigger crm_comprador_trilha before update on public.crm_comprador
  for each row execute function public.crm_comprador_trilha();

create or replace function public.crm_match_atualizado() returns trigger
language plpgsql security definer set search_path = public, pg_temp as $$
begin
  new.atualizado_em := now();
  return new;
end $$;
create trigger crm_match_atualizado before update on public.crm_match
  for each row execute function public.crm_match_atualizado();

-- RLS: tudo authenticated-only; histórico só select (insert vem do trigger, definer)
alter table public.crm_comprador enable row level security;
alter table public.crm_comprador_contato enable row level security;
alter table public.crm_comprador_nota enable row level security;
alter table public.crm_comprador_estagio_historico enable row level security;
alter table public.crm_match enable row level security;

create policy crm_comprador_sel on public.crm_comprador for select to authenticated using (true);
create policy crm_comprador_ins on public.crm_comprador for insert to authenticated with check (true);
create policy crm_comprador_upd on public.crm_comprador for update to authenticated using (true);
create policy crm_comprador_contato_sel on public.crm_comprador_contato for select to authenticated using (true);
create policy crm_comprador_contato_ins on public.crm_comprador_contato for insert to authenticated with check (true);
create policy crm_comprador_nota_sel on public.crm_comprador_nota for select to authenticated using (true);
create policy crm_comprador_nota_ins on public.crm_comprador_nota for insert to authenticated with check (true);
create policy crm_comprador_hist_sel on public.crm_comprador_estagio_historico for select to authenticated using (true);
create policy crm_match_sel on public.crm_match for select to authenticated using (true);
create policy crm_match_ins on public.crm_match for insert to authenticated with check (true);
create policy crm_match_upd on public.crm_match for update to authenticated using (true);

revoke all on public.crm_comprador, public.crm_comprador_contato, public.crm_comprador_nota,
  public.crm_comprador_estagio_historico, public.crm_match from anon;
grant select, insert, update on public.crm_comprador, public.crm_match to authenticated;
grant select, insert on public.crm_comprador_contato, public.crm_comprador_nota to authenticated;
grant select on public.crm_comprador_estagio_historico to authenticated;

comment on table public.crm_comprador is 'CRM lado COMPRADOR (receptor de potencial TDC) — v1, tabela própria (D-DONO-15/16). demanda_m2 = declaração do interessado; nenhum número legal nasce aqui (1.3).';
comment on table public.crm_match is 'Par comprador↔cedente (o negócio de TDC). m2/valor = termos negociados (comercial); preço LEGAL de referência = engine Art. 128 em motor4.cedentes.';
