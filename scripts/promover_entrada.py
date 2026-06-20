#!/usr/bin/env python3
"""
promover_entrada.py — Promove o VERBATIM cru de `_entrada/misto/<id>.txt` para
`leis/.../<id>.md` (com `## Texto integral (verbatim)`) + atualiza o `.json` para
`confianca:"alta"`, deixando a lei pronta para o `fatiar.py`.

Resolve o achado AUD-01 da auditoria profunda: o articulado integral de 12 leis federais já
estava local em `_entrada/misto/` mas os `.md` diziam "HTTP 403 / não baixado". Isto é
re-ingestão INTERNA determinística (1.2 extração pura: NÃO interpreta, só recorta o cru),
o mesmo movimento já feito à mão na Lei 7.228/1968.

Saneia SÓ lixo de CAPTURA (não conteúdo legal):
  - cabeçalho de captura (linhas `FONTE:`/`CAPTURA:`/`ID:` + brancos iniciais);
  - rodapé-lixo de captura (linhas só com `*`, espaços, ou marcadores "Stop Claude" no fim).
O boilerplate oficial do portal ("Presidência da República" etc.) é PRESERVADO — é parte do
verbatim de tela (nada se descarta).

GUARDA: só promove se o cru tiver corpo substancial (>= MIN_LINHAS úteis) — não promove stub.
Idempotente: reescreve `.md`/`.json` de forma determinística.

Uso:
    python3 scripts/promover_entrada.py                 # todas as leis com cru em _entrada/misto/
    python3 scripts/promover_entrada.py dl-57-1966 ec-29-2000
Trazido pela instância orquestradora do PU — auditoria profunda 2026-06-20 (destrave AUD-01).
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "_entrada" / "misto"
MIN_LINHAS = 15  # corpo mínimo útil para considerar "verbatim integral" (anti-stub)

RE_JUNK = re.compile(r"^\s*(\*+|stop\s+claude.*)?\s*$", re.IGNORECASE)


def localizar_par(_id):
    """Acha o .md/.json do id em leis/** (federal/ ou municipal-sp/)."""
    for jpath in (RAIZ / "leis").rglob(f"{_id}.json"):
        return jpath.with_suffix(".md"), jpath
    return None, None


def limpar_corpo(txt: str):
    linhas = txt.split("\n")
    # 1) tira o cabeçalho de captura: tudo até (e incluindo) a linha "ID:"
    inicio = 0
    for i, ln in enumerate(linhas[:10]):
        if ln.strip().lower().startswith("id:"):
            inicio = i + 1
            break
    corpo = linhas[inicio:]
    # 2) tira brancos iniciais
    while corpo and not corpo[0].strip():
        corpo.pop(0)
    # 3) tira rodapé-lixo de captura (só `*`, vazio, ou "Stop Claude")
    while corpo and RE_JUNK.match(corpo[-1]):
        corpo.pop(0) if False else corpo.pop()
    return "\n".join(corpo).strip("\n")


def promover(_id, reportar):
    cru = ENTRADA / f"{_id}.txt"
    if not cru.exists():
        reportar(f"  SKIP {_id}: sem cru em _entrada/misto/")
        return False
    md_path, jpath = localizar_par(_id)
    if not jpath:
        reportar(f"  SKIP {_id}: sem par .json em leis/")
        return False

    corpo = limpar_corpo(cru.read_text(encoding="utf-8"))
    uteis = [l for l in corpo.split("\n") if l.strip()]
    if len(uteis) < MIN_LINHAS:
        reportar(f"  SKIP {_id}: cru com {len(uteis)} linhas úteis (< {MIN_LINHAS}) — possível stub, não promovo")
        return False

    meta = json.loads(jpath.read_text(encoding="utf-8"))
    titulo_antigo = md_path.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip() if md_path.exists() else _id
    ementa = meta.get("ementa") or "(ver texto integral)"
    url = (meta.get("fonte") or {}).get("url") or ""

    novo_md = (
        f"# {titulo_antigo}\n\n"
        f"**URL oficial:** {url}\n"
        f"**Data de captura:** 2026-06-18\n"
        f"**Proveniência:** VERBATIM DE TELA — re-ingerido em 2026-06-20 de "
        f"`_entrada/misto/{_id}.txt` (o cru já estava local; supera a versão NÃO-VERBATIM "
        f"anterior, que dizia 'HTTP 403 / não baixado'). Saneado só lixo de captura; "
        f"boilerplate oficial do portal preservado.\n"
        f"**confianca_extracao:** alta (articulado integral verbatim)\n\n"
        f"## Ementa\n\n{ementa}\n\n"
        f"## Texto integral (verbatim)\n\n{corpo}\n"
    )
    md_path.write_text(novo_md, encoding="utf-8")

    fonte = meta.get("fonte") or {}
    fonte["path"] = f"_entrada/misto/{_id}.txt"
    fonte["metodo"] = "VERBATIM DE TELA (planalto); re-ingerido de _entrada/misto/ em 2026-06-20 (AUD-01)"
    fonte["obs"] = "articulado integral verbatim; saneado lixo de captura; supera resumo WebSearch anterior."
    fonte["ocr"] = False
    meta["fonte"] = fonte
    meta["confianca_extracao"] = "alta"
    # status_pipeline volta a 'bruto' para o fatiar.py reprocessar e marcar fatiado/indexado
    if meta.get("status_pipeline") not in ("fatiado", "indexado"):
        meta["status_pipeline"] = "bruto"
    jpath.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    arts = len(re.findall(r"(?m)^\s*Art\.?\s*\d+", corpo))
    reportar(f"  OK   {_id}: {len(uteis)} linhas úteis, ~{arts} artigos -> {md_path.relative_to(RAIZ)}")
    return True


def main(argv):
    ids = argv[1:]
    if not ids:
        ids = sorted(p.stem for p in ENTRADA.glob("*.txt")
                     if localizar_par(p.stem)[1] is not None)
    msgs, n = [], 0
    for _id in ids:
        if promover(_id, msgs.append):
            n += 1
    print("\n".join(msgs))
    print(f"\npromover_entrada: {n} leis promovidas a verbatim. Rode fatiar.py + indexar.py.")


if __name__ == "__main__":
    main(sys.argv)
