#!/usr/bin/env python3
"""
fatiar.py — Chunking ESTRUTURAL de uma norma verbatim, por dispositivo (CLAUDE.md 2.5).

Princípios atendidos:
- 2.5: a unidade atômica é o dispositivo (Título→Capítulo→Seção→Artigo→…). Nunca corta
  por tamanho fixo. Cada chunk carrega o caminho hierárquico e o id da lei.
- 1.7: cada chunk leva a citação (lei, dispositivo, fonte, vigência) — pré-requisito do RAG.
- 1.2: extração PURA. Este script NÃO interpreta, NÃO resume, NÃO usa LLM: só recorta o
  verbatim em pedaços rastreáveis. Número nasce no engine, não aqui (1.3).
- ZERO-COMPRESSÃO / nada se descarta: o preâmbulo (texto antes do 1º artigo) vira chunk próprio;
  as assinaturas/fecho ficam coladas ao chunk do ÚLTIMO artigo (fidelidade > granularidade — não
  se cria um chunk 'fecho' separado). Nada do corpo verbatim é jogado fora.

GUARDA DE VERBATIM: só fatia .md que tenha o cabeçalho `## Texto integral (verbatim)` e
cujo .json par esteja com `confianca_extracao: alta`. Resumo não-verbatim NÃO entra no RAG
(citaria síntese, não dispositivo — violaria 1.7). Itens recusados são reportados, não fatiados.

Uso:
    python3 scripts/fatiar.py                 # fatia todas as leis verbatim elegíveis
    python3 scripts/fatiar.py leis/municipal-sp/lei-municipal-saopaulo-7228-1968.md

Escreve: rag/chunks/<lei_id>/<seq>__<rotulo>.json  (um arquivo por dispositivo)
         e atualiza o status_pipeline do .json da lei para "fatiado".

Trazido pela instância orquestradora do Potencial Urbano — 2026-06-20.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MARCADOR_VERBATIM = "## Texto integral (verbatim)"

# Regex de dispositivos (início de linha). Aceita "Art. 1º", "Art 1o", "Art. 10 -", "Art. 156-A".
# CAPTURA o sufixo -A/-B (achado A2-02/B-11): "Art. 156-A" é dispositivo DISTINTO de "Art. 156";
# rotulá-lo "Art. 156" cita dispositivo inexistente (viola 1.7).
RE_ARTIGO = re.compile(r"^\s*Art\.?\s*(\d+(?:-[A-Z])?)\s*[ºoO°.\-–]?", re.IGNORECASE)
RE_TITULO = re.compile(r"^\s*T[ÍI]TULO\s+([IVXLCDM]+|\d+)\b", re.IGNORECASE)
RE_CAPITULO = re.compile(r"^\s*CAP[ÍI]TULO\s+([IVXLCDM]+|\d+)\b", re.IGNORECASE)
RE_SECAO = re.compile(r"^\s*SE[ÇC][ÃA]O\s+([IVXLCDM]+|\d+)\b", re.IGNORECASE)


def slug(texto: str, limite: int = 40) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t[:limite] or "trecho"


def extrair_corpo_verbatim(md: str):
    """Retorna o texto após o marcador de verbatim, ou None se ausente."""
    idx = md.find(MARCADOR_VERBATIM)
    if idx < 0:
        return None
    return md[idx + len(MARCADOR_VERBATIM):].strip("\n")


def fatiar_corpo(corpo: str):
    """
    Divide o corpo verbatim em dispositivos. Estratégia conservadora e fiel:
    - A unidade de corte é o ARTIGO (Art. N). Subdispositivos (incisos, §§, alíneas) e
      redações citadas entre aspas ficam DENTRO do chunk do artigo — recortá-los
      arriscaria mutilar o verbatim (esta é uma lei 'alteradora', cheia de texto citado).
    - Cabeçalhos Título/Capítulo/Seção, quando existem, compõem o caminho hierárquico.
    - O texto antes do 1º artigo vira 'preambulo'; assinaturas/fecho ficam no chunk do último artigo.
    Retorna lista de dicts: {tipo, rotulo, numero, caminho[], texto}.
    """
    linhas = corpo.split("\n")
    titulo = capitulo = secao = None
    chunks = []
    atual = {"tipo": "preambulo", "rotulo": "Preâmbulo", "numero": None,
             "caminho": [], "linhas": []}

    def fechar(c):
        texto = "\n".join(c.pop("linhas")).strip()
        if texto:
            c["texto"] = texto
            chunks.append(c)

    visto_artigo = False
    for ln in linhas:
        mt, mc, ms = RE_TITULO.match(ln), RE_CAPITULO.match(ln), RE_SECAO.match(ln)
        ma = RE_ARTIGO.match(ln)
        # GUARDA (B-11): "Art. N" que abre entre ASPAS é redação CITADA dentro de uma lei alteradora
        # (ex.: 7.228 transcreve o "Art. 77" da 6.989) — NÃO é dispositivo desta norma; não abre chunk.
        if ma and ln.lstrip()[:1] in ('"', '“', '«'):
            ma = None
        if mt:
            titulo, capitulo, secao = ln.strip(), None, None
        elif mc:
            capitulo, secao = ln.strip(), None
        elif ms:
            secao = ln.strip()
        if ma:
            fechar(atual)
            visto_artigo = True
            n = ma.group(1)
            # convenção legislativa BR: ordinal ("Art. 1º".."Art. 9º"), cardinal a partir de 10
            rot = f"Art. {n}º" if n.isdigit() and int(n) <= 9 else f"Art. {n}"
            caminho = [x for x in (titulo, capitulo, secao) if x] + [rot]
            atual = {"tipo": "artigo", "rotulo": rot, "numero": n,
                     "caminho": caminho, "linhas": [ln]}
            continue
        atual["linhas"].append(ln)

    # último bloco: se já vimos artigos, o resto após o último artigo é parte dele;
    # mas assinatura/fecho costuma vir no mesmo bloco do último artigo — mantemos junto
    # (fidelidade > granularidade), exceto se nenhum artigo foi visto.
    if not visto_artigo:
        atual["tipo"] = "documento"
        atual["rotulo"] = "Documento"
    fechar(atual)
    return chunks


def fatiar_lei(md_path: Path, reportar):
    jpath = md_path.with_suffix(".json")
    if not jpath.exists():
        reportar(f"  SKIP {md_path.name}: sem .json par")
        return 0
    # Guarda de encoding (RAG-05): um arquivo não-UTF-8 na zona de despejo não pode
    # derrubar o batch inteiro (e o CI). Reporta e pula só o malformado.
    try:
        meta = json.loads(jpath.read_text(encoding="utf-8"))
        corpo = extrair_corpo_verbatim(md_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        reportar(f"  SKIP {md_path.name}: erro de leitura/encoding ({e.__class__.__name__}) — pulado")
        return 0
    lei_id = meta.get("id") or md_path.stem
    confianca = meta.get("confianca_extracao")

    if corpo is None:
        reportar(f"  SKIP {lei_id}: sem '{MARCADOR_VERBATIM}' (não-verbatim) — não entra no RAG (1.7)")
        return 0
    if confianca != "alta":
        reportar(f"  SKIP {lei_id}: confianca_extracao={confianca!r} (só 'alta' é fatiável) — RO verbatim")
        return 0

    fonte = meta.get("fonte") or {}
    vigencia = meta.get("vigencia") or {}
    tema = meta.get("tema") or []
    jurisdicao = meta.get("jurisdicao")

    dispositivos = fatiar_corpo(corpo)
    if not dispositivos:
        reportar(f"  SKIP {lei_id}: corpo verbatim vazio")
        return 0

    destino = RAIZ / "rag" / "chunks" / lei_id
    if destino.exists():
        for antigo in destino.glob("*.json"):
            antigo.unlink()  # idempotência: regenera limpo
    destino.mkdir(parents=True, exist_ok=True)

    for i, d in enumerate(dispositivos, start=1):
        seq = f"{i:03d}"
        chunk_id = f"{lei_id}::{seq}-{slug(d['rotulo'])}"
        chunk = {
            "chunk_id": chunk_id,
            "lei_id": lei_id,
            "tipo_dispositivo": d["tipo"],
            "rotulo": d["rotulo"],
            "numero": d["numero"],
            "caminho_hierarquico": d["caminho"],
            "texto": d["texto"],
            # citação pré-montada (1.7): tudo que uma resposta precisa para fundamentar
            "citacao": {
                "norma": f"{meta.get('tipo_norma','norma')} nº {meta.get('numero')}/{meta.get('ano')} — {jurisdicao}",
                "dispositivo": " › ".join(d["caminho"]) if d["caminho"] else d["rotulo"],
                "fonte_url": fonte.get("url"),
                "vigencia": vigencia,
            },
            "tema": tema,
            "jurisdicao": jurisdicao,
            "ementa": meta.get("ementa"),
        }
        (destino / f"{seq}__{slug(d['rotulo'])}.json").write_text(
            json.dumps(chunk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # status_pipeline: bruto -> fatiado
    if meta.get("status_pipeline") in ("bruto", None):
        meta["status_pipeline"] = "fatiado"
        jpath.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    reportar(f"  OK   {lei_id}: {len(dispositivos)} dispositivos -> rag/chunks/{lei_id}/")
    return len(dispositivos)


def main(argv):
    alvos = []
    if len(argv) > 1:
        alvos = [Path(a) if Path(a).is_absolute() else RAIZ / a for a in argv[1:]]
    else:
        alvos = sorted((RAIZ / "leis").rglob("*.md"))

    msgs = []
    total_chunks = total_leis = 0
    for md in alvos:
        n = fatiar_lei(md, msgs.append)
        if n:
            total_leis += 1
            total_chunks += n
    print("\n".join(msgs))
    print(f"\nfatiar: {total_leis} leis fatiadas, {total_chunks} dispositivos no total.")


if __name__ == "__main__":
    main(sys.argv)
