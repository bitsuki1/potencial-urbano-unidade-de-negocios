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
  continuidade nas fronteiras + mutação anti-oráculo.
- `evals/eval-iptu-oficial.py` — **CONFRONTO contra o lançamento REAL** (3.905 cedentes, insumos do
  IPTU_2026). Os três no `consolidar.yml` e no `fechar-instancia.py`.

## Confronto com o lançamento REAL (2026-07-10) — pendência do dono "subir IPTU_2026" RESOLVIDA
O `IPTU_2026.csv` (894 MB, 3,92 M linhas) já estava no Supabase Storage. Extraí os 3.905 cedentes por
streaming (via Edge Function de uso único; ver `PROXIMA-INSTANCIA.md`) e obtive, POR IMÓVEL, os insumos
que a própria Prefeitura aplicou: **valor m² de terreno (PGV), valor m² de construção, ano da construção,
fator de obsolescência, tipo de terreno, esquinas, fração ideal** (`zepec/oficial/iptu2026_cedentes.csv`,
schema corrigido + enriquecido).
- **PROVA:** o engine reproduz EXATO `área × valor_m2_terreno` do lançamento nos **2.763 terrenos Normais**.
- **BUG corrigido:** a coluna 17 do IPTU_2026 é *valor do m² do terreno*, não *valor venal* — estava
  mal-rotulada `v_venal_m2` (3905/3905). Corrigido no CSV, no `filtro_iptu.py` e no `enriquecer_oficial.py`.

## Pendências DECLARADAS (o que falta para o VV TOTAL)
1. ~~**PGV por codlog**~~ ✅ **RESOLVIDA** — `valor_m2_terreno` por cedente veio do lançamento oficial.
2. ~~**Ano de construção por cedente**~~ ✅ **RESOLVIDA** — `ano_construcao` no CSV enriquecido.
3. **Tabela de obsolescência do exercício** — ACHADO QUANTIFICADO: a Tabela IV de 1986 (só idade, piso
   0,30) está SUPERADA; a curva vigente de 2026 tem piso 0,20 e depende de CATEGORIA, não só da idade
   (37/3861 batem). Não se ajusta tabela a partir do dado (1.1): **capturar a norma que alterou a Tabela IV**.
4. **Valores m² de construção do exercício** — a Tabela VI/2013 é nominal; 2026 é monetariamente atualizado
   (decreto anual). Capturar a tabela do exercício.
5. **Tabela I (profundidade)** e **Tabela V (enquadramento)** — não extraídas; fatores/tipo são entrada do chamador.
