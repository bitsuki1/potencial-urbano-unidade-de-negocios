-- Correção do critério da carteira_status_v1: pendencia_calculo que começa com 'OK' é NOTA de
-- cálculo completo, não pendência (878 cedentes carregam "OK (Atc+CAbás+V) — cálculo completo").
-- pronta_100 = todos os insumos + preço + pendência vazia OU 'OK…'. O resto = investigacao com motivo.
-- Placar na aplicação (2026-08-07): 878 pronta_100 · 3.027 investigacao.
create or replace view motor4.cedentes as
 SELECT c.sql_mestre,
    c.endereco,
    z.zona,
    z.ca_basico,
    c.area_terreno,
    c.valor_m2_terreno AS valor_m2_venal_iptu2026,
    q.valor_m2_brl AS vtcd_q14_2026_m2,
    c.uso,
    c.padrao,
    p.pcpt_m2,
    p.saldo_pcpt_m2,
    p.preco_proxy_brl,
    p.regime_pcpt,
    p.qualidade_estimativa,
    p.cobertura_oficial,
    p.memoria_calculo,
    p.pendencia_calculo,
    case
      when c.area_terreno is not null and z.ca_basico is not null
           and q.valor_m2_brl is not null and p.preco_proxy_brl is not null
           and (coalesce(p.pendencia_calculo, '') = '' or p.pendencia_calculo like 'OK%')
      then 'pronta_100'
      else 'investigacao'
    end as status_carteira,
    case
      when c.area_terreno is not null and z.ca_basico is not null
           and q.valor_m2_brl is not null and p.preco_proxy_brl is not null
           and (coalesce(p.pendencia_calculo, '') = '' or p.pendencia_calculo like 'OK%')
      then null
      else concat_ws('; ',
        case when c.area_terreno is null then 'sem área de terreno (cadastro IPTU)' end,
        case when z.ca_basico is null then 'sem zona/CA básico (geocodificação autorizada, em curso)' end,
        case when q.valor_m2_brl is null then 'sem VTcd publicado no Quadro 14 (fica NULL até fonte oficial)' end,
        case when p.preco_proxy_brl is null then 'sem preço legal calculado pelo engine' end,
        case when p.pendencia_calculo is not null and p.pendencia_calculo not like 'OK%' then p.pendencia_calculo end)
    end as status_motivo
   FROM motor4.c_iptu2026_cedentes c
     LEFT JOIN motor4.c_zona_por_cedente z ON z.sql_mestre = c.sql_mestre
     LEFT JOIN motor4.c_q14_cedentes_2026_oficial q ON q.sq = "left"(c.sql_mestre, 6)
          AND replace(q.codlog, '-'::text, ''::text) = replace(c.codlog, '-'::text, ''::text)
     LEFT JOIN motor4.preco_legal p ON p.sql_mestre = c.sql_mestre;
