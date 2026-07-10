#!/usr/bin/env python3
"""
oodc.py — Engine determinístico de OUTORGA ONEROSA (OODC) e POTENCIAL CONSTRUTIVO (TDC).

Resolve o achado AUD-08/DP-2 da auditoria profunda: as fórmulas de TDC/OODC existiam só como
PROSA (`.md`/`.json` em engines/tdc/), então qualquer cálculo nasceria no LLM — proibido por 1.3
("número nasce no engine, nunca no LLM"). Aqui elas viram CÓDIGO puro, determinístico, rastreável.

Princípios:
- 1.3 — todo número sai daqui, com memória de cálculo e citação do dispositivo/quadro de origem.
- 1.7 — cada resultado carrega `citacao` (fonte legal); engine não "acha", calcula e cita.
- DECIMAL(10,3) — aritmética exata (Decimal), como manda `travas_operacionais_v6.1.json`
  (`precision_decimal_utxo:[10,3]`), evitando erro de float.
- F_i de doação e ZEPEC DELEGADOS ao pcpt.py, que lê de `tabelas/*.csv` (ENG-01, auditoria
  2026-07-10 — fonte única, anti-oracle). Travas de precisão (DECIMAL(10,3)) de motor00/
  (metadado de sistema, não tabela legal). Fórmulas conferidas contra CHK_03 e
  `engines/FORMULAS-CONSOLIDADAS.md`.

DEPENDÊNCIA DE TABELA (achado AUD-04 — `tabelas/` vazio): `V` (valor do terreno, Quadro 14) e
`CA_max` (Quadro 3/LPUOS) são DADO de tabela, ainda não ingerido no repo. Por isso são ENTRADAS
OBRIGATÓRIAS aqui — o engine NÃO os inventa (1.3). Quando `tabelas/` for populado, o roteador busca
V por SQL e CA_max por ZONA e injeta. Até lá, o engine calcula sobre valores fornecidos/de teste.

VACINA (FORMULAS-CONSOLIDADAS L-2/CONF-2): a grafia `C = (At/Ac) × V × Fs × Fp` sugerida em pedidos
NÃO tem fonte. As 3 fontes-mestre usam unanimemente `OO = (Área_Adicional/CA_max) × Fp × Fs × V`.
Esta é a implementada. Tabelas Fs/Fp aqui são PARCIAIS (só F-A/V3.1) — completar ao ingerir os quadros.

Uso:
    python3 engines/tdc/oodc.py --demo     # exemplo trabalhado + auto-teste (gate)
Trazido pela instância orquestradora do PU — auditoria profunda 2026-06-20 (destrave AUD-03/08).
"""
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TRAVAS = json.loads((AQUI / "motor00" / "travas_operacionais_v6.1.json").read_text(encoding="utf-8"))
LOCKS = TRAVAS["system_locks"]
PRECISAO = LOCKS["precision_decimal_utxo"][1]           # 3 casas (DECIMAL(10,3))

# Fonte legal comum (CHK_01) — toda citação aponta para cá.
FONTE_LEGAL = ("PDE Lei 16.050/2014; LPUOS Lei 16.402/2016; COE Lei 16.642/2017; "
               "Lei Federal 10.257/2001 (Estatuto da Cidade); Decretos 57.536/2016, 58.289/2018")

# Tabelas Fs/Fp — REFERÊNCIA (não usadas no cálculo; `outorga_onerosa` recebe fp/fs como ENTRADA
# externa). Faixas como FAIXA, nunca valor único: o engine NÃO arbitra o valor dentro da faixa
# (achado E-01 da auditoria 2026-06-20 — HMP=0,5 era valor INVENTADO, viola 1.3). Parciais (só
# constam em F-A/V3.1; ver vacina L-3 de FORMULAS-CONSOLIDADAS). Completar ao ingerir os quadros (B-3).
FATOR_SOCIAL_REF = {        # Fs por uso (FORMULAS-CONSOLIDADAS §1.4) — faixa textual, não Decimal
    "HIS": "0.0",
    "HMP": "0.4..0.6",      # FAIXA — exige o valor pontual do quadro; o engine não escolhe a mediana
    "R_acima_70m2": "1.0",
}
FATOR_PLANEJAMENTO_REF = {  # Fp por localização (FORMULAS-CONSOLIDADAS §1.4)
    "arco_centro_eixos_R": "1.2",
    "arco_centro_eixos_nR": "1.3",
    "macroarea_qualificacao": "0.6",
}

