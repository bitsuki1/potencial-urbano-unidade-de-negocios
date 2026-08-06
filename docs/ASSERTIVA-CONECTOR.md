# Assertiva Soluções — conector (bureau de dados) · estado e proposta ao Escritório

> Frente aberta pelo dono (2026-08-05): "já temos a ferramenta [painel Assertiva] e precisamos conectar; iremos
> enviar também ao Escritório para ele incorporar essa ferramenta em portfolio-automação". Uso pedido: **as três
> pontas** (localizar/enriquecer, validar CPF-CNPJ, score/risco) **+ preparado para o que mais surgir**.

## O que a Assertiva é (glosa)
Bureau de dados brasileiro (*data bureau* — empresa de enriquecimento/consulta cadastral). Serve para achar e
qualificar contato/empresa a partir de CPF/CNPJ. No Potencial Urbano alimenta principalmente o **Motor Comercial**
(prospecção do lado vendedor / cedentes) e a qualificação de leads.

## Conector (construído; credencial SETADA e validada — probe OAuth2 v3 OK, sem consulta paga)
- **`tools/assertiva/assertiva_client.py`** — cliente OAuth2 (`client_credentials` + Basic), fail-closed (1.3),
  custo-consciente (1.4). Métodos: `localizar()`, `validar_cpf()`, `consultar_cnpj()`, `score()` e `chamar()`
  (porta genérica p/ qualquer endpoint v3 — extensível "para o que mais surgir"). Lê a credencial do ambiente.
- **`.github/workflows/assertiva-probe.yml`** — Action de *probe*: **só autentica** (prova credencial + rota,
  **não dispara consulta paga**). Roda com os secrets do repo.

## ▶️ Passo do dono — FEITO (credencial setada; probe autenticou). Registro do procedimento:
1. No painel `https://painel.assertivasolucoes.com.br` (ou `app.assertivasolucoes.com.br`), achar **Integração/API/
   Credenciais** e pegar **Client ID** + **Client Secret** (padrão OAuth2 da Assertiva).
2. No repo `potencial-urbano-unidade-de-negocios` → **Settings → Secrets and variables → Actions**, criar:
   - `ASSERTIVA_CLIENT_ID`
   - `ASSERTIVA_CLIENT_SECRET`
3. Avisar — eu disparo `assertiva-probe` (só-auth) para confirmar a rota; depois valido cada produto (localize/
   cpf/cnpj/score) contra o Swagger autenticado da conta e ligo o que o Motor Comercial precisar.

## Endpoints (padrão v3 documentado — a confirmar no Swagger da conta)
Base: `https://api.assertivasolucoes.com.br` · Token: `POST /oauth2/v3/token` (Basic + `grant_type=client_credentials`).
Produtos sob `/localize/v3`, `/cpf/v3`, `/cnpj/v3`, `/score/v3`. Os *leaf paths* exatos por produto contratado se
confirmam no Swagger autenticado (`integracao.assertivasolucoes.com.br/v3/doc/`) — por isso o *probe* (auth) é o
teste de conexão e cada produto é validado ao vivo quando a credencial estiver setada.

## 🧰 Proposta de ficha para o COFRE do hub `portfolio-automacoes` (D160/D162 · padroniza o Escritório, D38)
> Esta unidade **usa**, mas o SSOT do cofre é do hub e a incorporação é do Escritório (USO ≠ ESCRITA). Segue a
> ficha pronta para o Escritório colar em `ACESSOS-FERRAMENTAS.md` (credencial por ponteiro, postura amoral D106):

```
### Assertiva Soluções (bureau de dados / enriquecimento cadastral)
- O que é: consulta e enriquecimento por CPF/CNPJ (localizar contato, validar situação cadastral, score de crédito).
- Painel: painel.assertivasolucoes.com.br · app.assertivasolucoes.com.br
- API: OAuth2 client_credentials — POST https://api.assertivasolucoes.com.br/oauth2/v3/token (Basic id:secret);
  produtos /localize/v3, /cpf/v3, /cnpj/v3, /score/v3. Doc: integracao.assertivasolucoes.com.br/v3/doc/
- Credencial (ponteiro): Client ID/Secret na conta Assertiva do MOU. Cada unidade usa via Actions Secret próprio
  do seu repo (ASSERTIVA_CLIENT_ID / ASSERTIVA_CLIENT_SECRET); a chave é de poder e não vive no git (D106).
- Conector de referência: potencial-urbano-unidade-de-negocios/tools/assertiva/assertiva_client.py (reusável).
```
