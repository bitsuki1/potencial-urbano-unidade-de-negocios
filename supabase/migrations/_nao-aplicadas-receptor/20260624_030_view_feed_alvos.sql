-- ============================================================================
-- VIEW de alimentação do engine (H3) — Potencial Urbano, 2026-06-24.
-- Faz o JOIN espacial/cadastral e entrega as LINHAS DE ENTRADA do gerar_alvos.py.
-- NÃO calcula OODC (RO-04: número nasce no engine, não no SQL) — só monta o feed.
-- ============================================================================

create or replace view tabelas.v_feed_alvos as
select
  l.sql_mestre,
  l.sq,
  l.codlog,
  l.zona,
  l.area_lote_m2,
  q14.valor_m2_brl                               as v_m2,
  z.ca_max,
  i.contribuinte                                 as dono,
  i.area_construida,
  i.valor_venal,
  -- área adicional disponível = (CA_max − CA_utilizado) × área do lote, piso 0.
  -- CA_utilizado = área construída / área do terreno (do IPTU).
  greatest(
    (z.ca_max - coalesce(i.area_construida,0) / nullif(l.area_lote_m2,0)) * l.area_lote_m2,
    0
  )                                              as area_adicional_m2
from geo.lote l
join tabelas.q14_valor_terreno q14 on q14.sq = l.sq and q14.codlog = l.codlog
join tabelas.quadro3_ca_zona     z  on z.zona = l.zona and z.ca_max is not null
left join dados.iptu_2026        i  on i.sql_mestre = l.sql_mestre
where l.area_lote_m2 > 0;

comment on view tabelas.v_feed_alvos is
  'Feed do engine de alvos (E5): lote × Q14(V) × Quadro3(CA_max) × IPTU(uso/dono). '
  'Exportar para CSV e rodar scripts/gerar_alvos.py — que calcula a OODC (1.3). '
  'area_adicional_m2 = (CA_max − CA_utilizado)×area_lote, piso 0 (oportunidade construtiva).';

-- Export do feed para o engine:
--   \copy (select sql_mestre as sql, codlog, zona, area_adicional_m2 as area_adicional,
--                 1.2 as fp, 1.0 as fs, dono, '' as endereco
--          from tabelas.v_feed_alvos where area_adicional_m2 > 0)
--     to 'feed-alvos.csv' with (format csv, header true);
--   python3 scripts/gerar_alvos.py --entrada feed-alvos.csv
