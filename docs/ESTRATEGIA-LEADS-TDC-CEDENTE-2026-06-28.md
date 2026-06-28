> # ⚠️ SUPERADO (2026-06-28, mesma sessão) — redireção do MOU.
> O MOU corrigiu o rumo: **agnóstico — sem opinião, sem valor, sem cruzar com lista receptora.** A lista
> oficial **é** a planilha ZEPEC; o trabalho é **enriquecê-la**, não derivar/pontuar/precificar.
> Logo, ficam REJEITADAS as partes deste doc: modelo de **valor** (§2), **rubrica/tiers** (§3), **casamento
> cedente↔receptor** (§3 C3/§5), e as **opiniões/recomendações** (§6 E-01..03, §7).
> **Vale como referência apenas** o mapeamento legal AGNÓSTICO de QUEM pode ceder (§1, arts. 122–133 — fato, citado).
> **Doc vigente:** `docs/ENRIQUECIMENTO-PLANILHAS-ZEPEC-2026-06-28.md`. (nada se descarta — este fica como rastro.)

# ESTRATÉGIA — Lista de Leads TDC, lado CEDENTE (venda de créditos)
> Estudo estratégico · orquestrador do Potencial Urbano (PU 14) · 2026-06-28.
> Direção do MOU (2026-06-28): mirar o **lado cedente** (quem GERA e VENDE potencial construtivo) e **elaborar estratégia** antes de codar.
> Doutrina: número nasce no engine (1.3) · citação obrigatória (1.7) · dialético (Tese/Antítese/Vacina) · nada se descarta.
> **Natureza deste doc:** ESTUDO/estratégia. Nenhum número de prospecção aqui é definitivo — são o *modelo* de valor e a *rubrica*; o valor por imóvel nasce do engine sobre dado real (1.3).

---

## 0. A tese em uma frase
O universo de leads cedentes **não é o ~1M de linhas do IPTU** — é um **conjunto finito e identificável por classificação de zoneamento** (imóveis em ZEPEC-BIR, ZEPEC-APC e ZEPAM-urbana, mais os candidatos a doação para fins públicos). Isso o torna uma lista **mais curta, mais quente e mais tratável** que o lado receptor, e — decisivo — **com modelo de valor computável a partir de dados que em boa parte já temos** (Quadro 14 + Quadro 3 `ca_basico`). O gargalo não é cálculo; é **georreferenciar a classificação ZEPEC/ZEPAM ao lote**.

---

## 1. A base legal — QUEM pode ceder (o universo de leads)
> Fonte: PDE — Lei Municipal SP nº 16.050/2014, arts. 122–133 (texto consolidado indexado no RAG). Regulamentação: Decretos 57.536/2016 e 58.289/2018. Atualizações pela Lei 17.975/2023.

A TDC nasce do **art. 35 do Estatuto da Cidade** (Lei Federal 10.257/2001) e é disciplinada pelo PDE (**16.050/2014, Art. 122**). O **Art. 123** autoriza a transferência para viabilizar seis finalidades: preservação de bem histórico/paisagístico/ambiental/social/cultural (I); corredores de ônibus (II); parques (III); preservação ambiental em ZEPAM urbana (IV); regularização fundiária de baixa renda (V); e provisão de HIS (VI).

Há **dois caminhos** de cedência — e eles definem dois perfis de lead muito diferentes:

