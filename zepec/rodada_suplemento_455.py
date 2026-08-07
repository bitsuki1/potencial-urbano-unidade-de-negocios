#!/usr/bin/env python3
"""
rodada_suplemento_455.py — RODADA-SUPLEMENTO do preço legal p/ os 455 SEM cadastro IPTU (triagem GeoSampa).

Contexto: o gerador oficial (`enriquecer_oficial.py`) deixou 455 cedentes sem Atc ("Atc: SQL sem
cadastro no IPTU"). A triagem geoespacial (`ferramenta/triagem_455_final.csv`, 2026-08-07) resolveu:
  RECUPERAVEL_COM_AREA (171)  -> área oficial do lote no GeoSampa (camada lote_cidadao) vira Atc
  DESCARTE_VEDADO_LEI (19) · DESCARTE_MORTE_CONFIRMADA_2PASSADAS (80) · DESCARTE_SQL_INVALIDO (64)
  INCONCLUSIVO_REPASSAR (121)

O que esta rodada faz sobre `ferramenta/zepec_cedentes_oficial.csv`:
  1. Acrescenta a coluna `estado_triagem` a TODAS as linhas (classe da triagem p/ os 455; 'carteira'
     p/ o resto). NADA é deletado (doutrina: nada se joga fora).
  2. Para os 171 RECUPERAVEL_COM_AREA: calcula PCpt/saldo/preço-proxy REUSANDO as funções do gerador
     (`_calcular_pcpt`/`_precificar` -> engine `engines/tdc/pcpt.py`; número nasce no engine, 1.3),
     com Atc = área GeoSampa (fonte alternativa OFICIAL primária, 1.8 — não é derivado nosso),
     gravada na coluna própria `area_terreno_m2_geosampa` (a `area_terreno_m2` segue sendo só-IPTU).
     V de outorga: SEM cadastro IPTU não há codlog da face fiscal — usa a MEDIANA das faces oficiais
     do SQ no Quadro 14/2026 (mesmo fallback declarado MAT-3 do gerador; v_q14_origem='mediana_sq').
     memoria_calculo prefixada com a marca da fonte; qualidade_estimativa='estimada-geosampa'
     (exceto JÁ-DECLARADO, que preserva a flag T3 'PENDENTE_FI_DECLARADO' — Art. 125 §1º I; a
     proveniência GeoSampa fica na memória/pendência).
  3. TRAVA INVIOLÁVEL: nenhuma linha que JÁ tinha preco_proxy_brl é alterada (verificação
     campo-a-campo ao final; falha ALTO se qualquer uma mudar).

Uso:  python3 zepec/rodada_suplemento_455.py
Lente-executora PU · 2026-08-07.
"""
import csv
import statistics
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from decimal import Decimal
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import enriquecer_oficial as GEN  # reusa _calcular_pcpt/_precificar/regime_pcpt (engine pcpt via GEN)

Q2 = Decimal("0.01")
MARCA = "Atc=área do lote GeoSampa (lote_cidadao) [suplemento 2026-08-07]"
CSV_OFICIAL = AQUI / "ferramenta" / "zepec_cedentes_oficial.csv"
CSV_TRIAGEM = AQUI / "ferramenta" / "triagem_455_final.csv"

COLS_NOVAS = ["estado_triagem", "area_terreno_m2_geosampa"]


def carregar():
    tri = list(csv.DictReader(open(CSV_TRIAGEM, encoding="utf-8")))
    tri_por_sql = {r["sql_mestre"]: r for r in tri if r["sql_mestre"].strip()}
    rows = list(csv.DictReader(open(CSV_OFICIAL, encoding="utf-8")))
    q14 = {(r["sq"], GEN.norm_codlog(r["codlog"])): r["valor_m2_brl"]
           for r in csv.DictReader(open(AQUI / "oficial/q14_cedentes_2026_oficial.csv", encoding="utf-8"))}
    q14_por_sq = defaultdict(list)
    for (sq, _cl), val in q14.items():
        q14_por_sq[sq].append(Decimal(val))
    q14_mediana = {sq: statistics.median(sorted(v)) for sq, v in q14_por_sq.items()}
    q14_max = {sq: max(v) for sq, v in q14_por_sq.items()}
    zona = {r["sql_mestre"]: r for r in csv.DictReader(open(AQUI / "oficial/zona_por_cedente.csv", encoding="utf-8"))}
    return tri_por_sql, rows, q14_mediana, q14_max, zona


def estado_da_linha(r, tri_por_sql):
    """Classe da triagem p/ a linha do CSV oficial. Universo dos 455 = linha SEM cobertura IPTU2026.
    As 68 linhas com sql_mestre VAZIO não têm chave: re-deriva a classe deterministicamente do mesmo
    critério da triagem (vedado por lei -> DESCARTE_VEDADO_LEI; senão DESCARTE_SQL_INVALIDO)."""
    cob = (r.get("cobertura_oficial") or "").split("+")
    if "IPTU2026" in cob:
        return "carteira"
    sql = (r.get("sql_mestre") or "").strip()
    if sql:
        t = tri_por_sql.get(sql)
        return t["classe_final"] if t else "carteira"
    if (r.get("motivo_negociavel") or "").strip().startswith("vedado por lei"):
        return "DESCARTE_VEDADO_LEI"
    return "DESCARTE_SQL_INVALIDO"


