#!/usr/bin/env python3
"""
carregar_zonas_v5.py — consome o resultado da rodada v5 do hub e atualiza o SSOT das zonas.

Entrada : $HUB/tools/pu-geo/zonas_v5.csv
          (sql_mestre,x_utm23s,y_utm23s,origem_ponto,zona_v3,zona_18177,status)
Saída   : patch em zepec/oficial/zona_por_cedente.csv  (só com --aplicar)
          zepec/oficial/_pendencias_zona.csv regravado pelo gerar_alvos_zona_v5.py depois.

REGRA DE ENTRADA NO SSOT (fail-closed, 1.3/1.7):
  entra   -> status=ok_vigente_18177 E a zona tem CAbás no Quadro 3 (Lei 16.402/2016)
  NÃO entra -> status=so_v3_ainda      (camada ANTIGA 13.885/2004 — rótulo fora do Quadro 3)
               status=ponto_sem_zona   (nenhuma feição no ponto)
               status=sem_ponto_de_partida
               zona ZOE                (regime PRÓPRIO: CAbás vem do ato do perímetro, não do Q3)
               zona Praça/Canteiro     (bem público não-edificável)
               zona com CAbás 'NA' no Quadro 3
  Tudo que não entra fica declarado como pendência COM MOTIVO — nunca chutado.

Proveniência gravada no campo `fonte`:
  GeoSampa(Lei18177→<ZONA>)+Q3[ponto=<origem>]
  onde <origem> = centroide_lote_cidadao (centroide OFICIAL do lote) ou nominatim_v5 (endereço).

Uso:
  python3 zepec/pipeline/carregar_zonas_v5.py             # relatório (dry-run)
  python3 zepec/pipeline/carregar_zonas_v5.py --aplicar   # grava no SSOT
PU 23e · 2026-08-07.
"""
import argparse
import csv
import os
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(os.environ.get("PU_REPO", Path(__file__).resolve().parents[2]))
HUB = Path(os.environ.get("HUB", "/home/user/portfolio-automacoes"))

SSOT = RAIZ / "zepec/oficial/zona_por_cedente.csv"
QUADRO3 = RAIZ / "tabelas/quadro3-ca-por-zona.csv"
RESULTADO = HUB / "tools/pu-geo/zonas_v5.csv"

SEM_CA_POR_REGIME = {
    "ZOE": "ZOE tem regime PRÓPRIO — CAbás definido pelo ato/plano do perímetro, não pelo Quadro 3",
    "PRAÇA/CANTEIRO": "bem público não-edificável (praça/canteiro) — sem CAbás",
    "PRACA/CANTEIRO": "bem público não-edificável (praça/canteiro) — sem CAbás",
}


