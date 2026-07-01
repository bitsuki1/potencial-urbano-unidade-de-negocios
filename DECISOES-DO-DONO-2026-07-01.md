# DECISÕES DO DONO (MOU) — 2026-07-01

> Decisões tomadas pelo dono da unidade (contato@bitsuki.com.br) na sessão PU 15, lente loop de IA.
> Registradas aqui para não caírem (princípio D83 — "decisão que não é escrita, cai").
> Cada uma destrava trabalho; o estado de execução vive no `BACKLOG.md`.

| # | Decisão | Efeito | Destrava |
|---|---|---|---|
| **D-DONO-1** | **DESPAUSAR o preço (R$).** | O cálculo em reais volta ao escopo. Engine de preço (PDE Art. 128 + IPCA) a construir. | Codex Precificação (des-parkado); depende de V (Quadro 14) + Atc (IPTU) para valor real. |
| **D-DONO-2** | **PERMITIR embeddings / camada semântica.** | **Revisa a doutrina D-05** (que exigia RAG 100% determinístico, sem embeddings). A camada semântica passa a ser permitida para resolver a armadilha lexical. | B-5 (camada semântica) + B-6 (grafo de remissões). Depende de um provedor de embeddings (chave de API ou modelo local). |
| **D-DONO-3** | **AUTORIZAR o Produto B** (lista de receptores / OODC) ao `main`. | O merge da branch `project-audit-roadmap-2thi1g` ao `main` fica autorizado pelo dono. | B-17. Falta o mecanismo (PR + resolver conflito leis 16.050/17.844 → aceitar verbatim; clique final no main protegido). |
| **D-DONO-4** | **SÓ FONTES OFICIAIS.** NÃO usar nenhuma planilha DERIVADA/produzida internamente (não são confiáveis): descartar `MEGA_PLANILHA_*`, `PLANILHA_ENRIQUECIDA_*`, todos os `*_IA.csv`, `socios.csv`/`empresas.csv`/`holdings.csv` (todos marcados "derivado" no inventário §12). Reforça a doutrina de oficialidade (fonte oficial = PMSP/SMUL/GeoSampa/PDE/SIRGAS; derivado = pista, não fonte). | O produto passa a ser montado SÓ sobre fonte oficial (IPTU_2026, série ITBI, OODC oficial, SISSEL, alvarás ANUAL, Quadro 14 oficial, benstombados/ZEPEC, zoneamento GeoSampa). Owner em escala vem só das bases oficiais de PROCESSO (cobertura parcial do universo, mas 100% rastreável). | — |
| **D-DONO-4b** | **LGPD: não é preocupação.** | Some do caminho crítico (e, de todo modo, as bases com PII — `socios`/`empresas` — já saem por serem derivadas, D-DONO-4). | — |

## Consequências no BACKLOG
- **B-5 / B-6:** deixam de estar "roteados para decisão de doutrina" → **destravados** por D-DONO-2 (falta o provedor de embeddings).
- **B-17:** deixa de ser "aguarda decisão do MOU" → **autorizado** por D-DONO-3 (falta executar o merge).
- **Preço:** o `CODEX-PRECIFICACAO-TDC.md` sai de PARADO por D-DONO-1 (falta V/Atc do dado pesado).

## O que ainda depende do dono (físico/acesso) — ver o passo-a-passo entregue na sessão
1. Subir o **dado pesado** (IPTU/ITBI/geo/Quadro 14 completo) do Drive → Supabase Storage (o Claude não toca o Drive — cerca).
2. **Provedor de embeddings:** chave de API (Voyage/OpenAI) **ou** aprovar modelo local.
3. **LGPD do `socios`** (dado pessoal): subir com RLS restrito, ou deixar fora por ora.
4. **Merge do Produto B:** aprovar o PR / liberar o main protegido.
5. **SMUL:** confirmar a semântica do FUNDURB (teto 5%).
