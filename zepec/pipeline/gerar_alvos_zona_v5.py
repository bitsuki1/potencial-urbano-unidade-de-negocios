#!/usr/bin/env python3
"""
gerar_alvos_zona_v5.py — monta o INSUMO da rodada v5 de resolução de ZONA (camada vigente
Lei 18.177/2024) para TODOS os cedentes cuja zona ainda não está provada.

MUDANÇA DE MÉTODO (o achado que destrava as 3 lacunas):
  a rodada v4 (`pu-geo-474`) partia do ENDEREÇO -> Nominatim/OSM -> ponto. Isso produziu:
    · 31 sem_hit (o Nominatim não achou o logradouro abreviado do IPTU);
    · 11 ponto_sem_zona (4 deles geocodificados em OUTRA CIDADE — Iguape, Guarujá, Catanduva…);
    · 105 "só-v3" (o ponto caiu no EIXO DA VIA; a camada v3/2004 é de perímetro e cobre a via,
      a camada 18177/2024 é de polígono de zona e ali não tem feição -> voltou vazio).
  DEPOIS daquela rodada o repo ganhou `zepec/oficial/centroides_cedentes.csv`: o CENTROIDE
  OFICIAL do lote (camada `geoportal:lote_cidadao`, EPSG 31983, coleta por QUADRA). Ele existe
  para 298 dos 474 — inclusive para 102 dos 105 "só-v3", 29 dos 31 "sem_hit" e 9 dos 11
  "ponto_sem_zona". Um ponto DENTRO do lote não cai na via nem em outra cidade.

REGRA DE PONTO (proveniência declarada, 1.3/1.7):
  1) centroide OFICIAL do lote  -> origem_ponto=centroide_lote_cidadao  (preferencial)
  2) endereço do IPTU 2026      -> origem_ponto=endereco_iptu2026       (o runner geocodifica)
  3) sem os dois                -> origem_ponto=SEM_PONTO               (bloqueio declarado)
Nada é preenchido por vizinhança/quadra: sem fonte, fica PENDENTE.

Entra na fila v5 quem, no SSOT `zona_por_cedente.csv`, está:
  (A) AUSENTE e é um dos 474 alvos da geocodificação (as 3 lacunas);
  (B) REPROVADO pela auditoria de proveniência (auditar_zona_geocodificada.py);
  (C) com `zona` = SELO ZEPEC (ZEPEC_APC/AUE/BIR…): ZEPEC é categoria de PROTEÇÃO, não zona
      de uso — não tem CA no Quadro 3; falta a zona de uso SUBJACENTE;
  (D) com `fonte` da camada ANTIGA v3 (Lei 13.885/2004): rótulo fora do Quadro 3 da LPUOS.

Saídas:
  $HUB/tools/pu-geo/alvos_zona_v5.csv        (insumo do workflow `pu-zona-v5` do hub)
  zepec/oficial/_pendencias_zona.csv         (mapa das pendências, com motivo, no repo do PU)

Uso: python3 zepec/pipeline/gerar_alvos_zona_v5.py
PU 23e · 2026-08-07.
"""
import csv
import os
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(os.environ.get("PU_REPO", Path(__file__).resolve().parents[2]))
HUB = Path(os.environ.get("HUB", "/home/user/portfolio-automacoes"))

SSOT = RAIZ / "zepec/oficial/zona_por_cedente.csv"
CENTROIDES = RAIZ / "zepec/oficial/centroides_cedentes.csv"
IPTU = RAIZ / "zepec/oficial/iptu2026_cedentes.csv"
GEOCODE = HUB / "tools/pu-geo/geocode_474.csv"
AUDIT = RAIZ / "zepec/oficial/_auditoria_zona_geocodificada.csv"

OUT_HUB = HUB / "tools/pu-geo/alvos_zona_v5.csv"
OUT_PU = RAIZ / "zepec/oficial/_pendencias_zona.csv"


