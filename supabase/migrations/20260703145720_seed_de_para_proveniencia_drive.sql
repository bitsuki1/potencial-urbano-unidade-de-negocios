-- S4 (escrutinio conjunto): popular o SSOT de proveniencia governanca.de_para com as
-- fontes canonicas do Drive (docs/INVENTARIO-DRIVE.md). Idempotente. So OFICIAL/ADQUIRIDO
-- entra como fonte; o que e NOSSO fica marcado CRIADO-POR-NOS/confianca baixa (nunca usar).

insert into governanca.de_para
  (drive_id, titulo, destino, origem, tipo, vigencia_inicio, vigencia_fim, substitui, substituido_por, proveniencia, oficialidade, confianca, observacao)
values
  ('1SMJ5NlYfloTSOKt_PwwI618OToAKZQUk','ZEPEC_BIR.shp','geo: lotes tombados (overlay Motor 3)','Drive:01-_entrada','arquivo',null,null,null,null,'GeoSampa/CONPRESP','OFICIAL','alta','Geometria dos lotes tombados BIR — overlay do Motor 3'),
  ('1gYeb5cYlFgVlYt87VZhCSFgdja4njttK','ZEPEC_AUE.shp','geo: vedacao Art.124 par.2 (M1/M3)','Drive:geo-mae','arquivo',null,null,null,null,'GeoSampa','OFICIAL','alta','Area de Urbanizacao Especial — camada espacial que derruba a premissa D1 do Motor 1'),
  ('1nSJNIe4lhxSGAuVgdY2bMbr0pkLyoQbN','ZEPEC_APP-BIR.shp','geo: vedacao Art.124 par.2 (M1/M3)','Drive:01-_entrada','arquivo',null,null,null,null,'GeoSampa','OFICIAL','alta','APP sobre BIR — camada espacial da vedacao Art.124 par.2'),
  ('1X0muNAcafJYXqb52GsI5Jn69gSnQ_Arc','ZEPEC_BIR_INDIC.shp','geo: apoio (Motor 3)','Drive:01-_entrada','arquivo',null,null,null,null,'GeoSampa','OFICIAL','media','Lotes indicados/em estudo para BIR'),
  ('1ds4u4ZpoLl_ySSIDywPbh_iicRCt6zNI','Pasta-mae GEO (SIRGAS_LOTES 96 distritos + ZEPEC + tematicos)','geo/ (M2/M3)','Drive:05-Geo','pasta',null,null,null,null,'GeoSampa','OFICIAL','alta','SIRGAS_SHP_LOTES oficiais que SUBSTITUEM os LOTES_*_IA nossos'),
  ('1vjYfo976BeZOAO893iMIv3dWafjbNXcE','SIRGAS_SHP_LOTES_70_SANTANA.shp (representativo da familia)','geo: lotes (Motor 3)','Drive:geo-mae','arquivo',null,null,null,null,'GeoSampa','OFICIAL','alta','Malha cadastral oficial — familia de 96 distritos na pasta-mae'),
  ('1WpeKCsz2EcovMBUVOJH79OPE39iWNDeD','SIRGAS_SHP_benstombados.shp','geo: tombados (M3/M1)','Drive:geo-mae','arquivo',null,null,null,null,'GeoSampa','OFICIAL','alta','Bens tombados — reforca ZEPEC_BIR'),
  ('1Cu7SIG_gxzk9ItsmT0dv2qYDDIrh5Ps1','SIRGAS_SHP_setorfiscal','geo: join IPTU (M2/M3)','Drive:geo-mae','arquivo',null,null,null,null,'GeoSampa','OFICIAL','alta','Chave setor fiscal — join geo x IPTU'),
  ('1VdbAkuqv3p_yKX_rO_ZUzGw5MOfVsxOo','SIRGAS_SHP_quadraMDSF','geo: join IPTU (Motor 3)','Drive:geo-mae','arquivo',null,null,null,null,'GeoSampa','OFICIAL','alta','Quadras fiscais — join com IPTU'),
  ('118bVYfXP9mpu8VIbm_4qBazI4fQfcFWG','SIRGAS_SHP_logradouronbl','geo: geocodificacao (Motor 3)','Drive:geo-mae','arquivo',null,null,null,null,'GeoSampa','OFICIAL','alta','Eixo de logradouros para geocodificar os 63 sem SQL'),
  ('17j94xkgVk4eberaRpRLK2j_ekz480Lny','lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx','gate Motor 1 (declaracoes)','Drive:01-_entrada','arquivo','2025-08-01',null,null,null,'Prefeitura de Sao Paulo','OFICIAL','alta','Fonte de verdade das declaracoes ZEPEC-BIR — gate do Motor 1'),
  ('1en2WC2A-Wd21NNDhZ8ThheAyHmODIOl-','lista_certidao_ZEPEC-BIR_agosto-2025.xlsx','gate Motor 1 (certidoes)','Drive:01-_entrada','arquivo','2025-08-01',null,null,null,'Prefeitura de Sao Paulo','OFICIAL','alta','Fonte de verdade das certidoes ZEPEC-BIR emitidas — gate do Motor 1'),
  ('1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM','IPTU_2026.csv','bronze Motor 2 (oficiais.iptu2026_cedentes)','Drive:01-_entrada','arquivo','2026-01-01','2026-12-31',null,null,'PMSP cadastro IPTU 2026','OFICIAL','alta','937MB; recorte cedentes ja em oficiais.iptu2026_cedentes'),
  ('1AV8v4esuCxGulgxvGskzo595vycDa3U-','iptu-2020-cep01.csv','bronze Motor 2 (historico)','Drive:01-_entrada','arquivo','2020-01-01','2020-12-31',null,null,'PMSP IPTU 2020','OFICIAL','media','Historico para serie temporal'),
  ('154dJZeFloDrPrYXd8WMjaJErd9i168ER','PDE2013 Quadro 3 CA por zona (Tab_1)','tabelas: quadro3_ca (Motor Calculo)','Drive:tabelas-csv','arquivo',null,null,null,null,'derivado do PDE 2013 Quadro 3 (extracao NOSSA)','NAO-OFICIAL','media','Extracao NOSSA — revisar contra o dispositivo antes de usar como fonte'),
  ('1LHT2NfOmbzDS05gLytYY7i7iwyaKPShm','PDE2013 Quadro 5 Fator social Fs','tabelas: quadro5_fs','Drive:quadros-md','arquivo',null,null,null,null,'derivado do PDE 2013 Quadro 5 (extracao NOSSA)','NAO-OFICIAL','media','Extracao NOSSA — revisar contra o dispositivo'),
  ('1l0MZR786o_qdP0FREoBQMuwzkswGg_8e','Arvore de docs societarios (CNPJ)','Motor 6 PROP (fora de M1-M3)','Drive','pasta',null,null,null,null,'Receita Federal (adquirido)','CRIADO-POR-TERCEIROS','alta','Societario adquirido — Motor 6, fora do escopo vendedor atual'),
  ('1EyzQ9O6HTbiUSBgotHYBun_haesZHGC_','LOTES_Parte_1_IA.csv','NAO USAR','Drive','arquivo',null,null,null,'1vjYfo976BeZOAO893iMIv3dWafjbNXcE','derivado NOSSO dos lotes','CRIADO-POR-NOS','baixa','PROIBIDO como fonte (D-DONO-4). Substituido pelos SIRGAS_SHP_LOTES oficiais.'),
  ('1tbhRdfpD4pHeRl3wHSfusCBoNqCffn2xPJqSDhL05D8','DOCUMENTO MESTRE SISTEMA OPERACIONAL HOLDING TDC (gdoc)','NAO USAR','Drive','arquivo',null,null,null,null,'analise NOSSA','CRIADO-POR-NOS','baixa','Doc de analise nosso — nao e fonte'),
  ('1KAvM0NuHZzDo6jE-4BUX_CDBmIWXfi2m','Modelo Reduzido IPTU.xlsx','NAO USAR','Drive','arquivo',null,null,null,null,'planilha-modelo NOSSA','CRIADO-POR-NOS','baixa','Planilha-modelo nossa — nao e fonte')
