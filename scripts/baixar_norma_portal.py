#!/usr/bin/env python3
"""
baixar_norma_portal.py — Baixa o VERBATIM de uma norma municipal de SP direto do PORTAL OFICIAL
(legislacao.prefeitura.sp.gov.br) — a fonte mais auditável (é a URL que todo o corpus já registra).
Extrai o container `texto_compilado` (texto consolidado/vigente), limpa só a marcação HTML (nada de
conteúdo legal é descartado — 1.2 extração pura), grava `_entrada/misto/<id>.txt` e imprime o
sha256 da FONTE + o nº de caracteres (prova anti-truncamento).

Uso:
    python3 scripts/baixar_norma_portal.py <slug-do-portal> <id-do-corpus>
    ex.: python3 scripts/baixar_norma_portal.py lei-18298-de-17-de-setembro-de-2025 lei-municipal-saopaulo-18298-2025

NÃO escreve em leis/ — só prepara o cru. O .json (metadados) é escrito à parte (julgamento humano),
e o promover_entrada.py gera o .md verbatim. Determinístico e idempotente.
"""
import sys, re, html, hashlib, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "_entrada" / "misto"
BASE = "https://legislacao.prefeitura.sp.gov.br/leis/"
UA = {"User-Agent": "Mozilla/5.0 (ingestao-corpus-PU; auditoria juridica)"}


def baixar(slug):
    url = BASE + slug
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
        final_url = r.geturl()
    return raw, final_url


def extrair_texto(raw_html):
    h = raw_html.decode("utf-8", errors="replace")
    # o corpo consolidado vive na div class="...texto_compilado..."
    m = re.search(r'<div[^>]*class="[^"]*texto_compilado[^"]*"[^>]*>', h)
    if not m:
        return None, "container texto_compilado não encontrado"
    ini = m.end()
    # fecha no </div> equilibrado (heurística: próximo bloco de rodapé conhecido ou fim)
    resto = h[ini:]
    # tira blocos <script>/<style> (conteúdo não fica entre tags simples) ANTES de cortar
    resto = re.sub(r'(?is)<script[^>]*>.*?</script>', '', resto)
    resto = re.sub(r'(?is)<style[^>]*>.*?</style>', '', resto)
    # corta no rodapé do portal (âncoras conhecidas) se houver
    for marca in ['<div class="rodape', '<footer', 'id="rodape"', 'Voltar ao topo']:
        j = resto.find(marca)
        if j != -1:
            resto = resto[:j]
    # limpeza HTML -> texto. <br>,<p> viram quebra de linha.
    resto = re.sub(r'(?i)<\s*br\s*/?>', '\n', resto)
    resto = re.sub(r'(?i)</\s*p\s*>', '\n\n', resto)
    resto = re.sub(r'(?i)</\s*(div|tr|li|h[1-6])\s*>', '\n', resto)
    texto = re.sub(r'<[^>]+>', '', resto)
    texto = html.unescape(texto)
    # normaliza espaços/brancos sem colar palavras
    texto = re.sub(r'[ \t ]+', ' ', texto)
    texto = re.sub(r'\n[ \t]+', '\n', texto)
    # tira o CHROME de navegação do portal (não é texto de lei; UI da página)
    CHROME = {
        "você está em:", "voce esta em:", "início", "inicio",
        "pesquisa de leis municipais", "voltar", "imprimir",
        "compartilhar essa norma:", "compartilhar", "detalhes da norma",
        "texto consolidado", "texto compilado", "adin", "topo",
    }
    linhas = [ln for ln in texto.split("\n") if ln.strip().lower() not in CHROME]
    texto = "\n".join(linhas)
    texto = re.sub(r'\n{3,}', '\n\n', texto).strip()
    # corta no marcador de fim oficial (preserva o disclaimer, descarta o que vier depois)
    fim = "Este texto não substitui o original publicado no Diário Oficial"
    k = texto.find(fim)
    if k != -1:
        texto = texto[:k + len(fim) + 60].rstrip()
        # fecha na frase (até " Paulo" ou fim de linha)
        texto = re.sub(r'(Diário Oficial da Cidade de São Paulo)[\s\S]*$', r'\1.', texto)
    return texto, None


def main():
    if len(sys.argv) != 3:
        print(__doc__); return 2
    slug, cid = sys.argv[1], sys.argv[2]
    raw, final_url = baixar(slug)
    texto, err = extrair_texto(raw)
    if err:
        print(f"ERRO: {err}", file=sys.stderr); return 1
    sha_fonte = hashlib.sha256(raw).hexdigest()
    ENTRADA.mkdir(parents=True, exist_ok=True)
    cabecalho = (
        f"FONTE: {final_url}\n"
        f"CAPTURA: portal oficial legislacao.prefeitura.sp.gov.br (container texto_compilado)\n"
        f"ID: {cid}\n\n"
    )
    (ENTRADA / f"{cid}.txt").write_text(cabecalho + texto + "\n", encoding="utf-8")
    art = len(re.findall(r'\bArt\.\s*\d+', texto))
    print(f"OK {cid}")
    print(f"  url_final     : {final_url}")
    print(f"  sha256_fonte  : {sha_fonte}")
    print(f"  n_chars_texto : {len(texto)}")
    print(f"  artigos (Art.): {art}")
    print(f"  gravado       : _entrada/misto/{cid}.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
