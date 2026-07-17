#!/usr/bin/env python3
"""
art128.py — Engine determinístico do VALOR DE REFERÊNCIA LEGAL do potencial do CEDENTE (lado VENDEDOR),
segundo o Art. 128 da Lei 16.050/2014 (PDE). Complementa pcpt.py (que produz o PCpt) e é o motor do
"preço LEGAL" (D-DONO-7/15: preço é saída de engine rastreável ao artigo; a MARGEM é do usuário —
este engine NÃO define preço de venda, só a referência regulatória).

────────────────────────────────────────────────────────────────────────────────────────────────────
FÓRMULA (Art. 128, VERBATIM — rag/chunks/lei-municipal-saopaulo-16050-2014/133__art-128.json):

    PCr = (PCpt × VTcd) / (Cr × CAmaxcd)

    PCr     – potencial construtivo equivalente a ser recebido no imóvel RECEPTOR (m²);
    PCpt    – potencial construtivo passível de transferência do CEDENTE (m²) — vem do pcpt.py (Art. 125);
    VTcd    – valor unitário (R$/m²) do terreno CEDENTE, Cadastro de Valor de Terreno p/ Outorga Onerosa
              (= Quadro 14), vigente na data de referência;
    Cr      – valor unitário (R$/m²) da contrapartida da outorga onerosa no imóvel RECEPTOR (Art. 117);
    CAmaxcd – coef. de aproveitamento máximo do imóvel cedente.
      §1º — quando o PCpt foi originado no Art. 125 (SEM doação — NOSSO universo), CAmaxcd = 4 (quatro).
      §2º — o VTcd é corrigido pelo IPCA acumulado entre o mês seguinte ao mês de referência da Declaração
            e o último mês anterior ao protocolo do pedido de Certidão de Transferência.

────────────────────────────────────────────────────────────────────────────────────────────────────
ESCOPO VENDEDOR (D-DONO-15) — o que este engine PODE e o que NÃO faz:

  O único dado do RECEPTOR na equação é o Cr. Mas o VALOR ECONÔMICO que o potencial do vendedor
  representa é PCr × Cr (a outorga que o comprador DEIXA de pagar ao Município ao comprar via TDC):

      PCr × Cr = (PCpt × VTcd) / CAmaxcd          ← o Cr CANCELA algebricamente.

  Logo, a REFERÊNCIA regulatória do potencial do vendedor é (PCpt × VTcd) / CAmaxcd — receptor-INDEPENDENTE,
  100% rastreável a Art. 128 caput + §1º. Este engine entrega OS DOIS números (decisão do dono 2026-07-10,
  "mostrar os dois"), cada um citado:

    • numerador_brl  = PCpt × VTcd                (bruto — potencial avaliado pelo terreno cedente)
    • referencia_brl = (PCpt × VTcd) / CAmaxcd    (referência que independe do comprador; Cr cancela)

  O PCr em si (m² no receptor) e o Cr NÃO são calculados aqui — são do lado comprador (fora de escopo).

Princípios (iguais a pcpt.py):
  1.1 — VTcd/CAmaxcd são DADO extraído da lei (§1º) ou ENTRADA (Quadro 14); o engine não inventa tabela.
  1.3 — número nasce AQUI; PCpt/VTcd/fator IPCA são ENTRADAS; o engine não adivinha "hoje" nem a série IPCA.
  1.7 — cada linha do memorial carrega o dispositivo e a fonte.
  Decimal exato (nunca float); entrada ambígua é REJEITADA, não adivinhada.

Uso:
    python3 engines/tdc/art128.py --demo     # exemplo trabalhado + auto-teste (gate)
PU 18 · 2026-07-10.
"""
import re
import csv
import argparse
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

LEI = "Lei Municipal SP nº 16.050/2014 (PDE)"
DEC_ESQUINA = "Decreto Municipal SP nº 57.536/2016, Art. 3º, IV"   # regra da esquina (MAX Quadro 14)
QUADRO14 = "Quadro 14 do PDE (Cadastro de Valor de Terreno para fins de Outorga Onerosa)"
IPCA_FONTE = "IBGE/SIDRA tabela 1737 (IPCA número-índice) — tabelas/ipca-numero-indice-ibge.csv"
Q2 = Decimal("0.01")
CAMAXCD_VIA125 = Decimal("4")     # Art. 128 §1º — origem no Art. 125 (sem doação): CAmaxcd = 4 (fixo)
TABELAS = Path(__file__).resolve().parents[2] / "tabelas"
IPCA_CSV = TABELAS / "ipca-numero-indice-ibge.csv"
Q14_REAJUSTE_CSV = TABELAS / "q14-reajuste-anual.csv"   # série de reajuste do Quadro 14 (base 2014 → vigente)