# B-12d (auditoria 2026-06-27): citação por DISPOSITIVO, não pela lei inteira (FONTE_LEGAL blob).
# Âncoras VERIFICADAS: PDE art. 125 por remissão na LPUOS 16.402/2016 Art. 24 (indexada); OODC pelo
# Estatuto da Cidade art. 28-31 (estável). Onde o artigo do PDE não está confirmado no verbatim
# (PDE 16.050 ainda `bruto`, B-4), `confianca:"a_confirmar"` — apontar+sinalizar é mais honesto (1.7)
# que citar a lei inteira. Cada resultado do engine carrega a sua.
CITACAO = {
    "OODC": {"norma": "Estatuto da Cidade (Lei 10.257/2001), art. 28-31; PDE (Lei 16.050/2014)",
             "dispositivo": "Estatuto da Cidade art. 28-31 (outorga onerosa e contrapartida)",
             "confianca": "alta", "obs": "art. do PDE 16.050 a confirmar no verbatim (PDE ainda bruto, B-4)"},
    "TDC_geracao_ZEPEC_BIR": {"norma": "PDE (Lei 16.050/2014), art. 125; LPUOS (Lei 16.402/2016), art. 24-26",
             "dispositivo": "PDE art. 125 (declaração de potencial construtivo passível de transferência) + LPUOS art. 24 (Fator de Incentivo Fi)",
             "confianca": "alta", "obs": "art. 125 do PDE verificado por remissão na LPUOS 16.402 Art. 24 (indexada)"},
    "TDC_geracao_doacao": {"norma": "PDE (Lei 16.050/2014), TDC por doação",
             "dispositivo": "PDE art. 122-125 (TDC; modalidade por doação de área)",
             "confianca": "a_confirmar", "obs": "faixa de artigos; art. exato a confirmar no verbatim do PDE (B-4)"},
    "TDC_recepcao": {"norma": "PDE (Lei 16.050/2014), recepção de potencial",
             "dispositivo": "PDE art. 124 (recepção de potencial no terreno receptor)",
             "confianca": "a_confirmar", "obs": "art. 124 por remissão na LPUOS; confirmar no verbatim do PDE (B-4)"},
}


def _d(x, nome="valor"):
    """SÓ converte para Decimal (não valida sinal — isso é `_exigir_positivo`). Aceita número BR:
    vírgula = decimal, ponto = milhar (achado B-12: as tabelas-fonte, Q14, são BR e quebravam aqui).
    Ex.: '1,5'→1.5 · '1.500,00'→1500.00 · '1.5'(US, sem vírgula)→1.5."""
    s = str(x).strip()
    if "," in s:                       # formato BR: ponto=milhar, vírgula=decimal
        s = s.replace(".", "").replace(",", ".")
    try:
        return Decimal(s)
    except Exception as e:
        raise ValueError(f"{nome}: não-numérico ({x!r}) — {e}")


def _q(v: Decimal) -> Decimal:
    """Quantiza a 3 casas (escala do DECIMAL). Usado no R$ da OODC — ver decisão B-12 abaixo."""
    return v.quantize(Decimal(10) ** -PRECISAO, rounding=ROUND_HALF_UP)


# B-12 (RESÍDUO FECHADO 2026-07-01) — a guarda de DECIMAL(10,3) TOTAL.
# `precision_decimal_utxo:[10,3]` = 10 dígitos totais, 3 decimais ⇒ parte inteira ≤ 7 dígitos
# (máx. 9_999_999.999). DECISÃO (a que o resíduo do B-12 pedia): o [10,3] é a precisão do **UTXO** —
# a UNIDADE DE CRÉDITO TRANSFERÍVEL, o **potencial construtivo em m²** (PC_pt/PC_r), fisicamente
# limitado (Art. 124 §3º já parcela PC_pt > 50.000 m²). NÃO se aplica ao **R$ da OODC**, que é
# MONETÁRIO e rotineiramente passa de dezenas de milhões (um imóvel real já deu R$931.800; grandes
# terrenos estouram 10^7). Aplicar [10,3] ao R$ RECUSARIA valor legítimo — erro. Então:
#   • m² PC (UTXO): `_q_utxo` quantiza a 3 casas E LEVANTA se estourar DECIMAL(10,3) (não cabe no tipo);
#   • R$ OODC (monetário): `_q`, sem teto de 7 dígitos (precisão monetária, não-UTXO).
DECIMAL_UTXO_INT_MAX = Decimal(10) ** (LOCKS["precision_decimal_utxo"][0] - PRECISAO)  # 10^7


