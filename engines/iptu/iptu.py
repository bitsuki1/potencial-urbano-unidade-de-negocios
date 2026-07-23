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
    série de atualização monetária anual (decreto) já está INGERIDA em
    tabelas/iptu-atualizacao-anual.csv (helper fator_atualizacao_iptu, 2013→2026,
    verificada na fonte oficial). NÃO é aplicada automaticamente às faixas: o fator
    reseta a cada revisão de PGV (2015/2018/2022/2026, valores absolutos nos anexos) e
    é questão jurídica aberta se o adicional é corrigido por decreto — o engine expõe o
    fator, mas não presume onde aplicá-lo (1.3, fail-closed).

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
                        "série de atualização anual por decreto DISPONÍVEL em tabelas/iptu-atualizacao-anual.csv "
                        "(fator_atualizacao_iptu), reseta a cada revisão de PGV — NÃO aplicada por padrão às "
                        "faixas do adicional (questão jurídica aberta; 1.3 não presume)")


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


def _carrega_isencao():
    """Faixas de ISENÇÃO do Imposto Predial por vintage (Art. 2º das leis de PGV):
    (vigencia_de:int) → (limite_total, limite_residencial_abc, lei, dispositivo). O número
    NASCE aqui, verbatim da lei (1.3): 2022 = Lei 17.719/2021 (120k/230k); 2026 = Lei 18.330/2025
    (150k/260k). Ordenado por ano; a consulta usa a vintage vigente na data do fato gerador (1.6)."""
    out = []
    with open(TAB / "iptu-isencao-faixa.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append((int(r["vigencia_de"]), Decimal(r["limite_isencao_total_brl"]),
                        Decimal(r["limite_residencial_abc_brl"]), r["lei"], r["dispositivo"]))
    out.sort(key=lambda x: x[0])
    if not out:
        raise ValueError("iptu-isencao-faixa.csv vazio")
    return out


def _carrega_atualizacao_anual(path=None):
    """Série ANUAL de atualização do IPTU (tabelas/iptu-atualizacao-anual.csv) — DADO extraído por decreto,
    verbatim da fonte oficial (1.3/1.7/1.8). Devolve (linhas, completa_ate):
      linhas = [(ano:int, tipo:str, fator_acum_regime:Decimal|None, regime_base:int, norma:str, disp:str)]
               ordenado por ano; fator_acum_regime = None em revisao_lei (valores absolutos nos anexos).
      completa_ate = último exercício VERIFICADO (diretiva '# COMPLETA_ATE: AAAA') — o fator falha-fechado
                     para ano > completa_ate. Fail-closed se o arquivo sumir/vazio (o motor lê, não inventa)."""
    p = Path(path) if path else (TAB / "iptu-atualizacao-anual.csv")
    if not p.exists():
        raise FileNotFoundError(f"série de atualização anual do IPTU ausente: {p} "
                                "(o engine lê o fator vigente da tabela, não o inventa)")
    completa_ate = None
    for raw in p.read_text(encoding="utf-8").splitlines():
        m = re.search(r"COMPLETA_ATE:\s*(\d{4})", raw)
        if raw.lstrip().startswith("#") and m:
            completa_ate = int(m.group(1))
    linhas = []
    with open(p, encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0].lstrip().startswith("#") or row[0].strip() == "ano_ref":
                continue
            ano = int(row[0].strip())
            tipo = row[1].strip()
            acum = Decimal(row[4].strip()) if (row[4] or "").strip() else None
            acum = None if tipo == "revisao_lei" else acum
            regime = int(row[5].strip())
            linhas.append((ano, tipo, acum, regime, row[6].strip(), row[8].strip()))
    if not linhas:
        raise ValueError(f"série de atualização anual do IPTU vazia: {p}")
    if completa_ate is None:
        raise ValueError(f"série de atualização anual do IPTU sem diretiva '# COMPLETA_ATE:' — {p}")
    return sorted(linhas, key=lambda x: x[0]), completa_ate


BASE = _carrega_base()
FAIXAS = _carrega_faixas()
OBSOLESCENCIA = _carrega_obsolescencia()
TABELA_VI = _carrega_tabela_vi()
ISENCAO = _carrega_isencao()
ATUALIZACAO, ATUALIZACAO_COMPLETA_ATE = _carrega_atualizacao_anual()

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


def _isencao_vigente(ano_ref):
    """Vintage da isenção vigente na data do fato gerador (1.6): a última cujo vigencia_de ≤ ano_ref.
    ano_ref None → a mais recente. Fato gerador anterior à 1ª vintage (2022) → sem regra de isenção
    conhecida no engine (fail-closed: devolve None, o chamador NÃO presume isenção)."""
    if ano_ref is None:
        return ISENCAO[-1]
    aplicaveis = [x for x in ISENCAO if x[0] <= int(ano_ref)]
    return aplicaveis[-1] if aplicaveis else None


