# Auditoria por agentes (escrutínio dos métodos) — 2026-06-28
> 3 subagentes adversariais auditaram lógica, matching e base legal. Achados, severidade e o que foi corrigido. Pedido do MOU.

## Agente 1 — lógica de classificação (correção)
| # | Sev | Achado | Ação |
|---|---|---|---|
| 1 | ALTA | **Multi-lote: chave SQL divergia** entre base (explode) e ferramenta (só 1º lote) → `esgotado`/`m²`/OUC no SQL errado | ✅ **CORRIGIDO** — ferramenta agora explode lotes; flags p/ todos os irmãos, m² só no 1º (área é do conjunto, não duplica). Esgotado 6→9 |
| 2 | ALTA | `esgotado` lido da col 14 por coincidência | ✅ documentado (col 14 = "N. Declaração Saldo"); regra mantida, índice explícito |
| 3 | ALTA | Contagem 565≠407 (explosão infla "nº declarações") | ✅ **CORRIGIDO** — `montar_base` rotula grão: declaracoes-FONTE 407 → imoveis 565; certidoes 168 → 196 |
| 4 | MÉD | `certeza='alta'` em conflito vedado×prova | 🔶 a rebaixar p/ média |
| 5 | MÉD | negociável `sim` em vedado-que-vendeu sem sinal | 🔶 a marcar verificar+sinal |
| 6-12| BAIXA | m² órfão sem SQL; denominador de cobertura; `_num` BR/US latente; OUC regex frágil; data ambígua em `data_ref` | 🔶 registrados |

## Agente 2 — chave SQL e matching de donos
| # | Sev | Achado | Ação |
|---|---|---|---|
| 1 | ALTA | `donos.sm()[:10]` desloca a chave se zero à esquerda some | ✅ **CORRIGIDO** — `keys_single` exige 10–11 díg, parse estrutural |
| 2 | ALTA | **`sm_parts` ignorava multi-lote do OODC (`/`)** — 322/502 linhas perdiam dono silenciosamente | ✅ **CORRIGIDO** — explode lotes; donos 2.993→**4.965 chaves** |
| 3 | MÉD | `split_lotes` não separava por `/` | ✅ **CORRIGIDO** (base e donos) com proteção do DV `0021/4` |
| 5 | MÉD | 48 SQL inválidos: só 1 recuperável (`012/41/0039` → quadra `041`) | 🔶 candidato único anotado; 39 sem-lote ficam inválidos (correto) |
| — | — | SISSEL off-by-one (col 22/32)? | ✅ **VALIDADO OK** (col22=SQL_Incra, col32=Proprietário) |
| 6-7 | BAIXA | `norm_endereco` número/multi; conflito de dono silencioso | 🔶 `conflitos` agora logado (1.287) |

## Agente 3 — base legal (validação) e novas soluções
**Validações (citadas na Lei 16.050/2014):**
- (a) *transferiu = vendeu* → **PARCIAL**: na **doação** (Art. 126/127) transferir **não é venda** (dono doa o imóvel à PMSP e recebe potencial). Exceção maior que o "uso próprio".
- (b) *AUE/APPa vedadas* (Art. 124 §2º) → **VERDADEIRO**, mas a vedação é por **origem/overlay**, não pelo selo do cadastro → nossa marca é inferência (confirma B3: confirmar por geo).
- (c) *valor = PCpt × V* → **PARCIAL**: é **proxy do lado cedente**. O crédito recebido pelo receptor é **Art. 128**: `PCr = (PCpt × VTcd)/(Cr × CAmaxcd)`, **CAmaxcd=4 fixo**, com **correção IPCA**. V vale na **data de protocolo** (Art. 125 §2º), não hoje.
- (d) estados → **PARCIAL**: **ESGOTADO pode reativar** (renovação ZEPAM Art. 123 §5º: 70%@10a, 100%@15a; e Art. 129 §2º) → estado é **temporal**. **SO_ELEGIVEL não é incondicional** (ZEPAM exige FUNDURB+SVMA+TCA).

**Nuances em risco:** ZEPAM cede mas com gates pesados · **>50.000 m² sai em 10 parcelas anuais** (Art. 124 §3º — estoque não disponível à vista) · renovação congela V antigo (barato) · **via de DOAÇÃO (Art. 126/127) com Fi até 2,0 e CAmax** = alavanca inteira fora do modelo · conservação (Art. 129) é **gate de readiness** da certidão.

**Novas soluções propostas:** processo SEI do TDC = dono mais limpo (priorizar) · **FUNDURB = R$/m² regulatório** (Art.24 §5º LPUOS, ≠ preço de mercado) (o comparável de PREÇO que faltava) · validar engine segregando doação (Art.127) de sem-doação (Art.125) · OUC e áreas contaminadas como gates · Art.128+IPCA como 2ª checagem de preço.

## Pendências priorizadas (próxima rodada)
1. ✅ FEITO (etapa 2): achados 3/4/5 do Agente 1 — grão rotulado + certeza/negociável em conflito vedado.
2. ✅ FEITO (etapa 3): via de doação modelada — `engines/tdc/pcpt.py` (2 vias, Fi do Art.127, >50k parcelado), triplo limpo.
3. Engine de preço com **Art. 128 + V por data** (não só PCpt×V).
4. **FUNDURB** como fonte de preço real + intercorrências (já puxado).
