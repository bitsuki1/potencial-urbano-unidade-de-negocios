# Depósito ao Escritório do MOU — encerramento comercial PU + melhorias de portfólio
> Da unidade **Potencial Urbano** (PU 14) para o **Escritório do MOU** (PMO) · 2026-06-29.
> Canal D44. Esta unidade NÃO escreve no `escritorio-do-mou` (D120) — deposita aqui para o maestro relayar.

## 1. O que a unidade entregou (frente comercial TDC, lado cedente)
Base+ferramenta ZEPEC (6.131 imóveis: estado de venda·negociável·dono·m²·FUNDURB), lista de prospecção (2.740), 3 codexes (Comercial/Cálculos/Precificação), engine cedente de 2 vias. Tudo no git, gate VERDE. Detalhe: `zepec/HANDOFF-COMERCIAL-PU14-2026-06-28.md`, `docs/AUDITORIA-PROFUNDA-2026-06-29.md`, `docs/ROADMAP-PROJETO.md`.

## 2. Honestidade (o que NÃO está pronto — para o PMO não superestimar)
- Engine de potencial **nunca rodou sobre imóvel real** (falta Atc/IPTU); **R14 (validação) não rodou**.
- Cobertura de **dono = 79 cedentes** (1,8%), não os 4.965 do arquivo derivado.
- **Preço PARADO** (decisão do MOU); FUNDURB = valor regulatório, sensor de liquidez INDETERMINADO.
- Destrava tudo: **Supabase (IPTU/ITBI/sócios/geo)** + decisão **B-17** (PR ao main protegido).

## 3. Melhorias de PROCESSO propostas ao portfólio (reutilizáveis por qualquer unidade)
1. **Protocolo "auditoria triplo-limpo por lentes adversariais"** como SSOT do escritório: N agentes read-only, cada um numa lente distinta (código · dado/produto · norma/domínio · doutrina), laudo por convergência; regra "re-rodar a mesma lente = teatro". **Foi o método de maior ROI da sessão** (pegou 4+ bugs silenciosos que iriam a produto).
2. **"Verbatim-para-git"** como padrão de ingestão (cru imutável + proveniência fileId/hash/data).
3. **"Separação por artefato"** como template de repo (engine determinístico × prosa; número nasce no engine; preço PARADO em vez de inventado).
4. **Gate mecânico de fechamento** parametrizável de portfólio — lição: "dois gates que discordam é pior que um".
5. **"Estado DERIVADO, nunca declarado"** como regra transversal (pega falso-verde em qualquer unidade).
6. **Checklist de abertura:** "contrato de schema do bruto" + "mapa de dependências de dados" (interno×externo×ausente) — previnem as 2 maiores fontes de retrabalho desta sessão (schema presumido; insumo externo descoberto tarde) e **validação legal/normativa como gate de ENTRADA**, não de saída.

## 4. Pedido ao MOU (decisões que dependem do escritório)
- **B-17:** consolidar o produto preso na branch ao `main` (branch protegida).
- **B-9 / Supabase:** autorizar/operar a carga pesada Drive→Supabase (destrava dono/Atc/preço/geo de uma vez).
- **SMUL:** confirmar a semântica das colunas da fila FUNDURB (teto 5% vs arrecadação; somatória rolante vs all-time).
