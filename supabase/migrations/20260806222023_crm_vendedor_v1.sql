-- CRM lado VENDEDOR (cedentes) — v1. Autorizado pelo dono em 2026-08-06 ("pode executar o CRM").
-- Escopo D-DONO-15/16: cliente = vendedor; comprador FORA (vem depois, tabela própria).
-- Tabelas em public com prefixo crm_ (public é o schema exposto garantido da API; um schema
-- `crm` dedicado exigiria mudança de config de API). PII: proprietario_nome/contatos são
-- authenticated-only; NENHUM grant a anon; nenhuma view pública. Fonte obrigatória (1.7/1.8):
-- nome/contato sempre com origem primária anotada — derivado não vira fonte.
-- Aplicada via MCP em 2026-08-06 (migração crm_vendedor_v1).

create type public.crm_estagio as enum ('novo','contato','negociacao','fechado','descartado');

create table public.crm_lead (
  id uuid primary key default gen_random_uuid(),
  sql_mestre text not null unique,              -- FK-lógica p/ motor4.cedentes (view)
  estagio public.crm_estagio not null default 'novo',
  proprietario_nome text,                       -- nascido de fonte PRIMÁRIA (1.8)
  fonte_nome text,                              -- ex.: 'IPTU-2016' | 'JUCESP' | 'assertiva' | 'manual'
  responsavel uuid references auth.users(id),
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

create table public.crm_contato (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid not null references public.crm_lead(id) on delete cascade,
  tipo text not null check (tipo in ('telefone','whatsapp','email','endereco')),
  valor text not null,
  fonte text not null,                          -- 'assertiva' | 'manual' | ...
  payload jsonb,                                -- resposta bruta (auditoria; nunca exposta a anon)
  consultado_em timestamptz not null default now()
);

create table public.crm_nota (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid not null references public.crm_lead(id) on delete cascade,
  autor uuid references auth.users(id) default auth.uid(),
  texto text not null,
  criado_em timestamptz not null default now()
);

create table public.crm_estagio_historico (
  id bigint generated always as identity primary key,
  lead_id uuid not null references public.crm_lead(id) on delete cascade,
  de public.crm_estagio,
  para public.crm_estagio not null,
  autor uuid default auth.uid(),
  motivo text,
  criado_em timestamptz not null default now()
);

create index crm_lead_estagio_idx on public.crm_lead (estagio);
create index crm_contato_lead_idx on public.crm_contato (lead_id);
create index crm_nota_lead_idx on public.crm_nota (lead_id);
create index crm_hist_lead_idx on public.crm_estagio_historico (lead_id);

-- trilha imutável de estágio + atualizado_em automático
create or replace function public.crm_lead_trilha() returns trigger
language plpgsql security definer set search_path = public, pg_temp as $$
begin
  new.atualizado_em := now();
  if tg_op = 'UPDATE' and new.estagio is distinct from old.estagio then
    insert into public.crm_estagio_historico (lead_id, de, para, autor)
    values (new.id, old.estagio, new.estagio, auth.uid());
  end if;
  return new;
end $$;
create trigger crm_lead_trilha before update on public.crm_lead
  for each row execute function public.crm_lead_trilha();

-- RLS: tudo authenticated-only; histórico é só leitura+insert (imutável)
alter table public.crm_lead enable row level security;
alter table public.crm_contato enable row level security;
alter table public.crm_nota enable row level security;
alter table public.crm_estagio_historico enable row level security;

create policy crm_lead_sel on public.crm_lead for select to authenticated using (true);
create policy crm_lead_ins on public.crm_lead for insert to authenticated with check (true);
create policy crm_lead_upd on public.crm_lead for update to authenticated using (true);
create policy crm_contato_sel on public.crm_contato for select to authenticated using (true);
create policy crm_contato_ins on public.crm_contato for insert to authenticated with check (true);
create policy crm_nota_sel on public.crm_nota for select to authenticated using (true);
create policy crm_nota_ins on public.crm_nota for insert to authenticated with check (true);
create policy crm_hist_sel on public.crm_estagio_historico for select to authenticated using (true);

revoke all on public.crm_lead, public.crm_contato, public.crm_nota, public.crm_estagio_historico from anon;
grant select, insert, update on public.crm_lead to authenticated;
grant select, insert on public.crm_contato, public.crm_nota to authenticated;
grant select on public.crm_estagio_historico to authenticated;
