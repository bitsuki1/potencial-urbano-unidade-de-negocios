# 🧰🔑 ACESSOS ÀS FERRAMENTAS — todo projeto usa, com senha, à mão (D160)
> **Autorizado pelo MOU (2026-07-07):** "elas precisam estar acessíveis aos projetos, a todos, com senha e tudo, facilmente."
> **Repo PRIVADO.** Postura amoral D106: senha no git é risco conscientemente aceito pelo dono — não levantar, não rotacionar.
> **Este arquivo é sincronizado para TODOS os repos do portfólio** pelo robô (`.github/workflows/portfolio-robot.yml`), para que qualquer sessão de projeto o tenha localmente, sem co-montar o escritório.
> **USO ≠ ESCRITA:** ter a chave de uma ferramenta não muda as fronteiras de escrita em repositórios (DEV `keepee-facilities` = leitura por todos; canônico de unidade = via caixa).
> **As chaves de PODER TOTAL** (service_role do Supabase, private_key da conta de serviço, senha do certificado A1) **NÃO entram no git** — aqui só o ponteiro. Elas vivem em GitHub Secret / painel.

---

## 1. Supabase — banco de dados na nuvem (dado pesado + busca por IA + funções)
| Campo | Valor |
|---|---|
| Login | `contato@bitsuki.com.br` · senha `Duda@20262728` |
| Organização | **Gestão Integrada** (`kovmqsfwfytxnuspnxxc`) |
| Projeto principal | **gestao-integrada-dados** (`lbjudeifksyeqminwlto`, sa-east-1) — URL `https://lbjudeifksyeqminwlto.supabase.co` |
| Chave pública (para o cliente) | `sb_publishable_YkkrpqvZ4mDY2KLq0g473A_6JRrSqcj` |
| Projeto do Potencial Urbano | **potencial-urbano-iptu-tdc** (`csnalylpvysjvejgsymr`, sa-east-1) — PostGIS + busca por IA |
| service_role (poder total) | ⛔ **NÃO no git** — pegar no painel Supabase quando precisar |
| Como usar | MCP `Supabase` (já disponível em toda sessão) ou a chave pública no cliente. |
| Quem já usa | Keepee · bitsuki · Potencial Urbano · bitrix-aux. **Pode usar:** qualquer unidade com muito dado. |

## 2. VPS Brasil — máquina sempre ligada, com IP do Brasil
| Campo | Valor |
|---|---|
| O que é | Servidor próprio ligado 24h, endereço brasileiro (MasterDWeb, Ubuntu 22.04, ~R$60/mês). Abre sites .gov.br que só respondem do Brasil e roda tarefas agendadas. |
| Runner GitHub | label `brasil` — **só em repos PRIVADOS da conta `bitsuki1`** (fronteira de confiança, D155). Admin = MOU. |
| Como usar | no seu workflow, `runs-on: [self-hosted, brasil]`. Setup e exemplo: `sba-unidades-de-negocios/tools/br-runner/SETUP.md` + Action `rodar-mg-br.yml`. |
| Quem já usa | SBA (coleta de prefeituras). **Pode usar:** Potencial Urbano e Keepee (sites .gov.br), qualquer job agendado. |

## 3. Robô do Bitrix (bitrix-aux) — operar Tarefas e Projetos do Bitrix24
| Campo | Valor |
|---|---|
| O que é | 2 endpoints MCP (ler/escrever) no Supabase que operam o portal `keepee.bitrix24.com.br`. Já no ar. |
| Segredos (webhook + tokens) | ⛔ no env do Supabase (fora do git, por desenho). |
| Como usar | endpoints `bitrix-read`/`bitrix-write` (13 comandos). Manual: `bitrix-aux/HANDOFF.md` + `README.md`. |
| Quem já usa | Keepee. **Pode usar:** quem for tocar tarefas no Bitrix. |

