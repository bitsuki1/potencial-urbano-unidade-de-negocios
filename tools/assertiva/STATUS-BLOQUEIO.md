# Assertiva — status do bloqueio (turno noturno 2026-08-07)

> **Custo gasto até aqui: R$ 0,00.** Nenhuma consulta paga foi faturada — todas as tentativas
> pararam ANTES da consulta (erro de rota), e o desenho é fail-closed.

## O que funciona
- **Autenticação OK.** `POST /oauth2/v3/token` com Basic (client_id:secret) devolve `access_token`
  válido. As credenciais `ASSERTIVA_CLIENT_ID`/`SECRET` (GitHub Secrets) estão certas.
- **Conexão ao banco OK** (após a vacina de frota do pooler aws-0↔aws-1).

## O que trava
Toda chamada a produto (Localize, CPF, CNPJ, em vários caminhos candidatos) devolve:

```
HTTP 403 {"message":"Invalid key=value pair (missing equal-sign) in Authorization header
(hashed with SHA-256 and encoded with Base64): '<token>'"}
```

Esse é o erro do **AWS API Gateway** quando o endpoint espera assinatura **AWS SigV4** e recebe um
**Bearer**. Traduzindo: **o caminho que estamos chamando NÃO é a rota do produto** — está caindo
numa rota do gateway que exige outro tipo de autenticação. O token Bearer está certo; o **path** é
que é desconhecido.

## Por que não dá para descobrir daqui
- O caminho exato de cada produto se confirma no **Swagger autenticado da conta**
  (`integracao.assertivasolucoes.com.br/v3/doc/`), que exige **login interativo no portal** — não
  alcançável por esta sessão headless.
- Sondagens automáticas de caminhos candidatos (com documento inválido, sem faturar) não acharam
  uma rota que responda validação em vez do 403 do gateway.

## Caminho (ação do dono — deixado por último, conforme sua regra)
1. No **painel da Assertiva** (`portal.assertivasolucoes.com.br` → Integração/API/Swagger), confira:
   (a) se o produto **Localize** está **habilitado no plano** desta credencial; (b) o **path exato**
   do endpoint de consulta por CPF/CNPJ (algo como `/localize/v3/<recurso>?<param>=`).
2. Me passe o path (ou o link do Swagger da conta) e eu ajusto `assertiva_client.localizar()` numa
   linha e disparo o lote dos 100 do triângulo histórico (já selecionados em `alvos_lote1_100.csv`).

Tudo pronto do nosso lado: cliente, executor idempotente, workflow, alvos e destino (CRM no
Supabase). Falta só o **path certo**, que só o portal entrega.