def isencao_iptu(vv, ano_ref=None, residencial_abc=False):
    """Isenção do Imposto Predial (Art. 2º das leis de PGV) — número da lei, rastreável (1.3/1.7).
    Regra verbatim: (I) isento se VV ≤ limite_total (qualquer uso construído); (II) isento se
    residência de padrões A/B/C (tipos 1/2 da Tabela V) e VV ≤ limite_residencial. `residencial_abc`
    sinaliza o enquadramento do inciso II (decisão jurídica do lançamento, não chute do engine).
    Fail-closed: sem vintage aplicável → não presume isenção (isento=False, motivo explícito)."""
    V = _pos(_d(vv, "vv"), "vv")
    vig = _isencao_vigente(ano_ref)
    if vig is None:
        return {"isento": False, "motivo": f"sem faixa de isenção conhecida para ano_ref={ano_ref} "
                f"(1ª vintage = {ISENCAO[0][0]})", "citacao": None}
    ano_v, lim_total, lim_resid, lei, disp = vig
    if V <= lim_total:
        base = f"VV {V} ≤ R$ {lim_total} (limite de isenção total)"
        isento, inc = True, "I"
    elif residencial_abc and V <= lim_resid:
        base = f"VV {V} ≤ R$ {lim_resid} (residência A/B/C tipos 1/2)"
        isento, inc = True, "II"
    else:
        base = (f"VV {V} acima do limite ({lim_total} total"
                + (f"; {lim_resid} residencial A/B/C" if residencial_abc else "") + ")")
        isento, inc = False, None
    return {
        "isento": isento,
        "motivo": ("ISENTO — " if isento else "NÃO isento — ") + base,
        "vintage": ano_v,
        "citacao": {"dispositivo": f"{disp}" + (f", inciso {inc}" if inc else ""), "fonte": lei},
    }


