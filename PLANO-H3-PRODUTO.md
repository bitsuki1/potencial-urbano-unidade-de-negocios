# PLANO H3 — O PRODUTO (lista de alvos por imóvel) · tudo preparado, 2026-06-24
> Orquestrador PU. Estágio E5 PROVADO localmente; só falta a carga dos dados pesados (passo do MOU).
> Régua D26: "armado ≠ destravado" — aqui o trilho está montado e provado ponta a ponta sobre dado REAL.

## O fluxo (da fonte ao alvo)
```
  Drive (pesados)            git (leve, já feito)              Engine (já ligado)        Produto
  ─────────────────          ──────────────────               ─────────────────         ───────
  IPTU_2026.csv  ─┐          tabelas/q14-valor-terreno.csv ─┐                          alvos-*.csv
  socios.csv     ─┼─rclone→  tabelas/quadro3-ca-por-zona.csv─┼─ v_feed_alvos (SQL JOIN) ─→ gerar_alvos.py ─→ lista
  LOTES/geo      ─┘ Supabase tabelas/quadro5-fator-social    ┘   (lote×Q14×Q3×IPTU)        (OODC + citação,    ranqueada
                   Storage                                                                 número no engine)   por oportunidade
```

## Estado: o que JÁ está pronto (provado, no git)
- **Combustível (tabelas/):** Q14 (6.715 V por SQ+Codlog), Quadro 3 (39 zonas CA_max), Q5 (Fs). `scripts/extrair_quadros.py`.
- **Engine ligado:** `engines/tdc/oodc.py` → `oodc_por_imovel(sql,codlog,zona,…)` roda sobre V/CA_max REAIS (auto-teste: SQ 001003/Codlog 038121 × ZEU = R$931.800).
- **Estágio E5 (saída):** `scripts/gerar_alvos.py` → lista ranqueada com OODC + citação. PROVADO em `evals/ground-truth/amostra-alvos.csv` → `alvos-amostra-alvos.csv` (6 imóveis reais; topo R$1,68M).
- **Schema Supabase pronto (DDL):** `supabase/migrations/20260624_0{10,20,30}_*.sql` (estrutura + carga das tabelas pequenas + view do JOIN). RO-23: estrutura sem dado.
- **Storage:** 3 buckets criados (`dados-produto`, `geo-tabelas`, `geo-shapefiles`).

## O que FALTA (passos do MOU / fora do chat) — em ordem
1. **Subir os pesados** → `scripts/transferir-pesados-drive-supabase.md` (rclone Drive→Storage). Manifesto: `inventario/PESADOS-PARA-SUPABASE.csv`.
2. **Aplicar as migrations** (Supabase CLI/dashboard, na ordem 010→020→030). 020 carrega Q14/Q3/Q5 do git; estrutura de IPTU/socios/lote criada vazia.
3. **Carregar IPTU_2026 + socios + LOTES/geo** do Storage para `dados.*`/`geo.lote` (COPY a partir do bucket; geom dos shapefiles SIRGAS via ogr2ogr/PostGIS). Aqui entra a ponte **lote→(SQ,Codlog,zona)**: o JOIN espacial `ST_Within(lote.geom, zona.geom)` resolve a zona; SQ/Codlog vêm do cadastro.
4. **Gerar o feed e rodar o produto:**
   ```
   \copy (select sql_mestre as sql, codlog, zona, area_adicional_m2 as area_adicional,
                 1.2 as fp, 1.0 as fs, dono, '' as endereco
          from tabelas.v_feed_alvos where area_adicional_m2 > 0) to 'feed-alvos.csv' csv header;
   python3 scripts/gerar_alvos.py --entrada feed-alvos.csv --saida lista-alvos.csv
   ```
   Saída = **lista de prospecção por imóvel** (oportunidade construtiva + valor OODC + dono + citação).

## Decisões/pontos abertos para o MOU
- **Fp/Fs por imóvel:** hoje o feed usa Fp=1,2 / Fs=1,0 fixos. O Fp real é por localização (quadro do PDE — falta ingerir, B-3) e o Fs por uso (Q5, já temos). Definir se entram no JOIN ou ficam por faixa até a revisão jurídica (B-10).
- **Área adicional:** a fórmula usa CA_utilizado = área construída/terreno (do IPTU). Validar contra caso real (Fase 3 do CODEX) antes de virar número de prospecção.
- **PII (socios):** D106 — risco aceito; mecanismo RLS deny-all no schema permanece.
