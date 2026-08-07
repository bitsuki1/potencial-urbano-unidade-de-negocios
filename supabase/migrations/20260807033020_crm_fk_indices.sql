-- Advisor (varredura #3): FKs do CRM sem índice — cria os dois (tabelas pequenas; higiene).
create index if not exists crm_lead_responsavel_idx on public.crm_lead (responsavel);
create index if not exists crm_nota_autor_idx on public.crm_nota (autor);
