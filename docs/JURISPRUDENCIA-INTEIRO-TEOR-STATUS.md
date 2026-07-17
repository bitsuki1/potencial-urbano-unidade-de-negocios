# Inteiro teor da jurisprudência — status de captura (2026-07-17)

> **Tarefa:** capturar o INTEIRO TEOR (verbatim oficial) dos 10 processos hoje em FICHA (metadados + resumo
> próprio). **Decisões judiciais são domínio público** (Lei 9.610/98, Art. 8º, IV) — reproduzir o verbatim é
> legítimo. **Bloqueio atual é de INFRA de rede**, não de direito. Regra 1.7/1.8: **NÃO ingerir texto de
> espelho** (JusBrasil/Escavador) como fonte — só o primário oficial re-extraído.

## Veredito: BLOQUEADO por infra desta sessão (não por captcha nos 3 casos)
| Fonte | Acesso desta sessão | Efeito |
|---|---|---|
| **STF** (`jurisprudencia.stf.jus.br`) | ❌ falha de TLS no proxy de egresso (HTTP 000) | não abre nenhuma página do STF |
| **STJ** (`scon.stj.jus.br`) | ❌ desafio Cloudflare (403) | SCON + inteiro teor bloqueados |
| **TJSP `cposg`** (2º grau) | ✅ **aberto, sem captcha** | metadados oficiais + inteiro teor de decisões monocráticas |
| **TJSP `cjsg`** (ementa indexada) | ❌ reCAPTCHA | ementa dos acórdãos de mérito não sai por automação |

## Caminho para destravar (recomendação fechada)
1. **STF (RE 226942, RE 387047):** o bloqueio é o **proxy de egresso desta sessão** (não é captcha). Do
   **runner `brasil` do hub `portfolio-automacoes`** (rede no Brasil, sem esse proxy) os PDFs de inteiro teor
   abrem — é a melhor rota. _(Esta unidade NÃO escreve no hub, D120: é um disparo a pedir ao Escritório/MOU.)_
2. **STJ (AgRg AREsp 179340, REsp 1130545):** Cloudflare interativo — navegador headless com resolução de
   challenge (cookie/JS) OU o mesmo runner externo. Alvos: SCON + `documento/?documento_tipo=integra`.
3. **TJSP:** o `cposg` já entrega o inteiro teor das **decisões monocráticas** por automação (comprovado no
   item 5). Para a **ementa dos acórdãos** (itens 8–10), abrir a **pasta digital** a partir do `cposg` ou
   resolver o reCAPTCHA da `cjsg`.

## URLs OFICIAIS exatas (para captura em um passo quando destravar)
| # | Processo | id | URL oficial direta | Metadado oficial confirmado (cposg) |
|---|---|---|---|---|
| 1 | RE 226942/SC | `stf-re-226942-sc` | jurisprudencia.stf.jus.br (buscar "RE 226942") | 1ª Turma; solo criado (Florianópolis, Lei 3.338/89) — **a confirmar no oficial** |
| 2 | RE 387047/SC | `stf-re-387047-sc` | jurisprudencia.stf.jus.br (buscar "RE 387047") | Pleno; Rel. Eros Grau; DJe 30/04/2008 — **ementa a re-extrair do oficial** |
| 3 | AgRg AREsp 179340/SP | `stj-agrg-aresp-179340-sp` | scon.stj.jus.br/SCON (buscar "AgRg no AREsp 179340") | identidade não confirmada com segurança |
| 4 | REsp 1130545 | `stj-resp-1130545` | scon.stj.jus.br/SCON (buscar "REsp 1130545") | provável /RJ, Rel. Fux, repetitivo IPTU — **a confirmar** |
| 5 | AI 2126162-35.2025 | `tjsp-ai-2126162-35-2025` | esaj.tjsp.jus.br/cposg/show.do?processo.codigo=RI008R5FG0000 | Rel. Márcio Kammer de Lima; **decisão monocrática CAPTURÁVEL agora** (CONPRESP, Res. 20/2024) |
| 6 | AI 2257458-20.2024 | `tjsp-ai-2257458-20-2024` | esaj.tjsp.jus.br/cposg/show.do?processo.codigo=RI008ALQP0000 | Rel. José Luiz Mônaco da Silva |
| 7 | AI 2324382-13.2024 | `tjsp-ai-2324382-13-2024` | esaj.tjsp.jus.br/cposg/show.do?processo.codigo=RI008EQHX0000 | Rel. José Luiz Mônaco da Silva |
| 8 | ApCiv 0000175-39.2017 | `tjsp-apciv-0000175-39-2017` | esaj.tjsp.jus.br/cposg/show.do?processo.codigo=1H000A8VF0000 | Rel. Souza Meirelles; Fazenda Pública; tombamento |
| 9 | ApCiv 0000177-09.2017 | `tjsp-apciv-0000177-09-2017` | esaj.tjsp.jus.br/cposg/show.do?processo.codigo=RI00483UW0000 | Rel. Rebouças de Carvalho; **9ª Câmara Dir. Público**; tombamento |
| 10 | ApCiv 1070175-76.2019 | `tjsp-apciv-1070175-76-2019` | esaj.tjsp.jus.br/cposg/show.do?processo.codigo=RI005VFLP0000 | Rel. Spoladore Dominguez; Dir. Público |

> **O que NÃO foi feito (e por quê):** nenhuma ementa foi ingerida como verbatim — o que circula em espelhos
> (ex.: RE 387047) é não-oficial e fica FORA do corpus até re-extração do primário (1.8). As fichas atuais
> (resumo próprio) permanecem válidas como metadados. Este documento é o mapa para fechar a captura assim que
> a rota de rede (runner `brasil` / headless com challenge) estiver disponível.
