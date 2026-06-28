# HANDOFF EXTREMAMENTE HONESTO — Potencial Urbano, fim da sessão 2026-06-24
> Para a próxima instância (e para o MOU). Zero spin. Aqui eu digo o que um status polido esconderia.
> Estado VIVO: este doc + `PROXIMA-INSTANCIA.md` (topo) + `BACKLOG.md` + `docs/SESSAO-2026-06-24.md`.
> Branch: `claude/project-audit-roadmap-2thi1g` (PU e escritório). Gate mecânico: VERDE.

## 0. Veredito honesto em um parágrafo
A sessão entregou **dois destraves reais e verificáveis** (TDC no RAG; engine sobre tabelas reais) e **preparou** o produto (H3) sem poder prová-lo, porque o produto de verdade depende de dados que não estão e não podem entrar aqui. **Nada do que afirmo como "feito" é fé — é rodável** (evals 11/11, engine auto-testa, consultas TDC citam dispositivo). **Mas o "produto" ainda NÃO existe como número confiável por imóvel** — o que existe é o TRILHO provado em amostra. Não confunda trilho provado com produto entregue.

## 1. O que está REALMENTE pronto (e COMO eu sei — não acredite, rode)
- **RAG TDC vivo:** 19 leis / 1.877 dispositivos indexados. Prova: `python3 evals/rodar-evals.py` → 11/11 PASS (3 TDC ativos); `python3 scripts/consultar.py "outorga onerosa"` cita PDE Art. 114/116.
- **Engine sobre dado real:** `python3 engines/tdc/oodc.py` → auto-teste OK, inclui asserção sobre V real (SQ 001003/Codlog 038121 = R$3.106) × CA_max real (ZEU=4).
- **Tabelas:** `tabelas/q14-valor-terreno.csv` (6.715 V), `quadro3-ca-por-zona.csv` (39 zonas), `quadro5-fator-social-fs.csv`. Extraídas por `scripts/extrair_quadros.py` (determinístico).
- **Durabilidade:** ambos os repos commitados e pushados; gate verde; MANIFESTO idempotente.

## 2. O que PARECE pronto mas tem RESSALVA (não tome como verdade fechada)
- **Os R$ que o `gerar_alvos.py` imprime NÃO são produto.** São cálculo correto sobre uma AMOSTRA com `zona`, `area_adicional`, `fp`, `fs` ILUSTRATIVOS. Fp=1,2/Fs=1,0 são chute; a área adicional é fórmula não-validada contra caso real. **Nenhum número foi conferido contra uma OODC real da Prefeitura (Fase 3 do CODEX nunca foi feita).**
- **A fórmula do engine (OODC) só é correta para TRIAGEM de oportunidade máxima** (achado A-078). Para calcular a OODC de um projeto real com área < potencial pleno, ela SUBESTIMA (até ~2×). Está documentado (D-15) mas é uma armadilha se alguém usar como "calculadora".
- **As 6 leis-pilar TDC têm texto CONSOLIDADO (com emendas até 2023) mas metadado de vigência = data ORIGINAL** (A-079). Marquei `versao_texto:consolidada`, mas o filtro temporal do RAG (quando existir) ainda vai confundir redação de 2023 com a de 2014. Não confie em pergunta histórica ("o que valia em 2018?") até a vigência-por-chunk (B-11c).
- **CA_max de 8 zonas tem nota condicional `(d)(f)(g)…` cuja legenda NÃO foi capturada** (A-080). O engine AVISA, mas o valor pode estar errado para certos usos (ex.: ZEIS). Não use CA_max dessas zonas em produção sem buscar a legenda no PDF.
- **Engine "validado" = auto-teste, não caso real.** O auto-teste prova consistência interna e o wiring, não que o resultado bate com a Prefeitura.

## 3. O que está BLOQUEADO e EM QUEM (não dá pra destravar daqui)
- **O produto (B-2 / 1º JOIN) — bloqueado no MOU.** Precisa de `IPTU_2026.csv` (938MB) + `socios.csv` (3,4GB) + geo/LOTES, que estão atrás da cerca do Drive. Caminho pronto: `scripts/transferir-pesados-drive-supabase.md` (rclone) + `supabase/migrations/` (não aplicadas). **Sem o MOU rodar isso, o produto não anda.**
- **OCR das 12 municipais em resumo — decisão não tomada.** D-PU-OCR lista 4 opções; nenhuma escolhida.
- **Consolidação à `main` — decisão do MOU.** Esta frente está 13 commits à frente da main (`ad1af85`), só na branch. NÃO é estado oficial até alguém decidir mergear.
- **Supabase Storage / migrations — ação física.** MCP oscilou (caiu e voltou); as migrations de produto seguem não-aplicadas.

## 4. RISCOS que podem morder a próxima instância
1. **Tratar a lista de alvos como pronta para prospecção.** Não é. Falta dado real + validação Fase 3. Vender isso como produto = passivo.
2. **"Corrigir" o engine para a fórmula At/Ac** sem ler D-15 → quebra a triagem que está certa.
3. **Assumir a branch como oficial** e construir por cima sem o MOU consolidar → risco de divergência/retrabalho.
4. **Re-obter verbatim TDC do Drive achando que dá 403** → JÁ FOI FEITO; ler D-13 antes (não refazer).
5. **OCR de PDF-imagem sem validar texto×imagem** → traz alucinação (D-PU-OCR). As 12 restantes precisam disso.

## 5. Verdades desconfortáveis (o que eu NÃO resolvi)
- **3 dos 4 artefatos ainda são finos.** O corpus jurídico (Lei) está forte; **Tabela** está só com Q14/Q3/Q5 (falta Fp, IPTU, ITBI, geo); **Engine** roda mas sem validação real; **Tese** está vazia (`tese/` 0 arquivos). O "produto" é o cruzamento dos quatro — e três ainda não estão prontos.
- **O mérito JURÍDICO das teses/leis nunca foi auditado** (B-10) — só proveniência/fidelidade do texto.
- **A extração do Drive ficou parcial** (~55 de 378 docs-texto; 8 sub-agentes morreram no limite de sessão). Resume por `inventario/lotes-pull/`.
- **PII em `socios.csv`** será carregado por decisão amoral do MOU (D106) — risco aceito, mecanismo RLS deny-all permanece. Não é "resolvido", é "aceito".
- **Eu (a instância) cometi erros nesta sessão** que só pegamos por auditoria: loader que sobrescrevia V silenciosamente, jogar fora notas do Quadro 3, "6 schemas" onde eram 7, deixar o MANIFESTO dizendo "14". Todos corrigidos — mas o padrão é claro: **sem a lente adversarial + a emulação de boot, vários teriam passado.** Não baixe a guarda dessas duas ferramentas.

## 6. O próximo passo único mais honesto
**Não é codar.** É o MOU decidir e executar UMA coisa: **subir os dados pesados (rclone) + aplicar as migrations**, que destrava o B-2 (o produto). Tudo que dá pra fazer sem isso (semântico B-5, remissões B-6, vigência-por-chunk B-11c, OCR B-4) é melhoria de infraestrutura — legítima, mas **não é o produto**. Enquanto o dado não entra, o projeto fica "trilho pronto, trem sem carga".

> Se você é a próxima instância: rode `python3 scripts/fechar-instancia.py` para ver o gate, leia `BACKLOG.md` (SSOT do que falta), e **não acredite em mim — rode os 3 comandos da §1**. Se algum falhar, o handoff mentiu; conserte e me culpe no rastro.
