insert into governanca.registro_decisoes (id, categoria, titulo, descricao, status, fonte, data) values
  ('D-AUDIT-02','arrumacao','Auditoria PROFUNDA + encerramento: sessao entregou plano+fundacao, ZERO fix de produto',
   'Verificado em arquivo: NENHUM codigo de produto mudou (engines/ zepec/*.py intocados). Todos os defeitos diagnosticados seguem VIVOS: C-28 (133__art-124.json rotula a formula como Art.124), T3 (enriquecer_oficial.py:81 escalonado por default), T8 (montar_base.py:104 vedacao so substring), G1 (overlay_zona.py:77 centroide). Os ~2.937 precos e o R$8,83bi sao byte-identicos ao pre-sessao e NAO sao confiaveis (T3/T8 vivos). O gate verde cobre a FUNDACAO, nao o produto (T2 vivo). Fase 1 (codigo) NAO comecou. Detalhe: docs/AUDITORIA-PROFUNDA-E-ENCERRAMENTO-2026-07-03.md.',
   'vigente','docs/AUDITORIA-PROFUNDA-E-ENCERRAMENTO-2026-07-03.md', current_date)
on conflict (id) do update set
  categoria=excluded.categoria, titulo=excluded.titulo, descricao=excluded.descricao,
  status=excluded.status, fonte=excluded.fonte, data=excluded.data;
