# PLANEJAMENTO DOS MOTORES — notas de trabalho (FASE DE DISCUSSÃO, não executar)
> Registrado a pedido do dono (2026-07-06): *"quero planejar agora, não quero que produza, apenas anote
> e vamos discutir ponto a ponto antes."* Nada aqui vira código/engine sem o dono aprovar ponto a ponto.
> Doutrina: dialético · nada se descarta · citação obrigatória · **anti-oráculo** (do escrutínio 2026-07-06:
> um "codex único inabalável" já custou caro ao repo — Fi=1 canonizado errado).

## 0. Princípio transversal que o dono pediu (vale para TODOS os motores)
Direção literal do dono, a ser honrada em cada motor:
- **Contexto do PORQUÊ em tudo:** cada elemento (lei, fórmula, camada de mapa, fonte de dado) carrega
  *por que está sendo usado* e *por que essa e não aquela*.
- **Visão detalhada por motor:** o que **ENTRA**, o que **NÃO entra**, **por quê**, e quais as **TAGS**.
- **Escrutinável sob várias lentes sem o problema da REGRESSÃO e da SÍNTESE:** organizar de modo que dá
  para revisar/atacar cada peça isoladamente sem perder o rastro quando algo muda (lei que entra, lei que sai).

> **Proposta de instrumento (a discutir):** uma **"ficha detalhada do motor"** — template único preenchido
> por motor — ver §5. É o que materializa "quero mais dados de cada motor".

## 1. Chão — a Esteira de Dados
- **Direção do dono:** *"quero arrumar, quero ele perfeito, funcional, nos melhores moldes e técnicas
  possíveis."*
- **Pedido explícito:** **estudo com diversas lentes + plano de trabalho.**
- **[ABERTO — discutir antes de rodar]** quais lentes o estudo usa. Candidatas (a confirmar/podar com o dono):
  arquitetura de dados (medallion/lakehouse × simples) · canonicidade & reprodutibilidade (banco reconstruível
  do git) · vintage/vigência (1.6 em DADOS, não só em leis) · procedência/SSOT · segurança/PII · custo ·
  observabilidade/gates no CI · on-path × off-path (o número in-scope hoje NÃO toca o Postgres).
- **Ganchos que já existem (contexto):** crise de canonicidade do Supabase (migrations vivas sem `.sql` no
  git; migrations do git nunca aplicadas) — `MOTOR-2-ESTRATEGIA.md`, `docs/ESCRUTINIO-CONJUNTO-MOTORES.md` S1.

## 2. Motor da Lei — a questão do CODEX (a decisão mais rica)
- **Experiência do dono:** TDC e IPTU têm **muitos substitutivos, leis complementares, anexos, lei que entra
  e lei que sai.**
- **Estratégia anterior do dono:** um **CODEX** com **tese / antítese / síntese / vacina** para tudo que existe.
- **Dúvida do dono (aberta):** *"documento único talvez não seja o melhor... mas deixá-los organizados e o
  porquê de cada um estar sendo usado, assim dá para escrutinar sob várias lentes sem o problema da regressão
  e da síntese."*
- **[DECISÃO ABERTA — D?]** arquitetura do corpus da Lei: **(A)** documento único (codex monolítico) ×
  **(B)** peças organizadas por norma + camada de rationale ("por que em uso") + vigência × **(C)** híbrido.
- **Contexto que já existe:** o repo JÁ tem `leis/<id>.md` (verbatim) + `leis/<id>.json` (vigência,
  altera/alterada_por, remissões) + `MANIFESTO.json`. A doutrina 1.1 separa os 4 artefatos e 1.5/1.6 tratam
  vigência. O escrutínio marcou "não canonizar oráculo". → a opção (B) conversa com o que já existe.

## 3. Motor das Fórmulas — idem (contexto do porquê)
- **Direção do dono:** cada fórmula com o **contexto**: por que essa fórmula, por que esse valor/tabela e
  não outro.
- **Contexto que já existe:** `engines/tdc/pcpt.py` (Fi escalonado Art.24) e `oodc.py`; a divergência de ~27%
  vs certidões (exposta, não escondida); preço PAUSADO (`art128.py` inexistente).

## 4. Motor do Mapa — idem (contexto do porquê)
- **Direção do dono:** cada camada/decisão espacial com o porquê: por que essa geometria, essa fonte, essa regra.
- **Contexto que já existe:** overlay por área × centroide; ZOE com regime próprio (Quadro 2A); Regra da Esquina
  (Decreto 57.536); Motor do Mapa hoje FORA do selo (sem eval de zona).

## 5. Proposta de template — "ficha detalhada do motor" (a discutir o formato)
Para cada motor, uma ficha com estes campos (materializa "o que entra/não entra/por quê/tags/detalhe"):
- **Papel na corrente** (e dependências reais).
- **ENTRA** — fontes e artefatos, cada um com path e *por que está em uso*.
- **NÃO ENTRA** — e o *porquê* de ficar fora (escopo, doutrina, alternativa descartada).
- **Escolhas & alternativas** — por que essa técnica/fonte e não a outra (tese/antítese/decisão).
- **TAGS / metadados** — esquema de tags que torna cada peça filtrável e escrutinável isolada.
- **Vigência/versão** — o que muda no tempo (lei que entra/sai; dado com vintage).
- **Como se escrutina sem regressão** — lentes aplicáveis + âncora de prova.
- **As-built × alvo** — o que existe hoje vs o que falta (honestidade, sem fingir pronto).

## 6. Pontos para discutir (ponto a ponto — nada avança sem o dono)
1. Por qual motor começamos o detalhamento?
2. **Motor da Lei:** codex único (A) × organizado-com-rationale (B) × híbrido (C)?
3. **Esteira:** alinhar as lentes do estudo ANTES de rodar (§1) — quais entram, quais saem?
4. **Template da ficha (§5):** serve como está, ou ajustar campos?
5. Onde estas fichas vivem (um doc por motor? uma pasta `docs/motores/`?) e como se ligam ao MANIFESTO.

> Estado: **conversando.** Este arquivo é o rascunho vivo do planejamento; cada decisão fechada vira entrada
> datada nas DECISÕES e (se virar trabalho) DoD no BACKLOG.