def ler(p):
    if not p.exists():
        return []
    with open(p, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    ssot = {r["sql_mestre"]: r for r in ler(SSOT)}
    cen = {r["sql_mestre"]: r for r in ler(CENTROIDES)}
    ipt = {r["sql_mestre"]: r for r in ler(IPTU)}
    geo = {r["sql_mestre"]: r for r in ler(GEOCODE)}
    audit = ler(AUDIT)
    if not geo:
        print(f"AVISO: {GEOCODE} ausente — a lacuna (A) não entra na fila.", file=sys.stderr)

    alvos = {}   # sql -> (lacuna, motivo)

    def add(sql, lacuna, motivo):
        alvos.setdefault(sql, (lacuna, motivo))

    # (B) reprovados da auditoria de proveniência (primeiro: o motivo é mais específico
    #     que o "ausente do SSOT" de (A), já que a auditoria os REMOVEU do SSOT)
    for a in audit:
        if a["veredito"] == "REPROVADO":
            add(a["sql_mestre"], "B_proveniencia_reprovada", a["motivo"])

    # (A) os 474 da geocodificação que NÃO entraram no SSOT
    for sql, g in geo.items():
        if sql in ssot:
            continue
        st = g["status"]
        if st == "sem_hit_nominatim":
            tem_lote = bool(cen.get(sql, {}).get("x"))
            add(sql, "A3_sem_hit_nominatim",
                "endereço do IPTU não resolvido no Nominatim/OSM; lote "
                + ("EXISTE no lote_cidadao (usar centroide oficial)" if tem_lote
                   else "AUSENTE do lote_cidadao (sem geometria oficial)"))
        elif st == "ponto_sem_zona":
            add(sql, "A2_ponto_sem_zona",
                "ponto geocodificado não interseccionou NENHUMA camada de zoneamento "
                "(vários fora do município de São Paulo)")
        elif g["zona_v3"] and not g["zona_18177"]:
            add(sql, "A1_so_v3",
                f"zona só na camada ANTIGA v3/2004 ({g['zona_v3']}); camada vigente "
                "Lei 18.177/2024 sem feição no ponto (ponto no eixo da via)")
        else:
            add(sql, "A4_descartado",
                f"resolvido como '{g['zona_18177']}' mas não carregado no SSOT (sem CA no Quadro 3)")

    # (C) selo ZEPEC ocupando o lugar da zona de uso
    for sql, r in ssot.items():
        if r["zona"].strip().upper().startswith("ZEPEC"):
            add(sql, "C_selo_zepec_sem_zona_de_uso",
                f"'{r['zona']}' é SELO de proteção (ZEPEC), não zona de uso — sem CA no Quadro 3; "
                f"CA atual={r['ca_basico']} vem do fallback PDE Art.14§1, não do zoneamento")

    # (D) rótulo da camada antiga v3 no SSOT
    for sql, r in ssot.items():
        if "v3" in r["fonte"]:
            add(sql, "D_rotulo_v3_no_ssot",
                f"zona '{r['zona']}' é rótulo da LPUOS ANTIGA (Lei 13.885/2004), fora do Quadro 3 "
                f"da Lei 16.402/2016; fonte='{r['fonte']}'")

    # resolve o ponto de cada alvo
    linhas = []
    for sql in sorted(alvos):
        lacuna, motivo = alvos[sql]
        c = cen.get(sql, {})
        end = (ipt.get(sql, {}).get("endereco") or geo.get(sql, {}).get("endereco") or "").strip()
        if c.get("x") and c.get("y"):
            origem, x, y = "centroide_lote_cidadao", c["x"], c["y"]
        elif end:
            origem, x, y = "endereco_iptu2026", "", ""
        else:
            origem, x, y = "SEM_PONTO", "", ""
        linhas.append([sql, x, y, origem, end, lacuna, motivo])

    OUT_HUB.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_HUB, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sql_mestre", "x_utm23s", "y_utm23s", "origem_ponto", "endereco"])
        w.writerows([l[:5] for l in linhas])

    with open(OUT_PU, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sql_mestre", "x_utm23s", "y_utm23s", "origem_ponto", "endereco", "lacuna", "motivo"])
        w.writerows(linhas)

    print("=== FILA v5 DE RESOLUÇÃO DE ZONA (Lei 18.177/2024) ===")
    print("alvos:", len(linhas))
    for k, v in sorted(Counter(l[5] for l in linhas).items()):
        print(f"  {k:32s}: {v}")
    print("ponto de partida:")
    for k, v in sorted(Counter(l[3] for l in linhas).items()):
        print(f"  {k:26s}: {v}")
    bloq = [l for l in linhas if l[3] == "SEM_PONTO"]
    if bloq:
        print("BLOQUEADOS (sem centroide oficial E sem endereço — não entram em coleta):")
        for l in bloq:
            print(f"  {l[0]} | {l[5]}")
    print(f"insumo do hub: {OUT_HUB}")
    print(f"mapa no PU:    {OUT_PU.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
