#!/usr/bin/env python3
"""
pcpt.py — Engine determinístico do POTENCIAL CONSTRUTIVO PASSÍVEL DE TRANSFERÊNCIA (lado CEDENTE).

Complementa oodc.py (lado receptor). Modela as DUAS vias de geração de TDC (achado do agente legal
2026-06-28: a via de doação estava fora do modelo):

  • SEM doação (Art. 125, Lei 16.050/2014): PCpt = Atc × CAbas × Fi, com Fi ESCALONADO pela ÁREA do
    lote (LPUOS Lei 16.402/2016, Art. 24, I–VII: 1,2 / 1,0 / 0,9 / 0,7 / 0,5 / 0,2 / 0,1) — NÃO é fixo
    em 1 (correção 2026-07-02; a doutrina "Fi=1,0 estático" era stale — ver auditoria A-02 2026-07-05).
    O proprietário MANTÉM o imóvel (caso ZEPEC-BIR/ZEPAM, Art. 124 I–II).

  • COM doação (Art. 126/127): PCpt = Atc × CAmax × Fi(finalidade).
    O proprietário DOA o imóvel à PMSP (Art. 126: corredor/HIS/regularização/parque) e recebe potencial.
    Usa o coef. MÁXIMO e Fi até 2,0.

ATENÇÃO (universo): a via de doação atende um PÚBLICO DISJUNTO da lista ZEPEC — são doadores de
terreno comum (parques do Quadro 7, corredores, HIS/ZEIS), NÃO os tombados da nossa lista de cedentes.
Não confundir os dois universos.

Datas (entrada datada): CAbas/CAmax/V valem na DATA DE REFERÊNCIA — protocolo (Art. 125 §2º) na via
sem doação; data da doação (Art. 127 §3º) na via com doação. Renovação ZEPAM congela V antigo (Art.123 §5º).
O engine recebe esses valores como entrada (1.3 — não os inventa nem assume "hoje").

Princípios (iguais ao oodc.py):
- 1.3 — número E escolha de fator nascem AQUI; Atc/CAbas/CAmax/V são ENTRADAS; engine não inventa.
- 1.7 — cada resultado carrega `citacao` do dispositivo.
- DECIMAL exato (Decimal), nunca float, no valor em m². Entrada ambígua é REJEITADA, não adivinhada.

Fatores de incentivo à doação (Art. 127 §1º, incisos I–V; finalidades do Art. 126):
  I  corredores de ônibus ............ 2,0
  II HIS ............................. 1,9
  III regularização fundiária ........ 0,8
  IV parque (V ≤ R$2.000/m²) ......... 1,4   (Redação Lei 17.975/2023)
  V  parque (V > R$2.000/m²) ......... 1,0   — resolvido DENTRO do engine a partir de V.

LIMITE (Art. 124 §3º, por remissão Art.124 §5º): PCpt acima de 50.000 m² é transferido em 10 parcelas
anuais → o engine sinaliza `estoque_a_vista` vs `excedente_parcelado` (estoque não disponível à vista).

Uso:
    python3 engines/tdc/pcpt.py --demo     # exemplo trabalhado + auto-teste (gate)
PU 14 · 2026-06-28.
"""
import sys, re, csv, argparse
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

LEI = "Lei Municipal SP nº 16.050/2014 (PDE)"
Q2 = Decimal("0.01")
LIMITE_PARCELAMENTO = Decimal("50000")   # Art. 124 §3º

# ★ AUD-A01 (2026-07-05): os fatores NÃO moram mais hardcoded aqui — são LIDOS de `tabelas/*.csv`
# (doutrina 1.1: tabela de lei é DADO extraído e é INPUT do engine; o engine não duplica a tabela).
# Falha ALTO se o CSV sumir/corromper (1.3 fail-closed). O _autoteste ancora os valores LEGAIS
# (verbatim Art. 24 / Art. 127) de forma independente: sabotar o CSV ⇒ o gate FALHA.
TABELAS = Path(__file__).resolve().parents[2] / "tabelas"

