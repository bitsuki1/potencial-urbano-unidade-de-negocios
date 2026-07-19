#!/usr/bin/env python3
"""
capturar_lei_planalto.py — captura VERBATIM (texto consolidado federal) do Planalto (ccivil_03) para
`_entrada/misto/<id>.txt`, no formato que `promover_entrada.py` consome (cabeçalho FONTE:/CAPTURA:/ID:).

Par federal do `capturar_lei_portal.py` (que é do catálogo MUNICIPAL de SP). O Planalto serve o texto
compilado em latin-1; recortamos do título ("LEI Nº"/"DECRETO Nº"/"DECRETO-LEI Nº") até o fecho
("Brasília," do encerramento presidencial), inclusive — extração PURA (1.2), nada interpretado.

Fail-closed: sem título reconhecível ou com menos artigos que --min-arts, NADA é gravado (exit≠0).
O sha256 do HTML cru é carimbado no cabeçalho (prova anti-truncamento; o promover confere).

Uso:
  python3 scripts/capturar_lei_planalto.py <url-planalto> <id> [--min-arts N]
Ex.:
  python3 scripts/capturar_lei_planalto.py \
      https://www.planalto.gov.br/ccivil_03/leis/l6938.htm lei-federal-6938-1981

Trazido pela instância PU 22 — 2026-07-19 (Etapa D: federais ambientais 6.938/1981 e 11.428/2006,
que NÃO estão no catálogo municipal de SP).
"""
import hashlib
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

RE_TITULO = re.compile(r"(LEI|DECRETO(-LEI)?)\s+N[ºO°]", re.IGNORECASE)


def _ctx():
    for var in ("REQUESTS_CA_BUNDLE", "SSL_CERT_FILE", "CURL_CA_BUNDLE"):
        p = os.environ.get(var)
        if p and Path(p).exists():
            return ssl.create_default_context(cafile=p)
    p = "/root/.ccr/ca-bundle.crt"
    if Path(p).exists():
        return ssl.create_default_context(cafile=p)
    return ssl.create_default_context()


def baixar(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ingestao-corpus-PU)"})
    with urllib.request.urlopen(req, timeout=60, context=_ctx()) as r:
        raw = r.read()
    return raw


def extrair(raw: bytes):
    """Texto verbatim recortado do título ao encerramento. Planalto = latin-1; <p>/<br> viram quebra."""
    h = raw.decode("latin-1", errors="replace")
    h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", "", h)
    h = re.sub(r"(?i)<\s*br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</\s*(p|div|tr|li|h[1-6])\s*>", "\n", h)
    txt = re.sub(r"<[^>]+>", "", h)
    txt = H.unescape(txt)
    linhas = [re.sub(r"[ \t\xa0]+", " ", ln).strip() for ln in txt.split("\n")]
    linhas = [ln for ln in linhas if ln]
    ini = None
    for i, ln in enumerate(linhas):
        if RE_TITULO.search(ln):
            ini = i
            break
    if ini is None:
        raise SystemExit("FALHA fail-closed: título ('LEI Nº'/'DECRETO Nº') não encontrado.")
    # fecho: última linha 'Brasília,' (encerramento presidencial) — mantém tudo até ela, inclusive.
    fim = len(linhas)
    for j in range(len(linhas) - 1, ini, -1):
        if re.match(r"Bras[íi]lia,", linhas[j]):
            fim = j + 1
            break
    return linhas[ini:fim]


def main():
    import argparse
    ap = argparse.ArgumentParser(description="captura verbatim do Planalto (ccivil_03)")
    ap.add_argument("url")
    ap.add_argument("id")
    ap.add_argument("--min-arts", type=int, default=3)
    ns = ap.parse_args()
    raw = baixar(ns.url)
    corpo = extrair(raw)
    arts = sum(1 for p in corpo if re.match(r"Art\.?\s*\d+", p))
    if arts < ns.min_arts:
        raise SystemExit(f"FALHA fail-closed: só {arts} artigos (< {ns.min_arts}) — página suspeita, nada gravado.")
    sha = hashlib.sha256(raw).hexdigest()
    ENTRADA.mkdir(parents=True, exist_ok=True)
    alvo = ENTRADA / f"{ns.id}.txt"
    cab = (f"FONTE: {ns.url}\n"
           f"CAPTURA: {date.today().isoformat()} (texto consolidado federal do Planalto/ccivil_03, latin-1)\n"
           f"SHA256_FONTE: {sha}\n"
           f"ID: {ns.id}\n\n")
    alvo.write_text(cab + "\n\n".join(corpo) + "\n", encoding="utf-8")
    print(f"OK {ns.id}: {len(corpo)} parágrafos, {arts} artigos, sha {sha[:12]} -> {alvo.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
