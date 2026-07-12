#!/usr/bin/env python3
"""
iptu.py — Motor determinístico do IPTU de São Paulo (Valor Venal × alíquota progressiva).

Fórmula (README deste diretório; construção liberada pelo dono em 2026-07-10 —
"finalizarmos as duas frentes, tdc e iptu"):

  VV = VV_terreno + VV_construção                       (Art. 17, Lei 10.235/1986)
    VV_terreno    = área × valor_m2(PGV) × fatores      (Art. 4º c/c Tabelas I/II/III)
    VV_construção = área_construída_bruta × valor_m2(Tabela VI, por subdivisão)
                    × fator_obsolescência(Tabela IV)    (Art. 11, redação Lei 15.889/2013)
  IPTU = VV × alíquota_base(uso)                        (Arts. 7º/8º/27, Lei 6.989/1966,
                                                         redação Lei 13.250/2001)
         + Σ [porção do VV em cada faixa × ajuste_pct]  (Arts. 7º-A/8º-A/28, Lei 6.989/1966;
                                                         faixas da Lei 15.889/2013, Arts. 3º/4º/5º)

Doutrina do projeto: número nasce NO ENGINE (1.3); toda constante é DADO extraído
verbatim em tabelas/*.csv com vintage (1.1); fail-closed — entrada ausente/ambígua
recusa com a pendência NOMEADA (nunca chuta).

PENDÊNCIAS DECLARADAS (v1, 2026-07-10):
  · PGV (Listagem de Valores por logradouro/codlog) NÃO ingerida → valor_m2_terreno é
    ENTRADA obrigatória de vv_terreno (Anexo III da Lei 15.889/2013 — dado pesado).
  · Tabela I (profundidade) não extraída (lookup longo) → fator é ENTRADA do chamador.
  · Tabela V (enquadramento tipo/padrão) não extraída → tipo/padrão são ENTRADA.
  · Faixas dos Arts. 3º/4º/5º da Lei 15.889/2013 em VALORES NOMINAIS DE 2013 — a
    atualização monetária anual (decreto) NÃO está aplicada; confronto com lançamento
    de exercício ≠ 2014 exige a tabela do exercício (vintage!).

Uso: python3 engines/iptu/iptu.py --demo   (auto-teste ancorado em valores da lei)
"""
import csv
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
TAB = RAIZ / "tabelas"
Q2 = Decimal("0.01")
CEM = Decimal("100")

LEI_CTM = "Lei Municipal SP nº 6.989/1966 (texto compilado)"
LEI_VV = "Lei Municipal SP nº 10.235/1986 (texto compilado)"
LEI_FAIXAS = "Lei Municipal SP nº 15.889/2013"
NOTA_VIGENCIA_FAIXAS = ("faixas em valores NOMINAIS da Lei 15.889/2013 (vigência 2013-11-05); "
                        "atualização monetária anual por decreto NÃO aplicada (tabela a ingerir)")


# ---------------------------------------------------------------------------
# parsing defensivo (mesma semântica do pcpt.py — BR vírgula decimal; rejeita
# ponto-milhar ambíguo)
# ---------------------------------------------------------------------------
def _d(x, campo):
    s = str(x).strip()
    if ',' in s:
        s2 = s.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(\.\d{3})+', s):
        raise ValueError(f"{campo} ambíguo (ponto como milhar sem vírgula): {x!r} — "
                         "use vírgula decimal ou ponto decimal sem milhar")
    else:
        s2 = s
    try:
        return Decimal(s2)
    except Exception:
        raise ValueError(f"{campo} inválido: {x!r}")


def _pos(d, campo):
    if d <= 0:
        raise ValueError(f"{campo} deve ser > 0 (recebido {d})")
    return d


