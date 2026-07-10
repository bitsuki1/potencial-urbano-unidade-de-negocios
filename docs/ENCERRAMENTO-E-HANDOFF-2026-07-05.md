# ENCERRAMENTO + HANDOFF — Potencial Urbano — 2026-07-05 (PU 17)
> Honestidade total, zero síntese. Fatos, comandos, decisões. Cada afirmação é verificável pelo comando ao lado.
> Branch: `claude/potential-urban-instance-jsgvth` · último commit: `cfbae13` · gate: `python3 scripts/fechar-instancia.py` = **VERDE (17/17)**.

## 1. DECISÕES desta sessão (o que EU decidi, sob o gate do projeto D21)
| # | Decisão | Por quê | Reversível? |
|---|---|---|---|
| D-a | **Domínio TDC×IPTU = METADADO (`dominio[]`), não pasta.** | Uma norma serve aos dois; pasta duplica/perde. | sim (é campo no .json) |
| D-b | **`compartilhado` entra nas consultas dos DOIS domínios** (regra de não-perda). | Decisão do dono "não quero perder nada" → viés na dúvida = compartilhado. | sim |
| D-c | **Taxonomia do Drive = a de JUNHO** (00/02.1-2.7/03/05/99); a "Opção B" fica como reorg futura. | A de junho está fiada (1.360 mapeados, pastas criadas); rodar as duas colide. | sim (backlog) |
| D-d | **Lei 17.844/2022 → `tdc`** (estava mistagueada `iptu`). | É a lei-núcleo da Transferência do Direito de Construir. | sim |
| D-e | **Corpus declarado PARCIAL na vitrine** (README/DISCLAIMER/veredito), não "esperar ingerir tudo". | Honestidade: 19/31 leis, TDC normativo ausente. | — |
| D-f | **Saneamento do lago = dedup por hash + quarentena datada** (não lixeira, não congelar). | Decisão do dono; "nada se descarta". | sim (é onda Drive) |
| D-g | **Git limpo/pushado viram HARD no gate; o número entregue (pcpt_m2) vira gateado.** | "Perda de dados" é o modo de falha nº1; o produto não pode mentir número sem o gate pegar. | — |

## 2. DECISÕES que são do DONO (travam avanço; eu NÃO decido)
| # | Decisão pendente | O que destrava | Custo de NÃO decidir |
|---|---|---|---|
| O-1 | **Rodar os Apps Scripts no Drive** (Sanear-Lago → Organizar-Entrada), colar os logs em `inventario/gas-log-<data>.txt`. | A arrumação sai de PLANO → PROVADA; 1.360 arquivos organizados de verdade. | o Drive segue bagunçado; a toolchain fica só desenhada. |
| O-2 | **Ingerir o TDC normativo** (Decreto 57.536/2016 + decretos ZEPEC) em `leis/` verbatim. | o RAG passa a fundamentar consultas TDC-normativas; `dominio tdc` deixa de ser 1 lei só. | o produto TDC repousa sobre tabelas cujo texto-fonte está FORA do RAG (limite 1.7). |
| O-3 | **Re-ingerir as 12 municipais IPTU `bruto`** (verbatim do Drive) + **despausar preço**. | corpus 19→31; filtro temporal completo; preço de mercado (hoje só proxy). | corpus IPTU parcial; sem lei-mãe 6.989/1966. |
| O-4 | **Backfill de `fonte.hash`** (precisa dos arquivos-fonte, no Drive). | o gate de proveniência "hash confere" passa a rodar; D-DONO-4 auditável. | proveniência não é verificável campo-a-campo. |
| O-5 | **3 forks do ROADMAP** (posição na cadeia · ordem de expansão · **régua de preço**) — `ROADMAP-PU.md` §2; **B-23** (deletar 3 branches remotas — depende de consolidar `jsgvth`→`main` antes). | M1 (ferramenta religada com preço) destrava; higiene de branches. | preço fica pausado (só proxy); 5 branches `claude/` no remoto. |
| O-6 | **Recriar a tag `beta-2026-07-05`** na UI do GitHub (o push da tag caiu por política; a tag é LOCAL e some no reset). | marca durável do estado beta. | perde-se o marcador de release beta (cosmético). |

