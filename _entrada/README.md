# _entrada/ — ZONA DE DESPEJO (onde o MOU sobe os documentos)
> Trazido pelo Escritório do MOU — 2026-06-17. **É aqui que você joga o material bruto.** O Escritório
> processa daqui para o pipeline (`leis/`, `jurisprudencia/`, `tabelas/`, ...) seguindo o `CLAUDE.md`.

## Como subir (MISTURADO é esperado — taguear é o trabalho)
> **Decisão do MOU (2026-06-17):** os documentos virão em VOLUME e **MISTURADOS (IPTU + TDC juntos)**. Não
> precisa separar na mão — **a triagem/tagueamento é uma das tarefas centrais do projeto** (Etapa 2 do pipeline).
- **Jogue tudo em `_entrada/misto/`** (ou em `iptu/`/`tdc/` se já souber — opcional). O Escritório classifica.
- **O trabalho de TAG:** cada documento recebe `tema` (IPTU/TDC), esfera, jurisdição, ano, tipo (Lei/Tabela/Fórmula/Tese)
  e vigência — primeiro por **regra determinística** (regex/heurística, de graça), depois o que sobrar vai ao modelo barato.
  O resultado vira o `.json` de metadados de cada item (schema no `CLAUDE.md` 2.4) e alimenta o `MANIFESTO.json`.
- **Nome do arquivo:** o mais descritivo possível ajuda a triagem (ex.: `lei-municipal-sp-15889-2013.txt`), mas não é obrigatório.

## Formato (regra do ambiente)
- **TEXTO/Markdown, CSV ou IMAGEM (.png/.jpg).** Evite **PDF** (o ambiente não lê PDF com confiança) — se só
  tiver PDF, suba assim mesmo que eu trato, mas o texto/imagem é muito melhor.
- **Bruto muito pesado / volume grande** → vai para o **Supabase Storage** (decisão de armazenamento do MOU,
  2026-06-17), não para o git. Me avise que eu organizo a subida; o git guarda o texto limpo + metadados.

## O que o Escritório faz com o que você subir (pipeline do CLAUDE.md)
1. **Ingestão** (hash, sem corrupção) → 2. **Triagem** determinística (IPTU×TDC, esfera, ano, dedup) →
3. **Extração pura** (só o que está no texto → `leis/<id>.md` + `.json`; tabelas → `tabelas/*.csv`) →
4. **Tese** (só a fração que exige raciocínio jurídico, com citação) → 5. **Consulta** (RAG híbrido).
- **Número nasce no engine, nunca no LLM** (Princípio 1.3); **toda afirmação cita a fonte** (1.7).
- Pode subir aos poucos — a varredura é incremental. Documento suspeito/ilegível não some: fica marcado para revisão.

> **Decisão do MOU (2026-06-20):** base inicial = **TDC** (o pipeline começa por TDC; IPTU replica depois).