### Caminho A — SEM doação (o proprietário FICA com o imóvel e vende o potencial) — **Art. 124**
O lead ideal: o dono não abre mão do bem, só monetiza o direito de construir que não vai usar. Categorias elegíveis:
- **ZEPEC-BIR** (Bens Imóveis Representativos — tombados) e **ZEPEC-APC** (Áreas de Proteção Cultural) → transferem o **potencial construtivo BÁSICO definido pela localização** (Art. 124, I).
- **ZEPAM na zona urbana** → transferem seu **potencial construtivo básico** (Art. 124, II; Redação da Lei 17.975/2023), **condicionado** a autorização do **Conselho Gestor do FUNDURB**, parecer favorável da **SVMA** e celebração de **TCA** averbado na matrícula (Art. 124, §1º).
- **Fórmula do potencial cedível (Art. 125):** `PCpt = Atc × CAbas × Fi`, com **Fi = 1**.
  - `Atc` = área do terreno cedente · `CAbas` = coef. de aproveitamento **básico** vigente na data de referência.
  - A Declaração registra o **valor unitário V (R$/m²) do terreno cedente pelo Cadastro de Valor de Terreno para Outorga Onerosa** (Art. 125, §1º, III) — **é o nosso Quadro 14**.

**Exclusões duras (Art. 124, §2º):** **NÃO** podem transferir potencial os imóveis em **bairros tombados em Área de Urbanização Especial (AUE)** nem em **Áreas de Proteção Paisagística (APPa)**. → filtro obrigatório da lista.

**Trava de volume (Art. 124, §3º):** PCpt acima de **50.000 m²** é transferido de forma **gradativa, em 10 parcelas anuais**. → afeta liquidez do lead grande.

**Estado de conservação (Art. 129):** a Certidão para **ZEPEC-BIR** exige **comprovação de bom estado de preservação/conservação** do imóvel cedente. → flag de elegibilidade prática.

### Caminho B — COM doação / desapropriação amigável (o proprietário DOA o terreno) — **Art. 126/127**
O dono troca o terreno por créditos. Finalidades (Art. 126): corredores de ônibus (I), HIS (II), regularização fundiária (III), parques (IV).
- **Fórmula (Art. 127):** `PCpt = Atc × CAmax × Fi` — note **CAmax** (não básico) e **Fi variável por finalidade** (Art. 127, §1º):
  - **2,0** corredores de ônibus · **1,9** HIS · **0,8** regularização fundiária · **1,4** parque com V≤R$2.000/m² · **1,0** parque com V>R$2.000/m².
- Aqui o Fi premia a doação (chega a 2,0) e usa CAmax → **potencial gerado é muito maior** que no Caminho A, mas o dono **perde o imóvel**. Perfil de lead distinto (quem tem terreno em perímetro de melhoramento/parque e prefere crédito a uma desapropriação litigiosa).

### A ponte cedente→receptor (por que o crédito vale) — **Art. 128**
O potencial cedido vira área no receptor pela razão de valor de terreno:
`PCr = (PCpt × VTcd) / (Cr × CAmaxcd)` — onde VTcd = V do cedente (Q14) e Cr = contrapartida de outorga no receptor.
**Implicação comercial:** o crédito cedente só tem valor se houver **receptor com demanda**. A lista cedente e a lista receptora (OODC, que o engine já faz) são **os dois lados do mesmo mercado** — a inteligência de verdade é **casar** as duas.

---

## 2. O modelo de valor do lead (o que faz um cedente ser "quente")
> Número de prospecção nasce do engine (1.3). Abaixo é o MODELO; o valor por imóvel sai do `oodc.py` estendido sobre dado real.

**Valor potencial do crédito de um cedente (Caminho A, estimativa):**
```
PCpt  = Atc × CAbas × 1                      (Art. 125)
Valor ≈ PCpt × V_cedente                     (V = Q14 R$/m² do terreno cedente)
```
Três alavancas tornam um lead quente — e cada uma é um **dado que ranqueia**:
1. **Área do terreno (Atc)** — quanto maior, maior o potencial. (vem do cadastro/IPTU)
2. **CAbas da localização** — ZEPEC em zona de eixo/centro com CAbas alto gera MUITO crédito; ZEPAM tem CAbas = 0,1 (baixíssimo por m², mas costuma vir com áreas enormes). (vem do Quadro 3 — **já temos**)
3. **V (R$/m²) do terreno** — Q14; zonas valorizadas multiplicam o valor do crédito. (**já temos**)

