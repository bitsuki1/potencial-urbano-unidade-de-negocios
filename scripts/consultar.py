#!/usr/bin/env python3
"""
consultar.py — Consulta RAG híbrida COM CITAÇÃO OBRIGATÓRIA (CLAUDE.md 1.7 / 2.6 / Parte 3 etapa 5).

Retrieval híbrido determinístico:
    1. filtro por metadado  (--lei / --tema / --jurisdicao / --vigente)   [2.6]
    2. keyword scoring TF-IDF sobre o índice invertido                    [2.6]
    -> retorna os top-N dispositivos, CADA UM com sua citação rastreável (norma+dispositivo+fonte+vigência).

GATE 1.7 (citação obrigatória): se nenhum dispositivo passar o limiar, a resposta é
"NÃO-FUNDAMENTADA" — o RAG NUNCA responde sem citar (regra de ouro do Gen RAG, CLAUDE.md Parte 4).
Este script NÃO redige prosa nem inventa fato: ele DEVOLVE o(s) dispositivo(s) verbatim que
fundamentam — a redação fica a cargo do LLM roteador depois, sempre amarrado a estas citações (1.3).

Uso:
    python3 scripts/consultar.py "valor venal de imóvel residencial pode subir quanto em 1969?"
    python3 scripts/consultar.py --lei lei-municipal-saopaulo-7228-1968 --top 3 "multa por sonegação"
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


def filtrar(meta, lei=None, tema=None, jurisdicao=None):
    """Etapa 1 (2.6): conjunto de chunks elegíveis após filtro de metadado."""
    elegiveis = set(meta.keys())
    if lei:
        elegiveis = {c for c in elegiveis if meta[c]["lei_id"] == lei}
    if tema:
        tn = normalizar(tema)
        elegiveis = {c for c in elegiveis
                     if any(tn in normalizar(t) for t in (meta[c].get("tema") or []))}
    if jurisdicao:
        jn = normalizar(jurisdicao)
        elegiveis = {c for c in elegiveis if jn in normalizar(meta[c].get("jurisdicao") or "")}
    return elegiveis


# BM25 (k1,b) e o limiar de COBERTURA do gate 1.7.
BM25_K1, BM25_B = 1.5, 0.75
# Fração mínima dos termos-de-conteúdo da pergunta que o melhor dispositivo precisa cobrir
# para a resposta ser FUNDAMENTADA. Abaixo disso, o match é fraco/genérico (ex.: bater só em
# "direito" para uma pergunta sobre "direito de construir") e NÃO fundamenta (1.7).
COBERTURA_MIN = 0.34


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


def consultar(pergunta, lei=None, tema=None, jurisdicao=None, top=3):
    store, inv, meta = carregar_indice()
    elegiveis = filtrar(meta, lei=lei, tema=tema, jurisdicao=jurisdicao)
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
            "termos_casados": casados,
            "citacao": c.get("citacao"),
            "rotulo": c.get("rotulo"),
            "texto": c.get("texto"),
        })

    # GATE 1.7: fundamenta só se o melhor dispositivo cobrir fração suficiente da pergunta.
    cobertura_top = resultados[0]["cobertura"] if resultados else 0.0
    fundamentada = bool(resultados) and cobertura_top >= COBERTURA_MIN
    if fundamentada:
        veredito = "FUNDAMENTADA"
    elif resultados:
        veredito = (f"NÃO-FUNDAMENTADA (1.7: match fraco — cobertura {cobertura_top:.0%} "
                    f"< {COBERTURA_MIN:.0%}; candidatos abaixo, mas insuficientes para fundamentar)")
    else:
        veredito = "NÃO-FUNDAMENTADA (1.7: nenhum dispositivo no corpus indexado)"
    return {
        "pergunta": pergunta,
        "filtros": {"lei": lei, "tema": tema, "jurisdicao": jurisdicao},
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
        print(f"    termos: {', '.join(res['termos_casados'])}")
        trecho = res["texto"].strip().replace("\n", " ")
        print(f"    «{trecho[:300]}{'…' if len(trecho) > 300 else ''}»\n")


def main(argv):
    p = argparse.ArgumentParser(description="Consulta RAG com citação obrigatória (1.7).")
    p.add_argument("pergunta", help="pergunta em linguagem natural")
    p.add_argument("--lei", help="filtra por lei_id")
    p.add_argument("--tema", help="filtra por tema")
    p.add_argument("--jurisdicao", help="filtra por jurisdição")
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--json", action="store_true", help="saída JSON")
    args = p.parse_args(argv[1:])
    r = consultar(args.pergunta, lei=args.lei, tema=args.tema,
                  jurisdicao=args.jurisdicao, top=args.top)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        imprimir_humano(r)
    # exit code: 0 fundamentada, 3 não-fundamentada (útil em script/eval)
    sys.exit(0 if r["fundamentada"] else 3)


if __name__ == "__main__":
    main(sys.argv)
