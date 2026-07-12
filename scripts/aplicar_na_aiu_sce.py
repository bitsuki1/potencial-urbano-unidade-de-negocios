#!/usr/bin/env python3
"""
aplicar_na_aiu_sce.py — aplica a coluna `na_aiu_sce` ('1'/'0' do overlay do perímetro
AIU-SCE, GeoSampa) aos CSVs oficiais do PU, de forma CIRÚRGICA:

  · SÓ a coluna na_aiu_sce (zona/CAbás NÃO são tocados — o guard anti-clobber do probe
    existe exatamente p/ proteger a zona; aqui honramos a mesma doutrina).
  · SÓ linhas com status=ok e na_aiu_sce ∈ {0,1} (sem_lote/'?' ficam de fora — em runs
    parciais o throttle derruba lotes REAIS como 'sem_lote'; não é dado, é falha).
  · Idempotente; imprime contagens; falha se a fonte não tiver a coluna.

Fonte default: zepec/oficial/geosampa_sce_run29105687326.csv (CSV de 5 colunas extraído
MECANICAMENTE do log do run 29105687326 do workflow geosampa-siszon do hub — o probe
varreu 377 alvos com taxa 0,81 e, pelo guard <0,90, imprimiu o CSV no log sem gravar).

Alvos:
  zepec/oficial/zona_base_cedente.csv  (col na_aiu_sce)
  zepec/oficial/zona_por_cedente.csv   (col na_aiu_sce — criada se ausente; é a que o
                                        enriquecer_oficial.py consome p/ ligar o FSCE)

Uso: python3 scripts/aplicar_na_aiu_sce.py [fonte.csv]
PU 18 · 2026-07-10 — ativação do FSCE (Art. 57, Lei 17.844/2022) no pipeline.
"""
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "zepec/oficial/geosampa_sce_run29105687326.csv"
ZBASE = RAIZ / "zepec/oficial/zona_base_cedente.csv"
ZPC = RAIZ / "zepec/oficial/zona_por_cedente.csv"


def carregar_fonte():
    with open(FONTE, encoding="utf-8") as f:
        rd = csv.DictReader(f)
        if "na_aiu_sce" not in rd.fieldnames or "status" not in rd.fieldnames:
            raise SystemExit(f"FALHA: {FONTE.name} sem colunas na_aiu_sce/status — fonte errada")
        sce = {}
        for r in rd:
            if r["status"].strip() == "ok" and r["na_aiu_sce"].strip() in ("0", "1"):
                sce[r["sql_mestre"].strip()] = r["na_aiu_sce"].strip()
    if not sce:
        raise SystemExit("FALHA: fonte sem nenhuma linha ok com na_aiu_sce 0/1")
    return sce


def aplicar(path, sce):
    with open(path, encoding="utf-8", newline="") as f:
        rd = csv.reader(f)
        header = next(rd)
        rows = list(rd)
    if "na_aiu_sce" not in header:
        header = header + ["na_aiu_sce"]
    icol = header.index("na_aiu_sce")
    isql = header.index("sql_mestre")
    aplicados = ja_tinha = 0
    out = []
    for r in rows:
        r = r + [""] * (len(header) - len(r))
        sql = r[isql].strip()
        if sql in sce:
            if r[icol] == sce[sql]:
                ja_tinha += 1
            else:
                r[icol] = sce[sql]
                aplicados += 1
        out.append(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(out)
    return aplicados, ja_tinha, len(out)


def main():
    sce = carregar_fonte()
    uns = sum(1 for v in sce.values() if v == "1")
    print(f"fonte {FONTE.name}: {len(sce)} SQLs ok com na_aiu_sce (1={uns}, 0={len(sce)-uns})")
    for alvo in (ZBASE, ZPC):
        ap, ja, tot = aplicar(alvo, sce)
        print(f"  {alvo.name}: {ap} aplicados, {ja} já tinham, {tot} linhas")


if __name__ == "__main__":
    main()
