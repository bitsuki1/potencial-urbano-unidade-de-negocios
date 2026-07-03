-- T7 (escrutinio / PD-7): registrar o gate de seguranca pre-Fase B, com a prova.
insert into governanca.registro_decisoes (id, categoria, titulo, descricao, status, fonte, data)
values
  ('D-SEG-01','arrumacao','T7 — gate de seguranca pre-Fase B (fechado com residuo de baixo risco)',
   'Spend cap ATIVADO (org Pro, antes desligado). 3 S3 access keys da Fase A revogadas (IPTU_2026 Colab Upload, GeoShapefiles Colab Upload, GeoShapefiles v2) — nenhuma restante. Buckets dados-produto/geo-tabelas/geo-shapefiles PRIVADOS e oficiais.* com RLS deny-all (zero policies p/ anon) — verificado via MCP. RESIDUO de BAIXO RISCO: service_role legada nao rotacionada isoladamente (Supabase so oferece Generate-new-JWT-secret, que derruba anon+service_role); o vetor real de exposicao (chaves S3) foi eliminado e nada ativo usa a service_role (scripts leem CSV plano). PLANO: ao precisar de chave de servico (Fase 1 loaders), criar sb_secret nova e desabilitar as chaves legadas — zero quebra.',
   'vigente','ESCRUTINIO-CONJUNTO T7 / Plataforma PD-7; execucao do dono via extensao 2026-07-03', current_date)
on conflict (id) do update set
  categoria=excluded.categoria, titulo=excluded.titulo, descricao=excluded.descricao,
  status=excluded.status, fonte=excluded.fonte, data=excluded.data;
