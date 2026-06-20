# 2ª Auditoria Profunda — Potencial Urbano (pós-destraves)

> RO-24 (triplo-limpo após QUALQUER alteração). Audita a superfície NOVA da sessão: 12 federais
> verbatim (1.246 chunks), `engines/tdc/oodc.py`, mecanismo "ladrão", CI, docs. Lentes DIFERENTES da
> 1ª auditoria (D82 — re-rodar a mesma lente = falsa convergência). Read-only nas fontes; 2 correções
> aplicadas na hora, resto → `BACKLOG.md` (B-11..B-14). Cada conciliação é provisória.

## 0. Lentes (4, adversariais, paralelas) + ground-truth
1. **Fidelidade da promoção verbatim + chunking** (12 federais, 1.246 chunks).
2. **Correção do engine** (`oodc.py` — recálculo à mão de cada fórmula).
3. **O "ladrão" + malha de gates/CI** (testes destrutivos em cópia /tmp).
4. **Consistência documental & dívida de propagação** (estado real × o que os docs dizem).

## 1. Veredito
O **texto verbatim é fiel** (reconstrução byte-a-byte 12/12, nada perdido; saneamento de rodapé não
comeu conteúdo) e a **matemática do engine está correta** (9 casos recalculados à mão batem; constantes
F_i 1:1 com a fonte; auto-teste é prova, não circular). MAS há **3 defeitos sérios** no que a sessão
construiu: o **gate dá falso-verde** (o mais grave — o "ladrão" não protegia), o **chunker gera citações
falsas** (viola 1.7), e há **dívida de propagação** (docs antigos re-contaminam). O MANIFESTO e o
depósito ao escritório estão **factualmente limpos**.

## 2. CRÍTICOS

### A2-01 (CRÍTICO → **CORRIGIDO**) — O gate dava FALSO-VERDE: a flag `status` desarmava os evals. *(Lente 3 / F-1,F-2)*
- **ANTÍTESE:** com `rag/index` zerado (retrieval morto), bastava `status:"aguardando_verbatim"` no único
  ground-truth ativo (ou deletá-lo) → `falhas_ativas=0` → evals exit 0 → `fechar-instancia.py` VERDE.
  Índice destruído, gate verde. O "ladrão" não capturava o pior caso.
- **VACINA:** "evals exit 0" ≠ "evals provaram algo" — pode ser 0 casos ativos.
- **CORREÇÃO aplicada:** `rodar-evals.py` agora exige **piso de itens ATIVOS** (`MIN_ITENS_ATIVOS=4`);
  0 ativos → exit 1. Provado: flip→aguardando deixa 0 ativos → VERMELHO; restaurado → VERDE.

### A2-02 (CRÍTICO, parcial → suffix p/ B-11) — Chunker gera CITAÇÕES FALSAS (viola 1.7). *(Lente 1)*
- **ANTÍTESE:** `fatiar.py` regex `^\s*Art\.?\s*(\d+)` (a) descarta o sufixo: "Art. 156-A" (IBS, inserido
  pela EC-132 na Constituição) virou chunk `rotulo:"Art. 156"`, `citacao:"EC 132/2023 — Art. 156"` —
  dispositivo que **não existe**; `consultar.py` devolve isso no surface. (b) artigos CITADOS dentro de
  leis alteradoras viram chunks autônomos → **~409 chunks federais com rótulo duplicado** (6015:216,
  11101:81, 10931:41, 4591:30, 9514:28, 8668:11). O VERBATIM é completo (nada perdido) — o defeito é
  partição/rótulo/citação.
- **VACINA:** "fatiar por `^Art\.\d+` é fiel" está ERRADO em corpus alterador: "Art. N" citado ≠ "Art. N
  da norma X"; "-A/-B" é dispositivo distinto.
- **DESTRAVE → B-11** (não refatorei às pressas — re-fatiar toca 1.246 chunks; a própria 1ª auditoria
  mostrou que pressa gera bug). Mitigação imediata: as leis afetadas são federais/registrais, NÃO o
  produto TDC (base inicial).

### A2-03 (CRÍTICO → **CORRIGIDO**) — Engine inventava valor: HMP=0,5 (viola 1.3). *(Lente 2 / E-01)*
- **ANTÍTESE:** `FATOR_SOCIAL["HMP"]=Decimal("0.5")` — a fonte dá **0,4 a 0,6** (FAIXA). Escolher 0,5 é o
  engine arbitrando número de tabela (proibido por 1.3). Mitigado por ser código morto, mas latente.
