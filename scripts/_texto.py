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


def normalizar(texto: str) -> str:
    """minúsculas sem acento (NFKD -> ascii)."""
    return unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode("ascii").lower()


def tokenizar(texto: str):
    """Tokens alfanuméricos de conteúdo (>=2 chars, fora das stopwords)."""
    return [w for w in re.findall(r"[a-z0-9]+", normalizar(texto))
            if w not in STOPWORDS and len(w) > 1]
