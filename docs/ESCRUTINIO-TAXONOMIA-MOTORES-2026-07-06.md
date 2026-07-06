# ESCRUTÍNIO ADVERSARIAL — Taxonomia dos motores (D-DONO-14/15/16)
> PU 18 · 2026-07-06. Loop de lentes adversariais (workflow `escrutinio-taxonomia-motores`): 1 lente
> estrategista do próprio loop + 6 lentes adversariais + verificação adversarial de cada achado material
> + síntese. **36 agentes, 0 erros.** Método espelha `docs/ESCRUTINIO-CONJUNTO-MOTORES.md`.
> **Não é oráculo** (regra do próprio loop): é LENTE sobre os 3 papéis canônicos (git · MANIFESTO.json ·
> BACKLOG.md), não uma 4ª fonte-de-verdade.
>
> **Contagem:** 33 achados levantados · 28 materiais · **20 sobreviveram à verificação adversarial**.

## Veredito
**A taxonomia SOBREVIVE?** SIM — como **mapa de valor**, COM AJUSTES. NÃO ganha o selo "triplo-limpo" como estava.

Separando os dois vereditos que o estrategista exige:
- **NOME** — a moldura nomeia certo (alicerce/selo/4 motores) e comunica melhor que as versões anteriores. O **Corte 1 (ontologia) passa** desde que a topologia seja corrigida.
- **COSTURA** — a cadeia **NÃO flui 1:1 no código**: os 4 motores são **lentes conceituais sobre um pipeline compartilhado** (`zepec/` + `engines/`), não 4 módulos particionados. Dívida de costura CONFIRMADA em arquivo: `enriquecer_oficial.py` cavalga Fórmulas+Comercial (o preço LEGAL nasce em `:120/:136`, dentro do arquivo rotulado Comercial); as travas legais moram embutidas no Chão (`montar_base.py` Art.124§2/Art.129) e no Comercial (`montar_ferramenta.py` VEDADO_LEI), não numa caixa "Lei" a montante; o acervo (RAG) **não está cabeado** ao pipeline (grep zero); o Motor do Mapa alimenta o preço **fora do selo** (sem eval de zona; `overlay_zona.py` aponta `/tmp` morto); o elo Fórmulas→Comercial é **parcial** (só o preço do dossiê depende de Fórmulas — a fila/qualificação já roda sem elas).
- **DOUTRINA+ESCOPO** — dois furos reais: **vigência** (1.6 inviolável) não é nomeada no Selo; e um **vazamento de rótulo de demanda** (`FUNDURB (liquidez)`) num deliverable que D-DONO-15 declarou seller-only.

**Conclusão honesta:** "triplo-limpo" não estava provado. A taxonomia é leitura de VALOR válida, não afirmação de que a corrente flui em código. Com os ajustes abaixo (todos texto/rótulo — nenhum reabre o SE) mais o resíduo declarado, ela fica coerente e serve de mapa. Sem eles, o selo verde ao nome mascararia a costura quebrada — o "declarei ≠ provei" em nível de arquitetura.

## Mudanças (aplicadas 2026-07-06 — todas edição de doc/rótulo; nenhuma reabre o SE / D-DONO-8)
1. **[media] Topologia: aresta falsa Lei→Mapa.** A corrente é **{Lei + Mapa} → Fórmulas → Comercial** (Lei e Mapa em paralelo, convergindo em Fórmulas — só as Fórmulas dependem de Lei+Mapa). Corrigido no ROADMAP e na página. Geocodificar/achar zona não usa a saída das travas legais; a página entrega a decisão de ORDEM ao dono, então a aresta inventada distorcia o sequenciamento.
2. **[media] `enriquecer_oficial.py` é JUNTA, não Comercial puro.** Declarado em D-DONO-16: ele CAVALGA Fórmulas+Comercial — invoca o engine (`engines/tdc/pcpt.py:120`) e materializa o preço legal por linha (`:136` saldo×V) [Fórmulas] E empacota dossiê/saldo/pendência [Comercial]. Não dividir o arquivo.
3. **[media] Motor da Lei: rótulo PENDENTE (alvo, não as-built).** (a) acervo/RAG = corpo real mas **standalone, não cabeado** ao pipeline (grep zero em `zepec/`); (b) travas = gates embutidos em Chão (`montar_base.py`) e Comercial (`montar_ferramenta.py`) com citação hardcoded; a trava T8 (veredito citado a partir do acervo) **não existe** (backlog). Marcado como ALVO.
4. **[media] Vazamento de rótulo de demanda.** `zepec/pipeline/gerar_xlsx.py`: coluna `FUNDURB (liquidez)` → **`Status FUNDURB do cedente`** e tooltip reescrito (removido "liquidez"/"janela de mercado"). O dado é seller-side legítimo; só o RÓTULO vazava demanda (viola D-DONO-15). **Regressão de rótulo, não de número.**
5. **[media] Enumeração do `zepec/` fechada em D-DONO-16.** Os 3 scripts exatos (`montar_ferramenta.py`, `enriquecer_oficial.py`, `lista_prospeccao.py`) + `montar_base.py` (computa `cessao_vedada_art124p2`, a vedação Art.124§2). `liquidez.py` e a agregação-janela de `fundurb.py` ficam **FORA** do Motor Comercial (demanda fora de escopo).
6. **[media] "Pronto/abordável" = 2 pernas, não 3.** Hoje = **apto (negociável) + saldo/estado_venda**. O "preço legal" é perna **PENDENTE** (preço oficialmente PARADO; `art128.py` inexistente). Removida a afirmação de que o pipeline já produz a lista "com preço".
7. **[media] Vacina do D-DONO-14 reescrita.** Não é "Comercial antes das Fórmulas (não dá)" — é "não dá o **dossiê-com-preço** antes das Fórmulas; a originação/qualificação/fila do Comercial depende de Lei+dados, não das Fórmulas" (a fila já sai sem tocar preço — `lista_prospeccao.py`).
8. **[media] Vigência no Selo.** "citação + rótulo + teste" → **"citação + rótulo + VIGÊNCIA + teste"** (1.6 é inviolável, gêmea da citação; estava só funcional no RAG/schema).
9. **[media] Motor do Mapa é o único elo AINDA fora do selo.** Sem eval de zona (grep 0 em `evals/` e `consolidar.yml`); `overlay_zona.py:8` aponta `/tmp` morto (não reproduz). Backlog: eval zona→CAbás no gate + runner parametrizado.
10. **[baixa] Naming.** O SSOT chamava o alicerce de "Motor dos Dados" (um leigo conta 5 motores) → **"a Esteira de Dados (o Chão)"**.
11. **[baixa] Alicerce on-path × off-path.** O número in-scope NÃO toca Postgres (`enriquecer_oficial.py` lê CSVs planos). A reconciliação do banco (off-path) NÃO gateia a entrega de valor; "começa pelo chão" = arrumar a esteira CSV, não reconciliar o banco antes do valor.