def carregar_ipca(path=IPCA_CSV):
    """{ 'AAAA-MM': Decimal(numero_indice) } lido de tabelas/ (1.1 — o engine lê a tabela, não a inventa).
    Falha ALTO se o arquivo sumir/corromper (1.3 fail-closed)."""
    if not Path(path).exists():
        raise FileNotFoundError(f"série IPCA ausente: {path} (Art. 128 §2º — o engine lê a tabela, não a inventa)")
    serie = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0].lstrip().startswith("#") or row[0].strip() == "mes":
                continue
            serie[row[0].strip()] = Decimal(row[1].strip())
    if len(serie) < 2:
        raise ValueError(f"série IPCA vazia/corrompida: {path}")
    return serie


def carrega_reajuste_q14(path=Q14_REAJUSTE_CSV):
    """Série de reajuste do Quadro 14 → [(ano_ref, fator_acumulado, decreto, dispositivo)] ordenada por ano.
    1.1/1.3 — o motor LÊ a tabela (base 2014 → fator vigente por exercício), não inventa nem adivinha 'hoje'.
    Fail-closed se sumir/corromper."""
    if not Path(path).exists():
        raise FileNotFoundError(f"série de reajuste do Quadro 14 ausente: {path} "
                                "(o engine lê o fator vigente da tabela, não o inventa)")
    linhas = []
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0].lstrip().startswith("#") or row[0].strip() == "ano_ref":
                continue
            linhas.append((int(row[0].strip()), Decimal(row[3].strip()), row[4].strip(), row[6].strip()))
    if not linhas:
        raise ValueError(f"série de reajuste do Quadro 14 vazia: {path}")
    return sorted(linhas, key=lambda x: x[0])


def fator_reajuste_q14(ano_ref=None, serie=None):
    """Fator ACUMULADO do Quadro 14 vigente no exercício `ano_ref` (base 2014 = 1,0).
    ano_ref None ⇒ vintage MAIS RECENTE (o piso de prospecção de hoje). Devolve (fator, decreto, dispositivo).
    1.6 — retorna o fator da última linha com ano_ref <= exercício pedido (o reajuste vale até o próximo)."""
    linhas = serie if serie is not None else carrega_reajuste_q14()
    if ano_ref is None:
        f, dec, disp = linhas[-1][1], linhas[-1][2], linhas[-1][3]
        return f, dec, disp
    escolhido = linhas[0]
    for ln in linhas:
        if ln[0] <= int(ano_ref):
            escolhido = ln
        else:
            break
    return escolhido[1], escolhido[2], escolhido[3]


def vtcd_vigente(valor_base_2014, ano_ref=None, esquina=False):
    """VTcd VIGENTE = valor_base_2014 (Quadro 14, tabelas/q14-valor-terreno.csv) × fator de reajuste do
    exercício (tabelas/q14-reajuste-anual.csv). É o V que o Art. 128/OODC exige "vigente na data de referência".
    Sem esta correção, um cálculo para fato gerador recente usa o V CONGELADO de 2014 (subavaliado).
    Devolve dict com o valor vigente, o fator aplicado e a citação (1.7). ano_ref None ⇒ vintage mais recente."""
    base = _pos(_d(valor_base_2014, "valor_base_2014"), "valor_base_2014")
    fator, decreto, disp = fator_reajuste_q14(ano_ref)
    vig = (base * fator).quantize(Q2, ROUND_HALF_UP)
    disp_c = f"{QUADRO14}; reajuste acumulado {decreto} ({disp})"
    if esquina:
        disp_c += f"; {DEC_ESQUINA} (maior valor da quadra — lote de esquina)"
    return {
        "vtcd_base_2014_m2": str(base),
        "fator_reajuste": str(fator),
        "decreto_reajuste": decreto,
        "ano_ref": ("mais recente" if ano_ref is None else str(ano_ref)),
        "vtcd_vigente_m2": str(vig),
        "citacao": {"dispositivo": disp_c, "fonte": "tabelas/q14-reajuste-anual.csv"},
        "memoria_calculo": f"VTcd_vigente = base2014(R$ {base}) × fator({fator}) = R$ {vig}/m²  [{decreto}]",
    }


