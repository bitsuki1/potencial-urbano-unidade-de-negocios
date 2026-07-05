# potencial-urbano-unidade-de-negocios
Projeto RAG jurídico IPTU/TDC — Potencial Urbano. Documento de fundação e pipeline.

> **COBERTURA DO CORPUS (honestidade — auditoria A-11, 2026-07-05):** o RAG indexado hoje é **PARCIAL e
> majoritariamente IPTU**: 19 de 31 leis fatiadas/indexadas; **0 leis exclusivamente TDC no corpus git**
> exceto a Lei 17.844/2022. A massa normativa **TDC** (Decreto 57.536/2016 e decretos ZEPEC/CONPRESP)
> **AINDA NÃO foi ingerida** — logo o RAG **não fundamenta consultas TDC-normativas** sobre esses textos
> (as tabelas TDC existem e o engine `pcpt.py` está provado, mas o texto-fonte de vários dispositivos que
> elas citam está fora do RAG). A consulta declara "CORPUS: PARCIAL" no veredito. Ingerir o TDC normativo
> é decisão de escopo do dono (BACKLOG).

## Boot / instanciação
Toda instância nova roda o **ritual de boot**: ler `PROXIMA-INSTANCIA.md` → `HANDOFF-E-PENDENCIAS.md` → `MANIFESTO.json` → `BACKLOG.md`, processar a `caixa-de-entrada/`, confirmar o chapéu no `REGISTRO-DE-INSTANCIAS.md` e, ao fechar, rodar `python3 scripts/fechar-instancia.py` (gate mecânico).

**Nota de divergência de nomenclatura (registrada p/ o checklist do escritório não reflagar):** o hook de boot deste repo chama-se **`.claude/hooks/surface-backlog.sh`**; o nome canônico no template do escritório é **`ignicao-projeto.sh`**. A **função é a mesma** (surfaça BACKLOG + caixa + estampa a linha no REGISTRO no boot). Divergência apenas de nome, aceita conscientemente — não renomeado para não quebrar referências já lavradas em docs. (Pedido em `caixa-de-entrada/processados/2026-07-03_escritorio_ack-e-orfas.md` §2.)
