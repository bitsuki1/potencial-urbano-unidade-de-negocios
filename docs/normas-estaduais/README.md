# Normas ESTADUAIS — capturadas, FORA do corpus de uso

Esta pasta guarda normas **estaduais** capturadas verbatim da fonte oficial, **fora** do corpus de RAG
(`leis/`). Elas **não** entram na busca nem são fonte de trabalho — ficam aqui **documentadas e rastreáveis**
(doutrina "nada se joga fora") para o caso de o dono abrir uma frente que precise delas.

**Por que fora do corpus:** o produto é de **IPTU/TDC municipais de São Paulo**. Uma norma estadual, se
indexada em `leis/`, poluiria o retrieval municipal (o `fatiar.py` varre `leis/**/*.md` e indexaria tudo).
Mantê-las aqui respeita a decisão do dono ("documentar, não usar") sem arriscar o gate.

**Como promover uma para uso (só sob decisão do dono):** mover o `.md`/`.json` para `leis/estadual/`,
ajustar `no_corpus: true`, e rodar `fatiar`+`indexar` — mas isso **só** quando a frente correspondente for
aberta.

| Arquivo | Norma | Regula | Motivo de estar aqui |
|---|---|---|---|
| `decreto-estadual-59263-2013` | Decreto estadual SP 59.263/2013 | Lei estadual 13.577/2009 (solo contaminado / áreas contaminadas) | Estadual, não é IPTU/TDC municipal |
