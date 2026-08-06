# Auditoria de decisões — 2026-08-06 (pedido do MOU: "me parece que perdemos muita coisa aqui")

> Sessão PU 20c (branch `claude/urban-potential-instance-l3zed9`). Método: cruzamento das 6 fontes de
> registro — **ATA-VIVA-SESSAO.md** × **REGISTRO-DE-INSTANCIAS.md** × arquivos **DECISOES-\*** ×
> **BACKLOG.md** (headers "Atualizado") × banners do **PROXIMA-INSTANCIA.md** × `git log` (branch e
> `main`, PRs #37-#50) — procurando decisão/mandato do dono que exista numa fonte e falte nas demais.

## Veredito em uma linha
**A SUBSTÂNCIA não se perdeu; o REGISTRO sim.** Todo trabalho e toda decisão localizados têm rastro em
pelo menos uma fonte (banner, BACKLOG, arquivo de decisões, commit ou PR mesclado) — não achei
determinação do dono sem execução nem execução sem rastro. O que falhou foi a **disciplina de
lavratura**: ATA e REGISTRO pararam de ser alimentados por ~3 semanas e decisões recentes ficaram só
em chat/banner. Achados e reparos abaixo.

## Achados

**A1 — ATA VIVA com hiato de 2026-07-13 → 2026-08-05 (gravidade alta).** A ATA salta da PU 19
(07-12) direto para a PU 20c (08-06). Ficaram de fora: PU 19 autônomas 07-13/14/16 (vistoria 33.138 ·
TDC ENTREGUE · 5 teses · corpus 38→68 leis · receptor · cura 11.308), PU 20 07-17 (frente comercial
PJ→PF), PU 21 07-18 (série IPTU + Q14×GeoSampa), PU 22 07-19 (Etapa D 22/23 + Anexo I Q14 primário),
sessão 07-23 (decisões + merges #46/hub#28), PU 20a/20b 07-30→08-05 (migração C1 motor-a-motor,
front v1, Assertiva, C1 LIVE) e PU 20 autônoma 08-05. **Reparo:** entrada-índice do hiato lavrada na
ATA apontando o lar canônico de cada sessão (conteúdo existe; a ATA agora indexa).

**A2 — REGISTRO-DE-INSTANCIAS parado em 2026-07-12 (gravidade alta).** Última linha = PU 19 ABERTA.
Nenhuma sessão posterior estampou linha (o hook de boot não dispara em sessão remota — A-291/D132 —
e a rede manual falhou). **Reparo:** linhas retro compactas adicionadas (07-13→08-06), marcadas
"FECHADA (retro, auditoria 2026-08-06)" com handoff apontado.

**A3 — Decisões de 08-05 e 08-06 sem lavratura em arquivo DECISOES (gravidade alta).** O último
arquivo era o de 2026-07-23. As decisões de 08-05 ("quero 1" · mapa · federais · modo autônomo ·
"Apps Script já rodou") e as de 08-06 (mandato do validador · pedido do estudo ③a · **Opção B** ·
**27 órfãos = NULL/pendência** · pedido de mapa+auditoria) estavam só em banner/chat. **Reparo:**
`docs/DECISOES-DO-DONO-2026-08-06.md` lavrado (verbatim onde havia; reconstruído-marcado onde não).

**A4 — Espelho `supabase/migrations/` defasado (gravidade média; já detectado pela PU 20c).** As 9
migrações de 07-30→08-05 (motor0..4, views, hardening C1) foram aplicadas via MCP sem espelho no git
(SSOT = git, D38). A migração do card (08-06) foi espelhada; a de hoje
(`motor4_cedentes_precos_oficiais_nomeados`) **foi espelhada nesta auditoria**. **Resíduo:** as 9
anteriores seguem sem espelho — item de higiene na fila.

**A5 — Colisão de numeração de sessão (gravidade baixa).** "PU 20" foi usado em 2026-07-17 (frente
comercial, BACKLOG) e de novo em 2026-08-05/06 (banners PU 20/20b/20c). Não há perda de conteúdo, mas
a série PU N deixou de ser unívoca. **Reparo:** anotado no REGISTRO; próxima sessão nova segue de
**PU 23** em diante.

**A6 — Fila interna (tasks) × mapa dessincronizados (gravidade baixa).** A task #16 constava
`pending` com a etapa da view já em execução nesta sessão; #9/#18 concluídas já estavam corretas.
**Reparo:** #16 marcada em andamento; mapa do `PROXIMA-INSTANCIA.md` agora carrega, por item, se está
em andamento NESTA sessão e o nº na fila.

**A7 — Conferência decisão→execução (amostra dirigida, sem furo).** D-DONO-07-23 itens 1-9: todos
executados ou em espera-de-dado declarada (PRs mesclados; corte v1 respeitado; receptor aberto-mas-
depois; jurisprudência metade-runner na fila #7; Drive liberado→arrumação provada 08-06; estadual
59.263 capturado fora do corpus; 455 sem IPTU = espera de dado; faixas do adicional fail-closed;
`data_certidao_iso` plumbing pronto). D-DONO-07-18 (exclusão 90/99, janela, Etapa D, 49 HOLD):
executados (Etapa D 22/23; HOLD triado). Decisão 08-06 Opção B: aplicada e validada hoje.

## Estado dos reparos
| Reparo | Onde | Estado |
|---|---|---|
| Lavratura 08-05/08-06 | `docs/DECISOES-DO-DONO-2026-08-06.md` | ✅ nesta sessão |
| ATA — entrada 08-06 + índice do hiato | `ATA-VIVA-SESSAO.md` | ✅ nesta sessão |
| REGISTRO — linhas retro 07-13→08-06 | `REGISTRO-DE-INSTANCIAS.md` | ✅ nesta sessão |
| Espelho da migração de hoje | `supabase/migrations/20260806181000_*.sql` | ✅ nesta sessão |
| Mapa com fila + "nesta sessão" | `PROXIMA-INSTANCIA.md` (topo) | ✅ nesta sessão |
| Espelhar as 9 migrações 07-30→08-05 | `supabase/migrations/` | ⏳ fila (higiene) |
| Numeração: retomar em PU 23 | REGISTRO (nota) | ✅ anotado |
