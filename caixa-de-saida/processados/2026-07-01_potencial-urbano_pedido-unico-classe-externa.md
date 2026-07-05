> **⚠️ RECONCILIAÇÃO PU 17 (2026-07-03) — LER ANTES DE AGIR SOBRE ESTE PEDIDO.** O escritório (carta `ack-e-orfas`) + verificação no boot atualizam 2 itens do §2:
> - **Item 5(a) — merge do Produto B / B-17: RESOLVIDO.** O produto JÁ está no `main` (verificado: `engines/tdc/`, ZEPEC, oráculos presentes; DE-47 registra consolidação em 2026-06-28). **RETIRADO do pedido** — não levar ao MOU. A branch de origem `project-audit-roadmap-2thi1g` está coberta pelo main.
> - **Item 5(b) — despausar o preço: NÃO é pedido ao MOU; é decisão do DONO em aberto.** A direção MOU de 2026-06-28 foi **agnóstico, SEM preço**; "despausar" contraria essa direção e depende do **Atc do IPTU** (B-20b, ainda parado). Fica como **fork do dono** (régua de preço — `ROADMAP-PU.md §2`), não como item externo pendente.
> - Itens **1, 2, 3, 4** do §2 seguem VÁLIDOS (dado pesado Drive→Supabase, verbatim das 13 municipais, perímetros geo, semântica FUNDURB). A carta VPS-BRASIL (2026-07-03) pode ser o VEÍCULO dos itens 1 e 2 (IP-BR + job de carga) — ver `caixa-de-saida/para-escritorio/2026-07-03_potencial-urbano_resposta-VPS-brasil.md`.

# Potencial Urbano → Escritório do MOU — PEDIDO ÚNICO (Classe Externa) + relatório PU 15

> **De:** orquestrador do Potencial Urbano (PU 15, lente loop de IA) · **Data:** 2026-07-01
> **Branch:** `claude/potencial-urbano-strategy-kp9bgr` · **Doutrina:** diretriz é proposta fundamentada, não ordem (D44).
> **Contexto:** a estratégia de entregas (`ESTRATEGIA-DE-ENTREGAS-PU.md`) separou o que o loop de IA destrava
> sozinho (Classe LOCAL — **entregue nesta sessão**) do que exige um passo do MOU/infra (Classe EXTERNA — **este pedido**).

## 1. O que a PU 15 ENTREGOU sozinha (Classe Local — já no git, provado pelo gate)
- **B-12 FECHADO** (engine): guarda DECIMAL(10,3) do UTXO (m² PC estoura ⇒ LEVANTA; R$ OODC monetário não). Auto-teste verde.
- **B-11c FECHADO** (chunker/RAG): vigência POR CHUNK — o RAG **deixou de devolver redação revogada como vigente**
  (defeito real: PDE 16.050 Art. 148, revogado pela Lei 17.975/2023, vinha no topo). Eval ATIVO novo, verde.
- **B-7 (parte local) FEITO:** `verbatim_integral` derivado do `.md` no MANIFESTO; 7.228/1968 datada por Art. 11.
  Todas as 19 leis verbatim/indexadas agora têm `vigencia.inicio`.
- **B-10 FEITO** (mérito jurídico): 32 juris auditadas tema-a-tema (lente Gen Advogado + verificação adversarial).
  Laudo `docs/AUDITORIA-MERITO-JURIDICO-B10-2026-07-01.md`.
- **Gate `fechar-instancia.py` = VERDE** em todas as ondas.

## 2. O PEDIDO ÚNICO ao MOU (Classe Externa — o loop de IA NÃO resolve sozinho)
Ordenado por quanto destrava. Cada item já tem o trilho local pronto esperando o dado/decisão.

| # | Pedido | O que destrava | Trilho local pronto |
|---|---|---|---|
| **1** 🥇 | **Subir os pesados Drive→Supabase** (`IPTU_2026.csv` 937 MB, `socios.csv`, série ITBI) | **dono em escala + Atc** → eixo "dados ricos" + liga o engine de preço | `PLANO-H3-PRODUTO.md` + `scripts/transferir-pesados-drive-supabase.md` + migrations `supabase/migrations/` |
| **2** | **Cru verbatim das 13 municipais `bruto`** + Q14/Quadro 3 na fonte (B-4/B-9) | fecha o corpus jurídico + data as 13 (B-7 resíduo) | `scripts/promover_entrada.py` (padrão provado); guarda de verbatim no `fatiar.py` |
| **3** | **Perímetros geo** (ZEPAM/ZEIS/corredores) | vias de expansão 2/3/4/6 (`zepec/VIAS-EXPANSAO.md`) | engine `pcpt.py` (2 vias) + Fi por via já prontos |
| **4** | **Confirmar semântica FUNDURB na fonte SMUL** (teto 5% vs arrecadação; janela rolante vs all-time) | sensor de liquidez sai de `INDETERMINADO` | `zepec/liquidez.py` (reporta INDETERMINADO honesto hoje) |
| **5** | **2 decisões de negócio:** (a) merge do **Produto B** (E5 alvos, B-17) ao `main` protegido; (b) **despausar o preço** (Codex Precificação) | Produto B ao SSOT + engine de preço (Art. 128) | branch `project-audit-roadmap-2thi1g` (B-17); `CODEX-PRECIFICACAO-TDC.md` (parkado) |

## 3. Itens novos de backlog que a auditoria B-10 gerou (registrados, não perdidos)
- **B-21** 🟦 — **corpus é TDC-cego:** 0/32 jurisprudências tratam de TDC (VERIFICADO), apesar de TDC ser a base
  prioritária do MOU (2026-06-20). Construir jurisprudência de TDC (outorga onerosa / solo criado / potencial
  construtivo) — captura depende de egress/Drive.
- **B-22** 🟨 — dessincronização de notas de confiança `.md` ↔ `.json` em algumas juris (local; próxima janela).

## 4. Cerca respeitada
Nada tocado no Drive nem em `drive-arrumacao/`; trabalho só na branch; arquivos NOVOS. Este depósito é proposta
fundamentada (D44), sob o gate do projeto (D21) — não comando ao MOU.
