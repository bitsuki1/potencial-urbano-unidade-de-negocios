# PROMPTS PARA EXTENSÃO (navegador) — Branches + Supabase P6
> Pedidos pelo dono em 2026-07-05 ("me dê um prompt para uma extensão fazê-lo").
> Cada bloco é autocontido: cole no agente de navegador/extensão e execute.
> A sessão remota do PU NÃO consegue executar nenhum dos dois (delete de branch bloqueado
> pelo classificador de permissão; exposed-schemas é ação de Dashboard, sem API no MCP).

---

## PROMPT 1 — Deletar as 3 branches remotas redundantes (B-23, ordem obrigatória)

```
Você vai limpar branches remotas do repositório GitHub
`bitsuki1/potencial-urbano-unidade-de-negocios`. Trabalhe na UI do GitHub (ou gh CLI se
disponível). ORDEM OBRIGATÓRIA — há um pré-requisito de consolidação antes de 2 das 3:

PASSO 1 (deletável JÁ): delete a branch `claude/project-audit-roadmap-2thi1g`.
  Justificativa: 0 arquivos únicos vs main (verificado em 2026-07-03; dono autorizou).

PASSO 2 (pré-requisito): verifique se a branch `claude/potential-urban-instance-jsgvth`
  já foi consolidada ao `main` (procure um merge/PR dela no main, ou compare: a branch
  não pode ter commits à frente do main). SE AINDA NÃO FOI CONSOLIDADA: abra um PR de
  `claude/potential-urban-instance-jsgvth` -> `main`, faça o merge, e SÓ ENTÃO siga ao passo 3.
  (Motivo: os resgates de conteúdo único das branches do passo 3 aterrissaram na jsgvth;
  deletá-las antes do merge perderia o único caminho vivo desses arquivos.)

PASSO 3 (só após o passo 2): delete `claude/pu-14-instances-ey91o2` e
  `claude/backlog-audit-separation-w1vu4b`.
  Justificativa: o conteúdo único delas foi resgatado na jsgvth (auditoria "nada se
  descarta", 2026-07-03); após a consolidação ao main, o safety-check de arquivos únicos
  passa a dar 0.

AO FINAL: confirme que `git ls-remote --heads` mostra só `main` + branches de trabalho
vivas (claude/project-analysis-pending-20wc81 é a instância atual — NÃO deletar).
Reporte o que deletou e o que ficou.
```

---

## PROMPT 2 — Supabase P6: fechar a porta da API (exposed schemas)

```
Você vai fechar uma porta de API no projeto Supabase `potencial-urbano-iptu-tdc`
(ref: csnalylpvysjvejgsymr, região sa-east-1). É uma mudança de configuração no
Dashboard — não é SQL (a tabela PostGIS pertence ao supabase_admin e RLS nela é
bloqueado; o fix real é tirar o schema da API).

PASSOS:
1. Abra https://supabase.com/dashboard -> projeto `potencial-urbano-iptu-tdc`.
2. Project Settings -> API (ou "Data API") -> campo "Exposed schemas".
3. REMOVA `public` da lista. MANTENHA `graphql_public`. NÃO adicione `governanca`
   (o app não consome via REST hoje; governanca tem RLS deny-all e fica fora da API).
4. Salve.

VERIFICAÇÃO (obrigatória): faça um GET anônimo em
  https://csnalylpvysjvejgsymr.supabase.co/rest/v1/spatial_ref_sys?select=srid&limit=1
  com o header `apikey: <anon key>` (Settings -> API keys).
  ANTES da mudança isso retorna dados; DEPOIS deve retornar erro (schema não exposto).
NÃO mexa em nada de PostGIS/extensões (mexer arrisca o geoprocessamento — decisão M-41).
Reporte: print da config salva + resultado do GET de verificação.
```
