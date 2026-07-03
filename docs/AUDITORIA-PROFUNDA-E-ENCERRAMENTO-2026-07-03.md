# AUDITORIA PROFUNDA + ENCERRAMENTO HONESTO — 2026-07-03

> **Zero síntese.** Este documento não resume: declara, item a item, o que está PROVADO feito, o que
> foi apenas DOCUMENTADO (plano, não código), e o que continua VIVO no código — cada afirmação com a
> evidência em `arquivo:linha`. É o fecho honesto da sessão. Método: verificação direta nos arquivos e
> no banco vivo (`csnalylpvysjvejgsymr`), não confiança nos docs de estratégia.

---

## 1. A VERDADE CENTRAL (verificada, não afirmada)

**Esta sessão entregou o PLANO e a FUNDAÇÃO. Não entregou UMA correção de produto.**

Prova: `git log --since="2026-07-03" --name-only` nos caminhos de produto (`engines/`, `zepec/*.py`,
`scripts/fatiar`, `scripts/consultar`) retorna **VAZIO**. Nenhum arquivo de engine, pipeline ou chunker
foi tocado. O que mudou nesta sessão: `.claude/settings.json` (allowlist), `supabase/migrations/*`
(canonicidade/proveniência/decisões — schema e metadado, não produto), e `docs/*` + `MOTOR-*.md` +
`ROADMAP-PU.md` (estratégia).

**Consequência honesta:** a ferramenta que um corretor abre hoje (`zepec/ferramenta/zepec_cedentes_oficial.csv`,
os ~2.937 preços, o agregado R$ 8,83 bi) é **byte-idêntica à de antes da sessão** e carrega **todos** os
defeitos que os loops diagnosticaram. Os `MOTOR-*-ESTRATEGIA.md` são o MAPA; o território (código) não mudou.

---

## 2. DEFEITOS DE PRODUTO — status REAL no código (todos VIVOS, verificados)

| id | Defeito | Evidência ao vivo (2026-07-03) | Status código |
|---|---|---|---|
| **T1/C-28** | Fórmula PCpt citada como "Art. 124" (é Art. 125) — viola 1.7 na consulta mais importante | `rag/chunks/lei-municipal-saopaulo-16050-2014/133__art-124.json` carrega Atc/Fi rotulado `…› Art. 124`; idem `136__art-126.json` (com-doação, deveria Art. 127) | **VIVO** |
| **T3** | Escalonado aplicado por default ao cohort já-declarado (deveria ser Fi da certidão; restrição está no CAPUT do Art. 24, novas declarações) | `zepec/enriquecer_oficial.py:81` → `pcpt_sem_doacao(atc, cabas)` sem `fi` | **VIVO** |
| **T4** | Conservação não modelada como gate (Termo≠Atestado; filtro de cohort; Art.129 §2 idade→montante) | sem coluna `elegibilidade_conservacao`; `montar_base.py:173` põe `ato_conservacao=bp_compres` p/ tombado | **VIVO** |
| **T8** | Vedação Art.124§2 só por substring, sem geometria; fail-closed só-preço (pcpt/saldo seguem fabricados nas vedadas) | `montar_base.py:104 def cessao_vedada(cat)` (substring em categoria); linha 169 consome; sem `.shp` no fluxo | **VIVO** |
| **T5** | Divergência de 27% vs 55 certidões não surfaçada; sem disclaimer | sem coluna `qualidade_estimativa`; sem `DISCLAIMER.md` | **VIVO** |
| **T9** | Parcelamento >50.000 m² não separado no preço | preço usa saldo cheio | **VIVO** |
| **T11** | Saldo por lote, não por CONJUNTO cedente | `montar_ferramenta.py:46` atribui o m² do conjunto a `sms[0]` só | **VIVO** |
| **T6** | Cemitério de oráculos não arquivado | `engines/tdc/oraculos/` presente | **VIVO** |
| **G1** | Overlay por centroide/1ª feature, não por área | `zepec/pipeline/overlay_zona.py:77` usa `.centroid` para os lotes | **VIVO** |
| **G2** | Zona-base sob selo (os 454) não resolvida; ZOE usa Quadro 2A (não Q3) | overlay não devolve N:N; sem Quadro 2A ingerido | **VIVO** (bloqueado: Quadro 2A) |
| **G3** | 1.839 "sem SQL" tratados como geocode (96% é bem coletivo "Light") | `endereco_mestre` vazio em 1.772; alvo do fuzzy é recorte, não IPTU completo | **VIVO** |
| **G4** | V por 1 face (Regra da Esquina exige MAX/RANGE); citação não lida | `enriquecer_oficial.py:57` casa por `sql[:6]`+codlog único | **VIVO** (bloqueado: Decreto 57.536) |
| **G6** | Camada espacial sem eval | `rodar-evals.py` só schema RAG; sem `geo-overlay.json` | **VIVO** |
| **S2/T2** | Gate de CI não cobre o produto | `consolidar.yml` `on.push.paths` sem `zepec/**`,`engines/**`,`supabase/**` | **VIVO** |

