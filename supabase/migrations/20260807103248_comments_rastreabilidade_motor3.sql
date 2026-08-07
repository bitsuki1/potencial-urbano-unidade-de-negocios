-- Varredura #4 (turno noturno 2026-08-07): rastreabilidade 1.3/1.7 NO BANCO — o fonte_legal
-- do tabelas/METADATA.json (SSOT no git) espelhado como COMMENT ON TABLE em cada motor3.t_*.
-- Quem consome direto do banco passa a ver a origem legal sem abrir o repo.
comment on table motor3.t_fatores_tdc is 'Fonte legal: INVENTARIO derivado dos fatores de TDC (nao e tabela de lei; aponta a fonte de cada fator) — SSOT: tabelas/fatores-tdc.csv (METADATA.json).';
comment on table motor3.t_fi_incentivo_doacao is 'Fonte legal: PDE Lei 16.050/2014, Art. 127 §1º (incisos I-V) — SSOT: tabelas/fi-incentivo-doacao.csv (METADATA.json).';
comment on table motor3.t_fi_zepec_area_lpuos is 'Fonte legal: LPUOS Lei 16.402/2016, Art. 24 (incisos I-VII) — SSOT: tabelas/fi-zepec-area-lpuos.csv (METADATA.json).';
comment on table motor3.t_ipca_numero_indice_ibge is 'Fonte legal: IBGE/SIDRA tabela 1737 (IPCA numero-indice, base dez/1993=100) — insumo da correcao do Art. 128 §2º (PDE) — SSOT: tabelas/ipca-numero-indice-ibge.csv (METADATA.json).';
comment on table motor3.t_iptu_fator_obsolescencia is 'Fonte legal: Lei 10.235/1986, Tabela IV (redacao da Lei 11.152/1991) c/c Arts. 11 e 16 — SSOT: tabelas/iptu-fator-obsolescencia.csv (METADATA.json).';
comment on table motor3.t_iptu_fatores_terreno is 'Fonte legal: Lei 10.235/1986, Tabelas II e III na redacao da Lei 11.152/1991 (+ item ZER pela 15.889/2013) — SSOT: tabelas/iptu-fatores-terreno.csv (METADATA.json).';
comment on table motor3.t_iptu_valor_construcao_m2 is 'Fonte legal: Lei Municipal SP 18.330/2025, Anexo I (Tabela VI) — valores do EXERCICIO 2026 (substitui a Tabela VI da Lei 10.235/1986) — SSOT: tabelas/iptu-valor-construcao-m2.csv (METADATA.json).';
comment on table motor3.t_limiar_parque_art127 is 'Fonte legal: Decreto 64.884/2025, Art. 3º (atualiza o valor de referência do Art. 127 §1º IV/V da Lei 16.050/2014) — SSOT: tabelas/limiar-parque-art127.csv (METADATA.json).';
comment on table motor3.t_q14_reajuste_anual is 'Fonte legal: Decretos 59.166/2019 (+2%), 62.135/2022 (+5%), 63.108/2023 (+5%), 63.999/2024 (+4,5%), 64.884/2025 (+7,18%), Art. 1º de cada — reajuste do Quadro 14 (Cadastro de Valor de Terreno para Outorga) da Lei 16.050/2014 — SSOT: tabelas/q14-reajuste-anual.csv (METADATA.json).';
comment on table motor3.t_q14_valor_terreno is 'Fonte legal: PDE Lei 16.050/2014, Quadro 14 (Anexo) — SSOT: tabelas/q14-valor-terreno.csv (METADATA.json).';
comment on table motor3.t_quadro2a_ca_macroarea is 'Fonte legal: PDE Lei 16.050/2014, Quadro 2A (Anexo) — SSOT: tabelas/quadro2a-ca-macroarea.csv (METADATA.json).';
comment on table motor3.t_quadro3_ca_por_zona is 'Fonte legal: LPUOS Lei 16.402/2016, Quadro 3 — SSOT: tabelas/quadro3-ca-por-zona.csv (METADATA.json).';
comment on table motor3.t_quadro5_fator_social_fs is 'Fonte legal: PDE Lei 16.050/2014, Quadro 5 (Anexo) — SSOT: tabelas/quadro5-fator-social-fs.csv (METADATA.json).';
comment on table motor3.t_quadro6_fator_planejamento_fp is 'Fonte legal: PDE Lei 16.050/2014, Quadro 6 (Anexo) — SSOT: tabelas/quadro6-fator-planejamento-fp.csv (METADATA.json).';
comment on table motor3.t_quadro7_parques is 'Fonte legal: PDE Lei 16.050/2014, Quadro 7 (Anexo) — SSOT: tabelas/quadro7-parques.csv (METADATA.json).';
