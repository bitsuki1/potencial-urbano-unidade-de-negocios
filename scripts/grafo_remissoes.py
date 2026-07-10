#!/usr/bin/env python3
"""
grafo_remissoes.py — B-6 (grafo de remissões, 100% LOCAL — desacoplado de embeddings; ROADMAP M4/R4).

Extrai, por REGEX sobre o texto verbatim dos chunks (rag/chunks/**), as arestas de remissão:

  tipo                 | exemplo no verbatim                             | alvo
  ---------------------|--------------------------------------------------|---------------------
  redacao_dada_por     | "(Redação dada pela Lei nº 17.844/2022)"         | lei alteradora
  revogado_por         | "(Revogado pela Lei nº 16.402/2016)"             | lei revogadora
  regulamentado_por    | "(Regulamentado pelo Decreto nº 57.536/2016)"    | decreto
  acrescido_por        | "(Acrescido/Incluído pela Lei ...)"              | lei
  altera_lei           | "A Lei nº 6.989, ... é alterada"                 | lei alterada
  vigencia_de          | "entrará em vigor ... salvo o artigo 3º"         | dispositivo da MESMA lei
  remissao_interna     | "... nos termos do art. 125 ..."                 | dispositivo da MESMA lei

Saída: rag/grafo/remissoes.csv (determinístico, idempotente). O consultar.py exibe as arestas
do dispositivo topo ("citado por" / "cita") — extração pura (1.2): só o que está LITERALMENTE
no texto, com o trecho de prova; nenhuma interpretação.

Uso: python3 scripts/grafo_remissoes.py
PU 18 · 2026-07-05 (B-6; destravado por D-DONO-2).
"""
import csv
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CHUNKS = RAIZ / "rag" / "chunks"
OUT = RAIZ / "rag" / "grafo"

RE_MARCADOR = re.compile(
    r"\(?\s*(Reda[cç][aã]o dada|Revogad[oa]s?|Regulamentad[oa]s?|Acrescid[oa]s?|Inclu[ií]d[oa]s?)\s+"
    r"pel[ao]\s+(Lei(?:\s+Complementar)?|Decreto(?:-Lei)?|Emenda Constitucional)\s*"
    r"n?[ºo°.]*\s*([\d.]+)\s*(?:[,/]\s*(?:de\s+[^)]*?)?(\d{4}))?", re.I)
TIPO_POR_MARCADOR = {
    "redacao dada": "redacao_dada_por", "revogado": "revogado_por", "revogada": "revogado_por",
    "revogados": "revogado_por", "revogadas": "revogado_por",
    "regulamentado": "regulamentado_por", "regulamentada": "regulamentado_por",
    "acrescido": "acrescido_por", "acrescida": "acrescido_por",
    "incluido": "acrescido_por", "incluida": "acrescido_por",
}
RE_ALTERA = re.compile(r"\bA?\s*Lei\s+n?[ºo°.]*\s*([\d.]+)\s*,?[^.]{0,80}?[eé]\s+alterada", re.I)
RE_VIGOR = re.compile(r"entrar[aá]\s+em\s+vigor|produzir[aá]\s+(?:seus\s+)?efeitos", re.I)
RE_ART_INTERNO = re.compile(r"\bart(?:igo)?s?\.?\s*(\d+)\s*[ºo°]?", re.I)


def _norm_marcador(m):
    s = re.sub(r"[^a-z ]", "", m.lower().replace("ç", "c").replace("ã", "a"))
    return TIPO_POR_MARCADOR.get(s.strip().split(" pel")[0].strip(), None)


def _num_lei(bruto, ano):
    n = bruto.replace(".", "")
    return f"{n}/{ano}" if ano else n


def extrair(chunk, lei_id):
    texto = chunk.get("texto") or ""
    disp = chunk.get("rotulo") or ""
    cid = chunk.get("chunk_id") or ""
    proprio = RE_ART_INTERNO.match(disp.replace("Art.", "art. "))
    proprio_num = None
    m = re.search(r"(\d+)", disp)
    if m:
        proprio_num = m.group(1)
    arestas = []

    for mk in RE_MARCADOR.finditer(texto):
        tipo = _norm_marcador(mk.group(1) + " pel")
        if not tipo:
            continue
        alvo = f"{mk.group(2)} {_num_lei(mk.group(3), mk.group(4))}"
        arestas.append((tipo, alvo, mk.group(0)[:120]))

    for mk in RE_ALTERA.finditer(texto):
        arestas.append(("altera_lei", f"Lei {_num_lei(mk.group(1), None)}", mk.group(0)[:120]))

    tem_vigor = bool(RE_VIGOR.search(texto))
    for mk in RE_ART_INTERNO.finditer(texto):
        alvo_num = mk.group(1)
        if alvo_num == proprio_num:
            continue
        ini = max(0, mk.start() - 60)
        trecho = texto[ini:mk.end() + 60].replace("\n", " ")
        # Artigo DE OUTRA LEI ("artigos 26 ... da Lei nº 16.402")? Então a aresta é EXTERNA,
        # não interna — olha a janela após a referência por "d[ao] Lei/Decreto nº X".
        janela = texto[mk.end():mk.end() + 90]
        ext = re.search(r"\bd[ao]\s+(Lei|Decreto)(?:\s+Complementar)?\s+n?[ºo°.]*\s*([\d.]+)", janela, re.I)
        if ext:
            alvo = f"{ext.group(1)} {ext.group(2).replace('.', '')}, Art. {alvo_num}"
            arestas.append(("remissao_externa", alvo, trecho[:120]))
            continue
        tipo = "vigencia_de" if tem_vigor else "remissao_interna"
        arestas.append((tipo, f"Art. {alvo_num}", trecho[:120]))

    return [{"lei_id": lei_id, "chunk_id": cid, "dispositivo": disp,
             "tipo": t, "alvo": a, "trecho_prova": p} for t, a, p in arestas]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    linhas = []
    for lei_dir in sorted(p for p in CHUNKS.iterdir() if p.is_dir()):
        for cj in sorted(lei_dir.glob("*.json")):
            c = json.loads(cj.read_text(encoding="utf-8"))
            linhas.extend(extrair(c, lei_dir.name))
    # RAG-03 (auditoria 2026-07-10): dedup por (lei_id, chunk_id, tipo, alvo) — o mesmo dispositivo
    # pode referenciar o mesmo alvo várias vezes no texto, mas a aresta do grafo é UMA só.
    antes = len(linhas)
    visto = set()
    unicos = []
    for l in linhas:
        chave = (l["lei_id"], l["chunk_id"], l["tipo"], l["alvo"])
        if chave not in visto:
            visto.add(chave)
            unicos.append(l)
    linhas = unicos
    dest = OUT / "remissoes.csv"
    with dest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["lei_id", "chunk_id", "dispositivo", "tipo", "alvo", "trecho_prova"])
        w.writeheader()
        w.writerows(linhas)
    por_tipo = {}
    leis = set()
    for l in linhas:
        por_tipo[l["tipo"]] = por_tipo.get(l["tipo"], 0) + 1
        leis.add(l["lei_id"])
    if antes != len(linhas):
        print(f"grafo_remissoes: dedup {antes} -> {len(linhas)} ({antes - len(linhas)} duplicatas removidas)")
    print(f"grafo_remissoes (B-6): {len(linhas)} arestas de {len(leis)} leis -> {dest.relative_to(RAIZ)}")
    print(f"  por tipo: {dict(sorted(por_tipo.items()))}")


if __name__ == "__main__":
    main()
