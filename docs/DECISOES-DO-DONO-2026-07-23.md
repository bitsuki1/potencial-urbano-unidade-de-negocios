# Decisões do dono — 2026-07-23 (MOU)

> Lavradas nesta sessão a partir das respostas do MOU ao levantamento de pendências. Registro é doutrina
> ("nada se joga fora"; escopo é do dono, D21). O que ele pediu **não é extra**.

## D-DONO 2026-07-23

**1. Mesclar os dois PRs.** ✅ FEITO nesta sessão: **PU #46** (merge `077bec5`) e **hub #28** (merge
`3c10131`). Ambos entraram na `main`. Loop de vigilância dos PRs **encerrado** (estado terminal atingido).

**2. Front-end de validação — cortes aprovados:**
- **(a) Corte da v1 = OK** como proposto: **Painel · Carteira · Decisões · Assistente · Acessos** na **v1**;
  **Mercado** (comparáveis ITBI) e **Corpus** (busca no RAG bruto) ficam na **v2**.
- **(b) Usuários no começo = SÓ O DONO.** Não entram vendedor/equipe na validação → **LGPD**: sem
  necessidade imediata de mascarar CPF/nome na v1 (o dono vê tudo). Mascaramento entra **quando** o papel
  vendedor/equipe for ligado (fica no desenho, não na v1).
- **(c) Incluir as funções sugeridas:** **disparo por WhatsApp/e-mail (Resend)** · **mapa visual dos
  cedentes** · **painel financeiro**. Entram no escopo do front-end (posicionadas por onda no mapa dos
  motores).

**3. Escopo:**
- **Lado RECEPTOR (comprador): ABRIR** — mas **só trabalhamos nele quando o lado VENDEDOR estiver pronto**.
  Ordem mantida: vendedor-first; receptor fica aberto e priorizado **depois**.
- **IPTU: ABRIR** como frente. Sai de "trilha diferida". O motor de IPTU já está construído e verde; agora é
  frente de produto (sequenciada junto com a migração dos motores).

**4. Jurisprudência (inteiro teor):** o dono **executa a metade que precisa do navegador dele** (extensão) —
prompt entregue nesta sessão. A outra metade (STF + TJSP `cposg`) roda pelo **runner `brasil`** (autônomo).

**5. Janela de concorrência do Drive: LIBERADA** ("pode rodar"). O dono confirmou que a exclusão física do
`90`/`99` terminou → o recatálogo/selo/índice-mestre do Drive pode rodar (leitura + escrita liberadas,
respeitando as proteções D-DONO-4 · DE-PARA-06 · RESGATE · FILA · HOLD).

**6/7/8/9 — "faça também":**
- **6. Decreto ESTADUAL 59.263/2013:** ✅ capturado verbatim da fonte oficial (`al.sp.gov.br`, HTTP 200) →
  `docs/normas-estaduais/decreto-estadual-59263-2013.{md,json}` (sha256 registrado). **Fora do corpus de
  uso** (é estadual/solo contaminado, não IPTU/TDC municipal) — documentado e rastreável, pronto só se o dono
  abrir a frente. Ver `docs/normas-estaduais/README.md`.
- **7. 455 cedentes sem linha de IPTU:** lacuna do **cadastro de IPTU** da Prefeitura (dado externo), não
  buraco nosso. Engine **fail-closed** (não inventa). Preenche sozinho quando o cadastro do imóvel aparecer.
  Sem ação a forçar — registrado como espera de dado.
- **8. Faixas do adicional do IPTU:** questão **jurídica aberta** estruturada em
  `docs/IPTU-ADICIONAL-FAIXAS-QUESTAO-JURIDICA.md` (tese · antítese · vacina). Engine **fail-closed** (expõe
  o fator, não aplica às faixas). Passo para fechar: varrer o verbatim das 4 leis (15.889/16.768/17.719/
  18.330) por cláusula de atualização monetária → decisão citada.
- **9. `data_certidao_iso` dos já-declarados:** só 2 de 615 preenchidos → cobertura do §2º (IPCA) cresce
  sozinha conforme o dado do cliente entra. Plumbing pronto. Sem ação a forçar.

## Próximas execuções (derivadas destas decisões)
- Migração motor-a-motor para o Supabase + front-end v1 (ordem: base/canonicidade → Motor 3 dados →
  Motor 4 junção → Motor 0 → Motor 2 → Motor 1 RAG por último), agora com WhatsApp/e-mail + mapa + financeiro
  no desenho, papel único (dono) na v1.
- Jurisprudência: metade-runner (STF + TJSP `cposg`) dispara autônoma; metade-extensão aguarda o dono.
- Drive: recatálogo/selo pós-exclusão (janela liberada).
- IPTU: abrir como frente; fechar a questão do adicional (item 8) pela varredura de cláusula.
