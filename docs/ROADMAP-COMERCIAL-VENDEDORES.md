# ROADMAP — Frente comercial (Vendedores/Compradores) · decisões + plano até a entrega

> Registro vivo da estratégia acordada com o MOU (2026-07-16). "Registre tudo" — este é o SSOT do plano comercial.
> Entregável final: a **lista de vendedores** (e de compradores) da TDC em São Paulo, com dono, metragem, valor, datas e agenda.
> Base com nomes vive **neste repo** (privado, confirmado `private:true`, só o MOU acessa — risco aceito pelo dono, D106/postura amoral).

## Decisões travadas (log)
| # | Tema | Decisão do MOU |
|---|---|---|
| 1 | Carga | **Carga inicial + refresh a cada 2 meses** (a base envelhece; mantê-la viva). |
| 2 | Foco | **Agnóstico, sem carro-chefe.** Servir todos os segmentos; segmentação só adequa a abordagem. |
| 3 | Cidade | **Tudo de uma vez** — SEM separar centro/resto. (revoga o faseamento Etapa 1/2 anterior). |
| 4 | Gabarito do motor | Conferir contra **TODOS os oficiais — TDC inteiro** (não só ZEPEC-BIR). |
| 5 | Potencial | Usar o **potencial OFICIAL** (da carga SMUL) para os já-declarados; estimar só os virgens. |
| 6 | Agenda recarga (Art.129) | **Caminho B**: datas agora (janelas 70%/10a e 100%/15a, **alerta 1 ano antes**), como **coluna na lista**; Atestado de Conservação (DPH) por-imóvel **depois** (não há lista aberta — confirmado). |
| 7 | Limpeza público×privado | **Profunda**, via **contribuinte cadastral** (não cruzamento pobre de nomes); ela já entrega o proprietário de brinde. |
| 8 | Dono agrupado | Coluna "carteira" — juntar o mesmo dono em vários lotes (achar o **peixe grande**). |
| 9 | Frescor | Usar **ITBI pós-2020** como sinal de que o nome do IPTU-2020 está velho. |
| 10 | Contato | Após obter **nome + CPF**, buscar telefone/e-mail em **ferramentas externas** (BigDataCorp, Assertiva, Serpro…). |
| 11 | ITBI | Puxar a **série completa 2019→2026** do portal da Fazenda SP (aberto; SQL+valor+data, **sem nome**). |
| 12 | Cartório/matrícula | MOU **não achou** acesso fácil — **fase futura**, em aberto (confirma dono + ônus por lead quente). |
| 13 | Espólio/usufruto | **Fora por agora.** |
| 14 | Score de priorização | **Sem score** — o MOU decide vendo a lista. |
| 15 | Motor — reforços | Banda de confiança · dupla-fonte que precisa concordar · vintage em tudo · gate que trava se divergir do oficial. |
| 16 | Repo da base | **Este repo** (Potencial Urbano), privado. |

## Regra de ouro sobre os insumos (1.8)
As planilhas **enriquecidas** que já existem no Drive (ex.: `BENSTOMBADOS_ENRIQUECIDO`, `BASE_TDC_TOMBADOS_FINAL`, `PLANILHA_ENRIQUECIDA_*`) são **SÓ-IDEIA** — nunca fonte. Mas **se elas foram construídas, os insumos primários existiam** — e é esses insumos que recapturamos. Auditoria do Drive em curso para mapeá-los (4 lentes).

## Insumos primários conhecidos (as 43 bases de `inventario/drive-pu/DE-PARA-06-COMERCIAL.csv`)
- **Societário:** `empresas.csv` (razão social↔CNPJ), `socios.csv` (CNPJ→CPF/nome do sócio), `holdings.csv` (holding→holding).
- **IPTU com nome:** `iptu-2020-cep01` (SQL→nome, **sem CPF**, só CEP 01/centro). *Cobertura de outras regiões: em auditoria.*
- **ITBI:** guias 2023/2024/2026 (SQL+valor+data, sem nome). *Série completa 2019-2026: a puxar da Fazenda.*
- **Oficial SMUL:** `lista_declaracoes` + `lista_certidao` ZEPEC-BIR ago/2025 (potencial oficial + transferências).
- **Processos:** `extrato_ad` (Aprova Digital).

## Roadmap (cidade inteira, de uma vez)

