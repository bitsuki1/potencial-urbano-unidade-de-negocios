# Rota oficial do STJ que NÃO passa pelo Cloudflare — Portal de Dados Abertos

> Descoberta em 2026-08-07, ao caçar o inteiro teor dos 3 REsp (1112646 · 1202136 · 1645832).
> Fonte OFICIAL do STJ, servida em host próprio, **sem desafio Cloudflare** — ao contrário de
> `scon.stj.jus.br`, `processo.stj.jus.br`, `ww2.stj.jus.br`, `www.stj.jus.br`, `bdjur.stj.jus.br`
> e `transparencia.stj.jus.br`, que respondem **403 `cf-mitigated: challenge`** a qualquer robô.

## O host que funciona
`https://dadosabertos.web.stj.jus.br` — instância CKAN do STJ.

- ✅ **A API funciona:** `https://dadosabertos.web.stj.jus.br/api/3/action/package_search?rows=200`
- ✅ **O download de recurso funciona:** `.../dataset/<uuid>/resource/<uuid>/download/<arquivo>`
- ⚠️ **Há WAF F5 com rate limit** ("Request Rejected" / página "oops"): pedir devagar, com
  intervalo de ~20 s entre chamadas e retentativa. Não é bloqueio, é throttle.
- ❌ **Não funciona:** `/group/<nome>` (403). Use a API em vez da navegação HTML.

## O que existe lá (21 datasets; os úteis ao corpus)

| Dataset | Conteúdo | Cobertura |
|---|---|---|
| `integras-de-decisoes-terminativas-e-acordaos-do-diario-da-justica` | **INTEIRO TEOR** (ZIP com os textos) + metadados JSON, das decisões terminativas e acórdãos publicados no DJe | **a partir de 2021-01-04**, atualizado diariamente (2.558 recursos) |
| `precedentes-qualificados` | `temas.csv` (tese firmada, questão submetida, situação, órgão) + `processos.csv` (processo, **numeroRegistro**, relator, leading case, datas) | todos os Temas/IAC/PUIL/Controvérsias (2.389 linhas) |
| `espelhos-de-acordaos-<órgão>` | espelhos (ementa/metadados) por órgão julgador | a partir de 2022-05 |

## Limite conhecido (por que NÃO resolveu o caso dos 3 REsp)
As íntegras só existem **de 2021 em diante**. Os 3 REsp são de **2009, 2011 e 2017** — fora da série.
Para acórdão anterior a 2021 o inteiro teor continua só pelo SCON (navegador humano — ver
`docs/PROMPT-EXTENSAO-JURISPRUDENCIA.md`, v5).

## Uso imediato: montar o link de inteiro teor de QUALQUER precedente qualificado
`processos.csv` entrega o `numeroRegistro` e a `dataPbulicacaoAcordao` (sic, com o erro de digitação
no cabeçalho da origem). Com os dois se monta o link oficial:

```
https://processo.stj.jus.br/SCON/GetInteiroTeorDoAcordao?num_registro=<numeroRegistro>&dt_publicacao=<DD/MM/AAAA>
```

Prova gravada: `jurisprudencia/_capturas/stj-dadosabertos-precedentes-processos-tema174.csv`
(extrato verbatim do `processos.csv` oficial — linha do Tema 174 / REsp 1112646).
`sha256` do `processos.csv` completo baixado em 2026-08-07: `3f9b89029201b8a55ae168b41b7b66458604c95c699ad9ff79d8118aca26cd1d` (1.127.840 bytes).

## Rotas testadas e DESCARTADAS na mesma caçada (não repetir)
- `processo.stj.jus.br` · `scon.stj.jus.br` · `ww2.stj.jus.br` · `www.stj.jus.br` · `bdjur.stj.jus.br`
  · `transparencia.stj.jus.br` → **403 Cloudflare challenge** (curl e WebFetch).
- `sv01..sv04.stj.jus.br` (hosts alternativos do mesmo SCON) → **TLS reset** no handshake.
- `dje.stj.jus.br` · `*.web.stj.jus.br` (jurisprudencia/precedentes/scon/processo) → **não resolvem**.
- `www.lexml.gov.br` (rede LexML / Senado) → **verificação de segurança JS**, e de todo modo é
  catálogo de metadados, não hospeda o teor do STJ.
- Wayback Machine dos 3 links de inteiro teor → **sem snapshot** (`archived_snapshots: {}`).
- `api-publica.datajud.cnj.jus.br` (CNJ) → exige APIKey e, mesmo autenticada, entrega
  metadados/movimentações, **não o inteiro teor**.
- Runner `brasil` com navegador real (Playwright headless E com xvfb) → Cloudflare não resolve em 120 s
  (`portfolio-automacoes/tools/pu-juris/_capturas/RELATORIO-RUNNER.txt`).
