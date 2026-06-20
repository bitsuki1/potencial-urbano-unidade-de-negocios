# scripts/ — esteira determinística do RAG (E1→E5)

> A esteira que leva uma norma VERBATIM até uma **resposta com citação** (CLAUDE.md 1.7).
> Tudo aqui é **determinístico, stdlib-only, SEM LLM e SEM embeddings** (Princípios 1.3/1.4):
> o LLM (caro) só entra DEPOIS, para redigir prosa amarrada às citações que estes scripts devolvem.
> Trazido pela instância orquestradora do Potencial Urbano — 2026-06-20.

## Ordem do pipeline

```
leis/<id>.md (VERBATIM)  ──fatiar.py──▶  rag/chunks/<id>/*.json
                                              │
                                         indexar.py
                                              ▼
                         rag/index/{chunks,invertido,metadados}.json
                                              │
                          consultar.py "pergunta..."  ──▶  dispositivo(s) + CITAÇÃO
                                              │
                          evals/rodar-evals.py  ──▶  GATE (citação correta)
```

| script | papel | entra | sai | status_pipeline |
|---|---|---|---|---|
| `fatiar.py` | chunking estrutural por dispositivo (2.5) | `leis/**/*.md` verbatim | `rag/chunks/<id>/` | `bruto → fatiado` |
| `indexar.py` | índice invertido BM25 + metadados (2.6) | `rag/chunks/` | `rag/index/` | `fatiado → indexado` |
| `consultar.py` | retrieval híbrido c/ citação obrigatória (1.7 / Parte 3 etapa 5) | `rag/index/` + pergunta | citação rastreável | — |
| `consolidar.py` | regenera `MANIFESTO.json` (1.5/2.3) | `**/*.json` | `MANIFESTO.json` | — |
| `_texto.py` | tokenização CANÔNICA compartilhada (index ≡ consulta) | — | — | — |

## Rodar local

```bash
python3 scripts/fatiar.py        # fatia todas as leis verbatim elegíveis
python3 scripts/indexar.py       # (re)constrói o índice
python3 scripts/consultar.py "qual o limite de atualizacao do valor venal residencial em 1969?"
python3 evals/rodar-evals.py     # gate de aceite (exit !=0 se ground-truth ATIVO falhar)
```

A GitHub Action `consolidar.yml` roda essa cadeia inteira a cada push e usa os evals como gate.

## Decisões de projeto (e seus porquês)

- **GUARDA DE VERBATIM (1.7):** `fatiar.py` só fatia `.md` com o cabeçalho `## Texto integral (verbatim)`
  e `.json` com `confianca_extracao: "alta"`. Resumo não-verbatim **não entra no RAG** — citar uma
  síntese seria resposta não-fundamentada. Hoje só a **Lei 7.228/1968** (municipal-SP, re-ingerida
  verbatim de `_entrada/`) passa; as outras 26 leis aguardam re-ingestão verbatim (P2 do handoff).
- **BM25 (não TF bruto):** normaliza por tamanho do dispositivo. Sem isso, um artigo longo (cheio de
  texto citado) vence por volume, não por relevância — o `Art. 1º` mascararia o `Art. 5º`.
- **GATE DE COBERTURA (1.7):** uma resposta só é `FUNDAMENTADA` se o melhor dispositivo cobrir
  ≥ 34% dos termos-de-conteúdo da pergunta. Bater só em uma palavra genérica (ex.: "direito" para uma
  pergunta sobre "direito de construir") devolve **NÃO-FUNDAMENTADA** — o RAG nunca responde sem citar.
- **SEM embeddings (ainda):** a camada semântica é uma extensão FUTURA, plugável no mesmo índice. O
  tier keyword tem limites declarados (ver vacinas em `evals/ground-truth/iptu-7228-1968.json`): p.ex.
  data-de-vigência por remissão entre artigos exige grafo de remissões, não keyword puro.
- **Número NUNCA aqui (1.3):** estes scripts roteiam e citam; valor/cálculo é do engine (`engines/`).
