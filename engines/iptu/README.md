# engines/iptu — motor do IPTU (CONSTRUÍDO em 2026-07-10)
> **O "vai" do dono:** mensagem do MOU de 2026-07-10 — *"finalizarmos as duas frentes, tdc e iptu…
> execute tudo que for possível sem mim"* — abriu a frente IPTU (supera o congelamento D-DONO-14/17,
> que valia "até o dono abrir"). Construído pela instância PU 18 na mesma sessão, herdando esta spec.
> Doutrina: número nasce no engine (1.3); tabela = dado verbatim com vintage (1.1); citação por
> dispositivo (1.7); vigência declarada (1.6). Ver `docs/EXPERTISE-TDC-PARA-IPTU.md`.

## O que o motor calcula (engines/iptu/iptu.py — determinístico, fail-closed)
```
VV = VV_terreno + VV_construção                       (Art. 17, Lei 10.235/1986)
  VV_terreno    = área × valor_m2(PGV) × fatores      (Art. 4º c/c Tabelas I/II/III)
  VV_construção = área_construída_bruta × valor_m2(Tabela VI, por subdivisão)
                  × fator_obsolescência(Tabela IV)    (Art. 11, redação Lei 15.889/2013; Art. 16)
IPTU = VV × alíquota_base(uso)                        (Arts. 7º/8º/27, Lei 6.989/1966, red. 13.250/2001)
       + Σ (porção do VV em cada faixa × ajuste)      (Arts. 7º-A/8º-A/28; faixas Lei 15.889/2013)
```
- **Verbatim por trás:** Lei 6.989/1966 (328 arts) e Lei 10.235/1986 (texto compilado) capturadas do
  portal oficial em 2026-07-10 (`scripts/capturar_lei_portal.py`) e indexadas no corpus.
- **`uso_canonico()`**: mapeia o uso do lançamento (IPTU_2026) ao vocabulário legal
  {residencial · nao_residencial · territorial} — determinístico, recusa uso não mapeado.

## Tabelas de entrada (todas verbatim, com vintage em `tabelas/METADATA.json`)
- `tabelas/iptu-aliquota-base.csv` — 1,0% resid. · 1,5% não-resid. · 1,5% territorial (red. 13.250/2001).
- `tabelas/iptu-aliquotas-faixa.csv` — ajuste por porção, 5 faixas × 3 usos (Arts. 3º/4º/5º, Lei 15.889/2013).
- `tabelas/iptu-valor-construcao-m2.csv` — Tabela VI (tipo × padrão × subdivisão).
- `tabelas/iptu-fator-obsolescencia.csv` — Tabela IV (idade → fator 1,00…0,30).
- `tabelas/iptu-fatores-terreno.csv` — Tabelas II (esquina) e III (encravado/fundo/interno).

## Gate (ligado em 2026-07-10)
- `engines/iptu/iptu.py --demo` — ancorado em valores derivados À MÃO da lei (16 âncoras).
- `evals/eval-iptu.py` — golden independente: âncoras recomputadas + dupla-via CSV×engine +
  continuidade nas fronteiras + mutação anti-oráculo. **No `consolidar.yml` e no `fechar-instancia.py`.**

## Pendências DECLARADAS (o que falta para o confronto com o lançamento real)
1. **PGV / Listagem de Valores por codlog** (Anexo III, Lei 15.889/2013) — dado pesado; sem ela,
   `vv_terreno` exige `valor_m2_pgv` como entrada rastreável. → gabarito `gabarito-iptu-vv.json`
   com status `aguardando_pgv`.
2. **Ano de construção por cedente** (Art. 16 — idade p/ obsolescência) — não vem no IPTU_2026 atual.
3. **Faixas monetariamente atualizadas do exercício** (decreto anual) — as faixas nominais são de 2013;
   confronto com lançamento 2026 exige a tabela do exercício (vintage!).
4. **Tabela I (profundidade)** — lookup longo não extraído; fator é entrada do chamador.
5. **Tabela V (enquadramento tipo/padrão)** — não extraída; tipo/padrão são entrada do chamador.