def vtcd_na_data(vtcd_conhecido, ano_conhecido, ano_alvo):
    """Art. 128 §2º — converte um VTcd CONHECIDO de um exercício para o VTcd de OUTRO exercício
    (tipicamente: do vigente da base enriquecida → o da DATA DA DECLARAÇÃO). Como o reajuste do
    Quadro 14 é UNIFORME para todas as faces de quadra (Dec. 63.999/2024 Art. 1º; 64.884/2025 Art. 1º),
    vale a razão exata: VTcd(alvo) = VTcd(conhecido) × fator(alvo) ÷ fator(conhecido) — sem precisar do
    nominal por face. Fecha o resíduo "falta o VTcd histórico da Declaração": conhecendo o VTcd de
    QUALQUER exercício, o de outro sai exato. O §2º do Art. 128 aplica o IPCA DEPOIS (corrigir_vtcd_ipca)."""
    v = _pos(_d(vtcd_conhecido, "vtcd_conhecido"), "vtcd_conhecido")
    f_con = fator_reajuste_q14(ano_conhecido)[0]
    f_alv, dec_alv, disp_alv = fator_reajuste_q14(ano_alvo)
    vtcd = (v * f_alv / f_con).quantize(Q2, ROUND_HALF_UP)
    return {
        "vtcd_alvo_m2": str(vtcd),
        "ano_conhecido": str(ano_conhecido), "fator_conhecido": str(f_con),
        "ano_alvo": str(ano_alvo), "fator_alvo": str(f_alv), "decreto_alvo": dec_alv,
        "citacao": {"dispositivo": f"Art. 128 §2º — VTcd da data de referência via razão de reajuste do Quadro 14 ({disp_alv})",
                    "fonte": "tabelas/q14-reajuste-anual.csv"},
        "memoria_calculo": f"VTcd({ano_alvo}) = VTcd({ano_conhecido})=R$ {v} × fator({f_alv})÷fator({f_con}) = R$ {vtcd}/m²",
    }


def _mes_anterior(mes):
    """'AAAA-MM' → mês imediatamente anterior."""
    if not re.fullmatch(r"\d{4}-\d{2}", str(mes).strip()):
        raise ValueError(f"mês inválido (use AAAA-MM): {mes!r}")
    y, m = int(mes[:4]), int(mes[5:7])
    m -= 1
    if m == 0:
        y, m = y - 1, 12
    return f"{y:04d}-{m:02d}"


def fator_ipca(mes_ref, mes_protocolo, serie=None):
    """Art. 128 §2º — fator de correção do VTcd = índice[último mês ANTES do protocolo, se disponível]
    ÷ índice[mês de referência]. Devolve (fator, mes_fim). Fail-closed se o mês de referência estiver
    fora da série. Se o protocolo for no mesmo mês/antes da referência, fator = 1 (sem correção)."""
    s = serie or carregar_ipca()
    mr = str(mes_ref).strip()
    if mr not in s:
        raise ValueError(f"IPCA: mês de referência {mr} fora da série disponível (jan/2014–{max(s)})")
    ultimo = max(s)                        # ordenação lexicográfica de 'AAAA-MM' = cronológica
    fim = _mes_anterior(mes_protocolo)
    if fim > ultimo:                       # §2º: "para o qual o IPCA estiver disponível"
        fim = ultimo
    if fim not in s:
        raise ValueError(f"IPCA: mês-fim {fim} indisponível na série")
    if fim <= mr:                          # protocolo ≤ referência → nada a corrigir
        return Decimal("1"), fim
    return (s[fim] / s[mr]), fim


def _d(x, campo):
    """Parse para Decimal. BR (vírgula decimal) ou decimal puro. REJEITA ponto-milhar ambíguo (igual pcpt.py)."""
    s = str(x).strip()
    if ',' in s:                                   # BR: ponto=milhar, vírgula=decimal
        s2 = s.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(\.\d{3})+', s):    # "1.000"/"15.726" = ponto-milhar SEM decimal → ambíguo
        raise ValueError(f"{campo} ambíguo (ponto como milhar sem vírgula): {x!r} — use vírgula decimal ou ponto decimal sem milhar")
    else:
        s2 = s
    try:
        return Decimal(s2)
    except Exception:
        raise ValueError(f"{campo} inválido: {x!r}")


def _pos(dv, campo):
    if dv <= 0:
        raise ValueError(f"{campo} deve ser > 0 (recebido {dv})")
    return dv


