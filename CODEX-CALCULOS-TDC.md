# CODEX DE CÁLCULOS TDC (engines / fórmulas)
> Onde moram as **fórmulas e engines** do TDC — o "como se calcula o potencial em m²". Separado do Comercial (2026-06-28, decisão do MOU).
> Doutrina 1.1/1.3: fórmula é **engine determinístico**, separada da lei e da tese; **número nasce aqui, nunca no LLM**, com citação (1.7).
> Irmãos: `CODEX-COMERCIAL-TDC.md` (quem/onde/negociar) · `CODEX-PRECIFICACAO-TDC.md` (R$, PARADO).

## 1 — Os engines
| Engine | Arquivo | O que calcula | Citação |
|---|---|---|---|
| **PCpt cedente** | `engines/tdc/pcpt.py` | potencial passível de transferência (m²), **2 vias** | Art. 125 / 126-127 |
| **OODC receptor** | `engines/tdc/oodc.py` | outorga onerosa (o lado oposto) | LPUOS / PDE |

## 2 — As duas fórmulas do cedente (engine `pcpt.py`, auto-teste verde)
- **SEM doação (Art. 125):** `PCpt = Atc × CAbas × Fi`. ~~Fi = 1 (fixo)~~ **★ CORRIGIDO 2026-07-02 (loop de melhoria, lente jurídica; VERIFICADO no verbatim):** para NOVAS declarações ZEPEC o **Fi é ESCALONADO pela área do lote — LPUOS Lei 16.402/2016, Art. 24, I–VII**: ≤500m²→**1,2** · ≤2.000→**1,0** · ≤5.000→**0,9** · ≤10.000→**0,7** · ≤20.000→**0,5** · ≤50.000→**0,2** · >50.000→**0,1**. O engine `pcpt.py` resolve o Fi e cita o inciso; `fi` explícito sobrepõe (declaração antiga). Impacto da correção: agregado do produto caiu de R$17,5bi p/ R$8,8bi; lotes ≤500m² (maioria) subiram 20%. Dono **fica** com o imóvel (caso ZEPEC).
- **COM doação (Art. 126/127):** `PCpt = Atc × CAmax × Fi(finalidade)`. Dono **doa** o imóvel. CAmax + Fi até 2,0.
- **Fi de doação (Art. 127 §1º):** corredor 2,0 · HIS 1,9 · regularização 0,8 · parque 1,4 (V≤R$2.000) / 1,0 (V>R$2.000). Tabela: `tabelas/fi-incentivo-doacao.csv`. O fator do parque é resolvido **dentro do engine** a partir de V (1.3).
- **Limite (Art. 124 §3º):** PCpt > **50.000 m² → 10 parcelas anuais** (estoque não à vista). Engine emite `estoque_a_vista`/`excedente_parcelado`.
- **Entradas datadas:** CAbas/CAmax valem na **data de referência** (protocolo Art. 125 §2º / doação Art. 127 §3º). Engine recebe como entrada; não assume "hoje".

## 3 — Fórmula OODC (lado receptor — referência)
`OO = (Área_Adicional / CA_max) × Fp × Fs × V` (3 fontes-mestre convergem; ver `engines/FORMULAS-CONSOLIDADAS.md`). Fs/Fp dos Quadros 5/6; CA_max do Quadro 3; V do Quadro 14.

## 4 — Insumos do cálculo (tabelas e chaves)
- **CAbas / CAmax** por zona → `tabelas/quadro3-ca-por-zona.csv` (tem `ca_basico` e `ca_max`).
- **Fi doação** → `tabelas/fi-incentivo-doacao.csv` (Art. 127 §1º).
- **Atc** (área do terreno) → IPTU/cadastro (externo, pendente).
- **3 chaves de JOIN** (do `ORACULO_MESTRE_RELACIONAL_V4`): Lote↔Valor (SQ→Q14); Zoneamento↔Q3 (→CA); Qualif. Ambiental↔Q3A (→QA).
- **Protocolo SQL_MESTRE** 10 díg (`lo_setor`+`lo_quadra`=SQ + lote). Datum SIRGAS 2000.

## 5 — Resoluções de cálculo (realocadas do Comercial)
| # | Decisão |
|---|---|
| R10 | **Número nasce no engine**, nunca no chute (Art. 125: `PCpt = Atc × CAbas × Fi`). O LLM roteia; o engine calcula e cita |
| R14 | **m² já transferido = gabarito de validação.** `PCpt = Atc × CAbas` tem de **bater** com as áreas realmente transferidas (167 certidões). Método que não reproduz o real não passa |
| R18-fórmula | **Duas vias** (sem/ com doação) — fórmulas acima. _(A leitura COMERCIAL das duas vias como alavanca de negócio fica no Codex Comercial.)_ |

> Catálogo antigo (oráculos `engines/tdc/oraculos/`): Fórmula Mestra, constantes Fs/Fp, arquitetura medallion Bronze/Silver/Gold, índice de ~170 GeoJSON. Fonte preservada lá; títulos catalogados em `zepec/AUDITORIA-AGENTES-2026-06-28.md`/garimpo.
