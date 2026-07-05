#!/usr/bin/env python3
"""
_texto.py — Tokenização CANÔNICA compartilhada por indexar.py e consultar.py.

Por que um módulo só: o índice e a consulta PRECISAM tokenizar de forma idêntica — se
divergirem, um token indexado não casa com o mesmo token na pergunta e o retrieval falha
silenciosamente. DRY aqui é correção, não estética.

Stopwords PT: artigos, preposições, conjunções e INTERROGATIVAS ("qual", "como", "quanto").
NÃO removemos números (nº de lei/artigo/percentual são chave no jurídico) nem termos de
conteúdo. Lista deliberadamente curta e conservadora — tirar palavra de conteúdo cega a busca.
"""
import re
import unicodedata

STOPWORDS = {
    # artigos / preposições / conjunções
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "ou", "em", "no", "na",
    "nos", "nas", "um", "uma", "uns", "umas", "que", "se", "por", "para", "com", "ao",
    "aos", "sua", "seu", "suas", "seus", "ser", "sera", "foi", "sao", "entre", "sob",
    "sobre", "ate", "apos", "ante", "the", "of", "this",
    # interrogativas / palavras de pergunta (ruído de NL, não de conteúdo jurídico)
    "qual", "quais", "como", "quando", "quanto", "quantos", "quanta", "quantas", "onde",
    "quem", "porque", "pode", "podem", "funciona",
}


# Separador de milhar em número jurídico: "6.989" e "1.500.000" são UM número.
# Sem isto, o regex parte em ['989'] / ['500','000'] e a citação por "Lei nº 6.989"
# não casa "6989" (achado RAG-02 da auditoria 2026-06-20). Só remove o ponto/vírgula
# quando há exatamente 3 dígitos à direita (milhar) — decimal "20,00" fica intacto.
_RE_MILHAR = re.compile(r"(?<=\d)[.,](?=\d{3}(?:\D|$))")
# Ordinal jurídico colado ao número (achado B-6, 2026-07-05 — mesma classe do milhar RAG-02):
# "artigo 3º" normaliza (NFKD) para "3o", e o token "3o" NUNCA casa a pergunta "artigo 3".
# Dobra o sufixo ordinal pós-dígito ("3o"/"3a" -> "3"). Decimal não é afetado (dígito, não letra).
_RE_ORDINAL = re.compile(r"(?<=\d)[oa]\b")


def normalizar(texto: str) -> str:
    """minúsculas sem acento (NFKD -> ascii), milhar colado, ordinal dobrado."""
    t = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode("ascii").lower()
    return _RE_ORDINAL.sub("", _RE_MILHAR.sub("", t))


def tokenizar(texto: str):
    """Tokens alfanuméricos de conteúdo (fora das stopwords). Alfabéticos exigem >=2 chars;
    NÚMERO fica mesmo com 1 dígito — 'art. 3' é chave no jurídico e o filtro len>1 o derrubava,
    contradizendo a doutrina do próprio módulo (achado B-6, 2026-07-05)."""
    return [w for w in re.findall(r"[a-z0-9]+", normalizar(texto))
            if w not in STOPWORDS and (len(w) > 1 or w.isdigit())]