def _camaxcd(via, camaxcd):
    """CAmaxcd + citação. via '125' (sem doação) ⇒ 4 fixo (§1º). via '127' (com doação) ⇒ CAmax real (entrada)."""
    if via == "125":
        if camaxcd is not None and _d(camaxcd, "camaxcd") != CAMAXCD_VIA125:
            raise ValueError("via 125: CAmaxcd é fixo em 4 por força do Art. 128 §1º — não sobreponha")
        return CAMAXCD_VIA125, "Art. 128 §1º (PCpt originado no Art. 125 — sem doação): CAmaxcd = 4"
    if via == "127":
        if camaxcd is None:
            raise ValueError("via 127 (com doação) exige CAmaxcd do imóvel cedente vigente na data de referência (Art. 128 caput)")
        return _pos(_d(camaxcd, "camaxcd"), "camaxcd"), "Art. 128 caput: CAmaxcd do imóvel cedente (data de referência/doação)"
    raise ValueError(f"via inválida: {via!r}; use '125' (sem doação) ou '127' (com doação)")


def corrigir_vtcd_ipca(vtcd, ipca_fator, ipca_fonte=None):
    """Art. 128 §2º — corrige o VTcd pelo IPCA acumulado (mês seguinte ao mês de referência → mês anterior
    ao protocolo da Certidão). O `ipca_fator` (ex.: 1.0873 p/ +8,73%) é ENTRADA — o engine NÃO computa a
    série IBGE (1.3). Devolve (VTcd_corrigido, nota). ipca_fator None ⇒ sem correção (prospecção: sem data
    de referência protocolada, usa o Quadro 14 vigente — §2º N/A)."""
    Vt = _pos(_d(vtcd, "vtcd"), "vtcd")
    if ipca_fator is None:
        return Vt, ("sem correção IPCA — prospecção sem data de referência protocolada: usa o Quadro 14 "
                    "vigente (Art. 125 §2º); §2º do Art. 128 N/A até haver Declaração protocolada")
    f = _pos(_d(ipca_fator, "ipca_fator"), "ipca_fator")
    Vtc = (Vt * f).quantize(Q2, ROUND_HALF_UP)
    nota = f"VTcd × IPCA({f}) = R$ {Vtc}/m² (Art. 128 §2º)" + (f" — fonte: {ipca_fonte}" if ipca_fonte else "")
    return Vtc, nota


def referencia_art128(pcpt, vtcd, via="125", ipca_fator=None, ipca_fonte=None, camaxcd=None,
                      esquina=False, mes_ref=None, mes_protocolo=None):
    """Valor de referência LEGAL do potencial do cedente (Art. 128). Entradas (1.3):
      pcpt   — potencial vendável (m²), saída do pcpt.py / saldo líquido;
      vtcd   — valor do m² do terreno cedente (Quadro 14), R$/m²;
      via    — '125' (sem doação, CAmaxcd=4 §1º) | '127' (com doação, CAmaxcd real);
      mes_ref/mes_protocolo — 'AAAA-MM' da Declaração e do protocolo da Certidão: se ambos vierem (e
        ipca_fator não), o fator do §2º é CALCULADO da série IPCA (tabelas/ipca-numero-indice-ibge.csv);
      ipca_fator — fator IPCA já pronto (§2º) — sobrepõe mes_ref/mes_protocolo; None+sem meses = prospecção;
      esquina — True se o VTcd já é o MAIOR do Quadro 14 da quadra (Decreto 57.536/2016 Art. 3º IV).
    Devolve OS DOIS números (numerador bruto e ÷CAmaxcd), o memorial auditável e a citação."""
    P = _pos(_d(pcpt, "pcpt"), "pcpt")                    # m²
    Vt = _pos(_d(vtcd, "vtcd"), "vtcd")                   # R$/m² (Quadro 14, face)
    ca, ca_disp = _camaxcd(via, camaxcd)
    # §2º — se o chamador deu as datas (e não um fator pronto), calcula o fator da série IPCA.
    if ipca_fator is None and mes_ref and mes_protocolo:
        ipca_fator, mes_fim = fator_ipca(mes_ref, mes_protocolo)
        ipca_fonte = f"{IPCA_FONTE}: índice[{mes_fim}] ÷ índice[{mes_ref}]"
    Vtc, ipca_nota = corrigir_vtcd_ipca(Vt, ipca_fator, ipca_fonte)

    numerador = (P * Vtc).quantize(Q2, ROUND_HALF_UP)     # R$ — Art. 128 caput (numerador)
    referencia = (numerador / ca).quantize(Q2, ROUND_HALF_UP)   # R$ — ÷CAmaxcd (Cr cancela; §1º)

    disp_vtcd = f"Art. 128 caput; valor do {QUADRO14}"
    if esquina:
        disp_vtcd += f"; {DEC_ESQUINA} (maior valor da quadra — lote de esquina)"
    memorial = [
        {"linha": "PCpt — potencial vendável", "valor": f"{P} m²",
         "dispositivo": "Art. 125 (PDE) — entrada (engine pcpt.py: Atc×CAbás×Fi×FSCE)", "fonte": LEI},
        {"linha": "VTcd — valor do m² do terreno cedente", "valor": f"R$ {Vt}/m²",
         "dispositivo": disp_vtcd, "fonte": QUADRO14},
        {"linha": "VTcd corrigido (§2º IPCA)", "valor": f"R$ {Vtc}/m²",
         "dispositivo": "Art. 128 §2º", "fonte": ipca_nota},
        {"linha": "CAmaxcd", "valor": str(ca),
         "dispositivo": ca_disp, "fonte": LEI},
        {"linha": "Numerador = PCpt × VTcd (bruto)", "valor": f"R$ {numerador}",
         "dispositivo": "Art. 128 caput — numerador da equação de PCr", "fonte": LEI},
        {"linha": "Referência = Numerador ÷ CAmaxcd", "valor": f"R$ {referencia}",
         "dispositivo": "Art. 128 §1º — equivale a PCr×Cr; o Cr do receptor CANCELA (independe do comprador)",
         "fonte": LEI},
    ]
    memoria = (f"N = PCpt({P}) × VTcd({Vtc}) = R$ {numerador}  |  "
               f"VR = N ÷ CAmaxcd({ca}) = R$ {referencia}")
    disp = "Art. 128 (PDE), caput e §1º" + ("; §2º (IPCA)" if ipca_fator is not None else "")
    return {
        "via": via, "pcpt_m2": str(P), "vtcd_m2": str(Vt), "vtcd_corrigido_m2": str(Vtc),
        "camaxcd": str(ca), "esquina": bool(esquina),
        "numerador_brl": str(numerador),      # PCpt × VTcd
        "referencia_brl": str(referencia),    # ÷ CAmaxcd (Cr cancela)
        "memoria_calculo": memoria,
        "memorial": memorial,
        "citacao": {"dispositivo": disp, "fonte": LEI},
    }


