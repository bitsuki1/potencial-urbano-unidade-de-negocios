# Decisões do dono — 2026-07-18

> Lavradas pela instância a pedido do MOU (2026-07-18). Registro durável (D83). Idioma PT-BR (D164).

## D-DONO 2026-07-18 — Guarda do 90 revisada; exclusão física em curso
O dono revisou a guarda do **90** (decisão de 12/07): **exclusão física em curso** de **CRIADO (10.457)** + **ILEGÍVEL-png (12.373)**, por **lista congelada** derivada da vistoria de proveniência de 13/07, com **proteções intactas** (D-DONO-4 adquiridas · DE-PARA-06 · RESGATE-CANDIDATOS · FILA-INGESTAO · HOLD). A **99 — APAGAR** está sendo esvaziada pelo dono. O **razão sobrevive**: `PROVENIENCIA-DE-PARA.csv` (sha256 por arquivo) + `LISTA-EXCLUSAO-2026-07-18.csv` na pasta **00** do Drive. **Nada se perde do registro; perde-se só o arquivo físico.**

## Janela de concorrência (em vigor até o dono avisar o fim da exclusão)
- **NÃO disparar** Actions que **escrevem no Drive**: `sanear-drive` / `arrumar-drive` / `dedup` / `mover-para-apagar`.
- **Liberado:** git / corpus / ingestão que só LÊ do Drive.

## Etapa D — "PODE" do dono: ingerir o RESTANTE da fila de ingestão
Reconciliação de hoje contra o corpus atual: **31 de 54** normas da `FILA-INGESTAO-OFICIAL.csv` já ingeridas; **FALTAM 23**. Ingerir cada uma com **re-verificação verbatim + vigência + hash** (gates 1.6/1.7). Prioridade:
- **(a)** Dec. **63.698/2024** (Consolidação das Leis Tributárias);
- **(b)** municipais urbanísticas/TDC restantes: Leis 17.104/2019, 15.150/2010, 17.853/2022, 15.723/2013, 11.774, 14.094/2005 e Decretos 52.884/2011, 57.299, 57.378, 57.521, 57.770, 57.776, 58.707, 59.163, 59.263, 59.671, 60.581, 61.218, 62.175, 63.423;
- **(c)** federais ambientais (6.938, 11.428) por último.
Os melhores `drive_id` de cada uma estão na própria fila e foram **PROTEGIDOS** da exclusão.

## Re-extrair os 49 HOLD
Re-extrair `inventario/drive-pu/HOLD-ILEGIVEL-RECHECAR.csv` (49 itens).

## Pós-exclusão (GATED na confirmação do dono)
QUANDO O DONO CONFIRMAR O FIM DA EXCLUSÃO: recatalogar o Drive, rodar o **selo** e publicar o **índice-mestre pós-exclusão** na pasta 00 (relatório fonte × destino), atualizando o estado alvo: **7.465 oficiais + 2.348 adquiridas + canônicos, 90 residual, 99 vazia**.
