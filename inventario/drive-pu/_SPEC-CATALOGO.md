# SPEC — Catálogo da pasta POTENCIAL URBANO do Drive (PU 19, 2026-07-12)

Missão do dono: catalogar, organizar, taguear e ler TODO o drive de PU = a pasta **POTENCIAL URBANO**
(`1BrM6q36meTtn5guJoiGbqvCtZF11Uau3`), dentro de PORTFÓLIO DO MOU. Escopo: SÓ essa pasta e subpastas.

## Como acessar o Drive
`ToolSearch` query `select:mcp__Google_Drive__search_files` → chame com:
- query: `parentId = '<FOLDER_ID>'` (lista filhos: arquivos E pastas)
- pageSize: 100, excludeContentSnippets: true
- pagine com nextPageToken até esgotar.
Recurse: para cada filho que for pasta (`mimeType = application/vnd.google-apps.folder`), repita para o id dela,
acumulando o caminho (path = "PastaMãe/Subpasta/...").

## NÃO ler conteúdo de arquivo (só metadados + título). Essa é a fase de MAPEAR/TAGUEAR, não de LER a fundo.

## Colunas do CSV (vírgula; aspas quando o valor tiver vírgula)
`drive_id,path,nome,mime,ext,bytes,created,modified,tema,tipo_artefato,oficialidade,ja_indexado,observacao`
- path = caminho relativo dentro da POTENCIAL URBANO (ex.: "02 — Leis & Jurisprudência/2.1 PDE").
- tema (pelo título/pasta): TDC | IPTU | GEO | JURIDICO | GOVERNANCA | OUTRO.
- tipo_artefato: LEI | DECRETO | PORTARIA | JURISPRUDENCIA | TABELA_DADO | PLANILHA | CODEX_DOC | AUDITORIA | ENGINE_CODIGO | GEO_SHP | RASCUNHO | FORMULARIO | DOC_GOOGLE | PDF | OUTRO.
- oficialidade (heurística do título): OFICIAL (lei/decreto/portaria/diário oficial/prefeitura/SIRGAS/GeoSampa) | NOSSO (codex/auditoria/inventário/base/dossiê/memorial/análise nossos) | ADQUIRIDO | DESCONHECIDO.
- ja_indexado = SIM se o drive_id aparece em `inventario/INDICE-MESTRE-DRIVE.csv` (grep), senão NAO.
- observacao: curta. Marque duplicata (mesmo nome), versão (v1_2/v2.0/FINAL), gigante (>100MB), ou "pasta duplicada".

## Saída
Escreva em `/home/user/potencial-urbano-unidade-de-negocios/inventario/drive-pu/catalogo-<PARTE>.csv` (com cabeçalho).

## Retorno (compacto, sem colar o CSV)
(1) total de arquivos; (2) total de subpastas visitadas; (3) quantos ja_indexado=NAO; (4) breakdown por tipo_artefato;
(5) breakdown por tema; (6) top 5 maiores; (7) anomalias (duplicatas/versões/pastas repetidas); (8) caminho do CSV.
Se o Drive MCP falhar: retorne "FALHA: sem acesso ao Drive MCP" + o erro.