def fator_atualizacao_iptu(ano_ref=None, serie=None):
    """Fator de atualização monetária do IPTU vigente no exercício `ano_ref`, lido de
    tabelas/iptu-atualizacao-anual.csv (número NASCE do decreto, não do LLM — 1.3/1.7/1.8).

    Semântica HONESTA (a mecânica de SP, ver o cabeçalho do CSV): o fator é ACUMULADO DENTRO de um
    regime de PGV e RESETA a cada revisão por LEI (que substitui a tabela por valores absolutos nos
    anexos). Por isso devolve, além do fator, o `regime_base_ano` — o fator só multiplica um valor
    expresso NA BASE daquele regime; não existe fator contínuo cruzando leis de PGV.

    Fail-closed (nunca chuta):
      · ano_ref > COMPLETA_ATE (série ainda não verificada além dali) → ValueError com a pendência nomeada.
      · ano_ref anterior à 1ª linha → ValueError.
      · se o exercício pedido cai em ano de revisão por LEI (ou o regime vigente começa numa lei cujos
        anexos ainda não extraímos), devolve fator=1,0 COM `nota` explícita de que os valores absolutos
        vêm do anexo da lei (não aplicar como % sobre nominal antigo).

    ano_ref None ⇒ vintage MAIS RECENTE verificada. Devolve dict: {fator, regime_base_ano, tipo, norma,
    dispositivo, ano_ref, nota}."""
    linhas, completa_ate = serie if serie is not None else (ATUALIZACAO, ATUALIZACAO_COMPLETA_ATE)
    alvo = completa_ate if ano_ref is None else int(ano_ref)
    if alvo > completa_ate:
        raise ValueError(f"atualização IPTU não verificada para exercício {alvo} "
                         f"(série completa só até {completa_ate}; ingerir o decreto do ano na fonte oficial — "
                         "1.8: não se interpola/estima percentual)")
    if alvo < linhas[0][0]:
        raise ValueError(f"atualização IPTU inexistente para exercício {alvo} "
                         f"(1ª linha da série = {linhas[0][0]})")
    escolhido = linhas[0]
    for ln in linhas:
        if ln[0] <= alvo:
            escolhido = ln
        else:
            break
    ano, tipo, acum, regime, norma, disp = escolhido
    fator = acum if acum is not None else Decimal("1.00")
    nota = ""
    if acum is None:  # o exercício vigente é o próprio ano de revisão por LEI
        nota = (f"exercício {alvo} é de revisão por LEI ({norma}) — valores ABSOLUTOS nos anexos "
                "(Tabela VI + Listagem de terreno); não aplicar como % sobre nominal anterior. "
                "Anexos ainda não extraídos linha a linha (pendência nomeada).")
    return {
        "fator": str(fator),
        "regime_base_ano": regime,
        "tipo": tipo,
        "norma": norma,
        "ano_ref": ("mais recente" if ano_ref is None else str(alvo)),
        "citacao": {"dispositivo": disp, "fonte": "tabelas/iptu-atualizacao-anual.csv"},
        "nota": nota,
        "memoria_calculo": f"atualização IPTU exercício {alvo}: fator {fator} (regime base {regime}, {norma})",
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

    def anc_eq(nome, obtido, esperado):
        assert str(obtido) == str(esperado), f"{nome}: {obtido} ≠ {esperado}"
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

    # ISENÇÃO do Imposto Predial (Art. 2º) — ancorado verbatim nas leis de PGV, por vintage (1.3/1.6):
    # 2026 (Lei 18.330/2025): isento total ≤ 150.000; residencial A/B/C ≤ 260.000.
    anc_eq("isenç 2026 VV=150.000 (I)", isencao_iptu("150000", 2026)["isento"], "True")
    anc_eq("isenç 2026 VV=150.000,01 ñ-resid (não)", isencao_iptu("150000.01", 2026)["isento"], "False")
    anc_eq("isenç 2026 VV=260.000 resid A/B/C (II)", isencao_iptu("260000", 2026, residencial_abc=True)["isento"], "True")
    anc_eq("isenç 2026 VV=260.000,01 resid (não)", isencao_iptu("260000.01", 2026, residencial_abc=True)["isento"], "False")
    # 2022 (Lei 17.719/2021): isento total ≤ 120.000; residencial A/B/C ≤ 230.000.
    anc_eq("isenç 2022 VV=120.000 (I)", isencao_iptu("120000", 2022)["isento"], "True")
    anc_eq("isenç 2022 VV=230.000 resid A/B/C (II)", isencao_iptu("230000", 2022, residencial_abc=True)["isento"], "True")
    anc_eq("isenç 2022 VV=230.000,01 resid (não)", isencao_iptu("230000.01", 2022, residencial_abc=True)["isento"], "False")
    # vintage: 2025 ainda usa a faixa de 2022 (a de 2026 só vale no exercício 2026)
    anc_eq("isenç 2025 usa vintage 2022", isencao_iptu("150000", 2025)["citacao"]["fonte"], "Lei nº 17.719/2021")
    anc_eq("isenç 2026 usa vintage 2026", isencao_iptu("150000", 2026)["citacao"]["fonte"], "Lei nº 18.330/2025")

    # ATUALIZAÇÃO ANUAL (série de decretos, tabelas/iptu-atualizacao-anual.csv) — número nasce do decreto (1.3):
    # fator acumulado DENTRO do regime, resetando a cada lei de PGV (2015/2018/2022/2026).
    anc_eq("atualiz 2017 (regime 2015: 1,095×1,06)", fator_atualizacao_iptu(2017)["fator"], "1.1607")
    anc_eq("atualiz 2017 regime_base", fator_atualizacao_iptu(2017)["regime_base_ano"], "2015")
    anc_eq("atualiz 2020 (regime 2018: 1,035²)", fator_atualizacao_iptu(2020)["fator"], "1.071225")
    anc_eq("atualiz 2021 herda 2020 (0% pandemia)", fator_atualizacao_iptu(2021)["fator"], "1.071225")
    anc_eq("atualiz 2025 (regime 2022: 1,055×1,043×1,046)", fator_atualizacao_iptu(2025)["fator"], "1.15098179")
    anc_eq("atualiz 2025 regime_base", fator_atualizacao_iptu(2025)["regime_base_ano"], "2022")
    # revisão por LEI: fator 1,0 + nota nomeada (valores absolutos no anexo, não % sobre nominal antigo)
    anc_eq("atualiz 2026 é revisão-lei (fator 1,0)", fator_atualizacao_iptu(2026)["fator"], "1.00")
    assert fator_atualizacao_iptu(2026)["tipo"] == "revisao_lei" and fator_atualizacao_iptu(2026)["nota"], \
        "2026 deveria ser revisao_lei com nota"
    ok.append("  ✓ atualiz 2026: revisão por LEI (Lei 18.330/2025) com nota de anexo")
    # ano entre regimes herda o do último exercício verificado do regime; 2013 = base nominal (fator 1,0)
    anc_eq("atualiz 2013 base nominal", fator_atualizacao_iptu(2013)["fator"], "1.00")

    # Fail-closed:
    for nome, fn in [
        ("uso inválido", lambda: iptu_devido("1000", "rural")),
        ("vv ≤ 0", lambda: iptu_devido("0", "residencial")),
        ("construção sem obsolescência", lambda: vv_construcao("100", 1, "A", "1a")),
        ("tipo/padrão fora da Tabela VI", lambda: vv_construcao("100", 9, "Z", "1a", idade=1)),
        ("milhar ambíguo", lambda: iptu_devido("1.000", "residencial")),
        ("uso não mapeado", lambda: uso_canonico("chácara de lazer")),
        ("atualização além do verificado", lambda: fator_atualizacao_iptu(ATUALIZACAO_COMPLETA_ATE + 1)),
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
