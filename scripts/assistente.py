#!/usr/bin/env python3
"""
assistente.py — ORQUESTRADOR do produto (CLAUDE.md Parte 4): resposta única que amarra
NÚMERO (nasce no engine, 1.3) + CITAÇÃO (obrigatória, 1.7), sem o LLM inventar nada.

O que faz (determinístico; a PROSA final fica com o LLM roteador, amarrado a este esqueleto):
  1. SEMPRE roda o RAG (`consultar.py`) → dispositivo(s) verbatim que FUNDAMENTAM a resposta (1.7).
     Sem dispositivo que fundamente → NÃO-FUNDAMENTADA (o RAG nunca responde sem citar).
  2. Se a pergunta é de VALOR (preço/referência/quanto vale) E há contexto do cedente (saldo + VTcd),
     roteia ao ENGINE `art128` → o número nasce AQUI, rastreável ao Art. 128 (1.3), com memorial e o
     par piso×teto (OP-1b). O número JAMAIS vem do LLM nem de arquivo derivado (1.8) — vem do engine
     alimentado pela FONTE PRIMÁRIA (`--sql` lê o cedente de zepec/ferramenta/zepec_cedentes_oficial.csv).
  3. Monta a resposta estruturada: {tipo, numero, citacoes, veredito}. Regra de ouro (Parte 4):
     Gen Matemática é a única fonte de número; Gen RAG nunca responde sem citação.

Uso:
  python3 scripts/assistente.py "o que condiciona a certidão de transferência do ZEPEC-BIR?"
  python3 scripts/assistente.py --sql 0010800016 "quanto vale o potencial transferível deste imóvel?"
  python3 scripts/assistente.py --json "..."
  python3 scripts/assistente.py --autoteste
PU · 2026-07-17 (orquestrador — fecha o elo número+citação do produto).
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "engines" / "tdc"))
import consultar as _rag          # noqa: E402
import art128                     # noqa: E402

CED_OFICIAL = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes_oficial.csv"

# intenção de VALOR: a pergunta pede um número monetário/de potencial (roteia ao engine).
_VALOR_RX = re.compile(
    r"\b(valor|pre[çc]o|quanto\s+vale|quanto\s+custa|refer[êe]ncia|r\$|reais|"
    r"potencial\s+(construtivo|transfer[íi]vel)|vtcd|precifica|avalia[çc])\b", re.I)


def _e_pergunta_de_valor(pergunta):
    return bool(_VALOR_RX.search(pergunta or ""))


def _cedente_por_sql(sql):
    """Lê o cedente da FONTE PRIMÁRIA (não do derivado, 1.8): saldo + VTcd (Quadro 14) + esquina + datas."""
    alvo = re.sub(r"\D", "", str(sql or ""))[:10]
    if not alvo or not CED_OFICIAL.exists():
        return None
    for r in csv.DictReader(open(CED_OFICIAL, encoding="utf-8")):
        if re.sub(r"\D", "", (r.get("sql_mestre") or ""))[:10] == alvo:
            return r
    return None


def _numero_art128(ced):
    """Roteia ao engine (1.3): o número nasce aqui, com memorial e par piso×teto (OP-1b). None se
    faltar saldo/VTcd (não se inventa — devolve pendência explícita)."""
    def d(x):
        try:
            return art128._d(x, "x")
        except Exception:
            return None
    saldo = d(ced.get("saldo_pcpt_m2"))
    vtcd = d(ced.get("v_outorga_m2_q14"))
    if not saldo or saldo <= 0 or not vtcd or vtcd <= 0:
        return None
    vmax = d(ced.get("v_outorga_max_q14"))
    esquina = bool(vmax and vmax > vtcd)
    v_vig = str(vmax if esquina else vtcd)
    piso = art128.referencia_art128(str(saldo), v_vig, via="125", esquina=esquina)
    out = {
        "referencia_brl": piso["referencia_brl"],
        "numerador_brl": piso["numerador_brl"],
        "memoria_calculo": piso["memoria_calculo"],
        "memorial": piso["memorial"],
        "citacao_engine": piso["citacao"],
        "base": "A (Quadro 14 vigente — piso de prospecção)",
    }
    # teto §2º (OP-1b) só quando há as duas datas (não se adivinha protocolo)
    decl = (ced.get("data_declaracao_iso") or "").strip()
    cert = (ced.get("data_certidao_iso") or "").strip()
    if len(decl) >= 7 and len(cert) >= 7:
        try:
            vtcd_decl = art128.vtcd_na_data(v_vig, 2026, int(decl[:4]))["vtcd_alvo_m2"]
            mx = art128.referencia_max_art128(str(saldo), v_vig, via="125", esquina=esquina,
                                              vtcd_declaracao=vtcd_decl, mes_ref=decl[:7], mes_protocolo=cert[:7])
            out["max"] = {"referencia_max_brl": mx["referencia_max_brl"],
                          "base_vencedora": mx["base_vencedora"], "cenarios": mx["cenarios"],
                          "memoria_calculo": mx["memoria_calculo"]}
        except Exception:
            pass
    return out


def responder(pergunta, sql=None, cedente=None, dominio="tdc", data=None, top=3):
    """Resposta orquestrada. `cedente` (dict com saldo/VTcd) tem prioridade sobre `sql` (que carrega da
    fonte primária). Devolve estrutura número(engine)+citações(RAG), pronta para o LLM narrar (sem inventar)."""
    rag = _rag.consultar(pergunta, dominio=dominio, data=data, top=top)
    citacoes = [{
        "norma": (res.get("citacao") or {}).get("norma"),
        "dispositivo": (res.get("citacao") or {}).get("dispositivo") or res.get("rotulo"),
        "fonte_url": (res.get("citacao") or {}).get("fonte_url"),
        "vigencia": (res.get("citacao") or {}).get("vigencia"),
        "texto": (res.get("texto") or "").strip(),
        "vigencia_dispositivo": res.get("vigencia_dispositivo"),
    } for res in rag.get("resultados", [])]

    numero = None
    if _e_pergunta_de_valor(pergunta):
        ced = cedente or (_cedente_por_sql(sql) if sql else None)
        if ced:
            numero = _numero_art128(ced)

    # veredito composto (Parte 4): valor exige número-do-engine; legal exige citação.
    tipo = "valor" if _e_pergunta_de_valor(pergunta) else "juridica"
    if tipo == "valor":
        if numero is None:
            veredito = ("VALOR PENDENTE — informe o cedente (--sql com saldo+VTcd na base oficial). "
                        "O número nasce no engine Art. 128 (1.3), nunca no chute.") if not rag["fundamentada"] else \
                       ("VALOR PENDENTE (falta cedente para o engine), mas a base LEGAL está fundamentada abaixo.")
            fundamentada = False
        else:
            veredito = "RESPONDIDA — número do engine (Art. 128) + citação do dispositivo (1.3 + 1.7)."
            fundamentada = True
    else:
        veredito = rag["veredito"]
        fundamentada = rag["fundamentada"]

    return {
        "pergunta": pergunta,
        "tipo": tipo,
        "fundamentada": fundamentada,
        "veredito": veredito,
        "numero": numero,                       # do engine (1.3) — None se não-valor ou sem cedente
        "citacoes": citacoes,                   # do RAG (1.7)
        "rag_fundamentada": rag["fundamentada"],
        "corpus": rag.get("corpus"),
        "aviso": ("Número = saída determinística do engine Art. 128 rastreável ao artigo; a MARGEM comercial "
                  "é do usuário (D-DONO-7/15). Citações = dispositivos verbatim do corpus. Nada foi inventado."),
    }


def imprimir(r):
    print(f"PERGUNTA: {r['pergunta']}")
    print(f"TIPO:     {r['tipo']}   |   VEREDITO: {r['veredito']}\n")
    if r["numero"]:
        n = r["numero"]
        print(f"NÚMERO (engine Art. 128 — 1.3):")
        print(f"  {n['memoria_calculo']}")
        print(f"  → referência (÷CAmaxcd): R$ {n['referencia_brl']}   |   numerador bruto: R$ {n['numerador_brl']}")
        if n.get("max"):
            print(f"  piso×teto (OP-1b): {n['max']['memoria_calculo']}  (base vencedora: {n['max']['base_vencedora']})")
        print()
    if r["citacoes"]:
        print("CITAÇÕES (RAG — 1.7):")
        for i, c in enumerate(r["citacoes"], 1):
            print(f"  [{i}] {c['norma']} — {c['dispositivo']}")
            if c.get("fonte_url"):
                print(f"      fonte: {c['fonte_url']}")
            trecho = (c.get("texto") or "").replace("\n", " ")
            print(f"      «{trecho[:220]}{'…' if len(trecho) > 220 else ''}»")
    else:
        print("Sem dispositivo que fundamente — resposta NÃO emitida (1.7).")


def _autoteste():
    # 1) Pergunta jurídica pura → fundamentada por citação, sem número.
    r1 = responder("o que condiciona a expedição da certidão de transferência do ZEPEC-BIR?")
    assert r1["tipo"] == "juridica", r1["tipo"]
    assert r1["numero"] is None
    assert r1["fundamentada"] and r1["citacoes"], r1["veredito"]
    assert any("129" in (c.get("dispositivo") or "") for c in r1["citacoes"]), [c["dispositivo"] for c in r1["citacoes"]]

    # 2) Pergunta de VALOR com cedente sintético → número NASCE no engine + citação anexada.
    ced = {"saldo_pcpt_m2": "1000", "v_outorga_m2_q14": "3000", "v_outorga_max_q14": "",
           "data_declaracao_iso": "", "data_certidao_iso": ""}
    r2 = responder("quanto vale o potencial construtivo transferível?", cedente=ced)
    assert r2["tipo"] == "valor" and r2["numero"] is not None, r2["veredito"]
    assert r2["numero"]["referencia_brl"] == "750000.00", r2["numero"]     # 1000×3000/4
    assert r2["fundamentada"], r2["veredito"]

    # 3) Pergunta de VALOR SEM cedente → VALOR PENDENTE (não inventa número), mas não quebra.
    r3 = responder("qual o preço de referência?")
    assert r3["tipo"] == "valor" and r3["numero"] is None and not r3["fundamentada"], r3["veredito"]

    # 4) Regra de ouro: número só do engine (nunca preenchido sem cedente).
    assert r3["numero"] is None
    return 3


def main(argv):
    p = argparse.ArgumentParser(description="Assistente do produto: número(engine)+citação(RAG).")
    p.add_argument("pergunta", nargs="?", help="pergunta em linguagem natural")
    p.add_argument("--sql", help="SQL do cedente (carrega saldo+VTcd da base oficial p/ o engine)")
    p.add_argument("--dominio", default="tdc", choices=["tdc", "iptu"])
    p.add_argument("--data", help="filtro temporal AAAA-MM-DD")
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--json", action="store_true")
    p.add_argument("--autoteste", action="store_true")
    a = p.parse_args(argv[1:])
    if a.autoteste:
        n = _autoteste()
        print(f"AUTO-TESTE assistente: OK — {n} casos (jurídica cita 1.7; valor nasce no engine 1.3; "
              f"sem cedente = PENDENTE, nunca inventa).")
        return 0
    if not a.pergunta:
        print("informe a pergunta (ou --autoteste)", file=sys.stderr); return 2
    r = responder(a.pergunta, sql=a.sql, dominio=a.dominio, data=a.data, top=a.top)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        imprimir(r)
    return 0 if r["fundamentada"] else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))
