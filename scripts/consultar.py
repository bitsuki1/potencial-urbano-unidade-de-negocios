#!/usr/bin/env python3
"""
consultar.py — Consulta RAG híbrida COM CITAÇÃO OBRIGATÓRIA (CLAUDE.md 1.7 / 2.6 / Parte 3 etapa 5).

Retrieval híbrido determinístico:
    1. filtro por metadado  (--lei / --tema / --jurisdicao / --data)      [2.6]
    2. keyword scoring BM25 sobre o índice invertido                      [2.6]
    -> retorna os top-N dispositivos, CADA UM com sua citação rastreável (norma+dispositivo+fonte+vigência).

GATE 1.7 (citação obrigatória): a resposta só é FUNDAMENTADA se o melhor dispositivo (a) cobrir
fração suficiente dos termos-de-conteúdo da pergunta, (b) passar um piso de score BM25 e (c) casar
≥2 termos quando a pergunta tem ≥2 termos de conteúdo (impede falso-positivo de match genérico —
ex.: bater só em "direito" para "direito de construir"). Senão, "NÃO-FUNDAMENTADA": o RAG NUNCA
responde sem citar (regra de ouro do Gen RAG, CLAUDE.md Parte 4). Este script NÃO redige prosa nem
inventa fato: DEVOLVE o(s) dispositivo(s) verbatim; a redação fica com o LLM roteador, amarrado às
citações (1.3).

FILTRO TEMPORAL (2.6/1.6): `--data AAAA-MM-DD` exclui dispositivos cuja vigência (inicio/fim) não
cobre a data. LIMITE HONESTO: normas sem `vigencia.inicio/fim` (hoje as 15 municipais só têm
`em_vigor:true`, achado A-3) NÃO podem ser filtradas por data e são mantidas — o eixo temporal
existe mas degrada à honestidade do metadado disponível.

Uso:
    python3 scripts/consultar.py "valor venal de imóvel residencial pode subir quanto em 1969?"
    python3 scripts/consultar.py --lei lei-municipal-saopaulo-7228-1968 --top 3 "multa por sonegação"
    python3 scripts/consultar.py --data 1969-01-01 "imposto predial"
    python3 scripts/consultar.py --json "..."     # saída JSON (para evals/integração)

Trazido pela instância orquestradora do Potencial Urbano — 2026-06-20.
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _texto import normalizar, tokenizar  # noqa: E402  (tokenização canônica compartilhada)

RAIZ = Path(__file__).resolve().parent.parent
INDEX_DIR = RAIZ / "rag" / "index"


def carregar_indice():
    try:
        store = json.loads((INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))
        inv = json.loads((INDEX_DIR / "invertido.json").read_text(encoding="utf-8"))
        meta = json.loads((INDEX_DIR / "metadados.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("consultar: índice ausente — rode fatiar.py e indexar.py antes.", file=sys.stderr)
        sys.exit(2)
    return store, inv, meta


def _vigente_em(vig, data):
    """True se a vigência cobre `data` (AAAA-MM-DD). Sem inicio/fim datados -> mantém
    (não dá para excluir honestamente; degrada ao metadado disponível — achado A-3)."""
    if not data:
        return True
    inicio, fim = (vig or {}).get("inicio"), (vig or {}).get("fim")
    if inicio and str(inicio) > data:
        return False
    if fim and str(fim) < data:
        return False
    return True


def _casa_dominio(dom_chunk, alvo):
    """Regra de ouro da separação TDC×IPTU (plano 2026-07-04): um chunk casa o domínio-alvo se o
    alvo está no seu `dominio` OU se ele é 'compartilhado' (lar único que entra nas consultas dos
    DOIS). Por construção NÃO perde nada — compartilhado (CF/Estatuto/PDE/LPUOS/…) sempre acompanha."""
    dom_chunk = dom_chunk or []
    return (alvo in dom_chunk) or ("compartilhado" in dom_chunk)


def filtrar(meta, lei=None, tema=None, jurisdicao=None, data=None, dominio=None,
            incluir_revogado=False, incluir_nao_citavel=False):
    """Etapa 1 (2.6): conjunto de chunks elegíveis após filtro de metadado (inclui temporal e domínio).
    B-11c (1.6): por padrão EXCLUI dispositivos REVOGADOS — o RAG não pode devolver redação
    revogada como vigente. `incluir_revogado=True` reabre-os (consulta histórica explícita).
    B-11d (1.7): por padrão EXCLUI o preâmbulo/boilerplate NÃO-CITÁVEL — não se fundamenta uma
    resposta citando cabeçalho de portal. `incluir_nao_citavel=True` reabre-os (auditoria).
    `dominio` (tdc|iptu): restringe ao domínio, SEMPRE incluindo 'compartilhado' (não-perda)."""
    elegiveis = set(meta.keys())
    if not incluir_revogado:
        elegiveis = {c for c in elegiveis
                     if (meta[c].get("vigencia_dispositivo") or {}).get("status") != "revogado"}
    if not incluir_nao_citavel:
        elegiveis = {c for c in elegiveis if meta[c].get("citavel", True)}
    if dominio:
        dn = normalizar(dominio)
        elegiveis = {c for c in elegiveis if _casa_dominio(meta[c].get("dominio"), dn)}
    if lei:
        elegiveis = {c for c in elegiveis if meta[c]["lei_id"] == lei}
    if tema:
        tn = normalizar(tema)
        elegiveis = {c for c in elegiveis
                     if any(tn in normalizar(t) for t in (meta[c].get("tema") or []))}
    if jurisdicao:
        jn = normalizar(jurisdicao)
        elegiveis = {c for c in elegiveis if jn in normalizar(meta[c].get("jurisdicao") or "")}
    if data:
        elegiveis = {c for c in elegiveis if _vigente_em(meta[c].get("vigencia"), data)}
    return elegiveis


# BM25 (k1,b) e o limiar de COBERTURA do gate 1.7.
BM25_K1, BM25_B = 1.5, 0.75
# Gate 1.7 — três travas combinadas (achado RAG-01: cobertura sozinha é gameável por
# pergunta curta com 1 termo genérico):
#   COBERTURA_MIN — fração mínima dos termos-de-conteúdo da pergunta coberta pelo top;
#   SCORE_MIN     — piso absoluto de score BM25 (mata match raso);
#   ≥2 termos casados quando a pergunta tem ≥2 termos de conteúdo (mata "direito" p/ "direito de construir").
COBERTURA_MIN = 0.34
SCORE_MIN = 1.5


def pontuar(pergunta, inv, elegiveis):
    """Etapa 2 (2.6): BM25 sobre o índice invertido, restrito aos elegíveis.
    BM25 normaliza por tamanho do dispositivo — artigo longo (muito texto citado) não vence
    só por ser grande. Retorna (scores, termos_casados, termos_conteudo_da_pergunta)."""
    N = inv.get("N", 0) or 1
    avgdl = inv.get("avgdl") or 1.0
    df = inv.get("df", {})
    doclen = inv.get("doclen", {})
    postings = inv.get("postings", {})

    termos_pergunta = list(dict.fromkeys(tokenizar(pergunta)))  # distintos, ordem preservada
    scores = {}
    termos_casados = {}
    for tok in termos_pergunta:
        if tok not in postings:
            continue
        idf = math.log(1 + (N - df.get(tok, 1) + 0.5) / (df.get(tok, 1) + 0.5))
        for cid, tf in postings[tok].items():
            if cid not in elegiveis:
                continue
            dl = doclen.get(cid, avgdl)
            denom = tf + BM25_K1 * (1 - BM25_B + BM25_B * dl / avgdl)
            scores[cid] = scores.get(cid, 0.0) + idf * (tf * (BM25_K1 + 1)) / denom
            termos_casados.setdefault(cid, set()).add(tok)
    return scores, termos_casados, termos_pergunta


def consultar(pergunta, lei=None, tema=None, jurisdicao=None, data=None, dominio=None, top=3,
              incluir_revogado=False, incluir_nao_citavel=False):
    store, inv, meta = carregar_indice()
    elegiveis = filtrar(meta, lei=lei, tema=tema, jurisdicao=jurisdicao, data=data, dominio=dominio,
                        incluir_revogado=incluir_revogado, incluir_nao_citavel=incluir_nao_citavel)
    scores, termos, termos_pergunta = pontuar(pergunta, inv, elegiveis)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:top]

    n_conteudo = len(termos_pergunta) or 1
    resultados = []
    for cid, score in ranked:
        c = store[cid]
        casados = sorted(termos.get(cid, []))
        resultados.append({
            "chunk_id": cid,
            "score": round(score, 4),
            "cobertura": round(len(casados) / n_conteudo, 3),
            "n_casados": len(casados),
            "termos_casados": casados,
            "citacao": c.get("citacao"),
            "rotulo": c.get("rotulo"),
            "texto": c.get("texto"),
            "vigencia_dispositivo": c.get("vigencia_dispositivo") or {"status": "original"},
        })

    # GATE 1.7 (três travas — ver SCORE_MIN/COBERTURA_MIN acima).
    motivo = "nenhum dispositivo no corpus indexado"
    fundamentada = False
    if resultados:
        top1 = resultados[0]
        cob, sc, ncas = top1["cobertura"], top1["score"], top1["n_casados"]
        if cob < COBERTURA_MIN:
            motivo = f"cobertura {cob:.0%} < {COBERTURA_MIN:.0%}"
        elif sc < SCORE_MIN:
            motivo = f"score {sc} < piso {SCORE_MIN}"
        elif n_conteudo >= 2 and ncas < 2:
            motivo = f"só {ncas} termo casado (match genérico) para pergunta de {n_conteudo} termos"
        else:
            fundamentada = True
    veredito = "FUNDAMENTADA" if fundamentada else (
        f"NÃO-FUNDAMENTADA (1.7: {motivo}; candidatos abaixo são insuficientes para fundamentar)"
        if resultados else "NÃO-FUNDAMENTADA (1.7: nenhum dispositivo no corpus indexado)")
    return {
        "pergunta": pergunta,
        "filtros": {"lei": lei, "tema": tema, "jurisdicao": jurisdicao, "data": data,
                    "dominio": dominio},
        "termos_pergunta": termos_pergunta,
        "fundamentada": fundamentada,
        "veredito": veredito,
        "resultados": resultados,
    }


def imprimir_humano(r):
    print(f"PERGUNTA: {r['pergunta']}")
    if any(r["filtros"].values()):
        print(f"FILTROS:  {json.dumps(r['filtros'], ensure_ascii=False)}")
    print(f"VEREDITO: {r['veredito']}\n")
    if not r["fundamentada"]:
        print("Resposta NÃO emitida — sem dispositivo que fundamente com citação (CLAUDE.md 1.7).")
        if r["resultados"]:
            print("Candidatos fracos (apenas para auditoria, NÃO citáveis como resposta):")
        else:
            return
    for i, res in enumerate(r["resultados"], 1):
        cit = res["citacao"] or {}
        print(f"[{i}] {cit.get('norma','?')} — {cit.get('dispositivo', res['rotulo'])}  "
              f"(score {res['score']}, cobertura {res['cobertura']:.0%})")
        print(f"    fonte: {cit.get('fonte_url')}")
        vig = cit.get("vigencia") or {}
        print(f"    vigência: {json.dumps(vig, ensure_ascii=False)}")
        vd = res.get("vigencia_dispositivo") or {}
        if vd.get("status") and vd["status"] != "original":
            extra = f" (revogado por {vd['revogado_por']})" if vd.get("revogado_por") else ""
            print(f"    dispositivo: {vd['status']}{extra}  ← B-11c (vigência por chunk)")
        print(f"    termos: {', '.join(res['termos_casados'])}")
        trecho = res["texto"].strip().replace("\n", " ")
        print(f"    «{trecho[:300]}{'…' if len(trecho) > 300 else ''}»\n")


def main(argv):
    p = argparse.ArgumentParser(description="Consulta RAG com citação obrigatória (1.7).")
    p.add_argument("pergunta", help="pergunta em linguagem natural")
    p.add_argument("--lei", help="filtra por lei_id")
    p.add_argument("--tema", help="filtra por tema")
    p.add_argument("--dominio", choices=["tdc", "iptu"],
                   help="restringe ao domínio (tdc|iptu); 'compartilhado' entra SEMPRE (não-perda)")
    p.add_argument("--jurisdicao", help="filtra por jurisdição")
    p.add_argument("--data", help="filtro temporal AAAA-MM-DD (vigência na data do fato gerador)")
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--incluir-revogado", action="store_true",
                   help="inclui dispositivos REVOGADOS (consulta histórica; por padrão B-11c os exclui)")
    p.add_argument("--incluir-nao-citavel", action="store_true",
                   help="inclui preâmbulo/boilerplate não-citável (auditoria; por padrão B-11d os exclui)")
    p.add_argument("--json", action="store_true", help="saída JSON")
    args = p.parse_args(argv[1:])
    r = consultar(args.pergunta, lei=args.lei, tema=args.tema, jurisdicao=args.jurisdicao,
                  data=args.data, dominio=args.dominio, top=args.top,
                  incluir_revogado=args.incluir_revogado,
                  incluir_nao_citavel=args.incluir_nao_citavel)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        imprimir_humano(r)
    # exit code: 0 fundamentada, 3 não-fundamentada (útil em script/eval)
    sys.exit(0 if r["fundamentada"] else 3)


if __name__ == "__main__":
    main(sys.argv)
