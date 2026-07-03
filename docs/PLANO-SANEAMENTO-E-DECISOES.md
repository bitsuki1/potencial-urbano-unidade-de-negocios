> **⚠️ SUPERADO (2026-06-20) por `drive-arrumacao/SANEAMENTO-DUPLICATAS-DRIVE-2026-06-20.md`.** Documento histórico (2026-06-18); não usar como plano vivo. IDs canônicos do Drive foram reconciliados depois (B-8/AUD-02). _(banner lavrado pela PU 17, 2026-07-03 — DoD do B-8.)_

PLANO DE SANEAMENTO E DECISÕES — IPTU + TDC (Anexo de Execução)

Escritório do MOU — Projeto Potencial Urbano | Data: 2026-06-18

Documento-pai (inventário + estratégia): "MAPA IPTU + TDC — Inventário Classificado e Estratégia de Tratamento"

https://docs.google.com/document/d/1WB3AHhrZYxxItRPqljwLaRsJ4OgUStFucx5vNvcx3J4/edit

==================================================================

1. DECISÕES DO MOU (2026-06-18)

==================================================================

D-1  Foco primário agora: SANEAMENTO / ORGANIZAÇÃO PRIMEIRO (arrumar antes de avançar — D27).

D-2  Tratamento de duplicatas: SÓ MOVER (reversível) para "_ARQUIVO_SANEAMENTO"; NÃO excluir.

D-3  Inteligência operacional (motores/Gems/.md/.json/prompts): VERSIONAR no git (repo potencial-urbano).

D-4  Arquivos "compartilhados comigo" (ex.: PROSPECCAO_TDC_MULTI_CHAVES.xlsx): INCLUIR numa próxima varredura.

==================================================================

2. LIMITAÇÃO DE FERRAMENTA (transparência)

==================================================================

O conector do Google Drive desta sessão expõe apenas: buscar, ler, baixar, metadados, permissões, COPIAR e CRIAR.

NÃO expõe: mover (re-parent), renomear, enviar para lixeira ou excluir.

Consequência: o passo físico de saneamento (mover/arquivar cópias) precisa ser executado por VOCÊ na interface do Drive,

ou por uma automação com escopo de escrita (Apps Script / API com permissão drive.file). Este documento entrega a

WORKLIST exata para essa execução. A inteligência (D-3) eu CONSIGO versionar no git (tenho acesso ao repositório).

==================================================================

3. WORKLIST DE SANEAMENTO — PRIORIDADE 1: BASES PESADAS (maior ganho, risco baixo)

==================================================================

REGRA: manter UMA cópia canônica por base; MOVER as demais para "_ARQUIVO_SANEAMENTO/dados_pesados".

ANTES de tratar como idênticas, CONFERIR o tamanho em bytes (mesmo byte-size = cópia bit-a-bit). Onde o tamanho

diverge, é re-extração — preservar a mais recente/íntegra e revisar antes de arquivar.

[A] socios.csv — ~3,44 GB (Receita Federal: quadro societário)

    MANTER (canônica): 1ncSTA-P2GfV2cPN-y1f2cnjqFDGSqa9e  (POTENCIAL URBANO ATUAL/Não Oficiais)

    MOVER p/ arquivo:  1Lffz6w6OvS-5KqakDT71ZqIzsudRLnoI  (dados_pericia5)

    Ganho: ~3,44 GB.

[B] empresas.csv — ~2,27 GB (cadastro CNPJ)

    MANTER: 1u0ZaQCqfG0Moq2eroL-8_E1njnHJbgP5  (Não Oficiais)

    MOVER:  18Q-_8iD5ZihVh-UnmD4itZ8WEa19g02a  (dados_pericia5)

    Ganho: ~2,27 GB.

[C] holdings.csv — ~60 MB

    MANTER: 1LGUIQysj-1_8deN8AeQi5ChwORjyoWHR  (Não Oficiais)

    MOVER:  1lBfWs1FCsxCTgpAu_5WzbZJ8WnLodxi9  (dados_pericia5)

[D] IPTU_2026.csv — ATENÇÃO: há tamanhos DIFERENTES (937,9 MB vs 894 MB) = extrações distintas, NÃO bit-idênticas.

    CONFERIR qual é a íntegra/atual antes de arquivar. Cópias conhecidas (≥7):

      937,9 MB: 1A3NK8K6wAn4ZjGCl5rqb2mCB8j50t0Pl (IPTU 12-05)

      894 MB:   1EubfSLtbGNF5G2MLS9eT_DiAsVCtv0fM (XLS1)

      + 1oX6BDTF_MJhrt8es4xh3N-cFtDbeoNGt, 13rAbexq2GxyPHot5_RjmhzuZx94F7dG9, e outras.

    Recomendação: eleger 1 canônica (a íntegra mais recente), arquivar as demais. Ganho potencial ~5,6 GB.

[E] iptu-2020-cep01.csv — ~153 MB (≥8 cópias)

    MANTER 1 (ex.: 1n78kuJjKwRcSOWeYYqWjIuCLJmjK_6TE); MOVER as demais (11akLKBJStGa3jcfdXjBEn-mqQznl_Yax, etc.).

