# Auditoria — rodada FAMÍLIA AUSÊNCIA/VALOR/USO (D82) — Potencial Urbano — 2026-06-20

> ⚠️ **BANNER DE SUPERAÇÃO (2026-06-20, pós-destraves):** o achado **CRÍTICA-1** abaixo ("NENHUMA das 27
> leis é verbatim; 27 a re-ingerir") **era um FALSO-NEGATIVO** e foi **DESMENTIDO por AUD-01**
> (`docs/AUDITORIA-PROFUNDA-2026-06-20.md`) + CODEX **D-07**: o verbatim das 12 federais já estava em
> `_entrada/misto/*.txt` e foi promovido. **ESTADO REAL HOJE: 13 leis verbatim/indexadas; faltam 14
> municipais (não 27).** Mantido o texto original abaixo como antítese histórica (nada se descarta).

> Registro datado exigido pelo método (`escritorio-do-mou/processos/AUDITORIA-TRIPLO-LIMPO.md §8`).
> **D82:** rodadas anteriores cobriram as famílias INTERNA (consistência/doutrina/segurança) e DADO VIVO
> (corpus/docs/Drive/banco) — ver `AUDITORIA-TRIPLO-LIMPO-2026-06-20.md` (R1→R3). Esta rodada aplica a família
> que faltava: **AUSÊNCIA/VALOR/USO** (Completude · Acionabilidade/Valor · Usabilidade-pelo-MOU · Rastreabilidade).
> **A família nova achou o que 3 rodadas da família interna declararam "limpo"** — prova viva do D82.

## Lentes (3, paralelas, read-only)
Completude/Cobertura · Acionabilidade/Valor (D26) · Usabilidade-pelo-MOU + Rastreabilidade (conversa × registro).

## Achados → AÇÃO (oficializado nesta rodada, HEAD do PU)
| # | Sev | Achado | Correção |
|---|---|---|---|
| **CRÍTICA-1** | CRÍTICA | "12 federais verbatim" (correção da rodada anterior) era **FALSO**: os 12 `.md` federais carregam "Texto INTEGRAL não baixado — HTTP 403"; têm ementa + dispositivo-chave + síntese, NÃO o articulado integral. **NENHUMA das 27 leis é verbatim integral.** | Reescrito em PROXIMA P2 + linha 9, `consolidar.py _nota_verbatim`, CONSOLIDACAO:36, catalogo-README, AUDITORIA #6: **27 leis a re-ingerir verbatim**; só as 32 juris (curtas) são verbatim. |
| **ALTA-2** | ALTA | A ordem das pendências põe HIGIENE (P1 excluir Drive) no topo; o que destrava PRODUTO (consulta com citação) no fundo. Régua D26 invertida. | Adicionado **★ DESTRAVE-MESTRE** no topo de PENDÊNCIAS: fatia vertical fina de TDC (1 lei → verbatim → fatiar → indexar → 1 consulta com citação). P1/P3/P6 rotulados HIGIENE-paralela. |

## Achados → DEFERIDO (declarado, com recomendação — não bloqueia, para a próxima janela)
- **MÉDIA (Acionabilidade-4) — valor preso:** `engines/tdc/oraculos/` + `FORMULAS-CONSOLIDADAS.md` são markdown DESCRITIVO, não engine executável (1.3); dependem de CSVs não-ingeridos (estão no Drive); não validados (ground-truth vazio). Linguagem inflada herdada ("PERFEIÇÃO ABSOLUTA" no `ORACULO_MESTRE_RELACIONAL_V4`) — marcar com agnosticismo. *Rec.: declarar "valor parado, não-wired" e ligar só na fatia vertical.*
- **MÉDIA (Usabilidade-A.2) — cross-repo sem rótulo "não-clicável aqui":** refs a `M-24/M-41/M-49/D78/D79/D80` aparecem nas superfícies do MOU sem o disclaimer (perfil 404-sensível, D78). *Rec.: rotular "(vive no repo do escritório — não-clicável aqui)".*
- **MÉDIA (Completude) — dirs vazios sem marcador inline:** a tabela do `DO_ESCRITORIO.md` lista `tabelas/ tese/ rag/ evals/ engines/iptu/` como ponteiros mas não marca "(vazio — estágio X)"; a honestidade depende de cruzar 3 docs. *Rec.: marcador "(vazio — a popular no fatiamento)".*
- **MÉDIA (Rastreabilidade-B.1) — vacinas só no handoff volátil:** V-1/2/3 vivem só em `PROXIMA-INSTANCIA.md` (substituível). *Rec.: gravar no `CODEX-DO-PROJETO.md §8` (memória durável) + bump de versão datado. Re-declaradas abaixo para não se perderem.*
- **BAIXA/MÉDIA (Rastreabilidade-B.2) — V-2 (Gemini) sem virar tarefa:** é "ideia adiada" sem dono/gatilho. *Rec.: virar item com gatilho (avaliar Gemini p/ enumerar o corpus do Drive quando for re-ingerir).*
- **BAIXA (Usabilidade-A.3) — jargão git ao MOU:** "a cada push" (5×) e branch/hash no `HANDOFF §2`. *Rec.: "a cada vez que algo é salvo/oficializado".*
- **MÉDIA (Completude) — leis-bônus ausentes:** `Lei 6.989/66` (núcleo do IPTU-SP) e `11.154/91` ausentes — declaradas abertas no HANDOFF, aguardam OK do MOU. Maior ausência substantiva de conteúdo.

## VACINAS DURÁVEIS desta rodada (re-declaradas — candidatas ao CODEX §8)
- **V-CONFIANÇA≠VERBATIM:** "confiança de extração" não prova verbatim. Conferir o `.md` (marcador "Texto INTEGRAL não baixado") antes de declarar uma lei citável. As 27 leis NÃO são verbatim integral.
- **V-DESTRAVE≠SANEAMENTO:** "MANIFESTO ligado / enum saneado / docs reconciliados" é destrave de REGISTRO/INFRA, não passo de esteira de PRODUTO. Não vender saneamento como progresso de pipeline (régua D26).
- **V-1/V-2/V-3** (do chat): extensão de captura para no 1º item (conferir lote completo) · Gemini p/ corpus do Drive (caminho adiado) · dup do Drive = upload entre máquinas (causa-raiz: ponto único de upload + dedup no upload).

## VEREDITO
**ARMADO, NÃO DESTRAVADO** (honesto): o PU está no passo 1 da esteira (saneamento+corpus), e o FIM (consulta com citação) está a 0% (`rag/` vazio). O registro agora é honesto sobre isso. **Convergência da família:** Completude = cobertura honesta (0 ponto cego grave); Usabilidade = 0 link morto, médias de rótulo/jargão; Acionabilidade = 1 CRÍTICA + 1 ALTA (corrigidas) + valor-preso declarado. A família nova **NÃO está em falsa convergência** — achou material real; as médias/baixas ficam declaradas para a próxima janela (D66/tabuleiro). Severidade decaindo, sem oscilação.

## BETA-CONTÍNUO
Re-rodar a MESMA família é cego ao que ela não vê: 3 rodadas de consistência declararam "12 federais verbatim" consistente — a lente de **Acionabilidade** (outro ângulo: "isso serve ao produto?") foi a que viu que o corpus é furado. **D82 vale: a convergência exige famílias diferentes, não passadas repetidas.**