on conflict (drive_id) do update set
  titulo=excluded.titulo, destino=excluded.destino, origem=excluded.origem, tipo=excluded.tipo,
  vigencia_inicio=excluded.vigencia_inicio, vigencia_fim=excluded.vigencia_fim,
  substitui=excluded.substitui, substituido_por=excluded.substituido_por,
  proveniencia=excluded.proveniencia, oficialidade=excluded.oficialidade,
  confianca=excluded.confianca, observacao=excluded.observacao;

insert into governanca.registro_decisoes (id, categoria, titulo, descricao, status, fonte, data)
values
  ('D-CANON-01','arquitetura','Canonicidade do schema: git == banco vivo','As 5 migrations vivas (oficiais.*, governanca.*, storage, extensoes) passam a ter .sql no git; as 3 migrations 20260624_010/020/030 (schema receptor, nunca aplicadas) foram arquivadas em _nao-aplicadas-receptor. db reset reproduz producao.','vigente','ESCRUTINIO-CONJUNTO-MOTORES.md S1/M2-E6', current_date),
  ('D-CANON-02','arrumacao','Proveniencia (de_para) populada com o Drive','governanca.de_para (antes vazio) recebe as fontes canonicas do Drive com oficialidade/vigencia/confianca (1.6 + D-DONO-4). LOTES_*_IA marcado CRIADO-POR-NOS e substituido pelos SIRGAS oficiais.','vigente','ESCRUTINIO-CONJUNTO-MOTORES.md S4 + docs/INVENTARIO-DRIVE.md', current_date)
on conflict (id) do update set
  categoria=excluded.categoria, titulo=excluded.titulo, descricao=excluded.descricao,
  status=excluded.status, fonte=excluded.fonte, data=excluded.data;
