#!/usr/bin/env python3
"""
capturar_lei_portal.py — captura VERBATIM (texto COMPILADO) do Catálogo de Legislação
Municipal de São Paulo (legislacao.prefeitura.sp.gov.br) para `_entrada/misto/<id>.txt`,
no formato que `promover_entrada.py` consome (cabeçalho FONTE:/CAPTURA:/ID:).

Extração PURA (princípio 1.2): recorta o texto da página do título ("LEI Nº"/"DECRETO Nº")
até o aviso final ("Este texto não substitui..."), inclusive — sem interpretar nada.
As anotações de alteração do texto compilado ("Redação dada...", "Revogado...") são
CONTEÚDO e ficam (é o que dá a vigência por dispositivo, 1.6).

Fail-closed: sem título reconhecível, sem aviso final ou com menos artigos que --min-arts,
NADA é gravado (exit≠0). O sha256 do cru é carimbado depois pelo promover (AUD-A10).

Uso:
  python3 scripts/capturar_lei_portal.py <slug> <id> [--min-arts N]
Ex.:
  python3 scripts/capturar_lei_portal.py lei-10235-de-16-de-dezembro-de-1986 \
      lei-municipal-saopaulo-10235-1986

Trazido pela instância PU 18 — 2026-07-10 (destrave B-4: o portal oficial responde da
sessão remota; captura substitui OCR de PDF-scan e dependência do Drive para leis).
"""
import html as H
import os
import re
import ssl
import sys
import urllib.request
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "_entrada" / "misto"
BASE = "https://legislacao.prefeitura.sp.gov.br/"

RE_TITULO = re.compile(r"^(LEI|DECRETO(-LEI)?)\s+N[ºO°]?\s*[\d.]+", re.IGNORECASE)
RE_FIM = re.compile(r"^Este texto n[ãa]o substitui", re.IGNORECASE)


def _ctx():
    """Contexto TLS: respeita o CA do proxy da sessão quando existir (nunca desabilita verificação)."""
    for var in ("REQUESTS_CA_BUNDLE", "SSL_CERT_FILE", "CURL_CA_BUNDLE"):
        p = os.environ.get(var)
        if p and Path(p).exists():
            return ssl.create_default_context(cafile=p)
    p = "/root/.ccr/ca-bundle.crt"
    if Path(p).exists():
        return ssl.create_default_context(cafile=p)
    return ssl.create_default_context()


def baixar(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (captura verbatim PU)"})
    with urllib.request.urlopen(req, timeout=60, context=_ctx()) as r:
        return r.read().decode("utf-8", errors="replace")


def _tabelas_para_p(htm: str) -> str:
    """Converte <table> em pseudo-parágrafos '| c1 | c2 |' preservando a POSIÇÃO no fluxo."""
    def conv(m):
        rows = re.findall(r"<tr\b[^>]*>(.*?)</tr>", m.group(0), re.S | re.I)
        out = []
        for row in rows:
            cels = re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", row, re.S | re.I)
            cels = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", c))).strip() for c in cels]
            out.append("<p>| " + " | ".join(cels) + " |</p>")
        return "\n".join(out)
    return re.sub(r"<table\b[^>]*>.*?</table>", conv, htm, flags=re.S | re.I)


def extrair(htm: str):
    """Sequência de <p> limpos, recortada do título ao aviso final (inclusive)."""
    htm = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", htm, flags=re.S | re.I)
    htm = _tabelas_para_p(htm)
    paras = []
    for p in re.findall(r"<p\b[^>]*>(.*?)</p>", htm, re.S):
        p = re.sub(r"<br\s*/?>", "\n", p, flags=re.I)
        t = H.unescape(re.sub(r"<[^>]+>", "", p))
        for ln in t.split("\n"):
            ln = re.sub(r"\s+", " ", ln).strip()
            if ln:
                paras.append(ln)
    ini = fim = None
    for i, p in enumerate(paras):
        if ini is None and RE_TITULO.match(p):
            ini = i
        if ini is not None and RE_FIM.match(p):
            fim = i
            break
    if ini is None:
        raise SystemExit("FALHA fail-closed: título ('LEI Nº'/'DECRETO Nº') não encontrado na página.")
    if fim is None:
        raise SystemExit("FALHA fail-closed: aviso final ('Este texto não substitui...') não encontrado.")
    return paras[ini:fim + 1]


def main():
    import argparse
    ap = argparse.ArgumentParser(description="captura verbatim do Catálogo de Legislação Municipal SP")
    ap.add_argument("slug")
    ap.add_argument("id")
    ap.add_argument("--min-arts", type=int, default=3)
    ns = ap.parse_args()
    slug, _id, min_arts = ns.slug, ns.id, ns.min_arts
    url = BASE + slug.strip("/")
    corpo = extrair(baixar(url))
    arts = sum(1 for p in corpo if re.match(r"Art\.?\s*\d+", p))
    if arts < min_arts:
        raise SystemExit(f"FALHA fail-closed: só {arts} artigos (< {min_arts}) — página suspeita, nada gravado.")
    ENTRADA.mkdir(parents=True, exist_ok=True)
    alvo = ENTRADA / f"{_id}.txt"
    cab = (f"FONTE: {url}\n"
           f"CAPTURA: {date.today().isoformat()} (texto COMPILADO do Catálogo de Legislação Municipal, HTTPS direto)\n"
           f"ID: {_id}\n\n")
    alvo.write_text(cab + "\n\n".join(corpo) + "\n", encoding="utf-8")
    print(f"OK {_id}: {len(corpo)} parágrafos, {arts} artigos -> {alvo.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