def referencia_max_art128(pcpt, vtcd_vigente, via="125", camaxcd=None, esquina=False,
                          vtcd_declaracao=None, mes_ref=None, mes_protocolo=None):
    """OP-1b (tese `docs/TESE-VTCD-MAXIMO-ART128.md`) — REFERÊNCIA MÁXIMA rastreável do potencial do cedente:

        referência = MAX( (A) Quadro 14 VIGENTE ;  (B) VTcd da Declaração corrigido por IPCA §2º )

    (A) PISO de prospecção — Quadro 14 vigente (ano-ref 2026, Dec. 64.884/2025); é o que o produto usa hoje.
    (B) TETO §2º — só entra QUANDO há Declaração com valor de terreno (`vtcd_declaracao`) E as datas
        (`mes_ref` da Declaração + `mes_protocolo` da Certidão): VTcd_declaração × fator_ipca(§2º).
    Devolve o MAX, a BASE VENCEDORA (citada) e AMBOS os cenários lado a lado (piso+teto, 1.3 — nunca esconde
    a base perdedora). Sem (B): devolve só (A) — 100% compatível com a prospecção de hoje. O engine NÃO
    adivinha a data-ref nem a série IPCA (1.3): tudo é ENTRADA rastreável. 'O vendedor não deve receber menos
    que o maior valor que a própria lei lhe assegura' (Art. 128 §1º piso + §2º teto)."""
    # (A) — piso: Quadro 14 vigente, sem §2º
    ref_a = referencia_art128(pcpt, vtcd_vigente, via=via, camaxcd=camaxcd, esquina=esquina)
    cenarios = [{
        "base": "A", "rotulo": "Quadro 14 vigente (piso — Art. 125 §2º / Dec. 64.884/2025, ano-ref 2026)",
        "referencia_brl": ref_a["referencia_brl"], "numerador_brl": ref_a["numerador_brl"],
        "vtcd_aplicado_m2": ref_a["vtcd_corrigido_m2"], "detalhe": ref_a,
    }]
    if vtcd_declaracao is not None:
        if not (mes_ref and mes_protocolo):
            raise ValueError("base (B) do MAX exige mes_ref E mes_protocolo (Art. 128 §2º) para corrigir o "
                             "VTcd da Declaração pelo IPCA — sem as datas o §2º não se aplica (só o piso A)")
        ref_b = referencia_art128(pcpt, vtcd_declaracao, via=via, camaxcd=camaxcd, esquina=esquina,
                                  mes_ref=mes_ref, mes_protocolo=mes_protocolo)
        cenarios.append({
            "base": "B", "rotulo": "VTcd da Declaração × IPCA (teto — Art. 128 §2º)",
            "referencia_brl": ref_b["referencia_brl"], "numerador_brl": ref_b["numerador_brl"],
            "vtcd_aplicado_m2": ref_b["vtcd_corrigido_m2"], "detalhe": ref_b,
        })
    vencedora = max(cenarios, key=lambda c: Decimal(c["referencia_brl"]))
    memoria = ("MAX( " + " ; ".join(f"{c['base']}=R$ {c['referencia_brl']}" for c in cenarios)
               + f" ) = R$ {vencedora['referencia_brl']}  (base {vencedora['base']}: {vencedora['rotulo']})")
    disp = ("Art. 128 (PDE) — §1º (piso, Quadro 14 vigente)"
            + (" vs §2º (teto, IPCA); MAX = maior valor assegurado ao cedente" if len(cenarios) > 1
               else "; sem Declaração protocolada, §2º N/A → só o piso"))
    return {
        "referencia_max_brl": vencedora["referencia_brl"],
        "numerador_max_brl": vencedora["numerador_brl"],
        "base_vencedora": vencedora["base"],
        "base_vencedora_rotulo": vencedora["rotulo"],
        "cenarios": [{k: v for k, v in c.items() if k != "detalhe"} for c in cenarios],
        "detalhe": {c["base"]: c["detalhe"] for c in cenarios},
        "memoria_calculo": memoria,
        "citacao": {"dispositivo": disp, "fonte": LEI},
    }


