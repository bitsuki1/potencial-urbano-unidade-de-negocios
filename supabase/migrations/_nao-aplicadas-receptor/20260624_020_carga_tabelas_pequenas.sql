-- ============================================================================
-- Carga das TABELAS PEQUENAS (já no git) — Potencial Urbano, 2026-06-24.
-- Rodar via psql/Supabase CLI a partir da RAIZ do repo (os \copy leem os CSVs locais).
-- NÃO é dado pessoal/pesado — é combustível público do engine (RO-23 ok: tabela de lei).
-- Os CSVs têm 1 linha-comentário '#' no topo; o \copy abaixo a pula com HEADER + skip manual.
-- ============================================================================

-- Q14 (V por SQ+Codlog) — 6.715 linhas. O arquivo tem comentário '#'; carregue por staging.
create temp table _stg_q14 (setor text, quadra text, sql text, codlog text, valor text);
\copy _stg_q14 from program 'tail -n +3 tabelas/q14-valor-terreno.csv' with (format csv);
insert into tabelas.q14_valor_terreno (setor,quadra,sq,codlog,valor_m2_brl)
select setor, quadra, sql, codlog, replace(replace(valor,'.',''),',','.')::numeric
from _stg_q14
on conflict (sq,codlog) do update set valor_m2_brl = excluded.valor_m2_brl;

-- Quadro 3 (CA por zona) — 39 zonas. ca_max '(k)'/NA -> NULL.
create temp table _stg_q3 (zona text, ca_min text, ca_basico text, ca_max text);
\copy _stg_q3 from program 'tail -n +3 tabelas/quadro3-ca-por-zona.csv' with (format csv);
insert into tabelas.quadro3_ca_zona (zona,ca_min,ca_basico,ca_max)
select zona,
       nullif(replace(ca_min,',','.'),'NA')::numeric,
       nullif(replace(ca_basico,',','.'),'NA')::numeric,
       nullif(replace(ca_max,',','.'),'NA')::numeric
from _stg_q3
on conflict (zona) do update set ca_max = excluded.ca_max, ca_basico = excluded.ca_basico, ca_min = excluded.ca_min;

-- Quadro 5 (Fs)
create temp table _stg_q5 (categoria text, fs text);
\copy _stg_q5 from program 'tail -n +3 tabelas/quadro5-fator-social-fs.csv' with (format csv);
insert into tabelas.quadro5_fator_social (categoria_uso, fs)
select categoria, replace(fs,',','.')::numeric from _stg_q5
on conflict (categoria_uso) do nothing;

-- conferência
-- select 'q14' t, count(*) from tabelas.q14_valor_terreno
-- union all select 'q3', count(*) from tabelas.quadro3_ca_zona
-- union all select 'q5', count(*) from tabelas.quadro5_fator_social;