def suplementar(r, tri_r, q14_mediana, q14_max, zona, n):
    """Preenche PCpt/saldo/preço da linha RECUPERAVEL_COM_AREA via ENGINE, com Atc = área GeoSampa."""
    sql = r["sql_mestre"].strip()
    atc = str(Decimal(tri_r["area_m2_geosampa"]).quantize(Q2))  # 2 casas: formato inambíguo p/ o engine
    r["area_terreno_m2_geosampa"] = atc
    n["atc_geosampa"] += 1

    cob = [c for c in (r.get("cobertura_oficial") or "").split("+") if c]
    cob.append("GeoSampaArea")
    pend = ["IPTU: SQL sem cadastro no IPTU — Atc suprido pela área oficial do lote no GeoSampa "
            "(lote_cidadao; fonte alternativa oficial, suplemento 2026-08-07); venal/uso IPTU seguem ausentes"]

    # V de outorga (Quadro 14/2026): sem IPTU não há codlog da face fiscal -> MEDIANA das faces
    # oficiais do SQ (fallback declarado MAT-3 do gerador; todas as faces são Q14 oficial).
    sq6 = sql[:6]
    v = None
    if sq6 in q14_mediana:
        v = f"{q14_mediana[sq6]:.2f}"
        r["v_outorga_m2_q14"] = v
        r["v_q14_origem"] = "mediana_sq"
        cob.append("Q14~med")
        n["v_mediana"] += 1
        pend.append(f"V (Q14): sem cadastro IPTU -> sem codlog da face fiscal; usada a MEDIANA das "
                    f"faces oficiais do SQ {sq6} = R${v}/m² (v_q14_origem=mediana_sq — fallback declarado)")
        vmax = q14_max.get(sq6)
        if vmax is not None:
            r["v_outorga_max_q14"] = str(vmax)
            if Decimal(v) < vmax:
                n["multi_face"] += 1
                pend.append(f"Decreto 57.536/2016 Art. 3º IV: se lote tem frente p/ distintas faces, "
                            f"V=MAX(Q14)=R${vmax}/m² (face atual: R${v}/m²)")
    else:
        pend.append(f"V (Q14): SQ {sq6} sem face no Quadro 14/2026 — sem V, sem preço")

    cabas = GEN._num(r.get("ca_basico"))
    if not (r.get("zona") or "").strip():
        pend.append("Zona: lote sem sobreposição (sem SQL / lote / fora de zona)")
    elif not cabas:
        pend.append(f"CAbás: zona {r['zona']} sem CA no Quadro 3 (overlay — resolver zona-base)")

    vendido_bloqueado = (r.get("esgotado") or "").strip() == "sim" or (r.get("negociavel") or "").strip() == "nao"
    vedado_lei = (r.get("motivo_negociavel") or "").strip().startswith("vedado por lei")
    saldo = None
    if vedado_lei:
        pend.append("Art. 124 §2º: cessão VEDADA (AUE/APPa) — PCpt/saldo/preço não calculados "
                    "(potencial é intransferível; Lei 16.050/2014)")
        n["vedado"] += 1
    elif cabas:
        # FSCE (Art. 57, Lei 17.844/2022) — mesma régua do gerador: só na_aiu_sce=='1' liga; '?'/vazio
        # em BIR vira pendência declarada (fail-closed).
        z = zona.get(sql)
        bir = "BIR" in (r.get("tipo_zepec") or "")
        sce = ((z.get("na_aiu_sce") or "").strip() if z else "")
        saldo = GEN._calcular_pcpt(r, atc, cabas, pend, n, setor_central=(bir and sce == "1"))
        if bir and sce not in ("1", "0"):
            pend.append("FSCE (Art.57 Lei 17.844/2022): pertinência à AIU-SCE PENDENTE "
                        "(coleta GeoSampa) — PCpt calculado SEM FSCE")
        elif bir and sce == "1" and Decimal(atc) > Decimal("1000"):
            pend.append("Art. 57 Lei 17.844/2022: imóvel NA AIU-SCE porém terreno > 1.000 m² "
                        "— FSCE NÃO aplicável (teto do Art. 57); PCpt sem o fator")
        if saldo is not None and v:
            GEN._precificar(r, saldo, vendido_bloqueado, pend, n)

    # memória prefixada com a marca da fonte alternativa (1.7 — rastro da proveniência do Atc)
    if r.get("memoria_calculo"):
        r["memoria_calculo"] = f"{MARCA} | {r['memoria_calculo']}"

    # T3 — regime do PCpt: JÁ-DECLARADO preserva a flag PENDENTE_FI_DECLARADO (Art. 125 §1º I);
    # a marca 'estimada-geosampa' é só p/ prospecção nova (a proveniência GeoSampa fica na memória).
    reg, qual = GEN.regime_pcpt(r)
    r["regime_pcpt"] = reg
    if reg == "JA_DECLARADO":
        r["qualidade_estimativa"] = qual
        if r.get("pcpt_m2"):
            pend.append("PCpt do JÁ-DECLARADO governado pela Declaração (Art.125 §1º I); o escalonado é "
                        "ESTIMATIVA (Art.24 caput = NOVAS declarações), NÃO o valor declarado — Fi/PCpt da "
                        "Declaração ausente na base (PENDENTE). Confiável só p/ prospecção nova. "
                        "[Atc desta estimativa = GeoSampa, suplemento 2026-08-07]")
        n["ja_declarado"] += 1
    else:
        r["qualidade_estimativa"] = "estimada-geosampa"

    r["cobertura_oficial"] = "+".join(cob)
    r["pendencia_calculo"] = " | ".join(pend)
    return pend


