# EXPERTISE TDC → IPTU — o que o TDC ensinou e o IPTU herda
> PU 18 · 2026-07-09. Criado a pedido do dono ("já vai preparando terreno para IPTU" + D-DONO-14/17:
> IPTU fora desta rodada, mas a **expertise fica guardada** para herança). Doutrina: "o pipeline replica"
> (CLAUDE.md P4; base inicial = TDC, IPTU vem depois). Este doc é o **atalho** para quando o IPTU abrir:
> não recomeçar — herdar o método já provado no TDC.

## 1. O método que replica (mesmo esqueleto dos 4 artefatos, 1.1)
| Artefato | No TDC (feito) | No IPTU (a fazer, mesmo molde) |
|---|---|---|
| **Lei** | leis/ verbatim + .json (vigência/remissões) + RAG | idem — ingerir as leis IPTU de `_entrada/iptu/` |
| **Tabela** | Quadro 3 (CAbás/zona), Quadro 2A (macroárea), Fi (Art.24), Q14 (V do m²) | **PGV** (valor do m² terreno/construção), **alíquotas por faixa**, fatores corretivos |
| **Fórmula/Engine** | `engines/tdc/pcpt.py` (PCpt = Atc × CAbás × Fi) | `engines/iptu/` — VV × alíquota progressiva (ver `engines/iptu/README.md`) |
| **Tese** | tese/tdc (1-a-1, sob corpus verbatim) | tese/iptu — mesmo ritmo |

## 2. As lições duras (não repetir os erros do TDC)
1. **Número nasce no engine (1.3), nunca no CODEX.** O TDC canonizou um Fi=1 errado num monolito e pagou caro. IPTU: alíquotas/valores vêm de **tabela CSV rastreável ao dispositivo**, com grep-gate no CI (já existe: proíbe ler número de `CODEX-*.md`).
2. **Gabarito de ponta a ponta é obrigatório.** No TDC, o Termo 006/2026 (717,60 m²) pegou o furo GEO-2 ao vivo. IPTU: o gabarito é o **lançamento/carnê real** (SQL → valor venal → IPTU devido) — bater o engine contra ele com tolerância declarada. Fonte: o próprio `IPTU_2026.csv` traz `v_venal_m2` por SQL (a Prefeitura já calculou o VV — é o gabarito pronto do VV).
3. **Vigência por dispositivo (1.6).** Alíquota/PGV mudam por ano e por lei (15.889/2013 → 17.719/2021 → 17.733/2022…). A base guarda a data; o engine seleciona por ela; nunca aplicar a de hoje ao fato gerador de outro ano.
4. **A tabela SAI do texto (extração pura, 1.2).** PGV e alíquotas são tabelas — extrair verbatim dos anexos (ex.: Anexo I da Lei 15.889/2013 já em `_entrada/iptu/`), não digitar à mão.
5. **O gate primeiro.** O runner pinado + evals que reprovam sabotagem já existem no `consolidar.yml` — o IPTU entra no MESMO gate (mais linhas de eval), não num gate novo.

## 3. O que JÁ temos de IPTU (inventário, 2026-07-09)
- **Corpus bruto em `_entrada/iptu/`** (NÃO ingerido ainda — domínio IPTU=0 no MANIFESTO):
  Lei 15.889/2013 (+ Anexo I de valores), Decreto 57.443/2016, Lei 14.094/2005, Lei 17.733/2022,
  Lei 17.844/2022, Lei 11.428, + explicador "base de cálculo do IPTU".
- **Dados:** `IPTU_2026.csv` (~3,92M linhas no Drive; recorte cedentes em `zepec/oficial/iptu2026_cedentes.csv`)
  com `v_venal_m2`, `area_terreno`, `area_construida`, `uso`, `padrao` por SQL — insumo direto do VV.
- **Docs prévios:** `docs/CORRECOES-E-VACINAS-IPTU.md`, `_entrada/iptu/base-de-calculo-do-iptu-migalhas.txt`.
- **Faltam (captura/extração):** as leis de **alíquotas vigentes** (Lei 17.719/2021 e alterações) e a
  **PGV completa** (planta genérica de valores) como tabela; e ≥1 **gabarito de lançamento** real.

## 4. Diferenças TDC × IPTU (onde NÃO copiar cego)
- **Escopo/cliente:** TDC = vendedor de potencial (nicho). IPTU = universo de contribuintes (massa) — o
  produto-fim do IPTU é outro (ex.: revisão de lançamento, contestação de VV), a DEFINIR pelo dono (não
  presumir — D-DONO-8: o projeto não escolhe estratégia sem o dono pedir).
- **Geo:** o TDC precisa de zona-base/CAbás (SISZON). O IPTU precisa da **face/quadra** e da PGV por logradouro
  (CODLOG) — o `IPTU_2026` já traz `codlog`; a "Regra da Esquina" (Decreto 57.536, já ingerido no TDC) tem
  paralelo no IPTU (valor por face). Parte do geo do TDC (overlay lote×logradouro) reaproveita.
- **Fórmula:** TDC é 1 produto (PCpt). IPTU é **progressivo por faixa** com descontos — mais faixas, mesma
  disciplina determinística.

## 5. Ordem sugerida quando o IPTU abrir (NÃO executar agora — D-DONO-14)
1. Ingerir o corpus de `_entrada/iptu/` (verbatim → fatiar → indexar; domínio=iptu).
2. Extrair PGV + alíquotas por faixa → `tabelas/iptu-*.csv` (verbatim dos anexos).
3. `engines/iptu/` — VV × alíquota progressiva, auto-teste ancorado + eval contra 1 lançamento real.
4. Gabarito: SQL → VV (do IPTU_2026, oficial) → IPTU devido, com tolerância declarada.
> Tudo isto herda o gate, o método de gabarito e a separação de artefatos já provados no TDC. **É atalho, não recomeço.**
