-- Stack canônico Potencial Urbano (IPTU/TDC): espacial + RAG + busca textual jurídica
create extension if not exists postgis;            -- geo: lotes, zoneamento, ZEPEC (Motor 3)
create extension if not exists vector;             -- RAG: embeddings dos chunks de lei
create extension if not exists pg_trgm;            -- busca por similaridade de texto
create extension if not exists unaccent;           -- normalização PT-BR (acentos)
create extension if not exists fuzzystrmatch;      -- matching de endereço/nome
create extension if not exists btree_gin;          -- índices combinados (metadado + texto)
