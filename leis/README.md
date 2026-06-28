# leis/ — Artefato **LEI / NORMA** (RO-03, princípio 1.1)

> **O que mora aqui:** o TEXTO NORMATIVO limpo (constituição, leis, decretos, súmulas vão em `jurisprudencia/`).
> Vira **RAG** (fatiado por dispositivo → indexado → consultável com citação). **Só fonte OFICIAL vira lei** (RO-08).

## Estrutura
- `federal/` — normas federais (12 indexadas verbatim).
- `municipal-sp/` — normas do município de SP (1 indexada: 7.228/1968; **14 ainda só resumo** → re-ingerir verbatim, B-4/B-9).

## Par obrigatório por norma: `<id>.md` + `<id>.json`
- **`.md`** = texto integral. Para entrar no RAG precisa do cabeçalho `## Texto integral (verbatim)` — a guarda do `fatiar.py` recusa resumo (D-06). Resumo no RAG mente sobre a fonte (1.7).
- **`.json`** = metadados (schema em `CLAUDE.md` 2.4): id, tipo_norma, esfera, vigência{início,fim,revogada_por,...} (1.6), remissões, `confianca_extracao`, `status_pipeline`, `fonte{url oficial,hash,ocr}`.

## Como uma lei ENTRA (re-ingestão interna)
Cru em `_entrada/` → `python3 scripts/promover_entrada.py <id>` (escreve `.md` verbatim + `.json confianca:alta`) → `scripts/fatiar.py` → indexa. O estado de cada uma vive no `MANIFESTO.json` (gerado), nunca contado à mão.
