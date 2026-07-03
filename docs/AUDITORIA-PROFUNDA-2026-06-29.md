# Auditoria profunda — frente comercial TDC (PU 14, encerramento 2026-06-29)
> 3 auditorias adversariais (profunda · decisões · beta/processo) + correções. **Honestidade total** (pedido do MOU): o que está provado, o que é frágil, o que NÃO foi provado, o que pode enganar.
> Doutrina: D83 ("declarei feito ≠ provei feito"), zero-compressão, nada se descarta.

## 1. O QUE FIZEMOS (sessão PU 14)
- Puxei **4 planilhas ZEPEC verbatim** do Drive → base unificada (`zepec/limpo/zepec_unificada.csv`, **7.351 linhas**) → **ferramenta** (`zepec/ferramenta/zepec_cedentes.csv`, **6.131 imóveis**) com estado de venda, certeza, negociável, dono, m², FUNDURB.
- **Lista de prospecção** (`lista_prospeccao.csv`, 2.740) + fila de verificar (3.350) + guia.
- **3 codexes** separados (Comercial/Cálculos/Precificação).
- **Engine cedente** `engines/tdc/pcpt.py` (2 vias, Art.125/127 + Fi-área Art.24 LPUOS).
- Fontes externas verbatim (ANUAL/SISSEL/OODC → donos; FUNDURB fila; Quadro 7 parques; tabelas Fi).
- **Método triplo-limpo por agentes** em todas as etapas.

## 2. O QUE DECIDIMOS
R1-R18 nos codexes (realocadas: comerciais no Comercial; R10/R14 em Cálculos; R16/R17 em Precificação). **Novas (esta auditoria):** R19 (correção multi-lote como decisão de método) · R20 (Fi-área Art.24 corrige Fi=1).

## 3. AUDITORIA PROFUNDA — classificação honesta por componente
| Componente | Classe | Verdade nua |
|---|---|---|
| `montar_base.py` (unificação) | **SÓLIDO** | determinístico, agnóstico, reprodutível — a parte mais confiável |
| `montar_ferramenta.py` (estado/negociável) | **FRÁGIL** | lógica defensável, mas todos os rótulos dependem de premissas não-verificadas |
| `pcpt.py` (engine) | **NÃO-PROVADO** | **nunca rodou sobre imóvel real** (sem Atc); só auto-teste sintético |
| `donos.py` | **RISCO** | "4.965 donos" mascara que **só 79 são cedentes** (1,8%) — não vender titularidade |
| `fundurb.py` / `liquidez.py` | **FRÁGIL / honesto** | semântica das colunas incerta; sensor = INDETERMINADO (auto-rebaixado, virtude) |
| `extrair_quadro7.py` | **FRÁGIL** | PDF mastigado; 24 parques "sem situação"; campos brutos |
| 3 codexes | **RISCO (números defasados)** | contagens citadas divergiam do CSV (corrigido nesta auditoria) |

## 4. O QUE ESTÁ VENDIDO COMO CERTO MAS NÃO É (o que o sucessor PRECISA saber)
1. **Nenhum PCpt foi calculado para um imóvel real** — falta `Atc` (externo, IPTU). O engine é uma calculadora validada, não um produto aplicado.
2. **R14 (validar engine contra os 167 m² transferidos) NUNCA RODOU** — é intenção, não fato. Construir o teste antes de confiar no engine.
3. **Dono cobre 79 de ~4.292 cedentes (1,8%)** — o número grande (4.965) é de proprietários do lado receptor/comum, não dos tombados.
4. **`negociavel=sim` (2.750) ≠ prospectável** — inclui 3.659 SO_ELEGIVEL (ainda nem declararam). Prontos de fato (sim + INTACTO/TEM_SALDO) = **592**, e **87% sem dono**.
5. **FUNDURB cobre 7 de 6.131**; `valor_pecuniario_rs` é **regulatório, não preço de mercado**; sensor de liquidez = **INDETERMINADO** (semântica a confirmar na SMUL).
6. **VEDADO/INTACTO são INFERÊNCIAS** (sem confirmação geo/registral) — risco de falso positivo e negativo.
7. **Não há eval/teste de regressão** automatizado para a ferramenta comercial.

## 5. AUDITORIA DE DECISÕES
- **CONFIRMADAS:** citações Art. 124-129 + Art. 24 §5º conferem com o verbatim; cadeia R11→R15→R18 (doação) coerente; engine implementa fielmente as fórmulas.
- **CONTRADIÇÃO REAL CORRIGIDA — duplo Fi:** o engine usava Fi=1 (Art.125) ignorando que a **LPUOS 16.402 Art.24 modula o Fi por faixa de área** nas declarações ZEPEC pós-2016. **Corrigido** (R20, `fi_zepec_por_area` + tabela). Impacta R10/R14 (revalidar o gabarito com o Fi certo).
- **NÚMEROS DEFASADOS CORRIGIDOS:** ESGOTADO 6→**9**, sim 2.757→**2.750**, nao 38→**41**, TEM_SALDO 98→**95**, prontos 599→**592**, unificada 7.175→**7.351**, Quadro 7 257→**272**/147 propostos. Codex regenerado.
- **"~8× mais potencial"** é o exemplo didático (Atc=1000/CAbas=1/CAmax=4), não propriedade da via — marcado como exemplo.
- **Lacuna de registro:** a correção multi-lote (alto impacto) não tinha resolução → vira **R19**.

## 6. BETA CONTÍNUO (processo)
**Funcionou:** loop triplo-limpo com lentes DIFERENTES (maior ROI — pegou multi-lote, dono OODC, liquidez invertida); verbatim-para-git; separação por artefato; prova-vs-inferência; gate mecânico; estado derivado (não declarado).
**Falhou:** bugs silenciosos por **schema do bruto presumido** (não validado antes de codar); validação legal feita por ÚLTIMO (quase produziu semântica errada); dependência externa (Atc) descoberta tarde; parser xlsx ad-hoc frágil.
**Melhorias (ver `docs/MELHORIAS-PROCESSO-2026-06-29.md` + depósito ao escritório).**

## 7. O QUE VAMOS FAZER
Ver `docs/ROADMAP-PROJETO.md`. Curto prazo comercial: rodar R14 (validar engine), regenerar números do dado (não à mão), Supabase (dono/Atc), confirmar semântica FUNDURB na SMUL.
