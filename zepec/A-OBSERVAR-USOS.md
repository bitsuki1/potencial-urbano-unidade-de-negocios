# ZEPEC — itens A OBSERVAR e para que servem (venda · precificação · outros)
> PU 14 · 2026-06-28. Agnóstico: os campos são FATO; venda/precificação são usos DOWNSTREAM.
> Doutrina: **número/preço nasce no engine (1.3)**, não aqui; estes campos são INSUMO. Sem ranking, sem "melhor/pior".
> Decisões do MOU confirmadas: grão = **1 linha por SQL** (endereço multi não explode) · sem-tipo **mantido como veio**.

## O mapa dos itens observáveis
| Item (fato) | Onde está | Nº | Serve à VENDA (responde…) | Serve à PRECIFICAÇÃO (insumo do engine) | Outros |
|---|---|---|---|---|---|
| **Saldo / ESGOTADO** | certidões (`N. Declaração Saldo`) | 6 esgotadas | "ainda há potencial a transferir?" (esgotado = nada a vender) | tamanho do estoque remanescente a precificar | priorização do funil |
| **Área cedida (m²)** | certidões | 167 valores | prova de que o imóvel já transacionou | **comparáveis reais de mercado** (R$/m² aplicado a m²) | histórico de mercado |
| **Vínculo declaração↔certidão** | derivado | 49 imóveis | "já está ativo no mercado ou só declarado?" | track-record do cedente | dedup / qualidade |
| **Conservação art.129** (Atestado/Termo) | certidões | tipos vários | condição cumprida = pronto p/ emitir certidão (readiness) | — (gate, não preço) | elegibilidade prática |
| **Situação / Status** | decl + cert | — | estágio no processo (documental/análise) | — | gestão de funil |
| **Categoria + `cessao_vedada` (AUE/APPa)** | tombados | 56 | quem **não pode** ceder (Art.124 §2º) → não prospectar | — (binário elegível) | filtro legal |
| **Esfera (mun/est/fed)** | tombados | 697 est · 72 fed | nº de órgãos = complexidade da negociação | — | due diligence |
| **SQL_MESTRE + endereço** | todos | 5.336 ok | localização p/ abordagem | **chave p/ puxar V (Q14) e Atc → engine** | geo |
| **Data de referência** | todos | 5.084 ISO | recência da classificação | o **V é o vigente na data** (Art.125 §1º III) → data muda o valor | temporal |

## O gap honesto da precificação (D24 — declarar o que falta)
A **lista de declarações não carrega o m² de potencial**. Logo:
- Para um imóvel que **já transferiu** → o m² está nas **certidões** (comparável real).
- Para um imóvel **só declarado / ainda não transferido** → o m² **nasce no engine**: `PCpt = Atc × CAbas × Fi` (**Art. 125**), com `Atc` (área do terreno, do IPTU/cadastro) × `CAbas` (Quadro 3, já temos) × `Fi=1`. O **valor** = `PCpt × V`, com `V` do **Quadro 14** (já temos), na **data de referência**.
- **Conclusão:** estas planilhas dão **quem, onde, em que estado e quanto já se transacionou**; o **preço de uma oferta nova** exige o engine + `Atc` (enriquecimento externo: IPTU/geo). Os Quadros 14 e 3 já estão em mãos.

## Higiene pendente quando formos TOCAR os números (ainda A OBSERVAR)
- **Área (m²):** arredondar ruído de float (`4314.14000003 → 4314.14`); são número-fato.
- **Saldo:** parsear `ESGOTADO` vs saldo remanescente (texto na coluna `N. Declaração Saldo`).
- **Vínculo:** ligar declaração→certidões sucessivas (Art. 131) por `N. Declaração` para somar/consumir saldo.

## Próximo passo possível
1. **Operacionalizar o vínculo+saldo** (interno, sem Drive): ligar declaração↔certidões, marcar esgotado/saldo e os 49 ativos — vira a camada de **estado de venda**.
2. **Ligar o engine de preço** (Art.125): precisa de `Atc` (externo, IPTU/geo) — os outros insumos (V, CAbas) já temos.