def _q_utxo(v: Decimal, nome="PC") -> Decimal:
    """Quantiza a DECIMAL(10,3) o m² de potencial (UTXO) e EXIGE que caiba no tipo (B-12):
    parte inteira ≥ 10^7 não representável em DECIMAL(10,3) ⇒ LEVANTA (não trunca silencioso)."""
    q = v.quantize(Decimal(10) ** -PRECISAO, rounding=ROUND_HALF_UP)
    if q.copy_abs() >= DECIMAL_UTXO_INT_MAX:
        raise ValueError(
            f"{nome}={q} estoura DECIMAL(10,3) (parte inteira ≥ {DECIMAL_UTXO_INT_MAX}); "
            f"potencial construtivo (UTXO) não cabe no tipo — revisar insumos ou o tipo da coluna.")
    return q


def _exigir_positivo(v: Decimal, nome):
    if v <= 0:
        raise ValueError(f"{nome} deve ser > 0 (insumo de tabela ausente? ver AUD-04: tabelas/ vazio). Recebido: {v}")
    return v


def outorga_onerosa(area_adicional, ca_max, fp, fs, v):
    """OODC = (Área_Adicional / CA_max) × Fp × Fs × V   (FORMULAS-CONSOLIDADAS §1.4; F-A/F-B/F-C).
    `v` = valor do m² de terreno (Quadro 14, por SQL); `ca_max` = Quadro 3/LPUOS por ZONA."""
    aa = _exigir_positivo(_d(area_adicional, "area_adicional"), "area_adicional")
    cam = _exigir_positivo(_d(ca_max, "ca_max"), "ca_max")
    fpd, fsd, vd = _d(fp, "fp"), _d(fs, "fs"), _exigir_positivo(_d(v, "v"), "v")
    # guardas de sinal (B-12): Fp>0; Fs>=0 (HIS=0,0 é legítimo). OODC negativa = absurdo tributário.
    if fpd <= 0:
        raise ValueError(f"fp deve ser > 0 (Fator de Planejamento). Recebido: {fpd}")
    if fsd < 0:
        raise ValueError(f"fs deve ser >= 0 (Fator Social; HIS=0,0). Recebido: {fsd}")
    oo = (aa / cam) * fpd * fsd * vd
    return {
        "artefato": "OODC",
        "valor": _q(oo),
        "formula": "OO = (Área_Adicional / CA_max) × Fp × Fs × V",
        "memoria_calculo": f"({aa} / {cam}) × {fpd} × {fsd} × {vd} = {_q(oo)}",
        "inputs": {"area_adicional": str(aa), "ca_max": str(cam), "fp": str(fpd), "fs": str(fsd), "v": str(vd)},
        "citacao": CITACAO["OODC"],
    }


def potencial_gerado_zepec(atc_matricula, area_desapropriada, ca_basico):
    """ZEPEC-BIR: PC_pt = Atc_Liquido × CA_bas × F_i(area) ; Atc_Liquido = Atc_Matricula − Área_Desapropriada.
    A-02 (auditoria 2026-07-05): DELEGA ao engine de referência `pcpt.pcpt_sem_doacao`, que aplica o F_i
    ESCALONADO pela ÁREA (LPUOS Art. 24, I–VII). Antes usava F_i=1,0 estático (stale/errado) — fonte única
    agora é o pcpt; esta função é só o adaptador com a subtração de área desapropriada (CHK_03)."""
    import importlib
    _pcpt = importlib.import_module("pcpt")
    atc = _exigir_positivo(_d(atc_matricula, "atc_matricula"), "atc_matricula")
    desap = _d(area_desapropriada, "area_desapropriada")
    cab = _exigir_positivo(_d(ca_basico, "ca_basico"), "ca_basico")
    atc_liq = atc - desap
    e = _pcpt.pcpt_sem_doacao(str(atc_liq), str(cab))   # F_i escalonado nasce AQUI (fonte única)
    return {
        "artefato": "TDC_geracao_ZEPEC_BIR",
        "valor": _q_utxo(_d(e["valor_m2"], "PC_pt"), "PC_pt(ZEPEC)"),
        "formula": "PC_pt = (Atc_Matrícula − Área_Desapropriada) × CA_bas × F_i(área, Art.24)",
        "memoria_calculo": f"({atc} − {desap})={atc_liq} → {e['memoria_calculo']}",
        "inputs": {"atc_matricula": str(atc), "area_desapropriada": str(desap),
                   "ca_basico": str(cab), "fi": str(e["fi"]), "atc_liquido": str(atc_liq)},
        "citacao": CITACAO["TDC_geracao_ZEPEC_BIR"],
    }