# ---------------------------------------------------------------------------
# tabelas (dado extraído verbatim; o engine só LÊ — 1.1)
# ---------------------------------------------------------------------------
def _carrega_base():
    """uso → (pct, dispositivo, lei). Arts. 7º/8º/27 (redação 13.250/2001)."""
    out = {}
    with open(TAB / "iptu-aliquota-base.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["uso"]] = (Decimal(r["aliquota_pct"]), r["dispositivo"], r["lei"])
    if set(out) != {"residencial", "nao_residencial", "territorial"}:
        raise ValueError(f"iptu-aliquota-base.csv inválido: usos {sorted(out)}")
    return out


def _carrega_faixas():
    """uso → [(de, até|None, ajuste_pct, dispositivo)] ordenado; valida 5 faixas
    contíguas com a última aberta (desenho dos Arts. 3º/4º/5º da Lei 15.889/2013)."""
    porc = {}
    with open(TAB / "iptu-aliquotas-faixa.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            de = Decimal(r["faixa_de_brl"])
            ate = Decimal(r["faixa_ate_brl"]) if (r["faixa_ate_brl"] or "").strip() else None
            pct = Decimal(r["aliquota_pct"].replace("+", ""))
            porc.setdefault(r["uso"], []).append((de, ate, pct, r["dispositivo"]))
    for uso, fx in porc.items():
        fx.sort(key=lambda t: t[0])
        if len(fx) != 5 or fx[-1][1] is not None:
            raise ValueError(f"faixas de {uso}: esperadas 5 com última aberta (veio {len(fx)})")
        for a, b in zip(fx, fx[1:]):
            if a[1] is None or b[0] != a[1] + Q2:
                raise ValueError(f"faixas de {uso} não-contíguas em {a[1]} → {b[0]}")
    return porc


def _carrega_obsolescencia():
    """{idade: (fator_tipo12_ab, fator_demais)} — Tabela IV ANO A ANO (2 colunas), Lei 10.235/1986
    (redação Lei 11.152/1991; não alterada pela Lei 18.330/2025 — vigente para 2026)."""
    m = {}
    with open(TAB / "iptu-fator-obsolescencia.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not (r.get("idade") or "").strip():
                continue
            m[int(r["idade"])] = (Decimal(r["fator_tipo12_ab"]), Decimal(r["fator_demais"]))
    if len(m) != 61 or m[0] != (Decimal("1.00"), Decimal("1.00")) or m[60] != (Decimal("0.20"), Decimal("0.20")):
        raise ValueError("iptu-fator-obsolescencia.csv inválido: esperadas 61 idades (0..60), colunas "
                         "fator_tipo12_ab e fator_demais, de 1,00 (idade 0) a 0,20 (idade 60)")
    return m


def _carrega_tabela_vi():
    """(tipo, padrão) → {subdivisão: R$/m²} — Tabela VI (Anexo I da Lei 18.330/2025, exercício 2026;
    substitui a Tabela VI da Lei 10.235/1986). Valores reproduzem o lançamento oficial 2026 (eval-iptu-oficial)."""
    out = {}
    with open(TAB / "iptu-valor-construcao-m2.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[(str(r["tipo"]).strip(), r["padrao"].strip().upper())] = {
                "1a": Decimal(r["subdivisao_1a_brl"]),
                "2a": Decimal(r["subdivisao_2a_brl"]),
                "alem": Decimal(r["alem_2a_brl"]),
            }
    if not out:
        raise ValueError("iptu-valor-construcao-m2.csv vazio")
    return out


BASE = _carrega_base()
FAIXAS = _carrega_faixas()
OBSOLESCENCIA = _carrega_obsolescencia()
TABELA_VI = _carrega_tabela_vi()

USOS = sorted(BASE)


def uso_canonico(uso_iptu: str):
    """Mapeia o uso do lançamento IPTU_2026 ao vocabulário do engine (Art. 7º: 'exclusiva
    ou predominantemente como residência'). Determinístico e fail-closed: uso fora do
    mapa → ValueError (enquadrar é decisão jurídica, não chute)."""
    u = (uso_iptu or "").strip().lower()
    if not u:
        raise ValueError("uso vazio")
    if "terreno" in u:
        return "territorial"
    if "predominancia comercial" in u or "predominância comercial" in u:
        return "nao_residencial"
    # Art. 7º parágrafo único (incluído pela Lei 13.698/2003): vaga de garagem NÃO pertencente
    # a estacionamento comercial, em prédio exclusiva/predominantemente residencial = uso residencial.
    if "exclusivamente residencial" in u and "garagem" in u:
        return "residencial"
    if "predominancia residencial" in u or "predominância residencial" in u or u == "residencia" \
            or u == "residência" or u.startswith("residencia ") or u.startswith("residência ") \
            or "apartamento" in u or "cortiço" in u or "cortico" in u:
        # cortiço = habitação (residência coletiva) — enquadra no Art. 7º ("utilizados
        # exclusiva ou predominantemente como residência").
        return "residencial"
    if u in ("nao residencial", "não residencial") or any(t in u for t in (
            "loja", "comercial", "escritorio", "escritório", "industria",
            "indústria", "cinema, teatro", "uso especial", "armazem", "armazém",
            "armazens", "armazéns", "deposito", "depósito",
            "oficina", "posto", "hotel", "hospital", "escola", "templo",
            "clube", "estacionamento", "garagem nao residencial")):
        return "nao_residencial"
    raise ValueError(f"uso não mapeado: {uso_iptu!r} — enquadre explicitamente "
                     f"(vocabulário: {USOS})")


# ---------------------------------------------------------------------------
# IPTU devido — Arts. 7º/8º/27 (base) + 7º-A/8º-A/28 (ajuste por porção)
# ---------------------------------------------------------------------------
def iptu_devido(vv, uso):
    """Imposto = VV × alíquota_base(uso) + Σ(porção na faixa × ajuste da faixa).
    O ajuste é POR PORÇÃO (verbatim dos Arts. 7º-A/8º-A/28: 'calculados sobre a porção
    do valor venal compreendida em cada uma das faixas... total = soma') — o desenho é
    CONTÍNUO por construção (sem salto em fronteira de faixa)."""
    V = _pos(_d(vv, "vv"), "vv")
    if uso not in BASE:
        raise ValueError(f"uso inválido: {uso!r}; use {USOS}")
    pct_base, disp_base, _lei = BASE[uso]
    base = V * pct_base / CEM
    ajuste = Decimal("0")
    detalhe = []
    for de, ate, pct, disp in FAIXAS[uso]:
        if V < de:
            break
        topo = V if ate is None else min(V, ate)
        porcao = topo - de + (Q2 if de > 0 else Decimal("0"))
        if porcao <= 0:
            continue
        contrib = porcao * pct / CEM
        ajuste += contrib
        detalhe.append(f"[{de}–{ate if ate is not None else '∞'}]: {porcao} × {pct}% = {contrib.quantize(Q2)}")
    imposto = (base + ajuste).quantize(Q2, ROUND_HALF_UP)
    memoria = (f"IPTU = VV({V}) × {pct_base}% ({disp_base}) "
               f"{'+' if ajuste >= 0 else '−'} |Σ porções| ({abs(ajuste).quantize(Q2)}) = {imposto}")
    return {
        "imposto_brl": imposto,
        "vv": V,
        "uso": uso,
        "aliquota_base_pct": str(pct_base),
        "ajuste_brl": str(ajuste.quantize(Q2)),
        "faixas_detalhe": detalhe,
        "memoria_calculo": memoria,
        "citacao": {
            "dispositivo": f"{disp_base} c/c ajuste por porção (Arts. 7º-A/8º-A/28, Lei 6.989/1966; "
                           f"faixas: Arts. 3º/4º/5º, {LEI_FAIXAS})",
            "fonte": f"{LEI_CTM}; {LEI_FAIXAS}",
        },
        "nota_vigencia": NOTA_VIGENCIA_FAIXAS,
    }


# ---------------------------------------------------------------------------
# Valor venal — Lei 10.235/1986
# ---------------------------------------------------------------------------
def fator_obsolescencia(idade, tipo=None, padrao=None):
    """Tabela IV (ano a ano) c/c Art. 16 (idade = exercício − ano do término/ocupação).
    Duas colunas: Tipos 1 e 2 nos Padrões A/B usam a 1ª (deprecia mais rápido, piso 0,20 aos 40 anos);
    os demais Padrões/Tipos usam a 2ª (piso 0,20 aos 60). idade > 60 usa o fator da idade 60."""
    i = int(idade)
    if i < 0:
        raise ValueError(f"idade inválida: {idade!r}")
    ab, demais = OBSOLESCENCIA[min(i, 60)]
    usa_ab = str(tipo).strip() in ("1", "2") and str(padrao).strip().upper() in ("A", "B")
    return ab if usa_ab else demais


def vv_construcao(area_construida, tipo, padrao, subdivisao, idade=None, fator_obs=None):
    """Art. 11 (redação Lei 15.889/2013): área construída bruta × valor m² (Tabela VI,
    por subdivisão da zona urbana) × fator de obsolescência (Tabela IV).
    Informe `idade` (Art. 16) OU `fator_obs` explícito — sem nenhum, recusa (fail-closed)."""
    A = _pos(_d(area_construida, "area_construida"), "area_construida")
    chave = (str(tipo).strip(), str(padrao).strip().upper())
    if chave not in TABELA_VI:
        raise ValueError(f"(tipo, padrão) fora da Tabela VI: {chave} — enquadramento é a "
                         "Tabela V (não extraída; PENDÊNCIA declarada no cabeçalho)")
    sub = str(subdivisao).strip().lower()
    if sub not in ("1a", "2a", "alem"):
        raise ValueError(f"subdivisão inválida: {subdivisao!r}; use 1a | 2a | alem (Anexo II, {LEI_FAIXAS})")
    if fator_obs is None:
        if idade is None:
            raise ValueError("informe idade (Art. 16) ou fator_obs explícito — sem obsolescência não há VV de construção (Art. 11)")
        F = fator_obsolescencia(idade, tipo, padrao)
        origem_f = f"Tabela IV por idade={int(idade)} (Tipo {chave[0]}/Padrão {chave[1]})"
    else:
        F = _d(fator_obs, "fator_obs")
        if not (0 < F <= 1):
            raise ValueError(f"fator_obs fora de (0,1]: {F}")
        origem_f = "fator_obs informado pelo chamador"
    vm2 = TABELA_VI[chave][sub]
    vv = (A * vm2 * F).quantize(Q2, ROUND_HALF_UP)
    return {
        "vv_construcao_brl": vv,
        "valor_m2_brl": str(vm2),
        "fator_obsolescencia": str(F),
        "memoria_calculo": f"VVc = A({A}) × R${vm2}/m² (Tabela VI {chave[0]}-{chave[1]}, subdiv. {sub}) × {F} ({origem_f}) = {vv}",
        "citacao": {"dispositivo": "Art. 11 (fórmula, red. Lei 15.889/2013) c/c Tabela IV (obsolescência, "
                                   "Lei 11.152/1991) e Tabela VI (valores 2026, Anexo I Lei 18.330/2025); Art. 16",
                    "fonte": f"{LEI_VV}; {LEI_FAIXAS}; Lei 18.330/2025 (Tabela VI 2026)"},
    }


def vv_terreno(area, valor_m2_pgv, fator_profundidade="1", fator_esquina="1", fator_diverso="1", fracao_ideal=None):
    """Art. 4º: área × valor unitário do m² (Listagem de Valores/PGV) × fatores das
    Tabelas I/II/III. PGV NÃO ingerida → `valor_m2_pgv` é ENTRADA obrigatória e
    rastreável do chamador (pendência declarada). Condomínio: Art. 10 (fração ideal)."""
    A = _pos(_d(area, "area"), "area")
    V = _pos(_d(valor_m2_pgv, "valor_m2_pgv"), "valor_m2_pgv")
    fp = _d(fator_profundidade, "fator_profundidade")
    fe = _d(fator_esquina, "fator_esquina")
    fd = _d(fator_diverso, "fator_diverso")
    for nome, f in (("fator_profundidade", fp), ("fator_esquina", fe), ("fator_diverso", fd)):
        if not (0 < f <= 2):
            raise ValueError(f"{nome} fora de (0,2]: {f}")
    fi = _d(fracao_ideal, "fracao_ideal") if fracao_ideal is not None else Decimal("1")
    if not (0 < fi <= 1):
        raise ValueError(f"fracao_ideal fora de (0,1]: {fi}")
    vv = (A * V * fp * fe * fd * fi).quantize(Q2, ROUND_HALF_UP)
    return {
        "vv_terreno_brl": vv,
        "memoria_calculo": (f"VVt = A({A}) × R${V}/m² (PGV/Listagem — ENTRADA; Anexo III {LEI_FAIXAS}) "
                            f"× prof.{fp} × esq.{fe} × div.{fd}" + (f" × FI {fi}" if fi != 1 else "") + f" = {vv}"),
        "citacao": {"dispositivo": "Art. 4º c/c Tabelas I/II/III" + ("; Art. 10 (fração ideal)" if fi != 1 else ""),
                    "fonte": LEI_VV},
        "nota_pendencia": "PGV (Listagem de Valores por codlog) não ingerida — valor_m2_pgv é entrada do chamador",
    }


def valor_venal(vvt_brl, vvc_brl):
    """Art. 17: VV do imóvel construído = valor do terreno + valor da construção."""
    t = _d(vvt_brl, "vvt_brl"); c = _d(vvc_brl, "vvc_brl")
    if t < 0 or c < 0:
        raise ValueError("VV parcial negativo")
    vv = (t + c).quantize(Q2, ROUND_HALF_UP)
    return {"vv_brl": vv, "memoria_calculo": f"VV = VVt({t}) + VVc({c}) = {vv}",
            "citacao": {"dispositivo": "Art. 17", "fonte": LEI_VV}}


# ---------------------------------------------------------------------------
# demo — ANCORADO em valores derivados À MÃO da lei (falha = engine quebrado)
# ---------------------------------------------------------------------------
def _demo():
    ok = []

    def anc(nome, obtido, esperado):
        assert Decimal(str(obtido)) == Decimal(esperado), f"{nome}: {obtido} ≠ {esperado}"
        ok.append(f"  ✓ {nome}: {obtido}")

    # Residencial (Art. 7º 1,0% + Art. 7º-A):
    # VV 100.000 → 1.000 + 100.000×(−0,3%) = 700,00 (faixa 1 inteira)
    anc("resid VV=100.000", iptu_devido("100000", "residencial")["imposto_brl"], "700.00")
    # VV 400.000 → 4.000 + (150k×−0,3% + 150k×−0,1% + 100k×+0,1%) = 4.000 − 450 − 150 + 100 = 3.500,00
    anc("resid VV=400.000", iptu_devido("400000", "residencial")["imposto_brl"], "3500.00")
    # VV 1.500.000 → 15.000 + (−450 −150 +300 +1.800 + 300k×0,5%=1.500) = 18.000,00 (última faixa aberta)
    anc("resid VV=1.500.000", iptu_devido("1500000", "residencial")["imposto_brl"], "18000.00")
    # Não-residencial (Art. 8º 1,5% + Art. 8º-A): VV 100.000 → 1.500 − 400 = 1.100,00
    anc("ñ-resid VV=100.000", iptu_devido("100000", "nao_residencial")["imposto_brl"], "1100.00")
    # Territorial (Art. 27 1,5% + Art. 28): VV 1.000.000 → 15.000 + (−600 −300 + 0 + 800) = 14.900,00
    anc("territ VV=1.000.000", iptu_devido("1000000", "territorial")["imposto_brl"], "14900.00")
    # Continuidade na fronteira (desenho por porção): 150.000,00 × 150.000,01 diferem ≤ 1 centavo
    a = iptu_devido("150000.00", "residencial")["imposto_brl"]
    b = iptu_devido("150000.01", "residencial")["imposto_brl"]
    assert abs(a - b) <= Q2, f"salto na fronteira de faixa: {a} → {b}"
    ok.append(f"  ✓ continuidade na fronteira: {a} → {b}")

    # Construção (Art. 11 + Tabelas IV/VI): 100 m², tipo 1-A, 1ª subdiv., idade 3 → 100×920×1,00
    anc("VVc 1-A/1a idade=3", vv_construcao("100", 1, "A", "1a", idade=3)["vv_construcao_brl"], "267623.00")
    # idade 12 → fator 0,86 → 79.120,00
    anc("VVc 1-A/1a idade=12", vv_construcao("100", 1, "A", "1a", idade=12)["vv_construcao_brl"], "231756.00")
    # Terreno (Art. 4º): 500 m² × R$2.000 × prof. 0,7071 = 707.100,00
    anc("VVt 500×2000×0,7071", vv_terreno("500", "2000", fator_profundidade="0.7071")["vv_terreno_brl"], "707100.00")
    # Art. 17: soma
    anc("VV=VVt+VVc", valor_venal("707100.00", "79120.00")["vv_brl"], "786220.00")

    # Fail-closed:
    for nome, fn in [
        ("uso inválido", lambda: iptu_devido("1000", "rural")),
        ("vv ≤ 0", lambda: iptu_devido("0", "residencial")),
        ("construção sem obsolescência", lambda: vv_construcao("100", 1, "A", "1a")),
        ("tipo/padrão fora da Tabela VI", lambda: vv_construcao("100", 9, "Z", "1a", idade=1)),
        ("milhar ambíguo", lambda: iptu_devido("1.000", "residencial")),
        ("uso não mapeado", lambda: uso_canonico("chácara de lazer")),
    ]:
        try:
            fn()
        except ValueError:
            ok.append(f"  ✓ fail-closed: {nome} recusado")
        else:
            raise AssertionError(f"fail-closed FURADO: {nome} passou")

    print("iptu.py --demo (ancorado na lei):")
    print("\n".join(ok))
    print(f"  NOTA: {NOTA_VIGENCIA_FAIXAS}")
    return 0


if __name__ == "__main__":
    if "--demo" in sys.argv:
        sys.exit(_demo())
    print(__doc__)