def _autoteste():
    # Constante legal ancorada de forma independente (verbatim §1º): via-125 ⇒ CAmaxcd = 4.
    assert CAMAXCD_VIA125 == Decimal("4")

    # Caso limpo: PCpt=1000 m², VTcd=3000 R$/m² → N=3.000.000; VR=N/4=750.000.
    r = referencia_art128("1000", "3000")
    assert r["numerador_brl"] == "3000000.00", r
    assert r["referencia_brl"] == "750000.00", r
    assert r["camaxcd"] == "4", r
    assert "§1º" in r["memorial"][-1]["dispositivo"], r

    # §2º IPCA: VTcd 3000 × 1,10 = 3300 → N=3.300.000; VR=825.000.
    ri = referencia_art128("1000", "3000", ipca_fator="1.10", ipca_fonte="IBGE/SIDRA 1737")
    assert ri["vtcd_corrigido_m2"] == "3300.00", ri
    assert ri["numerador_brl"] == "3300000.00" and ri["referencia_brl"] == "825000.00", ri
    assert "§2º" in ri["citacao"]["dispositivo"], ri

    # §2º IPCA da TABELA real (IBGE/SIDRA 1737): fator = índice[mês ANTES do protocolo] ÷ índice[mês ref].
    serie = carregar_ipca()
    f, fim = fator_ipca("2020-01", "2026-07", serie=serie)   # protocolo jul/26 → fim jun/26 (disponível)
    assert fim == "2026-06" and f == serie["2026-06"] / serie["2020-01"], (f, fim)
    f2, fim2 = fator_ipca("2020-01", "2030-01", serie=serie)  # protocolo à frente → clampa ao último disponível
    assert fim2 == max(serie), fim2
    f3, _ = fator_ipca("2025-06", "2025-06", serie=serie)     # protocolo ≤ referência → sem correção (fator 1)
    assert f3 == Decimal("1"), f3
    rd = referencia_art128("1000", "3000", mes_ref="2020-01", mes_protocolo="2026-07")  # datas → fator sozinho
    vtc_esp = (Decimal("3000") * (serie["2026-06"] / serie["2020-01"])).quantize(Q2, ROUND_HALF_UP)
    assert rd["vtcd_corrigido_m2"] == str(vtc_esp), rd
    try:                                                       # mês de referência fora da série → fail-closed
        fator_ipca("2010-01", "2020-01", serie=serie); raise AssertionError("deveria rejeitar mês fora da série")
    except ValueError:
        pass

    # via 127 (com doação): CAmaxcd real (=2) entra na conta; N igual, VR=N/2.
    r7 = referencia_art128("1000", "3000", via="127", camaxcd="2")
    assert r7["referencia_brl"] == "1500000.00", r7

    # regra da esquina anotada na citação do VTcd
    re_ = referencia_art128("1000", "3000", esquina=True)
    assert "57.536/2016" in re_["memorial"][1]["dispositivo"], re_

    # Decimal exato + parse BR (VTcd "2.819,20" = 2819,20): 717,60 × 2819,20 = 2.023.057,92; /4 = 505.764,48
    rb = referencia_art128("717,60", "2.819,20")
    assert rb["numerador_brl"] == "2023057.92", rb
    assert rb["referencia_brl"] == "505764.48", rb

    # rejeições (fail-closed)
    casos_ruins = [
        {"pcpt": "0", "vtcd": "3000"},           # PCpt <= 0
        {"pcpt": "1000", "vtcd": "-1"},          # VTcd <= 0
        {"pcpt": "1000", "vtcd": "3000", "via": "999"},        # via inválida
        {"pcpt": "1000", "vtcd": "3000", "via": "127"},        # via 127 sem CAmaxcd
        {"pcpt": "1000", "vtcd": "3000", "via": "125", "camaxcd": "3"},  # via 125 não aceita CAmaxcd≠4
        {"pcpt": "1.000", "vtcd": "3000"},       # ponto-milhar ambíguo
    ]
    for bad in casos_ruins:
        try:
            referencia_art128(**bad); raise AssertionError(f"deveria rejeitar {bad}")
        except ValueError:
            pass

    # ── OP-1b: MAX(A vigente ; B Declaração×IPCA §2º) ──────────────────────────────────────────────
    serie = carregar_ipca()
    # (i) sem base B → só o piso A (compatível com a prospecção de hoje).
    m_soA = referencia_max_art128("1000", "3000")
    assert m_soA["base_vencedora"] == "A" and m_soA["referencia_max_brl"] == "750000.00", m_soA
    assert len(m_soA["cenarios"]) == 1, m_soA
    # (ii) base B VENCE: VTcd_decl 2000 corrigido de jan/2014 (fator ~1,93) supera o piso vigente 3000.
    fB, _ = fator_ipca("2014-01", "2026-07", serie=serie)
    refB_esp = ((Decimal("1000") * (Decimal("2000") * fB).quantize(Q2, ROUND_HALF_UP)) / CAMAXCD_VIA125).quantize(Q2, ROUND_HALF_UP)
    refA_esp = Decimal("750000.00")
    mB = referencia_max_art128("1000", "3000", vtcd_declaracao="2000", mes_ref="2014-01", mes_protocolo="2026-07")
    assert refB_esp > refA_esp, (refB_esp, refA_esp)                          # sanidade do fixture
    assert mB["base_vencedora"] == "B", mB
    assert mB["referencia_max_brl"] == str(refB_esp), (mB["referencia_max_brl"], refB_esp)
    assert len(mB["cenarios"]) == 2 and mB["cenarios"][0]["referencia_brl"] == "750000.00", mB
    # (iii) base A VENCE: VTcd_decl 1000 (baixo) mesmo corrigido não alcança o piso vigente 3000.
    mA = referencia_max_art128("1000", "3000", vtcd_declaracao="1000", mes_ref="2014-01", mes_protocolo="2026-07")
    assert mA["base_vencedora"] == "A" and mA["referencia_max_brl"] == "750000.00", mA
    # (iv) base B sem as datas → fail-closed (§2º exige mes_ref+mes_protocolo).
    try:
        referencia_max_art128("1000", "3000", vtcd_declaracao="2000"); raise AssertionError("deveria exigir datas p/ B")
    except ValueError:
        pass

    # ── Reajuste do Quadro 14 (base 2014 → VTcd vigente): fatores + PROVA DE BATER O PONTO ────────────
    assert fator_reajuste_q14(2014)[0] == Decimal("1.00"), fator_reajuste_q14(2014)
    assert fator_reajuste_q14(2019)[0] == Decimal("1.00"), "até 2019 é a base 2014"      # antes do 1º reajuste
    assert fator_reajuste_q14(2020)[0] == Decimal("1.0200"), fator_reajuste_q14(2020)    # Dec. 59.166/2019 +2%
    assert fator_reajuste_q14(2022)[0] == Decimal("1.0200"), "2021/2022 seguem no +2% (sem reajuste)"
    assert fator_reajuste_q14(2023)[0] == Decimal("1.071000"), fator_reajuste_q14(2023)  # +5% (62.135/2022)
    assert fator_reajuste_q14(2024)[0] == Decimal("1.12455000"), fator_reajuste_q14(2024)  # +5% (63.108/2023)
    assert fator_reajuste_q14(2025)[0] == Decimal("1.17515475000"), fator_reajuste_q14(2025)  # +4,5% (63.999/2024)
    assert fator_reajuste_q14(2026)[0] == Decimal("1.259530861050000"), fator_reajuste_q14(2026)  # +7,18% (64.884/2025)
    assert fator_reajuste_q14(None)[0] == fator_reajuste_q14(2026)[0], "None ⇒ vintage mais recente"
    # PROVA: base 2014 do SQL 001003/codlog 038121 = R$ 3.106,00 → vigente 2024 = R$ 3.492,85, IGUAL ao
    #        valor nominal publicado na Portaria SMUL nº 19/2024 (Anexo I, mesmo SQL/codlog). Auditoria fechada.
    v24 = vtcd_vigente("3106,00", 2024)
    assert v24["vtcd_vigente_m2"] == "3492.85", v24
    # e o vigente mais recente (2026) sobre a mesma base:
    v26 = vtcd_vigente("3106,00")
    assert v26["vtcd_vigente_m2"] == str((Decimal("3106.00") * Decimal("1.259530861050000")).quantize(Q2, ROUND_HALF_UP)), v26
    # vtcd_na_data (§2º VTcd histórico): conhecendo o vigente de 2024 (R$ 3.492,85), o de 2026 sai EXATO
    #  e igual ao vigente 2026 sobre a mesma base (round-trip pela razão de reajuste uniforme).
    conv = vtcd_na_data("3492,85", 2024, 2026)
    assert conv["vtcd_alvo_m2"] == v26["vtcd_vigente_m2"], (conv, v26)
    # e a volta (2026 → 2024) reconstrói o de 2024:
    volta = vtcd_na_data(v26["vtcd_vigente_m2"], 2026, 2024)
    assert volta["vtcd_alvo_m2"] == "3492.85", volta
    return r, ri


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.parse_args()
    r, ri = _autoteste()
    print("AUTO-TESTE art128: OK (gate verde — numerador, ÷CAmaxcd, §1º=4, §2º IPCA, via 127, parse BR, rejeições)\n")

    # Exemplo trabalhado end-to-end: parte de um cedente real (via pcpt.py) e chega ao valor de referência.
    print("Exemplo trabalhado (cedente ZEPEC-BIR, Setor Central — via Art. 125, sem doação):")
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import pcpt
        p = pcpt.pcpt_sem_doacao("299", "1.0", setor_central=True)   # gab.006: 299×1×1,2×2 = 717,60 m²
        pcpt_m2 = p["valor_m2"]
        print(f"  1) {p['memoria_calculo']}   [{p['citacao']['dispositivo']}]")
    except Exception as e:
        pcpt_m2 = "717.60"
        print(f"  1) PCpt = 717,60 m² (pcpt.py indisponível no demo: {e})")
    ref = referencia_art128(str(pcpt_m2), "2819,20", esquina=False)
    print(f"  2) VTcd = R$ 2.819,20/m² (Quadro 14, face da quadra)")
    print(f"  3) {ref['memoria_calculo']}")
    print("\n  Memorial auditável (cada linha → dispositivo → fonte):")
    for ln in ref["memorial"]:
        print(f"     • {ln['linha']:38} {ln['valor']:>18}   [{ln['dispositivo']}]")
    print(f"\n  → Referência que INDEPENDE do comprador (Cr cancela): R$ {ref['referencia_brl']}")
    print(f"  → Numerador bruto (potencial × terreno):              R$ {ref['numerador_brl']}")
    print("  (Preço LEGAL de referência — a MARGEM é do usuário; este engine não define preço de venda.)")

    print("\n  Variante JÁ-DECLARADO (§2º IPCA — Declaração de jan/2020, Certidão protocolada em jul/2026):")
    refi = referencia_art128(str(pcpt_m2), "2819,20", mes_ref="2020-01", mes_protocolo="2026-07")
    print(f"     VTcd corrigido: R$ 2.819,20 → R$ {refi['vtcd_corrigido_m2']}/m²  (IPCA índice jun/26 ÷ jan/20, IBGE/SIDRA 1737)")
    print(f"     Referência (÷4): R$ {refi['referencia_brl']}    |    Numerador: R$ {refi['numerador_brl']}")

    print("\n  OP-1b — REFERÊNCIA MÁXIMA = MAX(A piso vigente ; B Declaração×IPCA §2º), cada base citada:")
    mx = referencia_max_art128(str(pcpt_m2), "2819,20", vtcd_declaracao="1500,00",
                               mes_ref="2014-01", mes_protocolo="2026-07")
    for c in mx["cenarios"]:
        marca = "◄ VENCE" if c["base"] == mx["base_vencedora"] else "        "
        print(f"     ({c['base']}) VTcd aplicado R$ {c['vtcd_aplicado_m2']:>10}/m² → referência R$ {c['referencia_brl']:>14}  {marca}  [{c['rotulo']}]")
    print(f"     → {mx['memoria_calculo']}")
    print(f"       [{mx['citacao']['dispositivo']}]")
