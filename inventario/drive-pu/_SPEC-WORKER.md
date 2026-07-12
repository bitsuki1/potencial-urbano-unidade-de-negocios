# SPEC — Trabalhador de catálogo (TRAVADO) — DataLake "TODOS TDC" da pasta POTENCIAL URBANO

## 🚫 TRAVAS DURAS (violar = falha grave)
1. **PROIBIDO usar a ferramenta `Agent`.** **PROIBIDO usar a ferramenta `Task`/`TaskCreate`.** NÃO spawne subagentes, NÃO delegue, sob NENHUMA circunstância. Se sentir vontade de paralelizar: NÃO. Faça sequencial você mesmo.
2. Você cobre **APENAS a subárvore que te foi atribuída** (um id de pasta). Não saia dela. Não suba para a pasta-mãe.
3. Recurse VOCÊ MESMO, sequencialmente: mantenha uma LISTA Python de ids de pasta a visitar; retire uma, busque os filhos, escreva as linhas de arquivo, empilhe os ids de subpasta encontrados, repita até a lista esvaziar. Uma pasta por vez.

## Acesso ao Drive
`ToolSearch` `select:mcp__Google_Drive__search_files` → chame com query `parentId = '<id>'`, pageSize 100, excludeContentSnippets true. Pagine com nextPageToken até esgotar CADA pasta. NÃO leia conteúdo de arquivo (só metadados+título).

## Processar sem estourar contexto
Resultados grandes o MCP salva em disco (avisa o caminho .txt) — processe com `jq`/python a partir do arquivo. Há um transformador pronto: `inventario/drive-pu/_transform.py <json_file> "<path_label>" inventario/drive-pu/_indexed-ids.txt >> <seu_csv>`. Use-o (ele já faz triagem tema/tipo/oficialidade + cross-ref ja_indexado). Para resultados inline pequenos, salve o JSON num arquivo temporário e rode o mesmo transformador.

## Saída
Anexe as linhas em `/home/user/potencial-urbano-unidade-de-negocios/inventario/drive-pu/catalogo-lake-<NOME>.csv`. SEM cabeçalho (eu junto depois). `path_label` = caminho a partir da sua pasta raiz (ex.: "02_SILVER/Legislacao_Urbanistica/Decretos").

## Retorno (compacto — NÃO cole o CSV)
(1) total de arquivos; (2) total de pastas visitadas; (3) ja_indexado=NAO; (4) breakdown por tipo_artefato; (5) por tema; (6) top 5 maiores; (7) anomalias (duplicatas/versões/pastas de descarte/vazias); (8) caminho do CSV. Se o Drive MCP falhar: "FALHA: sem acesso ao Drive MCP" + erro.