**Assimetria estratégica a explorar:** ZEPEC (patrimônio) tende a sentar em **zonas centrais valiosas** → CAbas e V altos → **crédito de alto valor unitário**, e o dono normalmente **quer** monetizar (o imóvel tombado "trava" o aproveitamento). É o **filão mais quente**: alta disposição a vender × alto valor × o dono mantém o bem.

---

## 3. Rubrica de qualificação e priorização (o "quente/morno/frio")
Proposta de scoring multi-critério (a calibrar com o MOU):

| Critério | Sinal | Fonte do dado | Peso sugerido |
|---|---|---|---|
| **Valor estimado do crédito** (PCpt × V) | maior = mais quente | Q14 ✓ + Q3 ✓ + Atc | alto |
| **Folga / não-uso do potencial** | imóvel tombado/subutilizado = vende o que não usa | IPTU (área construída) | alto |
| **Categoria** | ZEPEC-BIR/APC (dono fica) > doação (dono perde) | zoneamento/overlay | alto |
| **Tipo de proprietário** | PJ/holding/espólio = decisão mais rápida | socios.csv | médio |
| **Liquidez** | PCpt < 50.000 m² = transfere de uma vez (Art. 124 §3º) | engine | médio |
| **Elegibilidade prática** | ZEPEC-BIR exige bom estado (Art. 129); ZEPAM exige FUNDURB+SVMA+TCA (Art. 124 §1º) | inspeção/cadastro | filtro |

**Filtros eliminatórios (hard):**
- **Excluir** AUE e APPa (Art. 124, §2º) — não podem ceder.
- **Excluir** o que já emitiu Declaração/Certidão esgotando o potencial (Art. 132 — declarações pré-16.050 permanecem válidas; checar estoque já emitido para não prospectar quem já vendeu).

**Tiers de saída:** **A (quente)** = ZEPEC em zona de alto V, PCpt<50k, PJ; **B (morno)** = ZEPAM/doação com Fi alto; **C (frio/observação)** = pendente de elegibilidade (estado de conservação, AUE/APPa duvidoso).

---

## 4. Dados — o que TEMOS × o que FALTA
| Insumo | Para quê | Status |
|---|---|---|
| **Quadro 14 (V R$/m²)** | valor do crédito | ✅ `tabelas/q14-valor-terreno.csv` (6.715 SQ+Codlog) |
| **Quadro 3 (`ca_basico`/`ca_max`)** | PCpt (Art. 125/127) | ✅ `tabelas/quadro3-ca-por-zona.csv` (tem CAbas!) |
| **Fatores de incentivo Fi (doação)** | Caminho B (Art. 127 §1º) | ✅ extraível do próprio PDE (acima) — falta tabelar |
| **Perímetros ZEPEC-BIR / ZEPEC-APC / ZEPAM** | **definir o universo de leads** | ❌ shapefiles de zoneamento (LPUOS 16.402 + geo) — **Drive/geo** |
| **Área do terreno (Atc) por lote** | PCpt | ❌ cadastro/IPTU/LOTES — **Drive→Supabase** |
| **Proprietário (Atc → dono)** | contatar o lead | ❌ `socios.csv` — **Drive** (PII, D106/RLS) |
| **Estoque de Declarações/Certidões já emitidas** | não prospectar quem já vendeu | ❌ SMDU / fila FUNDURB (oráculo cita `fila_tdc_5porcento_fundurb`) |

**Leitura honesta (D26 "armado ≠ destravado"):** o **modelo de valor e a rubrica** estão prontos para virar engine; o **bloqueio real e único** para a lista REAL é **georreferenciar a classificação ZEPEC/ZEPAM ao lote** + a área do terreno. Diferente do lado receptor, isso **não exige o IPTU inteiro** — exige os **perímetros de zoneamento especial** (conjunto público, finito), o que é **mais barato de obter**.

---

