-- Decisão do dono (2026-08-07, mensagem D): coluna de STATUS na carteira — tratar primeiro
-- as 100% prontas; as demais ficam "investigação" COM O MOTIVO explícito (nada de valor
-- duplicado/inventado: órfão do Q14 segue NULL). Recria a view acrescentando 2 colunas ao FIM
-- (create or replace preserva grants). Nenhum número novo nasce aqui (1.3) — só classificação.
-- ⚠️ CRITÉRIO CORRIGIDO pela 20260807140952 (pendência 'OK…' é nota de completo, não pendência)
-- — o estado FINAL da view é o da migração seguinte; esta fica pelo histórico (nada se apaga).
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
           and coalesce(p.pendencia_calculo, '') = ''
      then 'pronta_100'
      else 'investigacao'
    end as status_carteira,
    case
      when c.area_terreno is not null and z.ca_basico is not null
           and q.valor_m2_brl is not null and p.preco_proxy_brl is not null
           and coalesce(p.pendencia_calculo, '') = ''
      then null
      else concat_ws('; ',
        case when c.area_terreno is null then 'sem área de terreno (cadastro IPTU)' end,
        case when z.ca_basico is null then 'sem zona/CA básico (geocodificação autorizada, em curso)' end,
        case when q.valor_m2_brl is null then 'sem VTcd publicado no Quadro 14 (fica NULL até fonte oficial)' end,
        case when p.preco_proxy_brl is null then 'sem preço legal calculado pelo engine' end,
        nullif(p.pendencia_calculo, ''))
    end as status_motivo
   FROM motor4.c_iptu2026_cedentes c
     LEFT JOIN motor4.c_zona_por_cedente z ON z.sql_mestre = c.sql_mestre
     LEFT JOIN motor4.c_q14_cedentes_2026_oficial q ON q.sq = "left"(c.sql_mestre, 6)
          AND replace(q.codlog, '-'::text, ''::text) = replace(c.codlog, '-'::text, ''::text)
     LEFT JOIN motor4.preco_legal p ON p.sql_mestre = c.sql_mestre;

comment on view motor4.cedentes is 'Carteira de cedentes (produto). Dois preços NOMEADOS (venal IPTU × VTcd Q14); preço legal do engine Art. 128 com memória e pendência; status_carteira = pronta_100 (todos os insumos + preço, sem pendência) × investigacao (status_motivo diz o porquê). Órfãos do Q14 = NULL por decisão do dono (2026-08-06/07).';
