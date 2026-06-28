# Handoff — frente comercial TDC (instância PU 14, 2026-06-28)
> O que foi construído na sessão comercial e o que fica aberto. Estado vive no git; isto é o índice.

## O que existe agora (comercial)
- **Base unificada:** `zepec/limpo/zepec_unificada.csv` (7.175 linhas; 4 fontes ZEPEC com tag, SQL_MESTRE/endereço/datas padronizados).
- **A FERRAMENTA:** `zepec/ferramenta/zepec_cedentes.csv` — **6.131 imóveis, 1 linha cada**, com: `estado_venda` (6 estados) · `certeza` · `negociavel` (só com prova) · `proprietario` · `m2_ja_transferido` · `valor_pecuniario_rs`/`status_fundurb`/`intercorrencia_fundurb`. Programa: `zepec/montar_ferramenta.py`.
- **3 codexes separados:** `CODEX-COMERCIAL-TDC.md` (foco) · `CODEX-CALCULOS-TDC.md` (engines) · `CODEX-PRECIFICACAO-TDC.md` (R$, **PARADO**).
- **Engine cedente:** `engines/tdc/pcpt.py` (2 vias — sem doação Art.125 / com doação Art.126-127; auto-teste verde).
- **Fontes externas verbatim no git:** `zepec/raw/externo/` (ANUAL-2022, SISSEL-2024, OODC-2024-2025 → donos; FUNDURB fila → status/intercorrência). `tabelas/quadro7-parques.csv` (272 parques, 147 propostos) + `tabelas/fi-incentivo-doacao.csv`.
- **Inteligência comercial garimpada** (Codex Comercial Parte 5): 6 vias de negócio, contrato OPIT-SP/Bairro Vivo, sensor de liquidez, score geográfico, timing 2026.

## Disciplina aplicada
- **Triplo limpo por agentes:** cada trabalho passou por lentes de escrutínio adversarial; bugs silenciosos corrigidos (multi-lote SQL, dono OODC `/`, sensor de liquidez invertido, completude Quadro 7). Registro: `zepec/AUDITORIA-AGENTES-2026-06-28.md`.
- **Só fato, sem preço, sem inventar.** Onde a semântica é incerta (liquidez FUNDURB), o sistema diz **INDETERMINADO**, não chuta.

## Aberto (próxima instância / MOU)
1. **Dono + Atc em escala → Supabase** (ITBI 45 anos + IPTU 937 MB). Pesado/infra (rclone Drive→Supabase). Destrava cobertura de dono (hoje 79) e o **engine de preço**.
2. **Engine de preço** (Codex Precificação, PARADO): Art.128 + V por data + IPCA. Só quando despausar.
3. **Resolver SQL dos 1.791 sem cadastro** (geo, por endereço).
4. **Confirmar semântica FUNDURB** (teto 5% vs arrecadação; somatória rolante vs all-time) na fonte SMUL → destrava o sensor de liquidez.
5. **Vias de expansão 2-6** (ZEPAM, ZEIS/HIS, parques, corredores) — substrato de parques já extraído.

## Mapa completo: `zepec/MAPA-DE-TOPICOS.md` · Resoluções: `CODEX-COMERCIAL-TDC.md` (R1-R18, realocadas para os 3 codexes).
