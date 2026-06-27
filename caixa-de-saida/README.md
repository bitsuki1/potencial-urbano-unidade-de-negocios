# caixa-de-saida/ — o que o Potencial Urbano MANDA (caixas v2, PROTOCOLO-DE-CAIXAS §1)
> **Vigência:** ATIVO desde 2026-06-27 (bootstrap §5.5.6). SÓ o projeto escreve aqui. O **sync do escritório** recolhe e carrega.

## Como usar
- `para-escritorio/` — recados/achados/pedidos ao Escritório do MOU.
- `para-<outro-projeto>/` — recados a outra unidade (um por destino; criar a pasta quando houver o 1º cruzamento).
- `processados/` — o que o sync do escritório já carregou (rastro). **Não apague.**

## Regras (invariantes §5)
- Naming ISO: `AAAA-MM-DD_potencial-urbano_assunto.md`. Atribuído (dono+data). **Zero síntese** no conteúdo.
- O projeto **NÃO** monta o escritório e **NÃO** escreve o canônico de ninguém — só esta pasta.
- O carregamento entre repos é EXCLUSIVO do escritório (sessão-escritório-sync). Comunicação assíncrona, pelo documento (D1).