def _linhas_csv(nome):
    p = TABELAS / nome
    if not p.exists():
        raise FileNotFoundError(f"tabela obrigatória ausente: {p} (1.1 — o engine lê a tabela, não a inventa)")
    with open(p, encoding="utf-8") as f:
        rows = [r for r in csv.reader(f) if r and not r[0].lstrip().startswith("#")]
    if len(rows) < 2:
        raise ValueError(f"tabela vazia/corrompida: {p}")
    hdr = rows[0]
    return [dict(zip(hdr, r)) for r in rows[1:]]

def _carrega_fi_doacao():
    """Art. 127 §1º I–V ← tabelas/fi-incentivo-doacao.csv. Devolve (FI_DOACAO, fi_parque_ate, fi_parque_acima)."""
    doacao, p_ate, p_acima = {}, None, None
    for r in _linhas_csv("fi-incentivo-doacao.csv"):
        fin = r["finalidade"].strip()
        fi = Decimal(r["fi"].strip())
        # normaliza o inciso p/ o formato de citação do engine ("Art. 127 §1º, I")
        inciso = re.sub(r"(§1º) (I|II|III|IV|V)$", r"\1, \2", r["inciso"].strip())
        if fin == "parque_v_ate_2000":     p_ate = (fi, inciso)
        elif fin == "parque_v_acima_2000": p_acima = (fi, inciso)
        else:                              doacao[fin] = (fi, inciso)
    if not doacao or p_ate is None or p_acima is None:
        raise ValueError("fi-incentivo-doacao.csv incompleto (faltam finalidades ou faixas de parque)")
    return doacao, p_ate, p_acima

def _carrega_limiar_parque():
    """Art. 127 §1º IV/V — limiar do valor de terreno (Quadro 14) por VINTAGE ← tabelas/limiar-parque-art127.csv.
    Devolve {ano_ref:int -> (limiar:Decimal, fonte, dispositivo)} (1.1/1.3 — o número nasce da tabela, com vigência 1.6)."""
    tab = {}
    for r in _linhas_csv("limiar-parque-art127.csv"):
        tab[int(r["ano_ref"].strip())] = (Decimal(r["limiar_rs_m2"].strip()), r["fonte"].strip(), r["dispositivo"].strip())
    if not tab:
        raise ValueError("limiar-parque-art127.csv sem linhas úteis")
    return tab

def limiar_parque(ano_ref=None):
    """Limiar vigente do Art. 127 §1º IV/V para a vintage pedida (default = a MAIS RECENTE, hoje 2026 =
    R$ 2.352,06/m², Dec. 64.884/2025 Art. 3º). Compare V e limiar na MESMA vintage (1.6)."""
    tab = _LIMIAR_PARQUE
    ano = max(tab) if ano_ref is None else int(ano_ref)
    if ano not in tab:
        raise ValueError(f"limiar do parque para ano-ref {ano} ausente na tabela (vintages: {sorted(tab)})")
    return tab[ano]

def _carrega_fi_zepec():
    """LPUOS Art. 24 I–VII (Fi escalonado pela área do lote) ← tabelas/fi-zepec-area-lpuos.csv.
    Faixas: 'ate X' / 'A a B' (teto=B) / 'acima de X' (teto=None). Limite superior INCLUSIVO."""
    faixas = []
    for r in _linhas_csv("fi-zepec-area-lpuos.csv"):
        fx = r["faixa_area_lote_m2"].strip().lower()
        fi = Decimal(r["fi"].strip())
        inciso = re.sub(r"^(Art\. 24) (I|II|III|IV|V|VI|VII)$", r"\1, \2", r["inciso"].strip())
        if fx.startswith("acima"):
            teto = None
        else:
            m = re.findall(r"\d+", fx)
            if not m: raise ValueError(f"faixa ilegível na tabela Fi ZEPEC: {fx!r}")
            teto = Decimal(m[-1])
        faixas.append((teto, fi, inciso))
    faixas.sort(key=lambda t: (t[0] is None, t[0] or 0))
    if len(faixas) != 7 or faixas[-1][0] is not None:
        raise ValueError(f"fi-zepec-area-lpuos.csv inválido: esperadas 7 faixas Art. 24 I–VII com última aberta (veio {len(faixas)})")
    return faixas

