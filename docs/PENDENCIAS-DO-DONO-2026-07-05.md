# PENDÊNCIAS DO DONO — passo a passo (2026-07-05, PU 18)
> Só o que depende de VOCÊ (ações fora do meu alcance: UI de sites, credenciais, decisões).
> Tudo o que é código/corpus eu faço e provo por gate. Ordem = do que mais destrava para o que pode esperar.
> Cada item traz link, valores e cliques exatos. Ao terminar um, me avise que eu sigo/verifico.

---

## ✅ ATUALIZAÇÃO 2026-07-06 (verificado pelo assistente)
- **Secret `GOOGLE_SA_KEY`: SETADO e VÁLIDO** — o ensaio (dry-run) autenticou como
  `escritorio-do-mou@portfolio-do-mou.iam.gserviceaccount.com` e rodou limpo:
  **1.360 movidos / 0 erros / 0 multi-pai** (666 Geo · 468 Leis · 166 Tabelas · 54 Gov · 6 Inbox),
  batendo o de-para auditado. Log lido direto da API do GitHub (não relatório de extensão).
- **Branches antigas: APAGADAS** — sobrou só `main` + branch de trabalho + `jsgvth`.
- **FALTA:** o **OK do dono para o move REAL** (dry_run=false). Depois eu conto a `_entrada` (deve zerar).

---

## 🔴 1. AGORA — destrava a arrumação do Drive (5 min)
**Setar o secret `GOOGLE_SA_KEY`** (a chave JSON do robô que você baixou do Google Cloud).
Sem ele o workflow que move os 1.360 arquivos não roda.

1. Abra: `https://github.com/bitsuki1/potencial-urbano-unidade-de-negocios/settings/secrets/actions`
2. Botão **New repository secret**.
3. **Name:** `GOOGLE_SA_KEY`
4. **Secret:** cole o **conteúdo inteiro** do arquivo `.json` da conta de serviço
   (`escritorio-do-mou@portfolio-do-mou.iam.gserviceaccount.com`). É o arquivo que baixou —
   abra no bloco de notas, Ctrl+A, Ctrl+C, cole aqui. (NÃO é o ID de 40 caracteres.)
5. **Add secret**.
6. Me diga **"secret setado"**.

Depois disso é **comigo**: eu disparo o ensaio (dry_run) pela API, **leio o log** e **conto a
`_entrada`** para provar. Se limpar, te peço o OK e rodo o move de verdade, e re-conto (deve zerar).
**Nenhum relatório de extensão conta como prova — só a minha contagem.**

---

## 🟠 2. RÁPIDAS — higiene (5 min cada, quando puder)

### 2A. Fechar a porta da API do Supabase (P6)
O dado real vive em `governanca` (fechado); o certo é tirar `public` da API. É clique de painel (não dá por SQL).
1. Abra: `https://supabase.com/dashboard/project/csnalylpvysjvejgsymr/settings/api`
   (projeto **potencial-urbano-iptu-tdc**).
2. Seção **Exposed schemas** (ou "Data API" → schemas expostos).
3. **Remova `public`.** **Mantenha `graphql_public`.** **Não** adicione `governanca`.
4. **Save**.
5. NÃO mexa em PostGIS/extensões (mexer arrisca o geoprocessamento).
6. Me avise — eu confirmo com um GET anônimo que a porta fechou.

### 2B. Apagar as branches antigas (opcional — o conteúdo já está na `main`)
O resgate (`_garimpo-branches/`) já aterrissou na `main`, então estas são seguras de apagar.
1. Abra: `https://github.com/bitsuki1/potencial-urbano-unidade-de-negocios/branches`
2. No ícone de **lixeira**, apague **estas 4** (deixe `main` e a de trabalho atual):
   - `claude/backlog-audit-separation-w1vu4b`
   - `claude/escritorio-instance-organization-4zpyoh`
   - `claude/project-audit-roadmap-2thi1g`
   - `claude/pu-14-instances-ey91o2`
3. **NÃO apague** `main` nem `claude/project-analysis-pending-20wc81` (é onde estou trabalhando agora).
4. A `claude/potential-urban-instance-jsgvth` pode ser apagada também, mas se tiver qualquer dúvida
   me peça que eu confirmo item a item antes.

---

## 🟡 3. QUANDO PUDER — destravam recursos

### 3A. Chave de embeddings (destrava a busca semântica, B-5)
Hoje a busca é por palavra-chave (já melhorei com o grafo de remissões). Para busca por SIGNIFICADO,
preciso de UMA destas opções — você escolhe:
- **Opção fácil:** uma chave de API da **Voyage** (`voyage.ai`) ou **OpenAI**. Você gera e me passa
  (eu guardo como secret, não no git).
- **Opção sem chave:** eu uso um modelo local (roda no CI, mais lento). Basta você dizer "usa local".
> Me diga qual e, se for chave, me passe — ou salve como secret `VOYAGE_API_KEY` do jeito do item 1.

### 3B. Revisão humana de 1 lei-âncora (tira o `revisado_por_humano` de 0/61)
Rápido e vale muito para credibilidade. Sugiro o **Decreto 57.536/2016** (núcleo do TDC, que acabei de ingerir).
1. Abra: `https://github.com/bitsuki1/potencial-urbano-unidade-de-negocios/blob/main/leis/municipal-sp/decreto-saopaulo-57536-2016.md`
2. Compare por cima com a fonte oficial (o PDF que está no Drive) — confere se o texto bate.
3. Me diga **"conferi o 57.536, está fiel"** que eu marco `revisado_por_humano: true` no `.json`.

---

## 🔵 4. DEPENDE DE FONTE EXTERNA (egress .gov.br / MOU / dado pesado)
> Não são cliques rápidos — são pedidos ou cargas. Listo para não cair no esquecimento.

- **4A. 5 leis municipais que NÃO existem no Drive** (10.365/87, 11.338/92, 12.350/97, 13.475/02, 17.759/22)
  e o **corpo do Decreto 58.289/2018** (só os anexos estão no Drive): precisam ser capturadas de fonte
  oficial (o egress .gov.br está bloqueado nesta sessão). Caminho: pedir ao MOU / rodar de um ambiente
  com internet liberada. As **outras 7 municipais + o 6.989/66 ESTÃO no Drive** — essas eu ingiro sozinho
  (a 6.989 é scan de 12,5 MB, precisa de OCR antes).
- **4B. Semântica do FUNDURB** (o teto em R$ é por operação ou somatório?): confirmar na fonte da SMUL —
  destrava a precificação por FUNDURB.
- **4C. Dado pesado → Supabase** (sócios/ITBI/IPTU completo): é a carga que resolve "dono em escala"
  (hoje só 19 dos 599 prontos têm dono). Usa o mesmo robô/Colab; é passo de infra do MOU.

---

## ✅ Já resolvido nesta sessão (não precisa fazer nada)
- Preço = **preço legal** (margem é do usuário) — decidido, lavrado.
- Projeto **não julga produto/mercado** — decidido.
- Itens fora de escopo (ISS/previdenciário) — **arquivados**.
- Bem coletivo "Light" (1.772 postes) — **cravado no motor** como não-comercializável.
- **Decreto 57.536/2016 (núcleo TDC) — ingerido, indexado, com evals verdes** (fecha a maior lacuna).
- Grafo de remissões, hash de proveniência, saldo por conjunto, parcelamento — feitos e provados.
