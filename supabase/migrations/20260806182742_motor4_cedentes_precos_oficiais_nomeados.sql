-- Espelho da migração aplicada via MCP em 2026-08-06 ~18h10 UTC (projeto csnalylpvysjvejgsymr).
-- Opção B (decisão MOU 2026-08-06, lavrada em docs/DECISOES-DO-DONO-2026-08-06.md): a view expõe
-- SÓ dados oficiais, com nome que diz a origem legal de cada valor. O "preço legal" (Art. 128 §2º)
-- NÃO sai daqui — nasce no engine determinístico, rastreável ao artigo (princípio 1.3).
-- Validação pós-aplicação: base 3.905 = view 3.905 (zero fan-out) · 3.905 sql_mestre distintos ·
-- 27 órfãos com vtcd NULL (pendência, não zero) · 474 ca_basico NULL (zona não resolvida, PU 20 ②).
drop view motor4.cedentes;

create view motor4.cedentes as
select
  c.sql_mestre,
  c.endereco,
  z.zona,
  z.ca_basico,
  c.area_terreno,
  c.valor_m2_terreno as valor_m2_venal_iptu2026,  -- valor venal IPTU 2026 (base do imposto; NÃO é o VTcd do Art. 128)
  q.valor_m2_brl     as vtcd_q14_2026_m2,          -- VTcd Quadro 14 Lei 16.050/2014 (ed. 2026) — insumo do engine Art. 128 §2º
  c.uso,
  c.padrao
from motor4.c_iptu2026_cedentes c
left join motor4.c_zona_por_cedente z
  on z.sql_mestre = c.sql_mestre
left join motor4.c_q14_cedentes_2026_oficial q
  on q.sq = left(c.sql_mestre, 6)
 and replace(q.codlog, '-', '') = replace(c.codlog, '-', '');

comment on view motor4.cedentes is
'Carteira de cedentes ZEPEC (fontes oficiais). Dois preços/m² DISTINTOS: valor_m2_venal_iptu2026 = valor venal de terreno do IPTU 2026 (base tributária); vtcd_q14_2026_m2 = VTcd do Quadro 14 do PDE (Lei 16.050/2014, ed. 2026), insumo do preço legal do Art. 128 §2º. O preço legal em si é saída do engine (engines/tdc), nunca desta view. NULL em vtcd = imóvel fora do Q14 (pendência, não zero).';

grant select on motor4.cedentes to authenticated;