def potencial_gerado_doacao(atc, ca_max, finalidade, v=None):
    """Doação: PC_pt = Atc × CA_max × F_i. DELEGA ao engine pcpt.pcpt_com_doacao (ENG-01: Fi
    lido de tabelas/*.csv, não de motor00/). finalidade ∈ {corredor_onibus, his,
    regularizacao_fundiaria, parque}. Para 'parque', V é obrigatório (resolve Fi pelo Art.127 §1º)."""
    import importlib
    _pcpt = importlib.import_module("pcpt")
    a = _exigir_positivo(_d(atc, "atc"), "atc")
    cam = _exigir_positivo(_d(ca_max, "ca_max"), "ca_max")
    e = _pcpt.pcpt_com_doacao(str(a), str(cam), finalidade, v=str(v) if v is not None else None)
    return {
        "artefato": f"TDC_geracao_{finalidade}",
        "valor": _q_utxo(_d(e["valor_m2"], "PC_pt"), "PC_pt(doacao)"),
        "formula": "PC_pt = Atc × CAmax × Fi",
        "memoria_calculo": e["memoria_calculo"],
        "inputs": {"atc": str(a), "ca_max": str(cam), "finalidade": finalidade,
                   "v": str(v) if v is not None else None},
        "citacao": CITACAO["TDC_geracao_doacao"],
    }


def potencial_recebido(pc_pt, vt_cd, c_r, ca_maxcd):
    """Recepção: PC_r = (PC_pt × VT_cd) / (C_r × CA_maxcd)   (CHK_03)."""
    pcp = _exigir_positivo(_d(pc_pt, "pc_pt"), "pc_pt")
    vt = _exigir_positivo(_d(vt_cd, "vt_cd"), "vt_cd")
    cr = _exigir_positivo(_d(c_r, "c_r"), "c_r")
    camcd = _exigir_positivo(_d(ca_maxcd, "ca_maxcd"), "ca_maxcd")
    pr = (pcp * vt) / (cr * camcd)
    return {
        "artefato": "TDC_recepcao",
        "valor": _q_utxo(pr, "PC_r"),
        "formula": "PC_r = (PC_pt × VT_cd) / (C_r × CA_maxcd)",
        "memoria_calculo": f"({pcp} × {vt}) / ({cr} × {camcd}) = {_q_utxo(pr, 'PC_r')}",
        "inputs": {"pc_pt": str(pcp), "vt_cd": str(vt), "c_r": str(cr), "ca_maxcd": str(camcd)},
        "citacao": CITACAO["TDC_recepcao"],
    }


def travas_operacionais(contexto: dict):
    """Versão EXECUTÁVEL (parcial) dos `conditional_blocks` de travas_operacionais_v6.1.json.
    Recebe um contexto da operação e devolve as travas DISPARADAS (bloqueios). Determinístico.
    NÃO cobre todos os 9 blocos (alguns exigem dados espaciais/registrais externos) — declara
    quais avaliou. Cada trava aponta o bloco-fonte."""
    disparadas = []
    c = contexto or {}
    if str(c.get("uso_receptor", "")).upper() == "HIS":
        disparadas.append("BLOCK_OPERATION — Uso_Receptor == 'HIS'")
    if c.get("lote_receptor_contaminacao") is True:
        disparadas.append("BLOCK_AVERBACAO — Lote_Receptor_Contaminacao == TRUE")
    if str(c.get("cnib_status", "")).upper() == "INDISPONIVEL" or c.get("cadin_status") is True:
        disparadas.append("BLOCK_EMISSION — CNIB indisponível ou CADIN ativo")
    if str(c.get("status_alvara_receptor", "")).upper() == "CANCELED":
        disparadas.append("ROLLBACK_TRANSACTION — Status_Alvara_Receptor == 'CANCELED'")
    if c.get("analise_conjunto_aprovada") is True and _d(c.get("area_global", 0)) > 500:
        disparadas.append("DISABLE_ISENCAO_QA + REQUIRE área consolidada — gatilho 500m² (evasão Quota Ambiental)")
    avaliados = ["HIS", "contaminação", "CNIB/CADIN", "alvará cancelado", "gatilho 500m²"]

    # B-12c: trava FATAL de gabarito em CAMPO PRÓPRIO e EXECUTADA (antes caía mudo em
    # blocos_nao_avaliados). Regra (travas_operacionais_v6.1.json): projeção volumétrica TDC >
    # Min(LPUOS_Q3, COMAER_ZCS, CONPRESP_Envoltória) ⇒ FATAL_ERROR — gabarito aeronáutico/tombamento
    # NÃO admite potencial acima do envelope. Avalia se o contexto fornecer projeção + ≥1 limite.
    limites = {k: _d(c[k], k) for k in ("lpuos_q3_max", "comaer_zcs_max", "conpresp_envoltoria_max")
               if c.get(k) is not None}
    fatal = {
        "avaliavel": False, "disparado": False, "limite_aplicado": None,
        "limites_recebidos": {k: str(v) for k, v in limites.items()},
        "citacao": {"norma": "COMAER (ZCS — gabarito aeronáutico); CONPRESP (envoltória de tombamento); LPUOS Quadro 3",
                    "dispositivo": "Min(LPUOS Quadro 3, COMAER ZCS, CONPRESP Envoltória) — trava FATAL de gabarito",
                    "confianca": "a_confirmar",
                    "obs": "limites externos (espacial/registral); fornecer projecao_volumetrica_tdc + lpuos_q3_max/comaer_zcs_max/conpresp_envoltoria_max no contexto"},
    }
    proj = c.get("projecao_volumetrica_tdc")
    if proj is not None and limites:
        projd = _d(proj, "projecao_volumetrica_tdc")
        lim = min(limites.values())
        fatal.update({
            "avaliavel": True, "disparado": projd > lim, "limite_aplicado": str(lim),
            "projecao_volumetrica_tdc": str(projd),
            "motivo": (f"projeção {projd} > Min(gabaritos)={lim} ⇒ FATAL_ERROR" if projd > lim
                       else f"projeção {projd} ≤ {lim} (dentro do gabarito)"),
        })

    return {
        "travas_disparadas": disparadas,
        "bloqueado": bool(disparadas) or fatal["disparado"],
        "fatal": fatal,
        "blocos_avaliados": avaliados + (["gabarito FATAL (COMAER/CONPRESP/LPUOS-Q3)"] if fatal["avaliavel"] else []),
        "blocos_nao_avaliados": "ZOE Butantan (ADI), ITCMD/óbito, FUNDURB 5% — exigem dados externos"
                                + ("" if fatal["avaliavel"] else "; gabarito FATAL não avaliado (faltou projeção/limites no contexto)"),
        "citacao": {"fonte": "travas_operacionais_v6.1.json (system_locks.conditional_blocks)",
                    "obs": "trava FATAL com citação por dispositivo no campo 'fatal' (B-12d)"},
    }


