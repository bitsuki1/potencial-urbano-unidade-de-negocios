# BETA CONTÍNUO — Método, Stack e Registro (escritório + projeto)

> **O que é.** Ativo vivo que destila a experiência deste projeto num **método
> reutilizável** pelo Escritório (MOU) e por qualquer projeto. Subordinado ao
> `CODEX-DO-PROJETO.md` (SSOT, RO-17). "Beta contínuo": evolui a cada lição —
> toda regra nova nasce na conversa (RO-11) e é **registrada no Codex** (SSOT,
> RO-17), refletindo-se aqui.

---

## 1. Princípios (resumo — canônicos no Codex §1/§8)
Inteligência fora do LLM (RO-01) · número nasce no engine (RO-04) · 4 artefatos
separados — Lei·Tabela·Fórmula·Tese (RO-03) · só fonte oficial vira lei (RO-08) ·
**nada se descarta** (RO-09) · **operador não lê doc; tudo na tela** (RO-11) ·
trazer tudo → identificar → deduplicar com cuidado, **versão ≠ duplicata**
(RO-12/14) · citação obrigatória (RO-15) · **SSOT única** (RO-17) · redundância é
inimiga (RO-19) · proveniência honesta (RO-20) · **não cravar ausência sem
varredura** (RO-21) · **toda escolha vem como sugestão pronta** (RO-22) · **banco
limpo até a organização completa** (RO-23) · **triplo-limpo após qualquer
alteração** (RO-24).

## 2. O método de trabalho (fases)
1. **Trazer tudo** (completude primeiro; Fase 0). Varredura por pasta; ilegíveis
   trazidos ao operador (RO-13). Produz o **De/Para localizador**.
2. **Identificar e taguear** entrando NO documento (conteúdo, não título; §2).
3. **Separar nos 4 artefatos** (RO-03) → schemas no banco (§4).
4. **Escrutinar** documento a documento (Tese/Antítese/Vacina) → Codex Mestre.
5. **Identificar imóveis** (Fase 2) e **validar por casos reais** (Fase 3).

## 3. Protocolos operacionais reutilizáveis
- **Escrutínio cruzado / saturação.** Auditar cada local (conversa · docs/repo ·
  Drive · banco) em rodadas até **N rodadas limpas seguidas**; depois repetir
  TUDO até N limpas em todos. Achou ouro → captura/corrige (zera o contador).
- **Auditoria por sub-agentes.** Disparar agentes paralelos read-only que
  retornam só conclusões (integridade, catalogação, consistência). Padrão usado
  aqui (agentes `afbaa6f5…` integridade, `a1046b44…` catalogação).
- **Sempre-sugestão (RO-22) + na-tela (RO-11).** Decisão do operador = recomendação
  na frente + trade-offs; ele só veta/confirma. Nunca mandar pra arquivo.
- **De/Para = livro-razão (RO-14).** Uma linha por arquivo: destino + vigência +
  linhagem (substitui/substituído) + proveniência + oficialidade + confiança.
- **Movimentação física (opcional).** Apps Script que MOVE sem duplicar,
  idempotente, com ensaio (dry-run), relatório e auto-retomada por orçamento de
  tempo. **Gotcha cravado:** nome de pasta com "/" colide com separador de path —
  ancorar destinos a IDs reais (`CONFIG.FOLDER_IDS`). Ver `drive-arrumacao/`.
- **Esteira RAG DETERMINÍSTICA (reutilizável; 2026-06-20).** `fatiar` (chunk por
  dispositivo, 2.5; guarda de verbatim) → `indexar` (BM25 + metadados, 2.6) →
  `consultar` (citação obrigatória 1.7; gate de cobertura) → `evals/` (gate =
  citação correta). Stdlib, sem LLM/embeddings (D-05). **Vacina:** match lexical ≠
  relevância semântica — gate de keyword não distingue "direito de construir" (TDC)
  de "construir habitações" (Lei 4.591 Art. 68). Embeddings/filtro-por-tema = extensão.
- **Promotor de verbatim (`promover_entrada.py`).** Quando o cru já está em
  `_entrada/`, a re-ingestão é INTERNA (sem Drive/egress): recorta o cru → `.md`
  verbatim + `.json confianca:alta` → `fatiar`. **Vacina (D-07):** `.md` dizer "não
  baixado/403" ≠ o verbatim não existir; conferir `_entrada/` antes de cravar ausência (RO-21).
- **Engine como CÓDIGO, não prosa (`engines/tdc/oodc.py`).** Fórmula em `.md` =
  número no LLM (proibido RO-04). Transcrever para função pura determinística
  (DECIMAL exato, constante de fonte única, citação no resultado). Insumo de tabela
  ausente = entrada obrigatória, nunca inventada (D-08).