> **Correções de sessões ANTERIORES que continuam válidas** (não regrediram): Fi escalonado tabelado em
> `pcpt.py` (LPUOS Art. 24 I-VII), saldo líquido (abate m² transferido), esgotado/vedado des-precificado,
> vigência-por-chunk. **Nota T3:** o Fi escalonado existe e está certo COMO TABELA; o defeito VIVO é
> aplicá-lo por DEFAULT ao já-declarado em vez do Fi da certidão.

---

## 3. O QUE ESTÁ DE FATO FEITO E PROVADO (Fundação + inteligência)

**Fase 0 — Fundação (provada ao vivo, ver `docs/AUDITORIA-BETA-2026-07-03.md`):**
- Canonicidade: 7 migrations git == banco (versão a versão); fantasmas receptor arquivados; `dados.*`/`geo.lote` ausentes. **PROVADO.**
- Proveniência: `governanca.de_para` = 20 fontes (14 OFICIAL, 3 NOSSO marcadas). **PROVADO.**
- Segurança T7: buckets privados; `oficiais.*` RLS deny-all; spend cap ON; 3 S3 keys revogadas. **PROVADO** (resíduo: service_role legada não rotacionada).
- Decisões no banco: D-CANON-01/02, D-SEG-01, D-ESCOPO-01, D-DRIVE-01, D-MOTOR-01, D-AUDIT-01, D-FORK-00. **PROVADO.**

**Inteligência produzida (docs, não código):**
- `ROADMAP-PU.md` (6 marcos, 3 forks), `MOTOR-1/2/3-ESTRATEGIA.md` (12+7+6 itens, nenhum triplo limpo),
  `docs/ESCRUTINIO-CONJUNTO-MOTORES.md` (48 achados, 5 doenças, crítica adversarial),
  `docs/INVENTARIO-DRIVE.md`, `docs/HANDOFF-2026-07-03-MOTORES-FASE0.md`. **ESCRITOS.**

---

## 4. CONFIANÇA E LACUNAS (o que NÃO sei / não provei)

- **`db reset` clean-room:** não executado; canonicidade provada por match-de-versão + DDL verbatim + seeds idempotentes, não por reconstrução real. Selar na Fase 1.
- **Gate cego ao produto:** o "verde" do gate cobre corpus/engine/manifesto, **não** o pipeline nem o banco. Uma regressão no produto passa verde hoje (é o T2). **Logo, a auditoria beta "verde" NÃO é atestado do produto — só da fundação.**
- **Números do produto:** os ~2.937 preços e o R$ 8,83 bi são o output do engine ATUAL, que aplica escalonado por default (T3 vivo) e não desconta corretamente vedação por geometria (T8 vivo). **Não trate esses números como corretos/vendáveis.**
- **G2/G4 bloqueados externamente:** dependem de 2 verbatim que o dono ainda não trouxe (Decreto 57.536/16, Quadro 2A). Sem eles, FLAG/RANGE — nunca fabricar.
- **Loops sem triplo limpo:** os 3 motores pararam no teto/sem-ALTA; o resíduo é dívida declarada, não "resolvido".

---

## 5. ENCERRAMENTO — o que a próxima instância NÃO pode assumir como feito

1. **NÃO** assuma que os motores estão corrigidos. Estão **planejados**. Fase 1 (código) não começou.
2. **NÃO** confie nos números do produto atual (T3/T8 vivos). O primeiro fix que muda número deve vir com eval de regressão.
3. **NÃO** re-rode os loops de estratégia — eles já convergiram no que dava; o resíduo está em `MOTOR-*.md` + handoff §8. Recomeçar é desperdício.
4. **NÃO** aposente o substring da vedação ao codar T8 (crítica adversarial); âncora é `montar_base.py`, não `enriquecer_oficial.py`.
5. **NÃO** trate o gate verde como prova do produto até o T2 fechar.

**Ordem de ataque (Fase 1), inalterada:** **T1 (C-28)** → **T2 (gate de CI que fecha o ponto cego)** → **T8 (vedação c/ geometria AUE/APPa do Drive)** → **T4 (conservação)** → **G1 (overlay por área)**; G2/G4 quando os 2 verbatim chegarem. Detalhe com gotchas: `docs/HANDOFF-2026-07-03-MOTORES-FASE0.md` §8.

**Estado do dono:** 2 verbatim pendentes; forks abertos (D-FORK-00). **Estado do código:** intocado, todos os defeitos vivos. **Estado da fundação:** sólida e provada.

Fim do encerramento. Sessão entregou mapa + alicerce; a obra (Fase 1) está inteira à frente, com o passo-a-passo e os riscos na mão.