LEI_LPUOS = "Lei Municipal SP nº 16.402/2016 (LPUOS)"
LEI_SCE = "Lei Municipal SP nº 17.844/2022, Art. 57 (AIU-SCE / Setor Central)"
FSCE_SCE = Decimal("2.0")            # Art. 57, Lei 17.844/2022: fator setor central
FSCE_TETO_TERRENO = Decimal("1000")  # Art. 57: só ZEPEC-BIR com terreno ≤ 1.000 m²
FI_DOACAO, _FI_PARQUE_ATE, _FI_PARQUE_ACIMA = _carrega_fi_doacao()   # Art. 127 §1º (tabela extraída)
_LIMIAR_PARQUE = _carrega_limiar_parque()                            # Art. 127 §1º IV/V — limiar por vintage (Dec. 64.884/2025)
FI_ZEPEC_ART24 = _carrega_fi_zepec()                                 # LPUOS Art. 24 I–VII (tabela extraída)

def fi_zepec_por_area(atc):
    """Fi da via sem-doação p/ NOVAS declarações ZEPEC, escalonado pela área do lote
    (LPUOS Art. 24, I–VII). Devolve (Fi, inciso). O engine escolhe o fator (1.3)."""
    A = _pos(_d(atc, "atc"), "atc")
    for teto, fi, inciso in FI_ZEPEC_ART24:
        if teto is None or A <= teto:
            return fi, inciso
    raise AssertionError("faixa Art. 24 não resolvida")  # inalcançável

def _d(x, campo):
    """Parse para Decimal. BR (vírgula decimal) ou decimal puro. REJEITA ponto-milhar ambíguo."""
    s = str(x).strip()
    if ',' in s:                                   # BR: ponto=milhar, vírgula=decimal
        s2 = s.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(\.\d{3})+', s):    # ex.: "1.000" / "15.726" = ponto-milhar SEM decimal
        raise ValueError(f"{campo} ambíguo (ponto como milhar sem vírgula): {x!r} — use vírgula decimal ou ponto decimal sem milhar")
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

def _estoque(pcpt):
    """Art. 124 §3º: acima de 50.000 m² o excedente sai em 10 parcelas anuais."""
    if pcpt <= LIMITE_PARCELAMENTO:
        return {"estoque_a_vista_m2": pcpt, "excedente_parcelado_m2": Decimal("0.00"), "parcelas_anuais": 0}
    exc = (pcpt - LIMITE_PARCELAMENTO).quantize(Q2)
    return {"estoque_a_vista_m2": LIMITE_PARCELAMENTO, "excedente_parcelado_m2": exc, "parcelas_anuais": 10,
            "obs_estoque": "Art. 124 §3º — excedente de 50.000 m² em 10 parcelas anuais"}

