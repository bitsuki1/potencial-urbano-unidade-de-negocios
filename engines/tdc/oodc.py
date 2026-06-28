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
- Constantes NÃO duplicadas: F_i e travas são lidos de `motor00/travas_operacionais_v6.1.json`
  (fonte única). Fórmulas conferidas contra `motor00/semantic_chunks_v6.1.json` (CHK_03) e
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
FATOR_INCENTIVO = LOCKS["fator_incentivo_fi"]           # zepec_bir, doacao_his, doacao_viario, ...
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
    """Quantiza a DECIMAL(10,3)."""
    return v.quantize(Decimal(10) ** -PRECISAO, rounding=ROUND_HALF_UP)


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
    """ZEPEC-BIR: PC_pt = Atc_Liquido × CA_bas × 1.0 ; Atc_Liquido = Atc_Matricula − Área_Desapropriada.
    (semantic_chunks CHK_03). F_i = 1.0 (zepec_bir)."""
    atc = _exigir_positivo(_d(atc_matricula, "atc_matricula"), "atc_matricula")
    desap = _d(area_desapropriada, "area_desapropriada")
    cab = _exigir_positivo(_d(ca_basico, "ca_basico"), "ca_basico")
    fi = _d(FATOR_INCENTIVO["zepec_bir"], "fi")
    atc_liq = atc - desap
    pc = atc_liq * cab * fi
    return {
        "artefato": "TDC_geracao_ZEPEC_BIR",
        "valor": _q(pc),
        "formula": "PC_pt = (Atc_Matrícula − Área_Desapropriada) × CA_bas × F_i(=1.0)",
        "memoria_calculo": f"({atc} − {desap}) × {cab} × {fi} = {_q(pc)}",
        "inputs": {"atc_matricula": str(atc), "area_desapropriada": str(desap),
                   "ca_basico": str(cab), "fi": str(fi), "atc_liquido": str(atc_liq)},
        "citacao": CITACAO["TDC_geracao_ZEPEC_BIR"],
    }


def potencial_gerado_doacao(atc, ca_max, modalidade):
    """Doação: PC_pt = Atc × CA_max × F_i.  modalidade ∈ {doacao_his, doacao_viario,
    doacao_parques_low_val, doacao_parques_high_val} (F_i de travas_operacionais)."""
    if modalidade not in FATOR_INCENTIVO:
        raise ValueError(f"modalidade {modalidade!r} sem F_i; válidas: {sorted(FATOR_INCENTIVO)}")
    a = _exigir_positivo(_d(atc, "atc"), "atc")
    cam = _exigir_positivo(_d(ca_max, "ca_max"), "ca_max")
    fi = _d(FATOR_INCENTIVO[modalidade], "fi")
    pc = a * cam * fi
    return {
        "artefato": f"TDC_geracao_{modalidade}",
        "valor": _q(pc),
        "formula": "PC_pt = Atc × CA_max × F_i",
        "memoria_calculo": f"{a} × {cam} × {fi} = {_q(pc)}",
        "inputs": {"atc": str(a), "ca_max": str(cam), "modalidade": modalidade, "fi": str(fi)},
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
        "valor": _q(pr),
        "formula": "PC_r = (PC_pt × VT_cd) / (C_r × CA_maxcd)",
        "memoria_calculo": f"({pcp} × {vt}) / ({cr} × {camcd}) = {_q(pr)}",
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


# ----------------------------------------------------------------------------- auto-teste / demo
def _autoteste():
    falhas = []

    def checa(nome, got, esperado):
        if Decimal(str(got)) != Decimal(str(esperado)):
            falhas.append(f"{nome}: obtido {got}, esperado {esperado}")

    # OODC: (1000/4)×1.2×1.0×3000 = 250×3600 = 900000
    checa("OODC", outorga_onerosa(1000, 4, "1.2", "1.0", 3000)["valor"], "900000.000")
    # ZEPEC: (500−50)×2.0×1.0 = 900
    checa("ZEPEC", potencial_gerado_zepec(500, 50, 2)["valor"], "900.000")
    # Doação viário: 300×2.5×2.0 = 1500
    checa("doacao_viario", potencial_gerado_doacao(300, "2.5", "doacao_viario")["valor"], "1500.000")
    # F_i HIS = 1.9: 100×1×1.9 = 190
    checa("doacao_his Fi", potencial_gerado_doacao(100, 1, "doacao_his")["valor"], "190.000")
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
    return falhas


def _demo():
    print("# DEMO — engine OODC/TDC (valores ILUSTRATIVOS; V e CA_max viriam de tabelas/ — AUD-04)\n")
    casos = [
        ("Outorga Onerosa (R>70m², Arco)", outorga_onerosa(1200, 4, "1.2", "1.0", 2500)),
        ("Geração ZEPEC-BIR (tombado)", potencial_gerado_zepec(800, 0, 1)),
        ("Geração Doação viário (F_i=2.0)", potencial_gerado_doacao(600, "2.5", "doacao_viario")),
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
