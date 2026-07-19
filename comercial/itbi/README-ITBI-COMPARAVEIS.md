# ITBI — comparáveis de mercado (2006–2025) para o Comercial

> **Fonte OFICIAL primária** (SF/PMSP — "Guias de ITBI Pagas"), baixada do Drive do MOU via conta de
> serviço e consolidada pela Action `drive-itbi-consolidar` do hub `portfolio-automacoes`. É **dado**
> (transação real), **não entra no RAG de leis** (1.1). Como é fonte oficial de terceiro já publicada,
> **não** é um derivado nosso — serve como dado (não cai no 1.8).

## O que é
`itbi-cedentes-comparaveis.csv` — **toda transação de ITBI nas QUADRAS dos cedentes ZEPEC** (SQ = setor+quadra),
de 2006 a 2025. São as **comparáveis de mercado diretas** da carteira: o que efetivamente foi vendido perto de
cada cedente, com valor declarado + valor venal de referência.

- Colunas: `sql · ano_arquivo · data · natureza · valor_transacao · valor_venal_ref`.
- Cobertura: **9.798 transações · 8.625 imóveis distintos** nas quadras dos cedentes (2006–2025;
  2024 = só FEV/2024 no arquivo de origem).
- Chave `sql`: **canônica de 11 dígitos** (setor3+quadra3+lote4+dv1) — o Excel guardava como número e comia
  os zeros à esquerda; o consolidador re-padroniza (`zfill 11`). Sem isso, a carteira central quase não casava
  (253 → 9.798 ao corrigir).

## Método (auditável)
Mapeamento de colunas por palavra-chave (robusto a 20 anos de drift) + varredura de todas as abas (resgata anos
cuja 1ª aba é capa/resumo, ex.: 2024). Relatório de prova por arquivo em `itbi-consolidar-relatorio.md`.

## O que fica FORA daqui (por tamanho / camada)
- **`itbi-por-sql-resumo.csv`** (137.026 SQLs citywide, 6,4 MB) e o **cru de ~500 MB** ficam **no hub**
  (`portfolio-automacoes/tools/drive/out/`) — são **candidatos ao Supabase** (a "vitrine", Fase 3), grandes
  demais para o git de produto. Aqui no PU fica só o recorte útil ao Comercial.

## Uso
Base de comparáveis para **Comercial** (prospecção/negociação) e insumo de calibração para **Tec & Dados**
(sempre rastreável ao registro — o preço LEGAL continua saindo do engine, 1.3; o ITBI é referência de mercado,
não fonte do preço legal).