## 3. ESTADO REAL (medido agora, não declarado)
```
gate de fechamento .............. VERDE 17/17     (python3 scripts/fechar-instancia.py)
evals RAG ....................... 17/17 PASS       (python3 evals/rodar-evals.py)
produto (cedentes reais) ........ 7/7 PASS         (python3 evals/eval-produto.py)
arrumação (loop e2e sintético) .. OK               (python3 evals/eval-arrumacao.py)
corpus indexado ................. 19/31 leis · 1.865 chunks
  dominio dos chunks ............ iptu 753 · compartilhado 996 · tdc 116
arrumação Drive ................. PLANO — 1.360 arquivos no índice, 0 movidos no Drive
fonte.hash ...................... null em 31/31 leis  (proveniência não-verificável mecanicamente)
revisado_por_humano ............. 0/63               (tudo confia na extração do modelo)
MOTORES ......................... T1·T2·T3·T4 FEITOS e provados · T8·G1 VIVOS
```

## 4. BETA — o que está USÁVEL agora (com o limite explícito)
| Entregável | Como usar | LIMITE honesto |
|---|---|---|
| **Ferramenta de cedentes ZEPEC** (`zepec/ferramenta/`) | `lista_prospeccao.csv` (2.740 prontos p/ abordar) + `COMO-USAR.md` | preço é **proxy** (PCpt×V), não mercado; PCpt do já-declarado é estimativa; divergência ≈1,66× vs certidões. |
| **Engine PCpt/OODC** (`engines/tdc/`) | `pcpt.py --demo` | Fi escalonado provado; mas `pcpt.py` **hardcoda** os CSVs (AUD-A01) — corrigir antes de escalar. |
| **RAG por domínio** (`scripts/consultar.py`) | `consultar.py --dominio tdc "..."` | corpus **PARCIAL** (declara "CORPUS: PARCIAL"); TDC normativo ausente (O-2). |
| **Toolchain de arrumação do Drive** | ver §5 | está em **PLANO**; a prova é o log do dono, nenhum check confronta o Drive ao vivo (AUD-A08). |
**Selo BETA:** número confiável SÓ onde o gate cobre (Fi/PCpt dos cedentes). Fora disso: `PENDENTE` declarado. Não é laudo/parecer (DISCLAIMER).

## 5. COMANDOS — o dono roda, em ordem (arrumação do Drive)
```
1. script.google.com → ligar Serviços+ > Drive API v3.
2. Sanear-Lago-TDC-2026-07-04.gs      : DRY_RUN=true → conferir Log → DRY_RUN=false → rodar.
3. Organizar-Entrada-2026-07-04.gs    : idem (ensaio → real).
4. Colar os dois Logs em inventario/gas-log-2026-07-XX.txt (no repo).
5. python3 scripts/reconciliar_arrumacao.py   → MESTRE + trilha; gate sai de 'plano'.
6. Se aparecer inventario/cross-tree-dups.csv: python3 scripts/gerar_gas_crosstree.py → rodar o .gs → repetir 5.
7. python3 scripts/gate-arrumacao.py --require-executed   (exit 0 = Drive PROVADO).
```

## 6. BACKLOG vivo (D83 — DoD mecânica em `docs/AUDITORIA-PROFUNDA-2026-07-05.md` §onda-2/3 e em `BACKLOG.md`)
`AUD-A01` pcpt lê CSV · `AUD-A10` backfill fonte.hash · `AUD-A11`(=O-2) ingerir TDC · `AUD-B08/B09` schema+vigência das 12 · `AUD-A08` gate real vs Drive · `AUD-B01` fixture domínio independente + revisão humana · `AUD-C05/C06` data de redação / anexo PDE · **T8** (vedação substring) · **G1** (overlay centroide).

## 7. O que NÃO é verdade (para ninguém se enganar)
- ❌ "O RAG cobre IPTU e TDC." → cobre IPTU parcial; TDC normativo NÃO ingerido.
- ❌ "O Drive está arrumado." → está PLANEJADO; nada foi movido (O-1).
- ❌ "A proveniência é auditável." → `fonte.hash` é null; é doutrinária, não verificada.
- ❌ "O gate de arrumação prova que o Drive ficou certo." → prova que o LOG é consistente; não confronta o Drive.
- ❌ "Os números foram revisados por humano." → 0/63; confiam na extração do modelo (gate mecânico ≠ revisão jurídica).

---
> **Próxima instância:** o gate é a verdade. Rode `python3 scripts/fechar-instancia.py` — se VERDE, não recomece o que ele prova. Comece pelo §6 (backlog) ou pelas decisões do dono §2. Zero-compressão: nada aqui é resumo do que existe no git; é o ponteiro para o git.