**FASE 0 — Auditoria do Drive (EM CURSO).** 4 lentes varrendo o inventário atrás de todo insumo primário útil (dono/CPF, ITBI, contato, IPTU de outras regiões, engenharia reversa das enriquecidas). Entrega: a lista definitiva de insumos que temos vs que faltam.

**FASE 1 — Carga oficial (SMUL, TDC inteiro).** Potencial oficial + estados + datas de cada imóvel. Fundação de tudo.

**FASE 2 — Motor confiável.** Potencial oficial p/ já-declarados; calibrar virgens contra TODOS os oficiais; banda de confiança; dupla-fonte; vintage total; gate. Conserta o saldo (o "vendeu mais que o pcpt").

**FASE 3 — Dono + limpeza (cidade inteira).** SQL→nome (IPTU cadastral) → limpeza público×privado → cadeia societária p/ PJ → dono agrupado. Insumos da FASE 0.

**FASE 4 — ITBI (preço + frescor).** Série 2019-2026 da Fazenda → preço real por SQL + flag de frescor do dono.

**FASE 5 — Contato.** Nome+CPF → BigDataCorp/Assertiva/Serpro → telefone/e-mail.

**FASE 6 — Lista + Agenda.** Montar o entregável (layout abaixo) com a coluna de agenda de recarga.

**FASE 7 — Refresh a cada 2 meses.** Re-puxar SMUL+ITBI, re-rodar motor, atualizar lista/agenda.

**Fases futuras (em aberto):** cartório/matrícula · Atestado de Conservação (DPH) · espólio/usufruto · processos SEI/e-SAJ · lado comprador/receptor.

## Layout do entregável (1ª versão — o MOU afina)
Identificação (SQL·endereço·distrito·zona·tombamento) · Imóvel (área terreno) · Potencial (potencial·saldo·estado) · Fase (1 obter / 2 vender) · Preço (piso Art.128 · preço real ITBI+data) · Agenda (data declaração · recarga 70%/100% · alerta 1 ano) · Dono (nome·PF/PJ·sócios·**dono agrupado**) · **Frescor** (ITBI pós-2020?) · Contato (tel/email) · Processo (SEI) · Rastro (fonte de cada campo·1.8).

---

## EXECUÇÃO iniciada (2026-07-16, modo autônomo) — pipeline comercial construído

MOU: "vamos colocar no roadmap e começar o trabalho completo, modo autônomo até o final."

**Pipeline determinístico (pasta `comercial/`, testado contra fixtures sintéticos — sem PII real):**
1. `itbi_para_sql.py` — guias de ITBI (xlsx) → `itbi_por_sql.csv` (transação mais recente: valor+data por SQL). ✅ autoteste.
2. `iptu2020_para_contribuinte.py` — cadastro IPTU 2020/2016 (com NOME) → `iptu_contribuinte.csv` (contrato do resolver) + `iptu_flags.csv` (PF/PJ/PÚBLICO — limpeza público×privado **pelo contribuinte**, não por nome de logradouro). ✅ autoteste.
3. `resolver_dono.py` (já existia) — cadeia CNPJ→sócios→PF controladora (só PJ, opcional/pesado). ✅ autoteste.
4. `enriquecer_lista.py` — junta base 4.292 + nome (PF direto) + controlador (PJ) + preço/frescor ITBI + **dono agrupado (peixe grande)** + agenda → `LISTA-VENDEDORES-ENRIQUECIDA.csv`. **contato SEMPRE marcado p/ ferramenta externa** (CPF completo + tel/email — nunca inventado). ✅ autoteste.
5. `baixar_drive_sa.py` — primitivo de download do Drive (conta de serviço).

**Action `comercial-lista.yml`** (workflow_dispatch): baixa IPTU (drive_id/URL) + guias ITBI → roda o pipeline → commita a lista enriquecida **neste repo privado** (nomes no git, decisão do MOU). PJ→sócio é opcional (`com_pj`, pesado — v2).

**Estagiamento:** v1 = IPTU centro (cep01, confirmado) + ITBI recente + PF direto → primeira lista real. v2 = IPTU citywide (mirror 2020/2016 com nome) + cadeia PJ. Contato (CPF+tel/email) = ferramenta externa (BigDataCorp/Assertiva/Serpro), fora do git — precisa da conta do MOU.