def quadro3():
    q3 = {}
    with open(QUADRO3, encoding="utf-8") as fh:
        linhas = [l for l in fh if not l.startswith("#")]
    for r in csv.DictReader(linhas):
        q3[r["zona"].strip().upper()] = r["ca_basico"].strip()
    return q3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()

    if not RESULTADO.exists():
        print(f"GATE: {RESULTADO} ainda não existe — rode o workflow `pu-zona-v5` do hub "
              f"(Actions -> pu-zona-v5 -> Run workflow) e traga o CSV.", file=sys.stderr)
        return 2

    q3 = quadro3()
    with open(RESULTADO, encoding="utf-8") as fh:
        res = list(csv.DictReader(fh))
    with open(SSOT, encoding="utf-8") as fh:
        rd = csv.reader(fh)
        header = next(rd)
        rows = [r for r in rd if r]
    idx = {r[0]: i for i, r in enumerate(rows)}
    ncol = len(header)

    entram, recusas = {}, []
    contradizidos = []   # ver CONTRADIÇÃO, abaixo
    for r in res:
        sql, z = r["sql_mestre"].strip(), r["zona_18177"].strip()

        def recusar(codigo, motivo):
            recusas.append((sql, codigo, motivo))
            # CONTRADIÇÃO (fail-closed, 1.6/1.8): a camada VIGENTE respondeu no centroide
            # OFICIAL do lote e disse que ali NÃO há CAbás — mas o SSOT ainda carrega um
            # CAbás herdado de fonte MAIS FRACA (rótulo da camada v3/2004 + fallback do
            # PDE Art.14§1). Fonte oficial mais nova e mais forte contradiz o valor antigo:
            # ele sai. Manter seria cotar preço legal de transferência para um lote que a
            # Lei 18.177/2024 classifica como praça/canteiro. Só sai o que é CONTRADITO:
            # quem a v5 não conseguiu ler (zona vazia) não é tocado — ausência de leitura
            # não é prova de nada.
            if r["status"] != "ok_vigente_18177" or not z:
                return
            velho = idx.get(sql)
            if velho is None:
                return
            fonte_velha = rows[velho][3]
            if "Lei18177" in fonte_velha:
                return
            contradizidos.append((sql, rows[velho][1], rows[velho][2], fonte_velha, z, motivo))

        if r["status"] != "ok_vigente_18177" or not z:
            recusar(r["status"], f"sem zona na camada vigente (v3='{r['zona_v3']}')")
            continue
        zu = z.upper()
        if zu in SEM_CA_POR_REGIME:
            recusar("zona_sem_ca_por_regime", SEM_CA_POR_REGIME[zu])
            continue
        ca = q3.get(zu)
        if ca is None:
            recusar("zona_fora_do_quadro3", f"zona '{z}' não consta no Quadro 3 da Lei 16.402/2016")
            continue
        if ca.upper() == "NA":
            recusar("cabas_NA_no_quadro3", f"zona '{z}' com CAbás 'NA' no Quadro 3")
            continue
        entram[sql] = (z, ca, f"GeoSampa(Lei18177→{z})+Q3[ponto={r['origem_ponto']}]")

    novos = [s for s in entram if s not in idx]
    atualiza = [s for s in entram if s in idx]

    print("=== CARGA v5 NO SSOT DE ZONA ===")
    print("linhas no resultado do hub:", len(res))
    print("aprovadas (camada vigente + Quadro 3):", len(entram),
          f"({len(novos)} novas, {len(atualiza)} substituem linha existente)")
    print("recusadas (pendência declarada):", len(recusas))
    for k, v in Counter(x[1] for x in recusas).most_common():
        print(f"  {k:26s}: {v}")
    print("zonas aprovadas:", Counter(v[0] for v in entram.values()).most_common())
    # AUTO-CONTRADIÇÃO (trava geral, auditoria 2026-08-08): linha do SSOT cuja PRÓPRIA zona é de
    # regime SEM CAbás (praça/canteiro, ZOE) mas que carrega ca_basico preenchido — o CAbás veio de
    # fallback (PDE Art.14§1) que a própria zona registrada contradiz. Não depende da coleta v5:
    # pega quem nunca foi alvo por já "ter" zona. Achado real: 0020520001 (Palácio das Indústrias)
    # cotava R$ 22,9 mi de preço legal com zona 'Praça/Canteiro' + CAbás 1.
    for i, r in enumerate(rows):
        sql = r[0]
        if sql in {c[0] for c in contradizidos} or sql in entram:
            continue
        zona_ssot = (r[1] or "").strip()
        ca_ssot = (r[2] or "").strip()
        if not ca_ssot or zona_ssot.upper() not in SEM_CA_POR_REGIME:
            continue
        contradizidos.append((sql, zona_ssot, ca_ssot, r[3],
                              zona_ssot, SEM_CA_POR_REGIME[zona_ssot.upper()] +
                              " (auto-contradição no próprio SSOT: zona sem CAbás com CAbás preenchido)"))

    if contradizidos:
        print(f"\nCONTRADITOS pela camada VIGENTE (saem do SSOT, fail-closed): {len(contradizidos)}")
        for sql, zv, cav, fv, znovo, motivo in contradizidos:
            print(f"  {sql} | SSOT tinha zona={zv} CAbás={cav} ({fv})")
            print(f"           camada vigente no centroide oficial diz '{znovo}' → {motivo}")

    if not args.aplicar:
        print("\n(dry-run — nada gravado. Rode com --aplicar.)")
        return 0

    for sql, (z, ca, fonte) in entram.items():
        if sql in idx:
            r = rows[idx[sql]]
            while len(r) < ncol:
                r.append("")
            r[1], r[2], r[3] = z, ca, fonte
        else:
            nova = [sql, z, ca, fonte] + [""] * (ncol - 4)
            rows.append(nova)
    fora = {c[0] for c in contradizidos}
    if fora:
        rows = [r for r in rows if r[0] not in fora]
    rows.sort(key=lambda r: r[0])
    with open(SSOT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"\nSSOT gravado: {len(rows)} linhas.")

    # TRILHA DOS CONTRADITOS (fail-closed, auditoria 2026-08-08): quem SAIU do SSOT precisa
    # aparecer no mapa de pendências. O gerador de alvos varre o resultado da v5 — logo, quem
    # nunca foi alvo da coleta (saiu por AUTO-contradição) sumiria em silêncio. Este arquivo é
    # a ponte: `gerar_alvos_zona_v5.py` o lê e declara cada um como pendência com o motivo.
    trilha = SSOT.parent / "_zona_contraditos.csv"
    with open(trilha, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sql_mestre", "zona_removida", "ca_removido", "fonte_removida",
                    "zona_vigente", "motivo"])
        w.writerows(sorted(contradizidos))
    print(f"trilha dos contraditos: {trilha.relative_to(RAIZ)} ({len(contradizidos)} linhas)")
    print("PRÓXIMO: python3 zepec/enriquecer_oficial.py && python3 zepec/funil.py && "
          "python3 evals/eval-zona-mutacao.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
