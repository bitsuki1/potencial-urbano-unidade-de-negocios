# caixa-de-entrada/ — o que CHEGA ao Potencial Urbano (caixas v2, PROTOCOLO-DE-CAIXAS §1)
> **Vigência:** ATIVO desde 2026-06-27 (bootstrap §5.5.6). SÓ o **escritório** escreve aqui (no sync). O projeto **LÊ e aplica**.

## Conteúdo
- `do-escritorio/` — diretrizes do Escritório do MOU (canal D44). _(SSOT histórico das diretrizes ainda é `DO_ESCRITORIO.md` na raiz até o v2 operacionalizar.)_
- `de-<projeto>/` — recados de outra unidade, carregados pelo sync do escritório.
- `processados/` — o que esta unidade já aplicou (rastro). **Não apague.**

## Regra de pickup (§4)
- O boot **surfaça** os recados não-lidos (hook `surface-backlog.sh`).
- Ao aplicar um recado, **MOVA-o** para `processados/`.
- O `gate-fechamento.sh` **FALHA** se sobrar recado não-aplicado (fora de `processados/`) ao fechar.