## 4. Robô do Google Drive — escreve/organiza no Drive de ponta a ponta
| Campo | Valor |
|---|---|
| Conta de serviço | `escritorio-do-mou@portfolio-do-mou.iam.gserviceaccount.com` (projeto GCP `portfolio-do-mou`) |
| Chave JSON (poder total) | ⛔ **NÃO no git** — GitHub Secret **`GOOGLE_SA_KEY`** (o MOU seta por repo, na UI). |
| Estado | ✅ provado ponta-a-ponta (cria/apaga arquivo na pasta "PORTFÓLIO DO MOU"). |
| Como usar | no workflow, autenticar com `GOOGLE_SA_KEY` → Drive API. Exemplo pronto: AVC `publicar-bp-no-drive.yml`. |
| Quem já usa | Escritório · AVC. **Pode usar:** qualquer unidade que publica no Drive (ex.: SBA, que sobe estudos toda hora). |

## 5. OnSuite — o sistema do site da Keepee (ordens de serviço / faturamento)
| Campo | Valor |
|---|---|
| Login | `eduardo@saobentoservicos.com.br` · senha `Duda@2026` |
| Ambiente | ⚠️ **PRODUÇÃO** (apesar do "teste" na URL) |
| Front / API | `https://on-suite-teste.azurewebsites.net` · API `https://on-suite-teste-api.azurewebsites.net` |
| Autenticar | `POST /Security/Token` `{"email","senha"}` → Bearer (expira; gerar a cada uso) |
| Regra de ouro | **nenhuma escrita em produção sem OK explícito do MOU** ("isto escreve no Onsuite"). |
| Mapa da API + scripts | `keepee-unidade-de-negocios/.../dados/onsuite/` (145 controllers mapeados). |
| Quem já usa | Keepee + Profinders (compartilham). **Pode usar:** quem precisar dos dados de OS. |

## 6. Lovable — criar site/app com IA (código fica no Git)
| Campo | Valor |
|---|---|
| Como usar | MCP `Lovable` (já disponível na sessão). Git = fonte da verdade; Lovable espelha. |
| Quem já usa | bitsuki · AVC (3 apps) · CCEV (site). **Pode usar:** quem tem produto/site. |

## 7. Manus — faz tarefas longas sozinho (ex.: transcrever vídeos)
| Campo | Valor |
|---|---|
| O que é | Executa trabalhos pesados de muitos passos de ponta a ponta. |
| Como usar hoje | via MOU (relay inter-instância). Prompts de exemplo: Profinders `PROMPTS_MANUS.md`. |
| Quem já usa | Profinders. **Pode usar:** CCEV (transcrever gravações — em vez de construir do zero), qualquer tarefa longa. |

## 8. GitHub — conta bitsuki1
| Campo | Valor |
|---|---|
| Login | `contato@bitsuki.com.br` · senha `Duda@20262728` |
| Como usar | MCP `github` (já disponível). Git nativo no Claude Code. |
| Fronteira | DEV `keepee-facilities` = leitura por todos, escrita só do dono (D119/D145). |

## 9. Métodos replicáveis (não são app — são jeitos de fazer que já funcionam)
- **Lei ao pé da letra → número com fonte** (Potencial Urbano): extrair a lei exata e calcular citando a origem. Serve a qualquer fiscal/tributário (SBA, Keepee).
- **Estudo automático cidade-a-cidade** (SBA): calcular+escrever em série, conferível. Serve a qualquer produção repetível.
- **Conciliação de 3 fontes** (Keepee): cruzar sistema × ERP × banco para achar o dinheiro real.

## 10. Outros (ponteiro)
- **Gamma · Figma/FigJam** — apresentações e quadros (MCP disponível).
- **Certificado A1 (fiscal) · Protheus · e-CAC · Jira** — logins com o MOU / painel (poder sensível fora do git).

---
> **Falta acesso a alguma ferramenta?** Isso é **bloqueio de infra** — abra uma pendência de acesso (DE com DoD). Nunca "não é minha".
