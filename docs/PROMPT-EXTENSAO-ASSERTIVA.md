# Prompt para a extensão (Manus) — caminhos reais da API Assertiva (F)
> Entregue ao dono em 2026-08-07 (PU 23). Destrava o enriquecimento de contatos do Motor Comercial:
> a credencial OAuth2 JÁ está validada (R$ 0 gasto); falta só o CAMINHO exato dos endpoints,
> que aparece apenas no painel autenticado da conta. Colar o texto abaixo na extensão,
> com a sessão logada em painel.assertivasolucoes.com.br.

---

Você é meu assistente técnico. Estou logado no painel da Assertiva Soluções. Preciso que você colete a DOCUMENTAÇÃO DE INTEGRAÇÃO dos produtos contratados — sem fazer NENHUMA consulta de dados (consultas são pagas; documentação é grátis). Passos:

1. Acesse https://integracao.assertivasolucoes.com.br/v3/doc/ (ou o link "Documentação/Integração/API" do painel).
2. Liste TODOS os produtos/APIs que aparecem como CONTRATADOS/disponíveis para esta conta (ex.: Localize, CPF, CNPJ, Score, Crédito).
3. Para cada produto contratado, copie:
   a. O CAMINHO COMPLETO (path) de cada endpoint — ex.: `GET /localize/v3/cpf/{cpf}` ou o que estiver escrito, EXATAMENTE como aparece;
   b. Os parâmetros obrigatórios de cada endpoint;
   c. Um exemplo de RESPOSTA (o JSON de exemplo da documentação — NÃO faça chamada real).
4. Se houver um arquivo OpenAPI/Swagger para baixar (JSON ou YAML), baixe e me entregue.
5. NÃO clique em "Testar", "Executar", "Consultar" nem em nada que dispare uma consulta real — só leitura de documentação.

Entregue: a lista de produtos contratados + os paths exatos por produto + os exemplos de resposta + o arquivo OpenAPI se existir.

---
> **Destino (dono):** me mandar o texto/arquivo. Com os paths reais eu ligo o
> `assertiva-extrair` (parser já consertado; idempotência por nota de consulta; zero re-cobrança)
> e o botão "Enriquecer via Assertiva" do CRM sai do modo desabilitado.