# --------------------------------------------------- B-1/H3: roteador sobre DADO REAL (porte 2026-06-28)
# Porte do produto B-17 (branch project-audit-roadmap) ao engine do main, sob o gate (D38/D21).
# `oodc_por_imovel` busca V (Quadro 14 por SQ+Codlog) e CA_max (Quadro 3 por zona) das tabelas/ REAIS e
# chama `outorga_onerosa` — herdando a citação por DISPOSITIVO (B-12d). UNE a citação legal (B-12d) à
# PROVENIÊNCIA do dado (Q14/Quadro 3): "número nasce no engine" (1.3) ponta-a-ponta. O engine NÃO inventa
# V nem CA_max (1.3) — par/zona sem dado de tabela LEVANTA, não preenche. (Engine do B-17 era pré-B-12d:
# trouxe-se SÓ o roteador, preservando o `outorga_onerosa`+CITACAO B-12d do main — citação não regride.)
TABELAS = AQUI.parent.parent / "tabelas"


def _ler_csv(path):
    """Lê CSV ignorando linhas-comentário '#'. Retorna list[dict]."""
    import csv as _csv
    if not path.exists():
        return []
    linhas = [l for l in path.read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    return list(_csv.DictReader(linhas))


def carregar_tabelas():
    """Carrega o COMBUSTÍVEL real (1.1): V por (SQ,Codlog) (Quadro 14 — um SQ/quadra tem várias faces de
    rua, cada uma com seu V) e CA_max por zona (Quadro 3). Devolve (V:{(sql,codlog)->valor_brl},
    CA:{zona->ca_max}). Vazio se as tabelas não existirem (não inventa)."""
    V = {(r["sql"], r["codlog"]): r["valor_m2_brl"] for r in _ler_csv(TABELAS / "q14-valor-terreno.csv")}
    CA = {r["zona"]: r["ca_max"] for r in _ler_csv(TABELAS / "quadro3-ca-por-zona.csv")}
    return V, CA


def fs_por_categoria(categoria, _exato=False):
    """B-3 (lado Fs): Fator de interesse social Fs por CATEGORIA DE USO, lido do Quadro 5 REAL
    (`tabelas/quadro5-fator-social-fs.csv`, Anexo da Lei 16.050/2014) — o engine NÃO inventa (1.3).
    O Quadro 5 traz Fs DISCRETO (não faixa): HIS/públicos=0,0 · privados de interesse social=0,3/0,7 ·
    'Outras Atividades'=1,0. Casa por categoria (substring normalizado; `_exato` força igualdade).
    LEVANTA se a categoria não existe no quadro (não chuta valor de faixa — vacina E-01: HMP=0,5 era
    INVENTADO). NOTA: 'HMP' NÃO consta neste extrato do Quadro 5 — cobrir HMP exige a fonte completa (B-4).
    Devolve {fs, categoria_fonte, citacao}."""
    linhas = _ler_csv(TABELAS / "quadro5-fator-social-fs.csv")
    if not linhas:
        raise ValueError("Quadro 5 (Fs) ausente em tabelas/ — não há dado para o lookup (1.3).")
    alvo = "".join(ch for ch in str(categoria).lower() if ch.isalnum() or ch == " ").strip()
    achados = []
    for r in linhas:
        cat = r.get("categoria_uso", "")
        catn = "".join(ch for ch in cat.lower() if ch.isalnum() or ch == " ").strip()
        if (catn == alvo) if _exato else (alvo and alvo in catn):
            achados.append((cat, r.get("fs")))
    if not achados:
        raise ValueError(f"categoria {categoria!r} não encontrada no Quadro 5 (Fs). "
                         f"Fs nasce da tabela, não do chute (1.3) — confira a categoria ou ingira o quadro completo (B-4).")
    if len({fs for _, fs in achados}) > 1:
        raise ValueError(f"categoria {categoria!r} casou múltiplos Fs divergentes {achados} — "
                         f"desambiguar (use _exato=True ou categoria mais específica).")
    cat_fonte, fs = achados[0]
    return {
        "fs": _d(fs, "fs"),
        "categoria_fonte": cat_fonte,
        "citacao": {"norma": "PDE (Lei 16.050/2014), Quadro 5 (Anexo) — Fator de interesse social Fs",
                    "dispositivo": "Quadro 5 do PDE (Fs por categoria de uso)", "confianca": "alta",
                    "fonte_tabela": "tabelas/quadro5-fator-social-fs.csv"},
    }


def _ca_max_nota(zona):
    """Nota condicional do CA_max da zona (A-080), ou ''. Ex.: ZEIS-3 -> 'g'."""
    for r in _ler_csv(TABELAS / "quadro3-ca-por-zona.csv"):
        if r["zona"] == zona:
            return r.get("ca_max_nota", "") or ""
    return ""


def oodc_por_imovel(sql, codlog, zona, area_adicional, fp, fs):
    """OODC sobre dados REAIS (B-1): busca V por (SQ,Codlog) (Quadro 14) e CA_max por ZONA (Quadro 3/
    LPUOS) nas tabelas/ — o engine NÃO inventa nenhum dos dois (1.3). O operador fornece área adicional,
    Fp, Fs. (SQ+Codlog vêm do cadastro; zona vem do geo/zoneamento por lote — ligação espacial é H3.)
    O resultado UNE a citação por DISPOSITIVO (B-12d, via `outorga_onerosa`) à proveniência do dado."""
    V, CA = carregar_tabelas()
    v = V.get((sql, codlog))
    if v is None:
        raise ValueError(f"(SQ {sql!r}, Codlog {codlog!r}) sem V no Quadro 14. Confira o par no cadastro.")
    ca_max = CA.get(zona)
    if not ca_max or ca_max == "NA":
        raise ValueError(f"zona {zona!r} sem CA_max numérico no Quadro 3 (CA_max={ca_max!r}).")
    r = outorga_onerosa(area_adicional, ca_max, fp, fs, v)
    nota = _ca_max_nota(zona)
    r["fonte_dados"] = {"sql": sql, "codlog": codlog, "V_q14_brl": v, "zona": zona, "ca_max_q3": ca_max,
                        "proveniencia": "V=Quadro 14 (PDE) por SQ+Codlog, CA_max=Quadro 3 (LPUOS) por zona — tabelas/ reais, não ilustrativo"}
    if nota:   # A-080: CA_max condicional — não silenciar
        r["aviso"] = (f"CA_max da zona {zona} tem nota condicional '({nota})' no Quadro 3 (LPUOS) cuja legenda ainda "
                      f"não foi capturada do PDF — o valor {ca_max} pode depender do tipo de empreendimento. CONFERIR antes de usar em produção.")
    return r


# ----------------------------------------------------------------------------- auto-teste / demo
def _autoteste():
    falhas = []

    def checa(nome, got, esperado):
        if Decimal(str(got)) != Decimal(str(esperado)):
            falhas.append(f"{nome}: obtido {got}, esperado {esperado}")

    # OODC: (1000/4)×1.2×1.0×3000 = 250×3600 = 900000
    checa("OODC", outorga_onerosa(1000, 4, "1.2", "1.0", 3000)["valor"], "900000.000")
    # ZEPEC (A-02: F_i escalonado): Atc_liq=(500−50)=450 → área ≤500 → F_i=1,2 → 450×2×1,2 = 1080
    checa("ZEPEC (Fi escalonado Art.24)", potencial_gerado_zepec(500, 50, 2)["valor"], "1080.000")
    # ENG-01 corrigido: delega ao pcpt.py (Fi de tabelas/fi-incentivo-doacao.csv, não motor00/)
    # Doação corredor: 300×2.5×2.0 = 1500
    checa("doacao corredor", potencial_gerado_doacao(300, "2.5", "corredor_onibus")["valor"], "1500.000")
    # HIS: 100×1×1.9 = 190
    checa("doacao HIS", potencial_gerado_doacao(100, 1, "his")["valor"], "190.000")
    # ENG-02 corrigido: regularizacao_fundiaria (Art.127 §1º III, Fi=0.8): 100×1×0.8 = 80
    checa("doacao regularizacao", potencial_gerado_doacao(100, 1, "regularizacao_fundiaria")["valor"], "80.000")
    # Parque com V: 100×4×1.4 = 560 (V≤2000 → Fi=1.4)
    checa("doacao parque", potencial_gerado_doacao(100, 4, "parque", v=1500)["valor"], "560.000")
    # Recepção: (900×4000)/(2×2000) = 3.6e6/4000 = 900
    checa("recepcao", potencial_recebido(900, 4000, 2, 2000)["valor"], "900.000")
    # Trava HIS dispara
    if not travas_operacionais({"uso_receptor": "HIS"})["bloqueado"]:
        falhas.append("trava HIS não disparou")
    # Insumo de tabela ausente (v=0) deve levantar
    try:
        outorga_onerosa(1000, 4, "1.2", "1.0", 0); falhas.append("v=0 não levantou ValueError")
    except ValueError:
        pass
    # B-12: decimal BR não pode mais quebrar
    checa("decimal BR vírgula", _d("1,5"), "1.5")
    checa("decimal BR milhar", _d("1.500,00"), "1500.00")
    checa("decimal US (sem vírgula)", _d("1.5"), "1.5")
    # B-12: Fp<=0 e Fs<0 devem levantar (OODC negativa é absurdo)
    for fp, fs, rotulo in (("-1", "1", "fp negativo"), ("1", "-0.5", "fs negativo")):
        try:
            outorga_onerosa(1000, 4, fp, fs, 100); falhas.append(f"{rotulo} não levantou ValueError")
        except ValueError:
            pass
    # Fs=0 (HIS) é LEGÍTIMO, não pode levantar; OODC = 0
    checa("fs=0 (HIS) legítimo", outorga_onerosa(1000, 4, "1.2", "0.0", 100)["valor"], "0.000")
    # B-12c: trava FATAL de gabarito
    t_fatal = travas_operacionais({"projecao_volumetrica_tdc": "1200", "comaer_zcs_max": "1000", "lpuos_q3_max": "1500"})
    if not (t_fatal["fatal"]["avaliavel"] and t_fatal["fatal"]["disparado"] and t_fatal["bloqueado"]):
        falhas.append("FATAL gabarito não disparou com projeção 1200 > Min(1000,1500)")
    t_ok = travas_operacionais({"projecao_volumetrica_tdc": "800", "comaer_zcs_max": "1000"})
    if t_ok["fatal"]["disparado"] or not t_ok["fatal"]["avaliavel"]:
        falhas.append("FATAL gabarito disparou indevidamente com projeção 800 ≤ 1000")
    t_na = travas_operacionais({"uso_receptor": "R"})  # sem limites → não-avaliável, não some
    if t_na["fatal"]["avaliavel"]:
        falhas.append("FATAL marcou avaliável sem limites no contexto")
    # B-12d: citação por dispositivo (não a lei inteira) no resultado do engine
    cit = outorga_onerosa(1000, 4, "1.2", "1.0", 3000)["citacao"]
    if "dispositivo" not in cit or "art" not in cit["dispositivo"].lower():
        falhas.append("OODC sem citação por dispositivo (B-12d)")
    # B-12 (resíduo fechado): guarda DECIMAL(10,3) do UTXO (m² PC).
    #  (a) PC que ESTOURA o tipo (parte inteira ≥ 10^7) LEVANTA — não trunca silencioso.
    try:
        potencial_gerado_doacao("10000000", 1, "his"); falhas.append("PC_pt 10^7 (Fi 1.9) não levantou overflow DECIMAL(10,3)")
    except ValueError:
        pass
    #  (b) PC alto (< 10^7) NÃO levanta e quantiza a 3 casas. 5.000.000×1×1.9 = 9.500.000.
    checa("PC_pt alto (<10^7) não levanta", potencial_gerado_doacao("5000000", 1, "his")["valor"], "9500000.000")
    #  (c) DECISÃO B-12: o R$ da OODC é MONETÁRIO — NÃO se sujeita ao teto UTXO (pode passar de 10^7).
    #      (1000/4)×2×1×50000 = 25.000.000 (>10^7) tem de calcular, não levantar.
    r_grande = outorga_onerosa(1000, 4, "2", "1", 50000)
    checa("R$ OODC > 10^7 é legítimo (monetário, não-UTXO)", r_grande["valor"], "25000000.000")
    # B-3 (lado Fs): lookup do Fator social Fs no Quadro 5 REAL — HIS=0,0; 'Outras Atividades'=1,0.
    if _ler_csv(TABELAS / "quadro5-fator-social-fs.csv"):
        checa("Fs HIS (Quadro 5)", fs_por_categoria("Habitação de Interesse Social")["fs"], "0.0")
        checa("Fs Outras Atividades (Quadro 5)", fs_por_categoria("Outras Atividades")["fs"], "1.0")
        # categoria inexistente LEVANTA (não chuta — 1.3)
        try:
            fs_por_categoria("uso inexistente xyz"); falhas.append("Fs categoria inexistente não levantou")
        except ValueError:
            pass
        # categoria ambígua (Fs divergentes no quadro: 'Universidades' = 0,3 e 0,7) LEVANTA
        try:
            fs_por_categoria("Universidades"); falhas.append("Fs categoria ambígua (Univ. 0,3/0,7) não levantou")
        except ValueError:
            pass
    # B-1 (porte 2026-06-28): OODC sobre DADO REAL — V por SQL (Quadro 14) e CA_max por zona (Quadro 3).
    # SQ 001003/Codlog 038121 -> V=R$3.106,00 ; zona ZEU -> CA_max=4 ; (1000/4)×1.2×1.0×3106 = 931800.
    V, CA = carregar_tabelas()
    if V and CA:
        r = oodc_por_imovel("001003", "038121", "ZEU", 1000, "1.2", "1.0")
        checa("OODC dado real (SQ 001003/038121 × ZEU)", r["valor"], "931800.000")
        if r["fonte_dados"]["V_q14_brl"] != "3.106,00":
            falhas.append(f"V real de (001003,038121) mudou: {r['fonte_dados']['V_q14_brl']!r} (esperado '3.106,00')")
        # B-12d não regride no porte: o resultado por-imóvel carrega a citação por dispositivo
        if "dispositivo" not in r.get("citacao", {}) or "art" not in r["citacao"]["dispositivo"].lower():
            falhas.append("oodc_por_imovel: citação por dispositivo (B-12d) não veio no resultado")
        # zona sem CA_max numérico (AVP-1 = '(k)' variável) deve levantar — engine não inventa (1.3)
        try:
            oodc_por_imovel("001003", "038121", "AVP-1", 1000, "1.2", "1.0"); falhas.append("AVP-1 (CA_max NA) não levantou")
        except ValueError:
            pass
    return falhas


def _demo():
    print("# DEMO — engine OODC/TDC (valores ILUSTRATIVOS; V e CA_max viriam de tabelas/ — AUD-04)\n")
    casos = [
        ("Outorga Onerosa (R>70m², Arco)", outorga_onerosa(1200, 4, "1.2", "1.0", 2500)),
        ("Geração ZEPEC-BIR (tombado)", potencial_gerado_zepec(800, 0, 1)),
        ("Geração Doação corredor (F_i=2.0)", potencial_gerado_doacao(600, "2.5", "corredor_onibus")),
        ("Recepção no receptor", potencial_recebido(1500, 5000, 2, 2000)),
    ]
    for nome, r in casos:
        print(f"## {nome}\n   {r['formula']}\n   {r['memoria_calculo']}\n   = {r['valor']}  | cita: {r['citacao']['dispositivo']}\n")
    print("## Travas operacionais (exemplo HIS + contaminação):")
    print("  ", travas_operacionais({"uso_receptor": "HIS", "lote_receptor_contaminacao": True})["travas_disparadas"])


if __name__ == "__main__":
    if "--demo" in sys.argv:
        _demo()
    falhas = _autoteste()
    if falhas:
        print("\nAUTO-TESTE FALHOU:", *falhas, sep="\n  ", file=sys.stderr)
        sys.exit(1)
    print("\nauto-teste OODC/TDC: OK (todas as fórmulas conferem).")
