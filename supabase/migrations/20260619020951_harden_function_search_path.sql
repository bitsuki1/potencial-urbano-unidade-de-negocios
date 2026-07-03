-- Advisor 0011: fixa search_path da função canônica (segurança)
alter function governanca.is_sql_mestre(text) set search_path = '';