## Resíduo declarado (em aberto, com dono + marco — não fingir triplo-limpo)
- **COSTURA QUEBRADA:** a corrente não flui 1:1 no código (`enriquecer_oficial.py` cross-cut; RAG não cabeado; travas espalhadas; T8 não construída). Dono = loop do Motor 1 (Lei) + eng. Marco = T8 + wire `enriquecer/montar → consultar`. Registrado como S1–S5 do escrutínio conjunto.
- **MOTOR DO MAPA FORA DO SELO:** sem eval de zona; `overlay_zona.py` não reproduz. Dono = loop Motor 3. Marco = eval zona→CAbás + runner parametrizado.
- **PREÇO PARADO:** a perna "preço legal" fica PENDENTE (`art128.py` inexistente; preço oficialmente parado). Reabrir só por decisão do dono.
- **QUARENTENA ASSIMÉTRICA DO RECEPTOR:** `oodc.py` (engine do receptor, Art.128) segue vivo dentro de "Fórmulas" enquanto o schema-receptor-SQL foi parkado. É retenção para o preço-legal Art.128 **do cedente**, NÃO reintrodução do receptor (não viola D-DONO-15).
- **VIGÊNCIA (1.6)** hoje só funcional (RAG filtro temporal + schema), portadora nominal ausente até o fix do Selo (feito).
- **ALICERCE:** dissenso latente com o Motor 2 (que elege a canonicidade Postgres como "destrava tudo") — mas o banco está OFF-path do número in-scope hoje.
- **ÂNCORA ERRADA COM AR DE RIGOR (risco realizado):** achados citaram `zepec/gerar_xlsx.py`/`overlay_zona.py` mas os arquivos estão em `zepec/pipeline/`. Linha/conteúdo certos, prefixo errado — corrigido na síntese por releitura. Prova viva de que "path:linha vira teatro se ninguém reler".
- **COMERCIAL "fila priorizada" vs artefato (baixa):** `lista_prospeccao.py` produz SEGMENTAÇÃO factual (estado_venda × tem-dono), não ranking. Alinhar ao tocar o doc, ou construir a priorização antes de reivindicá-la.

## Recomendação para os loops futuros (lente estrategista)
Barra de done de uma TAXONOMIA = triplo-limpo com PROVA apontada (path:linha), não prosa; sobrevive à releitura de um cético. Regras operacionais:
1. **SEPARAR NOME de COSTURA** no veredito — nunca aprovar a corrente porque está bem nomeada enquanto o código não regenera.
2. **NÃO CANONIZAR** a taxonomia como 5ª fonte-de-verdade/oráculo — é LENTE sobre git/MANIFESTO/BACKLOG.
3. **RELER todo path:linha citado** antes de confiar (o miss do prefixo `pipeline/` neste próprio loop prova o risco).
4. **GATE MECÂNICO, não prosa** — antes de afirmar "sob o selo", adicionar eval de zona + gate de dados sobre `zepec/` no CI.
5. **ANTI-SCOPE-CREEP REVERSO** — buracos ontológicos (vigência, `oodc.py`, Tese) declaram-se FORA-DA-MOLDURA, nunca desculpa para recolocar receptor/demanda (D-DONO-15).
6. **DEFERÊNCIA ≠ SILÊNCIO** — a taxonomia foi validada pelo dono (veda re-perguntar o SE), mas apontar incoerência interna é dever.
7. **TODO RESÍDUO com DONO + MARCO.**