## 5. Caminho de execução (faseado)
**Fase C0 — Engine cedente (LOCAL, desbloqueado — posso fazer já).**
Estender `engines/tdc/oodc.py` com `pcpt_cedente(atc, cabas, fi=1)` (Art. 125) e `pcpt_doacao(atc, camax, fi_por_finalidade)` (Art. 127), com citação por dispositivo e auto-teste — espelho do que já existe para OODC. Saída: um `gerar_leads_cedentes.py` análogo ao `gerar_alvos.py`, provado na amostra. **Zero dependência de Drive.**

**Fase C1 — Universo por zoneamento (precisa dos perímetros ZEPEC/ZEPAM).**
Cruzar lotes × overlays ZEPEC-BIR/APC/ZEPAM (ST_Within) → lista de candidatos. Aqui entra o **pedido ao Drive/geo** (consolidar em B-9).

**Fase C2 — Enriquecimento + ranqueamento (precisa de Atc + socios).**
Atc do cadastro, dono do socios.csv, aplicar a rubrica §3 → **lista de leads cedentes ranqueada por valor de crédito, em tiers A/B/C**.

**Fase C3 — Casamento de mercado.**
Cruzar a lista cedente (oferta) com a lista receptora/OODC (demanda, Art. 128) → **deals potenciais** (quem vende ↔ quem compra), o produto de maior valor.

---

## 6. Dialética (Tese / Antítese / Vacina) das apostas estratégicas
**E-01 — Começar pelo cedente ZEPEC, não pelo receptor.**
- *Tese:* lista finita, dono motivado (imóvel tombado trava aproveitamento), alto valor unitário, dados de cálculo já em mãos.
- *Antítese:* "o receptor é mercado maior e o engine OODC já roda."
- *Vacina:* sem receptor a demanda existe, mas o **cedente é o lado escasso e diferenciado** — quem organiza a oferta de créditos captura o spread. E o cedente é **mais tratável** (não precisa do IPTU inteiro). Os dois lados convergem na Fase C3; começar pelo escasso é vantagem competitiva.

**E-02 — Priorizar Caminho A (sem doação) sobre Caminho B (doação).**
- *Tese:* no Caminho A o dono **mantém o imóvel** e vende só o ar — proposta comercial fácil ("dinheiro sem perder o bem").
- *Antítese:* "o Caminho B gera muito mais potencial (CAmax × Fi até 2,0)."
- *Vacina:* B exige doar o terreno — ciclo de venda longo, decisão pesada, concorre com desapropriação. A serve a um "sim" rápido. Manter B como trilha B2B com a Prefeitura/incorporadoras, não como topo do funil.

**E-03 — O valor é estimativa até o engine + dado real.**
- *Tese:* publicar já uma lista ranqueada por PCpt×V estimado acelera a prospecção.
- *Antítese:* "estimativa pode gerar promessa comercial falsa (passivo)."
- *Vacina:* todo valor sai do engine com citação (1.3/1.7) e **selo de estimativa** até Atc/CAbas reais por imóvel; a Declaração oficial (SMDU) é a única fonte do número fechado. Vender "oportunidade qualificada", nunca "valor garantido".

---

## 7. Próximos passos (decisão do MOU)
1. **Autorizar a Fase C0** (engine cedente local) — é trabalho desbloqueado, alto valor, espelha o que já validamos. *(Recomendado começar por aqui.)*
2. **Abrir o pedido de dados geo** (perímetros ZEPEC-BIR/APC + ZEPAM) — consolidar em B-9 (lane do Drive), pois é o que destrava o universo real (Fase C1).
3. **Calibrar a rubrica §3** (pesos, tiers) — decisão de negócio.
4. **Confirmar o apetite por Caminho B/doação** (relação com Prefeitura) — define se a Fase C entra agora ou depois.

> Registrado no BACKLOG como item da frente comercial (cedente). Citações verificadas contra o texto verbatim indexado (16.050/2014, arts. 122–133); mérito jurídico fino fica sob B-10 (auditoria de tese).
