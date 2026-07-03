# Migrations NÃO-APLICADAS (schema receptor — fora de escopo)

Estes 3 arquivos (`20260624_010/020/030`) **nunca foram aplicados** no banco de produção
(`csnalylpvysjvejgsymr`) — verificado ao vivo em 2026-07-03: os schemas/tabelas que eles
criam (`dados.*`, `geo.lote`, `tabelas.q14_valor_terreno`, `tabelas.quadro3_ca_zona`,
`tabelas.v_feed_alvos`) **não existem** no banco.

Além de nunca aplicados, são **schema do lado RECEPTOR** (`v_feed_alvos`/`gerar_alvos`/OODC),
**fora do escopo atual** (dono, 2026-07-03: só lado vendedor / só-tombado).

Foram MOVIDOS para cá (não apagados — reversível via `git log`/`git mv`) para que
`supabase db reset` reproduza EXATAMENTE o schema vivo (as 5 migrations canônicas em
`supabase/migrations/`), fechando a crise de canonicidade (escrutínio S1/M2-E6).

Se o lado receptor voltar ao escopo, revisar e re-datar antes de reaplicar.