- **CORREÇÃO aplicada:** removido o 0,5; Fs/Fp viraram `*_REF` (faixa textual "0.4..0.6", não usada no
  cálculo — `outorga_onerosa` recebe fp/fs como ENTRADA externa). O engine não escolhe a mediana.

## 3. ALTOS / MÉDIOS (→ BACKLOG)
- **A2-04 (ALTO, Lente 1) — vigência POR CHUNK (1.6):** texto compilado tem redação revogada/anterior como
  chunks separados, mesma vigência da atual, sem marca "revogado" (ex.: 6015 "Art. 288" 9×). → B-11(c).
- **A2-05 (ALTO, Lente 3 / F-6) — CI publica antes de testar:** `consolidar.yml` COMITA+PUSHA os artefatos
  ANTES de rodar evals/engine → estado quebrado vai pra branch e só então o build falha. → B-13(F-6).
- **A2-06 (ALTO, Lente 2 / E-03) — decimal BR quebra o engine:** `_d("1,5")` → ValueError; as tabelas-fonte
  (Q14) são BR (vírgula). Liga `tabelas/` e estoura. → B-12.
- **A2-07 (ALTO, Lente 4 / E-02) — 3 docs ainda cravam "NENHUMA das 27 é verbatim / 27 a re-ingerir"**
  (ACIONABILIDADE CRÍTICA-1, catalogo-README, CONSOLIDACAO) — a narrativa que a sessão inteira desmentiu,
  sem marca SUPERADO; re-contamina a próxima instância. → B-14.
- **A2-08 (MÉDIO, Lente 2) — código morto Fs/Fp** (resolvido junto de A2-03: agora `*_REF`, declarado).
- **A2-09 (MÉDIO, Lente 1) — boilerplate de portal** no chunk preâmbulo dos 12 federais (citável). → B-11(d).
- **A2-10 (MÉDIO, Lente 2 / E-04) — DECIMAL(10,3) sem guarda de 10 dígitos totais** (overflow silencioso). → B-12.
- **A2-11 (MÉDIO, Lente 2 / E-05) — Fp/Fs sem guarda de sinal** (OODC negativa aceita) + docstring de `_d` mente. → B-12.
- **A2-12 (MÉDIO, Lente 3 / F-3,F-4,F-5) — gate com furos menores:** stray-tag só vê 3 pastas/3 sufixos
  (ignora ground-truth/tabelas/csv); não checa push; backlog-fresh aceita data em qualquer linha. → B-13.
- **A2-13 (MÉDIO/CRÍTICO de propagação, Lente 4 / E-01,E-03) — `_PROCESSADOS.md` e `HANDOFF:33` dizem
  "bruto"** para o que está `indexado`. → B-14.
- **A2-14 (MÉDIO, Lente 4 / E-04) — "15 municipais a re-ingerir"** em ≥4 superfícies (real = 14). → B-14.
- **BAIXOS:** scripts/README sem 2 scripts; CODEX 3 versões; F-7 (manifesto worktree×index); F-8 (hook
  wrapper sem env); E-06 (FATAL_ERROR trava diluída); E-07 (citação por lei, não dispositivo). → B-12/B-13/B-14.

## 4. LIMPO (anti-viés — não inflar a crítica)
- **Texto verbatim:** reconstrução byte-a-byte 12/12; rodapé saneado removeu SÓ lixo ("Stop Claude"/`*`),
  preservou notas oficiais e assinaturas; 0 chunk vazio; 0 órfão; D24 ok; ECs com `tipo_norma` correto.
- **Matemática do engine:** as 4 fórmulas conferem com a fonte (recálculo à mão); constantes F_i 1:1;
  auto-teste é prova; as 5 travas implementadas batem com o pseudo-SQL.
- **Idempotência/CI determinismo:** `fatiar+indexar+consolidar` 2× = byte-idêntico (md5); sem loop de commit.
- **MANIFESTO coerente** com a realidade física (13/14/30, engines:11, 2 fora-escopo); `_nota_verbatim` correta.
- **Depósito ao escritório FACTUALMENTE FIEL:** todos os números batem (6015=4.601 linhas, 210 IRRF×1 IPTU,
  corpus 1→13, gate pegou .pyc 11×12). Nenhum exagero.
- **Doutrina preservada:** nenhum princípio 1.1–1.7 violado pelas mudanças (além dos defeitos acima, já
  endereçados/backlogados); vacinas "Tema 1130≠PU", "número no engine", "citação obrigatória" vivas.

## 5. Correções aplicadas nesta passada
A2-01 (gate falso-verde → piso de evals) · A2-03/A2-08 (valor inventado HMP + código morto → `*_REF`).
Gate verde após as correções. Resto registrado em `BACKLOG.md` B-11..B-14 com DoD.