def main():
    tri_por_sql, rows, q14_mediana, q14_max, zona, = carregar()
    campos = list(rows[0].keys()) + [c for c in COLS_NOVAS if c not in rows[0]]
    originais = deepcopy(rows)  # p/ a verificação da trava (a)

    n = Counter()
    pend_por_linha = {}
    for idx, r in enumerate(rows):
        for c in COLS_NOVAS:
            r.setdefault(c, "")
        est = estado_da_linha(r, tri_por_sql)
        r["estado_triagem"] = est
        n[f"estado:{est}"] += 1
        if est == "RECUPERAVEL_COM_AREA":
            if (r.get("preco_proxy_brl") or "").strip():
                raise AssertionError(f"TRAVA (a): linha {r['sql_mestre']} já tinha preço — suplemento não toca")
            pend_por_linha[idx] = suplementar(r, tri_por_sql[r["sql_mestre"].strip()], q14_mediana, q14_max, zona, n)

    # ── TRAVA (a): nenhuma linha que já tinha preco_proxy_brl mudou em NENHUMA coluna original ──
    mudadas = 0
    for antes, depois in zip(originais, rows):
        if (antes.get("preco_proxy_brl") or "").strip():
            for k in antes:
                if antes[k] != depois[k]:
                    mudadas += 1
                    print(f"VIOLAÇÃO trava (a): sql={antes['sql_mestre']} coluna={k}", file=sys.stderr)
    if mudadas:
        sys.exit(f"ABORTADO: {mudadas} alteração(ões) em linhas com preço pré-existente — nada gravado.")

    with open(CSV_OFICIAL, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ── placar ──
    recs = [r for r in rows if r["estado_triagem"] == "RECUPERAVEL_COM_AREA"]
    com_preco = [r for r in recs if (r.get("preco_proxy_brl") or "").strip()]
    soma = sum(Decimal(r["preco_proxy_brl"]) for r in com_preco)
    print(f"rodada_suplemento_455: {len(rows)} linhas -> {CSV_OFICIAL.name} (+colunas {COLS_NOVAS})")
    print("\nestado_triagem (todas as linhas):")
    for k in sorted(n):
        if k.startswith("estado:"):
            print(f"  {k[7:]:38}: {n[k]:5}")
    print(f"\nRECUPERAVEL_COM_AREA suplementados: {len(recs)}")
    print(f"  Atc GeoSampa aplicado    : {n['atc_geosampa']}")
    print(f"  V Q14 via mediana-SQ     : {n['v_mediana']}")
    print(f"  PCpt calculado (engine)  : {n['pcpt']}")
    print(f"  saldo líquido            : {n['saldo']}")
    print(f"  PREÇO-PROXY novo         : {n['preco']}")
    print(f"  soma dos preços novos    : R$ {soma:,.2f}")
    print(f"  já-declarado (T3 flag)   : {n['ja_declarado']}")
    sem_preco = [r for r in recs if not (r.get("preco_proxy_brl") or "").strip()]
    print(f"  ficaram SEM preço        : {len(sem_preco)}")
    motivos = Counter()
    for r in sem_preco:
        p = r["pendencia_calculo"]
        if "Zona: lote sem sobreposição" in p:
            motivos["sem zona -> sem CAbás"] += 1
        elif "sem CA no Quadro 3" in p:
            motivos["zona sem CAbás no Quadro 3"] += 1
        elif "sem face no Quadro 14" in p:
            motivos["SQ sem face no Q14"] += 1
        elif "já transferido > PCpt" in p:
            motivos["saldo zerado (transferido > PCpt) — REVISAR"] += 1
        elif "engine recusou" in p:
            motivos["engine recusou entrada"] += 1
        else:
            motivos["outro (ver pendencia_calculo)"] += 1
    for m, q in motivos.most_common():
        print(f"    - {m}: {q}")


if __name__ == "__main__":
    main()