def pcpt_sem_doacao(atc, cabas, fi=None, setor_central=False):
    """Art. 125 (PDE): PCpt = Atc × CAbas × Fi. O dono mantém o imóvel.
    Fi: por PADRÃO é resolvido AQUI pelo Art. 24 da LPUOS (escalonado pela área do lote,
    caso das NOVAS declarações ZEPEC — correção 2026-07-02; antes usava 1 fixo, ERRADO).
    `fi` explícito sobrepõe (ex.: declaração antiga emitida sob outro fator — informar o da certidão).

    setor_central: quando o cedente é ZEPEC-BIR DENTRO da AIU-SCE (Setor Central) E terreno ≤ 1.000 m²,
      aplica o FATOR SETOR CENTRAL FSCE = 2,0 (Art. 57, Lei 17.844/2022): PCpt = Atc × CAbas × Fi × FSCE.
      A PERTINÊNCIA à AIU-SCE é ENTRADA (número/gate nasce fora do LLM, 1.3) — quem chama informa (True/False)
      a partir da camada perímetro AIU-SCE (GeoSampa). Se setor_central=True mas terreno>1.000 m², o FSCE
      NÃO se aplica (fora do escopo do Art. 57) e o cálculo permanece Atc×CAbas×Fi, com nota."""
    A = _pos(_d(atc, "atc"), "atc"); C = _pos(_d(cabas, "cabas"), "cabas")
    if fi is None:
        F, inciso = fi_zepec_por_area(A)
        disp = f"Art. 125 (PDE) c/c LPUOS {inciso}"
        fonte = f"{LEI}; {LEI_LPUOS}"
    else:
        F = _pos(_d(fi, "fi"), "fi")
        disp, fonte = "Art. 125 (PDE); Fi informado pelo chamador", LEI
    fsce = Decimal("1")
    if setor_central:
        if A <= FSCE_TETO_TERRENO:
            fsce = FSCE_SCE
            disp += " × FSCE (Art. 57, Lei 17.844/2022 — AIU-SCE)"
            fonte += f"; {LEI_SCE}"
        else:
            disp += " (AIU-SCE porém terreno>1.000 m²: FSCE NÃO aplicável — Art. 57)"
    pcpt = (A * C * F * fsce).quantize(Q2, ROUND_HALF_UP)
    memoria = f"PCpt = Atc({A}) × CAbas({C}) × Fi({F})" + (f" × FSCE({fsce})" if fsce != 1 else "") + f" = {pcpt} m²"
    return {"via": "sem_doacao", "valor_m2": pcpt, "fi": str(F), "fsce": str(fsce),
            "memoria_calculo": memoria,
            "citacao": {"dispositivo": disp, "fonte": fonte}, **_estoque(pcpt)}

def pcpt_com_doacao(atc, camax, finalidade, v=None, ano_ref=None):
    """Art. 126/127: PCpt = Atc × CAmax × Fi(finalidade). O dono DOA o imóvel.
    finalidade ∈ {corredor_onibus, his, regularizacao_fundiaria, parque}. Para 'parque', V é obrigatório
    e o fator (1,4 se V≤limiar / 1,0 se V>limiar) é resolvido AQUI (1.3), não pelo chamador. O LIMIAR é
    vintage-aware (Art. 127 §1º IV/V): default = o mais recente (2026 = R$ 2.352,06/m², Dec. 64.884/2025);
    passe `ano_ref` para comparar V com o limiar da MESMA vintage (1.6 — ex.: V do Quadro 14 2026 ⇒ limiar 2026)."""
    A = _pos(_d(atc, "atc"), "atc"); C = _pos(_d(camax, "camax"), "camax")
    if finalidade == "parque":
        if v is None:
            raise ValueError("finalidade 'parque' exige V (valor do terreno, Quadro 14) para escolher o Fi (Art.127 §1º IV/V)")
        V = _pos(_d(v, "v"), "v")
        limiar, limiar_fonte, _ = limiar_parque(ano_ref)
        F, inc = _FI_PARQUE_ATE if V <= limiar else _FI_PARQUE_ACIMA   # da tabela (AUD-A01); limiar vintage (OP-1c)
        disp = f"{inc} (Lei 17.975/2023; limiar R$ {limiar}/m² — {limiar_fonte})"
    elif finalidade in FI_DOACAO:
        F, disp = FI_DOACAO[finalidade]
    else:
        raise ValueError(f"finalidade inválida: {finalidade!r}; use {list(FI_DOACAO)+['parque']}")
    pcpt = (A * C * F).quantize(Q2, ROUND_HALF_UP)
    return {"via": "com_doacao", "finalidade": finalidade, "valor_m2": pcpt,
            "memoria_calculo": f"PCpt = Atc({A}) × CAmax({C}) × Fi({F}) = {pcpt} m²",
            "citacao": {"dispositivo": f"Art. 126/127 e {disp}", "fonte": LEI}, **_estoque(pcpt)}

