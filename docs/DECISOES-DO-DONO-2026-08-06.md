# Decisões do dono — 2026-08-05 e 2026-08-06 (MOU)

> Lavradas em 2026-08-06 pela sessão PU 20c (branch `claude/urban-potential-instance-l3zed9`), como
> reparo da auditoria de decisões (`docs/AUDITORIA-DECISOES-2026-08-06.md`): as decisões abaixo tinham
> ficado só em banner/chat, sem lavratura em arquivo de decisões. Registro é doutrina (D83; "nada se
> joga fora"). Onde não há aspas, o teor foi reconstruído do banner/handoff da própria sessão que o
> recebeu — marcado como (reconstruído).

## D-DONO 2026-08-05 (sessão PU 20, antes do reset da janela)
1. **"quero 1"** — mandato de caracterizar os 474 cedentes sem `ca_basico` (a "opção 1" oferecida).
   Cumprido: 474 = 100% sem linha em `c_zona_por_cedente` (buraco de geometria/zona, não de coluna).
2. **"atualize o mapa de pendências, siga executando na sequência, trabalhe as normas federais"**
   (reconstruído do banner PU 20). Cumprido: federais 6.938/1981 + 11.428/2006 confirmadas JÁ indexadas
   (mapa estava defasado); gate RAG 33/33.
3. **"a janela vai travar (reset em ~7h14), organize-se para voltar em modo autônomo"** (reconstruído).
   Cumprido: retomada autônoma agendada e executada em 2026-08-06 05:18 UTC.
4. **Aviso do dono: o Apps Script da arrumação do Drive JÁ RODOU** → determinação de CONFERIR o
   resultado antes de redisparar (task #9). Cumprido em 2026-08-06 (confrontação SA independente:
   981/1360 movidos, gate 7/7 VERDE).

## D-DONO 2026-08-06 (sessão PU 20c)
1. **Mandato da manhã:** consertar os dois defeitos do validador (link "modo degradado" + card "Leis
   no corpus"). Cumprido com prova (rota `/publico` 200; card 39→132 via `public.v_corpus_resumo`).
2. **Pedido do estudo (item ③a da auditoria PU 20):** "estude sob várias lentes e me traga o resultado
   com sugestões" — sobre qual valor/m² o produto expõe (venal IPTU × VTcd Q14). Cumprido:
   `docs/ESTUDO-PRECO-VENAL-x-VTCD-2026-08-06.md` (5 lentes, opções A/B/C, recomendação B).
3. **★ DECISÃO DO PREÇO NA CAMADA DE PRODUTO — OPÇÃO B** (teor registrado nesta sessão): a view
   `motor4.cedentes` expõe **só dados oficiais, nomeados sem ambiguidade** —
   `valor_m2_venal_iptu2026` (venal IPTU/PGV, contexto) e `vtcd_q14_2026_m2` (VTcd Quadro 14, insumo
   legal) — e o **preço legal continua nascendo exclusivamente no engine** (`art128.py`, Art. 128
   caput/§1º/§2º), nunca num campo genérico `valor_m2`. Junto: **(b)** join cedentes↔Q14 com `codlog`
   normalizado dos dois lados; **(c)** expor `ca_basico` na view.
   **APLICADA na hora:** migração `20260806181000_motor4_cedentes_precos_oficiais_nomeados`
   (espelhada no git). Validação: 3.905=3.905 (zero fan-out), 27 órfãos NULL, 474 `ca_basico` NULL.
4. **★ Os 27 órfãos do Q14 (sem face na Portaria) = NULL/PENDÊNCIA** — nunca zero, nunca venal como
   substituto. O produto mostra "sem VTcd publicado" até existir fonte oficial (ou palavra do dono
   sobre outra via). Blindagem 1.3/1.7: número não nasce de aproximação.
5. **Pedido de governança (fim da tarde):** "atualize o mapa de pendências e nos que estão em
   andamento, coloque a informação se está em andamento nessa sessão e qual o número dela na sua
   fila, atualize com as nossas últimas conversas e aproveite e rode uma auditoria de decisões, pois
   me parece que perdemos muita coisa aqui." Cumprido: mapa com fila no topo do
   `PROXIMA-INSTANCIA.md` + `docs/AUDITORIA-DECISOES-2026-08-06.md` (achados + reparos).

## Derivações imediatas
- Preço no front: até a saída do engine ser materializada no banco (fila #22), a carteira NÃO exibe
  "preço" — exibe os dois campos oficiais nomeados. Campo genérico `valor_m2` deixou de existir.
- Fila #22 passa a ser o próximo passo de produto: executar `art128.py` sobre os cedentes e gravar a
  saída (com memorial/citação) numa tabela própria consumida pelo validador.
