# engines/iptu — spec do motor de IPTU (STUB, não construir sem "vai" do dono)
> PU 18 · 2026-07-09. Terreno preparado (D-DONO-14/17: IPTU fora desta rodada; expertise guardada).
> Espelha `engines/tdc/pcpt.py`. Doutrina: número nasce no engine (1.3); tabela = input rastreável;
> lei = fonte citada; vigência por dispositivo (1.6). Ver `docs/EXPERTISE-TDC-PARA-IPTU.md`.

## O que o motor calculará (determinístico)
```
Valor Venal (VV) = VV_terreno + VV_construção
  VV_terreno    = area_terreno   × valor_m2_terreno(PGV, logradouro/codlog) × fatores_terreno
  VV_construção = area_construida × valor_m2_construcao(padrao/uso)          × fatores_constr × depreciação
IPTU = VV × alíquota_progressiva(VV, uso) − desconto_da_faixa
```
- **Alíquota progressiva:** faixas de VV com alíquotas crescentes + parcela a deduzir por faixa
  (residencial × não-residencial). Fonte: Lei 15.889/2013 e alterações (17.719/2021, 17.733/2022) — a INGERIR.
- **Entradas oficiais já disponíveis:** `zepec/oficial/iptu2026_cedentes.csv` traz `area_terreno`,
  `area_construida`, `v_venal_m2`, `codlog`, `uso`, `padrao` por SQL. O `v_venal_m2` é o VV/m² que a
  **própria Prefeitura calculou** → serve de **gabarito do VV** (bater o nosso VV contra ele).

## Tabelas de entrada (a extrair verbatim — não digitar)
- `tabelas/iptu-pgv-terreno.csv` — valor do m² de terreno por logradouro/codlog (PGV, Anexo Lei 15.889/2013).
- `tabelas/iptu-valor-construcao.csv` — valor do m² de construção por padrão/tipo.
- `tabelas/iptu-aliquotas-faixa.csv` — faixas de VV × alíquota × parcela a deduzir (uso res./não-res.), datadas.
- `tabelas/iptu-fatores.csv` — fatores corretivos (terreno/construção) + depreciação.

## Gate (mesmo do TDC — só adicionar linhas)
- Auto-teste `engines/iptu/iptu.py --demo` ancorado em valores legais (como `pcpt.py --demo`).
- `evals/eval-iptu.py` — golden-assert contra ≥1 **lançamento real** (SQL → VV → IPTU), tolerância declarada.
- Entra no `consolidar.yml` como novos passos (não gate novo).

## NÃO fazer agora
Construção só quando o dono abrir o IPTU. Este stub existe para **herdar**, não recomeçar.