Subtotal P1 recuperável estimado: ~12–16 GB.

==================================================================

4. WORKLIST — PRIORIDADE 2: ÁRVORES-ESPELHO E LIXEIRAS

==================================================================

- DECIDIR a árvore canônica entre "DataLake_TDC" e "TODOS TDC" (são espelhos). Manter UMA; arquivar a outra inteira

  APÓS conferência (VACINA: triar shapefiles/.gpkg dentro das lixeiras — podem ser geodados únicos).

- Esvaziar para "_ARQUIVO_SANEAMENTO": 99_LIXEIRA_DUPLICADOS, 99_QUARENTENA_DUPLICADOS, 99_PARA_DELETAR_DUPLICADOS,

  MOTOR_1_Markdown_Limpo, 00_TABELAS_EXTRAIDAS_DOS_PDFS, "PASTA UNICA"/"CSV PASTA UNICA".

- PRESERVAR a camada 02_SILVER_STAGED (única com taxonomia temática) como base do destino curado.

- Legislação re-uploadada 3× no "Google AI Studio": manter 1 conjunto; arquivar 2.

==================================================================

5. WORKLIST — PRIORIDADE 3: DOCUMENTOS-ÂNCORA DUPLICADOS

==================================================================

- "Memorial de Fundamentação Estratégica": manter o Google Doc 1VM5iOyzkVSiQxqjp1O8t6c3EzfdYYNlPKYXgqHWeObk;

  arquivar as ~15–35 derivadas (pdf/csv/md/doc).

- "fila_tdc_5porcento_fundurb": manter 1 pdf + 1 csv oficial; arquivar fragmentos _PART_/_Pagina_/_Pag_.

- "manifesto_data_lake_tdc.json": manter o Google Doc 1emeA6wXOKiz0b3u5qLR4Wjw3YA9cAV2XZS1r4akqLzo.

- "GatewayCertificaPDF/GatewayPDF": manter 1–2 originais; arquivar ~50 variantes.

==================================================================

6. ORGANIZAÇÃO-ALVO (taxonomia curada única, por EIXO)

==================================================================

Criar uma árvore única "POTENCIAL URBANO — CURADO" com:

  A_DOCS_MESTRE/ (IPTU + TDC, 1 SSOT por tema)

  B_MOTORES_E_IA/ (espelho do que vai p/ git — D-3)

  C_JURIDICO/ (leis, jurisprudência, doutrina — 1 cópia cada)

  D_GEOESPACIAL/ (shapefiles completos + mapas PDF; completar os 13 distritos sem .shp)

  E_ENRIQUECIMENTO/ (1 cópia de socios/empresas/holdings/IPTU/ITBI + planilhas consolidadas)

  F_TDC_OFICIAL/ (TDC OFICIAL, fila FUNDURB, certidões, declarações SMUL)

  G_COMERCIAL/ (Comissão PU, contratos, forms, CRM)

  H_MEMORIAIS/ (auditorias/validações)

  _ARQUIVO_SANEAMENTO/ (tudo que sai de circulação, reversível)

==================================================================

7. FASE 0 — SSOT (decisões que só o MOU pode tomar)

==================================================================

S-1  Qual é o doc-mestre canônico de TDC? (candidatos: CODEX_TDC_MASTER 1bZ3Awl…, DOCUMENTO MESTRE HOLDING TDC

     1tbhRdfp…, ou consolidar um novo a partir deles + Memoriais). Recomendação do Escritório: consolidar UM "CODEX TDC

     v-final" tendo CODEX_TDC_MASTER como base e absorvendo Holding + Memoriais V9.0; aposentar CODEX/codex omega/BÍBLIA.

S-2  Doc-mestre canônico de IPTU: recomendação = "Mestre IPTU" (1h-hlgv…), absorvendo Estudo_Profundo + Documento Base IA.

S-3  Qual árvore de data lake é a canônica: DataLake_TDC ou TODOS TDC?

==================================================================

8. INTEGRIDADE GEOESPACIAL A CORRIGIR (bloqueio de precificação)

==================================================================

13 distritos de LOTES SEM geometria (.shp ausente; só .dbf/.shx): 11_BRASILANDIA, 22_CIDADE_ADEMAR,

29_FREGUESIA_DO_O, 30_GRAJAU, 36_ITAIM_PAULISTA, 38_JABAQUARA, 63_PIRITUBA, 68_SACOMA, 70_SANTANA,

76_SAPOPEMBA, 81_TREMEMBE, 82_TUCURUVI, 92_VILA_MEDEIROS. Também benstombados/planoacao/planomacro com tripé

shp/shx/dbf incompleto. Ação: rebaixar do GeoSampa as camadas faltantes.

==================================================================

9. PRÓXIMO PASSO EXECUTÁVEL PELO ESCRITÓRIO (sem depender de mover/excluir)

==================================================================

D-3 (versionar inteligência no git) é executável JÁ: baixar do Drive os motores/Gems/.md/.json/prompts e commitá-los

no repo potencial-urbano (branch claude/iptu-tdc-document-mapping), criando o SSOT versionado da inteligência +

este inventário em markdown. Aguardando "go" do MOU para iniciar.