def _autoteste():
    atc, cabas, camax = "1000", "1.0", "4.0"
    s = pcpt_sem_doacao(atc, cabas);                       assert s["valor_m2"] == Decimal("1000.00"), s  # faixa II Fi=1,0
    d = pcpt_com_doacao(atc, camax, "his");                assert d["valor_m2"] == Decimal("7600.00"), d
    d2 = pcpt_com_doacao(atc, camax, "corredor_onibus");   assert d2["valor_m2"] == Decimal("8000.00"), d2
    reg = pcpt_com_doacao(atc, camax, "regularizacao_fundiaria"); assert reg["valor_m2"] == Decimal("3200.00"), reg  # Fi<1
    pba = pcpt_com_doacao(atc, camax, "parque", v="1500"); assert pba["valor_m2"] == Decimal("5600.00"), pba          # Fi 1,4
    pal = pcpt_com_doacao(atc, camax, "parque", v="3000"); assert pal["valor_m2"] == Decimal("4000.00"), pal          # Fi 1,0
    # ★ OP-1c — LIMIAR do parque é VINTAGE-AWARE (Art. 127 §1º IV/V; Dec. 64.884/2025 Art. 3º):
    #   2026 = R$ 2.352,06/m² (default); 2014 = R$ 2.000/m². Da TABELA (limiar-parque-art127.csv), não hardcoded.
    assert limiar_parque()[0] == Decimal("2352.06"), limiar_parque()          # default = mais recente (2026)
    assert limiar_parque(2026)[0] == Decimal("2352.06")
    assert limiar_parque(2025)[0] == Decimal("2194.50")   # Decreto 63.999/2024 Art. 3º (ganho do garimpo Drive PU 19)
    assert limiar_parque(2014)[0] == Decimal("2000.00")
    #   V=2200 (entre R$ 2.000 e R$ 2.352,06): a vintage DECIDE o Fi — 2026 ⇒ 1,4 (V≤limiar); 2014 ⇒ 1,0 (V>limiar).
    pv26 = pcpt_com_doacao(atc, camax, "parque", v="2200")               # default 2026
    assert pv26["valor_m2"] == Decimal("5600.00"), pv26                  # Fi 1,4 (2200 ≤ 2352,06)
    pv14 = pcpt_com_doacao(atc, camax, "parque", v="2200", ano_ref=2014) # vintage 2014
    assert pv14["valor_m2"] == Decimal("4000.00"), pv14                  # Fi 1,0 (2200 > 2000)
    assert "2352.06" in pv26["citacao"]["dispositivo"], pv26            # cita o limiar aplicado (1.7)
    try:
        limiar_parque(1999); raise AssertionError("vintage inexistente deveria levantar")  # fail-closed
    except ValueError:
        pass
    # ★ Fi ESCALONADO (LPUOS Art. 24, correção 2026-07-02) — uma prova por faixa/borda:
    assert pcpt_sem_doacao("400", "1.0")["valor_m2"] == Decimal("480.00")        # I: ≤500 → 1,2
    assert pcpt_sem_doacao("500", "1.0")["valor_m2"] == Decimal("600.00")        # borda: 500 é "até 500" → 1,2
    assert pcpt_sem_doacao("501", "1.0")["valor_m2"] == Decimal("501.00")        # II: 1,0
    assert pcpt_sem_doacao("3000", "1.0")["valor_m2"] == Decimal("2700.00")      # III: 0,9
    assert pcpt_sem_doacao("8000", "1.0")["valor_m2"] == Decimal("5600.00")      # IV: 0,7
    assert pcpt_sem_doacao("15000", "1.0")["valor_m2"] == Decimal("7500.00")     # V: 0,5
    assert pcpt_sem_doacao("30000", "1.0")["valor_m2"] == Decimal("6000.00")     # VI: 0,2
    assert pcpt_sem_doacao("444030", "1.0")["valor_m2"] == Decimal("44403.00")   # VII: 0,1 (caso real Philipe Pinel)
    s24 = pcpt_sem_doacao("444030", "1.0"); assert "Art. 24, VII" in s24["citacao"]["dispositivo"], s24  # cita o inciso
    # `fi` explícito sobrepõe (declaração antiga com fator da certidão)
    assert pcpt_sem_doacao("444030", "1.0", fi="1")["valor_m2"] == Decimal("444030.00")
    # Decimal exato (3333.33 → faixa III, Fi=0,9)
    assert pcpt_sem_doacao("3333.33", "0.1")["valor_m2"] == Decimal("300.00")
    # parse BR (520,59 > 500 → faixa II, Fi=1,0)
    assert pcpt_sem_doacao("520,59", "1,0")["valor_m2"] == Decimal("520.59")
    # ★ FSCE — Setor Central (Art. 57, Lei 17.844/2022): PCpt = Atc × CAbas × Fi × 2,0 (terreno ≤ 1.000 m²).
    #   Ancorado em 4 Declarações oficiais (Diário Oficial 2026-07-08). CAbas=1 (ZC/ZM, Quadro 3).
    assert pcpt_sem_doacao("299", "1.0", setor_central=True)["valor_m2"] == Decimal("717.60")   # 299×1×1,2×2 (gab.006)
    assert pcpt_sem_doacao("734", "1.0", setor_central=True)["valor_m2"] == Decimal("1468.00")  # 734×1×1,0×2
    assert pcpt_sem_doacao("490", "1.0", setor_central=True)["valor_m2"] == Decimal("1176.00")  # 490×1×1,2×2
    assert pcpt_sem_doacao("320", "1.0", setor_central=True)["valor_m2"] == Decimal("768.00")   # 320×1×1,2×2 (ZM)
    fsce = pcpt_sem_doacao("299", "1.0", setor_central=True); assert "Art. 57" in fsce["citacao"]["dispositivo"], fsce
    # ESCOPO: terreno > 1.000 m² na AIU-SCE NÃO recebe FSCE (Art. 57 exige ≤ 1.000) — fica Atc×CAbas×Fi
    assert pcpt_sem_doacao("1345", "1.0", setor_central=True)["valor_m2"] == Decimal("1345.00") # 1345>1000 → sem FSCE
    # fora da AIU-SCE (padrão) segue sem FSCE
    assert pcpt_sem_doacao("299", "1.0")["valor_m2"] == Decimal("358.80")                        # 299×1×1,2 (sem FSCE)
    # >50.000 m² -> parcelamento (Art.124 §3º): 20000 × 4 × 2 = 160000
    big = pcpt_com_doacao("20000", "4.0", "corredor_onibus")
    assert big["estoque_a_vista_m2"] == Decimal("50000") and big["excedente_parcelado_m2"] == Decimal("110000.00"), big
    # rejeições
    for bad in [("1.000","1.0"), ("-50","1.0"), ("1000","0")]:
        try: pcpt_sem_doacao(*bad); raise AssertionError(f"deveria rejeitar {bad}")
        except ValueError: pass
    try: pcpt_com_doacao(atc, camax, "parque"); raise AssertionError("parque sem V deveria falhar")
    except ValueError: pass
    try: pcpt_com_doacao(atc, camax, "xpto"); raise AssertionError("finalidade invalida deveria falhar")
    except ValueError: pass
    return s, d, d2, pba

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--demo", action="store_true"); ap.parse_args()
    s, d, d2, pba = _autoteste()
    print("AUTO-TESTE: OK (gate verde — inclui parque, Fi<1, parse BR, >50k parcelado, rejeições)\n")
    print("Exemplo (Atc=1000 m², CAbas=1,0, CAmax=4,0):")
    print(f"  SEM doação (Art.125):           {s['memoria_calculo']}")
    print(f"  COM doação HIS (Art.127):       {d['memoria_calculo']}")
    print(f"  COM doação corredor (Art.127):  {d2['memoria_calculo']}")
    print(f"  COM doação parque V=1500 (≤2k): {pba['memoria_calculo']}")
    print(f"\n  -> via de doação gera até {d2['valor_m2']/s['valor_m2']:.0f}× mais potencial (mas o dono PERDE o imóvel).")
    print("\nFatores de incentivo (Art. 127 §1º):")
    for k,(fi,disp) in FI_DOACAO.items(): print(f"  {k:26} Fi={fi}  [{disp}]")
    print(f"  {'parque':26} Fi=1,4 se V≤R$2.000 senão 1,0  [Art.127 §1º IV/V]")
