# INFRA E ACESSOS — Potencial Urbano (identidades, projetos, credenciais)
> Registro de infraestrutura do projeto. **NÃO guarda segredos** (chaves/tokens ficam FORA do git —
> em env/Colab/secret manager). Guarda só IDENTIDADES, papéis e ONDE cada segredo mora.
> Criado em 2026-07-05 (PU 18) ao descobrir um recurso que NENHUM doc registrava — o dono
> perguntou "instalamos um robô no Drive e não lembro para que serve". Anti-perda (D83): agora está aqui.

## Conta de serviço do Drive (o "robô") — CONFIRMADO 2026-07-05 (SSOT = escritório, cofre)
> **Descoberto/confirmado ao cruzar com `escritorio-do-mou/cofre/COFRE-DE-ACESSOS.md` (M-81, trilho D153-B
> "Drive acessível a todos").** O dono não lembrava para que servia; o cofre do escritório tinha o registro
> completo. Este arquivo é a CÓPIA DE CONVENIÊNCIA no PU; a fonte da verdade é o cofre do escritório.
- **Identidade:** `escritorio-do-mou@portfolio-do-mou.iam.gserviceaccount.com` (conta de serviço do Google Cloud).
- **Projeto Google Cloud:** `portfolio-do-mou` (nº `496034297673`) — criado pelo MOU em 2026-07-03.
- **Escopo:** `https://www.googleapis.com/auth/drive` (Drive completo — LÊ e ESCREVE).
- **Papel no Drive:** **Editor (writer)** sobre a pasta-raiz **`PORTFÓLIO DO MOU`** (`1DkJl24-tQrLhO-WeuuAjwa8ahws8VbYf`)
  e, por herança, toda a árvore abaixo — inclui `POTENCIAL URBANO` (`1BrM6q36meTtn5guJoiGbqvCtZF11Uau3`)
  e a zona de despejo `01 — _entrada` (`1grhqYgttj7KnJmiu9U73z-lXFHnFthov`). Confirmado via
  `get_file_permissions` (MCP, 2026-07-05) e pela tela de Compartilhar do dono.
- **Dono humano da pasta:** `eduardo@saobentoservicos.com.br` (Proprietário). Acesso geral: **Restrito**.
- **PARA QUE SERVE (agora documentado):** identidade programática do **Escritório do MOU** para **ler E
  ESCREVER o Drive do portfólio sem interação humana** — feita para os **workflows automáticos (GitHub
  Actions)** de cada unidade operarem o Drive (M-81 / D153-B). Casa com a doutrina "Ingestão determinística
  via Drive/Supabase connector" (CLAUDE.md Parte 3).
- **ESTADO (cofre, 2026-07-03): ✅✅ PROVADO PONTA-A-PONTA** — chave válida + Drive API ATIVA + pasta
  PORTFÓLIO DO MOU compartilhada + **ESCRITA testada** (criou+apagou arquivo). Resíduo declarado: setar o
  secret `GOOGLE_SA_KEY` no repo de cada unidade (UI do MOU) para os workflows automáticos rodarem.
- **ONDE MORA A CHAVE (segredo — NUNCA no git):** valor da `private_key` vive como **GitHub Secret
  `GOOGLE_SA_KEY`** (setado por repo, na UI do MOU). É o mesmo desenho do `BITRIX_WEBHOOK`. Para gerar/rotacionar:
  Google Cloud Console → projeto `portfolio-do-mou` → IAM → Contas de serviço → esta conta → **Chaves** →
  *Adicionar chave → Criar nova → JSON*. NUNCA colar em chat nem commitar.
- **CAMINHO ROBUSTO para a arrumação:** um **GitHub Action** neste repo que lê o secret `GOOGLE_SA_KEY`,
  autentica como o robô e move os 1.360 arquivos pelo de-para auditado (`drive-arrumacao/de-para-COMPLETO-2026-07-04.csv`),
  DRY_RUN primeiro. Dispensa a extensão, o Apps Script, o consentimento OAuth e o limite de 6 min.
- **Nota de segurança (para o dono decidir depois):** writer sobre o portfólio INTEIRO inclui os CSVs de
  PII (sócios/CPF). Superfície ampla. Recomendação: estreitar o acesso do robô só às pastas que opera e
  rotacionar a chave após cada uso pesado (casa com o gate de segurança do ROADMAP, risco #5).

## Supabase
- **Projeto:** `potencial-urbano-iptu-tdc` — ref `csnalylpvysjvejgsymr`, região `sa-east-1` (Postgres 17 +
  PostGIS + pgvector + pg_trgm/unaccent/fuzzystrmatch). Dado real vive em `governanca` (RLS deny-all).
- **Segredos:** chaves S3 do Storage e chaves de API ficam em env/Colab (ver `zepec/pipeline/subir-grandes-colab.py`
  e `extracao/PROMPT-EXTENSAO-BRANCHES-E-SUPABASE.md`), NUNCA no git.

## Drive — IDs âncora (para scripts)
- Shared drive do portfólio: `0APQMETkmU9TbUk9PVA` · raiz PORTFÓLIO DO MOU: `1DkJl24-tQrLhO-WeuuAjwa8ahws8VbYf`.
- POTENCIAL URBANO: `1BrM6q36meTtn5guJoiGbqvCtZF11Uau3` · `01 — _entrada`: `1grhqYgttj7KnJmiu9U73z-lXFHnFthov`.
- Pastas-destino da arrumação: 00 Governança `1zfDGtvhZh1JDUykC6kouDPqm-E3u0bgO` · 02 Leis&Juris
  `1GRvv6Xbi3_rKpZvvIqKIjyByu1LgFjmJ` (+2.1–2.7) · 03 Tabelas `1v4H2YsIZSNDwNXiMtOAV1w1qy-5kOuvy` ·
  05 Geo/Mapas · 99 Inbox. (Mapa completo por arquivo: `drive-arrumacao/de-para-COMPLETO-2026-07-04.csv`.)
