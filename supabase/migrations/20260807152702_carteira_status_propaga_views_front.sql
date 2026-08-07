-- Propaga status_carteira/status_motivo (decisão D do dono) pela cadeia que o FRONT lê:
-- motor4.cedentes (já tem) → motor4.carteira_preco_legal → public.v_carteira_preco_legal.
-- Sem isso a Carteira mostraria "—" em todas as linhas (o Lovable já consome os campos).
-- create or replace acrescenta colunas ao FIM; grants preservados.
-- Verificado na aplicação: view pública devolve 878 pronta_100 · 3.027 investigacao.
create or replace view motor4.carteira_preco_legal as
 SELECT c.sql_mestre,
    c.endereco,
    c.zona,
    c.ca_basico,
    c.area_terreno,
    c.valor_m2_venal_iptu2026,
    c.vtcd_q14_2026_m2,
    c.uso,
    c.padrao,
    p.v_outorga_m2_q14,
    p.v_outorga_max_q14,
    p.fi_aplicado,
    p.fsce_aplicado,
    p.pcpt_m2,
    p.m2_ja_transferido,
    p.saldo_pcpt_m2,
    p.preco_proxy_brl,
    p.regime_pcpt,
    p.cobertura_oficial,
    p.qualidade_estimativa,
    p.pendencia_calculo,
    p.memoria_calculo,
    c.status_carteira,
    c.status_motivo
   FROM motor4.cedentes c
     LEFT JOIN motor4.preco_legal p ON p.sql_mestre = c.sql_mestre;

create or replace view public.v_carteira_preco_legal as
 SELECT sql_mestre,
    endereco,
    zona,
    ca_basico,
    area_terreno,
    valor_m2_venal_iptu2026,
    vtcd_q14_2026_m2,
    uso,
    padrao,
    v_outorga_m2_q14,
    v_outorga_max_q14,
    fi_aplicado,
    fsce_aplicado,
    pcpt_m2,
    m2_ja_transferido,
    saldo_pcpt_m2,
    preco_proxy_brl,
    regime_pcpt,
    cobertura_oficial,
    qualidade_estimativa,
    pendencia_calculo,
    memoria_calculo,
    status_carteira,
    status_motivo
   FROM motor4.carteira_preco_legal;
