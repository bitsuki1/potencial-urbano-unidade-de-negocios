-- Card "Leis no corpus" do front (validador Lovable): contagem agregada no servidor.
-- Motivo: o front baixava lei_id linha a linha e o Max Rows da API (1000)
-- truncava a resposta — o card mostrava 39 leis em vez de 132.
create or replace view public.v_corpus_resumo as
select
  count(*)::bigint          as total_chunks,
  count(distinct lei_id)::bigint as total_leis
from motor1.chunks;

comment on view public.v_corpus_resumo is
  'Resumo agregado do corpus jurídico (motor1.chunks): total de trechos e de leis distintas. Consumido pelo card "Leis no corpus" do validador. Sem dado sensível (só contagens).';

-- Contagens do corpus legal não são sensíveis (legislação pública):
-- titular logado usa no Painel; anon permite exibir no painel público.
grant select on public.v_corpus_resumo to authenticated, anon;