- **Mecanismo anti-perda — o "ladrão" (D83 do escritório, importado 2026-06-20).**
  `BACKLOG.md` (item com **DoD = prova mecânica**) + hook de boot que o surfaça +
  GATE de fechamento (`fechar-instancia.py`: evals+engine+sem-stray-tag+MANIFESTO
  idempotente+backlog fresco). Move regra de "o maestro lembra" para "o sistema
  garante" (D-09). Reutilizável por qualquer projeto.
- **Auditoria profunda por LENTES adversariais (reutilizável).** N sub-agentes
  read-only, cada um numa lente DIFERENTE (corpus · código · dado/produto · doutrina),
  + ground-truth vivo (Supabase/MCP); convergência dialética num laudo. Lentes
  diferentes evitam falsa convergência (re-rodar a mesma lente = teatro). Casa com o
  método `AUDITORIA-TRIPLO-LIMPO` do escritório.

## 4. STACK A USAR
| Camada | Ferramenta | Papel |
|---|---|---|
| **Banco relacional + espacial + RAG** | **Supabase / Postgres 17** | a casa do dado e do engine (a "verdade") |
| Espacial | PostGIS (+ pgrouting, address_standardizer) | lotes, zoneamento, ZEPEC, geocoding |
| RAG | pgvector + pg_trgm + unaccent | embeddings e busca de lei/jurisprudência |
| Fonte de documentos | Google Drive (MCP) | acervo bruto (RO-21: varrer, não presumir) |
| Arrumação física | Google Apps Script | conforto de navegação (opcional) |
| LLM (casca) | Claude (agnóstico, RO-02) | roteia e redige; nunca calcula |
| SSOT versionada | Git / GitHub | Codex + artefatos; consolidação serial (sem conflito) |

**Projeto Supabase (IPTU/TDC):** `potencial-urbano-iptu-tdc` ·
ref `csnalylpvysjvejgsymr` · região `sa-east-1` ·
URL `https://csnalylpvysjvejgsymr.supabase.co`.
**Separado do Keepee** (`gestao-integrada-dados`) — separação de escopo.
**Estado: esqueleto LIMPO, SEM DADO (RO-23)** — hoje existem só os schemas
`governanca` (`de_para` + `registro_decisoes`, vazios) e `public`/PostGIS. **VACINA
(2026-06-20, auditoria triplo-limpo):** os schemas dos 4 artefatos + `geo` + `rag`
da tabela abaixo (§5) são DESTINO FUTURO — ainda NÃO foram criados (verificado via
MCP); a coluna "Espelho no banco" é plano, não fato. A carga (De/Para, leis, geo,
tabelas) só acontece **depois da organização completa e aprovada**. Lá dentro tudo
nasce limpo.
🔑 Chaves (anon/publishable/service) ficam no **painel Supabase / variáveis de
ambiente — NUNCA commitadas no git.**

## 5. O QUE REGISTRAR (e onde)
| Registrar | Onde (canônico) | Espelho no banco |
|---|---|---|
| Regras de ouro e decisões | `CODEX-DO-PROJETO.md` (§1,§5,§7,§8) | `governanca.registro_decisoes` |
| De/Para de cada arquivo (RO-14) | `inventario/` + `drive-arrumacao/de-para-final.csv` | `governanca.de_para` |
| Leis/normas (RAG) | — | schema `leis` |
| Tabelas/valores | — | schema `tabelas` |
| Fórmulas/engine | `engines/FORMULAS-CONSOLIDADAS.md` | schema `engine` |
| Teses (Antítese/Vacina) | — | schema `tese` |
| Camadas geo | `inventario/camadas-geo.md` | schema `geo` (PostGIS) |
| Proveniência·oficialidade·confiança | em TODO registro | colunas dedicadas |

**Padrões canônicos no banco:** `SQL_MESTRE` (10 dígitos; `governanca.is_sql_mestre`)
e `ENDERECO_MESTRE` (Correios/DNE) — Codex §3.

> **RO-23:** a coluna "espelho no banco" é o destino FUTURO. Hoje as tabelas estão
> **vazias** — a carga só ocorre após a organização completa e aprovada do acervo.

## 6. Como o beta evolui
Lição nova → decidida na conversa (RO-11) → registrada no **Codex** (SSOT) →
refletida aqui e, quando couber, em `governanca.registro_decisoes`. O escrutínio
cruzado (§3) roda periodicamente até saturar. Nada se perde (RO-09).
