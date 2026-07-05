# Melhorias de processo (beta contínuo) — PU 14, 2026-06-29
> Retrospectiva do método desta sessão. Foco no COMO, não no quê. Para a unidade e para o escritório (PMO).

## O que FUNCIONOU (manter/repetir)
1. **Loop "triplo-limpo" com agentes adversariais em LENTES DIFERENTES** — maior ROI. Pegou bugs que a 1ª implementação passou em verde: chave SQL multi-lote divergente, dono OODC perdendo 322/502 linhas, sensor de liquidez que sairia INVERTIDO, Fi=1 errado (Art.24). **Lentes diferentes** (não re-rodar a mesma) evita falsa convergência.
2. **Verbatim-para-git** como ingestão: cru imutável em `raw/` + proveniência (fileId) versionada; transformação toda a jusante e rastreável.
3. **Separação por artefato** (3 codexes) — materializa 1.1; preço PARADO em vez de inventado; número no engine.
4. **Prova vs. inferência** na classificação ("só pula com ESGOTADO escrito; falta de dado = verificar, nunca morto").
5. **Gate mecânico** de fechamento (DoD = prova) + **estado DERIVADO, não declarado** (pega falso-verde).

## O que FALHOU / foi arriscado
1. **Bugs silenciosos por SCHEMA DO BRUTO PRESUMIDO** — quase todos os achados eram ambiguidade de coluna/formato não validada antes de codar (esgotado lido por coincidência; somatória all-time; dono `/`; Fi duplo).
2. **Validação legal feita por ÚLTIMO** — quase produziu semântica jurídica errada (transferir≠vender na doação; Fi por área; ESGOTADO temporal). Devia ser gate de ENTRADA do desenho.
3. **Dependência externa (Atc) descoberta tarde** — engine montado sem o insumo que se sabia necessário.
4. **Parser xlsx ad-hoc** (base64→stdlib) frágil (origem do bug US/BR, datas seriais).
5. **Sem teste de regressão** — bugs corrigidos não viraram vacina automatizada.

## Melhorias para a UNIDADE (Potencial Urbano)
1. **Etapa 0.5 — "contrato de schema do bruto"** antes de codar: por fonte, documentar índice→significado de cada coluna, formato (BR/US), separador de multi-valor, grão da linha, casos sujos. Ataca a raiz dos bugs silenciosos.
2. **Auditoria legal como GATE DE ENTRADA** do desenho (não só de saída).
3. **Mapa de dependências de dados** no início (interno×externo×ausente) — sinaliza bloqueios cedo.
4. **Helper único e testado de ingestão** de planilha (multi-sheet, datas Excel, BR/US).
5. **Suíte de vacinas** — 1 teste de regressão por bug pego, rodado no gate.

## Melhorias para o ESCRITÓRIO (PMO/portfólio) — padrões reutilizáveis
1. **Protocolo "auditoria triplo-limpo por lentes adversariais"** como SSOT do portfólio: N agentes read-only, cada um numa lente distinta (código · dado/produto · norma/domínio · doutrina), convergência num laudo; "re-rodar a mesma lente = teatro".
2. **"Verbatim-para-git"** como padrão de ingestão de qualquer fonte externa (cru imutável + proveniência).
3. **"Separação por artefato"** como template de repo (engine determinístico × prosa; número nasce no engine).
4. **Gate mecânico de fechamento** parametrizável de portfólio (lição: "dois gates que discordam é pior que um").
5. **"Estado derivado, nunca declarado"** como regra transversal (pega falso-verde em qualquer unidade).
6. **Checklist de abertura:** "contrato de schema do bruto" + "mapa de dependências de dados" — previnem as duas maiores fontes de retrabalho (schema presumido; insumo externo tarde).
