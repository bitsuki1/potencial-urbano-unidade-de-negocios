-- Auditoria beta + consolidacao de decisoes (2026-07-03). Idempotente.
insert into governanca.registro_decisoes (id, categoria, titulo, descricao, status, fonte, data) values
  ('D-ESCOPO-01','arquitetura','Escopo: SO lado vendedor (cedente), SO ja-tombado',
   'Produto e do lado VENDEDOR (cedente ZEPEC-BIR ja declarada). SEM comprador/matching/receptor, SEM vias 2-6 (doacao/parques), SEM OODC/v_feed_alvos/gerar_alvos. Todo residuo receptor arquivado.',
   'vigente','dono 2026-07-03 (nao e com comprador, e com vendedor; por enquanto so o que ja esta tombado)', current_date),
  ('D-DRIVE-01','arrumacao','CERCA do Google Drive suspensa pelo dono',
   'Leitura E escrita no Drive liberadas por decisao do dono em 2026-07-03 (antes: NAO tocar / drive-arrumacao). Escrita ampla; pode ser estreitada a pasta especifica se o dono pedir.',
   'vigente','dono 2026-07-03', current_date),
  ('D-FORK-00','pendente','Os 3 forks do roadmap seguem ABERTOS',
   'Posicao na cadeia (dados x corretagem x principal); ordem de expansao (via 1 x vias 2-6); regua de preco (proxy x ediv4 x mercado). NAO decididos. Roadmap Secao 2.',
   'pendente','ROADMAP-PU.md', current_date),
  ('D-MOTOR-01','arquitetura','Residuo dos motores aceito como divida de Fase 1',
   'Nenhum dos 3 motores atingiu triplo limpo nos loops de lente. O residuo esta declarado no header de cada MOTOR-*-ESTRATEGIA.md e na fila do handoff. Aceito conscientemente; Fase 1 (codigo dos motores) executa a partir dai.',
   'vigente','ESCRUTINIO-CONJUNTO + loops 2026-07-03', current_date),
  ('D-AUDIT-01','arrumacao','Auditoria beta 2026-07-03: Fase 0 PROVADA verde',
   'git==banco (7 migrations 1:1), de_para=20 (14 OFICIAL), buckets privados, oficiais.* RLS deny-all, gate 7/7 verde, working tree limpo. CAVEATS: db reset clean-room nao executado; CI ainda nao cobre o produto (T2); service_role legada nao rotacionada (residuo baixo risco).',
   'vigente','docs/AUDITORIA-BETA-2026-07-03.md', current_date)
on conflict (id) do update set
  categoria=excluded.categoria, titulo=excluded.titulo, descricao=excluded.descricao,
  status=excluded.status, fonte=excluded.fonte, data=excluded.data;
