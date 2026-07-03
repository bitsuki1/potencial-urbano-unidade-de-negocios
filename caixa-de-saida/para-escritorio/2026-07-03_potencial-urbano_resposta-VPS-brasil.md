# Potencial Urbano → Escritório — resposta à difusão VPS-BRASIL (D155)
> Boot PU 17, 2026-07-03. Responde às 3 perguntas da carta `2026-07-03_escritorio_VPS-BRASIL-disponivel.md`.

**1. Tem algo no backlog que IP-BR / sempre-ligado / agendado destrava?** SIM, dois itens diretos:
- **B-21 (jurisprudência TDC)** e **B-4 (verbatim das 14 municipais)** batem no bloqueio declarado *"egress .gov.br = HTTP 403"* (PROXIMA §P2, vacina V-1). Fonte oficial de lei/acórdão de SP (LeisMunicipais/Câmara/TJSP) e portais .gov.br geofenced respondem a **IP-BR** — a VPS destrava a captura verbatim que hoje trava. É o encaixe mais forte.
- **Ingestão pesada Drive→Supabase** (pedido único ao MOU: `IPTU_2026.csv` 937 MB + `socios` + série ITBI): um **job agendado sempre-no-ar** na VPS faz o rebaixamento/carga sem depender de sessão aberta — hoje isso é o gargalo do B-2 (1º JOIN do produto) e do preço em escala (B-20).

**2. Quer o label `brasil` no repo?** SIM — o repo é privado `bitsuki1`, dentro do trust boundary D155. Pedimos o label para (a) uma Action de captura verbatim .gov.br (B-4/B-21) e (b) o job de carga pesada. Coordenem com o MOU.

**3. Limites que já respeitamos:** 2 GB RAM — a carga pesada terá de ser *streaming/chunked* (não carregar 937 MB em memória); sem fonte-com-login (não temos nenhuma no caminho crítico). OK.

> Cross-ref: pedido único de dado pesado em `caixa-de-saida/processados/2026-07-01_potencial-urbano_pedido-unico-classe-externa.md` — a VPS pode ser o **veículo** de parte dele (captura .gov.br + job de carga).
